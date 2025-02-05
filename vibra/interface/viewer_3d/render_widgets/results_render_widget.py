from typing import Literal

from molde.render_widgets import AnimatedRenderWidget

from vibra import app
from vibra.engine.postprocessing import (
    compute_structural_modal_field,
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
        if self.current_analysis == "structural_modal":
            data = compute_structural_modal_field(
                app().project.structural_modal_solver.modal_shape,
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
        
        elif self.current_analysis == "acoustic_harmonic":
            data = compute_acoustic_harmonic_field(
                app().project.acoustic_harmonic_solver.solution,
                self.current_frequency_index,
                self.current_phase,
            )
        
        else:
            raise ValueError(f"Unknown analysis: {self.current_analysis}")

        self.analysis_actor.apply_deformation(displacements, self.current_phase, self.magnification_factor)
        self.edges_actor.extract_data(self.analysis_actor.data)

        self.analysis_actor.plot_color_bar(color_scalars, min_value, max_value)
        self.colorbar_actor.SetLookupTable(self.analysis_actor.color_table)
        self.update()

    def update_section_plane(self):
        pass
