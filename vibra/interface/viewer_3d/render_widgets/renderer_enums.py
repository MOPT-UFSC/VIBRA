from enum import Enum, StrEnum, auto

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


class GeometryRendererMode(Enum):
    EMPTY = auto()
    COLORED = auto()


class MeshRendererMode(StructEnum):
    class Default: ...

    class DisconectedNodes:
        nodes: list

    class CollapsedElementNodes:
        nodes: list


class ResultsRendererMode(StructEnum):
    class NoPlot: ...

    class FrequencyPressure:
        phase: float
        index: int
        plot_type: PressurePlotType

    class FrequencyDisplacement:
        phase: float
        index: int
        magnification_factor: float
        plot_type: DisplacementPlotType

    class StressPlot: ...

    class TransientPlot:
        magnification_factor: float
