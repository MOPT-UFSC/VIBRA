from vibra.engine.properties.fluid import Fluid
from vibra.engine.mesher.mesh import Mesh
from vibra.engine.mesher.element_type import *
from vibra.engine.model import Model
from vibra.engine.assemblers.acoustic_assembler import AcousticAssembler
from vibra.engine.solvers.acoustic_modal_solver import AcousticModalSolver
from vibra.engine.solvers.acoustic_harmonic_solver import AcousticHarmonicSolver
#
import numpy as np
import matplotlib.pyplot as plt
from time import time

def test_load_external_mesh_and_solve_lrf_model(reorder_nodes=True):
    return
    # Define the nodal coordinates and connectivity file path
    coord_path = "data/examples/mesh/muffler/coord_muff.csv"
    connect_path = "data/examples/mesh/muffler/connect_muff.csv"

    mesh = Mesh()
    mesh.import_external_nodal_coordinates(coord_path, index_zero=True)
    mesh.import_external_connectivity(connect_path, index_zero=True, etype_tag=4, e_nodes=4)
    mesh.element_type = TETRAHEDRON_4
    mesh.connectivity_from_surfaces = get_faces_connectivities()
    mesh.volume_from_surface[1].append(1)
    mesh.volume_from_surface[2].append(1)
    
    if reorder_nodes:
        mesh._process_nodes_reordering()
        map_nodes_indexes = mesh.reordering.map_nodes_indexes

    # Define the fluid properties
    diam_hole = 0.004
    rho_0 = 1.225
    c_0 = 346.25
    mu = 1*1.7894E-05
    gamma = 1.4
    Pr = 0.71
    P_0 = rho_0*(c_0**2)/gamma
    #
    lrf_prop = [diam_hole, c_0, rho_0, mu, gamma, Pr, P_0]
    #
    fluid = Fluid(  name = "Air",
                    identifier = 1,
                    color = (200, 200, 200),
                    fluid_density = rho_0,
                    speed_of_sound = c_0,
                    dynamic_viscosity = mu  )

    # Set the defined fluid
    model = Model()
    model.set_mesh(mesh)
    model.set_fluid(fluid, volume=1)

    # Normal surface velocity data
    data_Vn = { "real_values" : [1],
                "imag_values" : [0],
                "nodal_attribution" : False,
                "averaged" : False }
    
    # Impedance data
    Zo = fluid.impedance
    data_Z = {  "real_values" : [Zo],
                "imag_values" : [0],
                "nodal_attribution" : False,
                "averaged" : False  }

    model.set_surface_velocity(data_Vn, 1)
    model.set_specific_impedance(data_Z, 2)

    data = {"diameter" : diam_hole}
    model.set_lrf_eq_model_data(data, volume=1)
    model.set_lrf_eq_data([1], lrf_prop)
    
    # Create an object to assembler
    assembler = AcousticAssembler(model)
    
    # Define the analysis frequency setup
    df = 1
    f_min = 1
    f_max = 500
    frequencies = np.arange(f_min, f_max + df, df)

    # Set the analysis frequency setup
    assembler.set_frequencies(frequencies)
    
    model.process_lrf_properties(frequencies)
    assembler.process_assemble()
    
    # t0 = time()
    # # Run modal analysis
    # modal_solver = AcousticModalSolver(assembler)
    # natural_frequencies, modal_shape = modal_solver.solve()
    # dt = time() - t0
    # print(f"Elapsed time to solve modal analysis: {round(dt, 4)}s")
    # return
    
    # Define the analysis type and load setup
    analysis_data = {"analysis_id" : 3, "frequencies" : frequencies}
    harmonic_solver = AcousticHarmonicSolver(assembler, analysis_data=analysis_data)
    
    t0 = time()
    # Run harmonic analysis
    solution = harmonic_solver.solve(print_log=True)
    dt = time() - t0
    print(f"Elapsed time to solve harmonic analysis: {round(dt, 4)}")

    if solution is not None:

        cols = solution.shape[1]

        node = 3602
        if reorder_nodes:
            node = int(map_nodes_indexes[node])
        
        results = np.zeros((cols, 3), dtype=float)
        results[:, 0] = frequencies
        results[:, 1] = np.real(solution[node, :])
        results[:, 2] = np.imag(solution[node, :])
        filename = f"acoustic_pressure_at_node_{node}_Vibra_pardiso.dat"
        np.savetxt(filename, results, delimiter=",")

        results_path = "data/examples/mesh/muffler/LRF0_004.csv"

        data_ref = np.loadtxt(results_path, delimiter=",")
        freq_ref = data_ref[:, 0]
        P_ref = data_ref[:, 1] + 1j*data_ref[:, 2]

        # error_abs = np.abs((solution[node, :] - P_ref)/((solution[node, :] + P_ref)/2))
        # assert error_abs < 1e-1

        fig1, ax1 = plt.subplots()
        ax1.semilogy(frequencies, np.abs(solution[node, :]), 'r', label='VIBRA')
        ax1.semilogy(freq_ref, np.abs(P_ref), 'k--', label='ANSYS')
        # ax1.semilogy(freq_ref, np.abs(solution[node, :] - P_ref), 'k--', label='ANSYS')
        # ax1.semilogy(freq_ref, error_abs, 'k--', label='ANSYS')
        ax1.set(xlabel='Frequency [Hz]', ylabel='Acoustic Pressure [Pa] - Absolute', title='Harmonic Response - Outlet pressure')
        ax1.grid()

        fig2, ax2 = plt.subplots()
        ax2.plot(frequencies, np.real(solution[node, :]), 'r', label='VIBRA')
        ax2.plot(freq_ref, np.real(P_ref), 'k--', label='ANSYS')
        ax2.set(xlabel='Frequency [Hz]', ylabel='Acoustic Pressure [Pa] - Real', title='Harmonic Response - Outlet pressure')
        ax2.grid()

        fig3, ax3 = plt.subplots()
        ax3.plot(frequencies, np.imag(solution[node, :]), 'r', label='VIBRA')
        ax3.plot(freq_ref, np.imag(P_ref), 'k--', label='ANSYS')
        ax3.set(xlabel='Frequency [Hz]', ylabel='Acoustic Pressure [Pa] - Imaginary', title='Harmonic Response - Outlet pressure')
        ax3.grid()

        plt.legend()
        plt.show()

