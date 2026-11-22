from dataclasses import dataclass


@dataclass
class MemoryMetric:
    initial: float | None = None
    initial_subprocess: float | None = None
    peak: float | None = None
    peak_subprocess: float | None = None
    peak_total: float | None = None
    final: float | None = None
    final_subprocess: float | None = None

    @property
    def peak_increase(self) -> float | None:
        if self.initial is not None and self.peak is not None:
            return self.peak - self.initial

        return None

    @property
    def peak_subprocess_increase(self) -> float | None:
        if self.initial_subprocess is not None and self.peak_subprocess is not None:
            return self.peak_subprocess - self.initial_subprocess
        return None

    @property
    def final_change(self) -> float | None:
        if self.initial is not None and self.final is not None:
            return self.final - self.initial
        return None

    @property
    def final_subprocess_change(self) -> float | None:
        if self.initial_subprocess is not None and self.final_subprocess is not None:
            return self.final_subprocess - self.initial_subprocess
        return None


@dataclass
class MemorySample:
    rss: float | None = None
    rss_subprocess: float | None = None
    uss: float | None = None
    uss_subprocess: float | None = None


@dataclass(frozen=True)
class MemoryRecord:
    elapsed: float
    rss: float | None = None
    rss_subprocess: float | None = None
    uss: float | None = None
    uss_subprocess: float | None = None
