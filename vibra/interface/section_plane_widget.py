from PySide6.QtWidgets import QDialog, QSlider, QSpinBox, QPushButton, QWidget
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from vibra import app, UI_DIR
from molde import load_ui

class SectionPlaneWidget(QDialog):
    value_changed = Signal()
    closed = Signal()

    def __init__(self, parent):
        super().__init__(parent)

        ui_path = UI_DIR / "render/section_plane_inputs.ui"
        load_ui(ui_path, self, ui_path.parent)

        self.editing = False
        self.cutting = False
        self.invert_value = False
        self.keep_section_plane = False

        self._configure_window()
        self._define_qt_variables()
        self._create_connections()

    def _configure_window(self):
        self.setWindowFlags(
            Qt.Window
            | Qt.CustomizeWindowHint
            | Qt.WindowTitleHint
            | Qt.WindowStaysOnTopHint
            | Qt.WindowCloseButtonHint
            | Qt.FramelessWindowHint
            | Qt.WindowShadeButtonHint
            | Qt.WindowMinimizeButtonHint
        )
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowTitle("Vibra")
        self.setGeometry(200, 200, 400, 400)
    
    def show(self):
        super().show()
        self.keep_section_plane = False
        self.cutting = True
        self.value_changed.emit()

    def _define_qt_variables(self):
        # QPushButton
        self.pushButton_invert : QPushButton
        self.pushButton_reset : QPushButton
        self.pushButton_cancel : QPushButton
        self.pushButton_apply : QPushButton

        # QSlider
        self.relative_plane_position_x_slider: QSlider
        self.relative_plane_position_y_slider: QSlider
        self.relative_plane_position_z_slider: QSlider

        self.plane_rotation_x_slider: QSlider
        self.plane_rotation_y_slider: QSlider
        self.plane_rotation_z_slider: QSlider

        # QSpinBox
        self.relative_plane_position_x_spinbox: QSpinBox
        self.relative_plane_position_y_spinbox: QSpinBox
        self.relative_plane_position_z_spinbox: QSpinBox

        self.plane_rotation_x_spinbox: QSpinBox
        self.plane_rotation_y_spinbox: QSpinBox
        self.plane_rotation_z_spinbox: QSpinBox

    def _create_connections(self):
        #
        self.pushButton_invert.clicked.connect(self.invert_button_callback)
        self.pushButton_reset.clicked.connect(self.reset_button_callback)
        self.pushButton_apply.clicked.connect(self.apply_button_callback)
        self.pushButton_cancel.clicked.connect(self.close)
        #
        for slider in self._sliders():
            slider.valueChanged.connect(self.value_change_callback)
            slider.sliderReleased.connect(self.slider_release_callback)
            slider.sliderPressed.connect(self.slider_pressed_callback)

    def show(self):
        super().show()
        self.cutting = True
        self.keep_section_plane = False
        self.value_changed.emit()

    def closeEvent(self, event):
        if not self.keep_section_plane:
            app().main_window.action_section_plane.blockSignals(True)
            app().main_window.action_section_plane.setChecked(False)
            app().main_window.action_section_plane.blockSignals(False)
            self.cutting = False
        else:
            self.cutting = True
        self.value_changed.emit()
        # self.closed.emit()

    def get_position(self, get_from: str = "spinboxes"):
        if get_from == "sliders":
            Px = self.relative_plane_position_x_slider.value()
            Py = self.relative_plane_position_y_slider.value()
            Pz = self.relative_plane_position_z_slider.value()
        else:
            Px = self.relative_plane_position_x_spinbox.value()
            Py = self.relative_plane_position_y_spinbox.value()
            Pz = self.relative_plane_position_z_spinbox.value()
        return Px, Py, Pz

    def get_rotation(self, get_from: str = "spinboxes"):
        if get_from == "sliders":
            Rx = self.plane_rotation_x_slider.value()
            Ry = self.plane_rotation_y_slider.value()
            Rz = self.plane_rotation_z_slider.value()
        else:
            Rx = self.plane_rotation_x_spinbox.value()
            Ry = self.plane_rotation_y_spinbox.value()
            Rz = self.plane_rotation_z_spinbox.value()
        return Rx, Ry, Rz

    def get_inverted(self):
        return self.invert_value

    def value_change_callback(self):
        self.block_signals(self._spinboxes(), True)

        Px, Py, Pz = self.get_position("sliders")
        self.relative_plane_position_x_spinbox.setValue(Px)
        self.relative_plane_position_y_spinbox.setValue(Py)
        self.relative_plane_position_z_spinbox.setValue(Pz)

        Rx, Ry, Rz = self.get_rotation("sliders")
        self.plane_rotation_x_spinbox.setValue(Rx)
        self.plane_rotation_y_spinbox.setValue(Ry)
        self.plane_rotation_z_spinbox.setValue(Rz)

        self.block_signals(self._spinboxes(), False)
        self.editing = True
        self.value_changed.emit()

    def slider_release_callback(self):
        self.editing = False
        self.cutting = True
        self.value_changed.emit()

    def slider_pressed_callback(self):
        self.editing = True
        self.value_changed.emit()

    def reset_button_callback(self):
        self.relative_plane_position_x_slider.setValue(50),
        self.relative_plane_position_y_slider.setValue(50),
        self.relative_plane_position_z_slider.setValue(50),
        self.plane_rotation_x_slider.setValue(0),
        self.plane_rotation_y_slider.setValue(90),
        self.plane_rotation_z_slider.setValue(0),

        self.invert_value = False
        self.value_changed.emit()

    def invert_button_callback(self):
        self.invert_value = not self.invert_value
        self.value_changed.emit()

    def apply_button_callback(self):
        self.keep_section_plane = True
        self.close()

    def closeEvent(self, event):
        if not self.keep_section_plane:
            app().main_window.action_section_plane.blockSignals(True)
            app().main_window.action_section_plane.setChecked(False)
            app().main_window.action_section_plane.blockSignals(False)
            self.cutting = False
        else:
            self.cutting = True

        self.editing = False
        self.value_changed.emit()
        self.closed.emit()

        nodes_to_highlight = list(np.unique(app().project.model.mesh.nodes_to_highlight))
        faces_to_highlight = app().project.model.mesh.efaces_to_highlight
        if nodes_to_highlight or faces_to_highlight:
            import numpy as np
            app().main_window.set_mesh_selection(
                                                nodes = nodes_to_highlight,
                                                faces = faces_to_highlight
                                                )

    def block_signals(self, widgets: QWidget, option: bool):
        for widget in widgets:
            if hasattr(widget, "blockSignals"):
                widget.blockSignals(option)

    def _sliders(self):
        return (
            self.relative_plane_position_x_slider,
            self.relative_plane_position_x_slider,
            self.relative_plane_position_x_slider,
            self.relative_plane_position_y_slider,
            self.relative_plane_position_y_slider,
            self.relative_plane_position_y_slider,
            self.relative_plane_position_z_slider,
            self.relative_plane_position_z_slider,
            self.relative_plane_position_z_slider,
            self.plane_rotation_x_slider,
            self.plane_rotation_x_slider,
            self.plane_rotation_x_slider,
            self.plane_rotation_y_slider,
            self.plane_rotation_y_slider,
            self.plane_rotation_y_slider,
            self.plane_rotation_z_slider,
            self.plane_rotation_z_slider,
            self.plane_rotation_z_slider,
        )

    def _spinboxes(self):
        return (
            self.relative_plane_position_x_spinbox,
            self.relative_plane_position_y_spinbox,
            self.relative_plane_position_z_spinbox,
            self.plane_rotation_x_spinbox,
            self.plane_rotation_y_spinbox,
            self.plane_rotation_z_spinbox,
        )
