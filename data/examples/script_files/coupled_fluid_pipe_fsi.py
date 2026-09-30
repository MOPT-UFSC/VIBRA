from pathlib import Path

from molde.colors import color_names

from vibra import PROJECT_DIR
from vibra.engine.analysis_info import AnalysisID, FrequencySpacing
from vibra.engine.mesher.mesh_setup import MeshSetup
from vibra.engine.project import Project
from vibra.engine.properties.fluid import Fluid
from vibra.engine.properties.material import Material
from vibra.interface.viewer_3d.plot_setup import (
    DisplacementFieldPlotSetupFrequency,
    DisplacementPlotType,
    PressureFieldPlotSetupFrequency,
    PressurePlotType,
)
from vibra.utils.interface_utils import MeshRendererConfig, SectionPlane, VisualizationFilter, preview_cache

GEOMETRY_PATH = Path(PROJECT_DIR) / "data/examples/geometry_files/curved_fluid_and_pipe_fsi_example.STEP"


@preview_cache
def setup_mesh() -> Project:
    """Import the geometry and generate the mesh."""
    mesh_setup = MeshSetup(
        minimum_element_size=10,
        maximum_element_size=30,
        element_geometry="tetrahedral",
        element_order="linear",
    )

    project = Project()
    project.import_geometry(GEOMETRY_PATH)
    project.generate_mesh(mesh_setup)

    return project


project = setup_mesh()

"""Assign properties, configure and run the coupled harmonic analysis."""
material = Material(
    name="Carbon_Steel",
    material_density=7850,
    elasticity_modulus=200e9,
    poisson_ratio=0.3,
    thermal_expansion_coefficient=1.2e-5,
    color=(170, 170, 170),
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
project.model.properties._reset_variables()

# Volume 2: enclosed fluid -> acoustic domain.
project.model.properties._set_property("fluid", fluid, volume=1)

# Volume 1: pipe wall -> structural domain.
project.model.properties._set_property("material", material, volume=2)

# Clamp one end of the pipe.
prescribed_dofs = {
    "element_type": "3d_element",
    "real_values": [0, 0, 0],
    "imag_values": [0, 0, 0],
}
project.model.properties._set_property("prescribed_dof", prescribed_dofs, surface=17)

# Acoustic excitation: unit normal surface velocity on the inlet face.
data_vn = {
    "real_values": [1.0],
    "imag_values": [0.0],
    "element_integration": False,
}
project.model.properties._set_property("surface_velocity", data_vn, surface=12)

analysis_setup = project.model.get_harmonic_analysis_setup(
    frequency_spacing=FrequencySpacing.EQUALLY_DISTRIBUTED,
    analysis_id=AnalysisID.COUPLED_HARMONIC,
    f_min=20,
    f_max=200,
    f_step=20,
)

project.configure_analysis(analysis_setup)

section_plane = SectionPlane(origin=(0, 0, 0), normal=(0, 0, -1))
visualization_filter = VisualizationFilter(points=False, lines=False, faces=True)
