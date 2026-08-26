
from numbers import Number

import numpy as np
from molde.utils import TreeInfo
from molde.utils.format_sequences import format_long_sequence

from vibra import app
from vibra.engine import AnalysisID
from vibra.engine.properties.fluid import Fluid
from vibra.engine.properties.material import Material
from vibra.utils.utils import are_there_values_different_from_zero


# GEOMETRY RENDER WIDGET INFO TEXTS
def points_info_text():

    mesh = app().project.model.mesh

    selected_points = app().main_window.selection.geometry_points
    node_ids = [mesh.nodes_from_points.get(point_id) for point_id in selected_points]
    point_ids = list(selected_points)

    if len(node_ids) == 0:
        return ""

    text = ""

    if len(point_ids) == 1:
        coords = mesh.nodal_coordinates[node_ids[0], 1:].round(6)
        tree = TreeInfo(f"POINT {point_ids[0]}")
        tree.add_item("Position", "({:.6f}, {:.6f}, {:.6f})".format(*coords), "m")
        text += str(tree)

    elif len(point_ids) == 2:
        coord_A = mesh.nodal_coordinates[node_ids[0], 1:]
        coord_B = mesh.nodal_coordinates[node_ids[1], 1:]
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
    line_ids = list(app().main_window.selection.geometry_lines)

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

    else:
        sequence = ", ".join(str(i) for i in line_ids)
        if len(sequence) > 20:
            sequence = sequence[:20 - 4] + " ..."

        tree = TreeInfo(f"{len(line_ids)} LINES IN SELECTION: {sequence}")
        tree.add_item("Length (compound)", f"{length : .6e}", "m")

    text += str(tree)
    return text


def faces_info_text():
    volumes = list(app().main_window.selection.geometry_volumes)

    if len(volumes) != 0:
        return ""
    
    surface_ids = list(app().main_window.selection.geometry_surfaces)

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

        surface_data = app().project.model.properties._get_property("surface_thickness", surface=surface_ids[0])
        if isinstance(surface_data, dict):
            tree.add_item("Thickness", surface_data["surface_thickness"], "m")
            tree.add_item("Offset", surface_data["thickness_offset"])

        diameter = app().project.model.mesh.cylindrical_surfaces_data.get(surface_ids[0])
        if isinstance(diameter, float):
            tree.add_item("Diameter", f"{diameter : .6e}", "m")

    else:
        sequence = ", ".join(str(i) for i in surface_ids)
        if len(sequence) > 20:
            sequence = sequence[:20 - 4] + " ..."

        tree = TreeInfo(f"{len(surface_ids)} SURFACES IN SELECTION: {sequence}")
        tree.add_item("Area (compound)", f"{area : .6e}", "m²")

    text += str(tree)

    return text


def volumes_info_text():
    volume_ids = list(app().main_window.selection.geometry_volumes)
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
            material_density = material.material_density
            material_mass += volume * material_density
    
    return volume_compound, fluid_mass, material_mass


def material_info_text():
    volumes = list(app().main_window.selection.geometry_volumes)
    surfaces = list(app().main_window.selection.geometry_surfaces)

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
    tree.add_item("Density", material.material_density, "kg/m³")
    tree.add_item("Elasticity modulus", material.elasticity_modulus / 1e9, "GPa")
    tree.add_item("Poisson ratio", material.poisson_ratio, "--")
    tree.add_item("Thermal expasion coefficient", material.thermal_expansion_coefficient, "1/K")

    text += str(tree)

    return text


def fluid_info_text():
    volumes = list(app().main_window.selection.geometry_volumes)
    surfaces = list(app().main_window.selection.geometry_surfaces)

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


def proportional_damping_info_text():
    volumes = list(app().main_window.selection.geometry_volumes)
    text = ""

    if len(volumes) != 1:
        return text

    pd_data = app().project.model.properties._get_property(
        "proportional_damping", volume=volumes[0]
    )
    if not isinstance(pd_data, dict):
        return text

    tree = TreeInfo("Proportional damping")

    speed_factor = pd_data.get("speed_of_sound_factor")
    if speed_factor:
        tree.add_item("Speed of sound factor", pd_data.get("speed_of_sound_factor", ""))

    density_factor = pd_data.get("density_factor")
    if density_factor:
        tree.add_item("Density factor", pd_data.get("density_factor", ""))

    return str(tree)


