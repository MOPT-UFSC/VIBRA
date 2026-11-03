import os
from time import time

import matplotlib.pyplot as plt
import numpy as np

from validation_files.data.WB.load_external_data import LoadExternalData
from vibra import PROJECT_DIR
from vibra.engine.analysis_info import AnalysisID, FrequencySpacing
from vibra.engine.assemblers.acoustic.acoustic_assembler import AcousticAssembler
from vibra.engine.assemblers.structural.structural_assembler import StructuralAssembler
from vibra.engine.mesher.mesh import Mesh
from vibra.engine.model import Model
from vibra.engine.postprocessing import StructuralPostprocessing
from vibra.engine.properties.fluid import Fluid
from vibra.engine.properties.material import Material
from vibra.engine.solvers.harmonic_solver import HarmonicSolver
from vibra.external_mesh.external_mesh_data import ExternalMeshData
from vibra.interface.user_input.data_handler.file_handlers.file_handler import FileHandler

udof_labels = [
    "ux", 
    "uy", 
    "uz",
    ]

stresses_labels = [
    "sigma_x", 
    "sigma_y", 
    "sigma_z", 
    "tau_xy", 
    "tau_xz",
    "tau_yz", 
    ]


def load_external_mesh_and_solve():

    # start decoding the Ansys script file (ds.dat file or input file)
    mesh_path = PROJECT_DIR / "validation_files/data/WB/fsi_model/tet10/mesh/curved_pipe_tet10_fsi_model.dat"
    if not os.path.exists(mesh_path):
        return

    # define the known 'Named selections' from model
    named_selection_map = {
        "input_face_act": 1,
        "output_face_act": 2,
        "input_face_struct": 3,
        "output_face_struct": 4,
        "curved_face_struct": 5,
        "fsi_faces": 6,
    }

    # define surfaces from each volume
    surfaces_from_volume = { 
        1 : [1, 2, 6],
        2 : [3, 4, 5, 6],
        }

    t0 = time()
    external_mesh = ExternalMeshData()
    external_mesh.read_file(mesh_path)
    external_mesh.set_named_selections(named_selection_map)
    external_mesh.decode_mesh_data_from_file()

    # nodes_from_named_selection = external_mesh.nodes_from_named_selection
    # for ns, nodes in nodes_from_named_selection.items():
    #     print(ns, len(nodes))

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

    # Define the material properties

    density = 7850
    elasticity_modulus = 2e11
    poisson_ratio = 0.30
    thermal_expansion_coefficient = 1.1e-5

    material = Material(   
        name = "Carbon steel",
        identifier = 1,
        color = (200, 200, 200),
        material_density = density,
        elasticity_modulus = elasticity_modulus,
        poisson_ratio = poisson_ratio,
        thermal_expansion_coefficient = thermal_expansion_coefficient
        )

    # define the fluid properties
    temperature = 293.15
    pressure = 101325
    rho_0 = 1.204263
    c_0 = 343.395034
    mu = 1 * 1.8247e-5
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
    model.properties._set_property("fluid", fluid, volume=2)
    model.properties._set_property("material", material, volume=1)

    for _surf_id in [1, 2]:
        model.properties._set_property("fluid", fluid, surface=_surf_id)

    # dof prescription data
    dof_prescription_data = {
        "element_type": "3d_element",
        "real_values": [0.0, 0.0, 0.0],
        "imag_values": [0.0, 0.0, 0.0],
        }

    model.properties._set_property("prescribed_dof", dof_prescription_data, surface=named_selection_map.get("input_face_struct"))

    ## normal surface velocity data
    data_Vn = {
        "real_values": [1],
        "imag_values": [0],
        "element_integration": True,
    }

    model.properties._set_property("surface_velocity", data_Vn, surface=named_selection_map.get("input_face_act"))

    ## boundary impedance setup
    Zo = fluid.impedance

    data_Z = {
        "real_values": [Zo],
        "imag_values": [0],
    }

    model.properties._set_property("specific_impedance", data_Z, surface=named_selection_map.get("output_face_act"))

    ## Define the analysis frequency setup
    analysis_setup = model.get_harmonic_analysis_setup(
        frequency_spacing = FrequencySpacing.EQUALLY_DISTRIBUTED,
        analysis_id = AnalysisID.COUPLED_HARMONIC,
        f_min = 20,
        f_max = 2000,
        f_step = 20,
        global_damping = (0.0, 0.0, 0.005),
    )

    frequencies = analysis_setup.get_frequencies()

    # Set the analysis setup
    model.set_analysis_setup(analysis_setup)

    # initialize the assemblers
    act_assembler = AcousticAssembler(model)
    struct_assembler = StructuralAssembler(model)

    # process the acoustic assembly
    act_assembler.assemble_global_matrices_and_excitations(reorder=False)
    act_harmonic_solver = HarmonicSolver(act_assembler)

    t0 = time()
    # Run modal analysis
    model.solution = act_harmonic_solver.solve_direct(print_log=True)
    dt = time() - t0
    print(f"Elapsed time to solve acoustic harmonic analysis: {round(dt, 4)}s")

    # process the structural assembly
    struct_assembler.assemble_global_matrices_and_excitations(reorder=False)
    struct_harmonic_solver = HarmonicSolver(struct_assembler)

    t0 = time()
    # Run modal analysis
    model.solution = struct_harmonic_solver.solve_direct(print_log=True)
    dt = time() - t0
    print(f"Elapsed time to solve structural harmonic analysis: {round(dt, 4)}s")

    structural_post = StructuralPostprocessing(model)

    t0 = time()
    avg_nodal_stresses = structural_post.recover_nodal_averaged_structural_stresses(volume_ids=1)
    dt = time() - t0
    print(f"Time to compute nodal stresses: {dt} s")

   # Nodal results comparisons
    results_path = "validation_files/data/WB/fsi_model/tet10/results/fsi_model_reference.xlsx"
    imported_results = FileHandler.read(results_path).to_dict()

    # define the plot type
    plot_type = "absolute"

    # proces the acoustic pressure plots
    for act_label in ["input_face_act", "output_face_act"]:

        surface_id = named_selection_map.get(act_label)
        prefix = act_label.split("_")[0]

        print()
        nodes_act = model.mesh.get_nodes_from_surface(surface_id)
        dofs_act = model.get_dof_indices_from_nodes(nodes_act, "acoustic")

        solution_act = np.average(model.solution.acoustic_solution[dofs_act.ravel(), :], axis=0)
        reference_data = imported_results.get(f"{prefix}_pressure")

        # plots for acoustic pressures
        compare_averaged_nodal_results(
            surface_id,
            frequencies,
            solution_act,
            reference_data,
            plot_type=plot_type,
            title=f"Harmonic response at surface {surface_id}",
            x_label="Frequency [Hz]",
            y_label=f"Nodal pressure [Pa] - {plot_type.capitalize()}",
            )

    # process the structural displacement plots
    dof_labels = ["ux", "uy", "uz"]

    for struct_label in ["ux_curve", "uy_curve", "uz_curve", "ux_free", "uy_free", "uz_free", ]:

        if "curve" in struct_label:
            surface_id = named_selection_map.get("curved_face_struct")
        elif "free" in struct_label:
            surface_id = named_selection_map.get("output_face_struct")
        else:
            continue

        prefix = struct_label.split("_")[0]
        dof_index = dof_labels.index(prefix)

        print()
        nodes_struct = model.mesh.get_nodes_from_surface(surface_id)
        dofs_struct = model.get_dof_indices_from_nodes(nodes_struct, "structural")

        solution_struct = np.average(model.solution.structural_solution[dofs_struct[:, dof_index], :], axis=0)
        reference_data = imported_results.get(struct_label)

        # plots for displacements
        compare_averaged_nodal_results(
            surface_id,
            frequencies,
            solution_struct,
            reference_data,
            plot_type=plot_type,
            title=f"Harmonic response at surface {surface_id}",
            x_label="Frequency [Hz]",
            y_label=f"Nodal displacement {prefix} [m] - {plot_type.capitalize()}"
            )

    stresses_labels = [
        "normal_stress_x",
        "normal_stress_y",
        "normal_stress_z",
        "shear_stress_xy",
        "shear_stress_xz",
        "shear_stress_yz",
        ]

    surface_id = named_selection_map.get("curved_face_struct")
    
    for stress_index, stress_label in enumerate(stresses_labels):

        reference_data = imported_results.get(stress_label)
        if reference_data is None:
            continue

        nodes_struct = model.mesh.get_nodes_from_surface(surface_id)
        nodes_struct_mapped = model.get_mapped_nodes(nodes_struct, "structural")
        avg_surface_stress = np.average(avg_nodal_stresses[nodes_struct_mapped, stress_index, :], axis=0)

        # plots for stresses
        compare_averaged_nodal_stresses_results(
            surface_id,
            stress_label,
            frequencies,
            avg_surface_stress,
            reference_data,
            plot_type=plot_type,
            )

    plt.show()

