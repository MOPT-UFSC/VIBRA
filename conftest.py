import pytest

from vibra import PROJECT_DIR
from vibra.engine.analysis_info import AnalysisID, FrequencySpacing
from vibra.engine.mesher.mesh_setup import MeshSetup
from vibra.engine.model import Model
from vibra.engine.properties.fluid import Fluid
from vibra.engine.properties.material import Material


@pytest.fixture(scope="module")
def fluid() -> Fluid:
    return Fluid(
        name="Air std",
        identifier=1,
        color=(200, 200, 200),
        pressure=101325,
        temperature=293.15,
        fluid_density=1.204263,
        speed_of_sound=343.395034,
        isentropic_exponent=1.401985,
        thermal_conductivity=2.5503e-02,
        specific_heat_Cp=1006.400178,
        dynamic_viscosity=1.8247e-05,
        molar_mass=28.958601,
    )


@pytest.fixture(scope="module")
def material() -> Material:
    (
        Material(
            name="Carbon_Steel",
            material_density=7850,
            elasticity_modulus=200e9,
            poisson_ratio=0.3,
            thermal_expansion_coefficient=1.2e-5,
            color=[170, 170, 170],  # Light Gray
        ),
    )


@pytest.fixture(scope="module")
def acoustic_model(fluid: Fluid) -> Model:
    path = str(PROJECT_DIR / "data/examples/geometry_files/cylinder.step")
    mesh_setup = MeshSetup(minimum_element_size=50, maximum_element_size=50)

    model = Model()
    model.properties._set_property("fluid", fluid, volume=1)
    # Normal surface velocity data
    data_Vn = {
        "real_values": [1],
        "imag_values": [0],
        "element_integration": True,
    }
    model.properties._set_property("fluid", fluid, surface=4)
    model.properties._set_property("surface_velocity", data_Vn, surface=4)
    model.set_geometry_path(path)
    model.set_length_unit()
    model.set_geometry_quality_factor()
    model.initialize_mesh()
    model.set_mesh_setup(mesh_setup)
    model.process_mesh()

    return model


@pytest.fixture(scope="module")
def viscous_thermal_acoustic_model(acoustic_model: Model) -> Model:
    viscous_thermal_model_data = {
        "formulation": "LRF model",
        "section_type": "Circular duct",
        "diameter": 0.005,
    }
    acoustic_model.set_viscous_thermal_model_data(viscous_thermal_model_data, volume=1)
    analysis_setup = acoustic_model.get_harmonic_analysis_setup(
        analysis_id=AnalysisID.ACOUSTIC_HARMONIC,
        frequency_spacing=FrequencySpacing.EQUALLY_DISTRIBUTED,
        f_min=100,
        f_max=300,
        f_step=100,
    )

    acoustic_model.set_analysis_setup(analysis_setup)
    acoustic_model.process_viscous_thermal_model_properties()

    return acoustic_model


@pytest.fixture(scope="module")
def material() -> Material:
    return Material(
        name="Carbon Steel",
        identifier=1,
        color=(200, 200, 200),
        elasticity_modulus=2e11,
        poisson_ratio=0.3,
        material_density=7850,
        thermal_expansion_coefficient=1.1e-5,
    )


@pytest.fixture(scope="module")
def structural_model(material: Material) -> Model:
    path = path = str(PROJECT_DIR / "data/examples/geometry_files/curve_L_3D.step")
    mesh_setup = MeshSetup(minimum_element_size=50, maximum_element_size=50)

    model = Model()
    model.properties._set_property("material", material, volume=1)

    # Fixed boundary conditions
    data_prescribed_dofs = {
        "element_type": "3d_element",
        "real_values": [0, 0, 0],
        "imag_values": [0, 0, 0],
    }
    model.properties._set_property("prescribed_dof", data_prescribed_dofs, surface=8)

    # Fx load on a surface
    data_load = {
        "element_type": "3d_element",
        "real_values": [1, 0, 0],
        "imag_values": [0, 0, 0],
        "element_integration": False,
        "averaged": True,
    }
    model.properties._set_property("material", material, surface=7)
    model.properties._set_property("nodal_loads", data_load, surface=7)
    model.set_geometry_path(path)
    model.set_length_unit()
    model.set_geometry_quality_factor()
    model.initialize_mesh()
    model.set_mesh_setup(mesh_setup)
    model.process_mesh()

    return model


@pytest.fixture(scope="module")
def structural_harmonic_analysis(structural_model: Model) -> Model:
    analysis_setup = structural_model.get_harmonic_analysis_setup(
        analysis_id=AnalysisID.STRUCTURAL_HARMONIC,
        frequency_spacing=FrequencySpacing.EQUALLY_DISTRIBUTED,
        f_min=100,
        f_max=500,
        f_step=200,
    )

    structural_model.set_analysis_setup(analysis_setup)
    return structural_model
