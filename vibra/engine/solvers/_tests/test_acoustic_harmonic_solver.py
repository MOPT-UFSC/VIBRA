import numpy as np

from vibra.engine.assemblers.acoustic_assembler import AcousticAssembler
from vibra.engine.solvers import HarmonicSolver
from vibra.project_files.project_file import ProjectFile


def test_regression_acoustic_harmonic_solver_solution(datadir, viscous_thermal_acoustic_model):
    assembler = AcousticAssembler(viscous_thermal_acoustic_model)
    assembler.process_assemble()
    project_file = ProjectFile(str(datadir))
    harmonic_solver = HarmonicSolver(assembler, project_file)

    frequencies = viscous_thermal_acoustic_model.frequencies

    # Solve and store solutions into hdf5 files
    saved_solutions = harmonic_solver.solve_direct()

    assembler = AcousticAssembler(viscous_thermal_acoustic_model)
    assembler.process_assemble()
    in_memory_harmonic_solver = HarmonicSolver(assembler)

    # Solve and store solution in memory
    in_memory_solutions = in_memory_harmonic_solver.solve_direct()

    for i, _ in enumerate(frequencies):
        assert np.allclose(saved_solutions[:, i], in_memory_solutions[:, i])

def test_acoustic_harmonic_modal_solver_solution(acoustic_model):
    # Define the analysis frequency setup
    df = 100
    f_min = 200
    f_max = 500
    frequencies = np.arange(f_min, f_max + df, df, dtype=float)

    analysis_setup = {
        "analysis_id": 3,
        "f_min": f_min,
        "f_max": f_max,
        "f_step": df,
        "frequencies": frequencies,
    }

    acoustic_model.set_analysis_setup(analysis_setup)
    acoustic_model.process_viscous_thermal_model_properties(frequencies)

    # Direct solver setup and solve
    assembler = AcousticAssembler(acoustic_model)
    assembler.process_assemble()
    harmonic_solver = HarmonicSolver(assembler)
    direct_solutions = harmonic_solver.solve_direct()

    # Modal solver setup and solve
    assembler = AcousticAssembler(acoustic_model)
    assembler.process_assemble()
    modal_harmonic_solver = HarmonicSolver(assembler)
    modal_solutions = modal_harmonic_solver.solve_mode_superposition()

    for i in range(frequencies.size):
        assert np.allclose(direct_solutions[:, i], modal_solutions[:, i])
