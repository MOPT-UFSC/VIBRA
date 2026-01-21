import numpy as np

from vibra.engine.analysis_info import AnalysisID, HarmonicAnalysisSetup, ModalAnalysisSetup
from vibra.engine.new_project import NewProject
from vibra.engine.properties.fluid import Fluid
from vibra.engine.properties.libraries.fluid_library import default_fluid_library

data_Vn = {
    "real_values": [1.0],
    "imag_values": [0.0],
    "nodal_attribution": True,
    "averaged": False,
}

fluid_library = default_fluid_library()
fluid = fluid_library.find_by_name("Air std")

analysis_setup = HarmonicAnalysisSetup(
    f_min=200,
    f_max=500,
    f_step=100,
)

project_a = NewProject()
project_a.import_mesh("cavidades_60mm_large.nas")
project_a.current_analysis_id = AnalysisID.ACOUSTIC_HARMONIC

project_a.model.properties._set_property("fluid", fluid, volume=1)
project_a.model.properties._set_property("fluid", fluid, volume=2)
project_a.model.properties._set_property("fluid", fluid, surface=1)  # this should be unecessary
project_a.model.properties._set_property("surface_velocity", data_Vn, surface=1)
project_a.model.new_set_analysis_setup(analysis_setup)
solution_a = project_a.run_analysis()

project_b = NewProject().load_project("acoustic_model.vibra")
solution_b = project_b.run_analysis()
project_b.save_project("acoustic_model_2.vibra")

project_c = NewProject().load_project("acoustic_model_2.vibra")
solution_c = project_c.solver.solution


assert np.allclose(solution_a[:], solution_b[:])
assert np.allclose(solution_a[:], solution_c[:])
