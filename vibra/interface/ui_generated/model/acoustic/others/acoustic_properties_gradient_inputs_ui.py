# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'acoustic_properties_gradient_inputs.ui'
##
## Created by: Qt User Interface Compiler version 6.9.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QDoubleSpinBox,
    QFrame, QGridLayout, QHeaderView, QLabel,
    QLineEdit, QPushButton, QScrollArea, QSizePolicy,
    QSpacerItem, QTabWidget, QTreeWidget, QTreeWidgetItem,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(512, 676)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.frame_top = QFrame(Dialog)
        self.frame_top.setObjectName(u"frame_top")
        self.frame_top.setMinimumSize(QSize(0, 48))
        self.frame_top.setMaximumSize(QSize(16777215, 48))
        self.frame_top.setFrameShape(QFrame.Shape.Box)
        self.frame_top.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_top)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label = QLabel(self.frame_top)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_top, 0, 0, 1, 1)

        self.frame_main = QFrame(Dialog)
        self.frame_main.setObjectName(u"frame_main")
        self.frame_main.setFrameShape(QFrame.Shape.Box)
        self.frame_main.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_main)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(4, 4, 4, 4)
        self.scrollArea = QScrollArea(self.frame_main)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 492, 552))
        self.gridLayout_5 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_5.setSpacing(4)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(2, 2, 2, 2)
        self.frame_fluid_info = QFrame(self.scrollAreaWidgetContents)
        self.frame_fluid_info.setObjectName(u"frame_fluid_info")
        self.frame_fluid_info.setMaximumSize(QSize(16777215, 160))
        self.frame_fluid_info.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_fluid_info.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_18 = QGridLayout(self.frame_fluid_info)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.gridLayout_18.setContentsMargins(6, 6, 6, 6)
        self.lineEdit_fluid_density = QLineEdit(self.frame_fluid_info)
        self.lineEdit_fluid_density.setObjectName(u"lineEdit_fluid_density")
        self.lineEdit_fluid_density.setEnabled(False)
        self.lineEdit_fluid_density.setMinimumSize(QSize(100, 28))
        self.lineEdit_fluid_density.setMaximumSize(QSize(100, 28))
        font1 = QFont()
        font1.setPointSize(10)
        self.lineEdit_fluid_density.setFont(font1)
        self.lineEdit_fluid_density.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.lineEdit_fluid_density.setStyleSheet(u"QLineEdit{background-color: rgb(255, 255, 255); color: rgb(0, 0, 0)}\n"
"QLineEdit:disabled {background-color: rgb(230, 230, 230); color: rgb(120, 120, 120)}")
        self.lineEdit_fluid_density.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_18.addWidget(self.lineEdit_fluid_density, 1, 2, 1, 1)

        self.pushButton_get_fluid = QPushButton(self.frame_fluid_info)
        self.pushButton_get_fluid.setObjectName(u"pushButton_get_fluid")
        self.pushButton_get_fluid.setMinimumSize(QSize(72, 28))
        self.pushButton_get_fluid.setMaximumSize(QSize(72, 28))
        self.pushButton_get_fluid.setFont(font1)

        self.gridLayout_18.addWidget(self.pushButton_get_fluid, 0, 3, 1, 1)

        self.label_36 = QLabel(self.frame_fluid_info)
        self.label_36.setObjectName(u"label_36")
        self.label_36.setMinimumSize(QSize(0, 28))
        self.label_36.setMaximumSize(QSize(16777215, 28))
        self.label_36.setFont(font1)
        self.label_36.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_18.addWidget(self.label_36, 1, 1, 1, 1)

        self.label_47 = QLabel(self.frame_fluid_info)
        self.label_47.setObjectName(u"label_47")
        self.label_47.setMinimumSize(QSize(0, 28))
        self.label_47.setMaximumSize(QSize(16777215, 28))
        self.label_47.setFont(font1)
        self.label_47.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_18.addWidget(self.label_47, 2, 1, 1, 1)

        self.lineEdit_selected_fluid = QLineEdit(self.frame_fluid_info)
        self.lineEdit_selected_fluid.setObjectName(u"lineEdit_selected_fluid")
        self.lineEdit_selected_fluid.setEnabled(False)
        self.lineEdit_selected_fluid.setMinimumSize(QSize(100, 28))
        self.lineEdit_selected_fluid.setMaximumSize(QSize(100, 28))
        self.lineEdit_selected_fluid.setFont(font1)
        self.lineEdit_selected_fluid.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.lineEdit_selected_fluid.setStyleSheet(u"QLineEdit{background-color: rgb(255, 255, 255); color: rgb(0, 0, 0)}\n"
"QLineEdit:disabled {background-color: rgb(230, 230, 230); color: rgb(120, 120, 120)}")
        self.lineEdit_selected_fluid.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_18.addWidget(self.lineEdit_selected_fluid, 0, 2, 1, 1)

        self.lineEdit_speed_of_sound = QLineEdit(self.frame_fluid_info)
        self.lineEdit_speed_of_sound.setObjectName(u"lineEdit_speed_of_sound")
        self.lineEdit_speed_of_sound.setEnabled(False)
        self.lineEdit_speed_of_sound.setMinimumSize(QSize(100, 28))
        self.lineEdit_speed_of_sound.setMaximumSize(QSize(100, 28))
        self.lineEdit_speed_of_sound.setFont(font1)
        self.lineEdit_speed_of_sound.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.lineEdit_speed_of_sound.setStyleSheet(u"QLineEdit{background-color: rgb(255, 255, 255); color: rgb(0, 0, 0)}\n"
"QLineEdit:disabled {background-color: rgb(230, 230, 230); color: rgb(120, 120, 120)}")
        self.lineEdit_speed_of_sound.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_18.addWidget(self.lineEdit_speed_of_sound, 2, 2, 1, 1)

        self.label_48 = QLabel(self.frame_fluid_info)
        self.label_48.setObjectName(u"label_48")
        self.label_48.setMinimumSize(QSize(0, 28))
        self.label_48.setMaximumSize(QSize(16777215, 28))
        self.label_48.setFont(font1)
        self.label_48.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_18.addWidget(self.label_48, 1, 3, 1, 1)

        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_18.addItem(self.horizontalSpacer_14, 0, 0, 1, 1)

        self.horizontalSpacer_18 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_18.addItem(self.horizontalSpacer_18, 0, 4, 1, 1)

        self.label_49 = QLabel(self.frame_fluid_info)
        self.label_49.setObjectName(u"label_49")
        self.label_49.setMinimumSize(QSize(0, 28))
        self.label_49.setMaximumSize(QSize(16777215, 28))
        self.label_49.setFont(font1)
        self.label_49.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_18.addWidget(self.label_49, 2, 3, 1, 1)

        self.label_31 = QLabel(self.frame_fluid_info)
        self.label_31.setObjectName(u"label_31")
        self.label_31.setMinimumSize(QSize(0, 28))
        self.label_31.setMaximumSize(QSize(16777215, 28))
        self.label_31.setFont(font1)
        self.label_31.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_18.addWidget(self.label_31, 0, 1, 1, 1)

        self.label_52 = QLabel(self.frame_fluid_info)
        self.label_52.setObjectName(u"label_52")
        self.label_52.setMinimumSize(QSize(0, 28))
        self.label_52.setMaximumSize(QSize(16777215, 28))
        self.label_52.setFont(font1)
        self.label_52.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_18.addWidget(self.label_52, 3, 1, 1, 1)

        self.comboBox_fluid_point_selector = QComboBox(self.frame_fluid_info)
        self.comboBox_fluid_point_selector.addItem("")
        self.comboBox_fluid_point_selector.addItem("")
        self.comboBox_fluid_point_selector.setObjectName(u"comboBox_fluid_point_selector")
        self.comboBox_fluid_point_selector.setMinimumSize(QSize(0, 28))
        self.comboBox_fluid_point_selector.setMaximumSize(QSize(200, 28))
        self.comboBox_fluid_point_selector.setFont(font1)

        self.gridLayout_18.addWidget(self.comboBox_fluid_point_selector, 3, 2, 1, 1)


        self.gridLayout_5.addWidget(self.frame_fluid_info, 1, 0, 1, 1)

        self.tabWidget_main = QTabWidget(self.scrollAreaWidgetContents)
        self.tabWidget_main.setObjectName(u"tabWidget_main")
        self.tabWidget_main.setMaximumSize(QSize(16777215, 16777215))
        self.tabWidget_main.setFont(font1)
        self.tab_rectangular = QWidget()
        self.tab_rectangular.setObjectName(u"tab_rectangular")
        self.gridLayout_6 = QGridLayout(self.tab_rectangular)
        self.gridLayout_6.setSpacing(4)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(4, 4, 4, 4)
        self.frame_4 = QFrame(self.tab_rectangular)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_7 = QGridLayout(self.frame_4)
        self.gridLayout_7.setSpacing(6)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(6, 6, 6, 6)
        self.comboBox_gradient_direction = QComboBox(self.frame_4)
        self.comboBox_gradient_direction.addItem("")
        self.comboBox_gradient_direction.addItem("")
        self.comboBox_gradient_direction.addItem("")
        self.comboBox_gradient_direction.setObjectName(u"comboBox_gradient_direction")
        self.comboBox_gradient_direction.setMinimumSize(QSize(0, 28))
        self.comboBox_gradient_direction.setMaximumSize(QSize(200, 28))
        self.comboBox_gradient_direction.setFont(font1)

        self.gridLayout_7.addWidget(self.comboBox_gradient_direction, 0, 3, 1, 1)

        self.label_50 = QLabel(self.frame_4)
        self.label_50.setObjectName(u"label_50")
        self.label_50.setMinimumSize(QSize(0, 28))
        self.label_50.setMaximumSize(QSize(148, 28))
        self.label_50.setFont(font1)
        self.label_50.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_50, 2, 1, 1, 1)

        self.doubleSpinBox_selection_radius = QDoubleSpinBox(self.frame_4)
        self.doubleSpinBox_selection_radius.setObjectName(u"doubleSpinBox_selection_radius")
        self.doubleSpinBox_selection_radius.setMinimumSize(QSize(100, 28))
        self.doubleSpinBox_selection_radius.setMaximumSize(QSize(200, 28))
        font2 = QFont()
        font2.setPointSize(9)
        self.doubleSpinBox_selection_radius.setFont(font2)
        self.doubleSpinBox_selection_radius.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.doubleSpinBox_selection_radius.setDecimals(0)
        self.doubleSpinBox_selection_radius.setMinimum(2.000000000000000)
        self.doubleSpinBox_selection_radius.setMaximum(50.000000000000000)
        self.doubleSpinBox_selection_radius.setSingleStep(1.000000000000000)
        self.doubleSpinBox_selection_radius.setValue(10.000000000000000)

        self.gridLayout_7.addWidget(self.doubleSpinBox_selection_radius, 2, 3, 1, 1)

        self.label_51 = QLabel(self.frame_4)
        self.label_51.setObjectName(u"label_51")
        self.label_51.setMinimumSize(QSize(0, 28))
        self.label_51.setMaximumSize(QSize(148, 28))
        self.label_51.setFont(font1)
        self.label_51.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_51, 1, 1, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_3, 0, 0, 1, 1)

        self.comboBox_refinement_regions = QComboBox(self.frame_4)
        self.comboBox_refinement_regions.addItem("")
        self.comboBox_refinement_regions.addItem("")
        self.comboBox_refinement_regions.setObjectName(u"comboBox_refinement_regions")
        self.comboBox_refinement_regions.setMinimumSize(QSize(0, 28))
        self.comboBox_refinement_regions.setMaximumSize(QSize(200, 28))
        self.comboBox_refinement_regions.setFont(font1)

        self.gridLayout_7.addWidget(self.comboBox_refinement_regions, 1, 3, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_2, 0, 4, 1, 1)

        self.label_14 = QLabel(self.frame_4)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setMinimumSize(QSize(120, 0))
        self.label_14.setMaximumSize(QSize(148, 16777215))
        self.label_14.setFont(font1)
        self.label_14.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_14, 3, 1, 1, 1)

        self.comboBox_beyond_bounds_values = QComboBox(self.frame_4)
        self.comboBox_beyond_bounds_values.addItem("")
        self.comboBox_beyond_bounds_values.addItem("")
        self.comboBox_beyond_bounds_values.setObjectName(u"comboBox_beyond_bounds_values")
        self.comboBox_beyond_bounds_values.setMinimumSize(QSize(0, 28))
        self.comboBox_beyond_bounds_values.setMaximumSize(QSize(200, 28))
        self.comboBox_beyond_bounds_values.setFont(font1)

        self.gridLayout_7.addWidget(self.comboBox_beyond_bounds_values, 3, 3, 1, 1)

        self.label_13 = QLabel(self.frame_4)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setMinimumSize(QSize(120, 0))
        self.label_13.setMaximumSize(QSize(148, 16777215))
        self.label_13.setFont(font1)
        self.label_13.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_13, 0, 1, 1, 2)


        self.gridLayout_6.addWidget(self.frame_4, 0, 0, 1, 1)

        self.frame = QFrame(self.tab_rectangular)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.NoFrame)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_10 = QGridLayout(self.frame)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.label_24 = QLabel(self.frame)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setMinimumSize(QSize(0, 28))
        self.label_24.setMaximumSize(QSize(200, 28))
        self.label_24.setFont(font1)
        self.label_24.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_10.addWidget(self.label_24, 0, 3, 1, 1)

        self.lineEdit_end_temperature = QLineEdit(self.frame)
        self.lineEdit_end_temperature.setObjectName(u"lineEdit_end_temperature")
        self.lineEdit_end_temperature.setEnabled(True)
        self.lineEdit_end_temperature.setMinimumSize(QSize(0, 28))
        self.lineEdit_end_temperature.setMaximumSize(QSize(180, 28))
        self.lineEdit_end_temperature.setFont(font1)
        self.lineEdit_end_temperature.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_10.addWidget(self.lineEdit_end_temperature, 2, 3, 1, 1)

        self.label_16 = QLabel(self.frame)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setMinimumSize(QSize(100, 0))
        self.label_16.setMaximumSize(QSize(140, 16777215))
        self.label_16.setFont(font1)
        self.label_16.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_16, 1, 0, 1, 1)

        self.lineEdit_end_pressure = QLineEdit(self.frame)
        self.lineEdit_end_pressure.setObjectName(u"lineEdit_end_pressure")
        self.lineEdit_end_pressure.setEnabled(True)
        self.lineEdit_end_pressure.setMinimumSize(QSize(0, 28))
        self.lineEdit_end_pressure.setMaximumSize(QSize(180, 28))
        self.lineEdit_end_pressure.setFont(font1)
        self.lineEdit_end_pressure.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_10.addWidget(self.lineEdit_end_pressure, 3, 3, 1, 1)

        self.label_20 = QLabel(self.frame)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setMinimumSize(QSize(100, 0))
        self.label_20.setMaximumSize(QSize(140, 16777215))
        self.label_20.setFont(font1)
        self.label_20.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_20, 3, 0, 1, 1)

        self.label_11 = QLabel(self.frame)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMinimumSize(QSize(0, 28))
        self.label_11.setMaximumSize(QSize(200, 28))
        self.label_11.setFont(font1)
        self.label_11.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_10.addWidget(self.label_11, 0, 1, 1, 1)

        self.lineEdit_end_coords = QLineEdit(self.frame)
        self.lineEdit_end_coords.setObjectName(u"lineEdit_end_coords")
        self.lineEdit_end_coords.setMinimumSize(QSize(0, 28))
        self.lineEdit_end_coords.setMaximumSize(QSize(180, 28))
        self.lineEdit_end_coords.setFont(font1)
        self.lineEdit_end_coords.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_10.addWidget(self.lineEdit_end_coords, 1, 3, 1, 1)

        self.lineEdit_start_temperature = QLineEdit(self.frame)
        self.lineEdit_start_temperature.setObjectName(u"lineEdit_start_temperature")
        self.lineEdit_start_temperature.setEnabled(True)
        self.lineEdit_start_temperature.setMinimumSize(QSize(0, 28))
        self.lineEdit_start_temperature.setMaximumSize(QSize(180, 28))
        self.lineEdit_start_temperature.setFont(font1)
        self.lineEdit_start_temperature.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_10.addWidget(self.lineEdit_start_temperature, 2, 1, 1, 1)

        self.lineEdit_start_pressure = QLineEdit(self.frame)
        self.lineEdit_start_pressure.setObjectName(u"lineEdit_start_pressure")
        self.lineEdit_start_pressure.setEnabled(True)
        self.lineEdit_start_pressure.setMinimumSize(QSize(0, 28))
        self.lineEdit_start_pressure.setMaximumSize(QSize(180, 28))
        self.lineEdit_start_pressure.setFont(font1)
        self.lineEdit_start_pressure.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_10.addWidget(self.lineEdit_start_pressure, 3, 1, 1, 1)

        self.lineEdit_start_coords = QLineEdit(self.frame)
        self.lineEdit_start_coords.setObjectName(u"lineEdit_start_coords")
        self.lineEdit_start_coords.setMinimumSize(QSize(0, 28))
        self.lineEdit_start_coords.setMaximumSize(QSize(180, 28))
        self.lineEdit_start_coords.setFont(font1)
        self.lineEdit_start_coords.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_10.addWidget(self.lineEdit_start_coords, 1, 1, 1, 1)

        self.comboBox_temperature_units = QComboBox(self.frame)
        self.comboBox_temperature_units.addItem("")
        self.comboBox_temperature_units.addItem("")
        self.comboBox_temperature_units.addItem("")
        self.comboBox_temperature_units.setObjectName(u"comboBox_temperature_units")
        self.comboBox_temperature_units.setMinimumSize(QSize(100, 28))
        self.comboBox_temperature_units.setMaximumSize(QSize(100, 28))
        font3 = QFont()
        font3.setFamilies([u"MS Shell Dlg 2"])
        font3.setPointSize(10)
        font3.setItalic(False)
        self.comboBox_temperature_units.setFont(font3)

        self.gridLayout_10.addWidget(self.comboBox_temperature_units, 2, 4, 1, 1)

        self.comboBox_pressure_units = QComboBox(self.frame)
        self.comboBox_pressure_units.addItem("")
        self.comboBox_pressure_units.addItem("")
        self.comboBox_pressure_units.addItem("")
        self.comboBox_pressure_units.addItem("")
        self.comboBox_pressure_units.addItem("")
        self.comboBox_pressure_units.addItem("")
        self.comboBox_pressure_units.addItem("")
        self.comboBox_pressure_units.addItem("")
        self.comboBox_pressure_units.addItem("")
        self.comboBox_pressure_units.addItem("")
        self.comboBox_pressure_units.addItem("")
        self.comboBox_pressure_units.addItem("")
        self.comboBox_pressure_units.addItem("")
        self.comboBox_pressure_units.addItem("")
        self.comboBox_pressure_units.setObjectName(u"comboBox_pressure_units")
        self.comboBox_pressure_units.setMinimumSize(QSize(100, 28))
        self.comboBox_pressure_units.setMaximumSize(QSize(100, 28))
        self.comboBox_pressure_units.setFont(font3)

        self.gridLayout_10.addWidget(self.comboBox_pressure_units, 3, 4, 1, 1)

        self.label_17 = QLabel(self.frame)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setMinimumSize(QSize(100, 28))
        self.label_17.setMaximumSize(QSize(100, 28))
        self.label_17.setFont(font1)

        self.gridLayout_10.addWidget(self.label_17, 1, 4, 1, 1)

        self.label_15 = QLabel(self.frame)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setMinimumSize(QSize(100, 0))
        self.label_15.setMaximumSize(QSize(140, 16777215))
        self.label_15.setFont(font1)
        self.label_15.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_15, 2, 0, 1, 1)


        self.gridLayout_6.addWidget(self.frame, 1, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_rectangular, "")
        self.tab_list = QWidget()
        self.tab_list.setObjectName(u"tab_list")
        self.gridLayout_16 = QGridLayout(self.tab_list)
        self.gridLayout_16.setSpacing(6)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.gridLayout_16.setContentsMargins(6, 6, 6, 6)
        self.treeWidget_viscous_thermal_model = QTreeWidget(self.tab_list)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(4, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(3, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(2, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter);
        self.treeWidget_viscous_thermal_model.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_viscous_thermal_model.setObjectName(u"treeWidget_viscous_thermal_model")
        self.treeWidget_viscous_thermal_model.setMinimumSize(QSize(320, 100))
        self.treeWidget_viscous_thermal_model.setMaximumSize(QSize(16777215, 16777215))
        self.treeWidget_viscous_thermal_model.setFont(font3)
        self.treeWidget_viscous_thermal_model.setAutoScroll(True)
        self.treeWidget_viscous_thermal_model.setAlternatingRowColors(True)
        self.treeWidget_viscous_thermal_model.setIndentation(1)
        self.treeWidget_viscous_thermal_model.setItemsExpandable(True)
        self.treeWidget_viscous_thermal_model.setHeaderHidden(False)
        self.treeWidget_viscous_thermal_model.header().setDefaultSectionSize(100)
        self.treeWidget_viscous_thermal_model.header().setHighlightSections(False)
        self.treeWidget_viscous_thermal_model.header().setProperty(u"showSortIndicator", False)
        self.treeWidget_viscous_thermal_model.header().setStretchLastSection(True)

        self.gridLayout_16.addWidget(self.treeWidget_viscous_thermal_model, 0, 0, 1, 1)

        self.frame_3 = QFrame(self.tab_list)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(320, 40))
        self.frame_3.setMaximumSize(QSize(16777215, 40))
        self.frame_3.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_15 = QGridLayout(self.frame_3)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.gridLayout_15.setHorizontalSpacing(12)
        self.gridLayout_15.setContentsMargins(4, 4, 4, 4)
        self.pushButton_reset = QPushButton(self.frame_3)
        self.pushButton_reset.setObjectName(u"pushButton_reset")
        self.pushButton_reset.setMinimumSize(QSize(100, 28))
        self.pushButton_reset.setMaximumSize(QSize(100, 28))
        font4 = QFont()
        font4.setFamilies([u"MS Shell Dlg 2"])
        font4.setPointSize(10)
        font4.setBold(False)
        font4.setItalic(False)
        self.pushButton_reset.setFont(font4)
        self.pushButton_reset.setStyleSheet(u"")

        self.gridLayout_15.addWidget(self.pushButton_reset, 0, 0, 1, 1)

        self.pushButton_remove = QPushButton(self.frame_3)
        self.pushButton_remove.setObjectName(u"pushButton_remove")
        self.pushButton_remove.setMinimumSize(QSize(100, 28))
        self.pushButton_remove.setMaximumSize(QSize(100, 28))
        self.pushButton_remove.setFont(font4)
        self.pushButton_remove.setStyleSheet(u"")

        self.gridLayout_15.addWidget(self.pushButton_remove, 0, 1, 1, 1)


        self.gridLayout_16.addWidget(self.frame_3, 1, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_list, "")

        self.gridLayout_5.addWidget(self.tabWidget_main, 2, 0, 1, 1)

        self.frame_6 = QFrame(self.scrollAreaWidgetContents)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setMinimumSize(QSize(400, 48))
        self.frame_6.setMaximumSize(QSize(16777215, 200))
        self.frame_6.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_6.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_6.setLineWidth(1)
        self.gridLayout_8 = QGridLayout(self.frame_6)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(6, 6, 6, 6)
        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_7, 0, 0, 1, 1)

        self.lineEdit_selection_id = QLineEdit(self.frame_6)
        self.lineEdit_selection_id.setObjectName(u"lineEdit_selection_id")
        self.lineEdit_selection_id.setEnabled(True)
        self.lineEdit_selection_id.setMinimumSize(QSize(200, 28))
        self.lineEdit_selection_id.setMaximumSize(QSize(200, 28))
        self.lineEdit_selection_id.setFont(font1)
        self.lineEdit_selection_id.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.lineEdit_selection_id.setStyleSheet(u"QLineEdit{background-color: rgb(255, 255, 255); color: rgb(0, 0, 0)}\n"
"QLineEdit:disabled {background-color: rgb(230, 230, 230); color: rgb(120, 120, 120)}")
        self.lineEdit_selection_id.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_8.addWidget(self.lineEdit_selection_id, 0, 2, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_6, 0, 6, 1, 1)

        self.comboBox_attribution_type = QComboBox(self.frame_6)
        self.comboBox_attribution_type.addItem("")
        self.comboBox_attribution_type.addItem("")
        self.comboBox_attribution_type.setObjectName(u"comboBox_attribution_type")
        self.comboBox_attribution_type.setMinimumSize(QSize(0, 28))
        self.comboBox_attribution_type.setMaximumSize(QSize(200, 28))
        self.comboBox_attribution_type.setFont(font1)

        self.gridLayout_8.addWidget(self.comboBox_attribution_type, 0, 3, 1, 1)

        self.label_12 = QLabel(self.frame_6)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setMinimumSize(QSize(150, 28))
        self.label_12.setMaximumSize(QSize(150, 28))
        font5 = QFont()
        font5.setFamilies([u"MS Shell Dlg 2"])
        font5.setPointSize(10)
        font5.setBold(False)
        self.label_12.setFont(font5)
        self.label_12.setTextFormat(Qt.TextFormat.AutoText)
        self.label_12.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_12, 0, 1, 1, 1)


        self.gridLayout_5.addWidget(self.frame_6, 0, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_3.addWidget(self.scrollArea, 1, 1, 1, 1)


        self.gridLayout.addWidget(self.frame_main, 1, 0, 1, 1)

        self.frame_buttons = QFrame(Dialog)
        self.frame_buttons.setObjectName(u"frame_buttons")
        self.frame_buttons.setMinimumSize(QSize(0, 48))
        self.frame_buttons.setMaximumSize(QSize(16777215, 48))
        self.frame_buttons.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_buttons.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_12 = QGridLayout(self.frame_buttons)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setVerticalSpacing(0)
        self.gridLayout_12.setContentsMargins(6, 0, 6, 0)
        self.pushButton_apply_and_close = QPushButton(self.frame_buttons)
        self.pushButton_apply_and_close.setObjectName(u"pushButton_apply_and_close")
        self.pushButton_apply_and_close.setMinimumSize(QSize(72, 30))
        self.pushButton_apply_and_close.setMaximumSize(QSize(72, 30))
        font6 = QFont()
        font6.setPointSize(10)
        font6.setBold(False)
        font6.setItalic(False)
        self.pushButton_apply_and_close.setFont(font6)
        self.pushButton_apply_and_close.setStyleSheet(u"")
        self.pushButton_apply_and_close.setAutoDefault(False)
        self.pushButton_apply_and_close.setFlat(False)

        self.gridLayout_12.addWidget(self.pushButton_apply_and_close, 0, 3, 1, 1)

        self.pushButton_apply = QPushButton(self.frame_buttons)
        self.pushButton_apply.setObjectName(u"pushButton_apply")
        self.pushButton_apply.setMinimumSize(QSize(72, 30))
        self.pushButton_apply.setMaximumSize(QSize(72, 30))
        self.pushButton_apply.setFont(font6)
        self.pushButton_apply.setStyleSheet(u"")
        self.pushButton_apply.setAutoDefault(False)
        self.pushButton_apply.setFlat(False)

        self.gridLayout_12.addWidget(self.pushButton_apply, 0, 2, 1, 1)

        self.pushButton_cancel = QPushButton(self.frame_buttons)
        self.pushButton_cancel.setObjectName(u"pushButton_cancel")
        self.pushButton_cancel.setMinimumSize(QSize(72, 30))
        self.pushButton_cancel.setMaximumSize(QSize(72, 30))
        self.pushButton_cancel.setFont(font6)
        self.pushButton_cancel.setStyleSheet(u"")
        self.pushButton_cancel.setAutoDefault(False)
        self.pushButton_cancel.setFlat(False)

        self.gridLayout_12.addWidget(self.pushButton_cancel, 0, 0, 1, 1)

        self.horizontalSpacer_19 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_12.addItem(self.horizontalSpacer_19, 0, 1, 1, 1)


        self.gridLayout.addWidget(self.frame_buttons, 2, 0, 1, 1)

        QWidget.setTabOrder(self.scrollArea, self.comboBox_attribution_type)
        QWidget.setTabOrder(self.comboBox_attribution_type, self.tabWidget_main)
        QWidget.setTabOrder(self.tabWidget_main, self.treeWidget_viscous_thermal_model)
        QWidget.setTabOrder(self.treeWidget_viscous_thermal_model, self.pushButton_remove)
        QWidget.setTabOrder(self.pushButton_remove, self.pushButton_reset)
        QWidget.setTabOrder(self.pushButton_reset, self.pushButton_get_fluid)

        self.retranslateUi(Dialog)

        self.tabWidget_main.setCurrentIndex(0)
        self.comboBox_temperature_units.setCurrentIndex(1)
        self.pushButton_apply_and_close.setDefault(False)
        self.pushButton_apply.setDefault(False)
        self.pushButton_cancel.setDefault(False)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Vibra", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Acoustic properties gradient setup", None))
        self.lineEdit_fluid_density.setText("")
        self.pushButton_get_fluid.setText(QCoreApplication.translate("Dialog", u"Get fluid", None))
        self.label_36.setText(QCoreApplication.translate("Dialog", u"Fluid density", None))
        self.label_47.setText(QCoreApplication.translate("Dialog", u"Speed of sound:", None))
        self.lineEdit_selected_fluid.setText("")
        self.lineEdit_speed_of_sound.setText("")
        self.label_48.setText(QCoreApplication.translate("Dialog", u"[kg/m\u00b3]", None))
        self.label_49.setText(QCoreApplication.translate("Dialog", u"[m/s]", None))
        self.label_31.setText(QCoreApplication.translate("Dialog", u"Selected fluid:", None))
        self.label_52.setText(QCoreApplication.translate("Dialog", u"Fluid for:", None))
        self.comboBox_fluid_point_selector.setItemText(0, QCoreApplication.translate("Dialog", u" Start point", None))
        self.comboBox_fluid_point_selector.setItemText(1, QCoreApplication.translate("Dialog", u" End point", None))

        self.comboBox_gradient_direction.setItemText(0, QCoreApplication.translate("Dialog", u" x-axis", None))
        self.comboBox_gradient_direction.setItemText(1, QCoreApplication.translate("Dialog", u" y-axis", None))
        self.comboBox_gradient_direction.setItemText(2, QCoreApplication.translate("Dialog", u" z-axis", None))

        self.label_50.setText(QCoreApplication.translate("Dialog", u"Refinement regions:", None))
        self.label_51.setText(QCoreApplication.translate("Dialog", u"RefProp refinement:", None))
        self.comboBox_refinement_regions.setItemText(0, QCoreApplication.translate("Dialog", u" Disabled", None))
        self.comboBox_refinement_regions.setItemText(1, QCoreApplication.translate("Dialog", u" Enabled", None))

        self.label_14.setText(QCoreApplication.translate("Dialog", u"Beyond bounds:", None))
        self.comboBox_beyond_bounds_values.setItemText(0, QCoreApplication.translate("Dialog", u" keep constant", None))
        self.comboBox_beyond_bounds_values.setItemText(1, QCoreApplication.translate("Dialog", u" extrapolate", None))

        self.label_13.setText(QCoreApplication.translate("Dialog", u"Gradient direction:", None))
        self.label_24.setText(QCoreApplication.translate("Dialog", u"End point", None))
        self.label_16.setText(QCoreApplication.translate("Dialog", u"Coords.:", None))
        self.label_20.setText(QCoreApplication.translate("Dialog", u"Pressure:", None))
        self.label_11.setText(QCoreApplication.translate("Dialog", u"Start point", None))
        self.comboBox_temperature_units.setItemText(0, QCoreApplication.translate("Dialog", u"  K", None))
        self.comboBox_temperature_units.setItemText(1, QCoreApplication.translate("Dialog", u"  \u00baC", None))
        self.comboBox_temperature_units.setItemText(2, QCoreApplication.translate("Dialog", u"  \u00baF", None))

        self.comboBox_pressure_units.setItemText(0, QCoreApplication.translate("Dialog", u" Pa (a)", None))
        self.comboBox_pressure_units.setItemText(1, QCoreApplication.translate("Dialog", u" kPa (a)", None))
        self.comboBox_pressure_units.setItemText(2, QCoreApplication.translate("Dialog", u" atm (a)", None))
        self.comboBox_pressure_units.setItemText(3, QCoreApplication.translate("Dialog", u" bar (a)", None))
        self.comboBox_pressure_units.setItemText(4, QCoreApplication.translate("Dialog", u" kgf/cm\u00b2 (a)", None))
        self.comboBox_pressure_units.setItemText(5, QCoreApplication.translate("Dialog", u" psi (a)", None))
        self.comboBox_pressure_units.setItemText(6, QCoreApplication.translate("Dialog", u" ksi (a)", None))
        self.comboBox_pressure_units.setItemText(7, QCoreApplication.translate("Dialog", u" Pa (g)", None))
        self.comboBox_pressure_units.setItemText(8, QCoreApplication.translate("Dialog", u" kPa (g)", None))
        self.comboBox_pressure_units.setItemText(9, QCoreApplication.translate("Dialog", u" atm (g)", None))
        self.comboBox_pressure_units.setItemText(10, QCoreApplication.translate("Dialog", u" bar (g)", None))
        self.comboBox_pressure_units.setItemText(11, QCoreApplication.translate("Dialog", u" kgf/cm\u00b2 (g)", None))
        self.comboBox_pressure_units.setItemText(12, QCoreApplication.translate("Dialog", u" psi (g)", None))
        self.comboBox_pressure_units.setItemText(13, QCoreApplication.translate("Dialog", u" ksi (g)", None))

        self.label_17.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.label_15.setText(QCoreApplication.translate("Dialog", u"Temperature:", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_rectangular), QCoreApplication.translate("Dialog", u"Setup", None))
        ___qtreewidgetitem = self.treeWidget_viscous_thermal_model.headerItem()
        ___qtreewidgetitem.setText(4, QCoreApplication.translate("Dialog", u"Parameters", None));
        ___qtreewidgetitem.setText(3, QCoreApplication.translate("Dialog", u"Formulation", None));
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("Dialog", u"Section type", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"ID", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Attribution", None));
#if QT_CONFIG(tooltip)
        self.treeWidget_viscous_thermal_model.setToolTip(QCoreApplication.translate("Dialog", u"Select a face to remove the previously attributed boundary condition.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_reset.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.pushButton_remove.setText(QCoreApplication.translate("Dialog", u"Remove", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_list), QCoreApplication.translate("Dialog", u"List", None))
        self.lineEdit_selection_id.setText("")
        self.comboBox_attribution_type.setItemText(0, QCoreApplication.translate("Dialog", u" All bodies", None))
        self.comboBox_attribution_type.setItemText(1, QCoreApplication.translate("Dialog", u" Selected bodies", None))

        self.label_12.setText(QCoreApplication.translate("Dialog", u"Selection ID:", None))
        self.pushButton_apply_and_close.setText(QCoreApplication.translate("Dialog", u"Ok", None))
        self.pushButton_apply.setText(QCoreApplication.translate("Dialog", u"Apply", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
    # retranslateUi



class AcousticPropertiesGradientInputs_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame_top: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
                - frame_main: QFrame
                    - (Layout): QGridLayout
                            - scrollArea: QScrollArea
                                - scrollAreaWidgetContents: QWidget
                                    - (Layout): QGridLayout
                                            - frame_fluid_info: QFrame
                                                - (Layout): QGridLayout
                                                        - lineEdit_fluid_density: QLineEdit
                                                        - pushButton_get_fluid: QPushButton
                                                        - label_36: QLabel
                                                        - label_47: QLabel
                                                        - lineEdit_selected_fluid: QLineEdit
                                                        - lineEdit_speed_of_sound: QLineEdit
                                                        - label_48: QLabel
                                                        - label_49: QLabel
                                                        - label_31: QLabel
                                                        - label_52: QLabel
                                                        - comboBox_fluid_point_selector: QComboBox
                                            - tabWidget_main: QTabWidget
                                                - tab_rectangular: QWidget
                                                    - (Layout): QGridLayout
                                                            - frame_4: QFrame
                                                                - (Layout): QGridLayout
                                                                        - comboBox_gradient_direction: QComboBox
                                                                        - label_50: QLabel
                                                                        - doubleSpinBox_selection_radius: QDoubleSpinBox
                                                                        - label_51: QLabel
                                                                        - comboBox_refinement_regions: QComboBox
                                                                        - label_14: QLabel
                                                                        - comboBox_beyond_bounds_values: QComboBox
                                                                        - label_13: QLabel
                                                            - frame: QFrame
                                                                - (Layout): QGridLayout
                                                                        - label_24: QLabel
                                                                        - lineEdit_end_temperature: QLineEdit
                                                                        - label_16: QLabel
                                                                        - lineEdit_end_pressure: QLineEdit
                                                                        - label_20: QLabel
                                                                        - label_11: QLabel
                                                                        - lineEdit_end_coords: QLineEdit
                                                                        - lineEdit_start_temperature: QLineEdit
                                                                        - lineEdit_start_pressure: QLineEdit
                                                                        - lineEdit_start_coords: QLineEdit
                                                                        - comboBox_temperature_units: QComboBox
                                                                        - comboBox_pressure_units: QComboBox
                                                                        - label_17: QLabel
                                                                        - label_15: QLabel
                                                - tab_list: QWidget
                                                    - (Layout): QGridLayout
                                                            - treeWidget_viscous_thermal_model: QTreeWidget
                                                            - frame_3: QFrame
                                                                - (Layout): QGridLayout
                                                                        - pushButton_reset: QPushButton
                                                                        - pushButton_remove: QPushButton
                                            - frame_6: QFrame
                                                - (Layout): QGridLayout
                                                        - lineEdit_selection_id: QLineEdit
                                                        - comboBox_attribution_type: QComboBox
                                                        - label_12: QLabel
                - frame_buttons: QFrame
                    - (Layout): QGridLayout
                            - pushButton_apply_and_close: QPushButton
                            - pushButton_apply: QPushButton
                            - pushButton_cancel: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
