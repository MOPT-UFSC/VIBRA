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
        self.peak_ram_usage = 0.0
        self.initial_ram = 0.0
        self.final_ram = 0.0
        self.monitor_error: psutil.Error | None = None

    def __call__(self, func: Callable) -> Callable:
        label = self.label or func.__qualname__
        @wraps(func)
        def wrapper(*args, **kwargs):
            with self._new_session(label=label):
                return func(*args, **kwargs)

        return wrapper

    def _new_session(self, label: str | None = None):
        return type(self)(interval=self.__interval, label=label)

    def _rss_monitor(self, stop_event: threading.Event):
        try:
            while not stop_event.wait(self.__interval):
                rss_mb = self.process.memory_info().rss / (1024 ** 2)
                self.peak_ram_usage = max(self.peak_ram_usage, rss_mb)
        except psutil.Error as e:
            self.monitor_error = e

    def _uss_monitor(self):
        try:
            while not self.stop_event.wait(self.__interval):
                uss_mib = self.process.memory_full_info().uss / (1024 ** 2)
                self.peak_ram_usage = max(self.peak_ram_usage, uss_mib)
        except psutil.Error as e:
            self.monitor_error = e

    def register_initial_ram_usage(self):
        self.peak_ram_usage = self.initial_ram = self.process.memory_info().rss / (1024 ** 2)

    def register_final_ram_usage(self):
        self.final_ram = self.process.memory_info().rss / (1024 ** 2)
        self.peak_ram_usage = max(self.peak_ram_usage, self.final_ram)

    def get_peak_usage(self):
        return self.peak_ram_usage

    def start_rss(self):
        if self.monitor_thread is not None and self.monitor_thread.is_alive():
            raise RuntimeError("RAM monitor is already running")

        self.monitor_error = None
        self.register_initial_ram_usage()
        self.final_ram = 0.0
        self.stop_event = threading.Event()
        self.monitor_thread = threading.Thread(target=self._rss_monitor, args=(self.stop_event,), daemon=True)
        self.monitor_thread.start()

        return self

    def stop_rss(self):
        if self.monitor_thread is None:
            return

        self.stop_event.set()
        self.monitor_thread.join()
        self.monitor_thread = None
        self.register_final_ram_usage()

    def __enter__(self):
        self.start_rss()
        return self

    def __exit__(self, exception_type, exception, traceback):
        self.stop_rss()

        if self.monitor_error is not None:
            print(self.monitor_error)

        print(self.__str__())

    def __str__(self) -> str:
        return f"""
            Resident memory (RSS) measurement: {self.label} 
                PID (Parent PID):     {os.getpid()} ({self.process.ppid()})
                Initial:              {round(self.initial_ram, 2)} MiB
                Peak:                 {round(self.peak_ram_usage, 2)} MiB
                Peak increase:        {round(self.peak_ram_usage - self.initial_ram, 2)} MiB
                Final:                {round(self.final_ram, 2)} MiB
                Final change:         {round(self.final_ram - self.initial_ram, 2)} MiB
                """
