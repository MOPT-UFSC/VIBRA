from PyQt5.QtCore import QCoreApplication, pyqtSignal
from PyQt5.QtWidgets import (
    QLabel,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from vibra.interface.help_widget import HelpWidget
from vibra.interface.viewer_3d.render_widgets.acoustic_harmonic_analysis_render_widget import (
    AcousticHarmonicAnalysisRenderWidget,
)
from vibra.interface.viewer_3d.render_widgets.acoustic_modal_analysis_render_widget import (
    AcousticModalAnalysisRenderWidget,
)
from vibra.interface.viewer_3d.render_widgets.common_render_widget import (
    CommonRenderWidget,
)
from vibra.interface.viewer_3d.render_widgets.example_render_widget import (
    ExampleRenderWidget,
)
from vibra.interface.viewer_3d.render_widgets.geometry_render_widget import (
    GeometryRenderWidget,
)
from vibra.interface.viewer_3d.render_widgets.mesh_render_widget import (
    MeshRenderWidget,
)
from vibra.interface.viewer_3d.render_widgets.structural_modal_analysis_render_widget import (
    StructuralModalAnalysisRenderWidget,
)
from vibra.interface.welcome_widget import WelcomeWidget
from vibra.utils.interface_functions import get_main_window


class ViewerTabs(QTabWidget):
    def __init__(self, parent, project, user_config):
        super(QWidget, self).__init__(parent)

        self.tabCloseRequested.connect(self.removeTab)
        self.configure_window()

        self.main_window = get_main_window()
        self.user_config = user_config

        self.geometry_widget = GeometryRenderWidget()
        self.mesh_widget = MeshRenderWidget()
        self.acoustic_modal_analysis = AcousticModalAnalysisRenderWidget()
        self.structural_modal_analysis = StructuralModalAnalysisRenderWidget()
        self.acoustic_harmonic_analysis = AcousticHarmonicAnalysisRenderWidget()

        self.welcome = WelcomeWidget()
        self.help_widget = HelpWidget()

        self.show_welcome()

    #
    def show_welcome(self):
        self.addTab(self.welcome, "Welcome!")
        self.setCurrentWidget(self.welcome)

    def show_example(self):
        example_widget = ExampleRenderWidget(self)
        example_widget.set_theme(self.user_config.theme)

        self.addTab(example_widget, "Example")
        self.setCurrentWidget(example_widget)

    def show_geometry(self):
        if self.geometry_widget not in self.tabs():
            self.addTab(self.geometry_widget, "Geometry")
        self.geometry_widget.update_plot()
        self.setCurrentWidget(self.geometry_widget)

    def show_mesh(self):
        if self.mesh_widget not in self.tabs():
            self.addTab(self.mesh_widget, "Mesh")
        self.mesh_widget.update_plot()
        self.setCurrentWidget(self.mesh_widget)

    def show_example_analysis(self):
        if self.example_analysis_widget not in self.tabs():
            self.addTab(self.example_analysis_widget, "Example analysis")

        self.example_analysis_widget.update_plot()
        self.setCurrentWidget(self.example_analysis_widget)

    def show_acoustic_modal_analysis(self):
        if self.acoustic_modal_analysis not in self.tabs():
            self.addTab(self.acoustic_modal_analysis, "Acoustic Modal Analysis")

        self.acoustic_modal_analysis.update_frequencies()
        self.acoustic_modal_analysis.update_plot()
        self.setCurrentWidget(self.acoustic_modal_analysis)

    def show_structural_modal_analysis(self):
        if self.structural_modal_analysis not in self.tabs():
            self.addTab(self.structural_modal_analysis, "Acoustic Modal Analysis")

        self.structural_modal_analysis.update_frequencies()
        self.structural_modal_analysis.update_plot()
        self.setCurrentWidget(self.structural_modal_analysis)

    def show_acoustic_harmonic_analysis(self):
        if self.acoustic_harmonic_analysis not in self.tabs():
            self.addTab(self.structural_modal_analysis, "Acoustic Modal Analysis")

        self.acoustic_harmonic_analysis.update_plot()
        self.setCurrentWidget(self.acoustic_harmonic_analysis)

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

    def update_plots(self):
        for tab in self.tabs():
            if isinstance(tab, CommonRenderWidget):
                tab.update_plot()

    def close_analysis_tabs(self):
        self._close_widgets(
            self.acoustic_modal_analysis,
            self.structural_modal_analysis,
        )

    def close_mesh_tabs(self):
        self._close_widgets(
            self.mesh_widget,
            self.geometry_widget,
            self.acoustic_modal_analysis,
            self.structural_modal_analysis,
        )

    def _close_widgets(self, *widgets_list):
        for widget in widgets_list:
            i = self.indexOf(widget)
            self.removeTab(i)

    #
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

    def apply_cutting_plane(self, position, orientation):
        for tab in self.tabs():
            if not hasattr(tab, "apply_cutting_plane"):
                continue
            tab.apply_cutting_plane(position, orientation)

    #
    def set_theme(self, theme):
        for tab in self.tabs():
            if isinstance(tab, CommonRenderWidget):
                tab.set_theme(theme)

    def configure_window(self):
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
