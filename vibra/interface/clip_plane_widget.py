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
        self.angle_label = [QLabel() for _ in range(3)]

        self.text1 = QLabel("Vertical Angle")
        self.text1.setFont(QFont("Decorative", 12))
        self.text2 = QLabel("Horizontal Angle")
        self.text2.setFont(QFont("Decorative", 12))
        self.text3 = QLabel("Percentage")
        self.text3.setFont(QFont("Decorative", 12))

        for label in self.angle_label:
            label.setFont(QFont("Decorative", 12))

        self.angle_label[0].setText("0 °")
        self.angle_label[1].setText("0 °")
        self.angle_label[2].setText("0 %")

        self.angle_slider = [QSlider(Qt.Orientation.Horizontal) for x in range(3)]

        self.angle_slider[0].setMaximum(360)
        self.angle_slider[0].setMinimum(0)
        self.angle_slider[0].valueChanged.connect(self.value_change)

        self.angle_slider[1].setMaximum(360)
        self.angle_slider[1].setMinimum(0)
        self.angle_slider[1].valueChanged.connect(self.value_change)

        self.angle_slider[2].setMaximum(100)
        self.angle_slider[2].setMinimum(0)
        self.angle_slider[2].valueChanged.connect(self.value_change)

        grid_layout = QGridLayout()
        grid_layout.addWidget(self.text1, 0, 0)
        grid_layout.addWidget(self.angle_slider[0], 0, 1)
        grid_layout.addWidget(self.angle_label[0], 0, 2)
        grid_layout.addWidget(self.text2, 1, 0)
        grid_layout.addWidget(self.angle_slider[1], 1, 1)
        grid_layout.addWidget(self.angle_label[1], 1, 2)
        grid_layout.addWidget(self.text3, 2, 0)
        grid_layout.addWidget(self.angle_slider[2], 2, 1)
        grid_layout.addWidget(self.angle_label[2], 2, 2)

        self.setLayout(grid_layout)
        self.setGeometry(1450, 150, 450, 200)

    def value_change(self):
        self.angle_label[0].setText(f"{self.angle_slider[0].value()} °")
        self.angle_label[1].setText(f"{self.angle_slider[1].value()} °")
        self.angle_label[2].setText(f"{self.angle_slider[2].value()} %")

        print(f"{self.angle_slider[2].value()}")

        
    
