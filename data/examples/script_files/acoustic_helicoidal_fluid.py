from pathlib import Path

from vibra import PROJECT_DIR
from vibra.engine.analysis_info import AnalysisID, FrequencySpacing
from vibra.engine.mesher.mesh_setup import MeshSetup
from vibra.engine.project import Project
from vibra.engine.properties.fluid import Fluid
from vibra.interface.viewer_3d.plot_setup import PressureFieldPlotSetupFrequency, PressurePlotType
from vibra.utils.interface_utils import SectionPlane, preview_cache


@preview_cache
def setup() -> Project:
    geometry_path = Path(PROJECT_DIR) / "data/examples/geometry_files/rectangular_expansion_chamber.STEP"

    mesh_setup = MeshSetup(
        minimum_element_size=80,
        maximum_element_size=100,
        element_geometry="tetrahedral",
        element_order="linear",
    )

    fluid = Fluid(
        name="Air std",
        identifier=1,
        fluid_density=1.204263,
        speed_of_sound=343.395034,
        isentropic_exponent=1.401985,
        thermal_conductivity=2.5503e-02,
        specific_heat_Cp=1006.400178,
        dynamic_viscosity=1.8247e-05,
        temperature=293.15,
        pressure=101325,
        molar_mass=28.958601,
        color=(200, 200, 200),
    )

    project = Project()
    project.import_geometry(geometry_path)
    project.generate_mesh(mesh_setup)

    # Assign the fluid to the acoustic volume (the chamber cavity).
    project.model.properties._set_property("fluid", fluid, volume=1)

    # --- Acoustic boundary conditions ---

    # 1. Excitation: unit normal surface velocity at the inlet face.
    data_vn = {
        "real_values": [1.0],
        "imag_values": [0.0],
        "element_integration": False,
    }
    project.model.properties._set_property("surface_velocity", data_vn, surface=12)

    # 2. Anechoic termination: specific impedance equal to the fluid impedance at the outlet.
    data_impedance = {
        "real_values": [fluid.impedance],
        "imag_values": [0.0],
    }
    project.model.properties._set_property("specific_impedance", data_impedance, surface=5)

    # 3. Rigid walls are implied wherever no other condition is set.

    analysis_setup = project.model.get_harmonic_analysis_setup(
        frequency_spacing=FrequencySpacing.EQUALLY_DISTRIBUTED,
        analysis_id=AnalysisID.ACOUSTIC_HARMONIC,
        f_min=20,
        f_max=500,
        f_step=20,
    )

    project.configure_analysis(analysis_setup)
    project.run_analysis()


    return project


project = setup()

section_plane = SectionPlane(
    origin=(0, 0, 0),
    normal=(0, 0, -1),
)

plot_setup = PressureFieldPlotSetupFrequency(
    phase=0.0,
    index=10,
    plot_type=PressurePlotType.ABSOLUTE_VALUES,
    unit="Pa",
)
