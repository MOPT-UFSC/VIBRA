from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSpacerItem, QSizePolicy, QGridLayout
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize, Qt

class WelcomeWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        image_message_layout = QGridLayout()

        pixmap = QPixmap("data/icons/logo_vibra.png")
        pixmap = pixmap.scaled(180, 180)
        image_label = QLabel(self)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignHCenter)
        layout.addWidget(image_label)

        message_label = QLabel("OpenPulse: Open Source Software for Pulsation Analysis of Pipeline Systems", self)
        message_label.setAlignment(Qt.AlignHCenter)
        image_message_layout.addWidget(message_label)
        layout.addLayout(image_message_layout)

        labels_layout = QGridLayout()
        layout.addLayout(labels_layout)

        new_project_label = QLabel("New")
        labels_layout.addWidget(new_project_label, 0, 0)

        open_project_label = QLabel("Open")
        labels_layout.addWidget(open_project_label, 0, 1)
        labels_layout.setAlignment(Qt.AlignLeft)

        new_button = QPushButton(self)
        new_button.setIcon(QIcon(""))
        new_button.setIconSize(QSize(100, 100))
        new_button.setFixedSize(70, 70)
        new_button.clicked.connect(self.new_project)
        labels_layout.addWidget(new_button, 1, 0)

        open_button = QPushButton(self)
        open_button.setIcon(QIcon(""))
        open_button.setIconSize(QSize(100, 100))
        open_button.setFixedSize(70, 70)
        open_button.clicked.connect(self.new_project)
        labels_layout.addWidget(open_button, 1, 1)


        recent_label = QLabel("Recent Projects", self)
        recent_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(recent_label)

        buttons_layout = QHBoxLayout()
        layout.addLayout(buttons_layout)

        recent_button1 = QPushButton(self)
        recent_button1.setIcon(QIcon(""))
        recent_button1.setIconSize(QSize(100, 100))
        recent_button1.setFixedSize(110, 110)
        recent_button1.clicked.connect(self.open_project1)
        buttons_layout.addWidget(recent_button1)
        
        recent_button2 = QPushButton(self)
        recent_button2.setIcon(QIcon(""))
        recent_button2.setIconSize(QSize(100, 100))
        recent_button2.setFixedSize(110, 110)
        recent_button2.clicked.connect(self.open_project2)
        buttons_layout.addWidget(recent_button2)

        recent_button3 = QPushButton(self)
        recent_button3.setIcon(QIcon(""))
        recent_button3.setIconSize(QSize(100, 100))
        recent_button3.setFixedSize(110, 110)
        recent_button3.clicked.connect(self.open_project3)
        buttons_layout.addWidget(recent_button3)

        recent_button4 = QPushButton(self)
        recent_button4.setIcon(QIcon(""))
        recent_button4.setIconSize(QSize(100, 100))
        recent_button4.setFixedSize(110, 110)
        recent_button4.clicked.connect(self.open_project3)
        buttons_layout.addWidget(recent_button4)

        recent_button5 = QPushButton(self)
        recent_button5.setIcon(QIcon(""))
        recent_button5.setIconSize(QSize(100, 100))
        recent_button5.setFixedSize(110, 110)
        recent_button5.clicked.connect(self.open_project3)
        buttons_layout.addWidget(recent_button5)


        example_label = QLabel("Example Projects", self)
        example_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(example_label)

        buttons_layout2 = QHBoxLayout()
        layout.addLayout(buttons_layout2)

        example_button1 = QPushButton(self)
        example_button1.setIcon(QIcon(""))
        example_button1.setIconSize(QSize(100, 100))
        example_button1.setFixedSize(110, 110)
        example_button1.clicked.connect(self.open_project1)
        buttons_layout2.addWidget(example_button1)
        
        example_button2 = QPushButton(self)
        example_button2.setIcon(QIcon(""))
        example_button2.setIconSize(QSize(100, 100))
        example_button2.setFixedSize(110, 110)
        example_button2.clicked.connect(self.open_project2)
        buttons_layout2.addWidget(example_button2)

        example_button3 = QPushButton(self)
        example_button3.setIcon(QIcon(""))
        example_button3.setIconSize(QSize(100, 100))
        example_button3.setFixedSize(110, 110)
        example_button3.clicked.connect(self.open_project3)
        buttons_layout2.addWidget(example_button3)

        example_button4 = QPushButton(self)
        example_button4.setIcon(QIcon(""))
        example_button4.setIconSize(QSize(100, 100))
        example_button4.setFixedSize(110, 110)
        example_button4.clicked.connect(self.open_project3)
        buttons_layout2.addWidget(example_button4)

        example_button5 = QPushButton(self)
        example_button5.setIcon(QIcon(""))
        example_button5.setIconSize(QSize(100, 100))
        example_button5.setFixedSize(110, 110)
        example_button5.clicked.connect(self.open_project3)
        buttons_layout2.addWidget(example_button5)

        spacer_horizontal = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        buttons_layout.addItem(spacer_horizontal)
        buttons_layout2.addItem(spacer_horizontal)

        spacer_vertical = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer_vertical)

    def open_project1(self):
        print("hello")
        pass

    def open_project2(self):
        pass

    def open_project3(self):
        pass

    def new_project(self):
        pass

    def open_project(self):
        pass
