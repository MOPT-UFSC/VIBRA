from PyQt5.QtCore import QCoreApplication, pyqtSignal
from PyQt5.QtWidgets import (
    QLabel,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from vibra.interface.help_widget import HelpWidget
from vibra.interface.viewer_3d.common_render_widget import CommonRenderWidget
from vibra.interface.viewer_3d.example_analisys_render_widget import (
    ExampleAnalisysRenderWidget,
)
from vibra.interface.viewer_3d.example_render_widget import ExampleRenderWidget
from vibra.interface.viewer_3d.model_render_widget import ModelRenderWidget


class ViewerTabs(QTabWidget):
    def __init__(self, parent, project, user_config):
        super(QWidget, self).__init__(parent)

        self.tabCloseRequested.connect(self.removeTab)
        self.configure_window()

        self.project = project
        self.user_config = user_config

        self.model_widget = ModelRenderWidget(self.project, self)
        self.example_analisys_widget = ExampleAnalisysRenderWidget(self.project, self)
        self.welcome = QLabel("Seja muito bem vindo!")
        self.help_widget = HelpWidget()

        self.model_widget.set_theme(self.user_config.theme)

        self.show_wellcome()
        self.show_model()
        self.show_analisys()
        self.show_example()

    def show_wellcome(self):
        self.addTab(self.welcome, "Wellcome!")
        self.setCurrentWidget(self.welcome)

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
        if self.example_analisys_widget not in self.tabs():
            self.addTab(self.example_analisys_widget, "Example Analisys")
        self.setCurrentWidget(self.example_analisys_widget)

    def show_example_analisys(self):
        if self.example_analisys_widget not in self.tabs():
            self.addTab(self.example_analisys_widget, "Example Analisys")

        self.example_analisys_widget.update_plot()
        self.setCurrentWidget(self.example_analisys_widget)

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
