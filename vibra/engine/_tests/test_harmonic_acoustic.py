import pytest

from vibra import PROJECT_DIR, errors
from vibra.engine.analysis_info import (
    AnalysisID,
    FrequencySpacing,
    ModalAnalysisSetup,
)
from vibra.engine.project import Project


def test_harmonic_acoustic():
    mesh_path = PROJECT_DIR / "data/examples/mesh_files/branch_cylinders.msh"
    reference_project = PROJECT_DIR / "validation_files/test_projects/branch_cylinders_harmonic_acoustic.vibra"

    project = Project()
    project.import_mesh(mesh_path)

    with pytest.raises(errors.IncompleteSetupError):
        project.run_analysis()

    with pytest.raises(errors.InvalidModelSetupError):
        # Incompatible AnalysisID and AnalysisSetup

        analysis_setup = ModalAnalysisSetup(
            analysis_id=AnalysisID.ACOUSTIC_MODAL,
            modes_number=10,
            sigma_factor=0.01,
        )

        project.configure_analysis(analysis_setup)
        project.run_analysis()

    ## Define the analysis frequency setup
    analysis_setup = project.model.get_harmonic_analysis_setup(
        frequency_spacing=FrequencySpacing.EQUALLY_DISTRIBUTED,
        analysis_id=AnalysisID.ACOUSTIC_HARMONIC,
        f_min=1000,
        f_max=10000,
        f_step=1000,
    )

    project.configure_analysis(analysis_setup)

    with pytest.raises(errors.InvalidModelSetupError):
        # Fluid not configured
        project.run_analysis()

    fluid = project.fluid_library.find_by_name("Methane")
    assert fluid is not None

    project.model.properties._set_property("fluid", fluid, volume=1)
    project.model.properties._set_property("fluid", fluid, surface=1)
    project.model.properties._set_property("fluid", fluid, surface=2)
    project.model.properties._set_property("fluid", fluid, surface=3)
    project.model.properties._set_property("fluid", fluid, surface=4)
    project.model.properties._set_property("fluid", fluid, surface=5)

    project.model.properties._set_property(
        "surface_velocity",
        {
            "real_values": [1],
            "imag_values": [0],
            "element_integration": True,
        },
        surface=2,
    )

    project.model.properties._set_property(
        "absorption_surface",
        {
            "real_values": [0.2],
            "imag_values": [0],
        },
        surface=3,
    )

    project.model.properties._set_property(
        "specific_impedance",
        {
            "anechoic_termination": True,
            "volume_id": 1,
        },
        surface=5,
    )

    solution = project.run_analysis()
    reference_solution = Project().load_project(reference_project).run_analysis()

    assert solution == reference_solution
