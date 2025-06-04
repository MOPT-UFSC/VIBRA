
from vibra import app
from vibra.engine import AnalysisID
from vibra.engine.properties.fluid import Fluid
from vibra.engine.properties.material import Material

from molde.utils import TreeInfo
from molde.utils.format_sequences import format_long_sequence

import numpy as np
from numbers import Number


# GEOMETRY RENDER WIDGET INFO TEXTS
def points_info_text():

    selected_points = app().main_window.selected_geometry_points
    node_ids = [int(point_id)-1 for point_id in selected_points]
    point_ids = list(selected_points)

    if len(node_ids) == 0:
        return ""

    text = ""

    if len(point_ids) == 1:
        coords = app().project.model.mesh.nodal_coordinates[node_ids[0], 1:].round(6)
        tree = TreeInfo(f"POINT {point_ids[0]}")
        tree.add_item("Position", "({:.6f}, {:.6f}, {:.6f})".format(*coords), "m")
        text += str(tree)

    elif len(point_ids) == 2:
        coord_A = app().project.model.mesh.nodal_coordinates[node_ids[0], 1:]
        coord_B = app().project.model.mesh.nodal_coordinates[node_ids[1], 1:]
        dx, dy, dz = np.round(np.abs(coord_A - coord_B), 6)
        distance = np.linalg.norm(coord_A - coord_B)

        tree = TreeInfo(f"2 POINTS IN SELECTION: {point_ids[0]}, {point_ids[1]}")
        tree.add_item("Total distance", f"{distance : .6f}", "m")
        tree.add_item("Distance dx", f"{dx : .6f}", "m")
        tree.add_item("Distance dy", f"{dy : .6f}", "m")
        tree.add_item("Distance dz", f"{dz : .6f}", "m")
        text += str(tree)

    else:
        sequence = ", ".join(str(i) for i in point_ids)
        if len(sequence) > 20:
            sequence = sequence[:20 - 4] + " ..."

        text += f"{len(point_ids)} POINTS IN SELECTION: {sequence}\n\n"
    
    return text

def lines_info_text():
    line_ids = list(app().main_window.selected_geometry_lines)

    if len(line_ids) == 0:
        return ""
    
    length_from_lines = app().project.model.mesh.length_from_lines

    text = ""
    length = 0
    for line_id in line_ids:
        length += length_from_lines.get(line_id, 0)

    if len(line_ids) == 1:
        tree = TreeInfo(f"LINE {line_ids[0]}")
        tree.add_item("Length", f"{length : .6e}", "m")

        # nodes_from_line = app().project.model.mesh.nodes_from_lines.get(line_ids[0])
        # if nodes_from_line is not None:
        #     print()
        #     print(f"There are {len(nodes_from_line)} nodes in line {line_ids[0]}")
        #     print(f"Nodes: {[int(node) for node in nodes_from_line]}")

    else:

        sequence = ", ".join(str(i) for i in line_ids)
        if len(sequence) > 20:
            sequence = sequence[:20 - 4] + " ..."

        tree = TreeInfo(f"{len(line_ids)} LINES IN SELECTION: {sequence}")
        tree.add_item("Length (compound)", f"{length : .6e}", "m")

    text += str(tree)
    return text

def faces_info_text():
    volumes = list(app().main_window.selected_geometry_volumes)

    if len(volumes) != 0:
        return ""
    
    surface_ids = list(app().main_window.selected_geometry_surfaces)

    if len(surface_ids) == 0:
        return ""

    area_from_surfaces = app().project.model.mesh.area_from_surfaces

    text = ""
    area = 0
    for surface_id in surface_ids:
        area += area_from_surfaces.get(surface_id, 0)

    if len(surface_ids) == 1:
        tree = TreeInfo(f"SURFACE {surface_ids[0]}")
        tree.add_item("Area", f"{area : .6e}", "m²")

        # nodes_from_surface = app().project.model.mesh.nodes_from_surfaces.get(surface_ids[0])
        # if nodes_from_surface is not None:
        #     print(f"There are {len(nodes_from_surface)} nodes in surface {surface_ids[0]}")
        #     print(f"Nodes: {nodes_from_surface}")
        #     print()

        surface_data = app().project.model.properties._get_property("surface_thickness", surface=surface_ids[0])
        if isinstance(surface_data, dict):
            tree.add_item("Thickness", surface_data["surface_thickness"], "m")
            tree.add_item("Offset", surface_data["thickness_offset"])

    else:
        sequence = ", ".join(str(i) for i in surface_ids)
        if len(sequence) > 20:
            sequence = sequence[:20 - 4] + " ..."

        tree = TreeInfo(f"{len(surface_ids)} SURFACES IN SELECTION: {sequence}")
        tree.add_item("Area (compound)", f"{area : .6e}", "m²")

    text += str(tree)

    return text

