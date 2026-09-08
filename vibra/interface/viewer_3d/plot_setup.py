from dataclasses import dataclass
from enum import IntEnum, StrEnum, auto
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


class StressPlotType(StrEnum):
    ABSOLUTE_ANIMATION = auto()
    NON_ABSOLUTE_ANIMATION = auto()
    ABSOLUTE_VALUES = auto()
    REAL_VALUES = auto()
    IMAG_VALUES = auto()


class StressType(IntEnum):
    NORMAL_STRESS_X = 0
    NORMAL_STRESS_Y = 1
    NORMAL_STRESS_Z = 2
    SHEAR_STRESS_XY = 3
    SHEAR_STRESS_XZ = 4
    SHEAR_STRESS_YZ = 5
    VON_MISSES_STRESS = 6
    TRESCA_STRESS = 7
    MAXIMUM_PRINCIPAL_STRESS_1 = 8
    MAXIMUM_PRINCIPAL_STRESS_2 = 9
    MAXIMUM_PRINCIPAL_STRESS_3 = 10

    def is_normal_or_shear_stress(self):
        return self in [
            StressType.NORMAL_STRESS_X,
            StressType.NORMAL_STRESS_Y,
            StressType.NORMAL_STRESS_Z,
            StressType.SHEAR_STRESS_XY,
            StressType.SHEAR_STRESS_XZ,
            StressType.SHEAR_STRESS_YZ,
        ]

    def is_post_processed_stress(self):
        return self in [
            StressType.VON_MISSES_STRESS,
            StressType.TRESCA_STRESS,
            StressType.MAXIMUM_PRINCIPAL_STRESS_1,
            StressType.MAXIMUM_PRINCIPAL_STRESS_2,
            StressType.MAXIMUM_PRINCIPAL_STRESS_3,
        ]


@dataclass(slots=True)
class NoPlotSetup:
    unit: str = "--"


@dataclass(slots=True)
class DisplacementFieldPlotSetupFrequency:
    phase: float
    index: int
    magnification_factor: float
    plot_type: DisplacementPlotType
    unit: str = "--"
    n_diff: int = 0
    unit_scale_factor: float = 1.0


@dataclass(slots=True)
class StressFieldPlotSetupFrequency:
    phase: float
    index: int
    magnification_factor: float
    stress_type: StressType
    plot_type: StressPlotType
    unit: str = "--"
    n_diff: int = 0
    unit_scale_factor: float = 1.0


@dataclass(slots=True)
class FrequencyPressurePlotSetup:
    phase: float
    index: int
    plot_type: PressurePlotType
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
    penalization_factor: int = 0


# Do not forget to add the type here
PlotSetup = Union[
    NoPlotSetup,
    DisplacementFieldPlotSetupFrequency,
    StressFieldPlotSetupFrequency,
    FrequencyPressurePlotSetup,
    TransientPressurePlotSetup,
    AllowablePulsationForScrewCompressorsPlotSetup,
]

AcousticPlotSetups = Union[
    FrequencyPressurePlotSetup,
    TransientPressurePlotSetup,
    AllowablePulsationForScrewCompressorsPlotSetup,
]

StructuralPlotSetups = Union[
    DisplacementFieldPlotSetupFrequency,
    StressFieldPlotSetupFrequency,
]
