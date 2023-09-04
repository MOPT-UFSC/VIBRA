from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtCore import QSize, Qt, pyqtSignal
from pathlib import Path
from functools import partial
import numpy as np
from vibra.file.vibra_file import VibraFile
from vibra.utils.interface_functions import get_main_window
from vibra.project import Project


class WelcomeWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.main_window = get_main_window()
        layout = QVBoxLayout(self)
        self.setLayout(layout)
        self.setup_image(layout)
        self.setup_labels(layout)
        self.setup_recent_projects(layout)
        self.setup_example_projects(layout)

    def setup_image(self, layout):
        image_label = QLabel(self)
        image_label.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap("data/icons/azul cinza.png").scaled(400, 400, Qt.KeepAspectRatio)
        image_label.setPixmap(pixmap)
        image_label.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(image_label)


        message_label = QLabel(
            "         Finite Element Software for Acoustic and Structural Analysis", self
        )
        message_label.setAlignment(Qt.AlignCenter)
        message_label.setContentsMargins(0, 0, 0, 0)

        # layout.setSpacing(15)
        layout.addWidget(message_label)
        layout.addStretch()

    def setup_labels(self, layout):
        labels_layout = QHBoxLayout()

        new_item = WelcomeItem("New", QIcon("data/icons/new_file.png"))
        new_item.clicked.connect(self.new_project)
        
        open_item = WelcomeItem("Open", QIcon("data/icons/import.png"))
        open_item.clicked.connect(self.open_project)

        labels_layout.addWidget(new_item)
        labels_layout.addWidget(open_item)
        labels_layout.setAlignment(Qt.AlignCenter)

        layout.addLayout(labels_layout)    
        layout.addStretch()

    def setup_recent_projects(self, layout):
        recent_label = QLabel("Recent Projects", self)
        recent_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(recent_label)

        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignCenter)
        layout.addLayout(buttons_layout)
        layout.addStretch()

        # recent_button_handlers = [self.open_recent_project1, self.open_recent_project2, self.open_recent_project3, self.open_recent_project4, self.open_recent_project5]

        # for handler in recent_button_handlers:
        for i in range(5):
            button = QPushButton(self)
            button.setIcon(QIcon(""))
            button.setIconSize(QSize(100, 100))
            button.setFixedSize(110, 110)
            # button.clicked.connect(handler)
            buttons_layout.addWidget(button)
        

    def setup_example_projects(self, layout):
        example_label = QLabel("Example Projects", self)
        example_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(example_label)

        examples_layout = QHBoxLayout()
        examples_layout.setAlignment(Qt.AlignCenter)
        layout.addLayout(examples_layout)
        layout.addStretch()

        examples_path = Path("data/examples/vibra_files/")

        for path in examples_path.glob("*.vibra"):
            with VibraFile(path) as file:
                thumbnail = file.get_thumbnail()

            if thumbnail is not None:
                array = np.array(thumbnail)
                image = QImage(array, array.shape[1], array.shape[0], QImage.Format_RGB888)
                icon = QIcon(QPixmap(image))
            else:
                icon = None

            name = path.name

            handler = partial(self.open_example_project, path)
            item = WelcomeItem(name, icon)
            item.clicked.connect(handler)
            examples_layout.addWidget(item)

    def new_project(self):
        self.main_window.import_geometry()

    def open_project(self):
        self.main_window.open_project()

    def open_recent_project(self, path):
        self.main_window.open_project(path)

    def open_example_project(self, path):
        self.main_window.project = Project.load(path)
        self.main_window.viewer_tabs.close_mesh_tabs()
        self.main_window.viewer_tabs.show_geometry()
        self.main_window.viewer_tabs.show_mesh()
        self.main_window.viewer_tabs.update_plots()


class WelcomeItem(QWidget):
    clicked = pyqtSignal()
    
    def __init__(self, text="", icon=None):
        super().__init__()

        button = QPushButton(self)
        button.clicked.connect(self.clicked.emit)
        button.setFixedSize(QSize(100, 100))
        button.setIconSize(QSize(90, 90))

        if icon is not None:
            button.setIcon(icon)

        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(button)
        layout.addWidget(label)
        self.setLayout(layout)
