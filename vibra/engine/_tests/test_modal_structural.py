import numpy as np
import pytest

from vibra import PROJECT_DIR, errors
from vibra.engine.analysis_info import AnalysisID, HarmonicAnalysisSetup, ModalAnalysisSetup
from vibra.engine.project import Project


def test_modal_structural():
    mesh_path = PROJECT_DIR / "data/examples/mesh_files/branch_cylinders.msh"
    reference_project = PROJECT_DIR / "validation_files/test_projects/branch_cylinders_modal_structural.vibra"

    project = Project()
    project.import_mesh(mesh_path)

    with pytest.raises(errors.IncompleteSetupError):
        project.run_analysis()

    with pytest.raises(errors.InvalidModelSetupError):
        # Incompatible AnalysisID and AnalysisSetup
        project.configure_analysis(
            HarmonicAnalysisSetup(
                analysis_id=AnalysisID.STRUCTURAL_MODAL,
                f_min=1,
                f_max=10,
                f_step=1,
            ),
        )
        project.run_analysis()

    analysis_setup = ModalAnalysisSetup(analysis_id=AnalysisID.STRUCTURAL_MODAL, modes_number=10, sigma_factor=0.01)

    project.configure_analysis(
        analysis_setup,
    )

    with pytest.raises(errors.InvalidModelSetupError):
        # Material not configured
        project.run_analysis()

    material = project.material_library.find_by_name("Brass")
    assert material is not None

    project.model.properties._set_property("material", material, volume=1)
    project.model.properties._set_property("material", material, surface=1)
    project.model.properties._set_property("material", material, surface=2)
    project.model.properties._set_property("material", material, surface=3)
    project.model.properties._set_property("material", material, surface=4)
    project.model.properties._set_property("material", material, surface=5)

    project.model.properties._set_property(
        "prescribed_dof",
        {
            "element_type": "3d_element",
            "real_values": [0, 0, 0],
            "imag_values": [0, 0, 0],
        },
        surface=5,
    )

    project.run_analysis()

    reference_project = Project().load_project(reference_project)
    reference_project.run_analysis()

    assert np.allclose(reference_project.assembler.stiffness_matrix.data, project.assembler.stiffness_matrix.data)
    assert np.allclose(reference_project.assembler.mass_matrix.data, project.assembler.mass_matrix.data)
