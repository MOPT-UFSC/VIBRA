
from PyQt5.QtCore import QSize, Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QImage, QPixmap
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from vibra import app, VIBRA_DIR, ICON_DIR
from vibra.vibra_file import VibraDecoder

import numpy as np

from functools import partial
from pathlib import Path

class WelcomeWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.main_window = app().main_window

        layout = QVBoxLayout(self)
        self.setLayout(layout)
        self.setup_image(layout)
        self.setup_labels(layout)
        self.setup_recent_projects(layout)
        self.setup_example_projects(layout)

    def setup_image(self, layout):
        image_label = QLabel(self)
        image_label.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap(str(ICON_DIR / "azul cinza.png")).scaled(350, 350, Qt.KeepAspectRatio)
        image_label.setPixmap(pixmap)
        image_label.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(image_label)

        layout.addStretch()

    def setup_labels(self, layout):
        labels_layout = QHBoxLayout()

        new_item = WelcomeItem("New", QIcon(str(ICON_DIR / "new_file.png")))
        new_item.clicked.connect(self.new_project)

        open_item = WelcomeItem("Open", QIcon(str(ICON_DIR / "import.png")))
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

        number_of_recent = 5

        for _ in range(number_of_recent):
            buttons_layout.addWidget(WelcomeItem())

    def setup_example_projects(self, layout):
        example_label = QLabel("Example Projects", self)
        example_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(example_label)

        examples_layout = QHBoxLayout()
        examples_layout.setAlignment(Qt.AlignCenter)
        layout.addLayout(examples_layout)
        layout.addStretch()

        # number of exam
        number_of_examples = 5
        example_paths = (VIBRA_DIR / "interface/data/examples/vibra_files/").glob("*.vibra")
        example_paths = list(example_paths)[:number_of_examples]

        for path in example_paths:
            with VibraDecoder(path) as file:
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

        # Complete the remaining with empty items
        for _ in range(number_of_examples - len(example_paths)):
            examples_layout.addWidget(WelcomeItem())

    def new_project(self):
        self.main_window.new_project_dialog()

    def open_project(self):
        self.main_window.open_project_dialog()

    def open_recent_project(self, path):
        self.main_window.open_project(path)

    def open_example_project(self, path):
        # self.main_window.project = Project.load(path)
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
        button.setFixedSize(QSize(90, 90))
        button.setIconSize(QSize(80, 80))

        if icon is not None:
            button.setIcon(icon)

        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(button)
        layout.addWidget(label)
        self.setLayout(layout)
