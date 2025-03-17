from PySide6.QtWidgets import QComboBox, QFrame, QLineEdit, QPushButton, QSlider, QTreeWidget, QTreeWidgetItem, QWidget
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, Signal

from vibra import app, UI_DIR

from molde import load_ui

import numpy as np


class PlotDisplacementField(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "plots/structural/plot_displacement_field.ui"
        load_ui(ui_path, self, ui_path.parent)

        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self.load_frequencies()
        self.load_user_preference_colormap()
    
    def showEvent(self, event):
        super().showEvent(event)

        render_widget = app().main_window.results_widget
        app().main_window.render_widgets_stack.setCurrentWidget(render_widget)
        app().main_window.render_widget_changed.emit()

        app().main_window.animation_toolbar.setDisabled(False)

    def _initialize(self):
        self.frequency_index = None

        self.colormaps = ["jet",
                          "viridis",
                          "inferno",
                          "magma",
                          "plasma",
                          "bwr",
                          "PiYG",
                          "PRGn",
                          "BrBG",
                          "PuOR",
                          "grayscale",
                          ]

    def _define_qt_variables(self):

        # QComboBox
        self.comboBox_color_scale : QComboBox
        self.comboBox_colormaps : QComboBox
        self.comboBox_displacements: QComboBox

        # QFrame
        self.frame_button : QFrame
        self.frame_button.setVisible(False)

        # QLineEdit
        self.lineEdit_selected_frequency : QLineEdit
        self.lineEdit_selected_frequency.setProperty("status", "information")

        # QPushButton
        self.pushButton_plot : QPushButton

        # QSlider
        self.slider_transparency : QSlider

        # QTreeWidget
        self.treeWidget_frequencies : QTreeWidget
        self._config_treeWidget()

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
        self.treeWidget_frequencies.itemDoubleClicked.connect(self.on_doubleclick_item)
        #
        self.update_animation_widget_visibility()
        self.load_user_preference_colormap()
        self.update_colormap_type()

    def update_animation_widget_visibility(self):
        return
        index = self.comboBox_color_scale.currentIndex()
        if index >= 4:
            app().main_window.animation_toolbar.setDisabled(True)
        else:
            app().main_window.animation_toolbar.setDisabled(False) 

    def load_user_preference_colormap(self):
        return
        try:
            colormap = app().config.user_preferences.color_map
            if colormap in self.colormaps:
                index = self.colormaps.index(colormap)
                self.comboBox_colormaps.setCurrentIndex(index)
        except:
            self.comboBox_colormaps.setCurrentIndex(0)

    def update_colormap_type(self):
        return
        index = self.comboBox_colormaps.currentIndex()
        colormap = self.colormaps[index]
        app().main_window.results_widget.set_colormap(colormap)
        self.update_plot()

    def get_plot_type(self):
        plot_types = [
            "u_sum",
            "u_x",
            "u_y",
            "u_z",
        ]
        index = self.comboBox_displacements.currentIndex()
        return plot_types[index]

    def _config_treeWidget(self):
        widths = [80, 140]
        for i, width in enumerate(widths):
            self.treeWidget_frequencies.setColumnWidth(i, width)
            self.treeWidget_frequencies.headerItem().setTextAlignment(i, Qt.AlignCenter)
        #
        self.lineEdit_selected_frequency.setDisabled(True)

    def update_transparency_callback(self):
        return
        transparency = self.slider_transparency.value() / 100
        app().main_window.results_widget.set_tube_actors_transparency(transparency)

    def update_plot(self):
        self.update_animation_widget_visibility()
        if self.lineEdit_selected_frequency.text() == "":
            return

        frequency_selected = float(self.lineEdit_selected_frequency.text())
        if frequency_selected in self.frequencies:
            
            results_widget = app().main_window.results_widget
            results_widget.configure_analysis("structural_harmonic")
            results_widget.update_plot()

            # frequency = self.frequency_to_index[frequency_selected]
            self.frequency_index = self.frequencies.index(frequency_selected)
            # color_scale_setup = self.get_user_color_scale_setup()
            # app().project.set_color_scale_setup(color_scale_setup)
            # app().main_window.structural_harmonic_analysis.update_plot()
            # app().main_window.results_widget.clear_cache()
        
    def current_frequency_index(self):
        if self.frequency_index is not None:
            return self.frequency_index
        return 0

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

        color_scale_setup = {   "absolute" : absolute,
                                "ux_abs_values" : ux_abs_values,
                                "uy_abs_values" : uy_abs_values,
                                "uz_abs_values" : uz_abs_values,
                                "ux_real_values" : ux_real_values,
                                "uy_real_values" : uy_real_values,
                                "uz_real_values" : uz_real_values,
                                "ux_imag_values" : ux_imag_values,
                                "uy_imag_values" : uy_imag_values,
                                "uz_imag_values" : uz_imag_values,
                                "absolute_animation" : absolute_animation,
                                "ux_animation" : ux_animation,
                                "uy_animation" : uy_animation,
                                "uz_animation" : uz_animation   }

        return color_scale_setup

    def load_frequencies(self):
        self.treeWidget_frequencies.setDisabled(False)
        if isinstance(app().project.model.frequencies, np.ndarray):
            self.frequencies = list(app().project.model.frequencies)
        else:
            return

        self.frequency_to_index = dict(zip(self.frequencies, np.arange(len(self.frequencies), dtype=int)))

        self.treeWidget_frequencies.clear()
        for index, frequency in enumerate(self.frequencies):

            item = QTreeWidgetItem([str(index+1), str(frequency)])
            for i in range(2):
                item.setTextAlignment(i, Qt.AlignCenter)
            self.treeWidget_frequencies.addTopLevelItem(item)
        
        first_item = self.treeWidget_frequencies.topLevelItem(0)
        first_item.setSelected(True)
        self.treeWidget_frequencies.itemClicked.emit(first_item, 0)

    def plot_displacement_for_static_analysis(self):
        #
        self.lineEdit_selected_frequency.setText("0.0")
        color_scale_setup = self.get_user_color_scale_setup()
        #
        app().project.set_color_scale_setup(color_scale_setup)
        app().main_window.results_widget.show_displacement_field(0)

    def on_click_item(self, item):
        self.lineEdit_selected_frequency.setText(item.text(1))
        self.update_plot()

    def on_doubleclick_item(self, item):
        self.lineEdit_selected_frequency.setText(item.text(1))
        self.update_plot()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.update_plot()
        elif event.key() == Qt.Key_Escape:
            self.close()