def volumes_info_text():
    volume_ids = list(app().main_window.selected_geometry_volumes)
    if len(volume_ids) == 0:
        return ""

    text = ""
    volume, fluid_mass, material_mass = process_volumes_and_masses(volume_ids)

    if len(volume_ids) == 1:
        tree = TreeInfo(f"VOLUME {volume_ids[0]}")
        tree.add_item("Volume", f"{volume : .6e}", "m³")

    else:
        sequence = ", ".join(str(i) for i in volume_ids)
        if len(sequence) > 20:
            sequence = sequence[:20 - 4] + " ..."

        tree = TreeInfo(f"{len(volume_ids)} VOLUMES IN SELECTION: {sequence}")
        tree.add_item("Volume (compound)", f"{volume : .6e}", "m³")

    if fluid_mass:
        tree.add_item("Fluid mass", f"{fluid_mass : .6e}", "kg")

    if material_mass:
        tree.add_item("Material mass", f"{material_mass : .6e}", "kg")

    text += str(tree)
    return text

def process_volumes_and_masses(volume_ids: list):
    fluid_mass = 0.
    material_mass = 0.
    volume_compound = 0.

    volume_from_bodies = app().project.model.mesh.volume_from_bodies

    for volume_id in volume_ids:
        volume = volume_from_bodies.get(volume_id, 0)
        volume_compound += volume

        fluid = app().project.model.properties._get_property("fluid", volume=volume_id)
        if isinstance(fluid, Fluid):
            fluid_density = fluid.fluid_density
            fluid_mass += volume * fluid_density

        material = app().project.model.properties._get_property("material", volume=volume_id)
        if isinstance(material, Material):
            material_density = material.density
            material_mass += volume * material_density
    
    return volume_compound, fluid_mass, material_mass

def material_info_text():
    volumes = list(app().main_window.selected_geometry_volumes)
    surfaces = list(app().main_window.selected_geometry_surfaces)

    text = ""
    if len(volumes) != 1 and len(surfaces) != 1:
        return text

    elif len(volumes) == 1:
        material = app().project.model.properties._get_property("material", volume=volumes[0])

    elif len(surfaces) == 1:
        material = app().project.model.properties._get_property("material", surface=surfaces[0])

    if material is None:
        return text

    tree = TreeInfo("Material")
    tree.add_item("Name", material.name)
    tree.add_item("Identifier", material.identifier)
    tree.add_item("Density", material.density, "kg/m³")
    tree.add_item("elasticity modulus", material.elasticity_modulus / 1e9, "GPa")
    tree.add_item("Poisson ratio", material.poisson_ratio, "--")
    tree.add_item("Thermal expasion coefficient", material.thermal_expansion_coefficient, "1/K")

    text += str(tree)

    return text

def fluid_info_text():
    volumes = list(app().main_window.selected_geometry_volumes)
    surfaces = list(app().main_window.selected_geometry_surfaces)

    text = ""
    if len(volumes) != 1 and len(surfaces) != 1:
        return text

    elif len(volumes) == 1:
        fluid = app().project.model.properties._get_property("fluid", volume=volumes[0])

    elif len(surfaces) == 1:
        fluid = app().project.model.properties._get_property("fluid", surface=surfaces[0])

    if fluid is None:
        return text

    tree = TreeInfo("Fluid")
    tree.add_item("Name", fluid.name)
    tree.add_item("Identifier", fluid.identifier)
    tree.add_item("Pressure", fluid.pressure, "Pa")
    tree.add_item("Temperature", fluid.temperature, "K")
    tree.add_item("Density", fluid.fluid_density, "kg/m³")
    tree.add_item("Speed of sound", fluid.speed_of_sound, "m/s")

    if fluid.molar_mass is not None:
        tree.add_item("Molar mass", fluid.molar_mass, "kg/kmol")

    text += str(tree)

    return text

