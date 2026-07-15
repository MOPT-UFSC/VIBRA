from enum import StrEnum, auto

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


# This is not just nestled classes, it is a StructEnum
class PlotSetup(StructEnum):
    class NoPlotSetup: ...

    class FrequencyDisplacement:
        phase: float
        index: int
        magnification_factor: float
        plot_type: PressurePlotType

    class FrequencyPressure:
        phase: float
        index: int
        plot_type: DisplacementPlotType

    class TransientPressure:
        frame: int
