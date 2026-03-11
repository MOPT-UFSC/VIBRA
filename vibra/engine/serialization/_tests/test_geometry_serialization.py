from pathlib import Path

import numpy as np

from vibra import PROJECT_DIR
from vibra.engine.analysis_info import AnalysisID, HarmonicAnalysisSetupRange
from vibra.engine.mesher.mesh_setup import MeshSetup
from vibra.engine.new_project import NewProject


def test_write_and_read_project(fluid):
    geometry_path = PROJECT_DIR / "data/examples/geometry_files/cylinder.step"
    project_path = Path("project.vibra")

    mesh_setup = MeshSetup(
        minimum_element_size=50,
        maximum_element_size=50,
    )

    data_Vn = {
        "real_values": [1.0],
        "imag_values": [0.0],
        "nodal_attribution": True,
        "averaged": False,
    }

    project_a = NewProject()
    project_a.import_geometry(geometry_path)
    project_a.configure_mesh(mesh_setup)
    project_a.generate_mesh()

    project_a.model.properties._set_property("fluid", fluid, volume=1)
    project_a.model.properties._set_property("fluid", fluid, volume=2)
    project_a.model.properties._set_property("fluid", fluid, surface=1)
    project_a.model.properties._set_property("surface_velocity", data_Vn, surface=1)

    project_a.configure_analysis(
        AnalysisID.ACOUSTIC_HARMONIC,
        HarmonicAnalysisSetupRange(
            f_min=100,
            f_max=500,
            f_step=200,
        ),
    )
    project_a.solve_acoustic_harmonic_analysis()
    project_a.save_project(project_path)

    project_b = NewProject()
    project_b.load_project(project_path)

    project_path.unlink()
    assert np.allclose(project_a.solver.solution[:], project_b.solver.solution[:])
