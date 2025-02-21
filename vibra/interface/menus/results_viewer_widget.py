from PyQt5.QtWidgets import QFrame, QWidget
from PyQt5.QtCore import Qt
from PyQt5 import uic

from vibra import app, UI_DIR
from vibra.interface.menus.results_viewer_items import ResultsViewerItems

class ResultsViewerWidget(QWidget):
    def __init__(self):
        super().__init__()

        ui_path = UI_DIR / "menu/left_menu_widget.ui"
        uic.loadUi(ui_path, self)

        self._reset()
        self._define_qt_variables()
        self._create_connections()

    def _reset(self):
        self.current_widget = None
    
    def hide_bottom_widget(self):
        self.bottom_widget.hide()

    def _define_qt_variables(self):

        self.main_frame = QFrame()

        # QWidget
        self.top_widget: QWidget
        self.bottom_widget: QWidget

        self.results_viewer_items = ResultsViewerItems()
        self.layout().replaceWidget(self.top_widget, self.results_viewer_items)
        self.adjustSize()
    
    def _create_connections(self):
        # Structural
        self.results_viewer_items.item_child_plot_structural_mode_shapes.clicked.connect(self.add_structural_mode_shape_widget)
        self.results_viewer_items.item_child_plot_structural_frequency_response.clicked.connect(self.add_structural_frequency_response_widget)
        self.results_viewer_items.item_child_plot_displacement_field.clicked.connect(self.add_displacement_field_widget)

        # Acoustic
        self.results_viewer_items.item_child_plot_acoustic_pressure_field.clicked.connect(self.add_acoustic_pressure_field_widget)
        self.results_viewer_items.item_child_plot_acoustic_pressure_frequency_response.clicked.connect(self.add_acoustic_pressure_frequency_response_widget)
        self.results_viewer_items.item_child_plot_acoustic_pressure_frequency_response_function.clicked.connect(self.add_acoustic_pressure_frequency_response_function_widget)
        self.results_viewer_items.item_child_plot_TL_NR.clicked.connect(self.add_TL_NR_widget)
        self.results_viewer_items.item_child_plot_acoustic_mode_shapes.clicked.connect(self.add_acoustic_mode_shape_widget)
    
    def get_item(self):
        return self.results_viewer_items

    def update_visibility_items(self):
        self.results_viewer_items._update_items()
        self.results_viewer_items.update_tree_visibility_after_solution()

    def add_structural_mode_shape_widget(self):
        self.current_widget = app().main_window.input_ui.plot_structural_mode_shapes()
        app().main_window.structural_modal_analysis.configure_menu_widget(self.current_widget)
        self.add_widget(self.current_widget, animation_widget=True)

    def add_displacement_field_widget(self):
        self.current_widget = app().main_window.input_ui.plot_displacement_field()
        app().main_window.configure_structural_harmonic_analysis_render_widget(True)
        app().main_window.structural_harmonic_analysis.configure_menu_widget(self.current_widget)

        app().main_window.animation_toolbar.setDisabled(False)

        self.add_widget(self.current_widget, animation_widget=True)

    def add_structural_frequency_response_widget(self):
        self.current_widget = app().main_window.input_ui.plot_structural_frequency_response()

        if app().main_window.structural_harmonic_analysis.playing_animation:
            app().main_window.structural_harmonic_analysis.stop_animation()
        
        app().main_window.animation_toolbar.setDisabled(True)

        self.add_widget(self.current_widget)

    def add_acoustic_pressure_field_widget(self):
        self.current_widget = app().main_window.input_ui.plot_acoustic_pressure_field()
        app().main_window.configure_acoustic_harmonic_analysis_render_widget(True)
        app().main_window.acoustic_harmonic_analysis.configure_menu_widget(self.current_widget)

        app().main_window.animation_toolbar.setDisabled(False)
        app().main_window.animation_toolbar.update_toolbar()

        self.add_widget(self.current_widget, animation_widget=True)
    
    def add_acoustic_pressure_frequency_response_widget(self):
        self.current_widget = app().main_window.input_ui.plot_acoustic_pressure_frequency_response()

        if app().main_window.acoustic_harmonic_analysis.playing_animation:
            app().main_window.acoustic_harmonic_analysis.stop_animation()
        
        app().main_window.animation_toolbar.setDisabled(True)

        self.add_widget(self.current_widget)
    
    def add_acoustic_pressure_frequency_response_function_widget(self):
        self.current_widget = app().main_window.input_ui.plot_acoustic_pressure_frequency_response_function()

        if app().main_window.acoustic_harmonic_analysis.playing_animation:
            app().main_window.acoustic_harmonic_analysis.stop_animation()

            app().main_window.animation_toolbar.setDisabled(True)

        self.add_widget(self.current_widget)
    
    def add_TL_NR_widget(self):
        self.current_widget = app().main_window.input_ui.plot_TL_NR()

        if app().main_window.acoustic_harmonic_analysis.playing_animation:
            app().main_window.acoustic_harmonic_analysis.stop_animation()
        
        app().main_window.animation_toolbar.setDisabled(True)

        self.add_widget(self.current_widget)

    def add_acoustic_mode_shape_widget(self):
        self.current_widget = app().main_window.input_ui.plot_acoustic_mode_shapes()
        app().main_window.configure_acoustic_modal_analysis_render_widget(True)
        app().main_window.acoustic_modal_analysis.configure_menu_widget(self.current_widget)
        self.add_widget(self.current_widget)

    def add_widget(self, widget: QWidget, animation_widget=False):

        # app().main_window.animation_toolbar.setEnabled(False)

        # TODO: please, remove the hide after all it shouldn't be needed
        if isinstance(self.bottom_widget, QWidget):
            self.bottom_widget.hide()

        self.layout().replaceWidget(self.bottom_widget, widget)
        self.bottom_widget = widget

        # app().main_window.animation_toolbar.setEnabled(animation_widget)
        self.adjustSize()