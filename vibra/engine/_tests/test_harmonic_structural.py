import pytest

from vibra import PROJECT_DIR, errors
from vibra.engine.analysis_info import (
    AnalysisID,
    FrequencySpacing,
    ModalAnalysisSetup,
)
from vibra.engine.project import Project


def test_harmonic_structural():
    mesh_path = PROJECT_DIR / "data/examples/mesh_files/branch_cylinders.msh"
    reference_project = PROJECT_DIR / "validation_files/test_projects/branch_cylinders_harmonic_structural.vibra"

    project = Project()
    project.import_mesh(mesh_path)

    with pytest.raises(errors.IncompleteSetupError):
        project.run_analysis()

    with pytest.raises(errors.InvalidModelSetupError):
        # Incompatible AnalysisID and AnalysisSetup

        analysis_setup = ModalAnalysisSetup(
            analysis_id=AnalysisID.STRUCTURAL_MODAL,
            modes_number=10,
            sigma_factor=0.01,
        )

        project.configure_analysis(analysis_setup)
        project.run_analysis()

    # Define the analysis frequency setup
    analysis_setup = project.model.get_harmonic_analysis_setup(
        analysis_id=AnalysisID.STRUCTURAL_HARMONIC,
        frequency_spacing=FrequencySpacing.EQUALLY_DISTRIBUTED,
        f_min=100,
        f_max=50000,
        f_step=5000,
    )

    project.configure_analysis(analysis_setup)

    with pytest.raises(errors.InvalidModelSetupError):
        # Material not configured
        project.run_analysis()

    material = project.material_library.find_by_name("Ni-Co-Cr_Alloy")
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
        surface=3,
    )

    project.model.properties._set_property(
        "nodal_loads",
        {
            "element_type": "3d_element",
            "real_values": [1, 0, 2],
            "imag_values": [0, 0, 0],
            "nodal_attribution": True,
            "averaged": True,
        },
        surface=5,
    )

    solution = project.run_analysis()
    reference_solution = Project().load_project(reference_project).run_analysis()

    assert solution == reference_solution
