# fmt: off

import numpy as np
from molde.render_widgets import CommonRenderWidget
from molde.utils import TreeInfo
from molde.utils.format_sequences import format_long_sequence
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from vtkmodules.vtkCommonCore import vtkIntArray
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkRenderingCore import vtkActor, vtkCellPicker

from vibra import app
from vibra.interface.tabs.geometry_info_bar import GeometryInfoBar
from vibra.interface.viewer_3d.actors.cutting_plane_actor import (
    CuttingPlaneActor,
)
from vibra.interface.viewer_3d.actors.faces_actor import FacesActor
from vibra.interface.viewer_3d.actors.lines_actor import LinesActor
from vibra.interface.viewer_3d.actors.points_actor import PointsActor
from vibra.interface.viewer_3d.actors.selection_spheres import SelectionSpheres
from vibra.interface.viewer_3d.interactor_styles.selection_interactor import (
    SelectionInteractor,
)

SHOW_POINTS = 0
SHOW_LINES = 1
SHOW_FACES = 2


class GeometryRenderWidget(CommonRenderWidget):
    selection_changed = pyqtSignal(set, set, set, set)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.main_window = app().main_window
        self.view_mode = SHOW_FACES

        self.left_clicked.connect(self.click_callback)
        self.left_released.connect(self.selection_callback)
        self.main_window.selection_changed.connect(self.update_selection)
        self.main_window.theme_changed.connect(self.set_theme)
        self.main_window.section_plane.value_changed.connect(self.update_section_plane)
        # self.geometry_info = GeometryInfoBar()

        # # replace the layout to add other usefull widgets
        # QObjectCleanupHandler().add(self.layout())
        # layout = QVBoxLayout()
        # # layout.addWidget(self.geometry_info)
        # layout.addWidget(self.render_interactor)
        # self.setLayout(layout)
        # self.setContentsMargins(0, 0, 0, 0)

        self.points_actor = None
        self.lines_actor = None
        self.faces_actor = None
        self.hidden_part_actor = None
        self.selection_spheres_actor = None

        self.selection_color = (20, 106, 245)
        self.selected_points = set()
        self.selected_lines = set()
        self.selected_faces = set()
        self.selected_volumes = set()

        # self.style = SelectionInteractor()
        # self.style.AddObserver("SelectionEvent", self.selection_callback)
        # self.render_interactor.SetInteractorStyle(self.style)

        self.create_axes()
        self.create_scale_bar()
        self.update_plot()

    def update_plot(self, reset_camera=True):
        if app().project is None:
            return

        model = app().project.model
        if model is None:
            return

        mesh = model.mesh
        if mesh is None:
            return

        self.remove_actors()

        self.selection_spheres_actor = SelectionSpheres()
        self.renderer.AddActor(self.selection_spheres_actor)

        self.points_actor = PointsActor(mesh)
        self.renderer.AddActor(self.points_actor)

        self.lines_actor = LinesActor(mesh)
        self.renderer.AddActor(self.lines_actor)

        self.faces_actor = FacesActor(mesh)
        self.renderer.AddActor(self.faces_actor)

        # Add a very subtle transparent actor to represent the whole
        # structure even if part of it is hidden
        has_hidden_part = bool(self.main_window.hidden_surfaces)
        self.hidden_part_actor = FacesActor(mesh, allow_hidding=False)
        self.hidden_part_actor.SetVisibility(has_hidden_part)
        self.hidden_part_actor.GetProperty().SetOpacity(0.05)
        self.hidden_part_actor.GetProperty().LightingOff()
        self.hidden_part_actor.PickableOff()
        self.renderer.AddActor(self.hidden_part_actor)

        self.plane_actor = CuttingPlaneActor(self.faces_actor.GetBounds())
        self.plane_actor.VisibilityOff()
        self.renderer.AddActor(self.plane_actor)

        if reset_camera:
            self.renderer.ResetCamera()
        self.show_faces()

        self.update_section_plane()

        # This seems to be running twice and I don't know why.
        # First it gets a terrible image then it gets a better one.
        # I will keep it like this because it is fast enough, but this
        # may be addressed in near future.
        app().project.thumbnail = self.get_thumbnail()

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
        self.hidden_part_actor.SetVisibility(has_hidden_part)

        self.update_section_plane()
        # self.update()

    def set_theme(self, theme):
        super().set_theme(theme)

        try:
            if not self._actors_exists():
                return
        except AttributeError:
            return

        if theme == "light":
            self.points_actor.GetProperty().SetColor(0.2, 0.2, 0.2)
            self.lines_actor.GetProperty().SetColor(0.2, 0.2, 0.2)
        elif theme == "dark":
            self.points_actor.GetProperty().SetColor(1, 1, 1)
            self.lines_actor.GetProperty().SetColor(1, 1, 1)

    #
    def show_points(self):
        if not self._actors_exists():
            return

        self.points_actor.VisibilityOn()
        self.lines_actor.VisibilityOff()
        self.faces_actor.GetProperty().SetOpacity(0.1)

        self.points_actor.PickableOn()
        self.lines_actor.PickableOff()
        self.faces_actor.PickableOff()

        self.view_mode = SHOW_POINTS
        self.update()

    def show_lines(self):
        if not self._actors_exists():
            return

        self.points_actor.VisibilityOff()
        self.lines_actor.VisibilityOn()
        self.faces_actor.GetProperty().SetOpacity(0.1)

        self.points_actor.PickableOff()
        self.lines_actor.PickableOn()
        self.faces_actor.PickableOff()

        self.view_mode = SHOW_LINES
        self.update()

    def show_faces(self):
        if not self._actors_exists():
            return

        self.points_actor.VisibilityOff()
        self.lines_actor.VisibilityOff()
        self.faces_actor.GetProperty().SetOpacity(1)

        self.points_actor.PickableOff()
        self.lines_actor.PickableOff()
        self.faces_actor.PickableOn()

        self.view_mode = SHOW_FACES
        self.update()

    #
    def click_callback(self, x, y):
        self.mouse_click = (x, y)

    def selection_callback(self, x, y):
        # This is a optimization, may imply side effects
        if not self.isVisible():
            return

        if not self._actors_exists():
            return

        mouse_moved = False
        if mouse_moved:
            (
                picked_nodes,
                picked_line_elements,
                picked_face_elements,
            ) = self._get_area_picked_cell_id(x, y)
        else:
            picked_nodes, picked_line_elements, picked_face_elements = self._get_picked_cell_id(
                x, y
            )

        picked_points = picked_nodes  # they have the same index
        picked_lines = set()
        picked_faces = set()
        picked_volumes = set()

        mesh = app().project.model.mesh

        for cell in picked_line_elements:
            line_entity = mesh.lines_connectivity[cell][1]
            picked_lines.add(line_entity)

        for cell in picked_face_elements:
            face_entity = mesh.faces_connectivity[cell][1]
            picked_faces.add(face_entity)
            for volume, surfaces in mesh.surfaces_from_volumes.items():
                if volume in self.main_window.hidden_volumes:
                    continue
                if face_entity in surfaces:
                    picked_volumes.add(volume)

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

        # if clicked_actor == self.points_actor:
        #     # self.select_point(clicked_cell, join=ctrl_pressed, remove=alt_pressed)
        #     self.main_window.set_geometry_selection(nodes=[clicked_cell], join=ctrl_pressed, remove=alt_pressed)

        # elif clicked_actor == self.lines_actor:
        #     line_entity = app().project.model.mesh.lines_connectivity[clicked_cell][1]
        #     self.main_window.set_geometry_selection(lines=[line_entity], join=ctrl_pressed, remove=alt_pressed)
        #     # self.select_line(line_entity, join=ctrl_pressed, remove=alt_pressed)

        # elif (clicked_actor == self.faces_actor) and not shift_pressed:
        #     face_entity = app().project.model.mesh.faces_connectivity[clicked_cell][1]
        #     # self.select_face(face_entity, join=ctrl_pressed, remove=alt_pressed)
        #     self.main_window.set_geometry_selection(surfaces=[face_entity], join=ctrl_pressed, remove=alt_pressed)

        # elif (clicked_actor == self.faces_actor) and shift_pressed:
        #     face_entity = app().project.model.mesh.faces_connectivity[clicked_cell][1]
        #     for (volume, surfaces) in app().project.model.mesh.surfaces_from_volumes.items():
        #         if face_entity in surfaces:
        #             # self.select_volume(volume, join=ctrl_pressed, remove=alt_pressed)
        #             self.main_window.set_geometry_selection(volumes=[volume], join=ctrl_pressed, remove=alt_pressed)
        #             break

        # else:
        #     # self.clear_selection()
        #     # self.selection_changed.emit(self.selected_points,
        #     #                             self.selected_lines,
        #     #                             self.selected_faces,
        #     #                             self.selected_volumes)
        #     self.main_window.set_geometry_selection(join=ctrl_pressed, remove=alt_pressed)

        # self.update()

    def update_selection(self):
        self.points_actor.clear_colors()
        self.lines_actor.clear_colors()
        self.faces_actor.clear_colors()

        points = app().main_window.selected_geometry_points
        lines = app().main_window.selected_geometry_lines
        faces = app().main_window.selected_geometry_surfaces
        volumes = app().main_window.selected_geometry_volumes

        mesh = app().project.model.mesh

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

        self.points_actor.paint_cells(self.selection_color, points)
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

        node_id, node_pos = self._pick_actor(x, y, self.points_actor)
        face_id, face_pos = self._pick_actor(x, y, self.lines_actor)
        solid_id, solid_pos = self._pick_actor(x, y, self.faces_actor)

        camera_position = np.array(self.renderer.GetActiveCamera().GetPosition())
        node_distance = np.linalg.norm(camera_position - node_pos) if node_id >= 0 else float("inf")
        face_distance = np.linalg.norm(camera_position - face_pos) if face_id >= 0 else float("inf")
        solid_distance = (
            np.linalg.norm(camera_position - solid_pos) if solid_id >= 0 else float("inf")
        )
        node_distance *= 0.98  # Cheating a bit to prioritize the node selection
        closest = min(node_distance, face_distance, solid_distance)

        if closest == float("inf"):
            return picked_nodes, picked_faces, picked_solids

        if closest == node_distance:
            picked_nodes.append(node_id)
        elif closest == face_distance:
            picked_faces.append(face_id)
        elif closest == solid_distance:
            picked_solids.append(solid_id)

        return picked_nodes, picked_faces, picked_solids

    def _get_area_picked_cell_id(self, x, y):
        # Not implemented
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
            self.plane_actor.configure_cutting_plane(position, rotation)
            self.plane_actor.VisibilityOn()
            self.plane_actor.GetProperty().SetColor(0, 0.333, 0.867)
            self.plane_actor.GetProperty().SetOpacity(0.8)
            self.update()
        else:
            self._apply_section_plane(position, rotation, inverted, section_plane.isVisible())

    def _disable_section_plane(self):
        has_hidden_part = bool(self.main_window.hidden_surfaces)
        self.hidden_part_actor.SetVisibility(has_hidden_part)
        self.plane_actor.VisibilityOff()
        self.points_actor.disable_cut()
        self.lines_actor.disable_cut()
        self.faces_actor.disable_cut()
        self.update()

    def _apply_section_plane(self, position, rotation, inverted, show_plane=True):
        self.plane_actor.configure_cutting_plane(position, rotation)
        xyz = self.plane_actor.calculate_x_y_z_position(position)
        normal = self.plane_actor.calculate_normal_vector(rotation)
        if inverted:
            normal = -normal

        self.points_actor.apply_cut(xyz, normal)
        self.faces_actor.apply_cut(xyz, normal)
        self.lines_actor.apply_cut(xyz, normal)

        self.hidden_part_actor.VisibilityOn()
        self.plane_actor.SetVisibility(show_plane)
        self.plane_actor.GetProperty().SetColor(0.5, 0.5, 0.5)
        self.plane_actor.GetProperty().SetOpacity(0.2)
        self.update()

    def remove_actors(self):
        self.renderer.RemoveActor(self.points_actor)
        self.renderer.RemoveActor(self.lines_actor)
        self.renderer.RemoveActor(self.faces_actor)
        self.renderer.RemoveActor(self.hidden_part_actor)
        self.renderer.RemoveActor(self.selection_spheres_actor)

        self.points_actor = None
        self.lines_actor = None
        self.faces_actor = None
        self.hidden_part_actor = None
        self.selection_spheres_actor = None

    def _actors_exists(self):
        actors = [
            self.points_actor,
            self.lines_actor,
            self.faces_actor,
            self.selection_spheres_actor,
            self.hidden_part_actor,
        ]

        return all([actor is not None for actor in actors])

    def update_info_text(self):
        text = ""
        text += self._nodes_info_text()
        text += self._faces_info_text()
        text += self._volumes_info_text()
        text += self._surface_thickness_info_text()
        text += self._material_info_text()
        text += self._fluid_info_text()
        text += self._porous_material_info_text()
        text += self._boundary_conditions_info_text()

        self.set_info_text(text)
        self.update()

    def _nodes_info_text(self):
        nodes = list(self.main_window.selected_geometry_points)
        text = ""

        if len(nodes) > 1:
            text += f"{len(nodes)} points in selection\n" f"{format_long_sequence(nodes)}\n\n"
        elif len(nodes) == 1:
            text += f"Point: {nodes[0]}\n\n"

        return text

    def _faces_info_text(self):
        text = ""
        volumes = list(self.main_window.selected_geometry_volumes)

        if len(volumes) == 0:
            faces = list(self.main_window.selected_geometry_surfaces)

            if len(faces) > 1:
                text += f"{len(faces)} surfaces in selection\n" f"{format_long_sequence(faces)}\n\n"
            elif len(faces) == 1:
                text += f"Surface: {faces[0]}\n\n"

        return text

    def _volumes_info_text(self):
        volumes = list(self.main_window.selected_geometry_volumes)
        text = ""

        if len(volumes) > 1:
            text += f"{len(volumes)} volumes in selection\n" f"{format_long_sequence(volumes)}\n\n"
        elif len(volumes) == 1:
            text += f"Volume: {volumes[0]}\n\n"

        return text
    
    def _surface_thickness_info_text(self):

        surfaces = list(self.main_window.selected_geometry_surfaces)
        text = ""

        if len(surfaces) == 1:
            surface_data = app().project.model.properties._get_property("surface_thickness", surface=surfaces[0])
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
        tree.add_item("elasticity modulus", material.young_modulus / 1e9, "GPa")
        tree.add_item("Poisson ratio", material.poisson_ratio, "--")
        tree.add_item("Thermal expasion coefficient", material.thermal_expansion_coefficient, "1/K")

        text += str(tree)

        return text

    def _fluid_info_text(self):

        volumes = list(self.main_window.selected_geometry_volumes)
        surfaces = list(self.main_window.selected_geometry_surfaces)

        text = ""
        if len(volumes) != 1 or len(surfaces) != 1:
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

        pm_model = app().project.model.properties.get_porous_material_model_data(
            volume=volumes[0]
        )
        if pm_model is None:
            return text

        tree = TreeInfo("Porous material")
        tree.add_item("Model", pm_model["model"])
        tree.add_item("Flow resistivity", pm_model["flow_resistivity"], "kg/m³s")

        text += str(tree)

        return text

    def _boundary_conditions_info_text(self):
        selected_faces = list(self.main_window.selected_geometry_surfaces)
        text = ""

        if len(selected_faces) != 1:
            return text

        acoustic_pressure = app().project.model.properties.get_acoustic_pressure(
            selected_faces[0]
        )
        surface_velocity = app().project.model.properties.get_surface_velocity(
            selected_faces[0]
        )
        specific_impedance = app().project.model.properties.get_specific_impedance(
            selected_faces[0]
        )
        boundary_conditions_list = [acoustic_pressure, surface_velocity, specific_impedance]

        if all(condition is None for condition in boundary_conditions_list):
            return text

        tree = TreeInfo("Boundary Conditions")

        if acoustic_pressure is not None:

            if "real_values" in acoustic_pressure.keys():
                real_values = np.array(acoustic_pressure["real_values"])
                imag_values = np.array(acoustic_pressure["imag_values"])
                complex_values = real_values + 1j * imag_values

            elif "values" in acoustic_pressure.keys():
                complex_values = acoustic_pressure["values"]

            if "table_names" in acoustic_pressure.keys():
                values = "table of values"
            else:
                values = f"{np.round(complex_values, 6)}"

            tree.add_item("Acoustic pressure", values, "Pa")

        if surface_velocity is not None:

            if "real_values" in surface_velocity.keys():
                real_values = np.array(surface_velocity["real_values"])
                imag_values = np.array(surface_velocity["imag_values"])
                complex_values = real_values + 1j * imag_values

            elif "values" in surface_velocity.keys():
                complex_values = surface_velocity["values"]

            if "table_names" in surface_velocity.keys():
                values = "table of values"
            else:
                values = f"{np.round(complex_values, 6)}"

            tree.add_item("Surface velocity", values, "m/s")

        if specific_impedance is not None:
            if "anechoic_termination" in specific_impedance.keys():
                fluid = app().project.model.properties.get_fluid(surface=selected_faces[0])
                density = fluid.fluid_density
                speed_of_sound = fluid.speed_of_sound
                complex_values = np.array([density * speed_of_sound], dtype=complex)

            elif "real_values" in specific_impedance.keys():
                real_values = np.array(specific_impedance["real_values"])
                imag_values = np.array(specific_impedance["imag_values"])
                complex_values = real_values + 1j * imag_values

            elif "values" in specific_impedance.keys():
                complex_values = specific_impedance["values"]

            if "table_names" in specific_impedance.keys():
                values = "table of values"
            else:
                values = f"{np.round(complex_values, 6)}"

            tree.add_item("Specific impedance", values, "kg/m²s")

            if "anechoic_termination" in specific_impedance.keys():
                tree.add_item("Impedance type", "anechoic (non-reflexive)")

        text += str(tree)

        return text

# fmt: on