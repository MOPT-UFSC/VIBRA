from .analysis_id import AnalysisID
from .harmonic_analysis_setup import AnalysisMethod, FrequencySpacing, HarmonicAnalysisSetup
from .harmonic_analysis_setup_frequencies import HarmonicAnalysisSetupList
from .harmonic_analysis_setup_interval import HarmonicAnalysisSetupInterval
from .modal_analysis_setup import ModalAnalysisSetup

AnalysisSetup = HarmonicAnalysisSetup | ModalAnalysisSetup


__all__ = [
    "AnalysisID",
    "HarmonicAnalysisSetup",
    "ModalAnalysisSetup",
    "AnalysisSetup",
    "HarmonicAnalysisSetupFrequencies",
    "HarmonicAnalysisSetupInterval",
    "FrequencySpacing",
    "AnalysisMethod",
]
