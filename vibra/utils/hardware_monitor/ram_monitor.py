from functools import wraps
from collections import deque
from pathlib import Path
from typing import Callable
import csv
import psutil
import threading
import time

from vibra.utils.hardware_monitor.memory_metric import MemoryMetric, MemoryRecord, MemorySample


class RamMonitor:
    _BYTES_PER_MIB = 1024**2
    _BYTES_PER_GIB = 1024**3

    def __init__(self, label: str = "", *, output_path: str | Path = "", term_print: bool = True, max_hist_size: int = 10_000, rss_interval: float = 0.05, uss_interval: float = 0.5, record_history: bool = False) -> None:
        '''
        max_hist_size: set the amount of records it will hold
        output_path: text report destination; empty disables report output.
        History is appended to <report>_history.csv when leaving the context or decorated call.

        Diff peak and Diff final are relative to the initial value.
        Peaks and minima are based on sampled measurements.
        '''
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
        self.record_history = record_history

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

    def _new_session(self, label: str) -> "RamMonitor":
        return type(self)(
            label=label,
            output_path=self.output_path or "",
            term_print=self.term_print,
            max_hist_size=self.max_hist_size,
            rss_interval=self.__rss_interval,
            uss_interval=self.__uss_interval,
            record_history=self.record_history,
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
        for proc in processes:
            try:
                mem = proc.memory_info()
            except psutil.NoSuchProcess:
                continue
            except psutil.Error as error:
                if self.monitor_error is None:
                    self.monitor_error = error
                return MemorySample()

            rss += mem.rss

        return MemorySample(
            rss=rss / self._BYTES_PER_MIB,
        )

    def _read_full_memory_mib(self) -> MemorySample:
        processes = self._get_processes()
        if processes is None:
            return MemorySample()

        rss = uss = 0.0
        uss_complete = True
        for proc in processes:
            try:
                mem = proc.memory_full_info()
                uss += mem.uss # exclusive from full_info
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

            rss += mem.rss

        return MemorySample(
            rss=rss / self._BYTES_PER_MIB,
            uss=uss / self._BYTES_PER_MIB if uss_complete else None,
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
                uss=sample.uss,
            )
        )

    def _update_available_memory(self):
        try:
            memory = psutil.virtual_memory()

            if memory.total <= 0:
                raise ValueError(f'Could not get memory from psutil: {memory.total}')

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

    def _update_peak(self, metric: MemoryMetric, value: float | None) -> None:
        if value is None:
            return

        if metric.peak is None:
            metric.peak = value
        else:
            metric.peak = max(metric.peak, value)

    def _monitor(self, stop_event: threading.Event) -> None:
        uss_time_ref = time.monotonic()
        while not stop_event.wait(self.__rss_interval):
            if time.monotonic() - uss_time_ref >= self.__uss_interval:
                sample = self._read_full_memory_mib()
                uss_time_ref = time.monotonic()
            else:
                sample = self._read_basic_memory_mib()

            if self.record_history:
                self._record_sample(sample)

            self._update_peak(self.rss, sample.rss)
            self._update_peak(self.uss, sample.uss)
            self._update_available_memory()

    def start(self) -> "RamMonitor":
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
        if self.record_history:
            self._record_sample(sample)

        self._update_peak(self.rss, sample.rss)
        self.rss.initial = sample.rss
        self._update_peak(self.uss, sample.uss)
        self.uss.initial = sample.uss
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
        if self.record_history:
            self._record_sample(sample)

        self._update_peak(self.rss, sample.rss)
        self.rss.final = sample.rss
        self._update_peak(self.uss, sample.uss)
        self.uss.final = sample.uss
        self._update_available_memory()

    def __enter__(self) -> "RamMonitor":
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
                self._write_report()
                if self.ram_record:
                    self._write_history()
            except OSError as error:
                self.export_error = error
                print(f"Could not save RAM report: {error}")

        return False

    def _write_report(self):
        if self.output_path:
            with open(self.output_path, "a", encoding="utf-8") as file:
                file.write(f"{self}\n\n")

    def _write_history(self) -> None:
        if self.output_path is None:
            return

        history_path = self.output_path.with_name(f"{self.output_path.stem}_history.csv")
        with open(history_path, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if file.tell() == 0:
                writer.writerow(["root_pid", "elapsed_s", "rss_mib", "uss_mib"])
            else:
                writer.writerow(["# SESSION", "", "", ""])

            for record in self.ram_record:
                writer.writerow([
                    self.process.pid,
                    record.elapsed,
                    record.rss,
                    record.uss,
                ])

    def __str__(self) -> str:
        def _format_number(value: float | None, *, signed: bool = False) -> str:
            if value is None:
                return "N/A"

            return f"{value:+.2f}" if signed else f"{value:.2f}"

        table = [f"{'Metric':<6} {'Initial':>12} {'Peak':>12} {'Diff peak':>12} {'Final':>12} {'Diff final':>12}"]
        for name, metric in (("RSS", self.rss), ("USS", self.uss)):
            table.append(
                f"{name:<6} "
                f"{_format_number(metric.initial):>12} "
                f"{_format_number(metric.peak):>12} "
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
