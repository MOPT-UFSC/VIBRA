from PyQt5.QtWidgets import QLabel, QFileDialog, QPushButton, QSlider, QSpinBox, QToolBar, QWidget, QCheckBox
from PyQt5.QtCore import QSize, Qt 
from PyQt5.QtGui import  QIcon, QFont, QColor

from vibra import app, UI_DIR, ICON_DIR
from vibra.interface.formatters import icons
from vibra.utils.icons import load_icon
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.viewer_3d.render_widgets.acoustic_harmonic_analysis_render_widget import AcousticHarmonicAnalysisRenderWidget

from molde.render_widgets.animated_render_widget import AnimatedRenderWidget

from pathlib import Path

window_title_1 = "Error"
window_title_2 = "Warning"


class AnimationToolbar(QToolBar):
    def __init__(self):
        super().__init__()

        self._initialize()
        self._load_icons()
        self._define_qt_variables()
        self._config_widgets()
        self._create_connections()
        self._configure_layout()
        self._configure_appearance()

        self.setWindowTitle("Animation toolbar")

    def _initialize(self):
        self.animating = False

    def _load_icons(self):
        color = QColor("#448cff")

        self.play_icon = load_icon(ICON_DIR / "play.png", color)
        self.pause_icon = load_icon(ICON_DIR / "pause.png", color)
        self.export_icon = load_icon(ICON_DIR / "save_as.png", color)

    def _define_qt_variables(self):

        # QLabel
        self.label_cycles = QLabel("Animation cycles:")
        self.label_frames = QLabel("Frames per cycle:")
        self.label_phase = QLabel("Animation phase [deg]:")
        self.label_degrees = QLabel("(0°)")
        self.label_magnification_factor = QLabel("Magnification factor:")
        self.label_factor = QLabel("(1.0x)")
        self.label_show_mesh = QLabel("Show mesh")

        # QPushButton
        self.pushButton_animate = QPushButton(self)
        self.pushButton_export = QPushButton(self)

        # QSlider
        self.phase_slider = QSlider(self)
        self.magnification_factor_slider = QSlider(self)

        # QSpinBox
        self.spinBox_frames = QSpinBox(self)
        self.spinBox_cycles = QSpinBox(self)

        # QCheckBox
        self.checkBox_show_mesh = QCheckBox(self)

    def _config_widgets(self):
        # QLabel
        self.label_degrees.setFixedWidth(42)
        self.label_factor.setFixedWidth(60)

        # QPushButton
        self.pushButton_animate.setFixedSize(50, 30)
        self.pushButton_animate.setIcon(self.play_icon)
        self.pushButton_animate.setIconSize(QSize(20,20))
        self.pushButton_animate.setCursor(Qt.PointingHandCursor)
        self.pushButton_animate.setToolTip("Play/Pause the animation")
        self.pushButton_animate.setCheckable(True)

        self.pushButton_export.setFixedSize(50, 30)
        self.pushButton_export.setIcon(self.export_icon)
        self.pushButton_export.setIconSize(QSize(20,20))
        self.pushButton_export.setCursor(Qt.PointingHandCursor)
        self.pushButton_export.setToolTip("Export the animation")

        # QSlider
        self.phase_slider.setOrientation(Qt.Orientation.Horizontal)
        self.phase_slider.setMaximumWidth(150)
        self.phase_slider.setCursor(Qt.PointingHandCursor)
        self.phase_slider.setMinimum(0)
        self.phase_slider.setMaximum(360)
        
        self.magnification_factor_slider.setOrientation(Qt.Orientation.Horizontal)
        self.magnification_factor_slider.setMaximumWidth(150)
        self.magnification_factor_slider.setCursor(Qt.PointingHandCursor)
        self.magnification_factor_slider.setMinimum(0)
        self.magnification_factor_slider.setMaximum(32)
        self.magnification_factor_slider.setValue(16)
        self.magnification_factor_slider.setSingleStep(1)

        # QSpinBox
        self.spinBox_cycles.setMinimum(0)
        self.spinBox_cycles.setMaximum(10)
        self.spinBox_cycles.setSingleStep(1)
        self.spinBox_cycles.setValue(3)
        self.spinBox_cycles.setFixedSize(70, 28)
        self.spinBox_cycles.setAlignment(Qt.AlignHCenter)
        self.spinBox_cycles.setCursor(Qt.PointingHandCursor)

        self.spinBox_frames.setMinimum(20)
        self.spinBox_frames.setMaximum(60)
        self.spinBox_frames.setSingleStep(10)
        self.spinBox_frames.setValue(40)
        self.spinBox_frames.setFixedSize(70, 28)
        self.spinBox_frames.setAlignment(Qt.AlignHCenter)
        self.spinBox_frames.setCursor(Qt.PointingHandCursor)

        # QCheckBox
        self.checkBox_show_mesh.setChecked(True)

    def _create_connections(self):
        self.phase_slider.valueChanged.connect(self.phase_slider_callback)
        self.magnification_factor_slider.valueChanged.connect(self.magnification_factor_slider_callback)

        self.pushButton_animate.clicked.connect(self.process_animation)
        self.pushButton_export.clicked.connect(self.export_video)

        app().main_window.render_widget_changed.connect(self.update_toolbar)
    
    def update_toolbar(self):
        current_render_widget = app().main_window.render_widgets_stack.currentWidget()

        if isinstance(current_render_widget, AcousticHarmonicAnalysisRenderWidget):
            self.magnification_factor_slider.setDisabled(True)
            self.label_factor.setDisabled(True)
        else:
            self.magnification_factor_slider.setDisabled(False)
            self.label_factor.setDisabled(False)

    def get_spacer(self):
        spacer = QWidget()
        spacer.setFixedWidth(8)
        return spacer

    def _configure_layout(self):
        #
        self.addSeparator()
        self.addWidget(self.label_frames)
        self.addWidget(self.spinBox_frames)
        self.addWidget(self.get_spacer())
        #
        self.addWidget(self.label_cycles)
        self.addWidget(self.spinBox_cycles)
        self.addWidget(self.get_spacer())
        #
        self.addWidget(self.label_phase)
        self.addWidget(self.phase_slider)
        self.addWidget(self.label_degrees)
        self.addWidget(self.get_spacer())
        #
        self.addWidget(self.label_magnification_factor)
        self.addWidget(self.magnification_factor_slider)
        self.addWidget(self.label_factor)
        self.addWidget(self.get_spacer())
        #
        self.addWidget(self.checkBox_show_mesh)
        self.addWidget(self.label_show_mesh)
        self.addWidget(self.get_spacer())
        #
        self.addSeparator()
        self.addWidget(self.get_spacer())
        self.addWidget(self.pushButton_animate)
        self.addWidget(self.get_spacer())
        self.addWidget(self.get_spacer())
        self.addWidget(self.pushButton_export)
        #

    def _configure_appearance(self):
        self.setMinimumHeight(40)
        self.setMovable(True)
        self.setFloatable(True)
        self.setStyleSheet(
            """
            QToolBar {
                border-style: solid;
                border-width: 1px;
                border-color: #888888;
            }

            QToolBar::separator {
            width: 1px;
            }
            """
        )

        font = QFont()
        font.setPointSize(10)

        widgets = list()
        for widget in [QLabel, QPushButton, QSpinBox]:
            widgets += self.findChildren(widget)

        for widget in widgets:
            widget.setFont(font)

    def frames_value_changed(self):
        self.frames = self.spinBox_frames.value()
        self.update_phase_slider_steps()

    def cycles_value_changed(self):
        self.cycles = self.spinBox_cycles.value()
        # app().project.cycles = self.cycles
        # app().main_window.results_widget.clear_cache()

    def phase_slider_callback(self):
        self.update_degree_label()
        # self.pause_animation()      
        # value = self.phase_slider.value()
        # app().main_window.results_widget.slider_callback(value)
    
    def magnification_factor_slider_callback(self):
        self.update_factor_label()

        current_render_widget = app().main_window.render_widgets_stack.currentWidget()

        if not isinstance(current_render_widget, AnimatedRenderWidget):
            return

        if hasattr(current_render_widget, "update_deformations"):
            current_render_widget.update_deformations()

    def pause_animation(self):
        if self.pushButton_animate.isChecked(): 
            self.pushButton_animate.blockSignals(True)
            self.pushButton_animate.setChecked(False)
            self.update_animate_button_icons(False)
            app().main_window.results_widget.stop_animation()
            self.pushButton_animate.blockSignals(False)

    def process_animation(self, state: bool):
        self.update_animation_settings()
        self.update_animate_button_icons(state)

        current_render_widget = app().main_window.render_widgets_stack.currentWidget()
        current_render_widget.toggle_animation()
    
    def export_video(self):
        current_render_widget = app().main_window.render_widgets_stack.currentWidget()
        current_render_widget.save_video()

    def update_animate_button_icons(self, state: bool):
        if state:
            self.pushButton_animate.setIcon(self.pause_icon)
        else:
            self.pushButton_animate.setIcon(self.play_icon)

        theme = app().user_config.theme

        if theme == "dark":
            icon_color = QColor("#5f9af4")
        elif theme == "light":
            icon_color = QColor("#1a73e8")

        widgets = self.findChildren((QPushButton))
        icons.change_icon_color_for_widgets(widgets, icon_color)

    def update_animation_settings(self):
        self.frames = self.spinBox_frames.value()
        self.cycles = self.spinBox_cycles.value()
    
    def update_degree_label(self):
        value = self.phase_slider.value()
        self.label_degrees.setText(f"({value}°)")
    
    def update_factor_label(self):
        value = self.magnification_factor_slider.value() * 2 / 32
        self.label_factor.setText(f"({value}x)")