def porous_material_info_text():
    volumes = list(app().main_window.selected_geometry_volumes)
    text = ""

    if len(volumes) != 1:
        return text

    pm_model = app().project.model.properties._get_property(
        "porous_material_model", volume=volumes[0]
    )
    if pm_model is None:
        return text

    tree = TreeInfo("Porous material")
    tree.add_item("Model", pm_model["model"])
    tree.add_item("Flow resistivity", pm_model["flow_resistivity"], "kg/m³s")

    text += str(tree)

    return text

def perforated_plate_info_text():

    text = ""
    surfaces = list(app().main_window.selected_geometry_surfaces)

    if not surfaces:
        return text

    surfaces.sort()
    surfaces = [int(surf_id) for surf_id in surfaces]

    if len(surfaces) == 1:
        pp_data = app().project.model.properties._get_property("perforated_plate_model", surface=surfaces[0])
    else:
        pp_data = app().project.model.properties._get_property("perforated_plate_model", surface=tuple(surfaces))

    if not isinstance(pp_data, dict):
        return text

    tree = TreeInfo("Perforated plate")

    tree.add_item("Formulation", pp_data["formulation"].replace("_", " "))
    if pp_data["formulation"] == "circular_hole":

        tree.add_item("Coupling type", pp_data.get("coupling_type").replace("_", " "))
        tree.add_item("Plate thickness", pp_data.get("plate_thickness"), "m")
        tree.add_item("Hole diameter", pp_data.get("hole_diameter"), "m")
        tree.add_item("Porosity", pp_data.get("porosity"), "--")
        tree.add_item("Linear discharge coefficient", pp_data.get("linear_discharge_coefficient"), "--")

        if "non_linear_discharge_coefficient" in pp_data.keys():
            tree.add_item("Non-linear discharge coefficient", pp_data.get("non_linear_discharge_coefficient"), "--")
            tree.add_item("Non-linear correction factor", pp_data.get("non_linear_correction_factor"), "--")

        if "table_names" in pp_data.keys():
            tree.add_item("User-defined transfer impedance", "active")

    text += str(tree)

    return text

def acoustic_boundary_conditions_info_text():
    text = ""
    selected_faces = list(app().main_window.selected_geometry_surfaces)

    if len(selected_faces) != 1:
        return text

    acoustic_pressure = app().project.model.properties._get_property(
        "acoustic_pressure",
        surface=selected_faces[0],
    )
    surface_velocity = app().project.model.properties._get_property(
        "surface_velocity",
        surface=selected_faces[0],
    )   
    mass_flow_rate = app().project.model.properties._get_property(
        "mass_flow_rate",
        surface=selected_faces[0],
    )
    absorption_surface = app().project.model.properties._get_property(
        "absorption_surface",
        surface=selected_faces[0],
    )
    specific_impedance = app().project.model.properties._get_property(
        "specific_impedance",
        surface=selected_faces[0],
    )

    boundary_conditions_list = [
                                acoustic_pressure,
                                surface_velocity,
                                mass_flow_rate,
                                absorption_surface,
                                specific_impedance,
                                ]

    if all(condition is None for condition in boundary_conditions_list):
        return text

    if acoustic_pressure is not None:
        values = acoustic_pressure["values"][0]
        text += acoustic_format("Acoustic pressure", values, "P", "Pa")

    if surface_velocity is not None:
        values = surface_velocity["values"][0]
        text += acoustic_format("Surface velocity", values, "Vn", "m/s")

    if mass_flow_rate is not None:
        values = mass_flow_rate["values"][0]
        text += acoustic_format("Mass flow rate", values, "Q", "kg/s")

    if absorption_surface is not None:
        values = absorption_surface["values"][0]
        text += acoustic_format("Absorption surface", values, "alpha", "--")

    if specific_impedance is not None:
        if "anechoic_termination" in specific_impedance.keys():
            fluid = app().project.model.properties._get_property("fluid", surface=selected_faces[0])
            if isinstance(fluid, Fluid):
                density = fluid.fluid_density
                speed_of_sound = fluid.speed_of_sound
                values = np.array([density * speed_of_sound], dtype=complex)
                text += acoustic_format(
                    "Specific impedance",
                    values[0],
                    "Zs",
                    "kg/m².s",
                    ("Impedance type", "anechoic (non-reflexive)"),
                )

        else:
            values = specific_impedance["values"]
            text += acoustic_format("Specific impedance", values[0], "Zs", "kg/m².s")

    return text

