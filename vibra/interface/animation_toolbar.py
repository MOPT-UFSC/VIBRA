from PySide6.QtWidgets import QLabel, QFileDialog, QPushButton, QSlider, QSpinBox, QToolBar, QWidget
from PySide6.QtGui import  QIcon, QFont, QColor
from PySide6.QtCore import Qt, QSize

from vibra import app, UI_DIR, ICON_DIR
from vibra.interface.formatters import icons
from vibra.utils.icons import load_icon
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.loading_bar import load_function

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
        self.current_render_widget = None

    def _load_icons(self):
        color = QColor("#448cff")

        self.play_icon = load_icon(ICON_DIR / "play.png", color)
        self.pause_icon = load_icon(ICON_DIR / "pause.png", color)
        self.save_animation_icon = load_icon(ICON_DIR / "create_video_icon.png", color)

    def _define_qt_variables(self):

        # QLabel
        self.label_cycles = QLabel("Animation cycles:")
        self.label_frames = QLabel("Frames per cycle:")
        self.label_phase = QLabel("Animation phase [deg]:")
        self.label_degrees = QLabel("(0°)")
        self.label_magnification_factor = QLabel("Magnification factor:")
        self.label_factor = QLabel("(1.0x)")

        # QPushButton
        self.pushButton_animate = QPushButton(self)
        self.pushButton_save_animation = QPushButton(self)

        # QSlider
        self.phase_slider = QSlider(self)
        self.magnification_factor_slider = QSlider(self)

        # QSpinBox
        self.spinBox_frames = QSpinBox(self)
        self.spinBox_cycles = QSpinBox(self)

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

        self.pushButton_save_animation.setFixedSize(50, 30)
        self.pushButton_save_animation.setIcon(self.save_animation_icon)
        self.pushButton_save_animation.setIconSize(QSize(20,20))
        self.pushButton_save_animation.setCursor(Qt.PointingHandCursor)
        self.pushButton_save_animation.setToolTip("Save animation")

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

    def _create_connections(self):
        self.spinBox_frames.valueChanged.connect(self.frames_value_changed)

        self.phase_slider.sliderPressed.connect(self.pause_animation)
        self.phase_slider.valueChanged.connect(self.phase_slider_callback)
        self.magnification_factor_slider.valueChanged.connect(self.magnification_factor_slider_callback)

        self.pushButton_animate.clicked.connect(self.process_animation)
        self.pushButton_save_animation.clicked.connect(self.save_animation)

        app().main_window.render_widget_changed.connect(self.update_current_render_widget)
        app().main_window.render_widget_changed.connect(self.update_toolbar)

        self.update_phase_slider_steps()
    
    def update_toolbar(self):
        if app().main_window.analysis_toolbar.combo_box_analysis_domain.currentIndex() == 1:
            self.magnification_factor_slider.setDisabled(True)
            self.label_magnification_factor.setDisabled(True)
            self.label_factor.setDisabled(True)
        else:
            self.magnification_factor_slider.setDisabled(False)
            self.label_magnification_factor.setDisabled(False)
            self.label_factor.setDisabled(False)
        
    def update_current_render_widget(self):
        self.current_render_widget = app().main_window.render_widgets_stack.currentWidget()

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
        self.addSeparator()
        self.addWidget(self.get_spacer())
        self.addWidget(self.pushButton_animate)
        self.addWidget(self.get_spacer())
        self.addWidget(self.get_spacer())
        self.addWidget(self.pushButton_save_animation)
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

    def phase_slider_callback(self, value: int):
        self.update_degree_label()
        app().main_window.results_widget.update_color_and_deformation(clear_cache=False)
    
    def magnification_factor_slider_callback(self, value: int):
        self.update_factor_label()
        app().main_window.results_widget.update_color_and_deformation()

        if hasattr(self.current_render_widget, "update_deformations"):
            self.current_render_widget.update_deformations()

    def pause_animation(self):
        self.update_animate_button_icons(False)

        if not isinstance(self.current_render_widget, AnimatedRenderWidget):
            return

        if self.current_render_widget is not None and self.current_render_widget.playing_animation:
            self.current_render_widget.stop_animation()

    def process_animation(self, state: bool):
        self.update_animation_settings()
        self.update_animate_button_icons(state)

        self.current_render_widget.toggle_animation(frames=self.frames, cycles=self.cycles)

    def update_animate_button_icons(self, state: bool):
        if state:
            self.pushButton_animate.setIcon(self.pause_icon)
        else:
            self.pushButton_animate.setIcon(self.play_icon)

        theme = app().config.user_preferences.interface_theme

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
    
    def update_phase_slider_steps(self):
        frames = self.spinBox_frames.value()
        single_step = int(360 / frames)
        self.phase_slider.setSingleStep(single_step)

    def save_animation(self):
        file_path, extension = QFileDialog.getSaveFileName(
            self, "Save As",
            filter = "Video (*.mp4);;WEBP (*.webp);;GIF (*.gif);; All Files ();;",
        )

        if not extension:
            return

        # Add default suffix if it does not have one
        file_path = Path(file_path)
        if extension == "Video (*.mp4)":
            suffix = ".mp4"
        elif extension == "WEBP (*.webp)":
            suffix = ".webp"
        elif extension == "GIF (*.gif)":
            suffix = ".gif"
        else:
            suffix = ".mp4"

        if not file_path.suffix:
            file_path = file_path.parent / (file_path.name + suffix)

        try:

            if file_path.suffix.lower() in [".gif", ".webp"]:
                save_animation = load_function(self.current_render_widget.save_animation, app().main_window)
                save_animation(file_path)
            else:
                save_video = load_function(self.current_render_widget.save_video, app().main_window)
                save_video(file_path)

        except Exception as error_log:
            title = "Error while exporting animation"
            message = "An error has occured while exporting the animation file.\n"
            message += str(error_log)
            PrintMessageInput([window_title_1, title, message])
