from PySide6.QtWidgets import QFrame, QWidget

from vibra import app
from vibra.interface.ui_generated.menu.left_menu_widget_ui import LeftMenuWidget_UI
from vibra.interface.menus.results_viewer_items import ResultsViewerItems
from vibra.interface.plots.acoustic.acoustic_mode_shape_inputs import AcousticModeShapeInputs
from vibra.interface.plots.acoustic.acoustic_pressure_field_inputs import AcousticPressureFieldInputs
from vibra.interface.plots.structural.displacement_field_inputs import PlotDisplacementFieldInputs
from vibra.interface.plots.structural.structural_mode_shape_inputs import PlotStructuralModeShapeInputs


class ResultsViewerWidget(LeftMenuWidget_UI):
    def __init__(self):
        super().__init__()

        self.plot_structural_modal = PlotStructuralModeShapeInputs()
        self.plot_structural_harmonic = PlotDisplacementFieldInputs()
        self.plot_acoustic_modal = AcousticModeShapeInputs()
        self.plot_acoustic_harmonic = AcousticPressureFieldInputs()

        self._reset()
        self._define_qt_variables()
        self._create_connections()

    def _reset(self):
        self.current_widget = None
    
    def hide_bottom_widget(self):
        self.bottom_widget.hide()

    def _define_qt_variables(self):
        self.main_frame = QFrame()
        self.results_viewer_items = ResultsViewerItems()
        
        self.layout().replaceWidget(self.top_widget, self.results_viewer_items)
        self.adjustSize()
    
    def _create_connections(self):

        # Structural
        self.results_viewer_items.item_child_structural_mode_shapes.clicked.connect(self.add_structural_modal_widget)
        self.results_viewer_items.item_child_structural_frequency_response.clicked.connect(self.add_structural_frequency_response_widget)
        self.results_viewer_items.item_child_displacement_field.clicked.connect(self.add_structural_harmonic_widget)

        # Acoustic
        self.results_viewer_items.item_child_acoustic_pressure_field.clicked.connect(self.add_acoustic_harmonic_widget)
        self.results_viewer_items.item_child_acoustic_pressure_frequency_response.clicked.connect(self.add_acoustic_pressure_frequency_response_widget)
        self.results_viewer_items.item_child_acoustic_pressure_frequency_response_function.clicked.connect(self.add_acoustic_pressure_frequency_response_function_widget)
        self.results_viewer_items.item_child_TL_NR.clicked.connect(self.add_TL_NR_widget)
        self.results_viewer_items.item_child_acoustic_mode_shapes.clicked.connect(self.add_acoustic_modal_widget)
        self.results_viewer_items.item_child_particle_velocity.clicked.connect(self.add_particle_velocity_plot_widget)
        self.results_viewer_items.item_child_acoustic_specific_impedance.clicked.connect(self.add_acoustic_specific_impedance_plot_widget)

    def get_item(self):
        return self.results_viewer_items

    def update_visibility_items(self):
        self.results_viewer_items._update_items()
        self.results_viewer_items.update_tree_visibility_after_solution()

    def add_structural_modal_widget(self):
        self.plot_structural_modal.load_natural_frequencies()
        self.plot_structural_modal.load_user_preference_colormap()
        self.plot_structural_modal.update_plot()
        self.add_widget(self.plot_structural_modal)

    def add_structural_harmonic_widget(self):
        self.plot_structural_harmonic.load_frequencies()
        self.plot_structural_harmonic.load_user_preference_colormap()
        self.plot_structural_harmonic.update_plot()
        self.add_widget(self.plot_structural_harmonic)

    def add_acoustic_modal_widget(self):
        self.plot_acoustic_modal.load_natural_frequencies()
        self.plot_acoustic_modal.load_user_preference_colormap()
        self.plot_acoustic_modal.update_plot()
        self.add_widget(self.plot_acoustic_modal)

    def add_acoustic_harmonic_widget(self):
        self.plot_acoustic_harmonic.load_frequencies()
        self.plot_acoustic_harmonic.load_user_preference_colormap()
        self.plot_acoustic_harmonic.update_plot()
        self.add_widget(self.plot_acoustic_harmonic)

    def add_structural_frequency_response_widget(self):
        self.current_widget = app().main_window.input_ui.plot_structural_frequency_response()

        if app().main_window.results_widget.playing_animation:
            app().main_window.results_widget.stop_animation()
        
        app().main_window.animation_toolbar.setDisabled(True)

        self.add_widget(self.current_widget)

    def add_acoustic_pressure_frequency_response_widget(self):
        self.current_widget = app().main_window.input_ui.plot_acoustic_pressure_frequency_response()
        
        if app().main_window.results_widget.playing_animation:
            app().main_window.results_widget.stop_animation()

        app().main_window.animation_toolbar.setDisabled(True)

        self.add_widget(self.current_widget)
    
    def add_acoustic_pressure_frequency_response_function_widget(self):
        self.current_widget = app().main_window.input_ui.plot_acoustic_pressure_frequency_response_function()

        if app().main_window.results_widget.playing_animation:
            app().main_window.results_widget.stop_animation()

        self.add_widget(self.current_widget)
    
    def add_TL_NR_widget(self):
        self.current_widget = app().main_window.input_ui.plot_TL_NR()

        if app().main_window.results_widget.playing_animation:
            app().main_window.results_widget.stop_animation()
        
        app().main_window.animation_toolbar.setDisabled(True)

        self.add_widget(self.current_widget)

    def add_particle_velocity_plot_widget(self):
        self.current_widget = app().main_window.input_ui.plot_particle_velocity()

        if app().main_window.results_widget.playing_animation:
            app().main_window.results_widget.stop_animation()
        
        app().main_window.animation_toolbar.setDisabled(True)

        self.add_widget(self.current_widget)

    def add_acoustic_specific_impedance_plot_widget(self):
        self.current_widget = app().main_window.input_ui.plot_acoustic_specific_impedance_from_surface()

        if app().main_window.results_widget.playing_animation:
            app().main_window.results_widget.stop_animation()
        
        app().main_window.animation_toolbar.setDisabled(True)

        self.add_widget(self.current_widget)

    def add_widget(self, widget: QWidget):

        # TODO: please, remove the hide after all it shouldn't be needed
        if isinstance(self.bottom_widget, QWidget):
            self.bottom_widget.hide()

        self.layout().replaceWidget(self.bottom_widget, widget)
        self.bottom_widget = widget

        self.adjustSize()
        widget.show()