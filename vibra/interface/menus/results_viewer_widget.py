from PySide6.QtWidgets import QFrame, QGridLayout, QWidget

from vibra import app
from vibra.interface.menus.results_viewer_items import ResultsViewerItems
from vibra.interface.plots.acoustic.acoustic_mode_shape_inputs import AcousticModeShapeInputs
from vibra.interface.plots.acoustic.acoustic_pressure_field_inputs import AcousticPressureFieldInputs
from vibra.interface.plots.acoustic.acoustic_pressure_waveform_field_inputs import AcousticPressureWaveformFieldInputs
from vibra.interface.plots.general.animation_widget import AnimationWidget
from vibra.interface.plots.structural.structural_mode_shape_inputs import PlotStructuralModeShapeInputs
from vibra.interface.plots.structural.structural_response_fields_inputs import StructuralResponseFieldsInputs
from vibra.interface.ui_generated.menu.left_menu_widget_ui import LeftMenuWidget_UI


class ResultsViewerWidget(LeftMenuWidget_UI):
    def __init__(self):
        super().__init__()

        self.plot_structural_modal = PlotStructuralModeShapeInputs()
        self.plot_structural_harmonic = StructuralResponseFieldsInputs()
        self.plot_acoustic_modal = AcousticModeShapeInputs()
        self.plot_acoustic_harmonic = AcousticPressureFieldInputs()

        self._reset()
        self._define_qt_variables()
        self._create_connections()

    def _reset(self):
        self.current_widget = None

    def hide_bottom_widget(self):
        self.bottom_widget.hide()

    def current_widget_is_animatable(self) -> bool:
        return isinstance(self.current_widget, (
            PlotStructuralModeShapeInputs,
            StructuralResponseFieldsInputs,
            AcousticModeShapeInputs,
            AcousticPressureFieldInputs,
            AcousticPressureWaveformFieldInputs,
        ))

    def clear_treeWidgets_of_frequencies(self):
        self.plot_structural_modal.treeWidget_frequencies.clear()
        self.plot_structural_harmonic.treeWidget_frequencies.clear()
        self.plot_acoustic_modal.treeWidget_frequencies.clear()
        self.plot_acoustic_harmonic.treeWidget_frequencies.clear()

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
        self.results_viewer_items.item_child_structural_frequency_response.clicked.connect(self.add_structural_frequency_response_widget)
        self.results_viewer_items.item_child_structural_results_fields.clicked.connect(self.add_structural_harmonic_widget)

        # Acoustic
        self.results_viewer_items.item_child_acoustic_pressure_field.clicked.connect(self.add_acoustic_harmonic_widget)
        self.results_viewer_items.item_child_acoustic_pressure_frequency_response.clicked.connect(self.add_acoustic_pressure_frequency_response_widget)
        self.results_viewer_items.item_child_acoustic_pressure_frf.clicked.connect(self.add_acoustic_pressure_frequency_response_function_widget)
        self.results_viewer_items.item_child_acoustic_shaking_forces.clicked.connect(self.add_acoustic_shaking_forces_widget)
        self.results_viewer_items.item_child_decompose_acoustic_waves.clicked.connect(self.add_decompose_acoustic_pressure_waves_widget)
        self.results_viewer_items.item_child_allowable_pulsations_for_reciprocating_compressor.clicked.connect(self.add_allowable_pulsations_for_reciprocating_compressor_widget)
        self.results_viewer_items.item_child_allowable_pulsations_for_screw_compressor.clicked.connect(self.add_allowable_pulsations_for_screw_compressor_widget)
        self.results_viewer_items.item_child_acoustic_pressure_waveform.clicked.connect(self.add_acoustic_pressure_waveform_widget)
        self.results_viewer_items.item_child_acoustic_pressure_waveform_field.clicked.connect(self.add_acoustic_pressure_waveform_widget_field)
        self.results_viewer_items.item_child_allowable_pulsations_field_for_screw_compressor.clicked.connect(self.add_allowable_pulsation_field_for_screw_compressor)
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

    def get_animation_widget(self) -> AnimationWidget | None:
        if self.current_widget_is_animatable():
            return self.current_widget.animation_widget

        return None

    def add_structural_modal_widget(self):
        self.top_widget.setFixedHeight(120)
        self.current_widget = self.plot_structural_modal
        self.plot_structural_modal.load_natural_frequencies()
        self.plot_structural_modal.load_user_preference_colormap()
        self.add_widget(self.plot_structural_modal)

    def add_structural_harmonic_widget(self):
        self.top_widget.setFixedHeight(120)
        self.current_widget = self.plot_structural_harmonic
        self.plot_structural_harmonic.load_frequencies()
        self.plot_structural_harmonic.load_user_preference_colormap()
        self.add_widget(self.plot_structural_harmonic)

    def add_acoustic_modal_widget(self):
        self.top_widget.setFixedHeight(220)
        self.current_widget = self.plot_acoustic_modal
        self.plot_acoustic_modal.load_natural_frequencies()
        self.plot_acoustic_modal.load_user_preference_colormap()
        self.add_widget(self.plot_acoustic_modal)

    def add_acoustic_harmonic_widget(self):
        self.top_widget.setFixedHeight(220)
        self.current_widget = self.plot_acoustic_harmonic
        self.plot_acoustic_harmonic.load_frequencies()
        self.plot_acoustic_harmonic.load_user_preference_colormap()
        self.add_widget(self.plot_acoustic_harmonic)

    def add_structural_frequency_response_widget(self):
        self.current_widget = app().main_window.input_ui.plot_structural_frequency_response()

        if app().main_window.results_widget.playing_animation:
            app().main_window.results_widget.stop_animation()

        self.add_widget(self.current_widget)

    def add_acoustic_pressure_frequency_response_widget(self):
        self.current_widget = app().main_window.input_ui.plot_acoustic_pressure_frequency_response()
        
        if app().main_window.results_widget.playing_animation:
            app().main_window.results_widget.stop_animation()

        self.add_widget(self.current_widget)
    
    def add_acoustic_pressure_frequency_response_function_widget(self):
        self.current_widget = app().main_window.input_ui.plot_acoustic_pressure_frequency_response_function()

        if app().main_window.results_widget.playing_animation:
            app().main_window.results_widget.stop_animation()

        self.add_widget(self.current_widget)

    def add_acoustic_shaking_forces_widget(self):
        self.current_widget = app().main_window.input_ui.plot_acoustic_shaking_forces()

        if app().main_window.results_widget.playing_animation:
            app().main_window.results_widget.stop_animation()

        self.add_widget(self.current_widget)

    def add_decompose_acoustic_pressure_waves_widget(self):
        self.current_widget = app().main_window.input_ui.decompose_acoustic_pressure_waves()

        if app().main_window.results_widget.playing_animation:
            app().main_window.results_widget.stop_animation()

        self.add_widget(self.current_widget)

    def add_allowable_pulsations_for_reciprocating_compressor_widget(self):
        self.current_widget = app().main_window.input_ui.plot_allowable_pulsation_criteria_for_reciprocating_compressor()

        if app().main_window.results_widget.playing_animation:
            app().main_window.results_widget.stop_animation()

        self.add_widget(self.current_widget)

    def add_allowable_pulsations_for_screw_compressor_widget(self):
        self.current_widget = app().main_window.input_ui.plot_allowable_pulsation_criteria_for_screw_compressor()

        if app().main_window.results_widget.playing_animation:
            app().main_window.results_widget.stop_animation()

        self.add_widget(self.current_widget)

    def add_acoustic_pressure_waveform_widget(self):
        self.current_widget = app().main_window.input_ui.plot_acoustic_pressure_waveform()
        
        if app().main_window.results_widget.playing_animation:
            app().main_window.results_widget.stop_animation()

        self.add_widget(self.current_widget)

    def add_acoustic_pressure_waveform_widget_field(self):
        self.current_widget = app().main_window.input_ui.plot_acoustic_pressure_waveform_field()
        
        if app().main_window.results_widget.playing_animation:
            app().main_window.results_widget.stop_animation()

        self.add_widget(self.current_widget)
        self.current_widget.plot_data_callback()

    def add_allowable_pulsation_field_for_screw_compressor(self):
        self.current_widget = app().main_window.input_ui.plot_allowable_pulsation_field_for_screw_compressor()
        
        if app().main_window.results_widget.playing_animation:
            app().main_window.results_widget.stop_animation()

        self.add_widget(self.current_widget)
        self.current_widget.plot_data_callback()

    def add_TL_NR_widget(self):
        self.current_widget = app().main_window.input_ui.plot_TL_NR()

        if app().main_window.results_widget.playing_animation:
            app().main_window.results_widget.stop_animation()

        self.add_widget(self.current_widget)

    def add_particle_velocity_plot_widget(self):
        self.current_widget = app().main_window.input_ui.plot_particle_velocity()

        if app().main_window.results_widget.playing_animation:
            app().main_window.results_widget.stop_animation()

        self.add_widget(self.current_widget)

    def add_acoustic_impedance_plot_widget(self):
        self.current_widget = app().main_window.input_ui.plot_acoustic_impedance()

        if app().main_window.results_widget.playing_animation:
            app().main_window.results_widget.stop_animation()

        self.add_widget(self.current_widget)

    def add_absorption_coefficient_plot_widget(self):
        self.current_widget = app().main_window.input_ui.plot_absorption_coefficient_from_surface()

        if app().main_window.results_widget.playing_animation:
            app().main_window.results_widget.stop_animation()

        self.add_widget(self.current_widget)

    def add_widget(self, widget: QWidget):

        # TODO: please, remove the hide after all it shouldn't be needed
        if isinstance(self.bottom_widget, QWidget):
            self.bottom_widget.hide()

        self.layout().replaceWidget(self.bottom_widget, widget)
        self.bottom_widget = widget

        self.adjustSize()
        widget.show()