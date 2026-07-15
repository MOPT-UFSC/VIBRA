from dataclasses import dataclass
from enum import StrEnum, auto
from typing import Union

from vibra.utils.struct_enum import StructEnum


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


@dataclass(slots=True)
class NoPlotSetup: ...


@dataclass(slots=True)
class FrequencyDisplacementPlotSetup:
    phase: float
    index: int
    magnification_factor: float
    plot_type: PressurePlotType


@dataclass(slots=True)
class FrequencyPressurePlotSetup:
    phase: float
    index: int
    plot_type: DisplacementPlotType


@dataclass(slots=True)
class TransientPressurePlotSetup:
    frame: int


# Do not forget to add the type here
PlotSetup = Union[
    NoPlotSetup,
    FrequencyDisplacementPlotSetup,
    FrequencyPressurePlotSetup,
    TransientPressurePlotSetup,
]
