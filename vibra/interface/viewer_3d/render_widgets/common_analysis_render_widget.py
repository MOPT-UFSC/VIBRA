from PyQt5.QtWidgets import QFileDialog

from molde.render_widgets import AnimatedRenderWidget

from vibra import app
from ..actors.edges_actor import EdgesActor
from ..actors.ghost_actor import GhostActor
from ..actors.section_plane_actor import SectionPlaneActor
from ..actors.analysis_actor import AnalysisActor
from ..actors.hollow_analysis_actor import HollowAnalysisActor
from ..coloring.color_table import ColorTable


class CommonAnalysisRenderWidget(AnimatedRenderWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.create_axes()
        self.create_color_bar()
        self.create_scale_bar()

    def update_plot(self, reset_camera=False):
        mesh = app().project.model.mesh
        if mesh is None:
            return

        self.remove_all_actors()

        self.analysis_actor = HollowAnalysisActor(mesh)
        self.edges_actor = EdgesActor(self.analysis_actor.data)
        self.ghost_actor = GhostActor(mesh)
        self.plane_actor = SectionPlaneActor(self.analysis_actor.GetBounds())

        self.update_color_and_deformation()

        self.add_actors(
            self.analysis_actor,
            self.edges_actor,
            self.ghost_actor,
            self.plane_actor,
        )

        has_hidden_part = bool(app().main_window.hidden_surfaces)
        self.ghost_actor.SetVisibility(has_hidden_part)
        self.plane_actor.VisibilityOff()

        if reset_camera:
            self.renderer.ResetCamera()

        self.update_section_plane()
        app().project.thumbnail = self.get_thumbnail()

    def update_color_and_deformation(self):
        pass

    def _actors_exists(self):
        return len(self._widget_actors) > 0

    def update_section_plane(self):
        if not self._actors_exists():
            return

        section_plane = app().main_window.section_plane

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
        else:
            self._apply_section_plane(position, rotation, inverted)
            self.ghost_actor.VisibilityOn()
            self.plane_actor.SetVisibility(not section_plane.keep_section_plane)
            self.plane_actor.GetProperty().SetColor(0.5, 0.5, 0.5)
            self.plane_actor.GetProperty().SetOpacity(0.2)

        self.update()

    def export_animation_to_file(self):
        file_path, check = QFileDialog.getSaveFileName(
            self,
            "Save As",
            filter="All Files ();; Video (*.mp4);; GIF (*.gif);;",
        )

        if not check:
            return

        self.save_video(file_path)

    def _disable_section_plane(self):
        has_hidden_part = bool(app().main_window.hidden_surfaces)
        self.ghost_actor.SetVisibility(has_hidden_part)
        self.plane_actor.VisibilityOff()
        self.analysis_actor.disable_cut()
        self.edges_actor.disable_cut()
        self.update()

    def _apply_section_plane(self, position, rotation, inverted):
        if isinstance(self.solids_actor, HollowAnalysisActor):
            mesh = app().project.model.mesh
            if mesh is None:
                return

            self.remove_actors(self.solids_actor)
            self.solids_actor = AnalysisActor(mesh)
            self.add_actors(self.solids_actor)

        self.plane_actor.configure_section_plane(position, rotation)
        xyz = self.plane_actor.calculate_xyz_position(position)
        normal = self.plane_actor.calculate_normal_vector(rotation)
        if inverted:
            normal = -normal

        self.analysis_actor.apply_cut(xyz, normal)
        self.edges_actor.apply_cut(xyz, normal)
        self.update()