def structural_boundary_conditions_info_text():
    text = ""
    distributed_loads_line = None
    prescribed_dofs = None
    nodal_loads = None
    distributed_loads_area = None
    normal_pressure_load = None

    selected_faces = list(app().main_window.selected_geometry_surfaces)
    selected_lines = list(app().main_window.selected_geometry_lines)

    if len(selected_faces) == 1:
        prescribed_dofs = app().project.model.properties._get_property(
            "prescribed_dofs", surface=selected_faces[0]
        )
        nodal_loads = app().project.model.properties._get_property(
            "nodal_loads", surface=selected_faces[0]
        )
        distributed_loads_area = app().project.model.properties._get_property(
            "distributed_loads", surface=selected_faces[0]
        )
        normal_pressure_load = app().project.model.properties._get_property(
            "normal_pressure_load", surface=selected_faces[0]
        )

    elif len(selected_lines) == 1:
        distributed_loads_line = app().project.model.properties._get_property(
            "distributed_loads", line=selected_lines[0]
        )

    else:
        return text

    boundary_conditions = [
        prescribed_dofs,
        nodal_loads,
        distributed_loads_area,
        normal_pressure_load,
        distributed_loads_line,
    ]

    if all(bc is None for bc in boundary_conditions):
        return text

    if prescribed_dofs is not None:
        values = prescribed_dofs["values"]
        loaded_table = "table_names" in prescribed_dofs.keys()
        text += structural_format(
            "Prescribed dofs", values, ("u", "r"), ("m", "rad"), loaded_table
        )

    if nodal_loads is not None:
        values = nodal_loads["values"]
        loaded_table = "table_names" in nodal_loads.keys()
        text += structural_format(
            "Nodal loads", values, ("F", "M"), ("N", "N.m"), loaded_table
        )

    if distributed_loads_area is not None:
        values = distributed_loads_area["values"]
        loaded_table = "table_names" in distributed_loads_area.keys()
        text += structural_format("Distributed loads", values, ["P"], ["N/m²"], loaded_table)

    if distributed_loads_line is not None:
        values = distributed_loads_line["values"]
        loaded_table = "table_names" in distributed_loads_line.keys()
        text += structural_format("Distributed loads", values, ["P"], ["N/m"], loaded_table)

    if normal_pressure_load is not None:
        values = normal_pressure_load["values"]
        loaded_table = "table_names" in normal_pressure_load.keys()
        text += structural_format("Normal pressure", values, ["P"], ["N/m²"], loaded_table)

    return text

def acoustic_format(property_name, value, label, unit, additional_labels=[]):
    tree = TreeInfo(property_name)
    if isinstance(value, Number | str | float | complex):
        tree.add_item(label, np.round(value, 4), unit)
    else:
        tree.add_item(label, "Table of values")

    if len(additional_labels) == 2:
        tree.add_item(additional_labels[0], additional_labels[1])

    return str(tree)


# MESH RENDER WIDGET INFO TEXTS

def nodes_info_text():
    text = ""
    node_ids = list(app().main_window.selected_mesh_nodes)

    if len(node_ids) == 0:
        return ""

    elif len(node_ids) == 1:
        coords = app().project.model.mesh.nodal_coordinates[node_ids[0], 1:].round(6)

        tree = TreeInfo(f"NODE {node_ids[0]}")
        tree.add_item("Position", "({:.6f}, {:.6f}, {:.6f})".format(*coords), "m")
        text += str(tree)

    elif len(node_ids) == 2:
        coord_A = app().project.model.mesh.nodal_coordinates[node_ids[0], 1:]
        coord_B = app().project.model.mesh.nodal_coordinates[node_ids[1], 1:]
        dx, dy, dz = np.round(np.abs(coord_A - coord_B), 6)
        distance = np.linalg.norm(coord_A - coord_B)

        tree = TreeInfo(f"2 NODES IN SELECTION: {node_ids[0]}, {node_ids[1]}")
        tree.add_item("Total distance", f"{distance : .6f}", "m")
        tree.add_item("Distance dx", f"{dx : .6f}", "m")
        tree.add_item("Distance dy", f"{dy : .6f}", "m")
        tree.add_item("Distance dz", f"{dz : .6f}", "m")
        text += str(tree)

    else:
        text += f"{len(node_ids)} NODES IN SELECTION:\n{format_long_sequence(node_ids)}\n\n"

    return text