def porous_material_info_text():
    volumes = list(app().main_window.selection.geometry_volumes)
    text = ""

    if len(volumes) != 1:
        return text

    pm_model = app().project.model.properties._get_property(
        "porous_material_model", volume=volumes[0]
    )
    if not isinstance(pm_model, dict):
        return text

    tree = TreeInfo("Porous material model")
    tree.add_item("Model", pm_model.get("model", ""))
    tree.add_item("Flow resistivity", pm_model.get("flow_resistivity", ""), "kg/m³s")

    return str(tree)


def viscous_thermal_info_text():
    volumes = list(app().main_window.selection.geometry_volumes)
    text = ""

    if len(volumes) != 1:
        return text

    vt_model = app().project.model.properties._get_property(
        "viscous_thermal_model", volume=volumes[0]
    )
    if not isinstance(vt_model, dict):
        return text

    tree = TreeInfo("Viscous-thermal loss model")
    tree.add_item("Formulation", vt_model.get("formulation", ""))
    tree.add_item("Section type", vt_model.get("section_type"))

    return str(tree)


def perforated_plate_info_text():

    text = ""
    surfaces = list(app().main_window.selection.geometry_surfaces)

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
        tree.add_item("Plate thickness", pp_data.get("plate_thickness"), "m")
        tree.add_item("Hole diameter", pp_data.get("hole_diameter"), "m")
        tree.add_item("Porosity", pp_data.get("porosity"), "--")
        tree.add_item("Linear discharge coefficient", pp_data.get("linear_discharge_coefficient"), "--")

        if "non_linear_discharge_coefficient" in pp_data:
            tree.add_item("Non-linear discharge coefficient", pp_data.get("non_linear_discharge_coefficient"), "--")
            tree.add_item("Non-linear correction factor", pp_data.get("non_linear_correction_factor"), "--")

        if "table_names" in pp_data:
            tree.add_item("User-defined transfer impedance", "active")

    text += str(tree)

    return text


def acoustic_boundary_conditions_info_text():
    text = ""
    selected_faces = list(app().main_window.selection.geometry_surfaces)

    if len(selected_faces) != 1:
        return text
    
    surface_id = selected_faces[0]
    properties = app().project.model.properties

    acoustic_pressure = properties._get_property("acoustic_pressure", surface=surface_id)
    surface_velocity = properties._get_property("surface_velocity", surface=surface_id)
    compressor_excitation_spectrum = properties._get_property("compressor_excitation_spectrum", surface=surface_id)
    compressor_excitation_waveform = properties._get_property("compressor_excitation_waveform", surface=surface_id)
    recip_compressor_excitation = properties._get_property("reciprocating_compressor_excitation", surface=surface_id)
    incident_plane_wave = properties._get_property("incident_plane_wave", surface=surface_id)
    absorption_surface = properties._get_property("absorption_surface", surface=surface_id)
    specific_impedance = properties._get_property("specific_impedance", surface=surface_id)

    properties_data = [
        acoustic_pressure,
        surface_velocity,
        compressor_excitation_spectrum,
        compressor_excitation_waveform,
        recip_compressor_excitation,
        incident_plane_wave,
        absorption_surface,
        specific_impedance,
        ]

    if all(condition is None for condition in properties_data):
        return text

    if acoustic_pressure is not None:
        values = acoustic_pressure["values"][0]
        text += acoustic_format("Acoustic pressure", values, "P", "Pa")

    if surface_velocity is not None:
        values = surface_velocity["values"][0]
        text += acoustic_format("Surface velocity", values, "Vn", "m/s")

    if isinstance(compressor_excitation_spectrum, dict):
        text += get_compressor_excitation_spectrum(compressor_excitation_spectrum)

    if isinstance(compressor_excitation_waveform, dict):
        text += get_compressor_excitation_waveform(compressor_excitation_waveform)

    if isinstance(recip_compressor_excitation, dict):
        text += get_reciprocating_compressor_text(recip_compressor_excitation)

    if isinstance(incident_plane_wave, dict):
        text += get_incident_plane_wave_text(incident_plane_wave)

    if absorption_surface is not None:
        values = absorption_surface["values"][0]
        text += acoustic_format("Absorption surface", values, "alpha", "--")

    if isinstance(specific_impedance, dict):
        text += get_specific_and_anechoic_impedance_text(selected_faces[0], specific_impedance)

    return text


