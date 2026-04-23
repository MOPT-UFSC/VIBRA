# isort:skip_file
from .harmonic_solution import HarmonicSolution
from .modal_solution import ModalSolution
from .lazy_harmonic_solution import LazyHarmonicSolution

Solution = HarmonicSolution | ModalSolution | LazyHarmonicSolution

__all__ = [
    "Solution",
    "ModalSolution",
    "HarmonicSolution",
    "LazyHarmonicSolution",
]
