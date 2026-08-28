from PySide6.QtWidgets import QWidget


def clear_style_sheet(widgets: QWidget | list[QWidget]):
    if isinstance(widgets, QWidget):
        widgets = [widgets]

    for widget in widgets:
        widget.setStyleSheet("")
        widget.style().unpolish(widget)
        widget.style().polish(widget)