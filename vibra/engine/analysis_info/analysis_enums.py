from enum import StrEnum, auto


class FrequencySpacing(StrEnum):
    USER_DEFINED = "user-defined"
    EQUALLY_DISTRIBUTED = "equally distributed"


class AnalysisMethod(StrEnum):
    DIRECT = auto()
    MODE_SUPERPOSITION = auto()


class AnalysisType(StrEnum):
    MODAL = auto()
    HARMONIC = auto()
    STATIC = auto()
    NO_ANALYSIS_TYPE = ""


class PhysicalDomain(StrEnum):
    ACOUSTIC = auto()
    STRUCTURAL = auto()
    COUPLED = auto()
    NO_PHYSICAL_DOMAIN = ""