from PyQt5.QtWidgets import QWidget, QLabel, QSlider, QGridLayout
from PyQt5.QtCore import  Qt
from PyQt5.QtGui import QFont

class ClipPlaneWidget(QWidget):
    def __init__(self,parent):
        super().__init__(parent)
        self.configure_window()
        self.create_sliders()
    
    def configure_window(self):
        self.setWindowTitle("Clip Plane")
        self.setGeometry(200, 200, 400, 350)

        self.setWindowFlags(
            Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowStaysOnTopHint
            | Qt.WindowCloseButtonHint | Qt.FramelessWindowHint | Qt.WindowShadeButtonHint
        )
    
    def create_sliders(self):
        # 
        self.v_angle_title_label = QLabel("Vertical Angle")
        self.h_angle_title_label = QLabel("Horizontal Angle")
        self.position_title_label = QLabel("Percentage")

        self.v_angle_value_label = QLabel("0 °")
        self.h_angle_value_label = QLabel("0 °")
        self.position_value_label = QLabel("0 %")

        # 
        self.v_angle_slider = QSlider(Qt.Orientation.Horizontal)
        self.v_angle_slider.setMaximum(360)
        self.v_angle_slider.setMinimum(0)
        self.v_angle_slider.valueChanged.connect(self.value_change)

        self.h_angle_slider = QSlider(Qt.Orientation.Horizontal)
        self.h_angle_slider.setMaximum(360)
        self.h_angle_slider.setMinimum(0)
        self.h_angle_slider.valueChanged.connect(self.value_change)

        self.position_slider = QSlider(Qt.Orientation.Horizontal)
        self.position_slider.setMaximum(100)
        self.position_slider.setMinimum(0)
        self.position_slider.valueChanged.connect(self.value_change) 

        # 
        grid_layout = QGridLayout()
        grid_layout.addWidget(self.v_angle_title_label, 0, 0)
        grid_layout.addWidget(self.v_angle_slider, 0, 1)
        grid_layout.addWidget(self.v_angle_value_label, 0, 2)

        grid_layout.addWidget(self.h_angle_title_label, 1, 0)
        grid_layout.addWidget(self.h_angle_slider, 1, 1)
        grid_layout.addWidget(self.h_angle_value_label, 1, 2)
        
        grid_layout.addWidget(self.position_title_label, 2, 0)
        grid_layout.addWidget(self.position_slider, 2, 1)
        grid_layout.addWidget(self.position_value_label, 2, 2)

        self.setLayout(grid_layout)
        self.setGeometry(1450, 150, 450, 200)

    def value_change(self):
        self.v_angle_value_label.setText(f"{self.v_angle_slider.value()} °")
        self.h_angle_value_label.setText(f"{self.h_angle_slider.value()} °")
        self.position_value_label.setText(f"{self.position_slider.value()} %")

        # print(f"{self.angle_slider[2].value()}")

        
    
