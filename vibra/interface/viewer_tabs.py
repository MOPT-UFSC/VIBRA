from PyQt5.QtCore import QCoreApplication, pyqtSignal
from PyQt5.QtWidgets import (
    QLabel,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from vibra.interface.help_widget import HelpWidget
from vibra.interface.viewer_3d.analisys_renderer import AnalisysRenderer
from vibra.interface.viewer_3d.vtk_widget import VTKWidget
from vibra.interface.viewer_3d.example_render_widget import ExampleRenderWidget
from vibra.interface.viewer_3d.model_render_widget import ModelRenderWidget
from vibra.interface.viewer_3d.common_render_widget import CommonRenderWidget


class ViewerTabs(QTabWidget):
    def __init__(self, parent, project, user_config):
        super(QWidget, self).__init__(parent)

        self.tabCloseRequested.connect(self.removeTab)
        self.configure_window()

        self.project = project
        self.user_config = user_config

        self.model_widget = ModelRenderWidget(self.project, self)
        self.modal_analisys_widget = None
        self.wellcome_widget = QLabel("Seja muito bem vindo!")
        self.help_widget = HelpWidget()

        self.model_widget.set_theme(self.user_config.theme)

        self.show_wellcome()
        self.show_example()
        self.show_model()
        self.show_analisys()

    def show_wellcome(self):
        self.addTab(self.wellcome_widget, "Wellcome!")
        self.setCurrentWidget(self.wellcome_widget)

    def show_example(self):
        example_widget = ExampleRenderWidget(self)
        example_widget.set_theme(self.user_config.theme)
        
        self.addTab(example_widget, "Example")
        self.setCurrentWidget(example_widget)

    def show_model(self):
        if self.model_widget not in self.tabs():
            self.addTab(self.model_widget, "Model")
        self.setCurrentWidget(self.model_widget)

    def show_analisys(self):
        if self.modal_analisys_widget is None:
            self.modal_analisys_widget = VTKWidget()
            self.modal_analisys_widget.set_renderer(AnalisysRenderer(self.project))
            self.modal_analisys_widget.set_theme(self.user_config.theme)
            self.modal_analisys_widget.renderer.apply_cut((50, 50, 50), (180, 180, 180))

        if self.modal_analisys_widget not in self.tabs():
            self.addTab(self.modal_analisys_widget, "Modal Analisys")
        self.setCurrentWidget(self.modal_analisys_widget)

    def show_help(self):
        self.addTab(self.help_widget, "Help")
        self.setCurrentWidget(self.help_widget)

    def update_plots(self):
        for tab in self.tabs():
            if isinstance(tab, CommonRenderWidget):
                tab.update_plot()

            if isinstance(tab, VTKWidget):
                tab.update_plot()

    def set_theme(self, theme):
        for tab in self.tabs():
            if isinstance(tab, CommonRenderWidget):
                tab.set_theme(theme)

            if isinstance(tab, VTKWidget):
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
