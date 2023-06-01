from PyQt5.QtCore import QCoreApplication, pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QTabWidget, QPushButton, QVBoxLayout

from vibra.interface.viewer_3d.viewer_3d import Viewer3D
from vibra.interface.viewer_3d.vtk_widget import VTKWidget
from vibra.interface.viewer_3d.example_renderer import ExampleRenderer
from vibra.interface.viewer_3d.model_renderer import ModelRenderer
from vibra.interface.help_widget import HelpWidget


class ViewerTabs(QTabWidget):
    def __init__(self, parent, project, user_config):
        super(QWidget, self).__init__(parent)

        self.tabCloseRequested.connect(self.removeTab)
        self.configure_window()

        self.project = project
        self.user_config = user_config

        self.model_widget = None
        self.wellcome_widget = QLabel("Seja muito bem vindo!")
        self.help_widget = HelpWidget()

        self.show_wellcome()
        self.show_model()

    def show_wellcome(self):
        self.addTab(self.wellcome_widget, "Wellcome!")
        self.setCurrentWidget(self.wellcome_widget)

    def show_model(self):
        if self.model_widget is None:
            self.model_widget = VTKWidget()
            self.model_widget.set_renderer(ModelRenderer(self.project))
            self.model_widget.set_theme(self.user_config.theme)

        if self.model_widget not in self.tabs():
            self.addTab(self.model_widget, "Model")
        self.setCurrentWidget(self.model_widget)

    def show_example(self):
        example_widget = VTKWidget()
        example_widget.set_renderer(ExampleRenderer())
        example_widget.set_theme(self.user_config.theme)
        self.addTab(example_widget, "Example")
        self.setCurrentWidget(example_widget)

    def show_help(self):
        self.addTab(self.help_widget, "Help")
        self.setCurrentWidget(self.help_widget)

    def update_plots(self):
        for tab in self.tabs():
            if isinstance(tab, VTKWidget):
                tab.update_plot()

    def set_theme(self, theme):
        for tab in self.tabs():
            if isinstance(tab, VTKWidget):
                tab.set_theme(theme)

    def configure_window(self):
        self.setStyleSheet(
            """
        QTabBar::tab {
            margin-left: 10px;
            margin-right: 10px;
        }
        """
        )
        self.setTabsClosable(True)
        self.setMovable(True)
        self.setDocumentMode(True)

    def tabs(self):
        for i in range(self.count()):
            yield self.widget(i)
