from PySide6.QtWidgets import QComboBox, QFrame, QLineEdit, QPushButton, QSlider, QTreeWidget, QTreeWidgetItem, QWidget
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, Signal

from vibra import app, UI_DIR

from molde import load_ui

import numpy as np


class PlotAcousticPressureField(QWidget):
    value_changed = Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        ui_path = UI_DIR / "plots/acoustic/plot_acoustic_pressure_field.ui"
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
        self.current_frequency = None
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
        # self.comboBox_colormaps.setDisabled(True)
        self.slider_transparency.setDisabled(True)
        #
        self.comboBox_colormaps.currentIndexChanged.connect(self.update_color_and_deformation)
        self.comboBox_color_scale.currentIndexChanged.connect(self.update_plot)
        #
        self.pushButton_plot.clicked.connect(self.update_plot)
        #
        self.slider_transparency.valueChanged.connect(self.update_transparency_callback)
        #
        self.treeWidget_frequencies.itemClicked.connect(self.on_click_item)
        self.treeWidget_frequencies.itemDoubleClicked.connect(self.on_doubleclick_item)
        #
        self.load_user_preference_colormap()

    def _config_treeWidget(self):
        widths = [80, 140]
        for i, width in enumerate(widths):
            self.treeWidget_frequencies.setColumnWidth(i, width)
            self.treeWidget_frequencies.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def update_animation_widget_visibility(self):
        index = self.comboBox_color_scale.currentIndex()
        if index >= 2:
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

    def update_color_and_deformation(self):
        app().main_window.results_widget.update_color_and_deformation()

    def update_transparency_callback(self):
        return
        transparency = self.slider_transparency.value() / 100
        app().main_window.results_widget.set_tube_actors_transparency(transparency)

    def update_plot(self):

        self.update_animation_widget_visibility()
        if self.lineEdit_selected_frequency.text() == "":
            return

        frequency_selected = float(self.lineEdit_selected_frequency.text())
        self.current_frequency = self.frequency_to_index[frequency_selected]

        app().main_window.results_widget.update_plot()

        results_widget = app().main_window.results_widget
        results_widget.configure_analysis("acoustic_harmonic")
        results_widget.update_plot()

        # color_scale_setup = self.get_user_color_scale_setup()
        # app().project.set_color_scale_setup(color_scale_setup)
        # app().main_window.results_widget.show_pressure_field(self.frequency)
        # app().main_window.results_widget.clear_cache()

    def get_colormap(self) -> str:
        colormaps = [
            "jet",
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
        index = self.comboBox_colormaps.currentIndex()
        return colormaps[index]

    def get_user_color_scale_setup(self):
        return

        absolute = False
        real_values = False
        imag_values = False
        absolute_animation = False

        index = self.comboBox_color_scale.currentIndex()

        if index == 0:
            absolute_animation = True
        if index == 2:
            absolute = True
        elif index == 3:
            real_values = True
        elif index == 4:
            imag_values = True
        
        color_scale_setup = {   "absolute" : absolute,
                                "real_values" : real_values,
                                "imag_values" : imag_values,
                                "absolute_animation" : absolute_animation   }

        return color_scale_setup

    def get_plot_type(self):
        plot_types = [
            "absolute_animation",
            "non_absolute_animation",
            "absolute_values",
            "real_values",
            "imag_values",
        ]
        index = self.comboBox_color_scale.currentIndex()
        return plot_types[index]

    def load_frequencies(self):
        if isinstance(app().project.model.frequencies, np.ndarray):
            self.frequencies = app().project.model.frequencies
        else:
            return

        self.frequency_to_index = dict(zip(self.frequencies, np.arange(len(self.frequencies), dtype=int)))

        self.treeWidget_frequencies.clear()
        for index, frequency in enumerate(self.frequencies):
            new = QTreeWidgetItem([str(index+1), str(frequency)])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_frequencies.addTopLevelItem(new)
        
        first_item = self.treeWidget_frequencies.topLevelItem(0)
        first_item.setSelected(True)
        self.treeWidget_frequencies.itemClicked.emit(first_item, 0)
        
    def current_frequency_index(self):
        if self.current_frequency is not None:
            return self.current_frequency
        return 0

    def on_click_item(self, item):
        self.lineEdit_selected_frequency.setText(item.text(1))
        self.update_plot()

    def on_doubleclick_item(self, item):
        self.lineEdit_selected_frequency.setText(item.text(1))
        self.update_plot()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.update_plot()