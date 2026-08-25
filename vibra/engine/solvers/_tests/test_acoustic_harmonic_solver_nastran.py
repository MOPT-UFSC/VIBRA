from os.path import dirname
from pathlib import Path

import numpy as np
import pytest

from vibra import PROJECT_DIR
from vibra.engine.assemblers.acoustic_assembler import AcousticAssembler
from vibra.engine.model import Model
from vibra.engine.properties.fluid import Fluid
from vibra.engine.serialization.project_paths import ProjectPaths
from vibra.engine.solvers import HarmonicSolver
from vibra.interface.user_input.data_handler.file_handlers.file_handler import FileHandler


def _acoustic_model_nastran(path: str, fluid: Fluid) -> Model:

    # mesh_setup = dict(minimum_element_size=50, maximum_element_size=50)

    model = Model()
    model.set_geometry_path(path)
    model.set_length_unit()
    model.set_geometry_quality_factor()
    model.initialize_mesh()
    # model.set_mesh_setup(mesh_setup)
    model.process_mesh_data(path)

    for vol_id in [1, 2]:
        model.properties._set_property("fluid", fluid, volume=vol_id)
        for surf_id in model.mesh.surfaces_from_volume.get(vol_id):
            model.properties._set_property("fluid", fluid, surface=surf_id)

    # # Normal surface velocity data
    # data_Vn = {
    #     "real_values": [1],
    #     "imag_values": [0],
    #     "nodal_attribution": False,
    #     "averaged": False,
    # }

    ## normal surface velocity data
    data_Pa = {
        "real_values": [1],
        "imag_values": [0],
    }

    ## boundary impedance setup
    Zo = fluid.impedance

    data_Z = {
        "real_values": [Zo],
        "imag_values": [0],
    }

    # model.properties._set_property("surface_velocity", data_Vn, surface=1)
    model.properties._set_property("acoustic_pressure", data_Pa, surface=1)
    model.properties._set_property("specific_impedance", data_Z, surface=11)

    # Define the analysis frequency setup
    df = 5
    f_min = 100
    f_max = 1400
    frequencies = np.arange(f_min, f_max + df, df, dtype=float)

    analysis_setup = {
        "analysis_id": 3,
        "f_min": f_min,
        "f_max": f_max,
        "f_step": df,
        "frequencies": frequencies,
    }

    model.old_set_analysis_setup(analysis_setup)
    model.process_viscous_thermal_model_properties()

    return model


def _solve_harmonic_problem(datadir, model: "Model", path: str):

    assembler = AcousticAssembler(model)
    assembler.assemble_global_matrices_and_excitations()
    project_paths = ProjectPaths(datadir)
    harmonic_solver = HarmonicSolver(assembler, project_paths)

    frequencies = model.frequencies

    # Solve and store solutions into hdf5 files
    model.solution = harmonic_solver.solve_direct(print_log=True)
    nodal_solution = model.solution.nodal_solution

    output_surface_nodes = model.mesh.get_nodes_from_surface(11)
    average_solution = np.average(nodal_solution[output_surface_nodes, :], axis=0)

    results_path = dirname(path) + "/acoustic_pressures_reference.xlsx"
    external_data = FileHandler.read(results_path).to_dict()

    output_pressures = external_data.get("output_surface")
    reference_solution = output_pressures[:, 1] + 1j * output_pressures[:, 2]

    if output_pressures[:, 0].size == frequencies.size:
        diff_abs = np.abs((average_solution - reference_solution) / reference_solution)
        assert np.max(diff_abs) < 0.02


@pytest.mark.skip
def test_solve_model_for_tet4_element(fluid: Fluid, datadir: Path):
    path = str(PROJECT_DIR / "validation_files/data/Comsol/tet4_linear/rectangular_cavities_tet4_40x30_mm.nas")
    model = _acoustic_model_nastran(path, fluid)
    _solve_harmonic_problem(datadir, model, path)


@pytest.mark.skip
def test_solve_model_for_tet10_element(fluid: Fluid, datadir: Path):
    path = str(PROJECT_DIR / "validation_files/data/Comsol/tet10_lagrange/rectangular_cavities_tet10_50x30_mm.nas")
    model = _acoustic_model_nastran(path, fluid)
    _solve_harmonic_problem(datadir, model, path)


@pytest.mark.skip
def test_solve_model_for_hex8_element(fluid: Fluid, datadir: Path):
    path = str(PROJECT_DIR / "validation_files/data/Comsol/hex8_linear/rectangular_cavities_hex8_40x30_mm.nas")
    model = _acoustic_model_nastran(path, fluid)
    _solve_harmonic_problem(datadir, model, path)


@pytest.mark.skip
def test_solve_model_for_hex20_element(fluid: Fluid, datadir: Path):
    path = str(PROJECT_DIR / "validation_files/data/Comsol/hex20_lagrange/rectangular_cavities_hex20_40x30_mm.nas")
    model = _acoustic_model_nastran(path, fluid)
    _solve_harmonic_problem(datadir, model, path)
