# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'viscous_thermal_model_inputs.ui'
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
    QSpacerItem, QSpinBox, QTabWidget, QTableWidget,
    QTableWidgetItem, QTreeWidget, QTreeWidgetItem, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(468, 480)
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
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 431, 552))
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
        self.label_47 = QLabel(self.frame_fluid_info)
        self.label_47.setObjectName(u"label_47")
        self.label_47.setMinimumSize(QSize(0, 28))
        self.label_47.setMaximumSize(QSize(16777215, 28))
        font1 = QFont()
        font1.setPointSize(10)
        self.label_47.setFont(font1)
        self.label_47.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_18.addWidget(self.label_47, 2, 1, 1, 1)

        self.doubleSpinBox_evaluated_depth = QDoubleSpinBox(self.frame_fluid_info)
        self.doubleSpinBox_evaluated_depth.setObjectName(u"doubleSpinBox_evaluated_depth")
        self.doubleSpinBox_evaluated_depth.setMinimumSize(QSize(100, 28))
        self.doubleSpinBox_evaluated_depth.setMaximumSize(QSize(100, 28))
        self.doubleSpinBox_evaluated_depth.setFont(font1)
        self.doubleSpinBox_evaluated_depth.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.doubleSpinBox_evaluated_depth.setDecimals(4)
        self.doubleSpinBox_evaluated_depth.setMinimum(0.001000000000000)
        self.doubleSpinBox_evaluated_depth.setMaximum(100.000000000000000)
        self.doubleSpinBox_evaluated_depth.setSingleStep(0.050000000000000)
        self.doubleSpinBox_evaluated_depth.setValue(0.100000000000000)

        self.gridLayout_18.addWidget(self.doubleSpinBox_evaluated_depth, 3, 2, 1, 1)

        self.pushButton_get_fluid = QPushButton(self.frame_fluid_info)
        self.pushButton_get_fluid.setObjectName(u"pushButton_get_fluid")
        self.pushButton_get_fluid.setMinimumSize(QSize(72, 28))
        self.pushButton_get_fluid.setMaximumSize(QSize(72, 28))
        self.pushButton_get_fluid.setFont(font1)
        self.pushButton_get_fluid.setAutoDefault(False)

        self.gridLayout_18.addWidget(self.pushButton_get_fluid, 0, 3, 1, 1)

        self.lineEdit_selected_fluid = QLineEdit(self.frame_fluid_info)
        self.lineEdit_selected_fluid.setObjectName(u"lineEdit_selected_fluid")
        self.lineEdit_selected_fluid.setEnabled(False)
        self.lineEdit_selected_fluid.setMinimumSize(QSize(100, 28))
        self.lineEdit_selected_fluid.setMaximumSize(QSize(100, 28))
        self.lineEdit_selected_fluid.setFont(font1)
        self.lineEdit_selected_fluid.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.lineEdit_selected_fluid.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_18.addWidget(self.lineEdit_selected_fluid, 0, 2, 1, 1)

        self.label_17 = QLabel(self.frame_fluid_info)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setFont(font1)
        self.label_17.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_18.addWidget(self.label_17, 3, 3, 1, 1)

        self.label_48 = QLabel(self.frame_fluid_info)
        self.label_48.setObjectName(u"label_48")
        self.label_48.setMinimumSize(QSize(0, 28))
        self.label_48.setMaximumSize(QSize(16777215, 28))
        self.label_48.setFont(font1)
        self.label_48.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_18.addWidget(self.label_48, 1, 3, 1, 1)

        self.horizontalSpacer_18 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_18.addItem(self.horizontalSpacer_18, 0, 4, 1, 1)

        self.label_36 = QLabel(self.frame_fluid_info)
        self.label_36.setObjectName(u"label_36")
        self.label_36.setMinimumSize(QSize(0, 28))
        self.label_36.setMaximumSize(QSize(16777215, 28))
        self.label_36.setFont(font1)
        self.label_36.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_18.addWidget(self.label_36, 1, 1, 1, 1)

        self.label_51 = QLabel(self.frame_fluid_info)
        self.label_51.setObjectName(u"label_51")
        self.label_51.setMinimumSize(QSize(0, 28))
        self.label_51.setMaximumSize(QSize(16777215, 28))
        self.label_51.setFont(font1)
        self.label_51.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_18.addWidget(self.label_51, 3, 1, 1, 1)

        self.label_31 = QLabel(self.frame_fluid_info)
        self.label_31.setObjectName(u"label_31")
        self.label_31.setMinimumSize(QSize(0, 28))
        self.label_31.setMaximumSize(QSize(16777215, 28))
        self.label_31.setFont(font1)
        self.label_31.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_18.addWidget(self.label_31, 0, 1, 1, 1)

        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_18.addItem(self.horizontalSpacer_14, 0, 0, 1, 1)

        self.lineEdit_speed_of_sound = QLineEdit(self.frame_fluid_info)
        self.lineEdit_speed_of_sound.setObjectName(u"lineEdit_speed_of_sound")
        self.lineEdit_speed_of_sound.setEnabled(False)
        self.lineEdit_speed_of_sound.setMinimumSize(QSize(100, 28))
        self.lineEdit_speed_of_sound.setMaximumSize(QSize(100, 28))
        self.lineEdit_speed_of_sound.setFont(font1)
        self.lineEdit_speed_of_sound.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.lineEdit_speed_of_sound.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_18.addWidget(self.lineEdit_speed_of_sound, 2, 2, 1, 1)

        self.label_49 = QLabel(self.frame_fluid_info)
        self.label_49.setObjectName(u"label_49")
        self.label_49.setMinimumSize(QSize(0, 28))
        self.label_49.setMaximumSize(QSize(16777215, 28))
        self.label_49.setFont(font1)
        self.label_49.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_18.addWidget(self.label_49, 2, 3, 1, 1)

        self.lineEdit_fluid_density = QLineEdit(self.frame_fluid_info)
        self.lineEdit_fluid_density.setObjectName(u"lineEdit_fluid_density")
        self.lineEdit_fluid_density.setEnabled(False)
        self.lineEdit_fluid_density.setMinimumSize(QSize(100, 28))
        self.lineEdit_fluid_density.setMaximumSize(QSize(100, 28))
        self.lineEdit_fluid_density.setFont(font1)
        self.lineEdit_fluid_density.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.lineEdit_fluid_density.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_18.addWidget(self.lineEdit_fluid_density, 1, 2, 1, 1)


        self.gridLayout_5.addWidget(self.frame_fluid_info, 2, 0, 1, 1)

        self.frame_plot_buttons = QFrame(self.scrollAreaWidgetContents)
        self.frame_plot_buttons.setObjectName(u"frame_plot_buttons")
        self.frame_plot_buttons.setMaximumSize(QSize(16777215, 48))
        self.frame_plot_buttons.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_plot_buttons.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_19 = QGridLayout(self.frame_plot_buttons)
        self.gridLayout_19.setObjectName(u"gridLayout_19")
        self.label_50 = QLabel(self.frame_plot_buttons)
        self.label_50.setObjectName(u"label_50")
        self.label_50.setMinimumSize(QSize(0, 28))
        self.label_50.setMaximumSize(QSize(16777215, 28))
        self.label_50.setFont(font1)
        self.label_50.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_19.addWidget(self.label_50, 0, 1, 1, 1)

        self.comboBox_plot_type = QComboBox(self.frame_plot_buttons)
        self.comboBox_plot_type.addItem("")
        self.comboBox_plot_type.addItem("")
        self.comboBox_plot_type.addItem("")
        self.comboBox_plot_type.addItem("")
        self.comboBox_plot_type.setObjectName(u"comboBox_plot_type")
        self.comboBox_plot_type.setMinimumSize(QSize(160, 28))
        self.comboBox_plot_type.setMaximumSize(QSize(200, 28))
        self.comboBox_plot_type.setFont(font1)

        self.gridLayout_19.addWidget(self.comboBox_plot_type, 0, 2, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_19.addItem(self.horizontalSpacer_5, 0, 4, 1, 1)

        self.pushButton_plot_data = QPushButton(self.frame_plot_buttons)
        self.pushButton_plot_data.setObjectName(u"pushButton_plot_data")
        self.pushButton_plot_data.setMinimumSize(QSize(80, 28))
        self.pushButton_plot_data.setMaximumSize(QSize(220, 28))
        self.pushButton_plot_data.setFont(font1)
        self.pushButton_plot_data.setAutoDefault(False)

        self.gridLayout_19.addWidget(self.pushButton_plot_data, 0, 3, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_19.addItem(self.horizontalSpacer_8, 0, 0, 1, 1)


        self.gridLayout_5.addWidget(self.frame_plot_buttons, 3, 0, 1, 1)

        self.tabWidget_main = QTabWidget(self.scrollAreaWidgetContents)
        self.tabWidget_main.setObjectName(u"tabWidget_main")
        self.tabWidget_main.setMinimumSize(QSize(0, 300))
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
        self.label_11 = QLabel(self.frame_4)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMinimumSize(QSize(120, 0))
        self.label_11.setMaximumSize(QSize(132, 16777215))
        self.label_11.setFont(font1)
        self.label_11.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_11, 5, 1, 1, 1)

        self.spinBox_number_of_terms = QSpinBox(self.frame_4)
        self.spinBox_number_of_terms.setObjectName(u"spinBox_number_of_terms")
        self.spinBox_number_of_terms.setMinimumSize(QSize(0, 28))
        self.spinBox_number_of_terms.setMaximumSize(QSize(16777215, 28))
        self.spinBox_number_of_terms.setFont(font1)
        self.spinBox_number_of_terms.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spinBox_number_of_terms.setMinimum(1)
        self.spinBox_number_of_terms.setMaximum(1000)
        self.spinBox_number_of_terms.setSingleStep(5)
        self.spinBox_number_of_terms.setValue(200)

        self.gridLayout_7.addWidget(self.spinBox_number_of_terms, 5, 3, 1, 1)

        self.label_3 = QLabel(self.frame_4)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(120, 0))
        self.label_3.setMaximumSize(QSize(132, 16777215))
        self.label_3.setFont(font1)
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_3, 1, 1, 1, 1)

        self.lineEdit_height_rectangular = QLineEdit(self.frame_4)
        self.lineEdit_height_rectangular.setObjectName(u"lineEdit_height_rectangular")
        self.lineEdit_height_rectangular.setMinimumSize(QSize(0, 28))
        self.lineEdit_height_rectangular.setMaximumSize(QSize(200, 28))
        self.lineEdit_height_rectangular.setFont(font1)
        self.lineEdit_height_rectangular.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_7.addWidget(self.lineEdit_height_rectangular, 1, 3, 1, 1)

        self.label_5 = QLabel(self.frame_4)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setEnabled(True)
        self.label_5.setMinimumSize(QSize(120, 0))
        self.label_5.setMaximumSize(QSize(132, 16777215))
        self.label_5.setFont(font1)
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_5, 4, 1, 1, 1)

        self.comboBox_section_type = QComboBox(self.frame_4)
        self.comboBox_section_type.addItem("")
        self.comboBox_section_type.addItem("")
        self.comboBox_section_type.addItem("")
        self.comboBox_section_type.setObjectName(u"comboBox_section_type")
        self.comboBox_section_type.setMinimumSize(QSize(0, 28))
        self.comboBox_section_type.setMaximumSize(QSize(200, 28))
        self.comboBox_section_type.setFont(font1)

        self.gridLayout_7.addWidget(self.comboBox_section_type, 0, 3, 1, 1)

        self.lineEdit_width_rectangular = QLineEdit(self.frame_4)
        self.lineEdit_width_rectangular.setObjectName(u"lineEdit_width_rectangular")
        self.lineEdit_width_rectangular.setMinimumSize(QSize(0, 28))
        self.lineEdit_width_rectangular.setMaximumSize(QSize(200, 28))
        self.lineEdit_width_rectangular.setFont(font1)
        self.lineEdit_width_rectangular.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_7.addWidget(self.lineEdit_width_rectangular, 2, 3, 1, 1)

        self.label_16 = QLabel(self.frame_4)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setMinimumSize(QSize(40, 0))
        self.label_16.setMaximumSize(QSize(40, 16777215))
        self.label_16.setFont(font1)

        self.gridLayout_7.addWidget(self.label_16, 1, 5, 1, 1)

        self.label_15 = QLabel(self.frame_4)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setMinimumSize(QSize(40, 0))
        self.label_15.setMaximumSize(QSize(40, 16777215))
        self.label_15.setFont(font1)

        self.gridLayout_7.addWidget(self.label_15, 2, 5, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_3, 2, 0, 1, 1)

        self.label_2 = QLabel(self.frame_4)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(120, 0))
        self.label_2.setMaximumSize(QSize(132, 16777215))
        self.label_2.setFont(font1)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_2, 2, 1, 1, 1)

        self.label_18 = QLabel(self.frame_4)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setEnabled(True)
        self.label_18.setMinimumSize(QSize(40, 0))
        self.label_18.setMaximumSize(QSize(40, 16777215))
        self.label_18.setFont(font1)

        self.gridLayout_7.addWidget(self.label_18, 4, 5, 1, 1)

        self.label_6 = QLabel(self.frame_4)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(120, 0))
        self.label_6.setMaximumSize(QSize(132, 16777215))
        self.label_6.setFont(font1)
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_6, 0, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_2, 2, 6, 1, 1)

        self.lineEdit_area_rectangular = QLineEdit(self.frame_4)
        self.lineEdit_area_rectangular.setObjectName(u"lineEdit_area_rectangular")
        self.lineEdit_area_rectangular.setEnabled(False)
        self.lineEdit_area_rectangular.setMinimumSize(QSize(0, 28))
        self.lineEdit_area_rectangular.setMaximumSize(QSize(200, 28))
        self.lineEdit_area_rectangular.setFont(font1)
        self.lineEdit_area_rectangular.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_7.addWidget(self.lineEdit_area_rectangular, 4, 3, 1, 1)


        self.gridLayout_6.addWidget(self.frame_4, 0, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_rectangular, "")
        self.tab_circular = QWidget()
        self.tab_circular.setObjectName(u"tab_circular")
        self.gridLayout_17 = QGridLayout(self.tab_circular)
        self.gridLayout_17.setSpacing(4)
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.gridLayout_17.setContentsMargins(4, 4, 4, 4)
        self.frame_5 = QFrame(self.tab_circular)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_9 = QGridLayout(self.frame_5)
        self.gridLayout_9.setSpacing(6)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(6, 6, 6, 6)
        self.comboBox_formulation = QComboBox(self.frame_5)
        self.comboBox_formulation.addItem("")
        self.comboBox_formulation.addItem("")
        self.comboBox_formulation.setObjectName(u"comboBox_formulation")
        self.comboBox_formulation.setMinimumSize(QSize(0, 28))
        self.comboBox_formulation.setMaximumSize(QSize(200, 28))
        self.comboBox_formulation.setFont(font1)

        self.gridLayout_9.addWidget(self.comboBox_formulation, 0, 3, 1, 1)

        self.label_21 = QLabel(self.frame_5)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setMinimumSize(QSize(40, 0))
        self.label_21.setMaximumSize(QSize(40, 16777215))
        self.label_21.setFont(font1)

        self.gridLayout_9.addWidget(self.label_21, 1, 5, 1, 1)

        self.lineEdit_area_circular = QLineEdit(self.frame_5)
        self.lineEdit_area_circular.setObjectName(u"lineEdit_area_circular")
        self.lineEdit_area_circular.setEnabled(False)
        self.lineEdit_area_circular.setMinimumSize(QSize(0, 28))
        self.lineEdit_area_circular.setMaximumSize(QSize(200, 28))
        self.lineEdit_area_circular.setFont(font1)
        self.lineEdit_area_circular.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_9.addWidget(self.lineEdit_area_circular, 3, 3, 1, 1)

        self.label_19 = QLabel(self.frame_5)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setEnabled(True)
        self.label_19.setMinimumSize(QSize(40, 0))
        self.label_19.setMaximumSize(QSize(40, 16777215))
        self.label_19.setFont(font1)

        self.gridLayout_9.addWidget(self.label_19, 3, 5, 1, 1)

        self.label_7 = QLabel(self.frame_5)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setEnabled(True)
        self.label_7.setMinimumSize(QSize(120, 0))
        self.label_7.setMaximumSize(QSize(132, 16777215))
        self.label_7.setFont(font1)
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_9.addWidget(self.label_7, 3, 1, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer_4, 1, 0, 1, 1)

        self.label_8 = QLabel(self.frame_5)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMinimumSize(QSize(120, 0))
        self.label_8.setMaximumSize(QSize(132, 16777215))
        self.label_8.setFont(font1)
        self.label_8.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_9.addWidget(self.label_8, 1, 1, 1, 1)

        self.lineEdit_radius_circular = QLineEdit(self.frame_5)
        self.lineEdit_radius_circular.setObjectName(u"lineEdit_radius_circular")
        self.lineEdit_radius_circular.setEnabled(False)
        self.lineEdit_radius_circular.setMinimumSize(QSize(0, 28))
        self.lineEdit_radius_circular.setMaximumSize(QSize(200, 28))
        self.lineEdit_radius_circular.setFont(font1)
        self.lineEdit_radius_circular.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_9.addWidget(self.lineEdit_radius_circular, 2, 3, 1, 1)

        self.label_10 = QLabel(self.frame_5)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setEnabled(True)
        self.label_10.setMinimumSize(QSize(120, 0))
        self.label_10.setMaximumSize(QSize(132, 16777215))
        self.label_10.setFont(font1)
        self.label_10.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_9.addWidget(self.label_10, 2, 1, 1, 1)

        self.lineEdit_diameter_circular = QLineEdit(self.frame_5)
        self.lineEdit_diameter_circular.setObjectName(u"lineEdit_diameter_circular")
        self.lineEdit_diameter_circular.setMinimumSize(QSize(0, 28))
        self.lineEdit_diameter_circular.setMaximumSize(QSize(200, 28))
        self.lineEdit_diameter_circular.setFont(font1)
        self.lineEdit_diameter_circular.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_9.addWidget(self.lineEdit_diameter_circular, 1, 3, 1, 1)

        self.label_22 = QLabel(self.frame_5)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setEnabled(True)
        self.label_22.setMinimumSize(QSize(40, 0))
        self.label_22.setMaximumSize(QSize(40, 16777215))
        self.label_22.setFont(font1)

        self.gridLayout_9.addWidget(self.label_22, 2, 5, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer, 1, 6, 1, 1)

        self.label_9 = QLabel(self.frame_5)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMinimumSize(QSize(120, 0))
        self.label_9.setMaximumSize(QSize(132, 16777215))
        self.label_9.setFont(font1)
        self.label_9.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_9.addWidget(self.label_9, 0, 1, 1, 1)


        self.gridLayout_17.addWidget(self.frame_5, 1, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_circular, "")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.gridLayout_10 = QGridLayout(self.tab)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.tabWidget_models = QTabWidget(self.tab)
        self.tabWidget_models.setObjectName(u"tabWidget_models")
        self.rectangular_tab = QWidget()
        self.rectangular_tab.setObjectName(u"rectangular_tab")
        self.gridLayout_11 = QGridLayout(self.rectangular_tab)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.tableWidget_rectangular = QTableWidget(self.rectangular_tab)
        if (self.tableWidget_rectangular.rowCount() < 6):
            self.tableWidget_rectangular.setRowCount(6)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_rectangular.setVerticalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_rectangular.setVerticalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        __qtablewidgetitem2.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_rectangular.setVerticalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        __qtablewidgetitem3.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_rectangular.setVerticalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        __qtablewidgetitem4.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_rectangular.setVerticalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        __qtablewidgetitem5.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_rectangular.setVerticalHeaderItem(5, __qtablewidgetitem5)
        self.tableWidget_rectangular.setObjectName(u"tableWidget_rectangular")
        self.tableWidget_rectangular.horizontalHeader().setVisible(False)

        self.gridLayout_11.addWidget(self.tableWidget_rectangular, 0, 0, 1, 1)

        self.tabWidget_models.addTab(self.rectangular_tab, "")
        self.circular_tab = QWidget()
        self.circular_tab.setObjectName(u"circular_tab")
        self.gridLayout_12 = QGridLayout(self.circular_tab)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.tableWidget_circular = QTableWidget(self.circular_tab)
        if (self.tableWidget_circular.rowCount() < 4):
            self.tableWidget_circular.setRowCount(4)
        __qtablewidgetitem6 = QTableWidgetItem()
        __qtablewidgetitem6.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_circular.setVerticalHeaderItem(0, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        __qtablewidgetitem7.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_circular.setVerticalHeaderItem(1, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        __qtablewidgetitem8.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_circular.setVerticalHeaderItem(2, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        __qtablewidgetitem9.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_circular.setVerticalHeaderItem(3, __qtablewidgetitem9)
        self.tableWidget_circular.setObjectName(u"tableWidget_circular")
        self.tableWidget_circular.horizontalHeader().setVisible(False)

        self.gridLayout_12.addWidget(self.tableWidget_circular, 0, 0, 1, 1)

        self.tabWidget_models.addTab(self.circular_tab, "")

        self.gridLayout_10.addWidget(self.tabWidget_models, 0, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab, "")
        self.tab_list = QWidget()
        self.tab_list.setObjectName(u"tab_list")
        self.gridLayout_16 = QGridLayout(self.tab_list)
        self.gridLayout_16.setSpacing(6)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.gridLayout_16.setContentsMargins(6, 6, 6, 6)
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
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        self.pushButton_reset.setFont(font2)
        self.pushButton_reset.setStyleSheet(u"")
        self.pushButton_reset.setAutoDefault(False)

        self.gridLayout_15.addWidget(self.pushButton_reset, 0, 0, 1, 1)

        self.pushButton_remove = QPushButton(self.frame_3)
        self.pushButton_remove.setObjectName(u"pushButton_remove")
        self.pushButton_remove.setMinimumSize(QSize(100, 28))
        self.pushButton_remove.setMaximumSize(QSize(100, 28))
        self.pushButton_remove.setFont(font2)
        self.pushButton_remove.setStyleSheet(u"")
        self.pushButton_remove.setAutoDefault(False)

        self.gridLayout_15.addWidget(self.pushButton_remove, 0, 1, 1, 1)


        self.gridLayout_16.addWidget(self.frame_3, 1, 0, 1, 1)

        self.treeWidget_viscous_thermal_model = QTreeWidget(self.tab_list)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter);
        self.treeWidget_viscous_thermal_model.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_viscous_thermal_model.setObjectName(u"treeWidget_viscous_thermal_model")
        self.treeWidget_viscous_thermal_model.setMinimumSize(QSize(320, 100))
        self.treeWidget_viscous_thermal_model.setMaximumSize(QSize(16777215, 16777215))
        font3 = QFont()
        font3.setFamilies([u"MS Shell Dlg 2"])
        font3.setPointSize(10)
        font3.setItalic(False)
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

        self.tabWidget_main.addTab(self.tab_list, "")

        self.gridLayout_5.addWidget(self.tabWidget_main, 1, 0, 1, 1)

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
        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_6, 0, 6, 1, 1)

        self.lineEdit_selection_id = QLineEdit(self.frame_6)
        self.lineEdit_selection_id.setObjectName(u"lineEdit_selection_id")
        self.lineEdit_selection_id.setEnabled(True)
        self.lineEdit_selection_id.setMinimumSize(QSize(140, 28))
        self.lineEdit_selection_id.setMaximumSize(QSize(200, 28))
        self.lineEdit_selection_id.setFont(font1)
        self.lineEdit_selection_id.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.lineEdit_selection_id.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_8.addWidget(self.lineEdit_selection_id, 0, 2, 1, 1)

        self.label_12 = QLabel(self.frame_6)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setMinimumSize(QSize(100, 28))
        self.label_12.setMaximumSize(QSize(120, 28))
        font4 = QFont()
        font4.setFamilies([u"MS Shell Dlg 2"])
        font4.setPointSize(10)
        font4.setBold(False)
        self.label_12.setFont(font4)
        self.label_12.setTextFormat(Qt.TextFormat.AutoText)
        self.label_12.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_12, 0, 1, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_7, 0, 0, 1, 1)

        self.comboBox_attribution_type = QComboBox(self.frame_6)
        self.comboBox_attribution_type.addItem("")
        self.comboBox_attribution_type.addItem("")
        self.comboBox_attribution_type.setObjectName(u"comboBox_attribution_type")
        self.comboBox_attribution_type.setMinimumSize(QSize(0, 28))
        self.comboBox_attribution_type.setMaximumSize(QSize(200, 28))
        self.comboBox_attribution_type.setFont(font1)

        self.gridLayout_8.addWidget(self.comboBox_attribution_type, 0, 3, 1, 1)


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
        self.gridLayout_13 = QGridLayout(self.frame_buttons)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_13.setVerticalSpacing(0)
        self.gridLayout_13.setContentsMargins(6, 0, 6, 0)
        self.pushButton_apply_and_close = QPushButton(self.frame_buttons)
        self.pushButton_apply_and_close.setObjectName(u"pushButton_apply_and_close")
        self.pushButton_apply_and_close.setMinimumSize(QSize(72, 30))
        self.pushButton_apply_and_close.setMaximumSize(QSize(72, 30))
        font5 = QFont()
        font5.setPointSize(10)
        font5.setBold(False)
        font5.setItalic(False)
        self.pushButton_apply_and_close.setFont(font5)
        self.pushButton_apply_and_close.setStyleSheet(u"")
        self.pushButton_apply_and_close.setAutoDefault(False)
        self.pushButton_apply_and_close.setFlat(False)

        self.gridLayout_13.addWidget(self.pushButton_apply_and_close, 0, 3, 1, 1)

        self.pushButton_apply = QPushButton(self.frame_buttons)
        self.pushButton_apply.setObjectName(u"pushButton_apply")
        self.pushButton_apply.setMinimumSize(QSize(72, 30))
        self.pushButton_apply.setMaximumSize(QSize(72, 30))
        self.pushButton_apply.setFont(font5)
        self.pushButton_apply.setStyleSheet(u"")
        self.pushButton_apply.setAutoDefault(False)
        self.pushButton_apply.setFlat(False)

        self.gridLayout_13.addWidget(self.pushButton_apply, 0, 2, 1, 1)

        self.pushButton_cancel = QPushButton(self.frame_buttons)
        self.pushButton_cancel.setObjectName(u"pushButton_cancel")
        self.pushButton_cancel.setMinimumSize(QSize(72, 30))
        self.pushButton_cancel.setMaximumSize(QSize(72, 30))
        self.pushButton_cancel.setFont(font5)
        self.pushButton_cancel.setStyleSheet(u"")
        self.pushButton_cancel.setAutoDefault(False)
        self.pushButton_cancel.setFlat(False)

        self.gridLayout_13.addWidget(self.pushButton_cancel, 0, 0, 1, 1)

        self.horizontalSpacer_17 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_13.addItem(self.horizontalSpacer_17, 0, 1, 1, 1)


        self.gridLayout.addWidget(self.frame_buttons, 2, 0, 1, 1)

        QWidget.setTabOrder(self.scrollArea, self.comboBox_attribution_type)
        QWidget.setTabOrder(self.comboBox_attribution_type, self.tabWidget_main)
        QWidget.setTabOrder(self.tabWidget_main, self.comboBox_section_type)
        QWidget.setTabOrder(self.comboBox_section_type, self.lineEdit_height_rectangular)
        QWidget.setTabOrder(self.lineEdit_height_rectangular, self.lineEdit_width_rectangular)
        QWidget.setTabOrder(self.lineEdit_width_rectangular, self.lineEdit_area_rectangular)
        QWidget.setTabOrder(self.lineEdit_area_rectangular, self.comboBox_formulation)
        QWidget.setTabOrder(self.comboBox_formulation, self.lineEdit_diameter_circular)
        QWidget.setTabOrder(self.lineEdit_diameter_circular, self.lineEdit_radius_circular)
        QWidget.setTabOrder(self.lineEdit_radius_circular, self.lineEdit_area_circular)
        QWidget.setTabOrder(self.lineEdit_area_circular, self.treeWidget_viscous_thermal_model)
        QWidget.setTabOrder(self.treeWidget_viscous_thermal_model, self.pushButton_remove)
        QWidget.setTabOrder(self.pushButton_remove, self.pushButton_reset)
        QWidget.setTabOrder(self.pushButton_reset, self.pushButton_get_fluid)
        QWidget.setTabOrder(self.pushButton_get_fluid, self.pushButton_plot_data)

        self.retranslateUi(Dialog)

        self.tabWidget_main.setCurrentIndex(0)
        self.tabWidget_models.setCurrentIndex(0)
        self.pushButton_apply_and_close.setDefault(False)
        self.pushButton_apply.setDefault(False)
        self.pushButton_cancel.setDefault(False)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Vibra", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Viscous-thermal loss models", None))
        self.label_47.setText(QCoreApplication.translate("Dialog", u"Speed of sound:", None))
        self.pushButton_get_fluid.setText(QCoreApplication.translate("Dialog", u"Get fluid", None))
        self.lineEdit_selected_fluid.setText("")
        self.label_17.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.label_48.setText(QCoreApplication.translate("Dialog", u"[kg/m\u00b3]", None))
        self.label_36.setText(QCoreApplication.translate("Dialog", u"Fluid density", None))
        self.label_51.setText(QCoreApplication.translate("Dialog", u"Evaluated depth:", None))
        self.label_31.setText(QCoreApplication.translate("Dialog", u"Selected fluid:", None))
        self.lineEdit_speed_of_sound.setText("")
        self.label_49.setText(QCoreApplication.translate("Dialog", u"[m/s]", None))
        self.lineEdit_fluid_density.setText("")
        self.label_50.setText(QCoreApplication.translate("Dialog", u"Plot selector:", None))
        self.comboBox_plot_type.setItemText(0, QCoreApplication.translate("Dialog", u" Fluid density", None))
        self.comboBox_plot_type.setItemText(1, QCoreApplication.translate("Dialog", u" Speed of sound", None))
        self.comboBox_plot_type.setItemText(2, QCoreApplication.translate("Dialog", u" Surface impedance", None))
        self.comboBox_plot_type.setItemText(3, QCoreApplication.translate("Dialog", u" Absorption coefficient", None))

        self.pushButton_plot_data.setText(QCoreApplication.translate("Dialog", u"Plot data", None))
        self.label_11.setText(QCoreApplication.translate("Dialog", u"Number of terms:", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Duct height (2b):", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"Duct area:", None))
        self.comboBox_section_type.setItemText(0, QCoreApplication.translate("Dialog", u" Rectangular", None))
        self.comboBox_section_type.setItemText(1, QCoreApplication.translate("Dialog", u" Quadrangular", None))
        self.comboBox_section_type.setItemText(2, QCoreApplication.translate("Dialog", u" Narrow slit", None))

        self.label_16.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.label_15.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Duct width (2a):", None))
        self.label_18.setText(QCoreApplication.translate("Dialog", u"[m\u00b2]", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"Section type:", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_rectangular), QCoreApplication.translate("Dialog", u"Rectangular", None))
        self.comboBox_formulation.setItemText(0, QCoreApplication.translate("Dialog", u" Stinson model", None))
        self.comboBox_formulation.setItemText(1, QCoreApplication.translate("Dialog", u" LRF model", None))

        self.label_21.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.label_19.setText(QCoreApplication.translate("Dialog", u"[m\u00b2]", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"Duct area:", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"Duct diameter:", None))
        self.label_10.setText(QCoreApplication.translate("Dialog", u"Duct radius:", None))
        self.label_22.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", u"Formulation:", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_circular), QCoreApplication.translate("Dialog", u"Circular", None))
        ___qtablewidgetitem = self.tableWidget_rectangular.verticalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Dialog", u"ID", None));
        ___qtablewidgetitem1 = self.tableWidget_rectangular.verticalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Dialog", u"Section type", None));
        ___qtablewidgetitem2 = self.tableWidget_rectangular.verticalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Dialog", u"Formulation type", None));
        ___qtablewidgetitem3 = self.tableWidget_rectangular.verticalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Dialog", u"Duct height", None));
        ___qtablewidgetitem4 = self.tableWidget_rectangular.verticalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Dialog", u"Duct width", None));
        ___qtablewidgetitem5 = self.tableWidget_rectangular.verticalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Dialog", u"Number of terms", None));
        self.tabWidget_models.setTabText(self.tabWidget_models.indexOf(self.rectangular_tab), QCoreApplication.translate("Dialog", u"Rectangular", None))
        ___qtablewidgetitem6 = self.tableWidget_circular.verticalHeaderItem(0)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("Dialog", u"ID", None));
        ___qtablewidgetitem7 = self.tableWidget_circular.verticalHeaderItem(1)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("Dialog", u"Section type", None));
        ___qtablewidgetitem8 = self.tableWidget_circular.verticalHeaderItem(2)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("Dialog", u"Formulation type", None));
        ___qtablewidgetitem9 = self.tableWidget_circular.verticalHeaderItem(3)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("Dialog", u"Duct diameter", None));
        self.tabWidget_models.setTabText(self.tabWidget_models.indexOf(self.circular_tab), QCoreApplication.translate("Dialog", u"Circular", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab), QCoreApplication.translate("Dialog", u"Edit", None))
        self.pushButton_reset.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.pushButton_remove.setText(QCoreApplication.translate("Dialog", u"Remove", None))
        ___qtreewidgetitem = self.treeWidget_viscous_thermal_model.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"Model ID", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Volume", None));
