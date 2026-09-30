import io

from matplotlib.backends.backend_qtagg import NavigationToolbar2QT
from PySide6.QtGui import QAction, QImage
from PySide6.QtWidgets import QApplication

from vibra import DARK_ICON_COLOR, LIGHT_ICON_COLOR, app
from vibra.interface.formatters.icons import Icon, change_icon_color_for_widgets


class CustomNavigationToolbar(NavigationToolbar2QT):

    def __init__(self, canvas, parent):
        super().__init__(canvas, parent)
 
        self.canvas = canvas

        self._create_connections()
        self._configure_toolbar()
        self._paint_toolbar_icons()

    def _create_connections(self):
        app().main_window.theme_changed.connect(self._paint_toolbar_icons)
    
    def _configure_toolbar(self):
        self.action_copy_graph = QAction()
        self.action_copy_graph.setToolTip("Copy Graph (Ctrl+C)")
        self.action_copy_graph.triggered.connect(self.copy_graph)
        self.action_copy_graph.setIcon(Icon(":/icons/copy_icon.png"))
        self.action_copy_graph.setShortcut("ctrl+c")

        action_save_figure = self._actions["save_figure"]
        self.insertAction(action_save_figure, self.action_copy_graph)
        self.insertAction(self.action_copy_graph, action_save_figure)
    
    def _paint_toolbar_icons(self):
        theme = app().config.user_preferences.interface_theme
        if theme == "dark":
            color = DARK_ICON_COLOR.to_qt()
        else:
            color = LIGHT_ICON_COLOR.to_qt()

        change_icon_color_for_widgets(self.actions(), color)

    def copy_graph(self):
        with io.BytesIO() as buffer:
            self.canvas.fig.savefig(buffer)
            QApplication.clipboard().setImage(QImage.fromData(buffer.getvalue()))