def get_incident_plane_wave_text(ipw_data: dict):

    if ipw_data is None:
        return ""

    value = ipw_data["values"][0]
    tree_pw = TreeInfo("Incident plane wave")
    if isinstance(value, Number | str | float | complex):
        tree_pw.add_item("P_inc", np.round(value, 4), "Pa")
    else:
        tree_pw.add_item("P_inc", "Table")

    ipw_vector = ipw_data["ipw_vector"]
    tree_pw.add_item("Incident wave vector", np.round(ipw_vector, 4))

    return str(tree_pw)

def get_compressor_excitation_spectrum(data: dict):
    tree_ec = TreeInfo("Compressor excitation")
    tree_ec.add_item("Data domain", "frequency")
    tree_ec.add_item("Compressor type", data.get("compressor_type"))
    tree_ec.add_item("Connection type", data.get("connection_type"))
    tree_ec.add_item("Excitation type", data.get("excitation_type"), data.get("excitation_units"))

    return str(tree_ec)


def get_compressor_excitation_waveform(data: dict):
    tree_ec = TreeInfo("Compressor excitation")
    tree_ec.add_item("Data domain", "time")
    tree_ec.add_item("Data source", data.get("data_source"))
    tree_ec.add_item("Compressor type", data.get("compressor_type"))
    tree_ec.add_item("Connection type", data.get("connection_type"))
    tree_ec.add_item("Excitation type", data.get("excitation_type"), data.get("excitation_units"))
    tree_ec.add_item("Excitation mapping", data.get("excitation_mapping"))
    tree_ec.add_item("Angular resolution", data.get("angular_resolution"), "deg")

    return str(tree_ec)


def get_reciprocating_compressor_text(rc_data: dict):

    rc_parameters = rc_data.get("parameters", dict)
    if not isinstance(rc_parameters, dict):
        return ""

    acting_label = ""
    acting_labels = ["both ends", "head end", "crank end"]

    # ensure the backwards compatibility
    for key in ["acting_mode", "acting_head", "acting_label"]:
        value = rc_parameters.get(key)
        if value is None:
            continue

        elif isinstance(value, int):
            acting_label = acting_labels[value]
            break

        elif isinstance(value, str):
            acting_label = value
            break
    
    acting_label = acting_label.replace("_", " ")
    pressure_unit = rc_parameters.get("pressure_unit", "")
    temperature_unit = rc_parameters.get("temperature_unit", "")

    comp_stg_value = rc_parameters.get("compression_stage")
    if isinstance(comp_stg_value, int):
        compression_labels = ["1st stage", "2nd stage", "3rd stage"]
        compression_stage = compression_labels[comp_stg_value]
    else:
        compression_stage = rc_parameters.get("compression_stage", "unknown")

    tdc_crank_angle = 0
    for key in ["tdc_crank_angle", "TDC_crank_angle", "TDC_crank_angle_1"]:
        value = rc_parameters.get(key)
        if isinstance(value, float):
            tdc_crank_angle = value
            break

    tree_rc = TreeInfo("Reciprocating compressor")
    tree_rc.add_item("Connection", rc_data.get("connection_type", ""))
    tree_rc.add_item("Compression stage", compression_stage)
    tree_rc.add_item("Valves per head", rc_parameters.get("valves_per_head", "1"))
    tree_rc.add_item("Acting head", acting_label)

    if acting_label in ["head end", "both ends"]:
        tree_rc.add_item("HE clearance", rc_parameters.get("clearance_HE", ""), "%")

    if acting_label in ["crank end", "both ends"]:
        tree_rc.add_item("CE clearance", rc_parameters.get("clearance_CE", ""), "%")

    tree_rc.add_item("Bore diameter", rc_parameters.get("bore_diameter", ""), "m")
    tree_rc.add_item("Stroke", rc_parameters.get("stroke", ""), "m")
    tree_rc.add_item("Connecting rod length", rc_parameters.get("connecting_rod_length", ""), "m")

    if acting_label in ["crank end", "both ends"]:
        tree_rc.add_item("Rod diameter", rc_parameters.get("rod_diameter", ""), "m")

    tree_rc.add_item("TDC angle", tdc_crank_angle, "deg")
    tree_rc.add_item("Capacity", rc_parameters.get("capacity", ""), "%")

    suction_pressure = ""
    for key in ["suction_pressure", "pressure_at_suction"]:
        suction_pressure = rc_parameters.get(key)
    
    suction_temperature = ""
    for key in ["suction_temperature", "temperature_at_suction"]:
        suction_temperature = rc_parameters.get(key)

    tree_rc.add_item("Suction pressure", suction_pressure, pressure_unit.replace(" ", ""))
    tree_rc.add_item("Suction temperature", suction_temperature, temperature_unit)
    tree_rc.add_item("Rotational speed", rc_parameters.get("rotational_speed", ""), "rpm")
    tree_rc.add_item("Pressure ratio", rc_parameters.get("pressure_ratio", ""), "--")

    return str(tree_rc)


