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