# isort:skip_file
from .common_solution import Solution, HarmonicSolution, ModalSolution
from .acoustic_harmonic_solution import AcousticHarmonicSolution
from .acoustic_modal_solution import AcousticModalSolution
from .structural_harmonic_solution import StructuralHarmonicSolution
from .structural_modal_solution import StructuralModalSolution

AcousticSolution = AcousticModalSolution | AcousticHarmonicSolution
StructuralSolution = StructuralModalSolution | StructuralHarmonicSolution

__all__ = [
    "Solution",
    "ModalSolution",
    "HarmonicSolution",
    "AcousticSolution",
    "StructuralSolution",
    "StructuralHarmonicSolution",
    "AcousticHarmonicSolution",
    "AcousticModalSolution",
    "StructuralModalSolution",
]
