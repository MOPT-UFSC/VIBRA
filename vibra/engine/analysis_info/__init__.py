from .analysis_enums import AnalysisMethod, AnalysisType, FrequencySpacing, PhysicalDomain
from .analysis_id import AnalysisID
from .harmonic_analysis_setup import HarmonicAnalysisSetup
from .harmonic_analysis_setup_list import HarmonicAnalysisSetupList
from .harmonic_analysis_setup_range import HarmonicAnalysisSetupRange
from .harmonic_analysis_setup_new import HarmonicAnalysisSetupNew
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
    "AnalysisType",
    "PhysicalDomain",
]
