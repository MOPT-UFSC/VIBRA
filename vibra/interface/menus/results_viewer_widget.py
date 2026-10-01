from PySide6.QtWidgets import QFrame, QGridLayout, QWidget

from vibra import app
from vibra.interface.menus.results_viewer_items import ResultsViewerItems
from vibra.interface.plots.acoustic.acoustic_impedance_inputs import AcousticImpedanceInputs
from vibra.interface.plots.acoustic.acoustic_mode_shape_inputs import AcousticModeShapeInputs
from vibra.interface.plots.acoustic.acoustic_nodal_solution_2d_plot_frequency_inputs import AcousticNodalSolution2dPlotFrequencyInputs
from vibra.interface.plots.acoustic.acoustic_nodal_solution_2d_plot_time_inputs import AcousticNodalSolution2dPlotTimeInputs
from vibra.interface.plots.acoustic.acoustic_nodal_solution_3d_plot_frequency_inputs import AcousticNodalSolution3dPlotFrequencyInputs
from vibra.interface.plots.acoustic.acoustic_nodal_solution_3d_plot_time_inputs import AcousticNodalSolution3dPlotTimeInputs
from vibra.interface.plots.acoustic.acoustic_pressure_frf_inputs import AcousticPressureFRFInputs
from vibra.interface.plots.acoustic.acoustic_shaking_forces_inputs import AcousticShakingForcesInputs
from vibra.interface.plots.acoustic.acoustic_waves_decomposition_inputs import AcousticWavesDecompositionInputs
from vibra.interface.plots.acoustic.allowable_pulsation_3d_plot_for_screw_compressor_inputs import AllowablePulsations3DPlotForScrewCompressorInputs
from vibra.interface.plots.acoustic.allowable_pulsations_2d_plot_for_screw_compressor_inputs import AllowablePulsations2DPlotForScrewCompressorInputs
from vibra.interface.plots.acoustic.allowable_pulsations_for_reciprocating_compressor import AllowablePulsationsForReciprocatingCompressorInputs
from vibra.interface.plots.acoustic.particle_velocity_inputs import ParticleVelocityInputs
from vibra.interface.plots.acoustic.surface_absorption_coefficient_inputs import SurfaceAbsorptionCoefficientInputs
from vibra.interface.plots.acoustic.transmission_loss_inputs import TransmissionLossInputs
from vibra.interface.plots.general.animation_widget import AnimationWidget
from vibra.interface.plots.structural.structural_mode_shape_inputs import StructuralModeShapeInputs
from vibra.interface.plots.structural.structural_nodal_solution_2d_plot_frequency_inputs import StructuralNodalSolution2dPlotFrequencytInputs
from vibra.interface.plots.structural.structural_nodal_solution_2d_plot_time_inputs import StructuralNodalSolution2dPlotTimeInputs
from vibra.interface.plots.structural.structural_nodal_solution_3d_plot_frequency_inputs import StructuralNodalSolution3dPlotFrequencyInputs
from vibra.interface.plots.structural.structural_nodal_solution_3d_plot_time_inputs import StructuralNodalSolution3dPlotTimeInputs
from vibra.interface.plots.structural.structural_stress_2d_plot_frequency_inputs import StructuralStress2dPlotFrequencyInputs
from vibra.interface.plots.structural.structural_stress_2d_plot_time_inputs import StructuralStress2dPlotTimeInputs
from vibra.interface.plots.structural.structural_stress_3d_plot_frequency_inputs import StructuralStress3dPlotFrequencyInputs
from vibra.interface.plots.structural.structural_stress_3d_plot_time_inputs import StructuralStress3dPlotTimeInputs
from vibra.interface.ui_generated.menu.left_menu_widget_ui import LeftMenuWidget_UI