def compare_averaged_nodal_results(
        surface_id: int, 
        frequencies: np.ndarray, 
        solution: np.ndarray,
        solution_reference: np.ndarray,
        plot_type: str = "absolute",
        title: str = "",
        x_label: str = "",
        y_label: str = "",
        ):

    freq_ref = solution_reference[:, 0]
    response_ref = solution_reference[:, 1] + 1j * solution_reference[:, 2]

    fig, ax = plt.subplots()
    if plot_type == "real":
        plot_data = np.real
        plot = ax.plot

    elif plot_type == "imaginary":
        plot_data = np.imag
        plot = ax.plot

    else:
        plot_data = np.abs
        plot = ax.semilogy

    plot(frequencies, plot_data(solution), 'r', label='Vibra')
    plot(freq_ref, plot_data(response_ref), 'k--', label='APDL')

    ax.set(xlabel=x_label, ylabel=y_label, title=title)
    ax.grid()
    ax.legend()

    if solution.size != response_ref.size:
        return

    abs_diff = np.abs((solution - response_ref) / response_ref)
    max_abs_diff = 100 * np.max(abs_diff)
    freq_max_diff = frequencies[np.argmax(abs_diff)]

    print(f"Maximum difference for acoustic pressure @ surface {surface_id}: {max_abs_diff} [%] @ {freq_max_diff} [Hz]")


