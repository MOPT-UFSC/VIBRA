from .analysis_id import AnalysisID
from .analysis_enums import AnalysisMethod, AnalysisType, FrequencySpacing, PhysicalDomain
from .harmonic_analysis_setup import HarmonicAnalysisSetup
from .modal_analysis_setup import ModalAnalysisSetup

AnalysisSetup = HarmonicAnalysisSetup | ModalAnalysisSetup


__all__ = [
    "AnalysisID",
    "AnalysisMethod",
    "HarmonicAnalysisSetup",
    "ModalAnalysisSetup",
    "AnalysisSetup",
    "FrequencySpacing",
    "AnalysisType",
    "PhysicalDomain",
]
