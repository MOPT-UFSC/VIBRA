from pathlib import Path

import numpy as np

from vibra import PROJECT_DIR
from vibra.engine import solution
from vibra.engine.analysis_info import (
    AnalysisID,
    FrequencySpacing,
    ModalAnalysisSetup,
)
from vibra.engine.project import Project
from vibra.engine.solution.harmonic_solution import HarmonicSolution
from vibra.engine.solution.modal_solution import ModalSolution


def test_write_and_read_mesh_project(fluid, datadir: Path):
    mesh_path = PROJECT_DIR / "data/examples/mesh_files/cavities_60mm_large.nas"
    project_path = datadir / "project.vibra"

    project_a = Project()
    project_a.import_mesh(mesh_path)

    project_a.model.properties._set_property("fluid", fluid, volume=1)
    project_a.model.properties._set_property("fluid", fluid, volume=2)

    project_a.configure_analysis(
        ModalAnalysisSetup(
            analysis_id=AnalysisID.ACOUSTIC_MODAL,
            modes_number=5,
            sigma_factor=0.01,
        ),
    )
    project_a.run_analysis()
    solution_a = project_a.model.solution
    project_a.save_project(project_path)

    project_b = Project().load_project(project_path)
    solution_b = project_b.model.solution
    project_path.unlink()

    assert isinstance(solution_a, ModalSolution)
    assert isinstance(solution_b, ModalSolution)
    assert solution_a.acoustic_modal_shapes is not None
    assert solution_b.acoustic_modal_shapes is not None

    assert np.allclose(
        solution_a.acoustic_modal_shapes,
        solution_b.acoustic_modal_shapes[:],
    )


def test_compare_interface_based_mesh_project():
    project_path = PROJECT_DIR / "validation_files/test_projects/cavities.vibra"
    mesh_path = PROJECT_DIR / "data/examples/mesh_files/cavities_60mm_large.nas"

    project_interface = Project().load_project(project_path)

    project_cli = Project()
    project_cli.import_mesh(mesh_path)
    fluid = project_cli.fluid_library.find_by_name("Hydrogen")
    assert fluid is not None

    # Not great yet =/
    project_cli.model.properties._set_property("fluid", fluid, volume=1)
    project_cli.model.properties._set_property("fluid", fluid, volume=2)
    project_cli.model.properties._set_property("fluid", fluid, surface=1)
    project_cli.model.properties._set_property(
        "acoustic_pressure",
        {
            "real_values": [1],
            "imag_values": [0],
        },
        surface=1,
    )

    # It is not ideal to have two functions setting a single property
    project_cli.model.properties._set_property("degrees_of_freedom_decoupling", data={"volume_to_decouple": 1}, surface=6)
    # project_cli.mesh.cache_mesh_information()
    project_cli.model.process_degrees_of_freedom_decoupling()

    ## Define the analysis frequency setup
    analysis_setup = project_cli.model.get_harmonic_analysis_setup(
        frequency_spacing=FrequencySpacing.EQUALLY_DISTRIBUTED,
        analysis_id=AnalysisID.ACOUSTIC_HARMONIC,
        f_min=200,
        f_max=500,
        f_step=100,
    )

    project_cli.configure_analysis(analysis_setup)
    project_cli.run_analysis()

    solution_a = project_interface.model.solution
    solution_b = project_cli.model.solution

    assert isinstance(solution_a, HarmonicSolution)
    assert isinstance(solution_b, HarmonicSolution)
    assert solution_a.acoustic_solution is not None
    assert solution_b.acoustic_solution is not None

    assert np.allclose(
        solution_a.acoustic_solution[:],
        solution_b.acoustic_solution[:],
    )