def compare_averaged_nodal_stresses_results(
    surface_id: int,
    stress_label: str, 
    frequencies: np.ndarray, 
    avg_surface_stress: np.ndarray,
    solution_reference,
    plot_type: str = "absolute",
    ):

    freq_ref = solution_reference[:, 0]
    response_ref = solution_reference[:, 1] + 1j * solution_reference[:, 2]

    title = f"Harmonic response at surface {surface_id}"
    x_label = "Frequency [Hz]"
    y_label = f'Structural stress {stress_label} [Pa] - {plot_type.capitalize()}'

    fig, ax = plt.subplots()
    if plot_type == "real":
        plot_data = np.real
        plot = ax.plot

    elif plot_type == "imaginary":
        plot_data = np.imag
        plot = ax.plot

    else:
        plot_data = np.abs
        plot = ax.semilogy

    plot(frequencies, plot_data(avg_surface_stress), 'r', label='Vibra')

    if isinstance(response_ref, np.ndarray):
        plot(freq_ref, plot_data(response_ref), 'k--', label='APDL')

    ax.set(xlabel=x_label, ylabel=y_label, title=title)
    ax.grid()
    ax.legend()

    if avg_surface_stress.size != response_ref.size:
        return

    abs_diff = np.abs((avg_surface_stress - response_ref) / response_ref)
    max_abs_diff = 100 * np.max(abs_diff)
    freq_max_diff = frequencies[np.argmax(abs_diff)]

    print(f"Maximum difference for averaged {stress_label.capitalize()} @ surface {surface_id}: {max_abs_diff} [%] @ {freq_max_diff} [Hz]")


if __name__ == "__main__":

    load_external_mesh_and_solve()