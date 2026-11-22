import csv
import threading
import time
from collections import deque
from collections.abc import Callable
from functools import wraps
from pathlib import Path
from typing import Self

import psutil

from vibra.utils.hardware_monitor.memory_metric import MemoryMetric, MemoryRecord, MemorySample


class RamMonitor:
    _BYTES_PER_MIB = 1024**2
    _BYTES_PER_GIB = 1024**3

    def __init__(
        self,
        label: str = "",
        *,
        output_path: str | Path = "",
        term_print: bool = True,
        max_hist_size: int = 10_000,
        rss_interval: float = 0.05,
        uss_interval: float = 0.5,
    ) -> None:
        """
        max_hist_size: set the amount of records it will hold
        output_path: text report destination; empty disables report output.
        History is appended to <report>_history.csv when leaving the context or decorated call.

        Diff peak and Diff final are relative to the initial value.
        Peaks and minima are based on sampled measurements.
        """
        if max_hist_size <= 0:
            raise ValueError("max_hist_size must be greater than 0")

        if rss_interval <= 0:
            raise ValueError("rss_interval must be greater than 0")

        if uss_interval <= 0:
            raise ValueError("uss_interval must be greater than 0")

        if uss_interval < rss_interval:
            raise ValueError("uss_interval must be greater than or equal to rss_interval")

        self.min_available_bytes: int | None = None
        self.min_available_percent: float | None = None

        self.max_hist_size = max_hist_size
        self.__rss_interval = rss_interval
        self.__uss_interval = uss_interval
        self.label = label
        self.output_path = Path(output_path).expanduser().resolve() if output_path else None
        self.term_print = term_print

        self.rss = MemoryMetric()
        self.uss = MemoryMetric()
        self.ram_record: deque[MemoryRecord] = deque(maxlen=self.max_hist_size)
        self._start_time: float | None = None
        self.export_error: OSError | None = None

        self.process = psutil.Process()
        self.monitor_thread: threading.Thread | None = None
        self.stop_event = threading.Event()
        self.monitor_error: Exception | None = None

    def __call__(self, func: Callable) -> Callable:
        label = func.__qualname__ if self.label == "" else self.label

        @wraps(func)
        def wrapper(*args, **kwargs):
            with self._new_session(label=label):
                return func(*args, **kwargs)

        return wrapper

    def _new_session(self, label: str) -> Self:
        return type(self)(
            label=label,
            output_path=self.output_path or "",
            term_print=self.term_print,
            max_hist_size=self.max_hist_size,
            rss_interval=self.__rss_interval,
            uss_interval=self.__uss_interval,
        )

    def get_ppid(self) -> int | None:
        try:
            return self.process.ppid()
        except Exception as error:
            if self.monitor_error is None:
                self.monitor_error = error

            return None

    def _get_processes(self) -> list[psutil.Process] | None:
        try:
            return [self.process, *self.process.children(recursive=True)]
        except psutil.Error as err:
            if self.monitor_error is None:
                self.monitor_error = err
            return None

    def _read_basic_memory_mib(self) -> MemorySample:
        processes = self._get_processes()
        if processes is None:
            return MemorySample()

        rss = 0.0
        rss_subprocess = 0.0
        for proc in processes:
            try:
                mem = proc.memory_info()
            except psutil.NoSuchProcess:
                continue
            except psutil.Error as error:
                if self.monitor_error is None:
                    self.monitor_error = error
                return MemorySample()

            if self.process.pid == proc.pid:
                rss += mem.rss
            else:
                rss_subprocess += mem.rss

        return MemorySample(rss=rss / self._BYTES_PER_MIB, rss_subprocess=rss_subprocess / self._BYTES_PER_MIB)

    def _read_full_memory_mib(self) -> MemorySample:
        processes = self._get_processes()
        if processes is None:
            return MemorySample()

        rss = uss = 0.0
        rss_subprocess = uss_subprocess = 0.0
        uss_complete = True
        for proc in processes:
            try:
                mem = proc.memory_full_info()
                if self.process.pid == proc.pid:
                    uss += mem.uss  # exclusive from full_info
                else:
                    uss_subprocess += mem.uss
            except psutil.NoSuchProcess:
                continue
            except psutil.Error as error:
                if self.monitor_error is None:
                    self.monitor_error = error

                try:
                    mem = proc.memory_info()
                except psutil.NoSuchProcess:
                    continue
                except psutil.Error:
                    return MemorySample()

                uss_complete = False

            if self.process.pid == proc.pid:
                rss += mem.rss
            else:
                rss_subprocess += mem.rss

        return MemorySample(
            rss=rss / self._BYTES_PER_MIB,
            rss_subprocess=rss_subprocess / self._BYTES_PER_MIB,
            uss=uss / self._BYTES_PER_MIB if uss_complete else None,
            uss_subprocess=uss_subprocess / self._BYTES_PER_MIB if uss_complete else None,
        )

    def _record_sample(self, sample: MemorySample) -> None:
        if self._start_time is None:
            return

        if sample.rss is None and sample.uss is None:
            return

        self.ram_record.append(
            MemoryRecord(
                elapsed=time.monotonic() - self._start_time,
                rss=sample.rss,
                rss_subprocess=sample.rss_subprocess,
                uss=sample.uss,
                uss_subprocess=sample.uss_subprocess,
            )
        )

    def _update_available_memory(self):
        try:
            memory = psutil.virtual_memory()

            if memory.total <= 0:
                raise ValueError(f"Could not get memory from psutil: {memory.total}")

            available_bytes = memory.available
            available_percent = 100 * memory.available / memory.total
        except (OSError, psutil.Error, ValueError) as e:
            if self.monitor_error is None:
                self.monitor_error = e
            return

        if self.min_available_bytes is None:
            self.min_available_bytes = available_bytes
        else:
            self.min_available_bytes = min(self.min_available_bytes, available_bytes)

        if self.min_available_percent is None:
            self.min_available_percent = available_percent
        else:
            self.min_available_percent = min(self.min_available_percent, available_percent)

    def _update_peak(self, metric: MemoryMetric, value: float | None, value_subprocess: float | None = None) -> None:
        if value is None:
            return

        if metric.peak is None:
            metric.peak = value
        else:
            metric.peak = max(metric.peak, value)

        if metric.peak_total is None:
            metric.peak_total = metric.peak
        else:
            metric.peak_total = max(metric.peak, metric.peak_total)

        if value_subprocess is None:
            return

        if metric.peak_subprocess is None:
            metric.peak_subprocess = value_subprocess
        else:
            metric.peak_subprocess = max(metric.peak_subprocess, value_subprocess)

        metric.peak_total = max(value + value_subprocess, metric.peak_total)

    def _monitor(self, stop_event: threading.Event) -> None:
        uss_time_ref = time.monotonic()
        while not stop_event.wait(self.__rss_interval):
            if time.monotonic() - uss_time_ref >= self.__uss_interval:
                sample = self._read_full_memory_mib()
                uss_time_ref = time.monotonic()
            else:
                sample = self._read_basic_memory_mib()

            if self.output_path is not None:
                self._record_sample(sample)

            self._update_peak(self.rss, sample.rss, sample.rss_subprocess)
            self._update_peak(self.uss, sample.uss, sample.uss_subprocess)
            self._update_available_memory()

    def start(self) -> Self:
        if self.monitor_thread is not None and self.monitor_thread.is_alive():
            raise RuntimeError("RAM monitor is already running")

        self.export_error = None
        self.min_available_bytes = None
        self.min_available_percent = None

        self.rss = MemoryMetric()
        self.uss = MemoryMetric()
        self.ram_record = deque(maxlen=self.max_hist_size)
        self._start_time = time.monotonic()

        self.monitor_error = None

        sample = self._read_full_memory_mib()
        if self.output_path is not None:
            self._record_sample(sample)

        self._update_peak(self.rss, sample.rss, sample.rss_subprocess)
        self.rss.initial = sample.rss
        self.rss.initial_subprocess = sample.rss_subprocess
        self._update_peak(self.uss,sample.uss,  sample.uss_subprocess)
        self.uss.initial = sample.uss
        self.uss.initial_subprocess = sample.uss_subprocess
        self._update_available_memory()

        self.stop_event = threading.Event()
        self.monitor_thread = threading.Thread(target=self._monitor, args=(self.stop_event,), daemon=True)
        self.monitor_thread.start()

        return self

    def stop(self) -> None:
        if self.monitor_thread is None:
            return

        self.stop_event.set()
        self.monitor_thread.join()
        self.monitor_thread = None

        sample = self._read_full_memory_mib()
        if self.output_path is not None:
            self._record_sample(sample)

        self._update_peak(self.rss, sample.rss, sample.rss_subprocess)
        self.rss.final= sample.rss
        self.rss.final_subprocess = sample.rss_subprocess
        self._update_peak(self.uss, sample.uss, sample.uss_subprocess)
        self.uss.final= sample.uss
        self.uss.final_subprocess = sample.uss_subprocess
        self._update_available_memory()

    def __enter__(self) -> Self:
        self.start()
        return self

    def __exit__(self, exception_type, exception, traceback) -> bool:
        self.stop()

        if self.monitor_error is not None:
            print(self.monitor_error)

        if self.term_print:
            print(self)

        if self.output_path:
            try:
                self.output_path.parent.mkdir(parents=True, exist_ok=True)
                if self.ram_record:
                    self._write_history()
            except OSError as error:
                self.export_error = error
                print(f"Could not save RAM report: {error}")

        return False

    def _write_history(self) -> None:
        if self.output_path is None:
            return

        columns = [
            "root_pid", "elapsed_s", "rss_mib", "uss_mib",
            "rss_subprocess_mib", "uss_subprocess_mib", "rss_total_mib", "uss_total_mib",
        ]
        history_path = self.output_path.with_suffix(".csv")
        if history_path.exists():
            with history_path.open(newline="", encoding="utf-8") as existing:
                if next(csv.reader(existing), None) == columns[:4]:
                    history_path = history_path.with_stem(history_path.stem + "_by_process")

        with history_path.open("a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if file.tell() == 0:
                writer.writerow(columns)
            else:
                writer.writerow(["# SESSION"] + [""] * (len(columns) - 1))

            for record in self.ram_record:
                rss_total = None
                if record.rss is not None and record.rss_subprocess is not None:
                    rss_total = record.rss + record.rss_subprocess

                uss_total = None
                if record.uss is not None and record.uss_subprocess is not None:
                    uss_total = record.uss + record.uss_subprocess

                writer.writerow([
                    self.process.pid, record.elapsed, record.rss, record.uss,
                    record.rss_subprocess, record.uss_subprocess, rss_total, uss_total,
                ])

    def __str__(self) -> str:
        def _format_number(value: float | None, *, signed: bool = False) -> str:
            if value is None:
                return "N/A"

            return f"{value:+.2f}" if signed else f"{value:.2f}"

        table = [f"{'Metric':<6} {'Initial':>12} {'Peak':>12} {'Peak subprocess':>15} {'Peak total':>12} {'Diff peak':>12} {'Final':>12} {'Diff final':>12}"]
        for name, metric in (("RSS", self.rss), ("USS", self.uss)):
            table.append(
                f"{name:<6} "
                f"{_format_number(metric.initial):>12} "
                f"{_format_number(metric.peak):>12} "
                f"{_format_number(metric.peak_subprocess):>15} "
                f"{_format_number(metric.peak_total):>12} "
                f"{_format_number(metric.peak_increase, signed=True):>12} "
                f"{_format_number(metric.final):>12} "
                f"{_format_number(metric.final_change, signed=True):>12}"
            )

        available_memory = "N/A"
        if self.min_available_bytes is not None:
            available_gib = self.min_available_bytes / self._BYTES_PER_GIB
            available_memory = f"{available_gib:.2f} GiB"

        available_percent = "N/A"
        if self.min_available_percent is not None:
            available_percent = f"{self.min_available_percent:.2f}%"

        ppid = self.get_ppid()
        return "\n".join(
            [
                "",
                f"RAM - {self.label or 'unnamed block'} | PID: {self.process.pid} | PPID: {ppid if ppid is not None else 'N/A'}",
                "",
                "Process tree - values in MiB",
                *table,
                "",
                "System - observed minima",
                f"Available RAM: {available_memory} ({available_percent} of total)",
                "",
            ]
        )