def get_faces_connectivities():
    
    ## Face da excitação F4
    #connect_face1 = np.array([[1,191,197,61,84],
    #                         [2,197,148,106,61],
    #                         [3,192,198,197,191],
    #                         [4,198,147,148,197]],dtype=int)
    #nel_face1 = len(connect_face1)
    ## Face da excitação F3
    # connect_face1 = np.array([[1,12,8,7],
    #                          [2,11,8,12],
    #                          [3,11,9,8],
    #                          [4,10,9,11]],dtype=int)

    connect_face1 = np.array([[  1,  184,  183, 3611 ],
                              [  2,  183,  182, 3609 ],
                              [  3,  182,  181, 3609 ],
                              [  4,  181,  180, 3607 ],
                              [  5,  180,  179, 3607 ],
                              [  6,  179,  178, 3605 ],
                              [  7,  178,  177, 3605 ],
                              [  8,  177,  189, 3606 ],
                              [  9,  189,  188, 3606 ],
                              [ 10,  188,  187, 3608 ],
                              [ 11,  187,  186, 3608 ],
                              [ 12,  186,  185, 3610 ],
                              [ 13,  185,  184, 3610 ],
                              [ 14,  183, 3609, 3611 ],
                              [ 15,  181, 3607, 3609 ],
                              [ 16,  179, 3605, 3607 ],
                              [ 17,  177, 3606, 3605 ],
                              [ 18,  188, 3608, 3606 ],
                              [ 19,  186, 3610, 3608 ],
                              [ 20,  184, 3611, 3610 ],
                              [ 21, 3609, 3604, 3611 ],
                              [ 22, 3607, 3604, 3609 ],
                              [ 23, 3605, 3604, 3607 ],
                              [ 24, 3606, 3604, 3605 ],
                              [ 25, 3608, 3604, 3606 ],
                              [ 26, 3610, 3604, 3608 ],
                              [ 27, 3611, 3604, 3610 ]], dtype=int) - 1
    
    nel_face1 = len(connect_face1)
    
    ## Face da impedância Z4
    #connect_face2 = np.array([[1,149,195,62,85],
    #                         [2,195,194,63,62],
    #                         [3,150,196,195,149],
    #                         [4,196,193,194,195]],dtype=int)
    #nel_face2 = len(connect_face2)

    # Face da impedância Z3
    #connect_face2 = np.array([[1,6,2,1],
    #                          [2,5,2,6],
    #                          [3,5,3,2],
    #                          [4,4,3,5]],dtype=int)
    
    connect_face2 = np.array([[  1,  375,  376, 3600 ],
                              [  2,  376,  377, 3600 ],
                              [  3,  377, 3598, 3600 ],
                              [  4,  377,  378, 3598 ],
                              [  5,  378,  366, 3598 ],
                              [  6,  366, 3597, 3598 ],
                              [  7,  366,  367, 3597 ],
                              [  8,  367,  368, 3597 ],
                              [  9,  368, 3599, 3597 ],
                              [ 10,  368,  369, 3599 ],
                              [ 11,  369,  370, 3599 ],
                              [ 12,  370, 3601, 3599 ],
                              [ 13,  370,  371, 3601 ],
                              [ 14,  371,  372, 3601 ],
                              [ 15,  372, 3603, 3601 ],
                              [ 16,  372,  373, 3603 ],
                              [ 17,  373, 3602, 3603 ],
                              [ 18,  373,  374, 3602 ],
                              [ 19,  374,  375, 3602 ],
                              [ 20,  375, 3600, 3602 ],
                              [ 21, 3602, 3600, 3596 ],
                              [ 22, 3600, 3598, 3596 ],
                              [ 23, 3598, 3597, 3596 ],
                              [ 24, 3597, 3599, 3596 ],
                              [ 25, 3599, 3601, 3596 ],
                              [ 26, 3601, 3603, 3596 ],
                              [ 27, 3603, 3602, 3596 ]], dtype=int) - 1

    nel_face2 = len(connect_face2)

    connectivity_from_surfaces = dict()
    
    connectivity_from_surfaces[1] = {   "element_indexes" : connect_face1[:, 0],
                                        "connectivity" : connect_face1[:, 1:]   }
    
    connectivity_from_surfaces[2] = {   "element_indexes" : connect_face2[:, 0],
                                        "connectivity" : connect_face2[:, 1:]   }
    
    return connectivity_from_surfaces