def get_specific_and_anechoic_impedance_text(surface: int, si_data: dict):
    text = ""
    properties = app().project.model.properties
    if "anechoic_termination" in si_data:
        fluid = properties._get_property("fluid", surface=surface)
        if isinstance(fluid, Fluid):
            density = fluid.fluid_density
            speed_of_sound = fluid.speed_of_sound
            values = np.array([density * speed_of_sound], dtype=complex)
            text = acoustic_format(
                "Specific impedance",
                values[0],
                "Zs",
                "kg/m².s",
                ("Impedance type", "anechoic (non-reflexive)"),
            )

    else:
        values = si_data["values"]
        text = acoustic_format("Specific impedance", values[0], "Zs", "kg/m².s")

    return text


def get_mass_source_text(**kwargs):
    properties = app().project.model.properties
    mass_source = properties._get_property("mass_source", **kwargs)
    if mass_source is None:
        return ""

    if isinstance(kwargs.get("volume"), Number):
        unit_label = "kg/m³.s"
    elif isinstance(kwargs.get("surface"), Number):
        unit_label = "kg/m².s"
    elif isinstance(kwargs.get("line"), Number):
        unit_label = "kg/m.s"
    elif isinstance(kwargs.get("point"), Number):
        unit_label = "kg/s"
    elif isinstance(kwargs.get("node"), Number):
        unit_label = "kg/s"
    else:
        return ""

    values = mass_source.get("values")[0]
    return acoustic_format("Mass source", values, "Qm", unit_label)


def mass_source_info_text():
    text = ""
    selected_volumes = list(app().main_window.selection.geometry_volumes)
    selected_surfaces = list(app().main_window.selection.geometry_surfaces)
    selected_lines = list(app().main_window.selection.geometry_lines)
    selected_points = list(app().main_window.selection.geometry_points)
    selected_nodes = list(app().main_window.selection.mesh_nodes)

    if len(selected_volumes) == 1:
        return get_mass_source_text(volume=selected_volumes[0])
    if len(selected_surfaces) == 1:
        return get_mass_source_text(surface=selected_surfaces[0])
    if len(selected_lines) == 1:
        return get_mass_source_text(line=selected_lines[0])
    if len(selected_points) == 1:
        return get_mass_source_text(point=selected_points[0])
    if len(selected_nodes) == 1:
        return get_mass_source_text(node=selected_nodes[0])
    else:
        return text


