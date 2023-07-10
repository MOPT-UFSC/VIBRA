from PyQt5.QtCore import QCoreApplication, pyqtSignal
from PyQt5.QtWidgets import (
    QLabel,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)
from vibra.interface.welcome_widget import WelcomeWidget
from vibra.interface.help_widget import HelpWidget
from vibra.interface.viewer_3d.common_render_widget import CommonRenderWidget
from vibra.interface.viewer_3d.example_analysis_render_widget import (
    ExampleAnalysisRenderWidget,
)
from vibra.interface.viewer_3d.example_render_widget import ExampleRenderWidget
from vibra.interface.viewer_3d.geometry_render_widget import (
    GeometryRenderWidget,
)
from vibra.interface.viewer_3d.mesh_render_widget import MeshRenderWidget
from vibra.interface.viewer_3d.acoustic_modal_analysis_render_widget import AcousticModalanalysisRenderWidget

class ViewerTabs(QTabWidget):
    def __init__(self, parent, project, user_config):
        super(QWidget, self).__init__(parent)

        self.tabCloseRequested.connect(self.removeTab)
        self.configure_window()

        self.project = project
        self.user_config = user_config

        self.geometry_widget = GeometryRenderWidget(self.project)
        self.mesh_widget = MeshRenderWidget(self.project)
        self.example_analysis_widget = ExampleAnalysisRenderWidget(self.project)
        self.welcome = WelcomeWidget()
        self.help_widget = HelpWidget()

        self.show_wellcome()
        self.show_acoustic_modal_analysis()

    def show_wellcome(self):
        self.addTab(self.welcome, "Wellcome!")
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

    def show_analysis(self):
        if self.example_analysis_widget not in self.tabs():
            self.addTab(self.example_analysis_widget, "Example analysis")
        self.setCurrentWidget(self.example_analysis_widget)

    def show_example_analysis(self):
        if self.example_analysis_widget not in self.tabs():
            self.addTab(self.example_analysis_widget, "Example analysis")
            self.example_analysis_widget.set_theme(self.user_config.theme)

        self.example_analysis_widget.update_plot()
        self.setCurrentWidget(self.example_analysis_widget)

    def show_acoustic_modal_analysis(self):
        widget = AcousticModalanalysisRenderWidget(self.project)
        if self.project.acoustic_modal_solver.natural_frequencies is None:
            return
        self.addTab(widget, "Acoustic Modal analysis")
        widget.update_plot()
        self.setCurrentWidget(widget)

    def show_help(self):
        self.addTab(self.help_widget, "Help")
        self.setCurrentWidget(self.help_widget)

    def update_plots(self):
        for tab in self.tabs():
            if isinstance(tab, CommonRenderWidget):
                tab.update_plot()

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