def mesh_faces_info_text():
    text = ""
    faces = list(app().main_window.selected_mesh_faces)

    if len(faces) > 1:
        text += f"{len(faces)} FACES IN SELECTION:\n"
        text += f"{format_long_sequence(faces)}\n\n"

    elif len(faces) == 1:
        text += f"FACE ELEMENT {faces[0]}\n\n"

    return text

def mesh_solids_info_text():
    solids_elem_ids = list(app().main_window.selected_mesh_solids)
    text = ""

    if len(solids_elem_ids) > 1:
        text += f"{len(solids_elem_ids)} SOLIDS IN SELECTION:\n"
        text += f"{format_long_sequence(solids_elem_ids)}\n\n"

    elif len(solids_elem_ids) == 1:
        element_id = solids_elem_ids[0]
        connect = app().project.model.mesh.solids_connectivity[element_id, 4:]

        tree = TreeInfo(f"SOLID ELEMENT {element_id}")
        tree.add_item("Connectivity", f"{connect}")
        text += str(tree)

    return text

def mesh_material_info_text():
    elements = list(app().main_window.selected_mesh_faces)
    text = ""

    if not elements:
        elements = list(app().main_window.selected_mesh_solids)

    if len(elements) == 1:
        current_solid = app().project.model.mesh.volume_from_element[elements[0]]
        material = app().project.model.properties._get_property("material", volume=current_solid)
        if material is None:
            return text

        tree = TreeInfo("Material")
        tree.add_item("Name", material.name)
        tree.add_item("Identifier", material.identifier)
        tree.add_item("Density", material.density, "kg/m³")
        tree.add_item("Young Modulus", material.elasticity_modulus / 1e9, "GPa")
        tree.add_item("Poisson Ratio", material.poisson_ratio, "--")
        tree.add_item(
            "Thermal Expasion Coefficient", material.thermal_expansion_coefficient, "1/K"
        )

        text += str(tree)

    return text

def mesh_fluid_info_text():
    elements = list(app().main_window.selected_mesh_faces)
    text = ""

    if not elements:
        elements = list(app().main_window.selected_mesh_solids)

    if len(elements) == 1:
        current_solid = app().project.model.mesh.volume_from_element[elements[0]]
        fluid = app().project.model.properties._get_property("fluid", volume=current_solid)
        if fluid is None:
            return text

        tree = TreeInfo("Fluid")
        tree.add_item("Name", fluid.name)
        tree.add_item("Identifier", fluid.identifier)
        tree.add_item("Pressure", fluid.pressure, "Pa")
        tree.add_item("Temperature", fluid.temperature, "K")
        tree.add_item("Density", fluid.fluid_density, "kg/m³")
        tree.add_item("Speed of sound", fluid.speed_of_sound, "m/s")
        tree.add_item("Molar mass", fluid.molar_mass, "kg/kmol")

        text += str(tree)

    return text

def mesh_structural_boundary_conditions_info_text():
    text = ""
    selected_nodes = list(app().main_window.selected_mesh_nodes)

    if len(selected_nodes) != 1:
        return text

    prescribed_dofs = app().project.model.properties._get_property(
        "prescribed_dofs", node=selected_nodes[0]
    )
    nodal_loads = app().project.model.properties._get_property(
        "nodal_loads", node=selected_nodes[0]
    )
    boundary_conditions_list = [prescribed_dofs, nodal_loads]

    if all(condition is None for condition in boundary_conditions_list):
        return text

    if prescribed_dofs is not None:
        values = prescribed_dofs["values"]
        loaded_table = "table_names" in prescribed_dofs.keys()
        text += structural_format(
            "Prescribed dofs", values, ("u", "r"), ("m", "rad"), loaded_table
        )

    if nodal_loads is not None:
        values = nodal_loads["values"]
        loaded_table = "table_names" in nodal_loads.keys()
        text += structural_format(
            "Nodal loads", values, ("F", "M"), ("N", "N.m"), loaded_table
        )

    return text

def mesh_structural_format(property_name, values, labels, units, has_table):
    if all_none(values):
        return ""

    u_values = list()
    u_labels = list()
    for val, label in zip(values[:3], "xyz"):
        if val is None:
            continue

        if not isinstance(val, Number | complex | str):
            val = "table"

        u_values.append(val)
        u_labels.append(labels[0] + label)

    r_values = list()
    r_labels = list()
    for val, label in zip(values[3:], "xyz"):
        if val is None:
            continue

        if not isinstance(val, Number | complex | str):
            val = "table"

        r_values.append(val)
        r_labels.append(labels[1] + label)

    tree = TreeInfo(property_name)
    if has_table:
        if u_values:
            tree.add_item(", ".join(u_labels), "Table of values")
        if r_values:
            tree.add_item(", ".join(r_labels), "Table of values")

    else:
        if u_values:
            tree.add_item(", ".join(u_labels), u_values, units[0])
        if r_values:
            tree.add_item(", ".join(r_labels), r_values, units[1])

    return str(tree)

