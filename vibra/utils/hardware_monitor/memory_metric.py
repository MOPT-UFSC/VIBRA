from dataclasses import dataclass


@dataclass
class MemoryMetric:
    initial: float | None = None
    peak: float | None = None
    final: float | None = None

    @property
    def peak_increase(self) -> float | None:
        if self.initial is not None and self.peak is not None:
            return self.peak - self.initial
        return None

    @property
    def final_change(self) -> float | None:
        if self.initial is not None and self.final is not None:
            return self.final - self.initial
        return None


@dataclass
class MemorySample:
    rss: float | None = None
    uss: float | None = None
    vms: float | None = None
