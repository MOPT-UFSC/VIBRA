from enum import IntEnum

class StandardTabType(IntEnum):
    CONSTANT_DATA = 0
    TABULAR_DATA = 1
    LIST = 2

class SetupTabType(IntEnum): 
    SETUP = 0

class AttributionBodiesType(IntEnum):
    ALL_BODIES = 0
    SELECTED_BODIES = 1