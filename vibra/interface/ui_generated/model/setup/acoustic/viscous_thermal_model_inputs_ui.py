# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'viscous_thermal_model_inputs.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
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
    QSpacerItem, QSpinBox, QTabWidget, QTreeWidget,
    QTreeWidgetItem, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(559, 741)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.frame_top = QFrame(Dialog)
        self.frame_top.setObjectName(u"frame_top")
        self.frame_top.setMinimumSize(QSize(0, 48))
        self.frame_top.setMaximumSize(QSize(16777215, 48))
        self.frame_top.setFrameShape(QFrame.Box)
        self.frame_top.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_top)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label = QLabel(self.frame_top)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_top, 0, 0, 1, 1)

        self.frame_main = QFrame(Dialog)
        self.frame_main.setObjectName(u"frame_main")
        self.frame_main.setFrameShape(QFrame.Box)
        self.frame_main.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_main)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(4, 4, 4, 4)
        self.scrollArea = QScrollArea(self.frame_main)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setFrameShape(QFrame.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 539, 617))
        self.gridLayout_5 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_5.setSpacing(4)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(2, 2, 2, 2)
        self.frame_6 = QFrame(self.scrollAreaWidgetContents)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setMinimumSize(QSize(400, 168))
        self.frame_6.setMaximumSize(QSize(16777215, 200))
        self.frame_6.setFrameShape(QFrame.NoFrame)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.frame_6.setLineWidth(1)
        self.gridLayout_8 = QGridLayout(self.frame_6)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(6, 6, 6, 6)
        self.comboBox_attribution_type = QComboBox(self.frame_6)
        self.comboBox_attribution_type.addItem("")
        self.comboBox_attribution_type.addItem("")
        self.comboBox_attribution_type.addItem("")
        self.comboBox_attribution_type.addItem("")
        self.comboBox_attribution_type.setObjectName(u"comboBox_attribution_type")
        self.comboBox_attribution_type.setMinimumSize(QSize(0, 28))
        self.comboBox_attribution_type.setMaximumSize(QSize(200, 28))
        font1 = QFont()
        font1.setPointSize(10)
        self.comboBox_attribution_type.setFont(font1)

        self.gridLayout_8.addWidget(self.comboBox_attribution_type, 0, 3, 1, 1)

        self.label_unit_5 = QLabel(self.frame_6)
        self.label_unit_5.setObjectName(u"label_unit_5")
        self.label_unit_5.setMinimumSize(QSize(36, 28))
        self.label_unit_5.setMaximumSize(QSize(36, 28))
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        self.label_unit_5.setFont(font2)
        self.label_unit_5.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_unit_5, 3, 3, 1, 1)

        self.label_diameter_3 = QLabel(self.frame_6)
        self.label_diameter_3.setObjectName(u"label_diameter_3")
        self.label_diameter_3.setMinimumSize(QSize(150, 28))
        self.label_diameter_3.setMaximumSize(QSize(150, 28))
        self.label_diameter_3.setFont(font2)
        self.label_diameter_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_diameter_3, 3, 1, 1, 1)

        self.lineEdit_center_coordinates = QLineEdit(self.frame_6)
        self.lineEdit_center_coordinates.setObjectName(u"lineEdit_center_coordinates")
        self.lineEdit_center_coordinates.setMinimumSize(QSize(200, 28))
        self.lineEdit_center_coordinates.setMaximumSize(QSize(200, 28))
        self.lineEdit_center_coordinates.setFont(font2)
        self.lineEdit_center_coordinates.setAlignment(Qt.AlignCenter)

        self.gridLayout_8.addWidget(self.lineEdit_center_coordinates, 3, 2, 1, 1)

        self.label_selection_type_2 = QLabel(self.frame_6)
        self.label_selection_type_2.setObjectName(u"label_selection_type_2")
        self.label_selection_type_2.setMinimumSize(QSize(150, 28))
        self.label_selection_type_2.setMaximumSize(QSize(150, 28))
        self.label_selection_type_2.setFont(font2)
        self.label_selection_type_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_selection_type_2, 4, 1, 1, 1)

        self.label_12 = QLabel(self.frame_6)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setMinimumSize(QSize(150, 28))
        self.label_12.setMaximumSize(QSize(150, 28))
        font3 = QFont()
        font3.setFamilies([u"MS Shell Dlg 2"])
        font3.setPointSize(10)
        font3.setBold(False)
        self.label_12.setFont(font3)
        self.label_12.setTextFormat(Qt.AutoText)
        self.label_12.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_12, 0, 1, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_7, 0, 0, 1, 1)

        self.comboBox_filter_type = QComboBox(self.frame_6)
        self.comboBox_filter_type.addItem("")
        self.comboBox_filter_type.addItem("")
        self.comboBox_filter_type.setObjectName(u"comboBox_filter_type")
        self.comboBox_filter_type.setMinimumSize(QSize(200, 26))
        self.comboBox_filter_type.setMaximumSize(QSize(200, 26))
        self.comboBox_filter_type.setFont(font1)

        self.gridLayout_8.addWidget(self.comboBox_filter_type, 2, 2, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_6, 0, 6, 1, 1)

        self.lineEdit_selection_id = QLineEdit(self.frame_6)
        self.lineEdit_selection_id.setObjectName(u"lineEdit_selection_id")
        self.lineEdit_selection_id.setEnabled(True)
        self.lineEdit_selection_id.setMinimumSize(QSize(200, 28))
        self.lineEdit_selection_id.setMaximumSize(QSize(200, 28))
        self.lineEdit_selection_id.setFont(font1)
        self.lineEdit_selection_id.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_selection_id.setAlignment(Qt.AlignCenter)

        self.gridLayout_8.addWidget(self.lineEdit_selection_id, 0, 2, 1, 1)

        self.label_selection_type_5 = QLabel(self.frame_6)
        self.label_selection_type_5.setObjectName(u"label_selection_type_5")
        self.label_selection_type_5.setMinimumSize(QSize(150, 26))
        self.label_selection_type_5.setMaximumSize(QSize(150, 26))
        self.label_selection_type_5.setFont(font2)
        self.label_selection_type_5.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_selection_type_5, 2, 1, 1, 1)

        self.doubleSpinBox_selection_radius = QDoubleSpinBox(self.frame_6)
        self.doubleSpinBox_selection_radius.setObjectName(u"doubleSpinBox_selection_radius")
        self.doubleSpinBox_selection_radius.setMinimumSize(QSize(200, 28))
        self.doubleSpinBox_selection_radius.setMaximumSize(QSize(200, 28))
        self.doubleSpinBox_selection_radius.setFont(font1)
        self.doubleSpinBox_selection_radius.setAlignment(Qt.AlignCenter)
        self.doubleSpinBox_selection_radius.setDecimals(3)
        self.doubleSpinBox_selection_radius.setMinimum(0.002000000000000)
        self.doubleSpinBox_selection_radius.setMaximum(10000.000000000000000)
        self.doubleSpinBox_selection_radius.setSingleStep(0.005000000000000)
        self.doubleSpinBox_selection_radius.setValue(0.050000000000000)

        self.gridLayout_8.addWidget(self.doubleSpinBox_selection_radius, 4, 2, 1, 1)

        self.pushButton_selection_info = QPushButton(self.frame_6)
        self.pushButton_selection_info.setObjectName(u"pushButton_selection_info")
        self.pushButton_selection_info.setMinimumSize(QSize(200, 28))
        self.pushButton_selection_info.setMaximumSize(QSize(200, 28))
        self.pushButton_selection_info.setFont(font2)
        self.pushButton_selection_info.setStyleSheet(u"")
        self.pushButton_selection_info.setAutoDefault(False)

        self.gridLayout_8.addWidget(self.pushButton_selection_info, 5, 2, 1, 1)

        self.label_unit = QLabel(self.frame_6)
        self.label_unit.setObjectName(u"label_unit")
        self.label_unit.setMinimumSize(QSize(36, 28))
        self.label_unit.setMaximumSize(QSize(36, 28))
        self.label_unit.setFont(font2)
        self.label_unit.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_unit, 4, 3, 1, 1)


        self.gridLayout_5.addWidget(self.frame_6, 0, 0, 1, 1)

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
        self.frame_4.setFrameShape(QFrame.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.gridLayout_7 = QGridLayout(self.frame_4)
        self.gridLayout_7.setSpacing(6)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(6, 6, 6, 6)
        self.label_2 = QLabel(self.frame_4)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(120, 0))
        self.label_2.setMaximumSize(QSize(132, 16777215))
        self.label_2.setFont(font1)
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_2, 2, 1, 1, 1)

        self.label_5 = QLabel(self.frame_4)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(120, 0))
        self.label_5.setMaximumSize(QSize(132, 16777215))
        self.label_5.setFont(font1)
        self.label_5.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

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

        self.label_18 = QLabel(self.frame_4)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setMinimumSize(QSize(40, 0))
        self.label_18.setMaximumSize(QSize(40, 16777215))
        self.label_18.setFont(font1)

        self.gridLayout_7.addWidget(self.label_18, 4, 5, 1, 1)

        self.label_3 = QLabel(self.frame_4)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(120, 0))
        self.label_3.setMaximumSize(QSize(132, 16777215))
        self.label_3.setFont(font1)
        self.label_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_3, 1, 1, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_3, 2, 0, 1, 1)

        self.label_6 = QLabel(self.frame_4)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(120, 0))
        self.label_6.setMaximumSize(QSize(132, 16777215))
        self.label_6.setFont(font1)
        self.label_6.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_6, 0, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_2, 2, 6, 1, 1)

        self.lineEdit_area_rectangular = QLineEdit(self.frame_4)
        self.lineEdit_area_rectangular.setObjectName(u"lineEdit_area_rectangular")
        self.lineEdit_area_rectangular.setEnabled(False)
        self.lineEdit_area_rectangular.setMinimumSize(QSize(0, 28))
        self.lineEdit_area_rectangular.setMaximumSize(QSize(200, 28))
        self.lineEdit_area_rectangular.setFont(font1)
        self.lineEdit_area_rectangular.setAlignment(Qt.AlignCenter)

        self.gridLayout_7.addWidget(self.lineEdit_area_rectangular, 4, 3, 1, 1)

        self.lineEdit_width_rectangular = QLineEdit(self.frame_4)
        self.lineEdit_width_rectangular.setObjectName(u"lineEdit_width_rectangular")
        self.lineEdit_width_rectangular.setMinimumSize(QSize(0, 28))
        self.lineEdit_width_rectangular.setMaximumSize(QSize(200, 28))
        self.lineEdit_width_rectangular.setFont(font1)
        self.lineEdit_width_rectangular.setAlignment(Qt.AlignCenter)

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

        self.lineEdit_height_rectangular = QLineEdit(self.frame_4)
        self.lineEdit_height_rectangular.setObjectName(u"lineEdit_height_rectangular")
        self.lineEdit_height_rectangular.setMinimumSize(QSize(0, 28))
        self.lineEdit_height_rectangular.setMaximumSize(QSize(200, 28))
        self.lineEdit_height_rectangular.setFont(font1)
        self.lineEdit_height_rectangular.setAlignment(Qt.AlignCenter)

        self.gridLayout_7.addWidget(self.lineEdit_height_rectangular, 1, 3, 1, 1)

        self.label_11 = QLabel(self.frame_4)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMinimumSize(QSize(120, 0))
        self.label_11.setMaximumSize(QSize(132, 16777215))
        self.label_11.setFont(font1)
        self.label_11.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_11, 5, 1, 1, 1)

        self.spinBox_number_of_terms = QSpinBox(self.frame_4)
        self.spinBox_number_of_terms.setObjectName(u"spinBox_number_of_terms")
        self.spinBox_number_of_terms.setMinimumSize(QSize(0, 28))
        self.spinBox_number_of_terms.setMaximumSize(QSize(16777215, 28))
        self.spinBox_number_of_terms.setFont(font1)
        self.spinBox_number_of_terms.setAlignment(Qt.AlignCenter)
        self.spinBox_number_of_terms.setMinimum(1)
        self.spinBox_number_of_terms.setMaximum(1000)
        self.spinBox_number_of_terms.setSingleStep(5)
        self.spinBox_number_of_terms.setValue(200)

        self.gridLayout_7.addWidget(self.spinBox_number_of_terms, 5, 3, 1, 1)


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
        self.frame_5.setFrameShape(QFrame.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Raised)
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
        self.lineEdit_area_circular.setAlignment(Qt.AlignCenter)

        self.gridLayout_9.addWidget(self.lineEdit_area_circular, 3, 3, 1, 1)

        self.label_19 = QLabel(self.frame_5)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setMinimumSize(QSize(40, 0))
        self.label_19.setMaximumSize(QSize(40, 16777215))
        self.label_19.setFont(font1)

        self.gridLayout_9.addWidget(self.label_19, 3, 5, 1, 1)

        self.label_7 = QLabel(self.frame_5)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(120, 0))
        self.label_7.setMaximumSize(QSize(132, 16777215))
        self.label_7.setFont(font1)
        self.label_7.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_9.addWidget(self.label_7, 3, 1, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer_4, 1, 0, 1, 1)

        self.label_8 = QLabel(self.frame_5)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMinimumSize(QSize(120, 0))
        self.label_8.setMaximumSize(QSize(132, 16777215))
        self.label_8.setFont(font1)
        self.label_8.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_9.addWidget(self.label_8, 1, 1, 1, 1)

        self.lineEdit_radius_circular = QLineEdit(self.frame_5)
        self.lineEdit_radius_circular.setObjectName(u"lineEdit_radius_circular")
        self.lineEdit_radius_circular.setEnabled(False)
        self.lineEdit_radius_circular.setMinimumSize(QSize(0, 28))
        self.lineEdit_radius_circular.setMaximumSize(QSize(200, 28))
        self.lineEdit_radius_circular.setFont(font1)
        self.lineEdit_radius_circular.setAlignment(Qt.AlignCenter)

        self.gridLayout_9.addWidget(self.lineEdit_radius_circular, 2, 3, 1, 1)

        self.label_10 = QLabel(self.frame_5)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(120, 0))
        self.label_10.setMaximumSize(QSize(132, 16777215))
        self.label_10.setFont(font1)
        self.label_10.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_9.addWidget(self.label_10, 2, 1, 1, 1)

        self.lineEdit_diameter_circular = QLineEdit(self.frame_5)
        self.lineEdit_diameter_circular.setObjectName(u"lineEdit_diameter_circular")
        self.lineEdit_diameter_circular.setMinimumSize(QSize(0, 28))
        self.lineEdit_diameter_circular.setMaximumSize(QSize(200, 28))
        self.lineEdit_diameter_circular.setFont(font1)
        self.lineEdit_diameter_circular.setAlignment(Qt.AlignCenter)

        self.gridLayout_9.addWidget(self.lineEdit_diameter_circular, 1, 3, 1, 1)

        self.label_22 = QLabel(self.frame_5)
        self.label_22.setObjectName(u"label_22")
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
        self.label_9.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_9.addWidget(self.label_9, 0, 1, 1, 1)


        self.gridLayout_17.addWidget(self.frame_5, 1, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_circular, "")
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
        font4 = QFont()
        font4.setFamilies([u"MS Shell Dlg 2"])
        font4.setPointSize(10)
        font4.setItalic(False)
        self.treeWidget_viscous_thermal_model.setFont(font4)
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
        self.frame_3.setFrameShape(QFrame.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.gridLayout_15 = QGridLayout(self.frame_3)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.gridLayout_15.setHorizontalSpacing(12)
        self.gridLayout_15.setContentsMargins(4, 4, 4, 4)
        self.pushButton_reset = QPushButton(self.frame_3)
        self.pushButton_reset.setObjectName(u"pushButton_reset")
        self.pushButton_reset.setMinimumSize(QSize(100, 28))
        self.pushButton_reset.setMaximumSize(QSize(100, 28))
        self.pushButton_reset.setFont(font2)
        self.pushButton_reset.setStyleSheet(u"")

        self.gridLayout_15.addWidget(self.pushButton_reset, 0, 0, 1, 1)

        self.pushButton_remove = QPushButton(self.frame_3)
        self.pushButton_remove.setObjectName(u"pushButton_remove")
        self.pushButton_remove.setMinimumSize(QSize(100, 28))
        self.pushButton_remove.setMaximumSize(QSize(100, 28))
        self.pushButton_remove.setFont(font2)
        self.pushButton_remove.setStyleSheet(u"")

        self.gridLayout_15.addWidget(self.pushButton_remove, 0, 1, 1, 1)


        self.gridLayout_16.addWidget(self.frame_3, 1, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_list, "")

        self.gridLayout_5.addWidget(self.tabWidget_main, 1, 0, 1, 1)

        self.frame_fluid_info = QFrame(self.scrollAreaWidgetContents)
        self.frame_fluid_info.setObjectName(u"frame_fluid_info")
        self.frame_fluid_info.setMaximumSize(QSize(16777215, 160))
        self.frame_fluid_info.setFrameShape(QFrame.NoFrame)
        self.frame_fluid_info.setFrameShadow(QFrame.Raised)
        self.gridLayout_18 = QGridLayout(self.frame_fluid_info)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.gridLayout_18.setContentsMargins(6, 6, 6, 6)
        self.label_36 = QLabel(self.frame_fluid_info)
        self.label_36.setObjectName(u"label_36")
        self.label_36.setMinimumSize(QSize(0, 28))
        self.label_36.setMaximumSize(QSize(16777215, 28))
        self.label_36.setFont(font1)
        self.label_36.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_18.addWidget(self.label_36, 1, 1, 1, 1)

        self.pushButton_get_fluid = QPushButton(self.frame_fluid_info)
        self.pushButton_get_fluid.setObjectName(u"pushButton_get_fluid")
        self.pushButton_get_fluid.setMinimumSize(QSize(72, 28))
        self.pushButton_get_fluid.setMaximumSize(QSize(72, 28))
        self.pushButton_get_fluid.setFont(font1)
        self.pushButton_get_fluid.setAutoDefault(False)

        self.gridLayout_18.addWidget(self.pushButton_get_fluid, 0, 3, 1, 1)

        self.lineEdit_fluid_density = QLineEdit(self.frame_fluid_info)
        self.lineEdit_fluid_density.setObjectName(u"lineEdit_fluid_density")
        self.lineEdit_fluid_density.setEnabled(False)
        self.lineEdit_fluid_density.setMinimumSize(QSize(100, 28))
        self.lineEdit_fluid_density.setMaximumSize(QSize(100, 28))
        self.lineEdit_fluid_density.setFont(font1)
        self.lineEdit_fluid_density.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_fluid_density.setAlignment(Qt.AlignCenter)

        self.gridLayout_18.addWidget(self.lineEdit_fluid_density, 1, 2, 1, 1)

        self.lineEdit_selected_fluid = QLineEdit(self.frame_fluid_info)
        self.lineEdit_selected_fluid.setObjectName(u"lineEdit_selected_fluid")
        self.lineEdit_selected_fluid.setEnabled(False)
        self.lineEdit_selected_fluid.setMinimumSize(QSize(100, 28))
        self.lineEdit_selected_fluid.setMaximumSize(QSize(100, 28))
        self.lineEdit_selected_fluid.setFont(font1)
        self.lineEdit_selected_fluid.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_selected_fluid.setAlignment(Qt.AlignCenter)

        self.gridLayout_18.addWidget(self.lineEdit_selected_fluid, 0, 2, 1, 1)

        self.lineEdit_speed_of_sound = QLineEdit(self.frame_fluid_info)
        self.lineEdit_speed_of_sound.setObjectName(u"lineEdit_speed_of_sound")
        self.lineEdit_speed_of_sound.setEnabled(False)
        self.lineEdit_speed_of_sound.setMinimumSize(QSize(100, 28))
        self.lineEdit_speed_of_sound.setMaximumSize(QSize(100, 28))
        self.lineEdit_speed_of_sound.setFont(font1)
        self.lineEdit_speed_of_sound.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_speed_of_sound.setAlignment(Qt.AlignCenter)

        self.gridLayout_18.addWidget(self.lineEdit_speed_of_sound, 2, 2, 1, 1)

        self.label_47 = QLabel(self.frame_fluid_info)
        self.label_47.setObjectName(u"label_47")
        self.label_47.setMinimumSize(QSize(0, 28))
        self.label_47.setMaximumSize(QSize(16777215, 28))
        self.label_47.setFont(font1)
        self.label_47.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_18.addWidget(self.label_47, 2, 1, 1, 1)

        self.label_31 = QLabel(self.frame_fluid_info)
        self.label_31.setObjectName(u"label_31")
        self.label_31.setMinimumSize(QSize(0, 28))
        self.label_31.setMaximumSize(QSize(16777215, 28))
        self.label_31.setFont(font1)
        self.label_31.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_18.addWidget(self.label_31, 0, 1, 1, 1)

        self.label_48 = QLabel(self.frame_fluid_info)
        self.label_48.setObjectName(u"label_48")
        self.label_48.setMinimumSize(QSize(0, 28))
        self.label_48.setMaximumSize(QSize(16777215, 28))
        self.label_48.setFont(font1)
        self.label_48.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_18.addWidget(self.label_48, 1, 3, 1, 1)

        self.label_49 = QLabel(self.frame_fluid_info)
        self.label_49.setObjectName(u"label_49")
        self.label_49.setMinimumSize(QSize(0, 28))
        self.label_49.setMaximumSize(QSize(16777215, 28))
        self.label_49.setFont(font1)
        self.label_49.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_18.addWidget(self.label_49, 2, 3, 1, 1)

        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_18.addItem(self.horizontalSpacer_14, 0, 0, 1, 1)

        self.horizontalSpacer_18 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_18.addItem(self.horizontalSpacer_18, 0, 4, 1, 1)

        self.label_51 = QLabel(self.frame_fluid_info)
        self.label_51.setObjectName(u"label_51")
        self.label_51.setMinimumSize(QSize(0, 28))
        self.label_51.setMaximumSize(QSize(16777215, 28))
        self.label_51.setFont(font1)
        self.label_51.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_18.addWidget(self.label_51, 3, 1, 1, 1)

        self.doubleSpinBox_evaluated_depth = QDoubleSpinBox(self.frame_fluid_info)
        self.doubleSpinBox_evaluated_depth.setObjectName(u"doubleSpinBox_evaluated_depth")
        self.doubleSpinBox_evaluated_depth.setMinimumSize(QSize(100, 28))
        self.doubleSpinBox_evaluated_depth.setMaximumSize(QSize(100, 28))
        self.doubleSpinBox_evaluated_depth.setFont(font1)
        self.doubleSpinBox_evaluated_depth.setAlignment(Qt.AlignCenter)
        self.doubleSpinBox_evaluated_depth.setDecimals(4)
        self.doubleSpinBox_evaluated_depth.setMinimum(0.001000000000000)
        self.doubleSpinBox_evaluated_depth.setMaximum(100.000000000000000)
        self.doubleSpinBox_evaluated_depth.setSingleStep(0.050000000000000)
        self.doubleSpinBox_evaluated_depth.setValue(0.100000000000000)

        self.gridLayout_18.addWidget(self.doubleSpinBox_evaluated_depth, 3, 2, 1, 1)

        self.label_17 = QLabel(self.frame_fluid_info)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setFont(font1)
        self.label_17.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_18.addWidget(self.label_17, 3, 3, 1, 1)


        self.gridLayout_5.addWidget(self.frame_fluid_info, 2, 0, 1, 1)

        self.frame_plot_buttons = QFrame(self.scrollAreaWidgetContents)
        self.frame_plot_buttons.setObjectName(u"frame_plot_buttons")
        self.frame_plot_buttons.setMaximumSize(QSize(16777215, 48))
        self.frame_plot_buttons.setFrameShape(QFrame.NoFrame)
        self.frame_plot_buttons.setFrameShadow(QFrame.Raised)
        self.gridLayout_19 = QGridLayout(self.frame_plot_buttons)
        self.gridLayout_19.setObjectName(u"gridLayout_19")
        self.label_50 = QLabel(self.frame_plot_buttons)
        self.label_50.setObjectName(u"label_50")
        self.label_50.setMinimumSize(QSize(0, 28))
        self.label_50.setMaximumSize(QSize(16777215, 28))
        self.label_50.setFont(font1)
        self.label_50.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

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

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_3.addWidget(self.scrollArea, 1, 1, 1, 1)


        self.gridLayout.addWidget(self.frame_main, 1, 0, 1, 1)

        self.frame_bottom = QFrame(Dialog)
        self.frame_bottom.setObjectName(u"frame_bottom")
        self.frame_bottom.setMinimumSize(QSize(0, 48))
        self.frame_bottom.setMaximumSize(QSize(16777215, 48))
        self.frame_bottom.setFrameShape(QFrame.NoFrame)
        self.frame_bottom.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_bottom)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.pushButton_confirm = QPushButton(self.frame_bottom)
        self.pushButton_confirm.setObjectName(u"pushButton_confirm")
        self.pushButton_confirm.setMinimumSize(QSize(100, 28))
        self.pushButton_confirm.setMaximumSize(QSize(100, 28))
        self.pushButton_confirm.setFont(font1)
        self.pushButton_confirm.setAutoDefault(False)

        self.gridLayout_4.addWidget(self.pushButton_confirm, 0, 1, 1, 1)

        self.pushButton_exit = QPushButton(self.frame_bottom)
        self.pushButton_exit.setObjectName(u"pushButton_exit")
        self.pushButton_exit.setMinimumSize(QSize(100, 28))
        self.pushButton_exit.setMaximumSize(QSize(100, 28))
        self.pushButton_exit.setFont(font1)
        self.pushButton_exit.setAutoDefault(False)

        self.gridLayout_4.addWidget(self.pushButton_exit, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_bottom, 2, 0, 1, 1)

        QWidget.setTabOrder(self.scrollArea, self.comboBox_attribution_type)
        QWidget.setTabOrder(self.comboBox_attribution_type, self.comboBox_filter_type)
        QWidget.setTabOrder(self.comboBox_filter_type, self.lineEdit_center_coordinates)
        QWidget.setTabOrder(self.lineEdit_center_coordinates, self.doubleSpinBox_selection_radius)
        QWidget.setTabOrder(self.doubleSpinBox_selection_radius, self.pushButton_selection_info)
        QWidget.setTabOrder(self.pushButton_selection_info, self.tabWidget_main)
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
        QWidget.setTabOrder(self.pushButton_plot_data, self.pushButton_confirm)
        QWidget.setTabOrder(self.pushButton_confirm, self.pushButton_exit)

        self.retranslateUi(Dialog)

        self.tabWidget_main.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Vibra", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Viscous-thermal loss models", None))
        self.comboBox_attribution_type.setItemText(0, QCoreApplication.translate("Dialog", u" All bodies", None))
        self.comboBox_attribution_type.setItemText(1, QCoreApplication.translate("Dialog", u" Selected bodies", None))
        self.comboBox_attribution_type.setItemText(2, QCoreApplication.translate("Dialog", u" Sphere (multiple)", None))
        self.comboBox_attribution_type.setItemText(3, QCoreApplication.translate("Dialog", u" Sphere (averaged)", None))

        self.label_unit_5.setText(QCoreApplication.translate("Dialog", u" [m]", None))
        self.label_diameter_3.setText(QCoreApplication.translate("Dialog", u"Center coords.: ", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_center_coordinates.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>The average coordinates center of selected surfaces in meters.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_center_coordinates.setText("")
        self.label_selection_type_2.setText(QCoreApplication.translate("Dialog", u"Selection radius: ", None))
        self.label_12.setText(QCoreApplication.translate("Dialog", u"Selection ID:", None))
        self.comboBox_filter_type.setItemText(0, QCoreApplication.translate("Dialog", u" Elements inside sphere", None))
        self.comboBox_filter_type.setItemText(1, QCoreApplication.translate("Dialog", u" Nodes inside sphere", None))

#if QT_CONFIG(tooltip)
        self.comboBox_filter_type.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Choose 'Elements inside sphere' to returns the elements list based on its coordinates center or 'Nodes inside sphere' to get elements connected with the nodes inside the selection sphere.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_selection_id.setText("")
        self.label_selection_type_5.setText(QCoreApplication.translate("Dialog", u"Filter type: ", None))
#if QT_CONFIG(tooltip)
        self.pushButton_selection_info.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Get the selection information</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_selection_info.setText(QCoreApplication.translate("Dialog", u"Get selection info", None))
        self.label_unit.setText(QCoreApplication.translate("Dialog", u" [m]", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Duct width (2a):", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"Duct area:", None))
        self.comboBox_section_type.setItemText(0, QCoreApplication.translate("Dialog", u" Rectangular", None))
        self.comboBox_section_type.setItemText(1, QCoreApplication.translate("Dialog", u" Quadrangular", None))
        self.comboBox_section_type.setItemText(2, QCoreApplication.translate("Dialog", u" Narrow slit", None))

        self.label_18.setText(QCoreApplication.translate("Dialog", u"[m\u00b2]", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Duct height (2b):", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"Section type:", None))
        self.label_16.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.label_15.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.label_11.setText(QCoreApplication.translate("Dialog", u"Number of terms:", None))
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
        self.label_36.setText(QCoreApplication.translate("Dialog", u"Fluid density", None))
        self.pushButton_get_fluid.setText(QCoreApplication.translate("Dialog", u"Get fluid", None))
        self.lineEdit_fluid_density.setText("")
        self.lineEdit_selected_fluid.setText("")
        self.lineEdit_speed_of_sound.setText("")
        self.label_47.setText(QCoreApplication.translate("Dialog", u"Speed of sound:", None))
        self.label_31.setText(QCoreApplication.translate("Dialog", u"Selected fluid:", None))
        self.label_48.setText(QCoreApplication.translate("Dialog", u"[kg/m\u00b3]", None))
        self.label_49.setText(QCoreApplication.translate("Dialog", u"[m/s]", None))
        self.label_51.setText(QCoreApplication.translate("Dialog", u"Evaluated depth:", None))
        self.label_17.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.label_50.setText(QCoreApplication.translate("Dialog", u"Plot selector:", None))
        self.comboBox_plot_type.setItemText(0, QCoreApplication.translate("Dialog", u" Fluid density", None))
        self.comboBox_plot_type.setItemText(1, QCoreApplication.translate("Dialog", u" Speed of sound", None))
        self.comboBox_plot_type.setItemText(2, QCoreApplication.translate("Dialog", u" Surface impedance", None))
        self.comboBox_plot_type.setItemText(3, QCoreApplication.translate("Dialog", u" Absorption coefficient", None))

        self.pushButton_plot_data.setText(QCoreApplication.translate("Dialog", u"Plot data", None))
        self.pushButton_confirm.setText(QCoreApplication.translate("Dialog", u"Confirm", None))
        self.pushButton_exit.setText(QCoreApplication.translate("Dialog", u"Exit", None))
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
                                            - frame_6: QFrame
                                                - (Layout): QGridLayout
                                                        - comboBox_attribution_type: QComboBox
                                                        - label_unit_5: QLabel
                                                        - label_diameter_3: QLabel
                                                        - lineEdit_center_coordinates: QLineEdit
                                                        - label_selection_type_2: QLabel
                                                        - label_12: QLabel
                                                        - comboBox_filter_type: QComboBox
                                                        - lineEdit_selection_id: QLineEdit
                                                        - label_selection_type_5: QLabel
                                                        - doubleSpinBox_selection_radius: QDoubleSpinBox
                                                        - pushButton_selection_info: QPushButton
                                                        - label_unit: QLabel
                                            - tabWidget_main: QTabWidget
                                                - tab_rectangular: QWidget
                                                    - (Layout): QGridLayout
                                                            - frame_4: QFrame
                                                                - (Layout): QGridLayout
                                                                        - label_2: QLabel
                                                                        - label_5: QLabel
                                                                        - comboBox_section_type: QComboBox
                                                                        - label_18: QLabel
                                                                        - label_3: QLabel
                                                                        - label_6: QLabel
                                                                        - lineEdit_area_rectangular: QLineEdit
                                                                        - lineEdit_width_rectangular: QLineEdit
                                                                        - label_16: QLabel
                                                                        - label_15: QLabel
                                                                        - lineEdit_height_rectangular: QLineEdit
                                                                        - label_11: QLabel
                                                                        - spinBox_number_of_terms: QSpinBox
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
                                                - tab_list: QWidget
                                                    - (Layout): QGridLayout
                                                            - treeWidget_viscous_thermal_model: QTreeWidget
                                                            - frame_3: QFrame
                                                                - (Layout): QGridLayout
                                                                        - pushButton_reset: QPushButton
                                                                        - pushButton_remove: QPushButton
                                            - frame_fluid_info: QFrame
                                                - (Layout): QGridLayout
                                                        - label_36: QLabel
                                                        - pushButton_get_fluid: QPushButton
                                                        - lineEdit_fluid_density: QLineEdit
                                                        - lineEdit_selected_fluid: QLineEdit
                                                        - lineEdit_speed_of_sound: QLineEdit
                                                        - label_47: QLabel
                                                        - label_31: QLabel
                                                        - label_48: QLabel
                                                        - label_49: QLabel
                                                        - label_51: QLabel
                                                        - doubleSpinBox_evaluated_depth: QDoubleSpinBox
                                                        - label_17: QLabel
                                            - frame_plot_buttons: QFrame
                                                - (Layout): QGridLayout
                                                        - label_50: QLabel
                                                        - comboBox_plot_type: QComboBox
                                                        - pushButton_plot_data: QPushButton
                - frame_bottom: QFrame
                    - (Layout): QGridLayout
                            - pushButton_confirm: QPushButton
                            - pushButton_exit: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