def plot_results():

    path_pardiso = "temp/acoustic_pressure_at_node_3596_Vibra_pardiso.dat"
    path_scipy = "temp/acoustic_pressure_at_node_3596_Vibra_scipy.dat"

    data_pardiso = np.loadtxt(path_pardiso, delimiter=",")
    data_scipy = np.loadtxt(path_scipy, delimiter=",")

    freq_pardiso = data_pardiso[:, 0]
    Xf_pardiso = data_pardiso[:, 1] + 1j*data_pardiso[:, 2]

    freq_scipy = data_scipy[:, 0]
    Xf_scipy = data_scipy[:, 1] + 1j*data_scipy[:, 2]

    fig, ax1 = plt.subplots()
    ax1.semilogy(freq_pardiso, np.abs(Xf_pardiso), 'r', label='pardiso')
    ax1.semilogy(freq_scipy, np.abs(Xf_scipy), 'k--', label='scipy')
    # ax1.semilogy(freq_scipy, np.abs(Xf_pardiso - Xf_scipy), 'k-', label='difference')
    ax1.set(xlabel='Frequency [Hz]', ylabel='Acoustic Pressure [Pa] - Absolute', title='Harmonic Response - Outlet pressure')
    ax1.grid()
    plt.legend()
    plt.show()

def save_results(data):
    pass

if __name__ == "__main__":
    test_load_external_mesh_and_solve_lrf_model(reorder_nodes=False)
    # plot_results()