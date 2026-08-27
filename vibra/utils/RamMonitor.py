from functools import wraps
import os
from typing import Callable
import psutil
import threading

class RamMonitor:
    def __init__(self, interval: float = 0.05, label: str | None = None) -> None:
        if interval <= 0:
            raise ValueError(f"Interval {interval} invalid. Needs to be greather than 0")

        self.__interval = interval
        self.label = label

        self.process = psutil.Process()
        self.monitor_thread: threading.Thread | None = None
        self.stop_event = threading.Event()
        self.monitor_error: Exception | None = None

        self.peak_ram_usage: float | None = None
        self.initial_ram: float | None = None
        self.final_ram: float | None = None

    def __call__(self, func: Callable) -> Callable:
        label = self.label or func.__qualname__
        @wraps(func)
        def wrapper(*args, **kwargs):
            with self._new_session(label=label):
                return func(*args, **kwargs)

        return wrapper

    def _new_session(self, label: str | None = None):
        return type(self)(interval=self.__interval, label=label)

    def _read_rss_mib(self) -> float | None:
        try:
            return self.process.memory_info().rss / (1024**2)
        except psutil.Error as error:
            if self.monitor_error is None:
                self.monitor_error = error
            return None

    def _rss_monitor(self, stop_event: threading.Event):
        while not stop_event.wait(self.__interval):
            if (rss_mb := self._read_rss_mib()) is None:
                return

            self.peak_ram_usage = max(self.peak_ram_usage, rss_mb)

    def _uss_monitor(self):
        try:
            while not self.stop_event.wait(self.__interval):
                uss_mib = self.process.memory_full_info().uss / (1024 ** 2)
                self.peak_ram_usage = max(self.peak_ram_usage, uss_mib)
        except psutil.Error as e:
            self.monitor_error = e

    def get_peak_usage(self) -> float | None:
        return self.peak_ram_usage

    def start_rss(self):
        if self.monitor_thread is not None and self.monitor_thread.is_alive():
            raise RuntimeError("RAM monitor is already running")

        if (initial_ram := self._read_rss_mib()) is None:
            return self

        self.peak_ram_usage = self.initial_ram = initial_ram
        self.monitor_error = None
        self.final_ram = -1.0

        self.stop_event = threading.Event()
        self.monitor_thread = threading.Thread(target=self._rss_monitor, args=(self.stop_event,), daemon=True)
        self.monitor_thread.start()

        return self

    def stop_rss(self):
        if self.monitor_thread is not None:
            self.stop_event.set()
            self.monitor_thread.join()
            self.monitor_thread = None

        if (final_ram := self._read_rss_mib()) is not None:
            self.final_ram = final_ram
            if self.peak_ram_usage is not None:
                self.peak_ram_usage = max(self.peak_ram_usage, self.final_ram)

    def __enter__(self):
        self.start_rss()
        return self

    def __exit__(self, exception_type, exception, traceback) -> bool:
        self.stop_rss()

        if self.monitor_error is not None:
            print(self.monitor_error)

        print(self.__str__())
        return False

    def __str__(self) -> str:
        def _format_memory(value: float | None) -> str:
            if value is None:
                return "N/A"

            return f"{value:.2f} MiB"

        peak = None
        if self.initial_ram and self.peak_ram_usage:
            peak = self.peak_ram_usage - self.initial_ram

        final_change = None
        if self.final_ram and self.initial_ram:
            final_change = self.final_ram - self.initial_ram

        return f"""
            Resident memory (RSS) measurement: {self.label} 
                PID (Parent PID):     {os.getpid()} ({self.process.ppid()})
                Initial:              {_format_memory(self.initial_ram)}
                Peak:                 {_format_memory(self.peak_ram_usage)}
                Peak increase:        {_format_memory(peak)}
                Final:                {_format_memory(self.final_ram)}
                Final change:         {_format_memory(final_change)}
                """
