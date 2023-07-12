from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize, Qt

class WelcomeWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        image_message_layout = QVBoxLayout()

        pixmap = QPixmap("data/icons/logo_vibra.png")
        pixmap = pixmap.scaled(180, 180)
        image_label = QLabel(self)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignHCenter)
        image_label.setFixedHeight(145)
        image_message_layout.addWidget(image_label)

        message_label = QLabel("Vibra: Finite Element Software for Acoustic and Structural Analysis", self)
        message_label.setStyleSheet("font: 11pt")
        message_label.setAlignment(Qt.AlignHCenter)
        image_message_layout.addWidget(message_label)
        layout.addLayout(image_message_layout)

        labels_layout = QHBoxLayout()
        layout.addLayout(labels_layout)

        new_project_label = QLabel("New Project", self)
        labels_layout.addWidget(new_project_label)
        spacer = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        labels_layout.addItem(spacer)
        open_project_label = QLabel("Open Project", self)
        labels_layout.addWidget(open_project_label)

        labels_layout.setAlignment(Qt.AlignLeft)

        buttons_layout2 = QHBoxLayout()
        layout.addLayout(buttons_layout2)
        buttons_layout2.setAlignment(Qt.AlignLeft)

        new_button = QPushButton(self)
        new_button.setIcon(QIcon(""))
        new_button.setIconSize(QSize(100, 100))
        new_button.setFixedSize(80, 80)
        new_button.clicked.connect(self.new_project)
        buttons_layout2.addWidget(new_button)

        open_button = QPushButton(self)
        open_button.setIcon(QIcon(""))
        open_button.setIconSize(QSize(100, 100))
        open_button.setFixedSize(80, 80)
        open_button.clicked.connect(self.new_project)
        buttons_layout2.addWidget(open_button)


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
