"""
View Toolbar Component for OCP Widget
A reusable toolbar providing view controls for 3D CAD visualization
"""

from typing import Union

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QGroupBox,
    QFrame,
    QSlider,
    QLabel,
)
from PySide6.QtCore import Signal, Qt

from cad_widgets.enums import DisplayMode


class CADViewToolbar(QWidget):
    """
    Toolbar component for controlling 3D view settings.

    Signals:
        display_mode_changed(str): Emitted when display mode changes (shaded/wireframe)
        transparency_changed(float): Emitted when global transparency changes (0.0-1.0)
    """

    # Define signals
    display_mode_changed = Signal(str)
    transparency_changed = Signal(float)

    def __init__(self, parent=None, orientation="horizontal"):
        """
        Initialize the view toolbar.

        Args:
            parent: Parent widget
            orientation: 'horizontal' or 'vertical' layout
        """
        super().__init__(parent)
        self._orientation = orientation
        self._setup_ui()

    def _setup_ui(self):
        """Setup the user interface."""
        # Main layout
        main_layout: Union[QVBoxLayout, QHBoxLayout]
        if self._orientation == "vertical":
            main_layout = QVBoxLayout(self)
        else:
            main_layout = QHBoxLayout(self)

        main_layout.setContentsMargins(5, 5, 5, 5)

        # Display mode group
        display_mode_group = self._create_display_mode_group()
        main_layout.addWidget(display_mode_group)

        # Transparency group
        transparency_group = self._create_transparency_group()
        main_layout.addWidget(transparency_group)

        # Separator
        separator = QFrame()
        if self._orientation == "vertical":
            separator.setFrameShape(QFrame.Shape.HLine)
        else:
            separator.setFrameShape(QFrame.Shape.VLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(separator)

        # Add stretch at the end
        main_layout.addStretch()

    def _create_display_mode_group(self):
        """Create the display mode control group."""
        group = QGroupBox("Display Mode")
        layout = QVBoxLayout(group)
        layout.setSpacing(5)

        # Create combo box
        self._display_mode_combo = QComboBox()
        self._display_mode_combo.addItem(
            DisplayMode.WIREFRAME.value.capitalize(), DisplayMode.WIREFRAME.value
        )
        self._display_mode_combo.addItem(
            DisplayMode.SHADED.value.capitalize(), DisplayMode.SHADED.value
        )
        self._display_mode_combo.addItem(
            "Shaded + Wireframe", DisplayMode.BOTH.value
        )
        self._display_mode_combo.setCurrentIndex(1)
        self._display_mode_combo.currentIndexChanged.connect(
            self._on_display_mode_combo_changed
        )

        layout.addWidget(self._display_mode_combo)

        return group

    def _create_transparency_group(self):
        """Create the transparency control group."""
        group = QGroupBox("Transparency")
        layout = QVBoxLayout(group)
        layout.setSpacing(5)

        # Create label
        self._transparency_label = QLabel("0%")
        self._transparency_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._transparency_label)

        # Create slider
        self._transparency_slider = QSlider(Qt.Orientation.Horizontal)
        self._transparency_slider.setMinimum(0)
        self._transparency_slider.setMaximum(100)
        self._transparency_slider.setValue(0)
        self._transparency_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self._transparency_slider.setTickInterval(10)
        self._transparency_slider.valueChanged.connect(self._on_transparency_changed)
        layout.addWidget(self._transparency_slider)

        return group

    def _on_display_mode_combo_changed(self, index: int):
        """Handle display mode combo box change."""
        mode_value = self._display_mode_combo.itemData(index)
        self.display_mode_changed.emit(mode_value)

    def _on_transparency_changed(self, value: int):
        """Handle transparency slider change."""
        transparency = value / 100.0
        self._transparency_label.setText(f"{value}%")
        self.transparency_changed.emit(transparency)

    def set_display_mode(self, mode: DisplayMode):
        """
        Programmatically set the display mode.

        Args:
            mode: DisplayMode enum
        """
        for i in range(self._display_mode_combo.count()):
            if self._display_mode_combo.itemData(i) == mode.value:
                self._display_mode_combo.setCurrentIndex(i)
                break

    def get_display_mode(self):
        """Get the current display mode."""
        return self._display_mode_combo.currentData()

    def set_transparency(self, transparency: float):
        """
        Programmatically set the transparency.

        Args:
            transparency: Float 0-1 for transparency
        """
        value = int(transparency * 100)
        self._transparency_slider.setValue(value)

    def get_transparency(self) -> float:
        """Get the current transparency as a float 0-1."""
        return self._transparency_slider.value() / 100.0
