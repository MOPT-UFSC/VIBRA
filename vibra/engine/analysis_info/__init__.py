from .analysis_id import AnalysisID
from .analysis_enums import AnalysisMethod, AnalysisType, FrequencySpacing, PhysicalDomain
from .harmonic_analysis_setup import HarmonicAnalysisSetup
from .modal_analysis_setup import ModalAnalysisSetup
from .static_analysis_setup import StaticAnalysisSetup

AnalysisSetup = HarmonicAnalysisSetup | ModalAnalysisSetup


__all__ = [
    "AnalysisID",
    "AnalysisMethod",
    "HarmonicAnalysisSetup",
    "ModalAnalysisSetup",
    "StaticAnalysisSetup",
    "AnalysisSetup",
    "FrequencySpacing",
    "AnalysisType",
    "PhysicalDomain",
]