def structural_boundary_conditions_info_text():
    text = ""
    distributed_loads_line = None
    prescribed_dof = None
    nodal_loads = None
    distributed_loads_area = None
    normal_pressure_load = None

    selected_faces = list(app().main_window.selection.geometry_surfaces)
    selected_lines = list(app().main_window.selection.geometry_lines)

    if len(selected_faces) == 1:
        prescribed_dof = app().project.model.properties._get_property(
            "prescribed_dof", surface=selected_faces[0]
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

    properties = [
        prescribed_dof,
        nodal_loads,
        distributed_loads_area,
        normal_pressure_load,
        distributed_loads_line,
    ]

    if all(prop_data is None for prop_data in properties):
        return text

    if isinstance(prescribed_dof, dict):
        values = prescribed_dof.get("values")
        n_int = prescribed_dof.get("integrate", 0)
        loaded_table = "table_names" in prescribed_dof

        if are_there_values_different_from_zero(values):
            property_label = "Prescribed DOF"
        else:
            property_label = "Constrained DOF"

        prefixes_dtype = ["u", "v", "a"]
        prefix_dtype = prefixes_dtype[n_int]
        dtypes = (prefix_dtype, f"{prefixes_dtype}r")

        unit_suffixes = ["", "/s", "/s²"]
        suffix_unit = unit_suffixes[n_int]        
        units = (f"m{suffix_unit}", f"rad{suffix_unit}")

        text += structural_format(property_label, values, dtypes, units, loaded_table)

    if isinstance(nodal_loads, dict):
        values = nodal_loads.get("values")
        loaded_table = "table_names" in nodal_loads
        text += structural_format(
            "Nodal loads", values, ("F", "M"), ("N", "N.m"), loaded_table
        )

    if isinstance(distributed_loads_area, dict):
        values = distributed_loads_area.get("values")
        loaded_table = "table_names" in distributed_loads_area
        text += structural_format("Distributed loads", values, ["P"], ["N/m²"], loaded_table)

    if isinstance(distributed_loads_line, dict):
        values = distributed_loads_line.get("values")
        loaded_table = "table_names" in distributed_loads_line
        text += structural_format("Distributed loads", values, ["P"], ["N/m"], loaded_table)

    if isinstance(normal_pressure_load, dict):
        values = normal_pressure_load.get("values")
        loaded_table = "table_names" in normal_pressure_load
        text += structural_format("Normal pressure", values, ["P"], ["N/m²"], loaded_table)

    return text


def structural_additional_info_text():
    text = ""
    distributed_mass_1d = None
    distributed_mass_2d = None

    selected_faces = list(app().main_window.selection.geometry_surfaces)
    selected_lines = list(app().main_window.selection.geometry_lines)

    if len(selected_faces) == 1:
        distributed_mass_2d = app().project.model.properties._get_property(
            "distributed_mass", surface=selected_faces[0]
        )

    elif len(selected_lines) == 1:
        distributed_mass_1d = app().project.model.properties._get_property(
            "distributed_mass", line=selected_lines[0]
        )

    else:
        return text

    properties = [
        distributed_mass_2d,
        distributed_mass_1d,
    ]

    if all(prop_data is None for prop_data in properties):
        return text

    if isinstance(distributed_mass_2d, dict):
        real_value = [value.real for value in distributed_mass_2d.get("values")]
        loaded_table = "table_names" in distributed_mass_2d
        text += structural_format("Distributed mass (area)", real_value, ["M"], ["kg"], loaded_table)

    if isinstance(distributed_mass_1d, dict):
        real_value = [value.real for value in distributed_mass_2d.get("values")]
        loaded_table = "table_names" in distributed_mass_1d
        text += structural_format("Distributed mass (line)", real_value, ["M"], ["kg"], loaded_table)

    return text


def acoustic_format(property_name, value, label, unit, additional_labels=[]):
    tree = TreeInfo(property_name)
    if isinstance(value, Number | str | float | complex):
        tree.add_item(label, np.round(value, 4), unit)
    else:
        tree.add_item(label, "Table")

    if len(additional_labels) == 2:
        tree.add_item(additional_labels[0], additional_labels[1])

    return str(tree)


# MESH RENDER WIDGET INFO TEXTS

def nodes_info_text():
    text = ""
    node_ids = list(app().main_window.selection.mesh_nodes)

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
    faces = list(app().main_window.selection.mesh_faces)

    if len(faces) > 1:
        text += f"{len(faces)} FACES IN SELECTION:\n"
        text += f"{format_long_sequence(faces)}\n\n"

    elif len(faces) == 1:
        text += f"FACE ELEMENT {faces[0]}\n\n"

    return text


def mesh_solids_info_text():
    text = ""
    solids_elem_ids = list(app().main_window.selection.mesh_solids)
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
    elements = list(app().main_window.selection.mesh_faces)
    text = ""

    if not elements:
        elements = list(app().main_window.selection.mesh_solids)

    if len(elements) == 1:
        current_solid = app().project.model.mesh.get_volume_from_element(elements[0])
        material = app().project.model.properties._get_property("material", volume=current_solid)
        if not isinstance(material, Material):
            return text

        tree = TreeInfo("Material")
        tree.add_item("Name", material.name)
        tree.add_item("Identifier", material.identifier)
        tree.add_item("Density", material.material_density, "kg/m³")
        tree.add_item("Elasticity Modulus", material.elasticity_modulus / 1e9, "GPa")
        tree.add_item("Poisson Ratio", material.poisson_ratio, "--")
        tree.add_item(
            "Thermal Expasion Coefficient", material.thermal_expansion_coefficient, "1/K"
        )

        text += str(tree)

    return text


def mesh_fluid_info_text():
    elements = list(app().main_window.selection.mesh_faces)
    text = ""

    if not elements:
        elements = list(app().main_window.selection.mesh_solids)

    if len(elements) == 1:
        current_solid = app().project.model.mesh.get_volume_from_element(elements[0])
        fluid = app().project.model.properties._get_property("fluid", volume=current_solid)
        if not isinstance(fluid, Fluid):
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
    selected_nodes = list(app().main_window.selection.mesh_nodes)

    if len(selected_nodes) != 1:
        return text

    prescribed_dof = app().project.model.properties._get_property(
        "prescribed_dof", node=selected_nodes[0]
    )
    nodal_loads = app().project.model.properties._get_property(
        "nodal_loads", node=selected_nodes[0]
    )
    boundary_conditions_list = [prescribed_dof, nodal_loads]

    if all(condition is None for condition in boundary_conditions_list):
        return text

    if isinstance(prescribed_dof, dict):
        values = prescribed_dof["values"]
        n_int = prescribed_dof.get("integrate", 0)
        loaded_table = "table_names" in prescribed_dof

        if are_there_values_different_from_zero(values):
            property_label = "Prescribed DOF"
        else:
            property_label = "Constrained DOF"

        prefixes_dtype = ["u", "v", "a"]
        prefix_dtype = prefixes_dtype[n_int]
        dtypes = (prefix_dtype, f"{prefixes_dtype}r")

        unit_suffixes = ["", "/s", "/s²"]
        suffix_unit = unit_suffixes[n_int]        
        units = (f"m{suffix_unit}", f"rad{suffix_unit}")

        text += structural_format(property_label, values, dtypes, units, loaded_table)

    if nodal_loads is not None:
        values = nodal_loads["values"]
        loaded_table = "table_names" in nodal_loads
        text += structural_format(
            "Nodal loads", values, ("F", "M"), ("N", "N.m"), loaded_table
        )

    return text


def mesh_structural_format(property_name, values, labels, units, has_table):
    if all_none(values):
        return ""

    u_values = []
    u_labels = []
    for val, label in zip(values[:3], "xyz"):
        if val is None:
            continue

        if not isinstance(val, Number | complex | str):
            val = "table"

        u_values.append(val)
        u_labels.append(labels[0] + label)

    r_values = []
    r_labels = []
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
            tree.add_item(", ".join(u_labels), "Table")
        if r_values:
            tree.add_item(", ".join(r_labels), "Table")

    else:
        if u_values:
            tree.add_item(", ".join(u_labels), u_values, units[0])
        if r_values:
            tree.add_item(", ".join(r_labels), r_values, units[1])

    return str(tree)

def problematic_nodes_info_text(self):
    ...
    
# RESULTS RENDER WIDGET INFO TEXTS

def analysis_info_text(frequency_index: int):

    project = app().project
    if not project.is_there_a_valid_solution():
        return ""

    analysis_setup = project.model.analysis_setup
    analysis_id = analysis_setup.analysis_id

    if analysis_id == AnalysisID.NO_ANALYSIS:
        return ""

    display_name = {
        AnalysisID.ACOUSTIC_MODAL : "Acoustic Modal Analysis",
        AnalysisID.STRUCTURAL_MODAL : "Structural Modal Analysis",
        AnalysisID.ACOUSTIC_HARMONIC : "Acoustic Harmonic Analysis",
        AnalysisID.STRUCTURAL_HARMONIC : "Structural Harmonic Analysis",
        AnalysisID.COUPLED_HARMONIC : "Coupled Harmonic Analysis",
        }

    tree = TreeInfo(display_name.get(analysis_id))

    if AnalysisID(analysis_id).is_modal():

        ## modal analysis info texts

        solution = project.model.solution
        if solution is None:
            return ""

        frequencies = None
        if analysis_id == AnalysisID.STRUCTURAL_MODAL:
            frequencies = solution.natural_frequencies

        if analysis_id == AnalysisID.ACOUSTIC_MODAL:
            if isinstance(solution.complex_natural_frequencies, np.ndarray) and solution.complex_natural_frequencies.size:
                frequencies = list(solution.complex_natural_frequencies)
            else:
                frequencies = list(solution.natural_frequencies)

        if frequencies is None:
            return ""

        if frequency_index >= len(frequencies):
            print(f"frequency index: {frequency_index}")
            print(f"frequencies: {frequencies}")
            return ""

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

        ## harmonic analysis info texts

        frequencies = project.model.solution.frequencies
        if frequencies is None:
            return ""

        if frequency_index >= len(frequencies):
            return ""

        analysis_method = analysis_setup.analysis_method.replace("_", " ")
        tree.add_item("Method", analysis_method)

        frequency = frequencies[frequency_index]
        tree.add_item("Frequency", f"{frequency:.4f}", "Hz")

    return str(tree)


def allowable_pulsation_for_screw_compressor_info_text(value: float, penalization_factor: int):
    analysis_setup = app().project.model.analysis_setup
    analysis_id = analysis_setup.analysis_id
    if AnalysisID.ACOUSTIC_HARMONIC != analysis_id:
        return ""

    tree = TreeInfo("Allowable pulsation for screw compressor systems")
    tree.add_item("Allowable level (p-p)", value, "kPa")
    tree.add_item("Penalization factor", penalization_factor, "%")

    return str(tree)


def structural_format(property_name, values, labels, units, has_table):
    if all_none(values):
        return ""

    if property_name == "Normal pressure":
        sufix_labels = "n"
    elif "Distributed mass" in property_name:
        sufix_labels = "d"
    else:
        sufix_labels = "xyz"

    u_values = []
    u_labels = []
    for val, label in zip(values[:3], sufix_labels):
        if val is None:
            continue

        if not isinstance(val, Number | complex | str):
            val = "table"

        u_values.append(val)
        u_labels.append(labels[0] + label)

    r_values = []
    r_labels = []
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
            tree.add_item(", ".join(u_labels), "Table")

        if r_values:
            tree.add_item(", ".join(r_labels), "Table")

    else:
        if u_values:
            tree.add_item(", ".join(u_labels), u_values, units[0])

        if r_values:
            tree.add_item(", ".join(r_labels), r_values, units[1])

    return str(tree)

# OTHER FUNCTIONS

def all_none(sequence) -> bool:
    return all(i is None for i in sequence)


