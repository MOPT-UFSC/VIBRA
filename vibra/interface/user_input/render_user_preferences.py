from copy import deepcopy
from dataclasses import fields

from PySide6.QtWidgets import QDialog, QCheckBox, QFrame, QLineEdit, QPushButton, QSlider, QSpinBox
from PySide6.QtGui import QIcon, QFont
from PySide6.QtCore import Qt

from vibra import app
from vibra.interface.ui_generated.project.render.renderer_user_preferences_ui import RendererUserPreferences_UI
from molde.colors import Color

from vibra.interface.general.pick_color_input import PickColorInput


class RendererUserPreferencesInput(RendererUserPreferences_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app().main_window.set_input_widget(self)

        self.config = app().config
        self.tmp_user_preferences = deepcopy(app().config.user_preferences)

        self._config_window()
        self._create_connections()
        self.load_user_preferences()
        self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setStyleSheet("QLineEdit { border: 1px solid gray; }")

    def _create_connections(self):
        self.pushButton_renderer_background_color_1.clicked.connect(self.update_renderer_background_color_1)
        self.pushButton_renderer_background_color_2.clicked.connect(self.update_renderer_background_color_2)
        self.pushButton_renderer_font_color.clicked.connect(self.update_renderer_font_color)
        self.pushButton_nodes_points_color.clicked.connect(self.update_nodes_points_color)
        self.pushButton_lines_color.clicked.connect(self.update_lines_color)
        self.pushButton_faces_color.clicked.connect(self.update_faces_color)
        self.pushButton_selection_faces_color.clicked.connect(self.update_selection_faces_color)
        self.pushButton_selection_nodes_points_color.clicked.connect(self.update_selection_nodes_points_color)
        self.pushButton_selection_lines_color.clicked.connect(self.update_selection_lines_color)
        self.pushButton_edges_color.clicked.connect(self.update_edges_color)
        self.pushButton_reset_to_default.clicked.connect(self.reset_to_default)
        self.pushButton_update_settings.clicked.connect(self.confirm_and_update_user_preferences)
        self.pushButton_apply_settings.clicked.connect(self.apply_user_preferences)
        self.spinBox_renderer_font_size.valueChanged.connect(self.update_renderer_font_size)
        self.spinBox_points_size.valueChanged.connect(self.update_points_size)
        self.spinBox_nodes_size.valueChanged.connect(self.update_nodes_size)
        self.spinBox_lines_thickness.valueChanged.connect(self.update_lines_thickness)
        self.spinBox_edges_thickness.valueChanged.connect(self.update_edges_thickness)

    def update_renderer_background_color_1(self):
        read = PickColorInput(title="Pick the background color")
        if read.complete:
            bg_color = Color(*read.color)
            self.lineEdit_renderer_background_color_1.setStyleSheet(f"background-color: {bg_color.to_hex()};\n color: {bg_color.to_hex()};")
            self.tmp_user_preferences.renderer_background_color_1 = bg_color

    def update_line_edit_renderer_background_color_1(self):
        bg_color = self.tmp_user_preferences.renderer_background_color_1
        self.lineEdit_renderer_background_color_1.setStyleSheet(f"background-color: {bg_color.to_hex()};\n color: {bg_color.to_hex()};")

    def update_renderer_background_color_2(self):
        read = PickColorInput(title="Pick the background color")
        if read.complete:
            bg_color = Color(*read.color)
            self.lineEdit_renderer_background_color_2.setStyleSheet(f"background-color: {bg_color.to_hex()};\n color: {bg_color.to_hex()};")
            self.tmp_user_preferences.renderer_background_color_2 = bg_color


    def update_line_edit_renderer_background_color_2(self):
        bg_color = self.tmp_user_preferences.renderer_background_color_2
        self.lineEdit_renderer_background_color_2.setStyleSheet(f"background-color: {bg_color.to_hex()};\n color: {bg_color.to_hex()};")
    
    def update_renderer_font_color(self):
        read = PickColorInput(title="Pick the font color")
        if read.complete:
            font_color = Color(*read.color)
            self.lineEdit_renderer_font_color.setStyleSheet(f"background-color: {font_color.to_hex()};\n color: {font_color.to_hex()};")
            self.tmp_user_preferences.renderer_font_color = font_color


    def update_line_edit_renderer_font_color(self):
        font_color = self.tmp_user_preferences.renderer_font_color
        self.lineEdit_renderer_font_color.setStyleSheet(f"background-color: {font_color.to_hex()};\n color: {font_color.to_hex()};")

    def update_nodes_points_color(self):
        read = PickColorInput(title="Pick the nodes color")
        if read.complete:
            nodes_color = Color(*read.color)
            self.lineEdit_nodes_points_color.setStyleSheet(f"background-color: {nodes_color.to_hex()};\n color: {nodes_color.to_hex()};")

            self.tmp_user_preferences.nodes_points_color = nodes_color
        
    def update_line_edit_nodes_points_color(self):
        nodes_color = self.tmp_user_preferences.nodes_points_color
        self.lineEdit_nodes_points_color.setStyleSheet(f"background-color: {nodes_color.to_hex()};\n color: {nodes_color.to_hex()};")
        
    def update_lines_color(self):
        read = PickColorInput(title="Pick the lines color")
        if read.complete:
            lines_color = Color(*read.color)
            self.lineEdit_lines_color.setStyleSheet(f"background-color: {lines_color.to_hex()};\n color: {lines_color.to_hex()};")

            self.tmp_user_preferences.lines_color = lines_color
    
    def update_line_edit_lines_color(self):
        lines_color = self.tmp_user_preferences.lines_color
        self.lineEdit_lines_color.setStyleSheet(f"background-color: {lines_color.to_hex()};\n color: {lines_color.to_hex()};")
    
    def update_edges_color(self):
        read = PickColorInput(title="Pick the edges color")
        if read.complete:
            edges_color = Color(*read.color)
            self.lineEdit_edges_color.setStyleSheet(f"background-color: {edges_color.to_hex()};\n color: {edges_color.to_hex()};")

            self.tmp_user_preferences.edges_color = edges_color
    
    def update_line_edit_edges_color(self):
        edges_color = self.tmp_user_preferences.edges_color
        self.lineEdit_edges_color.setStyleSheet(f"background-color: {edges_color.to_hex()};\n color: {edges_color.to_hex()};")

    def update_faces_color(self):
        read = PickColorInput(title="Pick the faces color")
        if read.complete:
            faces_color = Color(*read.color)
            self.lineEdit_faces_color.setStyleSheet(f"background-color: {faces_color.to_hex()};\n color: {faces_color.to_hex()};")
           
            self.tmp_user_preferences.faces_color = faces_color

    def update_line_edit_faces_color(self):
        faces_color = self.tmp_user_preferences.faces_color
        self.lineEdit_faces_color.setStyleSheet(f"background-color: {faces_color.to_hex()};\n color: {faces_color.to_hex()};")

    def update_selection_faces_color(self):
        read = PickColorInput(title="Pick the selection faces color")
        if read.complete:
            selection_faces_color = Color(*read.color)
            self.lineEdit_selection_faces_color.setStyleSheet(f"background-color: {selection_faces_color.to_hex()};\n color: {selection_faces_color.to_hex()};")

            self.tmp_user_preferences.selection_faces_color = selection_faces_color

    def update_line_edit_selection_faces_color(self):
        selection_faces_color = self.tmp_user_preferences.selection_faces_color
        self.lineEdit_selection_faces_color.setStyleSheet(f"background-color: {selection_faces_color.to_hex()};\n color: {selection_faces_color.to_hex()};")
    
    def update_selection_nodes_points_color(self):
        read = PickColorInput(title="Pick the selection nodes/points color")
        if read.complete:
            selection_nodes_points_color = Color(*read.color)
            self.lineEdit_selection_nodes_points_color.setStyleSheet(f"background-color: {selection_nodes_points_color.to_hex()};\n color: {selection_nodes_points_color.to_hex()};")

            self.tmp_user_preferences.selection_nodes_points_color = selection_nodes_points_color

    def update_line_edit_selection_nodes_points_color(self):
        selection_nodes_points_color = self.tmp_user_preferences.selection_nodes_points_color
        self.lineEdit_selection_nodes_points_color.setStyleSheet(f"background-color: {selection_nodes_points_color.to_hex()};\n color: {selection_nodes_points_color.to_hex()};")
    
    def update_selection_lines_color(self):
        read = PickColorInput(title="Pick the selection nodes/points color")
        if read.complete:
            selection_lines_color = Color(*read.color)
            self.lineEdit_selection_lines_color.setStyleSheet(f"background-color: {selection_lines_color.to_hex()};\n color: {selection_lines_color.to_hex()};")

            self.tmp_user_preferences.selection_lines_color = selection_lines_color

    def update_line_edit_selection_lines_color(self):
        selection_lines_color = self.tmp_user_preferences.selection_lines_color
        self.lineEdit_selection_lines_color.setStyleSheet(f"background-color: {selection_lines_color.to_hex()};\n color: {selection_lines_color.to_hex()};")
    
    def update_renderer_font_size(self):
        self.tmp_user_preferences.renderer_font_size = self.spinBox_renderer_font_size.value()

    def update_spin_box_renderer_font_size(self):
        renderer_font_size = self.tmp_user_preferences.renderer_font_size
        self.spinBox_renderer_font_size.setValue(renderer_font_size)
    
    def update_points_size(self):
        self.tmp_user_preferences.points_size = self.spinBox_points_size.value()

    def update_spin_box_points_size(self):
        points_size = self.tmp_user_preferences.points_size
        self.spinBox_points_size.setValue(points_size)
    
    def update_nodes_size(self):
        self.tmp_user_preferences.nodes_size = self.spinBox_nodes_size.value()

    def update_spin_box_nodes_size(self):
        nodes_size = self.tmp_user_preferences.nodes_size
        self.spinBox_nodes_size.setValue(nodes_size)
    
    def update_lines_thickness(self):
        self.tmp_user_preferences.lines_thickness = self.spinBox_lines_thickness.value()

    def update_spin_box_lines_thickness(self):
        lines_thickness = self.tmp_user_preferences.lines_thickness
        self.spinBox_lines_thickness.setValue(lines_thickness)
    
    def update_edges_thickness(self):
        self.tmp_user_preferences.edges_thickness = self.spinBox_edges_thickness.value()

    def update_spin_box_edges_thickness(self):
        edges_thickness = self.tmp_user_preferences.edges_thickness
        self.spinBox_edges_thickness.setValue(edges_thickness)

    def apply_user_preferences(self):
        app().config.user_preferences = self.tmp_user_preferences

        app().main_window.selection.selection_changed.emit()
        self.update_settings()
        self.config.update_config_file()

    def confirm_and_update_user_preferences(self):
        self.apply_user_preferences()
        self.accept()
    
    def update_settings(self):
        self.update_reference_scale_state()
        self.update_renderers_font_size()
        self.update_compatibility_mode()
        self.update_run_analysis_in_subprocess()
        self.update_generate_mesh_in_subprocess()
        app().main_window.update_plots(reset_camera=False)

    def reset_to_default(self):
        if self.config.user_preferences.interface_theme == "dark":
            app().config.user_preferences.set_dark_theme()
        else:
            app().config.user_preferences.set_light_theme()

        app().config.user_preferences.reset_attributes()
        self.tmp_user_preferences = deepcopy(app().config.user_preferences)

        self.load_user_preferences()
        self.apply_user_preferences()

    def update_reference_scale_state(self):
        if self.checkBox_reference_scale.isChecked():
            self.tmp_user_preferences.show_reference_scale_bar = True
            app().main_window.update_scale_bar(True)
        else:
            self.tmp_user_preferences.show_reference_scale_bar = False
            app().main_window.update_scale_bar(False)

    def update_compatibility_mode(self):
        is_checked = self.checkBox_compatibility_mode.isChecked()
        self.tmp_user_preferences.compatibility_mode = is_checked

    def update_compatibility_mode_checkbox(self): 
        self.checkBox_compatibility_mode.setChecked(self.tmp_user_preferences.compatibility_mode)

    def update_run_analysis_in_subprocess(self):
        is_checked = self.checkBox_run_analysis_in_subprocess.isChecked()
        self.tmp_user_preferences.run_analysis_in_subprocess = is_checked

    def update_run_analysis_in_subprocess_checkbox(self):
        self.checkBox_run_analysis_in_subprocess.setChecked(self.tmp_user_preferences.run_analysis_in_subprocess)

    def update_generate_mesh_in_subprocess(self):
        is_checked = self.checkBox_generate_mesh_in_subprocess.isChecked()
        self.tmp_user_preferences.generate_mesh_in_subprocess = is_checked

    def update_generate_mesh_in_subprocess_checkbox(self):
        self.checkBox_generate_mesh_in_subprocess.setChecked(self.tmp_user_preferences.generate_mesh_in_subprocess)

    def update_show_reference_scalebar_checkbox(self):
        self.checkBox_reference_scale.setChecked(self.tmp_user_preferences.show_reference_scale_bar)

    def update_renderers_font_size(self):
        app().main_window.update_renderer_font_size()

    def load_user_preferences(self):
        self.update_line_edit_renderer_background_color_1()
        self.update_line_edit_renderer_background_color_2()
        self.update_line_edit_renderer_font_color()
        self.update_line_edit_nodes_points_color()
        self.update_line_edit_lines_color()
        self.update_line_edit_edges_color()
        self.update_line_edit_faces_color()
        self.update_line_edit_selection_faces_color()
        self.update_line_edit_selection_nodes_points_color()
        self.update_line_edit_selection_lines_color()
        self.update_spin_box_renderer_font_size()
        self.update_spin_box_points_size()
        self.update_spin_box_nodes_size()
        self.update_spin_box_lines_thickness()
        self.update_spin_box_edges_thickness()
        self.update_show_reference_scalebar_checkbox()
        self.update_compatibility_mode_checkbox()
        self.update_run_analysis_in_subprocess_checkbox()
        self.update_generate_mesh_in_subprocess_checkbox()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.confirm_and_update_user_preferences()
        elif event.key() == Qt.Key_Escape:
            self.close()
