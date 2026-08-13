from typing import TYPE_CHECKING

from vibra import PROJECT_DIR
from vibra.engine.analysis_info import AnalysisID, ModalAnalysisSetup
from vibra.engine.assemblers.acoustic_assembler import AcousticAssembler
from vibra.engine.mesher.mesh import Mesh
from vibra.engine.model import Model
from vibra.engine.properties.fluid import Fluid
from vibra.engine.solvers.modal_solver import ModalSolver
from vibra.external_mesh.external_mesh_data import ExternalMeshData

if TYPE_CHECKING:
    from vibra.engine.model import Model

import os
from time import time

import numpy as np

# @pytest.mark.slow
# @pytest.mark.skip


def load_external_mesh_and_solve():

    # start decoding the Ansys script file (ds.dat file or input file)
    mesh_path = "validation_files/data/WB/acoustic/elements/tet10/mesh/ds_Lpipe_act_tet10_50mm.dat"
    results_path = PROJECT_DIR / "validation_files/data/WB/acoustic/elements/tet10/results/"

    if not os.path.exists(mesh_path):
        return

    if not results_path.exists():
        return

    # define the known 'Named selections' from model
    named_selecion_to_tag = {
        "input_face": 1,
        "output_face": 2,
    }

    # define surfaces from each volume
    surfaces_from_volume = {1: [1, 2]}

    t0 = time()
    external_mesh = ExternalMeshData()
    external_mesh.read_file(mesh_path)
    external_mesh.set_named_selections(list(named_selecion_to_tag.keys()))
    external_mesh.decode_mesh_data_from_file()

    # nodes_from_named_selection = external_mesh.nodes_from_named_selection
    # for ns, nodes in nodes_from_named_selection.items():
    #     print(ns, nodes)

    # return

    dt = time() - t0
    print(f"\nElapsed time to decode the external mesh data: {round(dt, 4)} s")

    mesh = Mesh()
    mesh.import_external_nodal_coordinates(external_mesh.nodal_coordinates, index_zero=True)
    mesh.import_external_faces_connectivity(external_mesh.faces_connectivities, index_zero=True, etype_tag=9)
    mesh.import_external_solids_connectivity(external_mesh.solids_connectivities, index_zero=True, etype_tag=11)
    mesh.map_face_elements_to_solid_elements()
    mesh.map_surfaces_to_volumes(surfaces_from_volume)

    # export the mesh data
    mesh.export_nodal_coordinates("nodal_coordinates.dat")
    mesh.export_solid_elements_connectivity("solids_connectivity.dat")
    mesh.export_face_elements_connectivity("faces_connectivity.dat")

    # check collapsed elements
    # collapsed_3d_elements, collapsed_2d_elements, collapsed_1d_elements = mesh.get_collapsed_elements()

    # return
    # define the fluid properties
    temperature = 293.15
    pressure = 101325
    rho_0 = 1.204263
    c_0 = 343.395034
    mu = 1.8247e-5
    Cp = 1006.400178
    kt = 2.5503e-02
    gamma = 1.401985
    molar_mass = 28.958601

    fluid = Fluid(
        name="Air_20C",
        identifier=1,
        color=(200, 200, 200),
        pressure=pressure,
        temperature=temperature,
        fluid_density=rho_0,
        speed_of_sound=c_0,
        isentropic_exponent=gamma,
        thermal_conductivity=kt,
        specific_heat_Cp=Cp,
        dynamic_viscosity=mu,
        molar_mass=molar_mass,
    )

    ## intialize the model
    model = Model()
    model.mesh = mesh

    ## assign the created fluid
    for _vol_id in [1]:
        model.properties._set_property("fluid", fluid, volume=_vol_id)

    for _surf_id in [1, 2]:
        model.properties._set_property("fluid", fluid, surface=_surf_id)

    # ## boundary impedance setup
    # Zo = fluid.impedance

    # data_Z = {
    #     "real_values": [Zo],
    #     "imag_values": [0],
    # }

    # model.properties._set_property("specific_impedance", data_Z, surface=1)
    # model.properties._set_property("specific_impedance", data_Z, surface=2)

    ## Define the analysis frequency setup

    ## Define the analysis setup
    analysis_setup = ModalAnalysisSetup(
        analysis_id = AnalysisID.ACOUSTIC_MODAL,
        modes_number = 100,
        sigma_factor = 0.01,
        )

    # Set the analysis setup
    model.set_analysis_setup(analysis_setup)

    assembler = AcousticAssembler(model)

    # Set the analysis frequency setup
    assembler.assemble_global_matrices_and_excitations(reorder=False)

    t0 = time()
    # Run modal analysis
    modal_solver = ModalSolver(assembler)
    solution = modal_solver.solve()
    natural_frequencies = solution.natural_frequencies
    dt = time() - t0
    print(f"Elapsed time to solve modal analysis: {round(dt, 4)}s")

    modes_indexes = np.arange(natural_frequencies.size)
    nat_freq_data = np.array([modes_indexes, natural_frequencies]).T

    natural_frequencies_ref = np.loadtxt(results_path / "natural_frequencies_Ansys.dat")[:, 1]
    np.savetxt("natural_frequencies_Vibra.dat", nat_freq_data, fmt="%i %.12e", delimiter=",")

    fnat_diff = 100 * (np.abs(natural_frequencies[1:] - natural_frequencies_ref[1:]) / natural_frequencies_ref[1:])
    assert np.max(fnat_diff) < 5e-3

    for i, nat_freq in enumerate(natural_frequencies):
        print(f"Mode {i + 1}: {nat_freq: .8f} Hz")

    print(f"\nMaximum percentual difference: {np.max(fnat_diff): .4e}")


if __name__ == "__main__":
    load_external_mesh_and_solve()
