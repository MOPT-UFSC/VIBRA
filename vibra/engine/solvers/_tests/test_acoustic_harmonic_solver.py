import numpy as np

from vibra.engine.assemblers.acoustic_assembler import AcousticAssembler
from vibra.engine.solvers import AcousticHarmonicSolver
from vibra.project_files.project_file import ProjectFile


def test_regression_harmonic_solver_solution(datadir, viscous_thermal_acoustic_model):
    assembler = AcousticAssembler(viscous_thermal_acoustic_model)
    assembler.process_assemble()
    project_file = ProjectFile(str(datadir))
    harmonic_solver = AcousticHarmonicSolver(assembler, project_file)

    frequencies = viscous_thermal_acoustic_model.frequencies

    # Solve and store solutions into hdf5 files
    saved_solutions = harmonic_solver.solve()

    assembler = AcousticAssembler(viscous_thermal_acoustic_model)
    assembler.process_assemble()
    in_memory_harmonic_solver = AcousticHarmonicSolver(assembler)

    # Solve and store solution in memory
    in_memory_solutions = in_memory_harmonic_solver.solve()

    for i, _ in enumerate(frequencies):
        assert np.allclose(saved_solutions[:, i], in_memory_solutions[:, i])
