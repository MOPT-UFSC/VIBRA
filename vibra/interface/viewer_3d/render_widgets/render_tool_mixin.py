from PySide6.QtCore import QSize
from PySide6.QtGui import QPixmap, Qt, QCursor

from vibra.interface.viewer_3d.render_tools import RenderTool


class RenderToolMixin:
    def setRenderTool(self, renderTool: RenderTool):
        self.set_interactor_style(renderTool)
        custom_pixmap = QPixmap(renderTool.cursor_path)

        if custom_pixmap.isNull():
            self.setCursor(Qt.CursorShape.ArrowCursor)
        else:
            custom_pixmap = custom_pixmap.scaled(QSize(24, 24), Qt.KeepAspectRatio)
            custom_cursor = QCursor(custom_pixmap, hotX=0, hotY=0)
            self.setCursor(custom_cursor)
