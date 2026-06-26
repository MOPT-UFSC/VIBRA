
from pathlib import Path

from molde import Color
from PySide6.QtCore import QSize
from PySide6.QtGui import QColor, QIcon, QPainter, QPixmap
from PySide6.QtWidgets import QWidget


def get_icons_path(path):
    path = Path(path)
    if path.exists():
        return str(path)

def get_formatted_icon(path: Path | str, color: QColor):
    pixmap = QPixmap(str(path))
    painter = QPainter(pixmap)
    painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
    painter.fillRect(pixmap.rect(), color)
    painter.end()
    return QIcon(pixmap)

def get_vibra_icon(color=None):
    icon_path = ":/icons/logos/logo_vibra.png"

    if color is None:
        return QIcon(icon_path)
    
    return get_formatted_icon(icon_path, color)

def get_warning_icon(color=None):
    if color is None:
        return QIcon(":/icons/warnings/warning_2.png")
   
    icon_path = ":/icons/warnings/transparent_warning.png"
    return get_formatted_icon(icon_path, color)

def get_error_icon(color=Color(255,0,0,200).to_qt()):
    icon_path = ":/icons/warnings/transparent_warning.png"
    return get_formatted_icon(icon_path, color)

def change_icon_color(icon: QIcon, color: QColor):
    if icon is None:
        return 

    size = icon.actualSize(QSize(10_000, 10_000))
    invalid_sizes = [-1, 0, 10_000]

    if size.width() in invalid_sizes:
        return
    
    if size.height() in invalid_sizes:
        return

    pixmap: QPixmap = icon.pixmap(size)
    paint_pixmap(pixmap, color)
    icon.addPixmap(pixmap)

def paint_pixmap(pixmap: QPixmap, color: QColor):
    painter = QPainter(pixmap)
    if not painter.isActive():
        return

    painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
    painter.fillRect(pixmap.rect(), color)
    painter.end()

def change_icon_color_for_widgets(widgets: list[QWidget], color: QColor):
    for widget in widgets:
        if not hasattr(widget, "icon") or not callable(widget.icon):
            continue

        if not hasattr(widget, "setIcon") or not callable(widget.setIcon):
            continue

        if hasattr(widget, "should_paint") and not widget.should_paint:
            continue

        icon = widget.icon()
        if icon is None or icon.isNull():
            continue

        size = icon.actualSize(QSize(10_000, 10_000))
        invalid_sizes = [-1, 0, 10_000]
        if size.width() in invalid_sizes or size.height() in invalid_sizes:
            continue

        pixmap = icon.pixmap(size)
        paint_pixmap(pixmap, color)
        widget.setIcon(QIcon(pixmap))
