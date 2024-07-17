from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QGridLayout, QLabel, QProxyStyle, QSlider, QWidget, QPushButton, QVBoxLayout, QHBoxLayout


class ClipPlaneWidget(QWidget):
    value_changed = pyqtSignal()
    slider_released = pyqtSignal()
    closed = pyqtSignal()
    slider_pressed = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self.invert_value = False

        self.configure_window()
        self.create_sliders_and_buttons()

    def configure_window(self):
        self.setWindowTitle("Section Plane")
        self.setGeometry(200, 200, 400, 400)

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

    def create_sliders_and_buttons(self):
        #
        self.x_angle_title_label = QLabel("Rx")
        self.y_angle_title_label = QLabel("Ry")
        self.z_angle_title_label = QLabel("Rz")
        self.x_pos_tittle_label = QLabel("Px")
        self.y_pos_tittle_label = QLabel("Py")
        self.z_pos_tittle_label = QLabel("Pz")
        self.position_tittle_label = QLabel("Position")
        self.rotation_tittle_label = QLabel("Rotation")
        self.position_tittle_label.setFont(QFont("Helvetica", 12, QFont.Bold))
        self.rotation_tittle_label.setFont(QFont("Helvetica", 12, QFont.Bold))

        self.v_angle_value_label = QLabel("0 °")
        self.h_angle_value_label = QLabel("0 °")
        self.position_value_label = QLabel("0 °")
        self.x_pos_tittle_value_label = QLabel("0 %")
        self.y_pos_tittle_value_label = QLabel("0 %")
        self.z_pos_tittle_value_label = QLabel("0 %")

        #
        self.y_angle_slider = QSlider(Qt.Orientation.Horizontal)
        self.y_angle_slider.setMaximum(360)
        self.y_angle_slider.setMinimum(0)
        self.y_angle_slider.valueChanged.connect(self.value_change_callback)
        self.y_angle_slider.sliderReleased.connect(self.slider_release_callback)
        self.y_angle_slider.sliderPressed.connect(self.slider_pressed_callback)

        self.x_angle_slider = QSlider(Qt.Orientation.Horizontal)
        self.x_angle_slider.setMaximum(360)
        self.x_angle_slider.setMinimum(0)
        self.x_angle_slider.valueChanged.connect(self.value_change_callback)
        self.x_angle_slider.sliderReleased.connect(self.slider_release_callback)
        self.x_angle_slider.sliderPressed.connect(self.slider_pressed_callback)

        self.z_angle_slider = QSlider(Qt.Orientation.Horizontal)
        self.z_angle_slider.setMaximum(360)
        self.z_angle_slider.setMinimum(0)
        self.z_angle_slider.valueChanged.connect(self.value_change_callback)
        self.z_angle_slider.sliderReleased.connect(self.slider_release_callback)
        self.z_angle_slider.sliderPressed.connect(self.slider_pressed_callback)

        self.x_pos_slider = QSlider(Qt.Orientation.Horizontal)
        self.x_pos_slider.setMaximum(100)
        self.x_pos_slider.setMinimum(0)
        self.x_pos_slider.setValue(50)
        self.x_pos_slider.valueChanged.connect(self.value_change_callback)
        self.x_pos_slider.sliderReleased.connect(self.slider_release_callback)
        self.x_pos_slider.sliderPressed.connect(self.slider_pressed_callback)

        self.y_pos_slider = QSlider(Qt.Orientation.Horizontal)
        self.y_pos_slider.setMaximum(100)
        self.y_pos_slider.setMinimum(0)
        self.y_pos_slider.setValue(50)
        self.y_pos_slider.valueChanged.connect(self.value_change_callback)
        self.y_pos_slider.sliderReleased.connect(self.slider_release_callback)
        self.y_pos_slider.sliderPressed.connect(self.slider_pressed_callback)

        self.z_pos_slider = QSlider(Qt.Orientation.Horizontal)
        self.z_pos_slider.setMaximum(100)
        self.z_pos_slider.setMinimum(0)
        self.z_pos_slider.setValue(50)
        self.z_pos_slider.valueChanged.connect(self.value_change_callback)
        self.z_pos_slider.sliderReleased.connect(self.slider_release_callback)
        self.z_pos_slider.sliderPressed.connect(self.slider_pressed_callback)

        self.v_angle_value_label.setFixedWidth(50)
        self.h_angle_value_label.setFixedWidth(50)
        self.position_value_label.setFixedWidth(50)
        self.x_pos_tittle_value_label.setFixedWidth(50)
        self.y_pos_tittle_value_label.setFixedWidth(50)
        self.z_pos_tittle_value_label.setFixedWidth(50)

        self.reset_button = QPushButton(text="Reset")
        self.reset_button.setFixedWidth(90)
        self.reset_button.setFixedHeight(35)
        self.reset_button.setFont(QFont("Helvetica", 8, QFont.Bold))
        self.reset_button.clicked.connect(self.reset_button_callback)

        self.invert_button = QPushButton(text="Invert")
        self.invert_button.setFixedWidth(90)
        self.invert_button.setFixedHeight(35)
        self.invert_button.setFont(QFont("Helvetica", 8, QFont.Bold))
        self.invert_button.clicked.connect(self.invert_button_callback)
        #
        grid_layout = QGridLayout()
        grid_layout.addWidget(self.rotation_tittle_label, 4, 1)
        grid_layout.addWidget(self.y_angle_title_label, 6, 0)
        grid_layout.addWidget(self.y_angle_slider, 6, 1)
        grid_layout.addWidget(self.v_angle_value_label, 6, 2)

        grid_layout.addWidget(self.x_angle_title_label, 5, 0)
        grid_layout.addWidget(self.x_angle_slider, 5, 1)
        grid_layout.addWidget(self.h_angle_value_label, 5, 2)

        grid_layout.addWidget(self.z_angle_title_label, 7, 0)
        grid_layout.addWidget(self.z_angle_slider, 7, 1)
        grid_layout.addWidget(self.position_value_label, 7, 2)

        grid_layout.addWidget(self.position_tittle_label, 0, 1)
        grid_layout.addWidget(self.x_pos_tittle_label, 1, 0)
        grid_layout.addWidget(self.x_pos_slider, 1, 1)
        grid_layout.addWidget(self.x_pos_tittle_value_label, 1, 2)

        grid_layout.addWidget(self.y_pos_tittle_label, 2, 0)
        grid_layout.addWidget(self.y_pos_slider, 2, 1)
        grid_layout.addWidget(self.y_pos_tittle_value_label, 2, 2)

        grid_layout.addWidget(self.z_pos_tittle_label, 3, 0)
        grid_layout.addWidget(self.z_pos_slider, 3, 1)
        grid_layout.addWidget(self.z_pos_tittle_value_label, 3, 2)

        grid_layout.addWidget(self.reset_button, 8, 1)
        grid_layout.addWidget(self.invert_button, 8, 2)

        grid_container_widget = QWidget()
        grid_container_widget.setLayout(grid_layout)

        hbox_layout = QHBoxLayout()
        hbox_layout.addWidget(self.reset_button)
        hbox_layout.addWidget(self.invert_button)

        hbox_container_widget = QWidget()
        hbox_container_widget.setLayout(hbox_layout)

        self.position_tittle_label.setAlignment(Qt.AlignCenter)
        self.rotation_tittle_label.setAlignment(Qt.AlignCenter)

        vbox_layout = QVBoxLayout()
        vbox_layout.addWidget(grid_container_widget)
        vbox_layout.addWidget(hbox_container_widget)

        self.setLayout(vbox_layout)
        self.setGeometry(1450, 150, 450, 200)

    def get_position(self):
        Px = self.x_pos_slider.value()
        Py = self.y_pos_slider.value()
        Pz = self.z_pos_slider.value()
        return Px, Py, Pz

    def get_rotation(self):
        Rx = self.x_angle_slider.value()
        Ry = self.y_angle_slider.value()
        Rz = self.z_angle_slider.value()
        return Rx, Ry, Rz
    
    def invert(self):
        pass

    def value_change_callback(self):
        self.setUpdatesEnabled(False)
        self.v_angle_value_label.setText(f"{self.y_angle_slider.value()} °")
        self.h_angle_value_label.setText(f"{self.x_angle_slider.value()} °")
        self.position_value_label.setText(f"{self.z_angle_slider.value()} °")
        self.x_pos_tittle_value_label.setText(f"{self.x_pos_slider.value()} %")
        self.y_pos_tittle_value_label.setText(f"{self.y_pos_slider.value()} %")
        self.z_pos_tittle_value_label.setText(f"{self.z_pos_slider.value()} %")
        self.setUpdatesEnabled(True)
        self.value_changed.emit()

    def slider_release_callback(self):
        self.slider_released.emit()

    def slider_pressed_callback(self):
        self.slider_pressed.emit()
    
    def reset_button_callback(self):
        self.x_pos_slider.setValue(0)
        self.y_pos_slider.setValue(0)
        self.z_pos_slider.setValue(0)
        self.x_angle_slider.setValue(0)
        self.y_angle_slider.setValue(0)
        self.z_angle_slider.setValue(0)
        self.invert_value = False
        self.slider_released.emit()

    def invert_button_callback(self):
        self.invert_value = not self.invert_value
        self.slider_released.emit()       

    def closeEvent(self, event):
        self.closed.emit()
