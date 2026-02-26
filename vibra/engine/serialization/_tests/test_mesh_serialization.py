from pathlib import Path

import numpy as np

from example import fluid_library
from vibra import PROJECT_DIR
from vibra.engine.analysis_info import AnalysisID, HarmonicAnalysisSetup, ModalAnalysisSetup
from vibra.engine.mesher.mesh_setup import MeshSetup
from vibra.engine.new_project import NewProject
from vibra.engine.properties import FluidLibrary


def test_write_and_read_mesh_project(fluid):
    mesh_path = PROJECT_DIR / "data/examples/mesh_files/cavities_60mm_large.nas"
    project_path = Path("project.vibra")

    project_a = NewProject()
    project_a.import_mesh(mesh_path)

    project_a.model.properties._set_property("fluid", fluid, volume=1)
    project_a.model.properties._set_property("fluid", fluid, volume=2)

    project_a.configure_analysis(
        AnalysisID.ACOUSTIC_MODAL,
        ModalAnalysisSetup(
            modes_number=5,
            sigma_factor=0.01,
        ),
    )
    project_a.run_analysis()
    project_a.save_project(project_path)

    project_b = NewProject()
    project_b.load_project(project_path)

    project_path.unlink()
    assert np.allclose(project_a.solver.solution[:], project_b.solver.solution[:])


def test_compare_interface_based_mesh_project():
    project_path = PROJECT_DIR / "validation_files/test_projects/cavities.vibra"
    project_interface = NewProject().load_project(project_path)

    project_cli = NewProject()
    fluid = project_cli.fluid_library.find_by_name("hydrogen")

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

    assert np.allclose(
        project_interface.solver.solution[:],
        project_cli.solver.solution[:],
    )
