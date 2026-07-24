import platform
from pathlib import Path

import numpy as np
from molde.render_widgets.animated_render_widget import AnimatedRenderWidget
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QFileDialog, QLabel, QPushButton, QSpinBox

from vibra import app
from vibra.engine.analysis_info import PhysicalDomain
from vibra.interface import error_title
from vibra.interface.formatters.icons import Icon
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.loading_window import LoadingWindow
from vibra.interface.ui_generated.plots.general.animation_widget_ui import AnimationWidget_UI
from vibra.interface.viewer_3d.plot_setup import FrequencyDisplacementPlotSetup, FrequencyPressurePlotSetup, TransientPressurePlotSetup


class AnimationWidget(AnimationWidget_UI):
    def __init__(self):
        super().__init__()

        self._initialize()
        self._configure_icons()
        self._config_widgets()
        self._create_connections()
        self._configure_appearance()

        self.setWindowTitle("Animation toolbar")

    def _initialize(self):
        self.animating = False
        self.fps = 30
        self.frames_number = 1
        self.sampling_time = 1
        self.current_render_widget = None

    def _configure_icons(self):
        self.play_icon = Icon(":/icons/play.png")
        self.pause_icon = Icon(":/icons/pause.png")
        self.save_animation_icon = Icon(":/icons/create_video_icon.png")

    def _config_widgets(self):

        # QLabel
        self.label_phase_angle.setFixedWidth(72)
        self.label_factor.setFixedWidth(72)

        # QPushButton
        # self.pushButton_animate.setFixedSize(50, 30)
        self.pushButton_animate.setIcon(self.play_icon)
        self.pushButton_animate.setIconSize(QSize(20, 20))
        self.pushButton_animate.setCursor(Qt.PointingHandCursor)
        self.pushButton_animate.setToolTip("Play/Pause the animation")
        self.pushButton_animate.setCheckable(True)

        # self.pushButton_export_video.setFixedSize(50, 30)
        self.pushButton_export_video.setIcon(self.save_animation_icon)
        self.pushButton_export_video.setIconSize(QSize(20, 20))
        self.pushButton_export_video.setCursor(Qt.PointingHandCursor)
        self.pushButton_export_video.setToolTip("Save animation")

        self.pushButton_animation_loop.setCursor(Qt.PointingHandCursor)
        self.pushButton_animation_loop.setToolTip("Loop the animation")
        self.pushButton_animation_loop.setCheckable(True)

        # QSlider
        self.phase_slider.setOrientation(Qt.Orientation.Horizontal)
        self.phase_slider.setCursor(Qt.PointingHandCursor)
        self.phase_slider.setMinimum(0)
        self.phase_slider.setMaximum(360)

        self.magnification_factor_slider.setOrientation(Qt.Orientation.Horizontal)
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
        self.spinBox_cycles.setFixedSize(60, 30)
        self.spinBox_cycles.setAlignment(Qt.AlignHCenter)
        self.spinBox_cycles.setCursor(Qt.PointingHandCursor)

        self.spinBox_frames.setMinimum(20)
        self.spinBox_frames.setMaximum(60)
        self.spinBox_frames.setSingleStep(10)
        self.spinBox_frames.setValue(40)
        self.spinBox_frames.setFixedSize(60, 30)
        self.spinBox_frames.setAlignment(Qt.AlignHCenter)
        self.spinBox_frames.setCursor(Qt.PointingHandCursor)
        self.update_phase_slider_steps()

    def _create_connections(self):
        self.spinBox_frames.valueChanged.connect(self.frames_value_changed)

        self.phase_slider.sliderPressed.connect(self.pause_animation)
        self.phase_slider.valueChanged.connect(self.phase_slider_callback)
        self.magnification_factor_slider.sliderPressed.connect(self.pause_animation)
        self.magnification_factor_slider.valueChanged.connect(self.magnification_factor_slider_callback)

        self.pushButton_animate.clicked.connect(self.process_animation)
        self.pushButton_export_video.clicked.connect(self.save_animation)
        self.pushButton_animation_loop.clicked.connect(self.animation_loop_callback)

        app().main_window.render_widget_changed.connect(self.update_current_render_widget)
        app().main_window.render_widget_changed.connect(self.update_toolbar)

    def update_toolbar(self):
        current_domain = app().main_window.analysis_toolbar.combo_box_physical_domain.currentText()
        structural_domain = current_domain.lower() == PhysicalDomain.STRUCTURAL
        self.magnification_factor_slider.setEnabled(structural_domain)
        self.label_magnification_factor.setEnabled(structural_domain)
        self.label_factor.setEnabled(structural_domain)

    def update_current_render_widget(self):
        self.current_render_widget = app().main_window.render_widgets_stack.currentWidget()

    def _configure_appearance(self):

        self.stylesheet = """
            QToolBar {
                border-style: solid;
                border-width: 1px;
                border-color: #888888;
            }

            QToolBar::separator {
            width: 1px;
            }
            """

        self.setStyleSheet(self.stylesheet)

        font = QFont()
        for widget in [QLabel, QPushButton, QSpinBox]:
            for _widget in self.findChildren(widget):
                if _widget in [self.label_factor, self.label_phase_angle]:
                    font.setPointSize(8)
                else:
                    font.setPointSize(10)

                _widget.setFont(font)

    def set_visible(self, visible: bool):
        for action in self.actions():
            action.setVisible(visible)

        stylesheet = self.stylesheet if visible else "QToolBar { border: none; }"
        self.setStyleSheet(stylesheet)
        self.setMovable(visible)

    def frames_value_changed(self):
        self.frames = self.spinBox_frames.value()
        self.update_phase_slider_steps()
        app().main_window.results_widget.stop_animation()
        app().main_window.results_widget.clear_cache()

    @property
    def phase_in_radians(self):
        return np.radians(self.phase_slider.value())

    @property
    def time(self):
        value = self.phase_slider.value()
        return (self.sampling_time / self.frames_number) * value

    @property
    def time_index(self):
        return min(self.phase_slider.value(), self.frames_number - 1)

    @property
    def magnification_factor(self):
        return self.magnification_factor_slider.value() / 16

    def phase_slider_callback(self, value: int):
        self.update_degree_label()
        self.update_color_and_deformation(clear_cache=False)

    def time_frame_slider_callback(self):
        self.update_time_frame_label()
        self.update_color_and_deformation(clear_cache=False)

    def configure_animation_widget_for_transient_plot(self, sampling_time: float, frames_number: int):
        self.phase_slider.valueChanged.disconnect(self.phase_slider_callback)
        self.update_animation_parameters(sampling_time, frames_number)
        self.phase_slider.valueChanged.connect(self.time_frame_slider_callback)

        self.label_phase_angle.setText("0s")

    def update_animation_parameters(self, sampling_time: float, frames_number: int):
        self.sampling_time = sampling_time
        self.fps = max(1, frames_number // 10)
        self.frames_number = frames_number

        self.phase_slider.setMaximum(frames_number)
        self.spinBox_frames.setMaximum(frames_number)
        self.spinBox_frames.setValue(frames_number)
        self.spinBox_frames.setEnabled(False)

    def magnification_factor_slider_callback(self, value: int):
        self.update_factor_label()
        self.update_color_and_deformation()

        if hasattr(self.current_render_widget, "update_deformations"):
            self.current_render_widget.update_deformations()

    def update_color_and_deformation(self, clear_cache: bool = True):
        plot_setup = app().main_window.results_widget.plot_setup

        match plot_setup:
            case FrequencyPressurePlotSetup():
                plot_setup.phase = self.phase_in_radians
            case FrequencyDisplacementPlotSetup():
                plot_setup.phase = self.phase_in_radians
                plot_setup.magnification_factor = self.magnification_factor
            case TransientPressurePlotSetup():
                plot_setup.time_index = self.time_index
            case _:
                return

        app().main_window.results_widget.update_color_and_deformation(clear_cache=clear_cache)

    def reset_sliders(self):
        # block the slider signal to avoid multiple render updates
        self.phase_slider.blockSignals(True)

        # reset the phase slider value
        self.phase_slider.setValue(0)

        # update labels
        self.update_degree_label()

        # unblocking the slider signals
        self.phase_slider.blockSignals(False)

    def pause_animation(self):
        self.update_animate_button_icons(False)

        if not isinstance(self.current_render_widget, AnimatedRenderWidget):
            return

        if (self.current_render_widget is not None) and self.current_render_widget.playing_animation:
            self.current_render_widget.stop_animation()

    def process_animation(self, button_pressed: bool):
        self.update_animation_settings()
        self.update_animate_button_icons(button_pressed)

        if button_pressed:
            cycles = 0 if self.pushButton_animation_loop.isChecked() else self.cycles
            app().main_window.results_widget.start_animation(fps=self.fps, frames=self.frames, cycles=cycles)
            return

        app().main_window.results_widget.stop_animation()

    def update_animate_button_icons(self, button_pressed: bool):
        if button_pressed:
            self.pushButton_animate.setIcon(self.pause_icon)
        else:
            self.pushButton_animate.setIcon(self.play_icon)

    def update_animation_settings(self):
        self.frames = self.spinBox_frames.value()
        self.cycles = self.spinBox_cycles.value()

    def update_degree_label(self):
        value = self.phase_slider.value()
        self.label_phase_angle.setText(f"{value}°")

    def update_time_frame_label(self):
        self.label_phase_angle.setText(f"{self.time: .4f}s")

    def update_factor_label(self, max_value=None):
        value = self.magnification_factor_slider.value() / 16
        if isinstance(max_value, float | int):
            if max_value:
                value /= 10 * max_value
            else:
                value = 1
        self.label_factor.setText(f"{value: .2e}x")

    def update_phase_slider_steps(self):
        frames = self.spinBox_frames.value()
        single_step = int(360 / frames)
        self.phase_slider.setSingleStep(single_step)

    def save_animation(self):
        kwargs = dict()
        if platform.system() == "Linux":
            kwargs["options"] = QFileDialog.Option.DontUseNativeDialog

        file_path, extension = QFileDialog.getSaveFileName(
            self, "Save As", filter="Video (*.mp4);;WEBP (*.webp);;GIF (*.gif);; All Files ();;", **kwargs
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
                LoadingWindow(self.current_render_widget.save_animation).run(file_path)
            else:
                LoadingWindow(self.current_render_widget.save_video).run(file_path)

        except Exception as error_log:
            title = "Error while exporting animation"
            message = "An error has occured while exporting the animation file.\n"
            message += str(error_log)
            PrintMessageInput([error_title, title, message])

    def animation_loop_callback(self):
        is_clicked = self.pushButton_animation_loop.isChecked()
        self.spinBox_cycles.setDisabled(is_clicked)