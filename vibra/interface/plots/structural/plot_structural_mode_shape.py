import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QLineEdit,
    QPushButton,
    QSlider,
    QTreeWidget,
    QTreeWidgetItem,
    QWidget,
)

from vibra import app
from vibra.interface.ui_generated.plots.structural.plot_structural_mode_shape_ui import PlotStructuralModeShape_UI
from vibra.interface.viewer_3d.coloring.color_palettes import COLORMAP_NAMES

window_title_1 = "Error"
window_title_2 = "Warning"


class PlotStructuralModeShape(PlotStructuralModeShape_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._initialize()
        self._create_connections()
        self._config_widgets()
        self.load_natural_frequencies()
        self.load_user_preference_colormap()

    def showEvent(self, event):
        super().showEvent(event)

        render_widget = app().main_window.results_widget
        app().main_window.render_widgets_stack.setCurrentWidget(render_widget)
        app().main_window.render_widget_changed.emit()

        app().main_window.animation_toolbar.setDisabled(False)

    def _initialize(self):
        self.mode_index = -1

    def _create_connections(self):
        #
        self.comboBox_colormaps.setDisabled(True)
        self.comboBox_color_scale.setDisabled(True)
        self.slider_transparency.setDisabled(True)

        self.comboBox_colormaps.currentIndexChanged.connect(self.update_colormap_type)
        self.comboBox_color_scale.currentIndexChanged.connect(self.update_plot)
        self.comboBox_displacements.currentIndexChanged.connect(self.update_plot)
        #
        self.pushButton_plot.clicked.connect(self.update_plot)
        #
        self.slider_transparency.valueChanged.connect(self.update_transparency_callback)
        #
        self.treeWidget_frequencies.itemClicked.connect(self.on_click_item)
        self.treeWidget_frequencies.itemDoubleClicked.connect(self.on_click_item)
        #
        self.update_animation_widget_visibility()
        self.load_user_preference_colormap()

    def _config_widgets(self):
        self.frame_button.setVisible(False)
        self.lineEdit_natural_frequency.setDisabled(True)
        self.lineEdit_natural_frequency.setProperty("status", "information")

        widths = [80, 140]
        for i, width in enumerate(widths):
            self.treeWidget_frequencies.setColumnWidth(i, width)
            self.treeWidget_frequencies.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def update_animation_widget_visibility(self):
        return
        index = self.comboBox_color_scale.currentIndex()
        if index >= 4:
            app().main_window.animation_toolbar.setDisabled(True)
        else:
            app().main_window.animation_toolbar.setDisabled(False)

    def load_user_preference_colormap(self):
        try:
            colormap = app().config.user_preferences.color_map
            if colormap in COLORMAP_NAMES:
                index = COLORMAP_NAMES.index(colormap)
                self.comboBox_colormaps.setCurrentIndex(index)
        except Exception:
            self.comboBox_colormaps.setCurrentIndex(0)

    def get_colormap(self) -> str:
        index = self.comboBox_colormaps.currentIndex()
        if not (0 <= index < len(COLORMAP_NAMES)):
            return "jet"
        return COLORMAP_NAMES[index]

    def update_colormap_type(self):
        app().config.user_preferences.color_map = self.get_colormap()
        app().config.update_config_file()
        try:
            app().main_window.results_widget.update_color_and_deformation()
        except AttributeError:
            pass

    def update_plot(self):
        self.update_animation_widget_visibility()
        if self.lineEdit_natural_frequency.text() == "":
            return

        frequency = self.selected_natural_frequency
        self.mode_index = self.natural_frequencies.index(frequency)
        app().main_window.results_widget.update_plot()

    def update_displacements(self):
        pass

    def update_transparency_callback(self):
        return
        transparency = self.slider_transparency.value() / 100
        app().main_window.results_widget.set_tube_actors_transparency(transparency)

    def get_plot_type(self):
        plot_types = [
            "u_sum",
            "u_x",
            "u_y",
            "u_z",
        ]
        index = self.comboBox_displacements.currentIndex()
        return plot_types[index]

    def get_user_color_scale_setup(self):
        return

        absolute = False
        ux_abs_values = False
        uy_abs_values = False
        uz_abs_values = False
        ux_real_values = False
        uy_real_values = False
        uz_real_values = False
        ux_imag_values = False
        uy_imag_values = False
        uz_imag_values = False
        absolute_animation = False
        ux_animation = False
        uy_animation = False
        uz_animation = False

        index = self.comboBox_color_scale.currentIndex()

        if index == 0:
            absolute_animation = True
        elif index == 1:
            ux_animation = True
        elif index == 2:
            uy_animation = True
        elif index == 3:
            uz_animation = True
        elif index == 4:
            absolute = True
        elif index == 5:
            ux_abs_values = True
        elif index == 6:
            uy_abs_values = True
        elif index == 7:
            uz_abs_values = True
        elif index == 8:
            ux_real_values = True
        elif index == 9:
            uy_real_values = True
        elif index == 10:
            uz_real_values = True
        elif index == 11:
            ux_imag_values = True
        elif index == 12:
            uy_imag_values = True
        elif index == 13:
            uz_imag_values = True

        color_scale_setup = {
            "absolute": absolute,
            "ux_abs_values": ux_abs_values,
            "uy_abs_values": uy_abs_values,
            "uz_abs_values": uz_abs_values,
            "ux_real_values": ux_real_values,
            "uy_real_values": uy_real_values,
            "uz_real_values": uz_real_values,
            "ux_imag_values": ux_imag_values,
            "uy_imag_values": uy_imag_values,
            "uz_imag_values": uz_imag_values,
            "absolute_animation": absolute_animation,
            "ux_animation": ux_animation,
            "uy_animation": uy_animation,
            "uz_animation": uz_animation,
        }

        return color_scale_setup

    def load_natural_frequencies(self):
        if app().project.structural_modal_solver is None:
            return

        self.natural_frequencies = list(app().project.structural_modal_solver.natural_frequencies)
        modes = np.arange(1, len(self.natural_frequencies) + 1, 1)
        self.modes_to_frequencies = dict(zip(modes, self.natural_frequencies))

        self.treeWidget_frequencies.clear()
        for mode, natural_frequency in self.modes_to_frequencies.items():
            new = QTreeWidgetItem([str(mode), str(round(natural_frequency, 4))])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_frequencies.addTopLevelItem(new)

        first_item = self.treeWidget_frequencies.topLevelItem(0)
        first_item.setSelected(True)
        self.treeWidget_frequencies.itemClicked.emit(first_item, 0)

    def on_click_item(self, item):
        self.selected_natural_frequency = self.modes_to_frequencies[int(item.text(0))]
        self.lineEdit_natural_frequency.setText(str(round(self.selected_natural_frequency, 4)))
        self.update_plot()

    def current_mode_index(self):
        if self.mode_index is not None:
            return self.mode_index
        return 0

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.update_plot()
        elif event.key() == Qt.Key_Escape:
            self.close()