# RESULTS RENDER WIDGET INFO TEXTS

def analysis_info_text(frequency_index: int):

    project = app().project
    if not project.is_there_a_valid_solution():
        return ""

    display_name = {
                    AnalysisID.STRUCTURAL_MODAL : "Structural Modal Analysis",
                    AnalysisID.ACOUSTIC_MODAL : "Acoustic Modal Analysis",
                    AnalysisID.STRUCTURAL_HARMONIC_DIRECT_METHOD : "Structural Harmonic Analysis",
                    AnalysisID.ACOUSTIC_HARMONIC : "Acoustic Harmonic Analysis",
                    }

    analysis_id = project.analysis_id
    tree = TreeInfo(display_name[analysis_id])

    if project.analysis_id in [
        AnalysisID.STRUCTURAL_MODAL,
        AnalysisID.ACOUSTIC_MODAL,
    ]:

        frequencies = None
        if analysis_id == AnalysisID.STRUCTURAL_MODAL:
            frequencies = project.structural_modal_solver.natural_frequencies

        if analysis_id == AnalysisID.ACOUSTIC_MODAL:
            if len(project.acoustic_modal_solver.complex_natural_frequencies):
                frequencies = list(project.acoustic_modal_solver.complex_natural_frequencies)
            else:
                frequencies = list(project.acoustic_modal_solver.natural_frequencies)

        if frequencies is None:
            return ""

        if frequency_index >= len(frequencies):
            print(f"frequency index: {frequency_index}")
            print(f"frequencies: {frequencies}")
            return ""
        
        # This works beacuse there is only this method for now
        # TODO: add logic for other methods
        tree.add_item("Method", "Direct")

        mode = frequency_index + 1
        tree.add_item("Mode", mode)

        if analysis_id == AnalysisID.ACOUSTIC_MODAL and isinstance(frequencies[0], complex):
            value = frequencies[frequency_index]
            damping_ratio = -np.real(value) / np.abs(value)
            damped_frequency = np.abs(value) * np.sqrt(1 - damping_ratio**2)
            tree.add_item("Damped Natural Frequency", f"{damped_frequency : .4f}", "Hz")
            tree.add_item("Damping Ratio", f"{damping_ratio : .4e}", "--")

        else:
            frequency = frequencies[frequency_index]
            tree.add_item("Natural Frequency", f"{frequency : .4f}", "Hz")

    else:

        frequencies = project.model.frequencies
        if frequencies is None:
            return ""

        if frequency_index-1 >= len(frequencies):
            return ""

        # TODO: add logic for other methods
        tree.add_item("Method", "Direct")

        frequency = frequencies[frequency_index-1]
        tree.add_item("Frequency", f"{frequency:.2f}", "Hz")

    return str(tree)

def structural_format(property_name, values, labels, units, has_table):
    if all_none(values):
        return ""

    if property_name == "Normal pressure":
        sufix_labels = "n"
    else:
        sufix_labels = "xyz"

    u_values = list()
    u_labels = list()
    for val, label in zip(values[:3], sufix_labels):
        if val is None:
            continue

        if not isinstance(val, Number | complex | str):
            val = "table"

        u_values.append(val)
        u_labels.append(labels[0] + label)

    r_values = list()
    r_labels = list()
    if len(values) > 3:
        for val, label in zip(values[3:], "xyz"):
            if val is None:
                continue

            if not isinstance(val, Number | complex | str):
                val = "table"

            r_values.append(val)
            r_labels.append(labels[1] + label)

    tree = TreeInfo(property_name)
    if has_table:
        if u_values:
            tree.add_item(", ".join(u_labels), "Table of values")

        if r_values:
            tree.add_item(", ".join(r_labels), "Table of values")

    else:
        if u_values:
            tree.add_item(", ".join(u_labels), u_values, units[0])

        if r_values:
            tree.add_item(", ".join(r_labels), r_values, units[1])

    return str(tree)

# OTHER FUNCTIONS

def all_none(sequence) -> bool:
    return all(i is None for i in sequence)


