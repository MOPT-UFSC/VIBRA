from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap, QCursor

from molde.interactor_styles.arcball_camera_style import ArcballCameraInteractorStyle

from vibra import app
from pathlib import Path


class RenderTool(ArcballCameraInteractorStyle):

    def __init__(self):
        super().__init__()
    
    def update_mouse_cursor_in_render_widgets(self, path: str | Path):
        custom_pixmap = QPixmap(path)

        for render in app().main_window.get_renderer_widgets():
            if custom_pixmap.isNull():
                render.setCursor(Qt.CursorShape.ArrowCursor)
            else:
                custom_pixmap = custom_pixmap.scaled(QSize(24, 24), Qt.KeepAspectRatio)
                custom_cursor = QCursor(custom_pixmap, hotX=0, hotY=0)
                render.setCursor(custom_cursor)
