from .analysis_id import AnalysisID
from .harmonic_analysis_setup import AnalysisMethod, FrequencySpacing, HarmonicAnalysisSetup
from .harmonic_analysis_setup_list import HarmonicAnalysisSetupList
from .harmonic_analysis_setup_range import HarmonicAnalysisSetupRange
from .modal_analysis_setup import ModalAnalysisSetup

AnalysisSetup = HarmonicAnalysisSetup | ModalAnalysisSetup


__all__ = [
    "AnalysisID",
    "HarmonicAnalysisSetup",
    "ModalAnalysisSetup",
    "AnalysisSetup",
    "HarmonicAnalysisSetupList",
    "HarmonicAnalysisSetupRange",
    "FrequencySpacing",
    "AnalysisMethod",
]
