
from pathlib import Path

from molde import Color
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QColor, QIcon, QIconEngine, QPainter, QPixmap
from PySide6.QtWidgets import QApplication, QStyleOption, QWidget


# Bumped whenever the active icon theme changes so cached pixmaps are dropped.
_icon_generation = 0


def invalidate_themed_icons() -> None:
    """Invalidate every ``ResourceIconEngine`` cache (call on icon theme change).

    Engines lazily clear their cache the next time they are asked for a pixmap,
    so this is a cheap O(1) operation; the actual re-read happens on the next
    repaint of each icon.
    """
    global _icon_generation
    _icon_generation += 1


class ResourceIconEngine(QIconEngine):
    """Icon engine that follows the active icon theme.

    Unlike a plain ``QIcon(":/icons/...")``, which permanently caches the
    pixmap of the resource that was active when it was created, this engine
    re-reads the currently registered resource whenever the theme changes.
    The same ``QIcon`` therefore follows a ``set_icon_theme`` swap, with no
    need to track icon paths externally nor recreate icons by hand.

    Pixmaps are cached per size and only dropped when
    :func:`invalidate_themed_icons` bumps the global generation, so normal
    repaints/scrolling cost the same as a standard ``QIcon``; only a theme
    switch forces a re-decode. A repaint of the owning widget is still
    required for the new pixmap to be requested.
    """

    def __init__(self, path: str):
        super().__init__()
        self._path = path
        self._cache: dict[tuple[int, int, int], QPixmap] = {}
        self._generation = -1

    def _sync_generation(self) -> None:
        if self._generation != _icon_generation:
            self._cache.clear()
            self._generation = _icon_generation

    def _base_pixmap(self, size: QSize) -> QPixmap:
        """Read and scale the Normal-mode pixmap, caching it per size."""
        key = (size.width(), size.height(), QIcon.Mode.Normal.value)
        pixmap = self._cache.get(key)
        if pixmap is None:
            pixmap = QPixmap(self._path)
            if not pixmap.isNull() and pixmap.size() != size:
                pixmap = pixmap.scaled(
                    size,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            self._cache[key] = pixmap
        return pixmap

    def pixmap(self, size: QSize, mode, state) -> QPixmap:
        self._sync_generation()

        key = (size.width(), size.height(), mode.value)
        cached = self._cache.get(key)
        if cached is not None:
            return cached

        base = self._base_pixmap(size)
        if mode == QIcon.Mode.Normal or base.isNull():
            pixmap = base
        else:
            # Derive Disabled/Active/Selected appearance from the style, just
            # like the default QIcon engine does (e.g. greys out disabled).
            pixmap = QApplication.style().generatedIconPixmap(mode, base, QStyleOption())
            if pixmap.isNull():
                pixmap = base

        self._cache[key] = pixmap
        return pixmap

    def paint(self, painter: QPainter, rect, mode, state) -> None:
        painter.drawPixmap(rect, self.pixmap(rect.size(), mode, state))

    def clone(self) -> QIconEngine:
        return ResourceIconEngine(self._path)


def themed_icon(path: str) -> QIcon:
    """Build a theme-reactive icon from a resource path (``:/icons/...``)."""
    return QIcon(ResourceIconEngine(path))

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

