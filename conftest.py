from vibra import PROJECT_DIR
from vibra.engine.model import Model
from vibra.engine.properties.fluid import Fluid

import numpy as np
import pytest


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
def acoustic_model(fluid: Fluid) -> Model:
    path = str(PROJECT_DIR / "data/examples/geometry_files/cylinder.step")
    mesh_setup = dict(minimum_element_size=50, maximum_element_size=50)

    model = Model()
    model.properties._set_property("fluid", fluid, volume=1)
    # Normal surface velocity data
    data_Vn = {
        "real_values": [1],
        "imag_values": [0],
        "nodal_attribution": False,
        "averaged": False,
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

    # Define the analysis frequency setup
    df = 100
    f_min = 100
    f_max = 300
    frequencies = np.arange(f_min, f_max + df, df, dtype=float)
    acoustic_model.process_viscous_thermal_model_properties(frequencies)

    analysis_setup = {
        "analysis_id": 3,
        "f_min": f_min,
        "f_max": f_max,
        "f_step": df,
        "frequencies": frequencies,
    }

    acoustic_model.set_analysis_setup(analysis_setup)

    return acoustic_model
