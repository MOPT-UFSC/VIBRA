from dataclasses import dataclass
from enum import StrEnum, auto
from typing import Union


class PressurePlotType(StrEnum):
    ABSOLUTE_ANIMATION = auto()
    NON_ABSOLUTE_ANIMATION = auto()
    ABSOLUTE_VALUES = auto()
    REAL_VALUES = auto()
    IMAG_VALUES = auto()


class DisplacementPlotType(StrEnum):
    U_SUM = auto()
    U_X = auto()
    U_Y = auto()
    U_Z = auto()
    V_SUM = auto()
    V_X = auto()
    V_Y = auto()
    V_Z = auto()
    A_SUM = auto()
    A_X = auto()
    A_Y = auto()
    A_Z = auto()


@dataclass(slots=True)
class NoPlotSetup:
    unit: str = "--"


@dataclass(slots=True)
class FrequencyDisplacementPlotSetup:
    phase: float
    index: int
    magnification_factor: float
    plot_type: PressurePlotType
    unit: str = "--"


@dataclass(slots=True)
class FrequencyPressurePlotSetup:
    phase: float
    index: int
    plot_type: DisplacementPlotType
    unit: str = "--"


@dataclass(slots=True)
class TransientPressurePlotSetup:
    time_index: int
    plot_type: PressurePlotType
    unit: str = "--"
    reduced_loop_time: float | None = None


@dataclass(slots=True)
class AllowablePulsationForScrewCompressorsPlotSetup:
    plot_type: PressurePlotType
    unit: str = "--"
    pre_study_analysis: bool = False


# Do not forget to add the type here
PlotSetup = Union[
    NoPlotSetup,
    FrequencyDisplacementPlotSetup,
    FrequencyPressurePlotSetup,
    TransientPressurePlotSetup,
    AllowablePulsationForScrewCompressorsPlotSetup,
]
