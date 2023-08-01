import numpy as np
from PyQt5.QtCore import QObjectCleanupHandler
from PyQt5.QtWidgets import *

from vibra.interface.viewer_3d.actors.analysis_actor import AnalysisActor
from vibra.interface.viewer_3d.actors.edges_actor import EdgesActor
from vibra.interface.viewer_3d.actors.cutting_plane_actor import (
    CuttingPlaneActor,
)
from vibra.interface.viewer_3d.common_render_widget import CommonRenderWidget
from vibra.interface.modal_analysis_bar import AcousticModalAnalysisBar
from vibra.utils.math_functions import bounds_distance, lerp, rotation_matrices


class AcousticHarmonicAnalysisRenderWidget(CommonRenderWidget):
    def __init__(self, project, parent=None):
        super().__init__(parent)

        self.project = project        
        self.control_bar = AcousticModalAnalysisBar()
        self.control_bar.plot_changed.connect(self.update_plot)
        self.control_bar.show_mesh_button.stateChanged.connect(self.set_mesh_visibility)

        # replace the layout to add other usefull widgets
        QObjectCleanupHandler().add(self.layout())
        layout = QVBoxLayout()
        layout.addWidget(self.control_bar)
        layout.addWidget(self.render_interactor)
        self.setLayout(layout)
        self.setContentsMargins(0, 0, 0, 0)

        self.analysis_actor = None
        self.edges_actor = None
        self.plane_actor = None
        self.bounds = (0, 0, 0, 0, 0, 0)

        self.create_axes()
        self.create_color_bar()
        self.update_frequencies()
        self.update_plot()

    def current_shape_index(self):
        return self.control_bar.frequency_box.currentIndex()
    
    def update_frequencies(self):
        solver = self.project.acoustic_harmonic_solver
        if solver is None:
            return
        self.control_bar.set_frequencies(solver.frequencies)

    def update_plot(self):
        if self.project is None:
            return

        model = self.project.model
        if model is None:
            return

        mesh = model.mesh
        if mesh is None:
            return

        solver = self.project.acoustic_harmonic_solver
        if solver.solution is None:
            return

        index = self.current_shape_index()
        if not (0 <= index < solver.solution.shape[1]):
            return

        self.update_theme()
        self.remove_actors()

        phase_deg = self.control_bar.phase_slider.value()
        phi_sld = phase_deg*np.pi/180

        current_pressures = solver.solution[:, index].copy()
        amplitudes = np.abs(current_pressures)
        phase = np.angle(current_pressures)
        output_pressures = amplitudes*np.cos(phase + phi_sld)

        min_value, max_value = solver.get_max_min_values_of_pressures(index)
        if self.control_bar.absolute_button.isChecked():
            min_value = 0
            output_pressures = np.abs(output_pressures)
        
        self.analysis_actor = AnalysisActor(mesh)
        self.analysis_actor.plot_colorbar(output_pressures, min_value, max_value)
        self.colorbar.SetLookupTable(self.analysis_actor.lookup_table)
        self.renderer.AddActor(self.analysis_actor)

        self.edges_actor = EdgesActor(self.analysis_actor.data)
        self.edges_actor.GetProperty().SetColor(0, 0, 0)
        self.renderer.AddActor(self.edges_actor)

        self.bounds = self.analysis_actor.GetBounds()
        scale = bounds_distance(self.bounds)
        self.plane_actor = CuttingPlaneActor()
        self.plane_actor.VisibilityOff()
        self.plane_actor.SetScale(scale, scale, scale)
        self.renderer.AddActor(self.plane_actor)
    
        mesh_visibility = self.control_bar.show_mesh_button.isChecked()
        self.set_mesh_visibility(mesh_visibility)

        if self.control_bar.show_mesh_button.isChecked():
            self.analysis_actor.VisibilityOn()
            self.analysis_actor.GetProperty().SetRepresentationToSurface()
            self.edges_actor.VisibilityOn()

        self.renderer.ResetCamera()
        self.update()

    def set_mesh_visibility(self, condition):
        if not self._actors_exists():
            return

        if condition:
            self.show_lines()
        else:
            self.show_faces()

    def show_points(self):
        if not self._actors_exists():
            return
        
        self.control_bar.show_mesh_button.setChecked(False)
        self.analysis_actor.VisibilityOn()
        self.analysis_actor.GetProperty().SetRepresentationToPoints()
        self.edges_actor.VisibilityOff()
        self.update()

    def show_lines(self):
        if not self._actors_exists():
            return
        
        self.control_bar.show_mesh_button.setChecked(True)
        self.analysis_actor.VisibilityOn()
        self.analysis_actor.GetProperty().SetRepresentationToSurface()
        self.edges_actor.VisibilityOn()
        self.update()

    def show_faces(self):
        if not self._actors_exists():
            return
        
        self.control_bar.show_mesh_button.setChecked(False)
        self.analysis_actor.VisibilityOn()
        self.analysis_actor.GetProperty().SetRepresentationToSurface()
        self.edges_actor.VisibilityOff()
        self.update()

    def start_cutting_mode(self):
        if not self._actors_exists():
            return
        self.plane_actor.VisibilityOn()

    def stop_cutting_mode(self):
        if not self._actors_exists():
            return
        self.plane_actor.VisibilityOff()
        self.analysis_actor.disable_cut()

    def configure_cutting_plane(self, position, orientation):
        if not self._actors_exists():
            return

        x = lerp(self.bounds[0], self.bounds[1], position[0] / 100)
        y = lerp(self.bounds[2], self.bounds[3], position[1] / 100)
        z = lerp(self.bounds[4], self.bounds[5], position[2] / 100)
        self.plane_actor.SetPosition(x, y, z)
        self.plane_actor.SetOrientation(orientation)

        self.plane_actor.GetProperty().SetColor(0, 0.333, 0.867)
        self.plane_actor.GetProperty().SetOpacity(0.8)
        self.update()

    def apply_cutting_plane(self, position, orientation):
        if not self._actors_exists():
            return
        
        x = lerp(self.bounds[0], self.bounds[1], position[0] / 100)
        y = lerp(self.bounds[2], self.bounds[3], position[1] / 100)
        z = lerp(self.bounds[4], self.bounds[5], position[2] / 100)
        normal = self._calculate_normal_vector(orientation)
        self.analysis_actor.apply_cut((x, y, z), normal)

        self.plane_actor.GetProperty().SetColor(0.5, 0.5, 0.5)
        self.plane_actor.GetProperty().SetOpacity(0.2)

        self.update()

    def remove_actors(self):
        self.renderer.RemoveActor(self.analysis_actor)
        self.renderer.RemoveActor(self.edges_actor)
        self.renderer.RemoveActor(self.plane_actor)
        self.analysis_actor = None
        self.edges_actor = None
        self.plane_actor = None

    def _actors_exists(self):
        actors = [
            self.analysis_actor,
            self.edges_actor,
            self.plane_actor,
        ]

        return all([actor is not None for actor in actors])

    def _calculate_normal_vector(self, orientation):
        # https://forum.gamemaker.io/index.php?threads/solved-3d-rotations-with-a-shader-matrix-or-a-matrix-glsl-es.61064/

        orientation = np.array(orientation) * np.pi / 180
        rx, ry, rz = rotation_matrices(*orientation)

        normal = rz @ rx @ ry @ np.array([1, 0, 0, 1])
        return normal[:3]
