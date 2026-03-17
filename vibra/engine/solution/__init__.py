# isort:skip_file
from .acoustic_harmonic_solution import AcousticHarmonicSolution
from .acoustic_modal_solution import AcousticModalSolution
from .structural_harmonic_solution import StructuralHarmonicSolution
from .structural_modal_solution import StructuralModalSolution
from .harmonic_solution import HarmonicSolution

"""
Here I am using multiple type aliases to group similar analysis.
This is very useful to use in type hints and to filter with "isinstance".

I am aware that using Inheritance to do similar stuff, but we have different
ways to group the data, and multiple inheritance is a terrible idea.

Using this syntax similar to Algebraic Data Types (ADT) we can do whatever
group we want, and everything becomes simpler and the type hinting works better.

The downside of this approach is the need to always update the types whenever
a new class is created.
But I do not think many new classes will be created, and in any case we already
need to manually update this file anyway to include the imports.
"""
ModalSolution = AcousticModalSolution | StructuralModalSolution
AcousticSolution = AcousticModalSolution | AcousticHarmonicSolution
StructuralSolution = StructuralModalSolution | StructuralHarmonicSolution
Solution = AcousticHarmonicSolution | AcousticModalSolution | StructuralModalSolution | StructuralHarmonicSolution

__all__ = [
    "Solution",
    "ModalSolution",
    "HarmonicSolution",
    "AcousticSolution",
    "StructuralSolution",
    "AcousticModalSolution",
    "StructuralModalSolution",
]
