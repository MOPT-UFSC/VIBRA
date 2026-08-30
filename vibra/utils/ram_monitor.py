from dataclasses import dataclass
from functools import wraps
import os
from typing import Callable
import psutil
import threading
import time


@dataclass
class MemoryMetric:
    initial: float | None = None
    peak: float | None = None
    final: float | None = None

    @property
    def peak_increase(self) -> float | None:
        if self.initial is not None and self.peak is not None:
            return self.peak - self.initial

    @property
    def final_change(self) -> float | None:
        if self.initial is not None and self.final is not None:
            return self.final - self.initial


class RamMonitor:
    def __init__(self, rss_interval: float = 0.05, uss_interval: float = 0.5, label: str | None = None) -> None:
        if (rss_interval <= 0 or uss_interval <= 0) and rss_interval < uss_interval:
            raise ValueError(f"Interval {rss_interval} or {uss_interval} invalid. Needs to be greater than 0")

        self.__rss_interval = rss_interval
        self.__uss_interval = uss_interval
        self.label = label

        self.rss = MemoryMetric()
        self.uss = MemoryMetric()

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

    def _new_session(self, label: str | None = None):
        return type(self)(rss_interval=self.__rss_interval, uss_interval=self.__uss_interval, label=label)

    def _read_rss_mib(self) -> float | None:
        try:
            return self.process.memory_info().rss / (1024**2)
        except psutil.Error as error:
            if self.monitor_error is None:
                self.monitor_error = error
            return None

    def _read_rss_uss_mib(self) -> tuple[float | None, float | None]:
        try:
            memory = self.process.memory_full_info()
            return memory.rss / (1024**2), memory.uss / (1024**2)
        except psutil.Error as error:
            if self.monitor_error is None:
                self.monitor_error = error
            return None, None

    def _update_peak(self, metric: MemoryMetric, value: float) -> None:
        if metric.peak is None:
            metric.peak = value
        else:
            metric.peak = max(metric.peak, value)

    def _monitor(self, stop_event: threading.Event):
        uss_time_ref = time.monotonic()
        while not stop_event.wait(self.__rss_interval):
            if time.monotonic() - uss_time_ref >= self.__uss_interval:
                rss_mb, uss_mb = self._read_rss_uss_mib()
                if rss_mb is None:
                    rss_mb = self._read_rss_mib()
                if rss_mb is not None:
                    self._update_peak(self.rss, rss_mb)

                if uss_mb is not None:
                    self._update_peak(self.uss, uss_mb)

                uss_time_ref = time.monotonic()
                continue

            if (rss_mb := self._read_rss_mib()) is None:
                return

            self._update_peak(self.rss, rss_mb)

    def start(self):
        if self.monitor_thread is not None and self.monitor_thread.is_alive():
            raise RuntimeError("RAM monitor is already running")

        self.rss = MemoryMetric()
        self.uss = MemoryMetric()

        initial_rss, initial_uss = self._read_rss_uss_mib()
        if initial_rss is None:
            initial_rss = self._read_rss_mib()
        if initial_rss is not None:
            self.rss.peak = self.rss.initial = initial_rss
        if initial_uss is not None:
            self.uss.peak = self.uss.initial = initial_uss
        if initial_rss is None and initial_uss is None:
            return self

        self.monitor_error = None
        self.rss.final = None

        self.stop_event = threading.Event()
        self.monitor_thread = threading.Thread(target=self._monitor, args=(self.stop_event,), daemon=True)
        self.monitor_thread.start()

        return self

    def stop(self):
        if self.monitor_thread is not None:
            self.stop_event.set()
            self.monitor_thread.join()
            self.monitor_thread = None

        final_rss, final_uss = self._read_rss_uss_mib()

        if final_rss is None:
            final_rss = self._read_rss_mib()

        if final_rss is not None:
            self.rss.final = final_rss
            self._update_peak(self.rss, final_rss)

        if final_uss is not None:
            self.uss.final = final_uss
            self._update_peak(self.uss, final_uss)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exception_type, exception, traceback) -> bool:
        self.stop()

        if self.monitor_error is not None:
            print(self.monitor_error)

        print(self.__str__())
        return False

    def __str__(self) -> str:
        def _format_memory(value: float | None) -> str:
            if value is None:
                return "N/A"

            return f"{value:.2f} MiB"

        return f"""
             Measurement: {self.label}
                PID (Parent PID):     {os.getpid()} ({self.process.ppid()})
                Resident memory (RSS):
                    Initial:              {_format_memory(self.rss.initial)}
                    Peak:                 {_format_memory(self.rss.peak)}
                    Peak increase:        {_format_memory(self.rss.peak_increase)}
                    Final:                {_format_memory(self.rss.final)}
                    Final change:         {_format_memory(self.rss.final_change)}
                Unique Set Size memory (USS):
                    Initial:              {_format_memory(self.uss.initial)}
                    Peak:                 {_format_memory(self.uss.peak)}
                    Peak increase:        {_format_memory(self.uss.peak_increase)}
                    Final:                {_format_memory(self.uss.final)}
                    Final change:         {_format_memory(self.uss.final_change)}
                """
