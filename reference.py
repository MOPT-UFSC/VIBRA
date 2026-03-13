import numpy as np

from vibra import PROJECT_DIR
from vibra.engine.assemblers.acoustic_assembler import AcousticAssembler
from vibra.engine.model import Model
from vibra.engine.properties.fluid import Fluid
from vibra.engine.properties.material import Material
from vibra.engine.solvers import HarmonicSolver
from vibra.project_files.project_file import ProjectFile

path = str(PROJECT_DIR / "data/examples/geometry_files/cylinder.step")
mesh_setup = {
    "minimum_element_size": 50,
    "maximum_element_size": 50,
    "element_type": "tetrahedral",
    "shape_function": "linear",
}

fluid = Fluid(
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

# Define the analysis frequency setup
df = 100
f_min = 200
f_max = 500
frequencies = np.arange(f_min, f_max + df, df, dtype=float)

analysis_setup = {
    "analysis_id": 3,
    "f_min": f_min,
    "f_max": f_max,
    "f_step": df,
    "frequencies": frequencies,
}

# Normal surface velocity data
data_Vn = {
    "real_values": [1],
    "imag_values": [0],
    "nodal_attribution": False,
    "averaged": False,
}

model = Model()
model.properties._set_property("fluid", fluid, volume=1)
model.properties._set_property("fluid", fluid, surface=4)
model.properties._set_property("surface_velocity", data_Vn, surface=4)
model.set_geometry_path(path)
model.set_length_unit()
model.set_geometry_quality_factor()
model.initialize_mesh()
model.set_mesh_setup(mesh_setup)
model.process_mesh()

acoustic_model = model
acoustic_model.old_set_analysis_setup(analysis_setup)
acoustic_model.process_viscous_thermal_model_properties()

# Direct solver setup and solve
assembler = AcousticAssembler(acoustic_model)
assembler.assemble_global_matrices_and_excitations()
harmonic_solver = HarmonicSolver(assembler)
direct_solutions = harmonic_solver.solve_direct()

# Modal solver setup and solve
assembler = AcousticAssembler(acoustic_model)
assembler.assemble_global_matrices_and_excitations()
modal_harmonic_solver = HarmonicSolver(assembler)
modal_solutions = modal_harmonic_solver.solve_mode_superposition()

for i in range(frequencies.size):
    assert np.allclose(direct_solutions[:, i], modal_solutions[:, i])