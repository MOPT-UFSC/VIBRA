from PyQt5.QtWidgets import QDialog, QSlider, QSpinBox, QPushButton, QWidget
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5 import uic

from vibra import app, UI_DIR

class SectionPlaneWidget(QDialog):
    value_changed = pyqtSignal()
    closed = pyqtSignal()

    # Remove
    slider_released = pyqtSignal()
    slider_pressed = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)

        self.editing = False
        self.cutting = True
        self.invert_value = False

        ui_path = UI_DIR / "render/section_plane_control_widget.ui"
        uic.loadUi(ui_path, self)

        self.configure_window()
        self._define_qt_variables()
        self._create_connections()
        self.reset_button_callback()

    def configure_window(self):
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

        self.setGeometry(200, 200, 400, 400)
        self.setWindowIcon(app().main_window.vibra_icon)
    
    def show(self):
        super().show()
        self.value_changed.emit()

    def _define_qt_variables(self):
        # QPushButton
        self.pushButton_invert : QPushButton
        self.pushButton_reset : QPushButton

        # QSlider
        self.relative_plane_position_x_slider : QSlider
        self.relative_plane_position_y_slider : QSlider
        self.relative_plane_position_z_slider : QSlider

        self.plane_rotation_x_slider : QSlider
        self.plane_rotation_y_slider : QSlider
        self.plane_rotation_z_slider : QSlider

        # QSpinBox
        self.relative_plane_position_x_spinbox : QSpinBox
        self.relative_plane_position_y_spinbox : QSpinBox
        self.relative_plane_position_z_spinbox : QSpinBox

        self.plane_rotation_x_spinbox : QSpinBox
        self.plane_rotation_y_spinbox : QSpinBox
        self.plane_rotation_z_spinbox : QSpinBox

    def _create_connections(self):
        #
        self.pushButton_invert.clicked.connect(self.invert_button_callback)
        self.pushButton_reset.clicked.connect(self.reset_button_callback)
        #
        for slider in self._sliders():
            slider.valueChanged.connect(self.value_change_callback)
            slider.sliderReleased.connect(self.slider_release_callback)
            slider.sliderPressed.connect(self.slider_pressed_callback)

        for spinbox in self._spinboxes():
            spinbox.valueChanged.connect(self.spinbox_value_change_callback)

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
        self.value_changed.emit()

    def spinbox_value_change_callback(self):
        self.block_signals(self._sliders(), True)

        Px, Py, Pz = self.get_position("spinboxes")
        self.relative_plane_position_x_slider.setValue(Px)
        self.relative_plane_position_y_slider.setValue(Py)
        self.relative_plane_position_z_slider.setValue(Pz)

        Rx, Ry, Rz = self.get_rotation("spinboxes")
        self.plane_rotation_x_slider.setValue(Rx)
        self.plane_rotation_y_slider.setValue(Ry)
        self.plane_rotation_z_slider.setValue(Rz)

        self.block_signals(self._sliders(), False)
        self.value_changed.emit()

        self.editing = False
        self.cutting = True

    def slider_release_callback(self):
        self.editing = False
        self.cutting = True
        self.value_changed.emit()
        self.slider_released.emit()

    def slider_pressed_callback(self):
        self.editing = True
        self.value_changed.emit()
        self.slider_pressed.emit()

    def reset_button_callback(self):
        self.relative_plane_position_x_slider.setValue(50)
        self.relative_plane_position_y_slider.setValue(50)
        self.relative_plane_position_z_slider.setValue(50)
        self.plane_rotation_x_slider.setValue(0)
        self.plane_rotation_y_slider.setValue(90)
        self.plane_rotation_z_slider.setValue(0)
        self.invert_value = False
        # self.value_changed.emit()
        # self.slider_released.emit()

    def invert_button_callback(self):
        self.invert_value = not self.invert_value
        self.slider_released.emit()
        self.value_changed.emit()

    def closeEvent(self, event):
        self.editing = False
        self.value_changed.emit()
        self.closed.emit()
    
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
