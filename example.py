import numpy as np
import pytest

from vibra import PROJECT_DIR
from vibra.engine.analysis_info import AnalysisID, HarmonicAnalysisSetup, ModalAnalysisSetup
from vibra.engine.assemblers.acoustic_assembler import AcousticAssembler
from vibra.engine.mesher.mesh_setup import MeshSetup
from vibra.engine.model import Model
from vibra.engine.new_project import NewProject
from vibra.engine.properties.fluid import Fluid
from vibra.engine.properties.libraries.fluid_library import default_fluid_library
from vibra.engine.properties.material import Material
from vibra.engine.solvers import HarmonicSolver
from vibra.project_files.project_file import ProjectFile

geometry_path = PROJECT_DIR / "data/examples/geometry_files/cylinder.step"

mesh_setup = MeshSetup(
    minimum_element_size=50,
    maximum_element_size=50,
    element_type="tetrahedral",
    shape_function="linear",
)

fluid_library = default_fluid_library()
fluid = fluid_library.find_by_name("Air std")

analysis_setup_a = HarmonicAnalysisSetup(
    f_min=200,
    f_max=500,
    f_step=100,
    analysis_method="direct",
)

analysis_setup_b = HarmonicAnalysisSetup(
    f_min=200,
    f_max=500,
    f_step=100,
    analysis_method="mode_superposition",
)

data_Vn = {
    "real_values": [1],
    "imag_values": [0],
    "nodal_attribution": False,
    "averaged": False,
}

project = NewProject()
project.generate_mesh_from_geometry(geometry_path, mesh_setup)
project.configure_analysis(
    analysis_id=AnalysisID.ACOUSTIC_HARMONIC,
    analysis_setup=analysis_setup_a,
)

project.model.properties._set_property("fluid", fluid, volume=1)
project.model.properties._set_property("fluid", fluid, surface=4)
project.model.properties._set_property("surface_velocity", data_Vn, surface=4)

direct_solutions = project.run_analysis()

project.configure_analysis(
    analysis_id=AnalysisID.ACOUSTIC_HARMONIC,
    analysis_setup=analysis_setup_b,
)
modal_solutions = project.run_analysis()

assert np.allclose(direct_solutions[:], modal_solutions[:])