#if QT_CONFIG(tooltip)
        self.treeWidget_viscous_thermal_model.setToolTip(QCoreApplication.translate("Dialog", u"Select an element to remove the previously attributed boundary condition.", None))
#endif // QT_CONFIG(tooltip)
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_list), QCoreApplication.translate("Dialog", u"List", None))
        self.lineEdit_selection_id.setText("")
        self.label_12.setText(QCoreApplication.translate("Dialog", u"Selection ID:", None))
        self.comboBox_attribution_type.setItemText(0, QCoreApplication.translate("Dialog", u" All bodies", None))
        self.comboBox_attribution_type.setItemText(1, QCoreApplication.translate("Dialog", u" Selected bodies", None))

        self.pushButton_apply_and_close.setText(QCoreApplication.translate("Dialog", u"Ok", None))
        self.pushButton_apply.setText(QCoreApplication.translate("Dialog", u"Apply", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
    # retranslateUi



class ViscousThermalModelInputs_UI(QDialog, Ui_Dialog):
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
                                                        - label_47: QLabel
                                                        - doubleSpinBox_evaluated_depth: QDoubleSpinBox
                                                        - pushButton_get_fluid: QPushButton
                                                        - lineEdit_selected_fluid: QLineEdit
                                                        - label_17: QLabel
                                                        - label_48: QLabel
                                                        - label_36: QLabel
                                                        - label_51: QLabel
                                                        - label_31: QLabel
                                                        - lineEdit_speed_of_sound: QLineEdit
                                                        - label_49: QLabel
                                                        - lineEdit_fluid_density: QLineEdit
                                            - frame_plot_buttons: QFrame
                                                - (Layout): QGridLayout
                                                        - label_50: QLabel
                                                        - comboBox_plot_type: QComboBox
                                                        - pushButton_plot_data: QPushButton
                                            - tabWidget_main: QTabWidget
                                                - tab_rectangular: QWidget
                                                    - (Layout): QGridLayout
                                                            - frame_4: QFrame
                                                                - (Layout): QGridLayout
                                                                        - label_11: QLabel
                                                                        - spinBox_number_of_terms: QSpinBox
                                                                        - label_3: QLabel
                                                                        - lineEdit_height_rectangular: QLineEdit
                                                                        - label_5: QLabel
                                                                        - comboBox_section_type: QComboBox
                                                                        - lineEdit_width_rectangular: QLineEdit
                                                                        - label_16: QLabel
                                                                        - label_15: QLabel
                                                                        - label_2: QLabel
                                                                        - label_18: QLabel
                                                                        - label_6: QLabel
                                                                        - lineEdit_area_rectangular: QLineEdit
                                                - tab_circular: QWidget
                                                    - (Layout): QGridLayout
                                                            - frame_5: QFrame
                                                                - (Layout): QGridLayout
                                                                        - comboBox_formulation: QComboBox
                                                                        - label_21: QLabel
                                                                        - lineEdit_area_circular: QLineEdit
                                                                        - label_19: QLabel
                                                                        - label_7: QLabel
                                                                        - label_8: QLabel
                                                                        - lineEdit_radius_circular: QLineEdit
                                                                        - label_10: QLabel
                                                                        - lineEdit_diameter_circular: QLineEdit
                                                                        - label_22: QLabel
                                                                        - label_9: QLabel
                                                - tab: QWidget
                                                    - (Layout): QGridLayout
                                                            - tabWidget_models: QTabWidget
                                                                - rectangular_tab: QWidget
                                                                    - (Layout): QGridLayout
                                                                            - tableWidget_rectangular: QTableWidget
                                                                - circular_tab: QWidget
                                                                    - (Layout): QGridLayout
                                                                            - tableWidget_circular: QTableWidget
                                                - tab_list: QWidget
                                                    - (Layout): QGridLayout
                                                            - frame_3: QFrame
                                                                - (Layout): QGridLayout
                                                                        - pushButton_reset: QPushButton
                                                                        - pushButton_remove: QPushButton
                                                            - treeWidget_viscous_thermal_model: QTreeWidget
                                            - frame_6: QFrame
                                                - (Layout): QGridLayout
                                                        - lineEdit_selection_id: QLineEdit
                                                        - label_12: QLabel
                                                        - comboBox_attribution_type: QComboBox
                - frame_buttons: QFrame
                    - (Layout): QGridLayout
                            - pushButton_apply_and_close: QPushButton
                            - pushButton_apply: QPushButton
                            - pushButton_cancel: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
