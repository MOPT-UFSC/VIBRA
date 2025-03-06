from PySide6.QtWidgets import QDialog, QCheckBox, QFrame, QLineEdit, QPushButton, QSlider, QSpinBox
from PySide6.QtGui import QIcon, QFont
from PySide6.QtCore import Qt

from vibra import app, UI_DIR
from molde.colors import Color
from molde import load_ui

from vibra.interface.user_input.model.color_selector import PickColorInput

class RendererUserPreferencesInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "project/render/renderer_user_preferences.ui"
        load_ui(ui_path, self, UI_DIR)

        app().main_window.set_input_widget(self)

        self.main_window = app().main_window
        self.config = app().config
        self.user_preferences = app().config.user_preferences

        self.renderer_background_color_1 = None
        self.renderer_background_color_2 = None
        self.renderer_font_color = None
        self.nodes_points_color = None
        self.lines_color = None
        self.edges_color = None
        self.faces_color = None
        self.renderer_font_size = None

        self._config_window()
        self._define_qt_variables()
        self._create_connections()
        self.load_user_preferences()
        self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setStyleSheet("QLineEdit { border: 1px solid gray; }")
                                           

    def _define_qt_variables(self):
        # QCheckBox
        self.checkBox_reference_scale : QCheckBox

        # QFrame
        self.frame_background_color : QFrame

        # QSlider
        self.slider_transparency : QSlider

        # QLineEdit
        self.lineEdit_renderer_background_color_1 : QLineEdit
        self.lineEdit_renderer_background_color_2 : QLineEdit
        self.lineEdit_renderer_font_color : QLineEdit
        self.lineEdit_nodes_points_color : QLineEdit
        self.lineEdit_lines_color : QLineEdit
        self.lineEdit_edges_color : QLineEdit
        self.lineEdit_faces_color : QLineEdit

        # QSpinBox
        self.spinBox_renderer_font_size: QSpinBox

        # QPushButton
        self.pushButton_renderer_background_color_1 : QPushButton
        self.pushButton_renderer_background_color_2 : QPushButton
        self.pushButton_renderer_font_color : QPushButton
        self.pushButton_nodes_points_color : QPushButton
        self.pushButton_lines_color : QPushButton
        self.pushButton_edges_color : QPushButton
        self.pushButton_faces_color : QPushButton
        self.pushButton_reset_to_default : QPushButton
        self.pushButton_update_settings : QPushButton
        self.pushButton_apply_settings: QPushButton

    def _create_connections(self):
        self.pushButton_renderer_background_color_1.clicked.connect(self.update_renderer_background_color_1)
        self.pushButton_renderer_background_color_2.clicked.connect(self.update_renderer_background_color_2)
        self.pushButton_renderer_font_color.clicked.connect(self.update_renderer_font_color)
        self.pushButton_nodes_points_color.clicked.connect(self.update_nodes_points_color)
        self.pushButton_lines_color.clicked.connect(self.update_lines_color)
        self.pushButton_faces_color.clicked.connect(self.update_faces_color)
        self.pushButton_edges_color.clicked.connect(self.update_edges_color)
        self.pushButton_reset_to_default.clicked.connect(self.reset_to_default)
        self.pushButton_update_settings.clicked.connect(self.confirm_and_update_user_preferences)
        self.pushButton_apply_settings.clicked.connect(self.apply_user_preferences)
        self.spinBox_renderer_font_size.valueChanged.connect(self.update_renderer_font_size)
        
    def update_renderer_background_color_1(self):
        read = PickColorInput(title="Pick the background color")
        if read.complete:
            renderer_background_color_1 = tuple(read.color)
            str_color = str(renderer_background_color_1)[1:-1]
            self.lineEdit_renderer_background_color_1.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")

            self.renderer_background_color_1 = Color(*renderer_background_color_1)

    def update_line_edit_renderer_background_color_1(self):
        str_color = str(self.user_preferences.renderer_background_color_1.to_rgb())[1:-1]
        self.lineEdit_renderer_background_color_1.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")

    def update_renderer_background_color_2(self):
        read = PickColorInput(title="Pick the background color")
        if read.complete:
            renderer_background_color_2 = tuple(read.color)
            str_color = str(renderer_background_color_2)[1:-1]
            self.lineEdit_renderer_background_color_2.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")

            self.renderer_background_color_2 = Color(*renderer_background_color_2)

    def update_line_edit_renderer_background_color_2(self):
        str_color = str(self.user_preferences.renderer_background_color_2.to_rgb())[1:-1]
        self.lineEdit_renderer_background_color_2.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")
    
    def update_renderer_font_color(self):
        read = PickColorInput(title="Pick the font color")
        if read.complete:
            renderer_font_color = tuple(read.color)
            str_color = str(renderer_font_color)[1:-1]
            self.lineEdit_renderer_font_color.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")

            self.renderer_font_color = Color(*renderer_font_color)

    def update_line_edit_renderer_font_color(self):
        str_color = str(self.user_preferences.renderer_font_color.to_rgb())[1:-1]
        self.lineEdit_renderer_font_color.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")

    def update_nodes_points_color(self):
        read = PickColorInput(title="Pick the nodes color")
        if read.complete:
            nodes_points_color = tuple(read.color)
            str_color = str(nodes_points_color)[1:-1]
            self.lineEdit_nodes_points_color.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")

            self.nodes_points_color = Color(*nodes_points_color)
        
    def update_line_edit_nodes_points_color(self):
        str_color = str(self.user_preferences.nodes_points_color.to_rgb())[1:-1]
        self.lineEdit_nodes_points_color.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")
        
    def update_lines_color(self):
        read = PickColorInput(title="Pick the lines color")
        if read.complete:
            lines_color = tuple(read.color)
            str_color = str(lines_color)[1:-1]
            self.lineEdit_lines_color.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")

            self.lines_color = Color(*lines_color)
    
    def update_line_edit_lines_color(self):
        str_color = str(self.user_preferences.lines_color.to_rgb())[1:-1]
        self.lineEdit_lines_color.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")
    
    def update_edges_color(self):
        read = PickColorInput(title="Pick the lines color")
        if read.complete:
            edges_color = tuple(read.color)
            str_color = str(edges_color)[1:-1]
            self.lineEdit_edges_color.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")

            self.edges_color = Color(*edges_color)
    
    def update_line_edit_edges_color(self):
        str_color = str(self.user_preferences.edges_color.to_rgb())[1:-1]
        self.lineEdit_edges_color.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")

    def update_faces_color(self):
        read = PickColorInput(title="Pick the surfaces color")
        if read.complete:
            faces_color = tuple(read.color)
            str_color = str(faces_color)[1:-1]
            self.lineEdit_faces_color.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")
           
            self.faces_color = Color(*faces_color)

    def update_line_edit_faces_color(self):
        str_color = str(self.user_preferences.faces_color.to_rgb())[1:-1]
        self.lineEdit_faces_color.setStyleSheet(f"background-color: rgb({str_color});\n color: rgb({str_color});")
    
    def update_renderer_font_size(self):
        self.renderer_font_size = self.spinBox_renderer_font_size.value()
        self.user_preferences.renderer_font_size = self.renderer_font_size

    def update_spin_box_renderer_font_size(self):
        renderer_font_size = self.user_preferences.renderer_font_size
        self.spinBox_renderer_font_size.setValue(renderer_font_size)

    def apply_user_preferences(self):
        if self.renderer_background_color_1 is not None:
            self.user_preferences.renderer_background_color_1 = self.renderer_background_color_1

        if self.renderer_background_color_2 is not None:
            self.user_preferences.renderer_background_color_2 = self.renderer_background_color_2

        if self.renderer_font_color is not None:
            self.user_preferences.renderer_font_color = self.renderer_font_color
        
        if self.nodes_points_color is not None:
            self.user_preferences.nodes_points_color = self.nodes_points_color

        if self.lines_color is not None:
            self.user_preferences.lines_color = self.lines_color
        
        if self.edges_color is not None:
            self.user_preferences.edges_color = self.edges_color

        if self.faces_color is not None:
            self.user_preferences.faces_color = self.faces_color

        if self.renderer_font_size is not None:
            self.user_preferences.renderer_font_size = self.renderer_font_size

        self.update_settings()
        self.config.update_config_file()

    def confirm_and_update_user_preferences(self):
        self.apply_user_preferences()
        self.accept()
    
    def update_settings(self):
        self.update_reference_scale_state()
        self.update_renderers_font_size()
        self.main_window.update_plots()

    def reset_to_default(self):
        if self.config.user_preferences.interface_theme == "dark":
            self.user_preferences.set_dark_theme()
        else:
            self.user_preferences.set_light_theme()
        
        self.reset_attributes()
        self.user_preferences.reset_font_size()
        self.reset_reference_scale_state()
        self.load_user_preferences()

        self.update_settings()
        self.config.update_config_file()
    
    def reset_attributes(self):
        self.renderer_background_color_1 = None
        self.renderer_background_color_2 = None
        self.renderer_font_color = None
        self.nodes_points_color = None
        self.lines_color = None
        self.edges_color = None
        self.faces_color = None
        self.renderer_font_size = None

    def reset_reference_scale_state(self):
        self.user_preferences.reset_reference_scale_bar()
        self.checkBox_reference_scale.setChecked(1)
    
    def update_reference_scale_state(self):
        if self.checkBox_reference_scale.isChecked():
            self.user_preferences.show_reference_scale_bar = True
            self.main_window.update_scale_bar(True)
        else:
            self.user_preferences.show_reference_scale_bar = False
            self.main_window.update_scale_bar(False)

    def update_show_reference_scalebar_checkbox(self):
        if self.user_preferences.show_reference_scale_bar:
            self.checkBox_reference_scale.setChecked(1)
        else:
            self.checkBox_reference_scale.setChecked(0)
        
    def update_renderers_font_size(self):
        self.main_window.update_renderer_font_size()

    def load_user_preferences(self):
        self.update_line_edit_renderer_background_color_1()
        self.update_line_edit_renderer_background_color_2()
        self.update_line_edit_renderer_font_color()
        self.update_line_edit_nodes_points_color()
        self.update_line_edit_lines_color()
        self.update_line_edit_edges_color()
        self.update_line_edit_faces_color()
        self.update_spin_box_renderer_font_size()
        self.update_show_reference_scalebar_checkbox()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.confirm_and_update_user_preferences()
        elif event.key() == Qt.Key_Escape:
            self.close()