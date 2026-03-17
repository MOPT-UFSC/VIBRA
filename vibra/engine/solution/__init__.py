# isort:skip_file
from .harmonic_solution import HarmonicSolution
from .modal_solution import ModalSolution

Solution = HarmonicSolution | ModalSolution

__all__ = [
    "Solution",
    "ModalSolution",
    "HarmonicSolution",
]
