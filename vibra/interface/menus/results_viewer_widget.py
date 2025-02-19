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
        self.results_viewer_items.item_child_plot_structural_mode_shapes.clicked.connect(self.add_structural_mode_shape_widget)
        self.results_viewer_items.item_child_plot_displacement_field.clicked.connect(self.add_displacement_field_widget)
        self.results_viewer_items.item_child_plot_structural_frequency_response.clicked.connect(self.add_structural_frequency_response_widget)
        self.results_viewer_items.item_child_plot_acoustic_pressure_field.clicked.connect(self.add_acoustic_pressure_field_widget)
    
    def get_item(self):
        return self.results_viewer_items

    def update_visibility_items(self):
        self.results_viewer_items._update_items()
        self.results_viewer_items.update_tree_visibility_after_solution()
    
    def update_render_by_menu_item(self):
        if hasattr(self.current_widget, "comboBox_selector_filter"):
            option = self.current_widget.comboBox_selector_filter.currentText()

            if option == " Nodes":
                app().main_window.show_mesh_render_widget()
            else:
                app().main_window.show_geometry_render_widget()

    def add_structural_mode_shape_widget(self):
        self.current_widget = app().main_window.input_ui.plot_structural_mode_shapes()
        app().main_window.structural_modal_analysis.configure_menu_widget(self.current_widget)
        self.add_widget(self.current_widget, animation_widget=True)

    def add_displacement_field_widget(self):
        self.current_widget = app().main_window.input_ui.plot_displacement_field()
        app().main_window.configure_structural_harmonic_analysis_render_widget(True)
        app().main_window.structural_harmonic_analysis.configure_menu_widget(self.current_widget)
        self.add_widget(self.current_widget, animation_widget=True)

    def add_structural_frequency_response_widget(self):
        self.current_widget = app().main_window.input_ui.plot_structural_frequency_response()
        self.add_widget(self.current_widget)

    def add_stress_field_widget(self):
        self.configure_render_according_to_plot_type("tubes")
        widget = app().main_window.input_ui.plot_stress_field()
        self.add_widget(widget, animation_widget=True)

    def add_stress_frequency_response_widget(self):
        self.configure_render_according_to_plot_type("nodes")
        widget = app().main_window.input_ui.plot_stress_frequency_response()
        self.add_widget(widget)

    def add_reaction_frequency_response_widget(self):
        self.configure_render_according_to_plot_type("nodes")
        widget = app().main_window.input_ui.plot_reaction_frequency_response()
        self.add_widget(widget)

    def add_acoustic_mode_shape_widget(self):
        self.configure_render_according_to_plot_type("tubes")
        widget = app().main_window.input_ui.plot_acoustic_mode_shapes()
        self.add_widget(widget, animation_widget=True)

    def add_acoustic_pressure_field_widget(self):
        self.current_widget = app().main_window.input_ui.plot_acoustic_pressure_field()
        app().main_window.acoustic_harmonic_analysis.configure_menu_widget(self.current_widget)
        self.add_widget(self.current_widget, animation_widget=True)

    def add_acoustic_frequency_response_widget(self):
        self.configure_render_according_to_plot_type("nodes")
        widget = app().main_window.input_ui.plot_acoustic_frequency_response()
        self.add_widget(widget)

    def add_acoustic_frequency_response_function_widget(self):
        self.configure_render_according_to_plot_type("nodes")
        widget = app().main_window.input_ui.plot_acoustic_frequency_response_function()
        self.add_widget(widget)

    def add_acoustic_delta_pressures_widget(self):
        self.configure_render_according_to_plot_type("nodes")
        widget = app().main_window.input_ui.plot_acoustic_delta_pressures()
        self.add_widget(widget)

    def add_transmission_loss_widget(self):
        self.configure_render_according_to_plot_type("nodes")
        widget = app().main_window.input_ui.plot_transmission_loss()
        self.add_widget(widget)

    def plot_perforated_plate_convergence_data(self):
        app().project.acoustic_solver.xy_plot.show()

    def add_reciprocating_compressor_pulsation_criteria_widget(self):
        self.configure_render_according_to_plot_type("nodes")
        widget = app().main_window.input_ui.reciprocating_compressor_pulsation_criteria()
        self.add_widget(widget)

    def add_reciprocating_pump_pulsation_criteria_widget(self):
        self.configure_render_according_to_plot_type("nodes")
        widget = app().main_window.input_ui.reciprocating_pump_pulsation_criteria()
        self.add_widget(widget)

    def add_reciprocating_pump_inlet_pressure_criteria_widget(self):
        self.configure_render_according_to_plot_type("nodes")
        widget = app().main_window.input_ui.reciprocating_pump_inlet_pressure_criteria()
        self.add_widget(widget)

    def add_shaking_forces_criteria_widget(self):
        self.configure_render_according_to_plot_type("lines")
        widget = app().main_window.input_ui.shaking_forces_criteria()
        self.add_widget(widget)

    def add_widget(self, widget: QWidget, animation_widget=False):

        # app().main_window.animation_toolbar.setEnabled(False)

        # TODO: please, remove the hide after all it shouldn't be needed
        if isinstance(self.bottom_widget, QWidget):
            self.bottom_widget.hide()

        self.layout().replaceWidget(self.bottom_widget, widget)
        self.bottom_widget = widget

        # app().main_window.animation_toolbar.setEnabled(animation_widget)
        self.adjustSize()

    def configure_render_according_to_plot_type(self, set_by: str):

        geometry_data = app().main_window.action_show_geometry_data.isChecked()
        mesh_data = app().main_window.action_show_mesh_data.isChecked()
        lines = app().main_window.action_plot_lines.isChecked()
        lines_with_cross_sections = app().main_window.action_plot_lines_with_cross_section.isChecked()

        if set_by == "nodes":
            if not (mesh_data or geometry_data):
                # app().main_window.plot_mesh()
                app().main_window.plot_geometry_points()

        elif set_by == "lines":
            if not (lines or lines_with_cross_sections):
                app().main_window.plot_lines_with_cross_sections()

        else:
            app().main_window.plot_results()