from PyQt5.QtWidgets import QLabel, QPushButton, QTabWidget, QVBoxLayout, QWidget
from PyQt5.QtCore import QCoreApplication, pyqtSignal

from molde.render_widgets import CommonRenderWidget

from vibra import app
from vibra.interface.help_widget import HelpWidget
from vibra.interface.viewer_3d.render_widgets.acoustic_harmonic_analysis_render_widget import AcousticHarmonicAnalysisRenderWidget
from vibra.interface.viewer_3d.render_widgets.acoustic_modal_analysis_render_widget import AcousticModalAnalysisRenderWidget
from vibra.interface.viewer_3d.render_widgets.example_render_widget import ExampleRenderWidget
from vibra.interface.viewer_3d.render_widgets.geometry_render_widget import GeometryRenderWidget
from vibra.interface.viewer_3d.render_widgets.mesh_render_widget import MeshRenderWidget
from vibra.interface.viewer_3d.render_widgets.structural_modal_analysis_render_widget import StructuralModalAnalysisRenderWidget
from vibra.interface.welcome_widget import WelcomeWidget


class ViewerTabs(QTabWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.main_window = app().main_window
        self.project = app().project
        self.user_config = app().user_config

        self.geometry_widget = GeometryRenderWidget()
        self.mesh_widget = MeshRenderWidget()
        self.acoustic_modal_analysis = AcousticModalAnalysisRenderWidget()
        self.structural_modal_analysis = StructuralModalAnalysisRenderWidget()
        self.acoustic_harmonic_analysis = AcousticHarmonicAnalysisRenderWidget()

        self.welcome_widget = WelcomeWidget()
        self.help_widget = HelpWidget()

        self._configure_window()

        self.add_tabs()
        self.reset_tab_visibility()
        self.show_welcome()

        self._create_connections()
        self._configure_widget()

        self.last_index = None

    def add_tabs(self):
        self.addTab(self.welcome_widget, "Welcome!")
        self.addTab(self.geometry_widget, "Geometry")
        self.addTab(self.mesh_widget, "Mesh")
        self.addTab(self.acoustic_modal_analysis, "Acoustic Modal Analysis")
        self.addTab(self.structural_modal_analysis, "Structural Modal Analysis")
        self.addTab(self.acoustic_harmonic_analysis, "Acoustic Harmonic Analysis")

    def hide_current_tab(self):
        index = self.currentIndex()
        self.setTabVisible(index, False)

    def _configure_widget(self):
        self.setTabsClosable(False)

    def _create_connections(self):
        # self.tabCloseRequested.connect(self.hide_current_tab)
        self.currentChanged.connect(self.current_tab_changed_callback)

    def reset_tab_visibility(self):
        for i in range(self.count()):
            self.setTabVisible(i, False)

    def reset_solution_tabs_visibility(self):
        for index in [3, 4, 5]:
            self.setTabVisible(index, False)

    def show_welcome(self):
        self.setTabVisible(0, True)

    def show_geometry(self):
        if not self.isTabVisible(1):
            self.setTabVisible(1, True)
            self.geometry_widget.update_plot()
        self.setCurrentIndex(1)

    def show_mesh(self):
        if not self.isTabVisible(2):
            self.setTabVisible(2, True)
            self.mesh_widget.update_plot()
        self.setCurrentIndex(2)
        nodes, face_elements, solid_elements = app().project.model.mesh.get_mesh_info()
        self.main_window.update_mesh_information(nodes, face_elements, solid_elements)

    def show_acoustic_modal_analysis(self):
        if not self.isTabVisible(3):
            self.setTabVisible(3, True)
            self.acoustic_modal_analysis.update_frequencies()
            self.acoustic_modal_analysis.update_plot()
        self.setCurrentIndex(3)

    def show_structural_modal_analysis(self):
        if not self.isTabVisible(4):
            self.setTabVisible(4, True)
            self.structural_modal_analysis.update_frequencies()
            self.structural_modal_analysis.update_plot()
        self.setCurrentIndex(4)

    def show_acoustic_harmonic_analysis(self):
        if not self.isTabVisible(5):
            self.setTabVisible(5, True)
            self.acoustic_harmonic_analysis.update_frequencies()
            self.acoustic_harmonic_analysis.update_plot()
        self.setCurrentIndex(5)

    # def show_example_analysis(self):
    #     if self.example_analysis_widget not in self.tabs():
    #         self.addTab(self.example_analysis_widget, "Example analysis")

    #     self.example_analysis_widget.update_plot()
    #     self.setCurrentWidget(self.example_analysis_widget)

    def create_a_new_tab_if_it_does_not_exist(self, widget, tab_text):
        for i in range(self.count()):
            if self.tabText(i) == tab_text:
                return
        self.addTab(widget, tab_text)

    def show_help(self):
        self.addTab(self.help_widget, "Help")
        self.setCurrentWidget(self.help_widget)

    def _create_a_new_tab_if_it_does_not_exist(self, widget, tab_text):
        for i in range(self.count()):
            if self.tabText(i) == tab_text:
                return
        self.addTab(widget, tab_text)

    def update_plots(self, reset_camera=True):
        for tab in self.tabs():
            if isinstance(tab, CommonRenderWidget):
                tab.update_plot(reset_camera)
    
    def update_hidden_plots(self):
        for tab in self.tabs():
            if not hasattr(tab, "update_hidden_plot"):
                continue
            tab.update_hidden_plot()

    def close_analysis_tabs(self):
        for i in range(self.count()):
            if i > 2:
                self.setTabVisible(i, False)

    def close_mesh_tabs(self):
        self.setTabVisible(2, False)

    def update_info_text(self):
        for tab in self.tabs():
            if not hasattr(tab, "update_info_text"):
                continue
            tab.update_info_text()

    def start_cutting_mode(self):
        for tab in self.tabs():
            if not hasattr(tab, "start_cutting_mode"):
                continue
            tab.start_cutting_mode()

    def stop_cutting_mode(self):
        for tab in self.tabs():
            if not hasattr(tab, "stop_cutting_mode"):
                continue
            tab.stop_cutting_mode()

    def configure_cutting_plane(self, position, orientation):
        for tab in self.tabs():
            if not hasattr(tab, "configure_cutting_plane"):
                continue
            tab.configure_cutting_plane(position, orientation)

    def apply_cutting_plane(self, position, orientation, invert=False):
        for tab in self.tabs():
            if not hasattr(tab, "apply_cutting_plane"):
                continue
            tab.apply_cutting_plane(position, orientation, invert)

    #
    def set_theme(self, theme):
        for tab in self.tabs():
            if isinstance(tab, CommonRenderWidget):
                tab.set_theme(theme)

    def _configure_window(self):
        self.setStyleSheet(
            """
        QTabBar::tab {
            margin-left: 5px;
            margin-right: 5px;
        }
        """
        )
        self.setTabsClosable(True)
        self.setMovable(True)
        self.setDocumentMode(True)

    def tabs(self):
        for i in range(self.count()):
            yield self.widget(i)

    def current_tab_changed_callback(self, new_index):
        if self.last_index is None:
            self.last_index = new_index
            return
        
        new_widget = self.widget(new_index)
        if isinstance(new_widget, CommonRenderWidget):
            last_widget = self.widget(self.last_index)
            new_widget.copy_camera_from(last_widget)
            # if last_widget is not a valid render the operation will be ignored

        if hasattr(new_widget, "update_selection"):
            new_widget.update_selection()

        self.last_index = new_index