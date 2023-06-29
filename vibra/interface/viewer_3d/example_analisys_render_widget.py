import numpy as np

from vibra.interface.viewer_3d.actors.analisys_actor import AnalisysActor
from vibra.interface.viewer_3d.actors.cutting_plane_actor import (
    CuttingPlaneActor,
)
from vibra.interface.viewer_3d.common_render_widget import CommonRenderWidget
from vibra.utils.math_functions import distance_points, lerp, rotation_matrices


class ExampleAnalisysRenderWidget(CommonRenderWidget):
    def __init__(self, project, parent=None):
        super().__init__(parent)

        self.project = project

        self.model_actor = None
        self.plane_actor = None
        self.bounds = (0, 0, 0, 0, 0, 0)

        self.create_axes()
        self.update_plot()

    def update_plot(self):
        if self.project is None:
            return

        solver = self.project.example_solver
        if solver.tensions is None:
            return

        model = self.project.model
        if model is None:
            return

        mesh = model.simulation_mesh
        if mesh is None:
            return

        self.remove_actors()

        self.model_actor = AnalisysActor(mesh)
        self.model_actor.plot_colorbar(solver.tensions)
        self.renderer.AddActor(self.model_actor)

        self.bounds = self.model_actor.GetBounds()
        scale = distance_points(self.bounds)
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
        self.model_actor.apply_cut((x, y, z), normal)
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
