import logging
from pathlib import Path
from time import sleep

import qdarktheme
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap, QColor, QPainter
from PyQt5.QtWidgets import QAction, QApplication, QMainWindow, QMessageBox

from vibra.interface.help_window import HelpWindow
from vibra.interface.loading_bar import LoadingWindow, ProgressBarLogUpdater
from vibra.interface.viewer_3d.viewer_3d import Viewer3D
from vibra.project import Project


def load_icon(path, color):
    pixmap = QPixmap(str(path))
    painter = QPainter(pixmap)
    painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
    painter.fillRect(pixmap.rect(), color)
    painter.end()
    return QIcon(pixmap)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.theme = "dark"

        self.project = Project()
        self.load_icons()
        self.config()
        self.create_actions()
        self.create_basic_layout()
        self.create_menu_bar()
        self.set_theme(self.theme)

    def load_icons(self):
        color = QColor("#0055DD")

        self.vibra_icon = load_icon(Path("data/icons/logo_vibra.png"), color)
        self.help_icon = load_icon(Path("data/icons/help.png"), color)
        self.new_project_icon = load_icon(Path("data/icons/new_file.png"), color)
        self.file_import_icon = load_icon(Path("data/icons/import.png"), color)
        self.exit_import_icon = load_icon(Path("data/icons/exit.png"), color)
        self.save_icon = load_icon(Path("data/icons/save.png"), color)
        self.save_as_icon = load_icon(Path("data/icons/save_as.png"), color)
        self.view_up_icon = load_icon(Path("data/icons/top.png"), color)
        self.view_down_icon = load_icon(Path("data/icons/bottom.png"), color)
        self.view_right_icon = load_icon(Path("data/icons/right.png"), color)
        self.view_left_icon = load_icon(Path("data/icons/left.png"), color)
        self.view_back_icon = load_icon(Path("data/icons/back.png"), color)
        self.view_front_icon = load_icon(Path("data/icons/front.png"), color)
        self.view_orthogonal_icon = load_icon(Path("data/icons/orthogonal.png"), color)
        self.view_mode_line_icon = load_icon(Path("data/icons/lines.png"), color)
        self.view_mode_nodes_icon = load_icon(Path("data/icons/nodes.png"), color)
        self.view_mode_face_icon = load_icon(Path("data/icons/faces.png"), color)
        self.recent_icon = load_icon(Path("data/icons/recent.png"), color)
        self.theme_sun_icon = load_icon(Path("data/icons/sun_icon.png"), color)
        self.theme_moon_icon = load_icon(Path("data/icons/moon_icon.png"), color)

    def config(self):
        self.setMinimumSize(800, 600)
        self.showMaximized()
        self.setWindowIcon(self.vibra_icon)
        self.setWindowTitle("Vibra")

    def create_actions(self):
        self.vibra_action = QAction(self.new_project_icon, "New Project", self)
        self.file_import_action = QAction(self.file_import_icon, "Import Project", self)
        self.exit_import_action = QAction(self.exit_import_icon, "Exit", self)
        self.save_action = QAction(self.save_icon, "Save", self)
        self.save_as_action = QAction(self.save_as_icon, "Save as", self)
        self.help_action = QAction(self.help_icon, "About Vibra", self)
        self.view_up_action = QAction(self.view_up_icon, "Up View", self)
        self.view_down_action = QAction(self.view_down_icon, "Down View", self)
        self.view_left_action = QAction(self.view_left_icon, "Left View", self)
        self.view_right_action = QAction(self.view_right_icon, "Right View", self)
        self.view_front_action = QAction(self.view_front_icon, "Front View", self)
        self.view_back_action = QAction(self.view_back_icon, "Back View", self)
        self.view_orthogonal_action = QAction(self.view_orthogonal_icon, "Orthogonal View", self)
        self.view_mode_face_action = QAction(self.view_mode_face_icon, "Face View", self)
        self.view_mode_line_action = QAction(self.view_mode_line_icon, "Line View", self)
        self.view_mode_nodes_action = QAction(self.view_mode_nodes_icon, "Node View", self)
        self.recent_action = QAction(self.recent_icon, "Recent", self)
        self.theme_action = QAction(self.theme_sun_icon, "Theme", self)

        self.save_action.triggered.connect(self.save_callback)
        self.help_action.triggered.connect(self.help_callback)
        self.exit_import_action.triggered.connect(self.exit_callback)
        self.view_mode_face_action.triggered.connect(self.show_faces_callback)
        self.view_mode_line_action.triggered.connect(self.show_edges_callback)
        self.view_mode_nodes_action.triggered.connect(self.show_points_callback)
        self.view_up_action.triggered.connect(self.show_view_up_callback)
        self.view_down_action.triggered.connect(self.show_view_down_callback)
        self.view_left_action.triggered.connect(self.show_view_left_callback)
        self.view_right_action.triggered.connect(self.show_view_right_callback)
        self.view_front_action.triggered.connect(self.show_view_front_callback)
        self.view_back_action.triggered.connect(self.show_view_back_callback)
        self.view_orthogonal_action.triggered.connect(self.show_view_orthogonal_callback)
        self.theme_action.triggered.connect(self.theme_callback)

        self.help_action.setShortcut("F1")
        self.view_up_action.setShortcut("Ctrl+Shift+1")
        self.view_down_action.setShortcut("Ctrl+Shift+2")
        self.view_left_action.setShortcut("Ctrl+Shift+3")
        self.view_right_action.setShortcut("Ctrl+Shift+4")
        self.view_front_action.setShortcut("Ctrl+Shift+5")
        self.view_back_action.setShortcut("Ctrl+Shift+6")
        self.view_orthogonal_action.setShortcut("Ctrl+Shift+7")

    def create_basic_layout(self):
        self.viewer_3d = Viewer3D(self)
        self.setCentralWidget(self.viewer_3d)
        self.create_progress_bar()

    def create_progress_bar(self):
        # Creates a loading bar window
        self.loading_window = LoadingWindow(self)

        # Updates the loading bar every a log is output
        progress_handler = ProgressBarLogUpdater(progress_bar=self.loading_window.progress_bar)
        progress_handler.setLevel(logging.INFO)
        logging.getLogger().addHandler(progress_handler)

    def long_exit_function(self):
        loaded_function = self.load_function()
        loaded_function()

    def load_function(self, function, *, text=""):
        def wrapper(*args, **kwargs):
            try:
                # Changes the cursor to wait
                QApplication.setOverrideCursor(Qt.WaitCursor)

                # Shows the empty progress bar
                self.loading_window.show()
                self.loading_window.text_label.setText(text)
                sleep(0.1)  # Without sleeps pyqt breaks
                QApplication.processEvents()

                # Calls the actual function
                function(*args, **kwargs)

                # Shows the full progress bar and closes
                self.loading_window.progress_bar.setValue(100)
                sleep(0.1)  # A small delay so we can see the 100%
                self.loading_window.hide()

                # Restores the previous cursor
                QApplication.restoreOverrideCursor()

            except AttributeError:
                logging.warn("No loading window found")

        return wrapper

    def create_menu_bar(self):
        self.menu_bar = self.menuBar()
        self.project_menu = self.menu_bar.addMenu("Project")
        self.views_menu = self.menu_bar.addMenu("Views")
        self.views_mode_menu = self.menu_bar.addMenu("View Mode")
        self.help_menu = self.menu_bar.addMenu("Help")

        self.load_project_menu()
        self.load_views_menu()
        self.load_help_menu()
        self.load_views_mode_menu()

    def load_project_menu(self):
        self.project_menu.clear()
        self.project_menu.addAction(self.vibra_action)
        self.project_menu.addAction(self.file_import_action)
        self.project_menu.addAction(self.save_action)
        self.project_menu.addAction(self.save_as_action)
        self.project_menu.addAction(self.recent_action)
        self.project_menu.addAction(self.theme_action)
        self.project_menu.addAction(self.exit_import_action)

    def load_views_menu(self):
        self.views_menu.addAction(self.view_up_action)
        self.views_menu.addAction(self.view_down_action)
        self.views_menu.addAction(self.view_left_action)
        self.views_menu.addAction(self.view_right_action)
        self.views_menu.addAction(self.view_front_action)
        self.views_menu.addAction(self.view_back_action)
        self.views_menu.addAction(self.view_orthogonal_action)

    def load_views_mode_menu(self):
        self.views_mode_menu.addAction(self.view_mode_nodes_action)
        self.views_mode_menu.addAction(self.view_mode_line_action)
        self.views_mode_menu.addAction(self.view_mode_face_action)

    def load_help_menu(self):
        self.help_menu.addAction(self.help_action)

    def save_callback(self):
        self.project.save()

    def help_callback(self):
        help_window = HelpWindow()
        help_window.exec()

    def exit_callback(self):
        loaded_function = self.load_function(self.project.long_function, text="Loading...")
        loaded_function()

    def theme_callback(self):
        if self.theme == "light":
            self.set_theme("dark")
            self.theme_action.setIcon(self.theme_sun_icon)

        elif self.theme == "dark":
            self.set_theme("light")
            self.theme_action.setIcon(self.theme_moon_icon)

    def set_theme(self, theme):
        qdarktheme.setup_theme(theme)
        self.viewer_3d.set_theme(theme)
        self.theme = theme
        print(self.theme)

    def show_points_callback(self):
        self.viewer_3d.model_renderer.show_points()

    def show_edges_callback(self):
        self.viewer_3d.model_renderer.show_edges()

    def show_faces_callback(self):
        self.viewer_3d.model_renderer.show_faces()

    def show_view_up_callback(self):
        self.viewer_3d.model_renderer.set_view_up()

    def show_view_down_callback(self):
        self.viewer_3d.model_renderer.set_view_down()

    def show_view_left_callback(self):
        self.viewer_3d.model_renderer.set_view_left()

    def show_view_right_callback(self):
        self.viewer_3d.model_renderer.set_view_right()

    def show_view_front_callback(self):
        self.viewer_3d.model_renderer.set_view_front()

    def show_view_back_callback(self):
        self.viewer_3d.model_renderer.set_view_back()

    def show_view_orthogonal_callback(self):
        self.viewer_3d.model_renderer.set_view_orthogonal()

    def closeEvent(self, event):
        close = QMessageBox.question(
            self, "QUIT", "Are you sure want to stop process?", QMessageBox.Yes | QMessageBox.No
        )
        if close == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
