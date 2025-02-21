from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication

from vibra import app

# from vibra.interface.tabs.geometry_info_bar import GeometryInfoBar
from ..actors.section_plane_actor import SectionPlaneActor
from ..actors.faces_actor import FacesActor
from ..actors.lines_actor import LinesActor
from ..actors.points_actor import PointsActor
from ..actors.selection_spheres import SelectionSpheres
from ..actors.ghost_actor import GhostActor
from ..selection.geometry_selection import GeometrySelection


from molde.render_widgets import CommonRenderWidget
from molde.utils import TreeInfo
from molde.utils.format_sequences import format_long_sequence
from molde.interactor_styles import BoxSelectionInteractorStyle

import numpy as np
from numbers import Number

from vtkmodules.vtkCommonCore import vtkIntArray
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkRenderingCore import vtkActor, vtkCellPicker


SHOW_POINTS = 0
SHOW_LINES = 1
SHOW_FACES = 2

# fmt: off

class GeometryRenderWidget(CommonRenderWidget):
    selection_changed = pyqtSignal(set, set, set, set)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.set_interactor_style(BoxSelectionInteractorStyle())

        self.main_window = app().main_window
        self.view_mode = SHOW_FACES

        self.left_clicked.connect(self.click_callback)
        self.main_window.visualization_changed.connect(self.visualization_changed_callback)
        self.left_released.connect(self.selection_callback)
        self.main_window.selection_changed.connect(self.update_selection)
        self.main_window.theme_changed.connect(self.set_theme)
        self.main_window.section_plane.value_changed.connect(self.update_section_plane)

        self.geometry_selection = GeometrySelection(self)

        self.points_actor = None
        self.lines_actor = None
        self.faces_actor = None
        self.ghost_actor = None
        self.selection_spheres_actor = None
        self.selection_color = (20, 106, 245)

        # The fast area selection just works if it is on
        self.renderer.GetActiveCamera().ParallelProjectionOn()
        self.renderer.RemoveAllLights()

        self.create_axes()
        self.create_scale_bar()
        self.create_camera_light(0.1, 0.1)
        self.update_plot()

    def update_plot(self, reset_camera=True):
        mesh = app().project.model.mesh
        if mesh is None:
            return

        self.remove_all_actors()

        self.points_actor = PointsActor(mesh)
        self.lines_actor = LinesActor(mesh)
        self.faces_actor = FacesActor(mesh)
        self.selection_spheres_actor = SelectionSpheres()

        has_hidden_part = bool(self.main_window.hidden_surfaces)
        self.ghost_actor = GhostActor(mesh)
        self.ghost_actor.SetVisibility(has_hidden_part)

        self.plane_actor = SectionPlaneActor(self.faces_actor.GetBounds())
        self.plane_actor.VisibilityOff()

        self.add_actors(
            self.points_actor,
            self.lines_actor,
            self.faces_actor,
            self.selection_spheres_actor,
            self.ghost_actor,
            self.plane_actor,
        )

        if reset_camera:
            self.renderer.ResetCamera()

        self.visualization_changed_callback()
        self.update_section_plane()
        app().project.thumbnail = self.get_thumbnail()

    def visualization_changed_callback(self):
        if not self._actors_exists():
            return

        visualization = app().main_window.visualization_filter
        faces_opacity = 1 if visualization.faces else 0.1

        self.points_actor.SetVisibility(visualization.points)
        self.lines_actor.SetVisibility(visualization.lines)
        self.faces_actor.GetProperty().SetOpacity(faces_opacity)

        self.points_actor.SetPickable(visualization.faces)
        self.lines_actor.SetPickable(visualization.faces)
        self.faces_actor.SetPickable(visualization.faces)
        self.update()

    def update_hidden_plot(self):
        # We could just call the update_plot function,
        # but this is much simpler and faster
        if app().project is None:
            return

        model = app().project.model
        if model is None:
            return

        mesh = model.mesh
        if mesh is None:
            return

        if not self._actors_exists():
            self.update_plot()
            return

        self.renderer.RemoveActor(self.faces_actor)
        self.faces_actor = FacesActor(mesh)
        self.renderer.AddActor(self.faces_actor)

        has_hidden_part = bool(self.main_window.hidden_surfaces)
        self.ghost_actor.SetVisibility(has_hidden_part)

        self.update_section_plane()
        # self.update()

    #
    def click_callback(self, x, y):
        self.mouse_click = (x, y)

    def selection_callback(self, x, y):
        # This is a optimization, may have side effects
        if not self.isVisible():
            return

        if not self._actors_exists():
            return

        x0, y0 = self.mouse_click
        mouse_moved = (abs(x0 - x) > 10) or (abs(y0 - y) > 10)

        if mouse_moved:
            (
                picked_points,
                picked_lines,
                picked_faces,
                picked_volumes,
            ) = self.geometry_selection.area_pick(x0, y0, x, y)

        else:
            (
                picked_points,
                picked_lines,
                picked_faces,
                picked_volumes,
            ) = self.geometry_selection.pick(x, y)

        modifiers = QApplication.keyboardModifiers()
        ctrl_pressed = modifiers & Qt.ControlModifier
        shift_pressed = modifiers & Qt.ShiftModifier
        alt_pressed = modifiers & Qt.AltModifier

        if not shift_pressed:
            picked_volumes.clear()

        self.main_window.set_geometry_selection(
            points=picked_points,
            lines=picked_lines,
            surfaces=picked_faces,
            volumes=picked_volumes,
            join=ctrl_pressed,
            remove=alt_pressed,
        )

        self.update()

    def update_selection(self):
        self.points_actor.clear_colors()
        self.lines_actor.clear_colors()
        self.faces_actor.clear_colors()

        points = app().main_window.selected_geometry_points
        lines = app().main_window.selected_geometry_lines
        faces = app().main_window.selected_geometry_surfaces
        volumes = app().main_window.selected_geometry_volumes

        mesh = app().project.model.mesh

        # the cells are 0-indexed
        # but the points are 1-indexed
        point_cells = {i - 1 for i in points}

        # Get the line elements of all selected lines
        all_lines_elements = list()
        for line in lines:
            indexes = app().project.model.mesh.elements_from_line.get(line, [])
            all_lines_elements.extend(indexes)

        all_faces_elements = list()
        # Get the face elements of all selected faces
        for face in faces:
            indexes = mesh.elements_from_surface.get(face, [])
            all_faces_elements.extend(indexes)

        # Get the face elements of all selected volumes
        for volume in volumes:
            surfaces = app().project.model.mesh.surfaces_from_volumes[volume]
            for face in surfaces:
                indexes = app().project.model.mesh.elements_from_surface.get(face, [])
                all_faces_elements.extend(indexes)

        self.points_actor.paint_cells(self.selection_color, point_cells)
        self.lines_actor.paint_cells(self.selection_color, all_lines_elements)
        self.faces_actor.paint_cells(self.selection_color, all_faces_elements)

        self.update_info_text()

    def clear_selection_spheres(self):
        self.selection_spheres_actor.VisibilityOff()

    def set_selection_spheres(self, all_centers, all_radius):
        if self.selection_spheres_actor is None:
            return

        self.selection_spheres_actor.create_geometry(all_centers, all_radius)
        self.selection_spheres_actor.VisibilityOn()
        self.update()

    def update_section_plane(self):
        if not self._actors_exists():
            return

        section_plane = self.main_window.section_plane

        if not section_plane.cutting:
            self._disable_section_plane()
            return

        position = section_plane.get_position()
        rotation = section_plane.get_rotation()
        inverted = section_plane.get_inverted()

        if section_plane.editing:
            self.plane_actor.configure_section_plane(position, rotation)
            self.plane_actor.VisibilityOn()
            self.plane_actor.GetProperty().SetColor(0, 0.333, 0.867)
            self.plane_actor.GetProperty().SetOpacity(0.8)
            self.update()
        else:
            show_plane = not section_plane.keep_section_plane
            self._apply_section_plane(position, rotation, inverted, show_plane)

    def _disable_section_plane(self):
        has_hidden_part = bool(self.main_window.hidden_surfaces)
        self.ghost_actor.SetVisibility(has_hidden_part)
        self.plane_actor.VisibilityOff()
        self.points_actor.disable_cut()
        self.lines_actor.disable_cut()
        self.faces_actor.disable_cut()
        self.update()

    def _apply_section_plane(self, position, rotation, inverted, show_plane=True):
        self.plane_actor.configure_section_plane(position, rotation)
        xyz = self.plane_actor.calculate_xyz_position(position)
        normal = self.plane_actor.calculate_normal_vector(rotation)
        if inverted:
            normal = -normal

        self.points_actor.apply_cut(xyz, normal)
        self.faces_actor.apply_cut(xyz, normal)
        self.lines_actor.apply_cut(xyz, normal)

        self.ghost_actor.VisibilityOn()
        self.plane_actor.SetVisibility(show_plane)
        self.plane_actor.GetProperty().SetColor(0.5, 0.5, 0.5)
        self.plane_actor.GetProperty().SetOpacity(0.2)
        self.update()

    def remove_all_actors(self):
        super().remove_all_actors()
        self.nodes_actor = None
        self.edges_actor = None
        self.faces_actor = None
        self.solids_actor = None
        self.selection_spheres_actor = None
        self.plane_actor = None
        self.symbols_actor = None
        self.nodes_actor = None
        self.ghost_actor = None

    def _actors_exists(self):
        return len(self._widget_actors) > 0

    def update_info_text(self):
        text = ""
        text += self._points_info_text()
        text += self._lines_info_text()
        text += self._faces_info_text()
        text += self._volumes_info_text()
        text += self._surface_thickness_info_text()
        text += self._material_info_text()
        text += self._fluid_info_text()
        text += self._porous_material_info_text()
        text += self._acoustic_boundary_conditions_info_text()
        text += self._structural_boundary_conditions_info_text()

        self.set_info_text(text)
        self.update()

    def _points_info_text(self):
        points = list(self.main_window.selected_geometry_points)
        text = ""

        if len(points) > 1:
            text += f"{len(points)} points in selection\n{format_long_sequence(points)}\n\n"
        elif len(points) == 1:
            text += f"Point: {points[0]}\n\n"

        return text

    def _lines_info_text(self):
        lines = list(self.main_window.selected_geometry_lines)
        text = ""

        if len(lines) > 1:
            text += f"{len(lines)} lines in selection\n{format_long_sequence(lines)}\n\n"
        elif len(lines) == 1:
            text += f"Line: {lines[0]}\n\n"

        return text

    def _faces_info_text(self):
        text = ""
        volumes = list(self.main_window.selected_geometry_volumes)

        if len(volumes) == 0:
            faces = list(self.main_window.selected_geometry_surfaces)

            if len(faces) > 1:
                text += f"{len(faces)} surfaces in selection\n{format_long_sequence(faces)}\n\n"
            elif len(faces) == 1:
                text += f"Surface: {faces[0]}\n\n"

        return text

    def _volumes_info_text(self):
        volumes = list(self.main_window.selected_geometry_volumes)
        text = ""

        if len(volumes) > 1:
            text += f"{len(volumes)} volumes in selection\n{format_long_sequence(volumes)}\n\n"
        elif len(volumes) == 1:
            text += f"Volume: {volumes[0]}\n\n"

        return text

    def _surface_thickness_info_text(self):
        surfaces = list(self.main_window.selected_geometry_surfaces)
        text = ""

        if len(surfaces) == 1:
            surface_data = app().project.model.properties._get_property(
                "surface_thickness", surface=surfaces[0]
            )
        else:
            return text

        if surface_data is None:
            return text

        tree = TreeInfo("Shell data")
        tree.add_item("Thickness", surface_data["surface_thickness"], "m")
        tree.add_item("Offset", surface_data["thickness_offset"])

        text += str(tree)

        return text

    def _material_info_text(self):
        volumes = list(self.main_window.selected_geometry_volumes)
        surfaces = list(self.main_window.selected_geometry_surfaces)

        text = ""
        if len(volumes) != 1 and len(surfaces) != 1:
            return text

        elif len(volumes) == 1:
            material = app().project.model.properties.get_material(volume=volumes[0])

        elif len(surfaces) == 1:
            material = app().project.model.properties.get_material(surface=surfaces[0])

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

    def _fluid_info_text(self):
        volumes = list(self.main_window.selected_geometry_volumes)
        surfaces = list(self.main_window.selected_geometry_surfaces)

        text = ""
        if len(volumes) != 1 and len(surfaces) != 1:
            return text

        elif len(volumes) == 1:
            fluid = app().project.model.properties.get_fluid(volume=volumes[0])

        elif len(surfaces) == 1:
            fluid = app().project.model.properties.get_fluid(surface=surfaces[0])

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

    def _porous_material_info_text(self):
        volumes = list(self.main_window.selected_geometry_volumes)
        text = ""

        if len(volumes) != 1:
            return text

        pm_model = app().project.model.properties.get_porous_material_model_data(volume=volumes[0])
        if pm_model is None:
            return text

        tree = TreeInfo("Porous material")
        tree.add_item("Model", pm_model["model"])
        tree.add_item("Flow resistivity", pm_model["flow_resistivity"], "kg/m³s")

        text += str(tree)

        return text

    def _acoustic_boundary_conditions_info_text(self):
        text = ""
        selected_faces = list(self.main_window.selected_geometry_surfaces)

        if len(selected_faces) != 1:
            return text

        acoustic_pressure = app().project.model.properties._get_property("acoustic_pressure", surface=selected_faces[0])
        surface_velocity = app().project.model.properties._get_property("surface_velocity", surface=selected_faces[0])
        specific_impedance = app().project.model.properties._get_property("specific_impedance", surface=selected_faces[0])

        boundary_conditions_list = [acoustic_pressure, surface_velocity, specific_impedance]

        if all(condition is None for condition in boundary_conditions_list):
            return text

        if acoustic_pressure is not None:
            values = acoustic_pressure["values"][0]
            text += _acoustic_format("Acoustic pressure", values, "P", "Pa")

        if surface_velocity is not None:
            values = surface_velocity["values"][0]
            text += _acoustic_format("Surface velocity", values, "Vn", "m/s")

        if specific_impedance is not None:
            if "anechoic_termination" in specific_impedance.keys():
                fluid = app().project.model.properties.get_fluid(surface=selected_faces[0])
                density = fluid.fluid_density
                speed_of_sound = fluid.speed_of_sound
                values = np.array([density * speed_of_sound], dtype=complex)
                text += _acoustic_format("Specific impedance", values[0], "Zs", "kg/m².s", ("Impedance type", "anechoic (non-reflexive)"))

            else:
                values = surface_velocity["values"]
                text += _acoustic_format("Specific impedance", values[0], "Zs", "kg/m².s")

        return text

    def _structural_boundary_conditions_info_text(self):
        text = ""
        distributed_loads_line = None
        prescribed_dofs = None
        nodal_loads = None
        distributed_loads_area = None
        normal_pressure_load = None

        selected_faces = list(self.main_window.selected_geometry_surfaces)
        selected_lines = list(self.main_window.selected_geometry_lines)

        if len(selected_faces) == 1:
            prescribed_dofs = app().project.model.properties._get_property("prescribed_dofs", surface=selected_faces[0])
            nodal_loads = app().project.model.properties._get_property("nodal_loads", surface=selected_faces[0])
            distributed_loads_area = app().project.model.properties._get_property("distributed_loads", surface=selected_faces[0])
            normal_pressure_load = app().project.model.properties._get_property("normal_pressure_load", surface=selected_faces[0])

        elif len(selected_lines) == 1:
            distributed_loads_line = app().project.model.properties._get_property("distributed_loads", line=selected_lines[0])

        else:
            return text

        boundary_conditions = [prescribed_dofs, nodal_loads, distributed_loads_area, normal_pressure_load, distributed_loads_line]

        if all(bc is None for bc in boundary_conditions):
            return text

        if prescribed_dofs is not None:
            values = prescribed_dofs["values"]
            loaded_table = "table_names" in prescribed_dofs.keys()
            text += _structural_format(
                "Prescribed dofs", values, ("u", "r"), ("m", "rad"), loaded_table
            )

        if nodal_loads is not None:
            values = nodal_loads["values"]
            loaded_table = "table_names" in nodal_loads.keys()
            text += _structural_format("Nodal loads",  values, ("F", "M"), ("N", "N.m"), loaded_table)

        if distributed_loads_area is not None:
            values = distributed_loads_area["values"]
            loaded_table = "table_names" in distributed_loads_area.keys()
            text += _structural_format("Distributed loads",  values, ["P"], ["N/m²"], loaded_table)

        if distributed_loads_line is not None:
            values = distributed_loads_line["values"]
            loaded_table = "table_names" in distributed_loads_line.keys()
            text += _structural_format("Distributed loads",  values, ["P"], ["N/m"], loaded_table)

        if normal_pressure_load is not None:
            values = normal_pressure_load["values"]
            loaded_table = "table_names" in normal_pressure_load.keys()
            text += _structural_format("Normal pressure",  values, ["P"], ["N/m²"], loaded_table)

        return text


def _all_none(sequence) -> bool:
    return all(i is None for i in sequence)


def _structural_format(property_name, values, labels, units, has_table):
    if _all_none(values):
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


def _acoustic_format(property_name, value, label, unit, additional_labels=[]):
    tree = TreeInfo(property_name)
    if isinstance(value, Number | str | float | complex):
        tree.add_item(label, np.round(value, 4), unit)
    else:
        tree.add_item(label, "Table of values")

    if len(additional_labels) == 2:
        tree.add_item(additional_labels[0], additional_labels[1])

    return str(tree)

# fmt: on