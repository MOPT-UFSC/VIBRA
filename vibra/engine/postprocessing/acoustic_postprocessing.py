import numpy as np

from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from vibra.engine.solvers import AcousticHarmonicSolver, AcousticModalSolver

AcousticPlotTypes = Literal[
    "absolute_animation",
    "non_absolute_animation",
    "absolute_values",
    "real_values",
    "imag_values",
]


def compute_acoustic_modal_field(
    solver: "AcousticModalSolver",
    index: int,
    phase_rad: float,
    plot_type: AcousticPlotTypes,
):

    if solver.solution is None:
        return None

    selected_mode_shape = solver.solution[:, index]
    amplitudes = np.abs(selected_mode_shape)
    phases = np.angle(selected_mode_shape)
    delta = -phases[np.argmax(amplitudes)]
    acoustic_pressures = amplitudes * np.cos(phases + phase_rad + delta)
    
    if plot_type == "absolute_values":
        acoustic_pressures = np.abs(selected_mode_shape)
    elif plot_type == "real_values":
        acoustic_pressures = np.real(selected_mode_shape)
    elif plot_type == "imag_values":
        acoustic_pressures = np.imag(selected_mode_shape)
    elif plot_type == "absolute_animation":
        acoustic_pressures = np.abs(acoustic_pressures)

    min_value, max_value = solver.get_min_max_values_of_pressures(index, plot_type)

    return acoustic_pressures, min_value, max_value, np.imag(selected_mode_shape).any()


def compute_acoustic_harmonic_field(
    solver: "AcousticHarmonicSolver",
    index: int,
    phase_rad: float,
    plot_type: AcousticPlotTypes,
):
    
    if solver.solution is None:
        return None

    selected_results = solver.solution[:, index]
    amplitudes = np.abs(selected_results)
    phases = np.angle(selected_results)
    delta = -phases[np.argmax(amplitudes)]
    acoustic_pressures = amplitudes * np.cos(phases + phase_rad + delta)

    if plot_type == "absolute_values":
        acoustic_pressures = np.abs(selected_results)
    elif plot_type == "real_values":
        acoustic_pressures = np.real(selected_results)
    elif plot_type == "imag_values":
        acoustic_pressures = np.imag(selected_results)
    elif plot_type == "absolute_animation":
        acoustic_pressures = np.abs(acoustic_pressures)

    min_value, max_value = solver.get_min_max_values_of_pressures(index, plot_type)

    return acoustic_pressures, min_value, max_value, np.imag(selected_results).any()

def compute_particle_velocity( 
    hsolver: "AcousticHarmonicSolver",
    component_label: str,
    node_id : int | None = None,
    surface_id : int | None = None,
    ):

        frequencies = hsolver.assembler.frequencies
        zeros = np.zeros_like(frequencies, dtype=complex)

        if isinstance(node_id, int):
            surface_ids = hsolver.assembler.model.mesh.get_surfaces_from_node(node_id)
            if np.unique(surface_ids).size != 1:
                return zeros, None
            surface_id = surface_ids[0]

        rho, _ = hsolver.assembler.model.get_fluid_properties_from_surface(surface_id, frequencies)
        if rho is None:
            return zeros, None

        particle_velocities_data = hsolver.get_particle_velocity_from_surface(surface_id, rho)
        particle_velocities_Vj = particle_velocities_data.get(component_label)

        if not isinstance(particle_velocities_Vj, dict):
            return zeros, None

        if isinstance(node_id, int):
            return particle_velocities_Vj.get(node_id)

        else:
            array_particle_velocities_Vj = np.array(list(particle_velocities_Vj.values()), dtype=complex)
            return np.average(array_particle_velocities_Vj, axis=0)

def compute_acoustic_impedance( 
    hsolver: "AcousticHarmonicSolver",
    node_id : int | None = None,
    surface_id : int | None = None,
    ):

        frequencies = hsolver.assembler.frequencies
        aux_zeros = np.zeros_like(frequencies, dtype=complex)

        if isinstance(node_id, int):
            surface_ids = hsolver.assembler.model.mesh.get_surfaces_from_node(node_id)
            if np.unique(surface_ids).size != 1:
                return aux_zeros, None

            surface_id = surface_ids[0]

        elif isinstance(surface_id, int):
            nodes = hsolver.assembler.model.mesh.get_nodes_from_surface(surface_id)

        else:
            return aux_zeros, None

        rho, _ = hsolver.assembler.model.get_fluid_properties_from_surface(surface_id, frequencies)
        if rho is None:
            return aux_zeros, None

        particle_velocities_data = hsolver.get_particle_velocity_from_surface(surface_id, rho)
        particle_velocities_Vj = particle_velocities_data.get("Vn")

        if not isinstance(particle_velocities_Vj, dict):
            return aux_zeros, None

        if isinstance(node_id, int):
            pressure = hsolver.solution[node_id, :]
            particle_velocity = particle_velocities_Vj.get(node_id)
            return pressure / particle_velocity

        else:
            pressures = hsolver.solution[nodes, :]
            array_particle_velocities_Vj = np.array(list(particle_velocities_Vj.values()), dtype=complex)
            surface_impedance = pressures / array_particle_velocities_Vj
            return np.average(surface_impedance, axis=0)

def compute_surface_absorption_coefficient(
    hsolver: "AcousticHarmonicSolver",
    surface_id : int | None = None,
    ):

    frequencies = hsolver.assembler.frequencies
    aux_zeros = np.zeros_like(frequencies, dtype=complex)

    rho, speed_of_sound = hsolver.assembler.model.get_fluid_properties_from_surface(surface_id, frequencies)
    Z0 = rho * speed_of_sound

    Zs = compute_acoustic_impedance(hsolver, surface_id = surface_id)
    if not Zs.any():
        return aux_zeros

    # R is the sound reflection coefficient
    R = (Zs - Z0) / (Zs + Z0)

    # alpha is the sound absorption coefficient
    alpha = 1 - (np.abs(R))**2

    return alpha