from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from molde.render_widgets import CommonRenderWidget

from vibra import app
from vibra.interface.tabs.geometry_info_bar import GeometryInfoBar
from vibra.interface.viewer_3d.actors.faces_actor import FacesActor
from vibra.interface.viewer_3d.actors.lines_actor import LinesActor
from vibra.interface.viewer_3d.actors.points_actor import PointsActor
from vibra.interface.viewer_3d.interactor_styles.selection_interactor import SelectionInteractor
from vibra.interface.viewer_3d.actors.selection_spheres import SelectionSpheres
from vibra.interface.viewer_3d.actors.cutting_plane_actor import CuttingPlaneActor
from molde.utils.format_sequences import format_long_sequence
from molde.utils import TreeInfo


SHOW_POINTS = 0
SHOW_LINES = 1
SHOW_FACES = 2


class GeometryRenderWidget(CommonRenderWidget):
    selection_changed = pyqtSignal(set, set, set, set)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.main_window = app().main_window
        self.view_mode = SHOW_FACES

        self.main_window.selection_changed.connect(self.update_selection)
        # self.geometry_info = GeometryInfoBar()

        # replace the layout to add other usefull widgets
        QObjectCleanupHandler().add(self.layout())
        layout = QVBoxLayout()
        # layout.addWidget(self.geometry_info)
        layout.addWidget(self.render_interactor)
        self.setLayout(layout)
        self.setContentsMargins(0, 0, 0, 0)

        self.points_actor = None
        self.lines_actor = None
        self.faces_actor = None
        self.selection_spheres_actor = None

        self.selection_color = (20, 106, 245)
        self.selected_points = set()
        self.selected_lines = set()
        self.selected_faces = set()
        self.selected_volumes = set()

        self.style = SelectionInteractor()
        self.style.AddObserver("SelectionEvent", self.selection_callback)
        self.render_interactor.SetInteractorStyle(self.style)

        self.create_axes()
        self.update_plot()

    def update_plot(self):
        if self.main_window.project is None:
            return

        model = self.main_window.project.model
        if model is None:
            return

        mesh = model.mesh
        if mesh is None:
            return

        # self.update_theme()
        self.remove_actors()

        self.selection_spheres_actor = SelectionSpheres()
        self.selection_spheres_actor.GetProperty().SetColor([1, 0, 0])
        self.selection_spheres_actor.VisibilityOff()
        self.selection_spheres_actor.PickableOff()
        self.renderer.AddActor(self.selection_spheres_actor)

        self.points_actor = PointsActor(mesh)
        self.renderer.AddActor(self.points_actor)

        self.lines_actor = LinesActor(mesh)
        self.renderer.AddActor(self.lines_actor)

        self.faces_actor = FacesActor(mesh)
        self.renderer.AddActor(self.faces_actor)

        self.plane_actor = CuttingPlaneActor(self.faces_actor.GetBounds())
        self.plane_actor.VisibilityOff()
        self.renderer.AddActor(self.plane_actor)

        self.renderer.ResetCamera()
        self.show_faces()

        # This seems to be running twice and I don't know why.
        # First it gets a terrible image then it gets a better one.
        # I will keep it like this because it is fast enough, but this
        # may be addressed in near future.
        self.main_window.project.thumbnail = self.get_thumbnail()

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
    def selection_callback(self, obj, event):
        if not self._actors_exists():
            return
        
        clicked_cell = obj.selection_picker.GetCellId()
        clicked_actor = obj.selection_picker.GetActor()

        modifiers = QApplication.keyboardModifiers()
        ctrl_pressed = modifiers & Qt.ControlModifier
        shift_pressed = modifiers & Qt.ShiftModifier
        alt_pressed = modifiers & Qt.AltModifier

        if clicked_actor == self.points_actor:
            # self.select_point(clicked_cell, join=ctrl_pressed, remove=alt_pressed)
            self.main_window.set_geometry_selection(nodes=[clicked_cell], join=ctrl_pressed, remove=alt_pressed)

        elif clicked_actor == self.lines_actor:
            line_entity = self.main_window.project.model.mesh.lines_connectivity[clicked_cell][1]
            self.main_window.set_geometry_selection(lines=[line_entity], join=ctrl_pressed, remove=alt_pressed)
            # self.select_line(line_entity, join=ctrl_pressed, remove=alt_pressed)

        elif (clicked_actor == self.faces_actor) and not shift_pressed:
            face_entity = self.main_window.project.model.mesh.faces_connectivity[clicked_cell][1]
            # self.select_face(face_entity, join=ctrl_pressed, remove=alt_pressed)
            self.main_window.set_geometry_selection(faces=[face_entity], join=ctrl_pressed, remove=alt_pressed)

        elif (clicked_actor == self.faces_actor) and shift_pressed:
            face_entity = self.main_window.project.model.mesh.faces_connectivity[clicked_cell][1]
            for (volume, surfaces) in self.main_window.project.model.mesh.surfaces_from_volumes.items():
                if face_entity in surfaces:
                    # self.select_volume(volume, join=ctrl_pressed, remove=alt_pressed)
                    self.main_window.set_geometry_selection(volumes=[volume], join=ctrl_pressed, remove=alt_pressed)
                    break

        else:
            # self.clear_selection()
            # self.selection_changed.emit(self.selected_points,
            #                             self.selected_lines,
            #                             self.selected_faces,
            #                             self.selected_volumes)
            self.main_window.set_geometry_selection(join=ctrl_pressed, remove=alt_pressed)

        self.update()

    def update_selection(self):
        self.points_actor.clear_colors()
        self.lines_actor.clear_colors()
        self.faces_actor.clear_colors()

        points = app().main_window.selected_geometry_points
        lines = app().main_window.selected_geometry_lines
        faces = app().main_window.selected_geometry_surfaces
        volumes = app().main_window.selected_geometry_volumes

        mesh = self.main_window.project.model.mesh

        # Get the line elements of all selected lines
        all_lines_elements = list()
        for line in lines:
            indexes = self.main_window.project.model.mesh.elements_from_line.get(line, [])
            all_lines_elements.extend(indexes)

        all_faces_elements = list()
        # Get the face elements of all selected faces
        for face in faces:
            indexes = mesh.elements_from_surface.get(face, [])
            all_faces_elements.extend(indexes)

        # Get the face elements of all selected volumes
        for volume in volumes:
            surfaces = self.main_window.project.model.mesh.surfaces_from_volumes[volume]
            for face in surfaces:
                indexes = self.main_window.project.model.mesh.elements_from_surface.get(face, [])
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

    ################################# TODO: Remove these commented lines
    ################################# I am just not brave enought to do it

    # def select_point(self, new_point, *, join=False, remove=False):
    #     self.select_multiple_points([new_point], join=join, remove=remove)

    # def select_line(self, new_line, *, join=False, remove=False):
    #     self.select_multiple_lines([new_line], join=join, remove=remove)

    # def select_face(self, new_face, *, join=False, remove=False):
    #     self.select_multiple_faces([new_face], join=join, remove=remove)

    # def select_volume(self, new_volume, *, join=False, remove=False):
    #     self.select_multiple_volumes([new_volume], join=join, remove=remove)

    # def select_multiple_points(self, new_points, *, join=False, remove=False):
    #     if self.view_mode != SHOW_POINTS:
    #         return

    #     if join:
    #         self.selected_points |= set(new_points)
    #     elif remove:
    #         self.selected_points -= set(new_points)
    #     else:
    #         self.selected_points = set(new_points)

    #     self.points_actor.clear_colors()
    #     self.points_actor.paint_cells(self.selection_color, self.selected_points)
    #     self.update()
    #     self.selection_changed.emit(
    #                                 self.selected_points, 
    #                                 self.selected_lines, 
    #                                 self.selected_faces, 
    #                                 self.selected_volumes
    #                                 )

    # def select_multiple_lines(self, new_lines, *, join=False, remove=False):
    #     if self.view_mode != SHOW_LINES:
    #         return

    #     if join:
    #         self.selected_lines |= set(new_lines)
    #     elif remove:
    #         self.selected_lines -= set(new_lines)
    #     else:
    #         self.selected_lines = set(new_lines)

    #     all_element_indexes = list()
    #     for line in self.selected_lines:

    #         if line not in self.main_window.project.model.mesh.elements_from_line.keys():
    #             return
            
    #         indexes = self.main_window.project.model.mesh.elements_from_line[line]
    #         all_element_indexes.extend(indexes)

    #     self.lines_actor.clear_colors()
    #     self.lines_actor.paint_cells(self.selection_color, all_element_indexes)
    #     self.update()
    #     self.selection_changed.emit(
    #                                 self.selected_points, 
    #                                 self.selected_lines, 
    #                                 self.selected_faces, 
    #                                 self.selected_volumes
    #                                 )

    # def select_multiple_faces(self, new_faces, *, join=False, remove=False):
    #     if self.view_mode != SHOW_FACES:
    #         return

    #     if join:
    #         self.selected_faces |= set(new_faces)
    #     elif remove:
    #         self.selected_faces -= set(new_faces)
    #     else:
    #         self.selected_faces = set(new_faces)
    #     self.selected_volumes.clear()

    #     all_element_indexes = list()
    #     for face in self.selected_faces:

    #         if face not in self.main_window.project.model.mesh.elements_from_surface.keys():
    #             return

    #         indexes = self.main_window.project.model.mesh.elements_from_surface[face]
    #         all_element_indexes.extend(indexes)

    #     self.faces_actor.clear_colors()
    #     self.faces_actor.paint_cells(self.selection_color, all_element_indexes)
    #     self.update()
    #     self.selection_changed.emit(
    #                                 self.selected_points, 
    #                                 self.selected_lines, 
    #                                 self.selected_faces, 
    #                                 self.selected_volumes
    #                                 )

    # def select_multiple_volumes(self, new_volumes, *, join=False, remove=False):
    #     if self.view_mode != SHOW_FACES:
    #         return

    #     if join:
    #         self.selected_volumes |= set(new_volumes)
    #     elif remove:
    #         self.selected_volumes -= set(new_volumes)
    #     else:
    #         self.selected_volumes = set(new_volumes)
    #     self.selected_faces.clear()

    #     all_element_indexes = list()
    #     for volume in self.selected_volumes:

    #         surfaces = self.main_window.project.model.mesh.surfaces_from_volumes[volume]
    #         for face in surfaces:

    #             if face not in self.main_window.project.model.mesh.elements_from_surface.keys():
    #                 return

    #             indexes = self.main_window.project.model.mesh.elements_from_surface[face]
    #             all_element_indexes.extend(indexes)

    #     self.faces_actor.clear_colors()
    #     self.faces_actor.paint_cells(self.selection_color, all_element_indexes)
    #     self.update()
    #     self.selection_changed.emit(
    #                                 self.selected_points, 
    #                                 self.selected_lines, 
    #                                 self.selected_faces, 
    #                                 self.selected_volumes
    #                                 )

    # def clear_selection(self):
    #     self.points_actor.clear_colors()
    #     self.lines_actor.clear_colors()
    #     self.faces_actor.clear_colors()
    #     self.selected_points = set()
    #     self.selected_lines = set()
    #     self.selected_faces = set()
    #     self.selected_volumes = set()

    def start_cutting_mode(self):
        if not self._actors_exists():
            return
        self.plane_actor.VisibilityOn()
        self.update()

    def stop_cutting_mode(self):
        if not self._actors_exists():
            return
        self.plane_actor.VisibilityOff()
        self.points_actor.disable_cut()
        self.lines_actor.disable_cut()
        self.faces_actor.disable_cut()
        self.update()

    def configure_cutting_plane(self, position, orientation):
        if not self._actors_exists():
            return

        self.plane_actor.configure_cutting_plane(position, orientation)
        self.update()

    def apply_cutting_plane(self, position, orientation):
        if not self._actors_exists():
            return

        xyz = self.plane_actor.calculate_x_y_z_position(position)
        normal = self.plane_actor.calculate_normal_vector(orientation)
        self.points_actor.apply_cut(xyz, normal)
        self.faces_actor.apply_cut(xyz, normal)
        self.lines_actor.apply_cut(xyz, normal)

        self.plane_actor.GetProperty().SetColor(0.5, 0.5, 0.5)
        self.plane_actor.GetProperty().SetOpacity(0.2)

        self.update()

    def remove_actors(self):
        self.renderer.RemoveActor(self.points_actor)
        self.renderer.RemoveActor(self.lines_actor)
        self.renderer.RemoveActor(self.faces_actor)
        self.renderer.RemoveActor(self.selection_spheres_actor)

        self.points_actor = None
        self.lines_actor = None
        self.faces_actor = None
        self.selection_spheres_actor = None

    def _actors_exists(self):
        actors = [  
                    self.points_actor,
                    self.lines_actor,
                    self.faces_actor,
                    self.selection_spheres_actor,
                ]

        return all([actor is not None for actor in actors])

    def update_info_text(self):
        text = ""
        text += self._nodes_info_text()
        text += self._faces_info_text()
        text += self._material_info_text()
        text += self._fluid_info_text()
        text += self._boundary_conditions_info_text()
        
        self.set_info_text(text)
        self.update()
    
    def _nodes_info_text(self):
        nodes = list(self.main_window.selected_geometry_points)
        text = ""

        if len(nodes) > 1:
            text += (
                f"{len(nodes)} nodes in selection\n"
                f"{format_long_sequence(nodes)}\n\n"
            )
        elif len(nodes) == 1:
            text += f"Point: {nodes[0]}\n\n"

        return text

    def _faces_info_text(self):
        faces = list(self.main_window.selected_geometry_surfaces)
        text = ""

        if len(faces) > 1:
            text += (
                f"{len(faces)} surfaces in selection\n"
                f"{format_long_sequence(faces)}\n\n"
            )
        elif len(faces) == 1:
            text += f"Surface: {faces[0]}\n\n"
        
        return text

    def _material_info_text(self):
        elements = list(self.main_window.selected_geometry_surfaces)
        text = ""

        if len(elements) != 1:
            return text 
        
        material = self.main_window.project.model.properties.get_material(elements[0])
        if material is None:
            return text
        
        tree = TreeInfo("Material")
        tree.add_item("Name", material.name)
        tree.add_item("Identifier", material.identifier)
        tree.add_item("Density", material.density, "kg/m3")
        tree.add_item("Young Modulus", material.young_modulus/1e9, "GPa")
        tree.add_item("Poisson Ratio", material.poisson_ratio, "--")
        tree.add_item("Thermal Expasion Coefficient", material.thermal_expansion_coefficient, "1/K")

        text += str(tree)

        return text
        
    def _fluid_info_text(self):
        elements = list(self.main_window.selected_geometry_surfaces)
        text = ""

        if len(elements) != 1:
            return text
        
        fluid = self.main_window.project.model.properties.get_fluid(element=elements[0])
        if fluid is None:
            return text
        
        tree = TreeInfo("Fluid")
        tree.add_item("Name", fluid.name)
        tree.add_item("Identifier", fluid.identifier)
        tree.add_item("Pressure", fluid.pressure, "Pa")
        tree.add_item("Temperature", fluid.temperature, "K")
        tree.add_item("Density", fluid.fluid_density, "kg/m3")
        tree.add_item("Speed of sound", fluid.speed_of_sound, "m/s")
        if fluid.molar_mass is not None:
            tree.add_item("Molar mass", fluid.molar_mass, "kg/kmol")

        text += str(tree)

        return text

    def _boundary_conditions_info_text(self):
        elements = list(self.main_window.selected_geometry_surfaces)
        text = ""

        if len(elements) != 1:
            return text

        acoustic_pressure = self.main_window.project.model.properties.get_acoustic_pressure(elements[0])
        surface_velocity = self.main_window.project.model.properties.get_surface_velocity(elements[0])
        specific_impedance = self.main_window.project.model.properties.get_specific_impedance(elements[0])
        boundary_conditions_list = [acoustic_pressure, surface_velocity, specific_impedance]

        if all(condition is None for condition in boundary_conditions_list):
            return text
        
        tree = TreeInfo("Boundary Conditions")

        if acoustic_pressure is not None:
            tree.add_item("Acoustic pressure", acoustic_pressure["real_values"][0], "Pa")
        if surface_velocity is not None:
            tree.add_item("Surface velocity", surface_velocity["real_values"][0], "m/s")
        if specific_impedance is not None:
            tree.add_item("Specific impedance", specific_impedance["real_values"][0], "kg/m2s")

        text += str(tree)
        
        return text



    
