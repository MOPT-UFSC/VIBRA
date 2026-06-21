import numpy as np
from typing_extensions import TYPE_CHECKING

from vibra.engine.analysis_info import (
    AnalysisID,
    FrequencySpacing,
)
from vibra.engine.serialization.project_paths import ProjectPaths
from vibra.engine.solution import HarmonicSolution, LazyHarmonicSolution

if TYPE_CHECKING:
    from vibra.engine.model import Model

from vibra.engine.assemblers.acoustic_assembler import AcousticAssembler
from vibra.engine.solvers import HarmonicSolver


def test_regression_acoustic_harmonic_solver_solution(datadir, viscous_thermal_acoustic_model: "Model"):
    assembler = AcousticAssembler(viscous_thermal_acoustic_model)
    assembler.assemble_global_matrices_and_excitations()
    project_paths = ProjectPaths(datadir)
    harmonic_solver = HarmonicSolver(assembler, project_paths)

    frequencies = viscous_thermal_acoustic_model.frequencies

    # Solve and store solutions into hdf5 files
    solution = harmonic_solver.solve_direct()

    assembler = AcousticAssembler(viscous_thermal_acoustic_model)
    assembler.assemble_global_matrices_and_excitations()
    in_memory_harmonic_solver = HarmonicSolver(assembler)

    # Solve and store solution in memory
    in_memory_solution = in_memory_harmonic_solver.solve_direct()

    print(type(solution), type(in_memory_solution))

    assert type(solution) is LazyHarmonicSolution
    assert type(in_memory_solution) is HarmonicSolution

    for i, _ in enumerate(frequencies):
        assert np.allclose(
            solution.nodal_solution[:, i],
            in_memory_solution.nodal_solution[:, i],
        )


def test_acoustic_harmonic_modal_solver_solution(acoustic_model: "Model"):

    ## Define the analysis frequency setup
    analysis_setup = acoustic_model.get_harmonic_analysis_setup(
        frequency_spacing=FrequencySpacing.EQUALLY_DISTRIBUTED,
        analysis_id=AnalysisID.ACOUSTIC_HARMONIC,
        f_min=200,
        f_max=500,
        f_step=100,
    )

    acoustic_model.set_analysis_setup(analysis_setup)
    acoustic_model.process_viscous_thermal_model_properties()

    # Direct solver setup and solve
    assembler = AcousticAssembler(acoustic_model)
    assembler.assemble_global_matrices_and_excitations()
    harmonic_solver = HarmonicSolver(assembler)
    direct_solutions = harmonic_solver.solve_direct()

    # Modal solver setup and solve
    assembler = AcousticAssembler(acoustic_model)
    assembler.assemble_global_matrices_and_excitations()
    modal_harmonic_solver = HarmonicSolver(assembler)
    modal_solutions = modal_harmonic_solver.solve_mode_superposition()

    for i in range(analysis_setup.f_size):
        assert np.allclose(direct_solutions.nodal_solution[:, i], modal_solutions.nodal_solution[:, i])