class ResultsViewerWidget(LeftMenuWidget_UI):
    def __init__(self):
        super().__init__()

        self._reset()
        self._define_qt_variables()
        self._create_connections()

    def _reset(self):
        self.current_widget = None
        self.animation_widget: AnimationWidget | None = None

    def process_input(self, working_class, *args, **kwargs):
        app().main_window.close_dialogs()
        read = working_class(*args, **kwargs)
        return read

    def hide_bottom_widget(self):
        self.bottom_widget.hide()

    def current_widget_is_animatable(self) -> bool:
        return isinstance(self.current_widget, (
            StructuralModeShapeInputs,
            StructuralNodalSolution3dPlotFrequencyInputs,
            StructuralNodalSolution3dPlotTimeInputs,
            StructuralStress3dPlotFrequencyInputs,
            StructuralStress3dPlotTimeInputs,
            AcousticModeShapeInputs,
            AcousticNodalSolution3dPlotFrequencyInputs,
            AcousticNodalSolution3dPlotTimeInputs,
        ))

    def _define_qt_variables(self):
        self.main_frame = QFrame()
        self.results_viewer_items = ResultsViewerItems()

        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.top_widget.setLayout(self.grid_layout)

        self.grid_layout.addWidget(self.results_viewer_items)
        self.top_widget.adjustSize()

    def _create_connections(self):

        # Structural
        self.results_viewer_items.item_child_structural_mode_shapes.clicked.connect(self.add_structural_modal_widget)
        self.results_viewer_items.item_child_structural_nodal_solution_2d_plot_frequency.clicked.connect(self.add_structural_nodal_solution_2d_plot_frequency_widget)
        self.results_viewer_items.item_child_structural_nodal_solution_2d_plot_time.clicked.connect(self.add_structural_nodal_solution_2d_plot_time_widget)
        self.results_viewer_items.item_child_structural_nodal_solution_3d_plot_frequency.clicked.connect(self.add_structural_nodal_solution_3d_plot_frequency_widget)
        self.results_viewer_items.item_child_structural_nodal_solution_3d_plot_time.clicked.connect(self.add_structural_nodal_solution_3d_plot_time_widget)
        self.results_viewer_items.item_child_stresses_3d_plot_frequency.clicked.connect(self.add_stresses_frequency_domain_3d_plot_widget)
        self.results_viewer_items.item_child_stresses_3d_plot_time.clicked.connect(self.add_stresses_time_domain_3d_plot_widget)
        self.results_viewer_items.item_child_stresses_2d_plot_frequency.clicked.connect(self.add_stresses_frequency_domain_2d_plot_widget)
        self.results_viewer_items.item_child_stresses_2d_plot_time.clicked.connect(self.add_stresses_time_domain_2d_plot_widget)

        # Acoustic
        self.results_viewer_items.item_child_acoustic_nodal_solution_2d_plot_frequency.clicked.connect(self.add_acoustic_nodal_solution_2d_plot_frequency_widget)
        self.results_viewer_items.item_child_acoustic_nodal_solution_3d_plot_frequency.clicked.connect(self.add_acoustic_nodal_solution_3d_plot_frequency_widget)
        self.results_viewer_items.item_child_acoustic_nodal_solution_frf.clicked.connect(self.add_acoustic_nodal_solution_frf_widget)
        self.results_viewer_items.item_child_acoustic_shaking_forces.clicked.connect(self.add_acoustic_shaking_forces_widget)
        self.results_viewer_items.item_child_decompose_acoustic_waves.clicked.connect(self.add_decompose_acoustic_pressure_waves_widget)
        self.results_viewer_items.item_child_acoustic_nodal_solution_2d_plot_time.clicked.connect(self.add_acoustic_nodal_solution_2d_plot_time_widget)
        self.results_viewer_items.item_child_acoustic_nodal_solution_3d_plot_time.clicked.connect(self.add_acoustic_nodal_solution_3d_plot_time_widget)
        self.results_viewer_items.item_child_allowable_pulsations_screw_compressor_2d_plot.clicked.connect(self.add_allowable_pulsations_for_screw_compressor_2d_plot_widget)
        self.results_viewer_items.item_child_allowable_pulsations_screw_compressor_3d_plot.clicked.connect(self.add_allowable_pulsations_for_screw_compressor_3d_plot_widget)
        self.results_viewer_items.item_child_allowable_pulsations_for_reciprocating_compressor.clicked.connect(self.add_allowable_pulsations_for_reciprocating_compressor_widget)
        self.results_viewer_items.item_child_TL_NR.clicked.connect(self.add_TL_NR_widget)
        self.results_viewer_items.item_child_acoustic_mode_shapes.clicked.connect(self.add_acoustic_modal_widget)
        self.results_viewer_items.item_child_particle_velocity.clicked.connect(self.add_particle_velocity_plot_widget)
        self.results_viewer_items.item_child_acoustic_impedance.clicked.connect(self.add_acoustic_impedance_plot_widget)
        self.results_viewer_items.item_child_absorption_coefficient.clicked.connect(self.add_absorption_coefficient_plot_widget)

    def get_item(self):
        return self.results_viewer_items

    def update_visibility_items(self):
        self.results_viewer_items._update_items()
        self.results_viewer_items.update_tree_visibility_after_solution()

    def add_structural_modal_widget(self):
        self.top_widget.setFixedHeight(120)
        self.current_widget = self.process_input(StructuralModeShapeInputs)

        if app().main_window.results_widget.playing_animation:
            app().main_window.results_widget.stop_animation()

        self.add_widget(self.current_widget)

    def add_structural_nodal_solution_3d_plot_frequency_widget(self):
        self.top_widget.setFixedHeight(120)
        self.current_widget = self.process_input(StructuralNodalSolution3dPlotFrequencyInputs)

        if app().main_window.results_widget.playing_animation:
            app().main_window.results_widget.stop_animation()

        self.add_widget(self.current_widget)

    def add_structural_nodal_solution_3d_plot_time_widget(self):
        self.current_widget = self.process_input(StructuralNodalSolution3dPlotTimeInputs)

        if app().main_window.results_widget.playing_animation:
            app().main_window.results_widget.stop_animation()

        self.add_widget(self.current_widget)

    def add_stresses_frequency_domain_3d_plot_widget(self):
        self.current_widget = self.process_input(StructuralStress3dPlotFrequencyInputs)

        if app().main_window.results_widget.playing_animation:
            app().main_window.results_widget.stop_animation()

        self.add_widget(self.current_widget)

    def add_stresses_time_domain_3d_plot_widget(self):
        self.current_widget = self.process_input(StructuralStress3dPlotTimeInputs)

        if app().main_window.results_widget.playing_animation:
            app().main_window.results_widget.stop_animation()

        self.add_widget(self.current_widget)

    def add_stresses_frequency_domain_2d_plot_widget(self):
        self.current_widget = self.process_input(StructuralStress2dPlotFrequencyInputs)

        if app().main_window.results_widget.playing_animation:
            app().main_window.results_widget.stop_animation()

        self.add_widget(self.current_widget)

    def add_stresses_time_domain_2d_plot_widget(self):
        self.current_widget = self.process_input(StructuralStress2dPlotTimeInputs)

        if app().main_window.results_widget.playing_animation:
            app().main_window.results_widget.stop_animation()

        self.add_widget(self.current_widget)

    def add_acoustic_modal_widget(self):
        self.top_widget.setFixedHeight(220)
        self.current_widget = self.process_input(AcousticModeShapeInputs)

        if app().main_window.results_widget.playing_animation:
            app().main_window.results_widget.stop_animation()

        self.add_widget(self.current_widget)

    def add_acoustic_nodal_solution_3d_plot_frequency_widget(self):
        self.top_widget.setFixedHeight(220)
        self.current_widget = self.process_input(AcousticNodalSolution3dPlotFrequencyInputs)

        if app().main_window.results_widget.playing_animation:
            app().main_window.results_widget.stop_animation()

        self.add_widget(self.current_widget)

    def add_structural_nodal_solution_2d_plot_frequency_widget(self):
        self.current_widget = self.process_input(StructuralNodalSolution2dPlotFrequencytInputs)

        if app().main_window.results_widget.playing_animation:
            app().main_window.results_widget.stop_animation()

        self.add_widget(self.current_widget)

    def add_structural_nodal_solution_2d_plot_time_widget(self):
        self.current_widget = self.process_input(StructuralNodalSolution2dPlotTimeInputs)

        if app().main_window.results_widget.playing_animation:
            app().main_window.results_widget.stop_animation()

        self.add_widget(self.current_widget)

    def add_acoustic_nodal_solution_2d_plot_frequency_widget(self):
        self.current_widget = self.process_input(AcousticNodalSolution2dPlotFrequencyInputs)

        if app().main_window.results_widget.playing_animation:
            app().main_window.results_widget.stop_animation()

        self.add_widget(self.current_widget)

    def add_acoustic_nodal_solution_frf_widget(self):
        self.current_widget = self.process_input(AcousticPressureFRFInputs)

        if app().main_window.results_widget.playing_animation:
            app().main_window.results_widget.stop_animation()

        self.add_widget(self.current_widget)

    def add_acoustic_shaking_forces_widget(self):
        self.current_widget = self.process_input(AcousticShakingForcesInputs)

        if app().main_window.results_widget.playing_animation:
            app().main_window.results_widget.stop_animation()

        self.add_widget(self.current_widget)

    def add_decompose_acoustic_pressure_waves_widget(self):
        self.current_widget = self.process_input(AcousticWavesDecompositionInputs)

        if app().main_window.results_widget.playing_animation:
            app().main_window.results_widget.stop_animation()

        self.add_widget(self.current_widget)

    def add_allowable_pulsations_for_reciprocating_compressor_widget(self):
        self.current_widget = self.process_input(AllowablePulsationsForReciprocatingCompressorInputs)

        if app().main_window.results_widget.playing_animation:
            app().main_window.results_widget.stop_animation()

        self.add_widget(self.current_widget)

    def add_allowable_pulsations_for_screw_compressor_widget(self):
        self.current_widget = app().main_window.input_ui.plot_allowable_pulsation_criteria_for_screw_compressor()

        if app().main_window.results_widget.playing_animation:
            app().main_window.results_widget.stop_animation()

        self.add_widget(self.current_widget)

    def add_acoustic_nodal_solution_2d_plot_time_widget(self):
        self.current_widget = self.process_input(AcousticNodalSolution2dPlotTimeInputs)

        if app().main_window.results_widget.playing_animation:
            app().main_window.results_widget.stop_animation()

        self.add_widget(self.current_widget)

    def add_acoustic_nodal_solution_3d_plot_time_widget(self):
        self.current_widget = self.process_input(AcousticNodalSolution3dPlotTimeInputs)

        if app().main_window.results_widget.playing_animation:
            app().main_window.results_widget.stop_animation()

        self.add_widget(self.current_widget)

    def add_allowable_pulsations_for_screw_compressor_2d_plot_widget(self):
        self.current_widget = self.process_input(AllowablePulsations2DPlotForScrewCompressorInputs)

        if app().main_window.results_widget.playing_animation:
            app().main_window.results_widget.stop_animation()

        self.add_widget(self.current_widget)

    def add_allowable_pulsations_for_screw_compressor_3d_plot_widget(self):
        self.current_widget = self.process_input(AllowablePulsations3DPlotForScrewCompressorInputs)

        if app().main_window.results_widget.playing_animation:
            app().main_window.results_widget.stop_animation()

        self.add_widget(self.current_widget)

    def add_TL_NR_widget(self):
        self.current_widget = self.process_input(TransmissionLossInputs)

        if app().main_window.results_widget.playing_animation:
            app().main_window.results_widget.stop_animation()

        self.add_widget(self.current_widget)

    def add_particle_velocity_plot_widget(self):
        self.current_widget = self.process_input(ParticleVelocityInputs)

        if app().main_window.results_widget.playing_animation:
            app().main_window.results_widget.stop_animation()

        self.add_widget(self.current_widget)

    def add_acoustic_impedance_plot_widget(self):
        self.current_widget = self.process_input(AcousticImpedanceInputs)

        if app().main_window.results_widget.playing_animation:
            app().main_window.results_widget.stop_animation()

        self.add_widget(self.current_widget)

    def add_absorption_coefficient_plot_widget(self):
        self.current_widget = self.process_input(SurfaceAbsorptionCoefficientInputs)

        if app().main_window.results_widget.playing_animation:
            app().main_window.results_widget.stop_animation()

        self.add_widget(self.current_widget)

    def add_widget(self, widget: QWidget):

        # update the animation widget attribute
        self.animation_widget = None
        if self.current_widget_is_animatable():
            self.animation_widget = self.current_widget.animation_widget

        # TODO: please, remove the hide after all it shouldn't be needed
        if isinstance(self.bottom_widget, QWidget):
            self.bottom_widget.hide()

        configure_results_display_widget = getattr(widget, "configure_results_display_widget", None)
        if configure_results_display_widget is not None:
            configure_results_display_widget()

        self.layout().replaceWidget(self.bottom_widget, widget)
        self.bottom_widget = widget

        self.adjustSize()
        widget.show()