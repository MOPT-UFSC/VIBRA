

import numpy as np
from vibra.engine.assemblers.structural_assembler import StructuralAssembler
from vibra.engine.solvers.harmonic_solver import HarmonicSolver
from vibra.project_files.project_file import ProjectFile


def test_regression_structural_harmonic_solver_solution(datadir, structural_harmonic_analysis):
    assembler = StructuralAssembler(structural_harmonic_analysis)
    assembler.assemble_global_matrices_and_excitations()
    project_file = ProjectFile(str(datadir))
    harmonic_solver = HarmonicSolver(assembler, project_file)

    frequencies = structural_harmonic_analysis.frequencies

    # Solve and store solutions into hdf5 files
    saved_solutions = harmonic_solver.solve_direct()

    assembler = StructuralAssembler(structural_harmonic_analysis)
    assembler.assemble_global_matrices_and_excitations()
    in_memory_harmonic_solver = HarmonicSolver(assembler)

    # # Solve and store solution in memory
    in_memory_solutions = in_memory_harmonic_solver.solve_direct()

    for i, _ in enumerate(frequencies):
        assert np.allclose(saved_solutions[:, i], in_memory_solutions[:, i])


def test_structural_harmonic_modal_solver_solution(structural_harmonic_analysis):
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

    for i, _ in enumerate(frequencies):
        assert np.allclose(direct_solutions[:, i], modal_solutions[:, i])