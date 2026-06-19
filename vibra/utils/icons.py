from pathlib import Path

from PySide6.QtGui import  QIcon, QPixmap


def load_icon(path: Path | str):
    pixmap = QPixmap(str(path))
    return QIcon(pixmap)
