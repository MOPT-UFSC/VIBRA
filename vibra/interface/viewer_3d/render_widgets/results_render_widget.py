from typing import Literal
from PySide6.QtWidgets import QFileDialog

from molde.render_widgets import AnimatedRenderWidget

from vibra import app
from vibra.engine.postprocessing import (
    compute_structural_modal_field,
    compute_structural_harmonic_field,
    compute_acoustic_modal_field,
    compute_acoustic_harmonic_field,
)

from ..actors import (
    EdgesActor,
    GhostActor,
    SectionPlaneActor,
    AnalysisActor,
    HollowAnalysisActor,
)

# Just for type hints
AnalysisType = Literal[
    "",
    "structural_modal",
    "acoustic_modal",
    "acoustic_harmonic",
]

class ResultsRenderWidget(AnimatedRenderWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.current_analysis: AnalysisType = ""
        self.current_frequency_index = 0
        self.current_phase = 0
        self.magnification_factor = 1

        self.create_axes()
        self.create_color_bar()
        self.create_scale_bar()
        self.update_plot()

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
        displacements = None

        if self.current_analysis == "structural_modal":
            data = compute_structural_modal_field(
                app().project.structural_modal_solver.modal_shape,
                self.current_frequency_index, 
                self.current_phase,
            )
            displacements, color_scalars, min_value, max_value = data

        elif self.current_analysis == "structural_harmonic":
            data = compute_structural_harmonic_field(
                app().project.structural_harmonic_solver.solution,
                self.current_frequency_index,
                self.current_phase,
            )
            displacements, color_scalars, min_value, max_value = data

        elif self.current_analysis == "acoustic_modal":
            data = compute_acoustic_modal_field(
                app().project.acoustic_modal_solver.modal_shape,
                self.current_frequency_index,
                self.current_phase,
            )
            color_scalars, min_value, max_value = data

        elif self.current_analysis == "acoustic_harmonic":
            data = compute_acoustic_harmonic_field(
                app().project.acoustic_harmonic_solver.solution,
                self.current_frequency_index,
                self.current_phase,
            )
            color_scalars, min_value, max_value = data

        else:
            raise ValueError(f"Unknown analysis: {self.current_analysis}")

        if displacements is not None:
            self.analysis_actor.apply_deformation(
                displacements,
                self.current_phase,
                self.magnification_factor,
            )
            self.edges_actor.extract_data(self.analysis_actor.data)

        self.analysis_actor.plot_color_bar(color_scalars, min_value, max_value)
        self.colorbar_actor.SetLookupTable(self.analysis_actor.color_table)
        self.update()

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
            show_plane = not section_plane.keep_section_plane
            self._apply_section_plane(position, rotation, inverted, show_plane)

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

    def _apply_section_plane(self, position, rotation, inverted, show_plane=True):
        if isinstance(self.solids_actor, HollowAnalysisActor):
            mesh = app().project.model.mesh
            self.remove_actors(self.solids_actor)
            self.solids_actor = AnalysisActor(mesh)
            self.add_actors(self.solids_actor)

        xyz, normal = self.plane_actor.configure_section_plane(position, rotation)
        if inverted:
            normal = -normal

        self.analysis_actor.apply_cut(xyz, normal)
        self.edges_actor.apply_cut(xyz, normal)
        self.update()
    
        self.ghost_actor.VisibilityOn()
        self.plane_actor.SetVisibility(show_plane)
        self.plane_actor.GetProperty().SetColor(0.5, 0.5, 0.5)
        self.plane_actor.GetProperty().SetOpacity(0.2)


    def _actors_exists(self):
        return len(self._widget_actors) > 0
