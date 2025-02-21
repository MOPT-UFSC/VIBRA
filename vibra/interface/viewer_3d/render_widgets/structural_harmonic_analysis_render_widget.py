import logging
from threading import Lock
from time import time

import numpy as np
from molde.render_widgets import AnimatedRenderWidget
from PyQt5.QtCore import QObjectCleanupHandler
from PyQt5.QtWidgets import *

from vibra import app

from ..actors.ghost_actor import GhostActor
from ..actors.analysis_actor import AnalysisActor
from ..actors.hollow_analysis_actor import HollowAnalysisActor
from ..actors.section_plane_actor import SectionPlaneActor
from ..actors.edges_actor import EdgesActor
from ..actors.faces_actor import FacesActor
from vibra.utils.math_functions import lerp


class StructuralHarmonicAnalysisRenderWidget(AnimatedRenderWidget):
    # many parts of this class is shared by StructuralHarmonicAnalysisRenderWidget
    # and probably with other analysis classes, so it may be a good idea to
    # make a superclass that controls all the common stuff.

    def __init__(self, parent=None):
        super().__init__(parent)

        self.main_window = app().main_window
        self.current_menu_widget = None

        self.main_window.theme_changed.connect(self.set_theme)
        self.main_window.section_plane.value_changed.connect(self.update_section_plane)

        # replace the layout to add other usefull widgets
        QObjectCleanupHandler().add(self.layout())
        layout = QVBoxLayout()
        layout.addWidget(self.render_interactor)
        self.setLayout(layout)
        self.setContentsMargins(0, 0, 0, 0)

        self.show_plane_actor = True
        self.section_plane_active = False
        self.section_plane_args = tuple()

        self.analysis_actor: AnalysisActor | HollowAnalysisActor = None
        self.edges_actor: EdgesActor = None
        self.plane_actor: SectionPlaneActor = None
        self.ghost_actor: GhostActor = None
        self.bounds = (0, 0, 0, 0, 0, 0)

        self.create_axes()
        self.create_color_bar()
        self.create_scale_bar()
        self.update_plot()
    
    def configure_menu_widget(self, menu_widget: QWidget):
        self.current_menu_widget = menu_widget

    def toggle_animation(self, *args, **kwargs):
        if self.playing_animation:
            self.stop_animation()
        else:
            self.start_animation(*args, **kwargs)

    def start_animation(self, *args, **kwargs):
        super().start_animation(*args, **kwargs)
        self.main_window.animation_toolbar.update_animate_button_icons(True)

    def stop_animation(self):
        super().stop_animation()
        self.main_window.animation_toolbar.update_animate_button_icons(False)

    def current_frequency_index(self):
        if self.current_menu_widget is not None:
            return self.current_menu_widget.current_frequency_index()
        return 0

    def update_plot(self, reset_camera=False):
        if app().project is None:
            return

        model = app().project.model
        if model is None:
            return

        mesh = model.mesh
        if mesh is None:
            return

        solver = app().project.structural_harmonic_solver
        if solver is None:
            return

        if solver.solution_full is None:
            return

        index = self.current_frequency_index()
        if not (0 <= index < solver.solution_full.shape[1]):
            return
        
        if self.plane_actor is not None:
            self.show_plane_actor = self.plane_actor.GetVisibility()

        self.remove_all_actors()

        self.analysis_actor = HollowAnalysisActor(mesh)

        self.edges_actor = EdgesActor(self.analysis_actor.data)
        self.edges_actor.GetProperty().SetColor(0, 0, 0)

        # Add a very subtle transparent actor to represent the whole
        # structure even if part of it is hidden
        has_hidden_part = bool(self.main_window.hidden_surfaces)
        self.ghost_actor = GhostActor(mesh)
        self.ghost_actor.SetVisibility(has_hidden_part)
        self.renderer.AddActor(self.ghost_actor)

        self.plane_actor = SectionPlaneActor(self.analysis_actor.GetBounds())
        self.plane_actor.VisibilityOff()

        self.update_deformations()
        self.renderer.AddActor(self.analysis_actor)
        self.renderer.AddActor(self.edges_actor)
        self.renderer.AddActor(self.plane_actor)

        # mesh_visibility = self.control_bar.show_mesh_button.isChecked()
        # self.set_mesh_visibility(mesh_visibility)

        if reset_camera:
            self.renderer.ResetCamera()
            
        self.update_section_plane()
        app().project.thumbnail = self.get_thumbnail()

    def update_hidden_plot(self):
        # in this case the update_plot function is fast enough
        self.update_plot(reset_camera=False)

    def update_deformations(self):
        if not self._actors_exists():
            return

        solver = app().project.structural_harmonic_solver
        if solver.solution_full is None:
            return

        index = self.current_frequency_index()
        if not (0 <= index < solver.solution_full.shape[1]):
            return

        # Do not update the deformation directly if an animation is running.
        # This makes the magnification factor work much smothly.
        if self.playing_animation:
            return

        sld_phase = self.main_window.animation_toolbar.phase_slider.value()
        magnification_factor = self.main_window.animation_toolbar.magnification_factor_slider.value() / 16
        displacements, color_scalars, min_value, max_value = self._calculate_displacements(index, sld_phase)

        self.analysis_actor.apply_deformation(displacements, magnification_factor, max_value)
        self.edges_actor.extract_data(self.analysis_actor.data)

        self.analysis_actor.plot_color_bar(color_scalars, min_value, max_value)
        self.colorbar_actor.SetLookupTable(self.analysis_actor.color_table)
        self.update()

    def set_mesh_visibility(self, condition):
        if not self._actors_exists():
            return

        if condition:
            self.show_lines()
        else:
            self.show_faces()

    #
    def show_points(self):
        return
        if not self._actors_exists():
            return

        self.control_bar.show_mesh_button.setChecked(False)
        self.analysis_actor.VisibilityOn()
        self.analysis_actor.GetProperty().SetRepresentationToPoints()
        self.edges_actor.VisibilityOff()
        self.update()

    def show_lines(self):
        return
        if not self._actors_exists():
            return

        self.control_bar.show_mesh_button.setChecked(True)
        self.analysis_actor.VisibilityOn()
        self.analysis_actor.GetProperty().SetRepresentationToSurface()
        self.edges_actor.VisibilityOn()
        self.update()

    def show_faces(self):
        return
        if not self._actors_exists():
            return

        self.control_bar.show_mesh_button.setChecked(False)
        self.analysis_actor.VisibilityOn()
        self.analysis_actor.GetProperty().SetRepresentationToSurface()
        self.edges_actor.VisibilityOff()
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
        self.analysis_actor.disable_cut()
        self.edges_actor.disable_cut()
        self.update()

    def _apply_section_plane(self, position, rotation, inverted, show_plane=True):
        if isinstance(self.analysis_actor, HollowAnalysisActor):
            mesh = app().project.model.mesh
            if mesh is None:
                return

            if mesh.solids_connectivity.size > 0:
                self.remove_actors(self.analysis_actor)
                self.analysis_actor = AnalysisActor(mesh)
                self.update_deformations()
                self.add_actors(self.analysis_actor)

        self.plane_actor.configure_section_plane(position, rotation)
        xyz = self.plane_actor.calculate_xyz_position(position)
        normal = self.plane_actor.calculate_normal_vector(rotation)
        if inverted:
            normal = -normal

        self.analysis_actor.apply_cut(xyz, normal)
        self.edges_actor.apply_cut(xyz, normal)

        self.ghost_actor.VisibilityOn()
        self.plane_actor.SetVisibility(show_plane)
        self.plane_actor.GetProperty().SetColor(0.5, 0.5, 0.5)
        self.plane_actor.GetProperty().SetOpacity(0.2)
        self.update()

    #
    # def start_section_mode(self):
    #     if not self._actors_exists():
    #         return
    #     self.section_plane_active = True
    #     self.plane_actor.VisibilityOn()
    #     self.ghost_actor.VisibilityOn()

    # def stop_section_mode(self):
    #     if not self._actors_exists():
    #         return
    #     self.section_plane_active = False
    #     self.plane_actor.VisibilityOff()
    #     has_hidden_part = bool(self.main_window.hidden_surfaces)
    #     self.ghost_actor.SetVisibility(has_hidden_part)
    #     self.analysis_actor.disable_cut()
    #     self.edges_actor.disable_cut()
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
    #     self.analysis_actor.apply_cut(xyz, normal)
    #     self.edges_actor.apply_cut(xyz, normal)

    #     self.plane_actor.VisibilityOn()
    #     self.plane_actor.configure_section_plane(position, orientation)
    #     self.plane_actor.GetProperty().SetColor(0.5, 0.5, 0.5)
    #     self.plane_actor.GetProperty().SetOpacity(0.2)

    #     self.update()

    def remove_all_actors(self):
        self.renderer.RemoveActor(self.analysis_actor)
        self.renderer.RemoveActor(self.edges_actor)
        self.renderer.RemoveActor(self.plane_actor)
        self.renderer.RemoveActor(self.ghost_actor)
        self.analysis_actor = None
        self.edges_actor = None
        self.plane_actor = None
        self.ghost_actor = None

    def update_animation(self, frame):

        if not self._actors_exists():
            return

        solver = app().project.structural_harmonic_solver
        if solver.solution_full is None:
            return

        index = self.current_frequency_index()
        if not (0 <= index < solver.solution_full.shape[1]):
            return

        logging.info(f"Rendering animation frame [{frame}/{self._animation_total_frames}]")

        # Map the frames from 0 to 1
        t = frame / (self._animation_total_frames - 1)
        phase = lerp(0, 360, t)

        magnification_factor = self.main_window.animation_toolbar.magnification_factor_slider.value() / 16
        displacements, color_scalars, min_value, max_value = self._calculate_displacements(index, phase)

        self.analysis_actor.apply_deformation(displacements, magnification_factor, max_value)
        self.ghost_actor.apply_deformation(displacements, magnification_factor, max_value)
        self.analysis_actor.plot_color_bar(color_scalars, min_value, max_value)
        # self.edges_actor.extract_data(self.analysis_actor.data)
        self.update()

    def _actors_exists(self):
        actors = [self.analysis_actor, self.edges_actor, self.plane_actor]
        return all([actor is not None for actor in actors])

    def _calculate_displacements(self, index: int, selected_phase_deg: float):

        solver = app().project.structural_harmonic_solver
        if solver.solution_full is None:
            return

        disp_dofs = solver.displacement_dofs
        results_complex = solver.solution_full[disp_dofs, index]

        amplitudes = np.abs(results_complex)
        phases = np.angle(results_complex)

        selected_phase_rad = selected_phase_deg * np.pi / 180
        results_real = amplitudes * np.cos(phases + selected_phase_rad)

        current_solution = results_real.reshape(-1, 3).copy()

        if self.current_menu_widget is None or self.current_menu_widget.comboBox_displacements.currentIndex() == 0:
            disp_type = "u_sum"
            color_scalars = np.linalg.norm(current_solution, axis=1)#.copy()
            displacements = current_solution.copy()

        elif self.current_menu_widget.comboBox_displacements.currentIndex() == 1:
            disp_type = "u_x"
            color_scalars = current_solution[:, 0]
            displacements = current_solution * np.array([1.0, 0.0, 0.0])

        elif self.current_menu_widget.comboBox_displacements.currentIndex() == 2:
            disp_type = "u_y"
            color_scalars = current_solution[:, 1]
            displacements = current_solution * np.array([0.0, 1.0, 0.0])

        else:
            disp_type = "u_z"
            color_scalars = current_solution[:, 2]
            displacements = current_solution * np.array([0.0, 0.0, 1.0])

        min_value, max_value = solver.get_max_min_values_of_displacements(index, disp_type)

        return displacements, color_scalars, min_value, max_value