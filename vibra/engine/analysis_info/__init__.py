from .analysis_id import AnalysisID
from .harmonic_analysis_setup import HarmonicAnalysisSetup
from .harmonic_analysis_setup_frequencies import HarmonicAnalysisSetupFrequencies
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
]
