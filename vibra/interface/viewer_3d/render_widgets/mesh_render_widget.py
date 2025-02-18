from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication

from vibra import app
# from vibra.interface.tabs.mesh_info_bar import MeshInfoBar
from ..actors.section_plane_actor import SectionPlaneActor
from ..actors.edges_actor import EdgesActor
from ..actors.faces_actor import FacesActor
from ..actors.nodes_actor import NodesActor
from ..actors.solids_actor import SolidsActor
from ..actors.hollow_solids_actor import HollowSolidsActor
from ..actors.selection_spheres import SelectionSpheres
from ..actors.symbols.symbols_actor import SymbolsActor
from ..actors.ghost_actor import GhostActor
from ..selection.mesh_selection import MeshSelection

from molde.render_widgets import CommonRenderWidget
from molde.utils import TreeInfo
from molde.utils.format_sequences import format_long_sequence
from molde.interactor_styles import BoxSelectionInteractorStyle

import numpy as np
from numbers import Number

from vtkmodules.vtkCommonCore import vtkIntArray
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkRenderingCore import vtkActor, vtkCellPicker


# SHOW_POINTS = 0
# SHOW_LINES = 1
# SHOW_FACES = 2
# SHOW_VOLUMES = 3


class MeshRenderWidget(CommonRenderWidget):
    selection_changed = pyqtSignal(list, list, list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.set_interactor_style(BoxSelectionInteractorStyle())
        self.mouse_click = (0, 0)

        self.main_window = app().main_window
        self.selection_color = (20, 106, 245)

        self.left_clicked.connect(self.click_callback)
        self.left_released.connect(self.selection_callback)
        self.main_window.selection_changed.connect(self.update_selection)
        self.main_window.theme_changed.connect(self.set_theme)
        self.main_window.section_plane.value_changed.connect(self.update_section_plane)

        self.mesh_selection = MeshSelection(self)
        self.section_plane_active = False
        self.section_plane_args = tuple()

        self.nodes_actor = None
        self.faces_actor = None
        self.solids_actor = None
        self.edges_actor = None
        self.selection_spheres_actor = None
        self.ghost_actor = None
        self.plane_actor = None
        self.symbols_actor = None

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

        self.mesh_selection.precompute_data()
        self.remove_all_actors()

        # TODO: load the mesh directly inside the actors
        self.nodes_actor = NodesActor(mesh)
        self.faces_actor = FacesActor(mesh)
        self.edges_actor = EdgesActor(self.faces_actor.data)
        self.solids_actor: SolidsActor | HollowSolidsActor = HollowSolidsActor(mesh)
        # self.solids_actor: SolidsActor | HollowSolidsActor = SolidsActor(mesh)
        self.symbols_actor = SymbolsActor(self.renderer)
        self.selection_spheres_actor = SelectionSpheres()

        has_hidden_part = bool(self.main_window.hidden_surfaces)
        self.ghost_actor = GhostActor(mesh)
        self.ghost_actor.SetVisibility(has_hidden_part)

        self.plane_actor = SectionPlaneActor(self.faces_actor.GetBounds())
        self.plane_actor.VisibilityOff()

        self.add_actors(
            self.nodes_actor,
            self.edges_actor,
            # self.faces_actor,
            self.solids_actor,
            self.ghost_actor,
            self.plane_actor,
            self.symbols_actor,
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
        has_hidden_part = bool(self.main_window.hidden_surfaces)

        self.nodes_actor.SetVisibility(visualization.points)
        self.edges_actor.SetVisibility(visualization.lines)
        self.faces_actor.SetVisibility(False)
        self.ghost_actor.SetVisibility(has_hidden_part)
        self.solids_actor.SetVisibility(visualization.solids)

        self.update()

    def update_symbols(self):
        self.remove_actors(self.symbols_actor)
        self.symbols_actor = SymbolsActor(self.renderer)
        self.add_actors(self.symbols_actor)

    def update_hidden_plot(self):
        self.update_plot(reset_camera=False)
        return 
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

        self.renderer.RemoveActor(self.solids_actor)
        self.solids_actor = SolidsActor(mesh)
        self.renderer.AddActor(self.solids_actor)

        self.renderer.RemoveActor(self.edges_actor)
        self.edges_actor = EdgesActor(self.solids_actor.data)
        self.edges_actor.GetProperty().SetColor(0, 0, 0)
        self.renderer.AddActor(self.edges_actor)

        has_hidden_part = bool(self.main_window.hidden_surfaces)
        self.ghost_actor.SetVisibility(has_hidden_part)

        # has_hidden_part = bool(self.main_window.hidden_surfaces)
        # faces_alpha = 12 if has_hidden_part else 0
        # self.faces_actor.clear_colors((255, 255, 255, faces_alpha))

        self.update_section_plane()

    # TODO: replace these methods to use flags
    # Then, combinations of these visualizations will be valid
    def show_points(self):
        return
        self.view_mode = SHOW_POINTS
        self.nodes_actor.VisibilityOn()
        self.edges_actor.VisibilityOff()
        self.faces_actor.VisibilityOff()
        self.solids_actor.VisibilityOff()
        self.update()

    def show_lines(self):
        return
        self.view_mode = SHOW_LINES
        self.nodes_actor.VisibilityOn()
        self.edges_actor.VisibilityOn()
        self.faces_actor.VisibilityOff()
        self.solids_actor.VisibilityOff()
        self.update()

    def show_faces(self):
        return
        self.view_mode = SHOW_FACES
        self.nodes_actor.VisibilityOn()
        self.edges_actor.VisibilityOn()
        self.faces_actor.VisibilityOn()
        self.solids_actor.VisibilityOn()
        self.edges_actor.GetProperty().SetColor(0, 0, 0)
        self.update()

    def show_volumes(self):
        return
        self.view_mode = SHOW_VOLUMES
        self.nodes_actor.VisibilityOn()
        self.edges_actor.VisibilityOn()
        self.faces_actor.VisibilityOff()
        self.solids_actor.VisibilityOn()
        self.edges_actor.GetProperty().SetColor(0, 0, 0)
        self.update()

    def set_theme(self, theme):
        super().set_theme(theme)
        return

        try:
            if not self._actors_exists():
                return
        except AttributeError:
            return

        light_color = (1, 1, 1)
        dark_color = (0, 0, 0)

        # It it is showing faces, the colors are fixed
        # otherwise it should follow the theme
        if self.view_mode in (SHOW_FACES, SHOW_VOLUMES):
            self.edges_actor.GetProperty().SetColor(dark_color)
            self.faces_actor.GetProperty().SetColor(light_color)
            self.solids_actor.GetProperty().SetColor(light_color)

        elif theme == "light":
            self.edges_actor.GetProperty().SetColor(dark_color)
            self.faces_actor.GetProperty().SetColor(dark_color)
            self.solids_actor.GetProperty().SetColor(dark_color)

        elif theme == "dark":
            self.edges_actor.GetProperty().SetColor(light_color)
            self.faces_actor.GetProperty().SetColor(light_color)
            self.solids_actor.GetProperty().SetColor(light_color)

    def click_callback(self, x, y):
        self.mouse_click = (x, y)

    def selection_callback(self, x, y):
        if not self._actors_exists():
            return

        x0, y0 = self.mouse_click
        mouse_moved = (abs(x0 - x) > 10) or (abs(y0 - y) > 10)

        if mouse_moved:
            picked_nodes, picked_solids = self.mesh_selection.area_pick(x0, y0, x, y)

            # picked_nodes, picked_faces, picked_solids = self._get_area_picked_cell_id(x, y)
            # picked_nodes = self.mesh_selection.area_pick_nodes(x0, y0, x, y)
            # picked_solids = self.mesh_selection.area_pick_solids(x0, y0, x, y)
        else:
            # picked_nodes, picked_faces, picked_solids = self._get_picked_cell_id(x, y)
            picked_nodes = self.mesh_selection.pick_node(x, y)
            picked_solids = self.mesh_selection.pick_solid(x, y)

        modifiers = QApplication.keyboardModifiers()
        ctrl_pressed = modifiers & Qt.ControlModifier
        alt_pressed = modifiers & Qt.AltModifier

        app().main_window.set_mesh_selection(
            nodes=picked_nodes,
            # faces=picked_faces,
            solids=picked_solids,
            join=ctrl_pressed,
            remove=alt_pressed,
        )

    # These pick functions can be placed into a separated class
    def _get_picked_cell_id(self, x, y):
        """
        Pick the nodes, faces and solids at the same time.
        Them select just the one that is closest to the camera.

        If the ID of a cell is lower than 1 the distance to the
        camera is set to infinite, so it will never be selected.
        """

        picked_nodes = []
        picked_faces = []
        picked_solids = []

        camera_position = np.array(self.renderer.GetActiveCamera().GetPosition())
        node_id, node_pos = self._pick_actor(x, y, self.nodes_actor)
        face_id, face_pos = self._pick_actor(x, y, self.nodes_actor)
        solid_id, solid_pos = self._pick_actor(x, y, self.solids_actor)

        node_distance = (
            np.linalg.norm(camera_position - node_pos) 
            if node_id >= 0 else float("inf")
        )

        face_distance = (
            np.linalg.norm(camera_position - face_pos) 
            if face_id >= 0 else float("inf")
        )

        solid_distance = (
            np.linalg.norm(camera_position - solid_pos) 
            if solid_id >= 0 else float("inf")
        )

        node_distance *= 0.96  # Cheating a bit to prioritize the node selection
        face_distance *= 0.98  # Cheating a bit to prioritize the face selection
        closest = min(node_distance, face_distance, solid_distance)

        if closest == float("inf"):
            return picked_nodes, picked_faces, picked_solids

        if closest == node_distance:
            picked_nodes.append(node_id)

        # elif closest == face_distance:
        #     picked_faces.append(face_id)

        elif closest == solid_distance:
            picked_solids.append(solid_id)

        return picked_nodes, picked_faces, picked_solids

    def _get_area_picked_cell_id(self, x, y):
        print("Area selection not implemented yet")
        picked_nodes = []
        picked_faces = []
        picked_solids = []
        return picked_nodes, picked_faces, picked_solids

    def _pick_actor(self, x, y, target_actor: vtkActor):
        cell_picker = vtkCellPicker()
        cell_picker.SetTolerance(0.003)

        pickability = self._narrow_pickability_to_actor(target_actor)
        cell_picker.Pick(x, y, 0, self.renderer)
        self._restore_pickability(pickability)

        cell_id = cell_picker.GetCellId()
        position = cell_picker.GetPickPosition()

        if cell_id < 0:
            return cell_id, position

        # Try to get the cell_indexes array that shows the original
        # cell array even if it is being clipped.
        data: vtkPolyData = target_actor.GetMapper().GetInput()
        if not data:
            return cell_id, position

        cell_indexes: vtkIntArray = data.GetCellData().GetArray("cell_indexes")
        if not cell_indexes:
            return cell_id, position

        new_cell_id = cell_indexes.GetValue(cell_id)
        return new_cell_id, position

    def _narrow_pickability_to_actor(self, target_actor: vtkActor):
        actor: vtkActor
        pickability = dict()
        for actor in self.renderer.GetActors():
            pickability[actor] = actor.GetPickable()
            actor.SetPickable(actor == target_actor)
        return pickability

    def _restore_pickability(self, pickability: dict):
        actor: vtkActor
        for actor in self.renderer.GetActors():
            actor.SetPickable(pickability[actor])

    def update_selection(self):
        """
        Update the visualization of selected data.
        """
        # This is a optimization, may imply side effects
        if not self.isVisible():
            return

        if not self._actors_exists():
            return

        self.update_info_text()

        self.nodes_actor.clear_colors((0, 0, 0, 0))
        self.faces_actor.clear_colors((255, 255, 255, 255))
        self.solids_actor.clear_colors()

        nodes = self.main_window.selected_mesh_nodes
        faces = self.main_window.selected_mesh_faces
        solids = self.main_window.selected_mesh_solids

        self.nodes_actor.paint_cells([255, 0, 0], nodes)
        # self.faces_actor.paint_cells(self.selection_color, faces)
        self.solids_actor.paint_cells(self.selection_color, solids)
        self.update()

    def select_multiple_nodes(self, new_nodes, *, join=False, remove=False):
        if not self._actors_exists():
            return
        self.nodes_actor.paint_cells([255, 0, 0], new_nodes)
        self.update()
        # if self.view_mode != SHOW_FACES:
        #     self.show_points()

    def select_multiple_faces(self, new_faces, *, join=False, remove=False):
        if not self._actors_exists():
            return
        self.faces_actor.paint_cells(self.selection_color, new_faces)
        self.update()
        self.show_faces()

    def select_multiple_volumes(self, new_volumes, *, join=False, remove=False):
        if not self._actors_exists():
            return
        self.solids_actor.paint_cells(self.selection_color, new_volumes)
        self.update()
        self.show_volumes()

    def clear_selection_spheres(self):
        if self.selection_spheres_actor is None:
            return
        self.selection_spheres_actor.VisibilityOff()

    def set_selection_spheres(self, all_centers, all_radius):
        if self.selection_spheres_actor is None:
            return
        self.selection_spheres_actor.create_geometry(all_centers, all_radius)
        self.selection_spheres_actor.VisibilityOn()
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

    def _get_info_tab(self):
        pass

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
            self._apply_section_plane(
                position,
                rotation,
                inverted,
                section_plane.isVisible(),
            )

    def _disable_section_plane(self):
        has_hidden_part = bool(self.main_window.hidden_surfaces)
        self.ghost_actor.SetVisibility(has_hidden_part)
        self.plane_actor.VisibilityOff()

        self.faces_actor.disable_cut()
        self.solids_actor.disable_cut()
        self.edges_actor.disable_cut()
        self.update()

    def _apply_section_plane(self, position, rotation, inverted, show_plane=True):
        if isinstance(self.solids_actor, HollowSolidsActor):
            mesh = app().project.model.mesh
            if mesh is None:
                return

            if mesh.solids_connectivity.size > 0:
                self.remove_actors(self.solids_actor)
                self.solids_actor = SolidsActor(mesh)
                self.add_actors(self.solids_actor)

        self.plane_actor.configure_section_plane(position, rotation)
        xyz = self.plane_actor.calculate_xyz_position(position)
        normal = self.plane_actor.calculate_normal_vector(rotation)
        if inverted:
            normal = -normal

        self.faces_actor.apply_cut(xyz, normal)
        self.solids_actor.apply_cut(xyz, normal)
        self.edges_actor.apply_cut(xyz, normal)

        self.ghost_actor.VisibilityOn()
        self.plane_actor.SetVisibility(show_plane)
        self.plane_actor.GetProperty().SetColor(0.5, 0.5, 0.5)
        self.plane_actor.GetProperty().SetOpacity(0.2)
        self.update()

    # def start_section_mode(self):
    #     if not self._actors_exists():
    #         return
    #     self.section_plane_active = True
    #     self.plane_actor.VisibilityOn()
    #     self.faces_actor.clear_colors((255, 255, 255, 12))
    #     self.update()

    # def stop_section_mode(self):
    #     if not self._actors_exists():
    #         return
    #     self.section_plane_active = False
    #     self.plane_actor.VisibilityOff()
    #     has_hidden_part = bool(self.main_window.hidden_surfaces)
    #     faces_alpha = 12 if has_hidden_part else 0
    #     self.faces_actor.clear_colors((255, 255, 255, faces_alpha))
    #     self.solids_actor.disable_cut()
    #     self.edges_actor.disable_cut()
    #     self.nodes_actor.disable_cut()
    #     self.update()

    # def configure_section_plane(self, position, orientation):
    #     if not self._actors_exists():
    #         return

    #     self.plane_actor.configure_section_plane(position, orientation)
    #     self.update()

    # def apply_section_plane(self, position, orientation, invert=False):
    #     if not self._actors_exists():
    #         return

    #     self.section_plane_args = (position, orientation, invert)
    #     xyz = self.plane_actor.calculate_xyz_position(position)
    #     normal = self.plane_actor.calculate_normal_vector(orientation)
    #     if invert:
    #         normal = -normal
    #     self.solids_actor.apply_cut(xyz, normal)
    #     # self.faces_actor.apply_cut(xyz, normal)
    #     self.edges_actor.apply_cut(xyz, normal)
    #     self.nodes_actor.apply_cut(xyz, normal)

    #     self.plane_actor.VisibilityOn()
    #     self.plane_actor.GetProperty().SetColor(0.5, 0.5, 0.5)
    #     self.plane_actor.GetProperty().SetOpacity(0.2)

    #     self.update()

    def update_info_text(self):
        text = ""
        text += self._nodes_info_text()
        text += self._faces_info_text()
        text += self._solids_info_text()
        # text += self._material_info_text()
        # text += self._fluid_info_text()
        text += self._structural_boundary_conditions_info_text()

        self.set_info_text(text)
        self.update()

    def _nodes_info_text(self):
        nodes = list(self.main_window.selected_mesh_nodes)
        text = ""
        if len(nodes) > 1:
            text += f"{len(nodes)} nodes in selection\n" f"{format_long_sequence(nodes)}\n\n"
        elif len(nodes) == 1:
            text += f"Node: {nodes[0]}\n"
            coords = app().project.model.mesh.nodal_coordinates[nodes[0], 1:]
            text += f"Coordinates: [{round(coords[0], 6)}, {round(coords[1], 6)}, {round(coords[2], 6)}] (m)\n\n"

        return text

    def _faces_info_text(self):
        faces = list(self.main_window.selected_mesh_faces)
        text = ""
        if len(faces) > 1:
            text += f"{len(faces)} faces in selection\n" f"{format_long_sequence(faces)}\n\n"
        elif len(faces) == 1:
            text += f"Face element: {faces[0]}\n\n"

        return text

    def _solids_info_text(self):
        solids_elem_ids = list(self.main_window.selected_mesh_solids)
        text = ""
        if len(solids_elem_ids) > 1:
            text += (
                f"{len(solids_elem_ids)} solids in selection\n"
                f"{format_long_sequence(solids_elem_ids)}\n\n"
            )
        elif len(solids_elem_ids) == 1:
            element_id = solids_elem_ids[0]
            connect = app().project.model.mesh.solids_connectivity[element_id, 4:]
            text += f"Solid element: {element_id}\n"
            text += f"Connectivity: {list(connect)}\n\n"

        return text

    def _material_info_text(self):
        elements = list(self.main_window.selected_mesh_faces)
        text = ""

        if not elements:
            elements = list(self.main_window.selected_mesh_solids)

        if len(elements) == 1:
            current_solid = app().project.model.mesh.volume_from_element[elements[0]]
            material = app().project.model.properties.get_material(volume=current_solid)
            if material is None:
                return text

            tree = TreeInfo("Material")
            tree.add_item("Name", material.name)
            tree.add_item("Identifier", material.identifier)
            tree.add_item("Density", material.density, "kg/m³")
            tree.add_item("Young Modulus", material.young_modulus / 1e9, "GPa")
            tree.add_item("Poisson Ratio", material.poisson_ratio, "--")
            tree.add_item(
                "Thermal Expasion Coefficient", material.thermal_expansion_coefficient, "1/K"
            )

            text += str(tree)

        return text

    def _fluid_info_text(self):
        elements = list(self.main_window.selected_mesh_faces)
        text = ""

        if not elements:
            elements = list(self.main_window.selected_mesh_solids)

        if len(elements) == 1:
            current_solid = app().project.model.mesh.volume_from_element[elements[0]]
            fluid = app().project.model.properties.get_fluid(volume=current_solid)
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


    def _structural_boundary_conditions_info_text(self):

        text = ""
        selected_nodes = list(self.main_window.selected_mesh_nodes)

        if len(selected_nodes) != 1:
            return text

        prescribed_dofs = app().project.model.properties._get_property("prescribed_dofs", node=selected_nodes[0])
        external_loads = app().project.model.properties._get_property("external_loads", node=selected_nodes[0])
        boundary_conditions_list = [prescribed_dofs, external_loads]

        if all(condition is None for condition in boundary_conditions_list):
            return text

        if prescribed_dofs is not None:
            values = prescribed_dofs["values"]
            loaded_table = "table_names" in prescribed_dofs.keys()
            text += _structural_format("Prescribed dofs",  values, ("u", "r"), ("m", "rad"), loaded_table)

        if external_loads is not None:
            values = external_loads["values"]
            loaded_table = "table_names" in external_loads.keys()
            text += _structural_format("External loads",  values, ("F", "M"), ("N", "N.m"), loaded_table)

        return text

def _all_none(sequence) -> bool:
    return all(i is None for i in sequence)

def _structural_format(property_name, values, labels, units, has_table):

    if _all_none(values):
        return ""

    u_values = list()
    u_labels = list()
    for val, label in zip(values[:3], "xyz"):
        if val is not None:
            u_values.append(val)
            u_labels.append(labels[0] + label)

    r_values = list()
    r_labels = list()
    for val, label in zip(values[3:], "xyz"):
        if val is None:
            continue

        if not isinstance(val, Number | str):
            val = "table"

        r_values.append(val)
        r_labels.append(labels[1] + label)

    tree = TreeInfo(property_name)
    if has_table:
        tree.add_item(u_labels, "Table of values")
        tree.add_item(r_labels, "Table of values")
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
