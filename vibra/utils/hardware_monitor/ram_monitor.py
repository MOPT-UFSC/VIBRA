from functools import wraps
from typing import Callable
import psutil
import threading
import time

from vibra.utils.hardware_monitor.memory_metric import MemoryMetric, MemoryRecord, MemorySample


class RamMonitor:
    _BYTES_PER_MIB = 1024**2

    def __init__(self, rss_interval: float = 0.05, uss_interval: float = 0.5, label: str | None = None) -> None:
        if rss_interval <= 0:
            raise ValueError("rss_interval must be greater than 0")

        if uss_interval <= 0:
            raise ValueError("uss_interval must be greater than 0")

        if uss_interval < rss_interval:
            raise ValueError("uss_interval must be greater than or equal to rss_interval")

        self.__rss_interval = rss_interval
        self.__uss_interval = uss_interval
        self.label = label

        self.rss = MemoryMetric()
        self.uss = MemoryMetric()
        self.vms = MemoryMetric()
        self.ram_record: list[MemoryRecord] = list()
        self._start_time: float | None = None

        self.process = psutil.Process()
        self.monitor_thread: threading.Thread | None = None
        self.stop_event = threading.Event()
        self.monitor_error: Exception | None = None

    def __call__(self, func: Callable) -> Callable:
        label = self.label or func.__qualname__
        @wraps(func)
        def wrapper(*args, **kwargs):
            with self._new_session(label=label):
                return func(*args, **kwargs)

        return wrapper

    def _new_session(self, label: str | None = None) -> "RamMonitor":
        return type(self)(
            rss_interval=self.__rss_interval,
            uss_interval=self.__uss_interval,
            label=label,
        )

    def get_ppid(self) -> int | None:
        try:
            return self.process.ppid()
        except Exception as error:
            if self.monitor_error is None:
                self.monitor_error = error

            return None

    def _read_basic_memory_mib(self) -> MemorySample:
        try:
            memory = self.process.memory_info()
            return MemorySample(
                rss=memory.rss / self._BYTES_PER_MIB,
                vms=memory.vms / self._BYTES_PER_MIB,
            )

        except psutil.Error as error:
            if self.monitor_error is None:
                self.monitor_error = error
            return MemorySample()

    def _read_full_memory_mib(self) -> MemorySample:
        try:
            memory = self.process.memory_full_info()
            return MemorySample(
                rss=memory.rss / self._BYTES_PER_MIB,
                uss=memory.uss / self._BYTES_PER_MIB,
                vms=memory.vms / self._BYTES_PER_MIB,
            )

        except psutil.Error as error:
            if self.monitor_error is None:
                self.monitor_error = error
            return self._read_basic_memory_mib()

    def _record_sample(self, sample: MemorySample) -> None:
        if self._start_time is None:
            return

        self.ram_record.append(
            MemoryRecord(
                elapsed=time.monotonic() - self._start_time,
                rss=sample.rss,
                uss=sample.uss,
                vms=sample.vms,
            )
        )

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

            self._record_sample(sample)
            self._update_peak(self.rss, sample.rss)
            self._update_peak(self.uss, sample.uss)
            self._update_peak(self.vms, sample.vms)

    def start(self) -> "RamMonitor":
        if self.monitor_thread is not None and self.monitor_thread.is_alive():
            raise RuntimeError("RAM monitor is already running")

        self.rss = MemoryMetric()
        self.uss = MemoryMetric()
        self.vms = MemoryMetric()
        self.ram_record = list()
        self._start_time = time.monotonic()

        self.monitor_error = None

        sample = self._read_full_memory_mib()
        self._record_sample(sample)
        if sample.rss is None and sample.uss is None and sample.vms is None:
            return self

        self._update_peak(self.rss, sample.rss)
        self.rss.initial = sample.rss
        self._update_peak(self.uss, sample.uss)
        self.uss.initial = sample.uss
        self._update_peak(self.vms, sample.vms)
        self.vms.initial = sample.vms

        self.stop_event = threading.Event()
        self.monitor_thread = threading.Thread(target=self._monitor, args=(self.stop_event,), daemon=True)
        self.monitor_thread.start()

        return self

    def stop(self) -> None:
        if self.monitor_thread is not None:
            self.stop_event.set()
            self.monitor_thread.join()
            self.monitor_thread = None

        sample = self._read_full_memory_mib()
        self._record_sample(sample)
        self._update_peak(self.rss, sample.rss)
        self.rss.final = sample.rss
        self._update_peak(self.uss, sample.uss)
        self.uss.final = sample.uss
        self._update_peak(self.vms, sample.vms)
        self.vms.final = sample.vms

    def __enter__(self) -> "RamMonitor":
        self.start()
        return self

    def __exit__(self, exception_type, exception, traceback) -> bool:
        self.stop()

        if self.monitor_error is not None:
            print(self.monitor_error)

        print(self)
        return False

    def __str__(self) -> str:
        def _format_memory(value: float | None) -> str:
            if value is None:
                return "N/A"

            return f"{value:.2f} MiB"

        return f"""
             Measurement: {self.label or "unnamed block"}
                PID (Parent PID):     {self.process.pid} ({self.get_ppid()})
                Resident memory (RSS):
                    Initial:              {_format_memory(self.rss.initial)}
                    Peak:                 {_format_memory(self.rss.peak)}
                    Peak increase:        {_format_memory(self.rss.peak_increase)}
                    Final:                {_format_memory(self.rss.final)}
                    Final change:         {_format_memory(self.rss.final_change)}
                Unique Set Size (USS):
                    Initial:              {_format_memory(self.uss.initial)}
                    Peak:                 {_format_memory(self.uss.peak)}
                    Peak increase:        {_format_memory(self.uss.peak_increase)}
                    Final:                {_format_memory(self.uss.final)}
                    Final change:         {_format_memory(self.uss.final_change)}
                VMS (Linux and Windows differ):
                    Initial:              {_format_memory(self.vms.initial)}
                    Peak:                 {_format_memory(self.vms.peak)}
                    Peak increase:        {_format_memory(self.vms.peak_increase)}
                    Final:                {_format_memory(self.vms.final)}
                    Final change:         {_format_memory(self.vms.final_change)}
                """
