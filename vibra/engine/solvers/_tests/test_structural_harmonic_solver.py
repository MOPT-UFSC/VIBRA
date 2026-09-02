from __future__ import annotations

import numpy as np
from typing_extensions import TYPE_CHECKING

from vibra.engine.assemblers.structural.structural_assembler import StructuralAssembler
from vibra.engine.serialization.project_paths import ProjectPaths
from vibra.engine.solution import HarmonicSolution, LazyHarmonicSolution
from vibra.engine.solvers.harmonic_solver import HarmonicSolver

if TYPE_CHECKING:
    from vibra.engine.model import Model


def test_regression_structural_harmonic_solver_solution(datadir, structural_harmonic_analysis: Model):
    assembler = StructuralAssembler(structural_harmonic_analysis)
    assembler.assemble_global_matrices_and_excitations()

    project_paths = ProjectPaths(datadir)
    harmonic_solver = HarmonicSolver(assembler, project_paths)

    # Solve and store solutions into hdf5 files
    # but returns in-memory data
    in_memory_solution = harmonic_solver.solve_direct()

    # Reads the written data lazily
    lazy_solution = LazyHarmonicSolution(project_paths)

    assert type(lazy_solution) is LazyHarmonicSolution
    assert type(in_memory_solution) is HarmonicSolution

    assert lazy_solution == in_memory_solution


def test_structural_harmonic_modal_solver_solution(structural_harmonic_analysis: Model):
    frequencies = structural_harmonic_analysis.frequencies

    # Direct solver setup and solve
    assembler = StructuralAssembler(structural_harmonic_analysis)
    assembler.assemble_global_matrices_and_excitations()
    harmonic_solver = HarmonicSolver(assembler)
    direct_solutions = harmonic_solver.solve_direct()

    # Modal solver setup and solve
    assembler = StructuralAssembler(structural_harmonic_analysis)
    assembler.assemble_global_matrices_and_excitations()
    modal_harmonic_solver = HarmonicSolver(assembler)
    modal_solutions = modal_harmonic_solver.solve_mode_superposition()

    assert direct_solutions == modal_solutions
