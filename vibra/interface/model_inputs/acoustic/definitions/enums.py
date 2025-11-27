from enum import IntEnum

class StandardTabType(IntEnum):
    CONSTANT_DATA = 0
    TABULAR_DATA = 1
    LIST = 2

class SetupTabType(IntEnum): 
    SETUP = 0
    LIST = 1

class AttributionBodiesType(IntEnum):
    ALL_BODIES = 0
    SELECTED_BODIES = 1

class PlotTypesTab(IntEnum):
    FLUID_DENSITY = 0
    SPEED_OF_SOUND = 1
    SURFACE_IMPEDANCE = 2
    ABSORPTION_COEFFICIENT = 3

# Enums used by ReciprocatingCompressorInputs

class RCTabTypes(IntEnum):
    SETUP = SetupTabType.SETUP
    ADVANCED_OPTIONS = 1
    LIST = 2

class ConnectionTypeComboBox(IntEnum):
    SUCTION = 0
    DISCHARGE = 1

class CompressionStageComboBox(IntEnum):
    FIRST_STAGE = 0
    SECOND_STAGE = 1
    THIRD_STAGE = 3

class ActingHeadComboBox(IntEnum):
    HEAD_END = 0
    CRANK_END = 1
    BOTH_ENDS = 2

class FluidDataComboBox(IntEnum):
    REF_PROP = 0
    USER_DEFINED = 1

class PressureUnitComboBox(IntEnum):
    KGF_CM2_A = 0
    BAR_A = 1
    KPA_A = 2
    PA_A = 3
    KGF_CM2_G = 4
    BAR_G = 5
    KPA_G = 6
    PA_G = 7

class TemperatureUnitComboBox(IntEnum):
    KELVIN = 0
    CELSIUS = 1

class OutputDataComboBox(IntEnum):
    SURFACE_VELOCITY = 0
    FLOW_RATE = 1

class InitialFrequencyComboBox(IntEnum):
    _0_DOT_1_HZ = 0
    _0_DOT_2_HZ = 1
    _0_DOT_5_HZ = 2
    _1_DOT_0_HZ = 3
    _2_DOT_0_HZ = 4