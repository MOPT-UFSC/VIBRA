from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QGridLayout
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize, Qt

class WelcomeWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        self.setLayout(layout)
        self.setup_image(layout)
        self.setup_labels(layout)
        self.setup_recent_projects(layout)
        self.setup_example_projects(layout)

    def setup_image(self, layout):
        image_label = QLabel(self)
        image_label.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap("data/icons/azul cinza.png").scaled(500, 500)
        image_label.setPixmap(pixmap)
        image_label.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(image_label)

        layout.setSpacing(15) 

        message_label = QLabel("Vibroacoustic Analysis using the Finite Element Method", self)
        message_label.setAlignment(Qt.AlignCenter)
        message_label.setContentsMargins(0, 0, 0, 0)
        
        layout.addWidget(message_label)

    def setup_labels(self, layout):
        labels_layout = QGridLayout()
        layout.addLayout(labels_layout)

        labels = ["New", "Open"]
        button_handlers = [self.new_project, self.open_project]

        for i, label_text in enumerate(labels):
            label = QLabel(label_text)
            labels_layout.addWidget(label, 0, i)

            button = QPushButton(self)
            button.setIcon(QIcon(""))
            button.setIconSize(QSize(100, 100))
            button.setFixedSize(70, 70)
            button.clicked.connect(button_handlers[i])
            labels_layout.addWidget(button, 1, i)

        labels_layout.setAlignment(Qt.AlignCenter)

    def setup_recent_projects(self, layout):
        recent_label = QLabel("Recent Projects", self)
        recent_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(recent_label)

        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignCenter)
        layout.addLayout(buttons_layout)

        recent_button_handlers = [self.open_recent_project1, self.open_recent_project2, self.open_recent_project3, self.open_recent_project4, self.open_recent_project5]

        for handler in recent_button_handlers:
            button = QPushButton(self)
            button.setIcon(QIcon(""))
            button.setIconSize(QSize(100, 100))
            button.setFixedSize(110, 110)
            button.clicked.connect(handler)
            buttons_layout.addWidget(button)

    def setup_example_projects(self, layout):
        example_label = QLabel("Example Projects", self)
        example_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(example_label)

        buttons_layout2 = QHBoxLayout()
        buttons_layout2.setAlignment(Qt.AlignCenter)
        layout.addLayout(buttons_layout2)

        example_button_handlers = [self.open_example_project1, self.open_example_project2, self.open_example_project3, self.open_example_project4, self.open_example_project5]

        for handler in example_button_handlers:
            button = QPushButton(self)
            button.setIcon(QIcon(""))
            button.setIconSize(QSize(100, 100))
            button.setFixedSize(110, 110)
            button.clicked.connect(handler)
            buttons_layout2.addWidget(button)

    def open_recent_project1(self):
        print("hello")

    def open_recent_project2(self):
        pass

    def open_recent_project3(self):
        pass

    def open_recent_project4(self):
        pass

    def open_recent_project5(self):
        pass

    def open_example_project1(self):
        print("hello")

    def open_example_project2(self):
        pass

    def open_example_project3(self):
        pass

    def open_example_project4(self):
        pass

    def open_example_project5(self):
        pass

    def new_project(self):
        pass

    def open_project(self):
        pass
