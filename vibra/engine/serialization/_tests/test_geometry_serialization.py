from pathlib import Path

from vibra import PROJECT_DIR
from vibra.engine.analysis_info import AnalysisID, HarmonicAnalysisSetupRange
from vibra.engine.mesher.mesh_setup import MeshSetup
from vibra.engine.project import Project


def test_write_and_read_project(fluid, datadir: Path):
    geometry_path = PROJECT_DIR / "data/examples/geometry_files/cylinder.step"
    project_path = datadir / "project.vibra"

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

    project_a = Project()
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
    solution_a = project_a.solve_acoustic_harmonic_analysis()
    project_a.save_project(project_path)

    project_b = Project()
    project_b.load_project(project_path)
    solution_b = project_b.model.solution

    project_path.unlink()
    assert solution_a == solution_b
