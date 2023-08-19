import numpy as np

from vibra.interface.viewer_3d.actors.analysis_actor import AnalysisActor
from vibra.interface.viewer_3d.actors.cutting_plane_actor import (
    CuttingPlaneActor,
)
from vibra.interface.viewer_3d.render_widgets.common_render_widget import CommonRenderWidget
from vibra.utils.math_functions import bounds_distance, lerp, rotation_matrices


class ExampleAnalysisRenderWidget(CommonRenderWidget):
    def __init__(self, project, parent=None):
        super().__init__(parent)

        self.project = project

        self.model_actor = None
        self.plane_actor = None
        self.bounds = (0, 0, 0, 0, 0, 0)

        self.update_plot()
        self.create_color_bar()
        self.create_axes()

    def update_plot(self):
        if self.project is None:
            return

        solver = self.project.acoustic_modal_solver
        # if solver.tensions is None:
        #     return

        model = self.project.model
        if model is None:
            return

        mesh = model.mesh
        if mesh is None:
            return

        self.remove_actors()

        self.model_actor = AnalysisActor(mesh)
        self.model_actor.plot_colorbar(solver.tensions)
        self.renderer.AddActor(self.model_actor)
        self.colorbar.SetLookupTable(self.model_actor.lookup_table)

        self.bounds = self.model_actor.GetBounds()
        scale = bounds_distance(self.bounds)
        self.plane_actor = CuttingPlaneActor()
        self.plane_actor.VisibilityOff()
        self.plane_actor.SetScale(scale, scale, scale)
        self.renderer.AddActor(self.plane_actor)

        self.renderer.ResetCamera()

    def show_points(self):
        if not self._actors_exists():
            return
        self.model_actor.GetProperty().SetRepresentationToPoints()
        self.update()

    def show_lines(self):
        if not self._actors_exists():
            return
        self.model_actor.GetProperty().SetRepresentationToWireframe()
        self.update()

    def show_faces(self):
        if not self._actors_exists():
            return
        self.model_actor.GetProperty().SetRepresentationToSurface()
        self.update()

    def configure_plane(self, position, orientation):
        if not self._actors_exists():
            return

        x = lerp(self.bounds[0], self.bounds[1], position[0] / 100)
        y = lerp(self.bounds[2], self.bounds[3], position[1] / 100)
        z = lerp(self.bounds[4], self.bounds[5], position[2] / 100)
        self.plane_actor.SetPosition(x, y, z)
        self.plane_actor.SetOrientation(orientation)
        self.plane_actor.VisibilityOn()
        self.update()

    def apply_cut(self, position, orientation):
        if not self._actors_exists():
            return

        x = lerp(self.bounds[0], self.bounds[1], position[0] / 100)
        y = lerp(self.bounds[2], self.bounds[3], position[1] / 100)
        z = lerp(self.bounds[4], self.bounds[5], position[2] / 100)
        normal = self._calculate_normal_vector(orientation)

        # actually I dont know why we need to sum the
        # normal vector but it works perfectly
        position = (x, y, z)
        self.model_actor.apply_cut(position, normal)
        self.update()

    def disable_cut(self):
        if not self._actors_exists():
            return
        self.plane_actor.VisibilityOff()
        self.model_actor.disable_cut()
        self.update()

    def show_plane(self):
        if not self._actors_exists():
            return
        self.plane_actor.VisibilityOn()
        self.plane_actor.GetProperty().SetOpacity(0.8)
        self.plane_actor.GetProperty().SetColor(0, 0.333, 0.867)
        self.update()

    def hide_plane(self):
        if not self._actors_exists():
            return
        self.plane_actor.GetProperty().SetOpacity(0.2)
        self.plane_actor.GetProperty().SetColor(0.5, 0.5, 0.5)
        self.update()

    def remove_actors(self):
        self.renderer.RemoveActor(self.model_actor)
        self.renderer.RemoveActor(self.plane_actor)
        self.model_actor = None
        self.plane_actor = None

    def _actors_exists(self):
        actors = [
            self.model_actor,
            self.plane_actor,
        ]

        return all([actor is not None for actor in actors])

    def _calculate_normal_vector(self, orientation):
        # https://forum.gamemaker.io/index.php?threads/solved-3d-rotations-with-a-shader-matrix-or-a-matrix-glsl-es.61064/

        orientation = np.array(orientation) * np.pi / 180
        rx, ry, rz = rotation_matrices(*orientation)

        normal = rz @ rx @ ry @ np.array([1, 0, 0, 1])
        return normal[:3]
