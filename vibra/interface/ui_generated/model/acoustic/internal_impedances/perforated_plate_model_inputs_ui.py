# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'perforated_plate_model_inputs.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFrame,
    QGridLayout, QHeaderView, QLabel, QLineEdit,
    QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
    QTabWidget, QTableWidget, QTableWidgetItem, QTreeWidget,
    QTreeWidgetItem, QWidget)

from vibra.interface.formatters.icons import Icon

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(576, 603)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setVerticalSpacing(4)
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.Box)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.frame)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(4, 4, 4, 4)
        self.frame_6 = QFrame(self.frame)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setMinimumSize(QSize(400, 48))
        self.frame_6.setMaximumSize(QSize(16777215, 48))
        self.frame_6.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_6.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_6.setLineWidth(1)
        self.gridLayout_8 = QGridLayout(self.frame_6)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(6, 6, 6, 6)
        self.label_selection_A = QLabel(self.frame_6)
        self.label_selection_A.setObjectName(u"label_selection_A")
        self.label_selection_A.setMinimumSize(QSize(140, 28))
        self.label_selection_A.setMaximumSize(QSize(140, 28))
        font = QFont()
        font.setFamilies([u"MS Shell Dlg 2"])
        font.setPointSize(10)
        font.setBold(False)
        self.label_selection_A.setFont(font)
        self.label_selection_A.setTextFormat(Qt.TextFormat.AutoText)
        self.label_selection_A.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_selection_A, 0, 1, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_6, 0, 4, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_7, 0, 0, 1, 1)

        self.lineEdit_selection_id = QLineEdit(self.frame_6)
        self.lineEdit_selection_id.setObjectName(u"lineEdit_selection_id")
        self.lineEdit_selection_id.setEnabled(True)
        self.lineEdit_selection_id.setMinimumSize(QSize(160, 28))
        self.lineEdit_selection_id.setMaximumSize(QSize(160, 28))
        font1 = QFont()
        font1.setPointSize(10)
        self.lineEdit_selection_id.setFont(font1)
        self.lineEdit_selection_id.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.lineEdit_selection_id.setStyleSheet(u"")
        self.lineEdit_selection_id.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_8.addWidget(self.lineEdit_selection_id, 0, 2, 1, 2)


        self.gridLayout_3.addWidget(self.frame_6, 0, 0, 1, 1)

        self.tabWidget_main = QTabWidget(self.frame)
        self.tabWidget_main.setObjectName(u"tabWidget_main")
        self.tabWidget_main.setMaximumSize(QSize(16777215, 16777215))
        self.tabWidget_main.setFont(font1)
        self.tab_setup = QWidget()
        self.tab_setup.setObjectName(u"tab_setup")
        self.gridLayout_5 = QGridLayout(self.tab_setup)
        self.gridLayout_5.setSpacing(4)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(4, 4, 4, 4)
        self.tabWidget_perforated_plate_models = QTabWidget(self.tab_setup)
        self.tabWidget_perforated_plate_models.setObjectName(u"tabWidget_perforated_plate_models")
        self.tabWidget_perforated_plate_models.setMinimumSize(QSize(0, 80))
        self.tab_circular_holes_setup = QWidget()
        self.tab_circular_holes_setup.setObjectName(u"tab_circular_holes_setup")
        self.gridLayout_6 = QGridLayout(self.tab_circular_holes_setup)
        self.gridLayout_6.setSpacing(4)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(4, 4, 4, 4)
        self.scrollArea = QScrollArea(self.tab_circular_holes_setup)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 511, 592))
        self.gridLayout_12 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setContentsMargins(4, 4, 4, 4)
        self.frame_plot_buttons = QFrame(self.scrollAreaWidgetContents)
        self.frame_plot_buttons.setObjectName(u"frame_plot_buttons")
        self.frame_plot_buttons.setMaximumSize(QSize(16777215, 48))
        self.frame_plot_buttons.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_plot_buttons.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_19 = QGridLayout(self.frame_plot_buttons)
        self.gridLayout_19.setObjectName(u"gridLayout_19")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_19.addItem(self.horizontalSpacer_5, 0, 4, 1, 1)

        self.comboBox_plot_type = QComboBox(self.frame_plot_buttons)
        self.comboBox_plot_type.addItem("")
        self.comboBox_plot_type.setObjectName(u"comboBox_plot_type")
        self.comboBox_plot_type.setMinimumSize(QSize(160, 28))
        self.comboBox_plot_type.setMaximumSize(QSize(200, 28))
        self.comboBox_plot_type.setFont(font1)

        self.gridLayout_19.addWidget(self.comboBox_plot_type, 0, 2, 1, 1)

        self.pushButton_plot_data = QPushButton(self.frame_plot_buttons)
        self.pushButton_plot_data.setObjectName(u"pushButton_plot_data")
        self.pushButton_plot_data.setMinimumSize(QSize(80, 28))
        self.pushButton_plot_data.setMaximumSize(QSize(220, 28))
        self.pushButton_plot_data.setFont(font1)
        self.pushButton_plot_data.setAutoDefault(False)

        self.gridLayout_19.addWidget(self.pushButton_plot_data, 0, 3, 1, 1)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_19.addItem(self.horizontalSpacer_9, 0, 0, 1, 1)

        self.label_18 = QLabel(self.frame_plot_buttons)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setMinimumSize(QSize(200, 0))
        self.label_18.setMaximumSize(QSize(200, 16777215))
        self.label_18.setFont(font1)
        self.label_18.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_19.addWidget(self.label_18, 0, 1, 1, 1)


        self.gridLayout_12.addWidget(self.frame_plot_buttons, 6, 0, 1, 1)

        self.frame_2 = QFrame(self.scrollAreaWidgetContents)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_7 = QGridLayout(self.frame_2)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.label_23 = QLabel(self.frame_2)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setMinimumSize(QSize(32, 0))
        self.label_23.setMaximumSize(QSize(32, 16777215))
        self.label_23.setFont(font1)

        self.gridLayout_7.addWidget(self.label_23, 0, 3, 1, 1)

        self.pushButton_load_path = QPushButton(self.frame_2)
        self.pushButton_load_path.setObjectName(u"pushButton_load_path")
        self.pushButton_load_path.setMinimumSize(QSize(32, 28))
        self.pushButton_load_path.setMaximumSize(QSize(32, 28))
        icon = Icon(u":/icons/document_search_blue.png")
        self.pushButton_load_path.setIcon(icon)
        self.pushButton_load_path.setIconSize(QSize(20, 20))
        self.pushButton_load_path.setAutoDefault(False)

        self.gridLayout_7.addWidget(self.pushButton_load_path, 4, 3, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_3, 0, 4, 1, 1)

        self.lineEdit_user_defined_transfer_impedance_path = QLineEdit(self.frame_2)
        self.lineEdit_user_defined_transfer_impedance_path.setObjectName(u"lineEdit_user_defined_transfer_impedance_path")
        self.lineEdit_user_defined_transfer_impedance_path.setEnabled(False)
        self.lineEdit_user_defined_transfer_impedance_path.setMinimumSize(QSize(200, 28))
        self.lineEdit_user_defined_transfer_impedance_path.setMaximumSize(QSize(200, 28))
        font2 = QFont()
        font2.setPointSize(8)
        self.lineEdit_user_defined_transfer_impedance_path.setFont(font2)
        self.lineEdit_user_defined_transfer_impedance_path.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_user_defined_transfer_impedance_path.setClearButtonEnabled(True)

        self.gridLayout_7.addWidget(self.lineEdit_user_defined_transfer_impedance_path, 4, 2, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_2, 0, 0, 1, 1)

        self.lineEdit_non_linear_correction_factor = QLineEdit(self.frame_2)
        self.lineEdit_non_linear_correction_factor.setObjectName(u"lineEdit_non_linear_correction_factor")
        self.lineEdit_non_linear_correction_factor.setEnabled(True)
        self.lineEdit_non_linear_correction_factor.setMinimumSize(QSize(200, 28))
        self.lineEdit_non_linear_correction_factor.setMaximumSize(QSize(200, 28))
        self.lineEdit_non_linear_correction_factor.setFont(font1)
        self.lineEdit_non_linear_correction_factor.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_non_linear_correction_factor.setClearButtonEnabled(True)

        self.gridLayout_7.addWidget(self.lineEdit_non_linear_correction_factor, 3, 2, 1, 1)

        self.lineEdit_non_linear_discharge_coefficient = QLineEdit(self.frame_2)
        self.lineEdit_non_linear_discharge_coefficient.setObjectName(u"lineEdit_non_linear_discharge_coefficient")
        self.lineEdit_non_linear_discharge_coefficient.setEnabled(True)
        self.lineEdit_non_linear_discharge_coefficient.setMinimumSize(QSize(200, 28))
        self.lineEdit_non_linear_discharge_coefficient.setMaximumSize(QSize(200, 28))
        self.lineEdit_non_linear_discharge_coefficient.setFont(font1)
        self.lineEdit_non_linear_discharge_coefficient.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_non_linear_discharge_coefficient.setClearButtonEnabled(True)

        self.gridLayout_7.addWidget(self.lineEdit_non_linear_discharge_coefficient, 2, 2, 1, 1)

        self.label_14 = QLabel(self.frame_2)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setMinimumSize(QSize(200, 0))
        self.label_14.setMaximumSize(QSize(200, 16777215))
        self.label_14.setFont(font1)
        self.label_14.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_14, 3, 1, 1, 1)

        self.comboBox_include_effects = QComboBox(self.frame_2)
        self.comboBox_include_effects.addItem("")
        self.comboBox_include_effects.addItem("")
        self.comboBox_include_effects.addItem("")
        self.comboBox_include_effects.addItem("")
        self.comboBox_include_effects.setObjectName(u"comboBox_include_effects")
        self.comboBox_include_effects.setMinimumSize(QSize(200, 28))
        self.comboBox_include_effects.setMaximumSize(QSize(200, 28))

        self.gridLayout_7.addWidget(self.comboBox_include_effects, 0, 2, 1, 1)

        self.label_11 = QLabel(self.frame_2)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMinimumSize(QSize(210, 0))
        self.label_11.setMaximumSize(QSize(210, 16777215))
        self.label_11.setFont(font1)
        self.label_11.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_11, 2, 1, 1, 1)

        self.label_15 = QLabel(self.frame_2)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setMinimumSize(QSize(200, 28))
        self.label_15.setMaximumSize(QSize(200, 28))
        self.label_15.setFont(font1)
        self.label_15.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_15, 0, 1, 1, 1)

        self.label_17 = QLabel(self.frame_2)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setMinimumSize(QSize(215, 28))
        self.label_17.setMaximumSize(QSize(215, 28))
        self.label_17.setFont(font1)
        self.label_17.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_17, 4, 1, 1, 1)


        self.gridLayout_12.addWidget(self.frame_2, 5, 0, 1, 1)

        self.frame_4 = QFrame(self.scrollAreaWidgetContents)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMaximumSize(QSize(16777215, 48))
        self.frame_4.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_11 = QGridLayout(self.frame_4)
        self.gridLayout_11.setSpacing(4)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setContentsMargins(4, 4, 4, 4)
        self.label_3 = QLabel(self.frame_4)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(340, 30))
        self.label_3.setMaximumSize(QSize(340, 30))
        self.label_3.setFrameShape(QFrame.Shape.Box)
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.label_3, 0, 0, 1, 1)


        self.gridLayout_12.addWidget(self.frame_4, 4, 0, 1, 1)

        self.frame_7 = QFrame(self.scrollAreaWidgetContents)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_7.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_9 = QGridLayout(self.frame_7)
        self.gridLayout_9.setSpacing(6)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(6, 6, 6, 6)
        self.label_8 = QLabel(self.frame_7)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMinimumSize(QSize(200, 0))
        self.label_8.setMaximumSize(QSize(200, 16777215))
        self.label_8.setFont(font1)
        self.label_8.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_9.addWidget(self.label_8, 2, 1, 1, 1)

        self.label_20 = QLabel(self.frame_7)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setMinimumSize(QSize(40, 0))
        self.label_20.setMaximumSize(QSize(40, 16777215))
        self.label_20.setFont(font1)

        self.gridLayout_9.addWidget(self.label_20, 5, 4, 1, 1)

        self.lineEdit_porosity = QLineEdit(self.frame_7)
        self.lineEdit_porosity.setObjectName(u"lineEdit_porosity")
        self.lineEdit_porosity.setEnabled(True)
        self.lineEdit_porosity.setMinimumSize(QSize(160, 28))
        self.lineEdit_porosity.setMaximumSize(QSize(200, 28))
        self.lineEdit_porosity.setFont(font1)
        self.lineEdit_porosity.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_porosity.setClearButtonEnabled(True)

        self.gridLayout_9.addWidget(self.lineEdit_porosity, 4, 3, 1, 1)

        self.label_21 = QLabel(self.frame_7)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setMinimumSize(QSize(40, 0))
        self.label_21.setMaximumSize(QSize(40, 16777215))
        self.label_21.setFont(font1)

        self.gridLayout_9.addWidget(self.label_21, 0, 4, 1, 1)

        self.label_19 = QLabel(self.frame_7)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setMinimumSize(QSize(40, 0))
        self.label_19.setMaximumSize(QSize(40, 16777215))
        self.label_19.setFont(font1)

        self.gridLayout_9.addWidget(self.label_19, 4, 4, 1, 1)

        self.label_7 = QLabel(self.frame_7)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(200, 0))
        self.label_7.setMaximumSize(QSize(200, 16777215))
        self.label_7.setFont(font1)
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_9.addWidget(self.label_7, 4, 1, 1, 1)

        self.lineEdit_linear_discharge_coefficient = QLineEdit(self.frame_7)
        self.lineEdit_linear_discharge_coefficient.setObjectName(u"lineEdit_linear_discharge_coefficient")
        self.lineEdit_linear_discharge_coefficient.setEnabled(True)
        self.lineEdit_linear_discharge_coefficient.setMinimumSize(QSize(160, 28))
        self.lineEdit_linear_discharge_coefficient.setMaximumSize(QSize(200, 28))
        self.lineEdit_linear_discharge_coefficient.setFont(font1)
        self.lineEdit_linear_discharge_coefficient.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_linear_discharge_coefficient.setClearButtonEnabled(True)

        self.gridLayout_9.addWidget(self.lineEdit_linear_discharge_coefficient, 5, 3, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer_8, 0, 0, 1, 1)

        self.lineEdit_hole_diameter = QLineEdit(self.frame_7)
        self.lineEdit_hole_diameter.setObjectName(u"lineEdit_hole_diameter")
        self.lineEdit_hole_diameter.setMinimumSize(QSize(160, 28))
        self.lineEdit_hole_diameter.setMaximumSize(QSize(200, 28))
        self.lineEdit_hole_diameter.setFont(font1)
        self.lineEdit_hole_diameter.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_hole_diameter.setClearButtonEnabled(True)

        self.gridLayout_9.addWidget(self.lineEdit_hole_diameter, 2, 3, 1, 1)

        self.label_10 = QLabel(self.frame_7)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(200, 0))
        self.label_10.setMaximumSize(QSize(200, 16777215))
        self.label_10.setFont(font1)
        self.label_10.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_9.addWidget(self.label_10, 5, 1, 1, 1)

        self.label_13 = QLabel(self.frame_7)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setMinimumSize(QSize(200, 0))
        self.label_13.setMaximumSize(QSize(200, 16777215))
        self.label_13.setFont(font1)
        self.label_13.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_9.addWidget(self.label_13, 0, 1, 1, 1)

        self.label_22 = QLabel(self.frame_7)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setMinimumSize(QSize(40, 0))
        self.label_22.setMaximumSize(QSize(40, 16777215))
        self.label_22.setFont(font1)

        self.gridLayout_9.addWidget(self.label_22, 2, 4, 1, 1)

        self.lineEdit_plate_thickness = QLineEdit(self.frame_7)
        self.lineEdit_plate_thickness.setObjectName(u"lineEdit_plate_thickness")
        self.lineEdit_plate_thickness.setEnabled(True)
        self.lineEdit_plate_thickness.setMinimumSize(QSize(160, 28))
        self.lineEdit_plate_thickness.setMaximumSize(QSize(200, 28))
        self.lineEdit_plate_thickness.setFont(font1)
        self.lineEdit_plate_thickness.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_plate_thickness.setClearButtonEnabled(True)

        self.gridLayout_9.addWidget(self.lineEdit_plate_thickness, 0, 3, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer, 0, 6, 1, 1)

        self.pushButton_clean_inputs = QPushButton(self.frame_7)
        self.pushButton_clean_inputs.setObjectName(u"pushButton_clean_inputs")
        self.pushButton_clean_inputs.setMinimumSize(QSize(36, 28))
        self.pushButton_clean_inputs.setMaximumSize(QSize(36, 28))
        icon1 = Icon(u":/icons/broom.png")
        self.pushButton_clean_inputs.setIcon(icon1)
        self.pushButton_clean_inputs.setIconSize(QSize(18, 18))
        self.pushButton_clean_inputs.setAutoDefault(False)

        self.gridLayout_9.addWidget(self.pushButton_clean_inputs, 0, 5, 1, 1)


        self.gridLayout_12.addWidget(self.frame_7, 3, 0, 1, 1)

        self.frame_fluid_info = QFrame(self.scrollAreaWidgetContents)
        self.frame_fluid_info.setObjectName(u"frame_fluid_info")
        self.frame_fluid_info.setMaximumSize(QSize(16777215, 160))
        self.frame_fluid_info.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_fluid_info.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_18 = QGridLayout(self.frame_fluid_info)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.gridLayout_18.setContentsMargins(6, 6, 6, 6)
        self.pushButton_get_fluid = QPushButton(self.frame_fluid_info)
        self.pushButton_get_fluid.setObjectName(u"pushButton_get_fluid")
        self.pushButton_get_fluid.setMinimumSize(QSize(80, 28))
        self.pushButton_get_fluid.setMaximumSize(QSize(80, 28))
        self.pushButton_get_fluid.setFont(font1)
        self.pushButton_get_fluid.setAutoDefault(False)

        self.gridLayout_18.addWidget(self.pushButton_get_fluid, 0, 3, 1, 1)

        self.label_36 = QLabel(self.frame_fluid_info)
        self.label_36.setObjectName(u"label_36")
        self.label_36.setMinimumSize(QSize(200, 28))
        self.label_36.setMaximumSize(QSize(200, 28))
        self.label_36.setFont(font1)
        self.label_36.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_18.addWidget(self.label_36, 2, 1, 1, 1)

        self.lineEdit_selected_fluid = QLineEdit(self.frame_fluid_info)
        self.lineEdit_selected_fluid.setObjectName(u"lineEdit_selected_fluid")
        self.lineEdit_selected_fluid.setEnabled(False)
        self.lineEdit_selected_fluid.setMinimumSize(QSize(160, 28))
        self.lineEdit_selected_fluid.setMaximumSize(QSize(200, 28))
        self.lineEdit_selected_fluid.setFont(font1)
        self.lineEdit_selected_fluid.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.lineEdit_selected_fluid.setStyleSheet(u"")
        self.lineEdit_selected_fluid.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_18.addWidget(self.lineEdit_selected_fluid, 0, 2, 1, 1)

        self.lineEdit_speed_of_sound = QLineEdit(self.frame_fluid_info)
        self.lineEdit_speed_of_sound.setObjectName(u"lineEdit_speed_of_sound")
        self.lineEdit_speed_of_sound.setEnabled(False)
        self.lineEdit_speed_of_sound.setMinimumSize(QSize(160, 28))
        self.lineEdit_speed_of_sound.setMaximumSize(QSize(200, 28))
        self.lineEdit_speed_of_sound.setFont(font1)
        self.lineEdit_speed_of_sound.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.lineEdit_speed_of_sound.setStyleSheet(u"")
        self.lineEdit_speed_of_sound.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_18.addWidget(self.lineEdit_speed_of_sound, 3, 2, 1, 1)

        self.lineEdit_fluid_density = QLineEdit(self.frame_fluid_info)
        self.lineEdit_fluid_density.setObjectName(u"lineEdit_fluid_density")
        self.lineEdit_fluid_density.setEnabled(False)
        self.lineEdit_fluid_density.setMinimumSize(QSize(160, 28))
        self.lineEdit_fluid_density.setMaximumSize(QSize(200, 28))
        self.lineEdit_fluid_density.setFont(font1)
        self.lineEdit_fluid_density.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.lineEdit_fluid_density.setStyleSheet(u"")
        self.lineEdit_fluid_density.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_18.addWidget(self.lineEdit_fluid_density, 2, 2, 1, 1)

        self.label_31 = QLabel(self.frame_fluid_info)
        self.label_31.setObjectName(u"label_31")
        self.label_31.setMinimumSize(QSize(200, 28))
        self.label_31.setMaximumSize(QSize(200, 28))
        self.label_31.setFont(font1)
        self.label_31.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_18.addWidget(self.label_31, 0, 1, 1, 1)

        self.label_48 = QLabel(self.frame_fluid_info)
        self.label_48.setObjectName(u"label_48")
        self.label_48.setMinimumSize(QSize(0, 28))
        self.label_48.setMaximumSize(QSize(16777215, 28))
        self.label_48.setFont(font1)
        self.label_48.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_18.addWidget(self.label_48, 2, 3, 1, 1)

        self.horizontalSpacer_18 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_18.addItem(self.horizontalSpacer_18, 0, 4, 1, 1)

        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_18.addItem(self.horizontalSpacer_14, 0, 0, 1, 1)

        self.label_47 = QLabel(self.frame_fluid_info)
        self.label_47.setObjectName(u"label_47")
        self.label_47.setMinimumSize(QSize(200, 28))
        self.label_47.setMaximumSize(QSize(200, 28))
        self.label_47.setFont(font1)
        self.label_47.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_18.addWidget(self.label_47, 3, 1, 1, 1)

        self.label_49 = QLabel(self.frame_fluid_info)
        self.label_49.setObjectName(u"label_49")
        self.label_49.setMinimumSize(QSize(0, 28))
        self.label_49.setMaximumSize(QSize(16777215, 28))
        self.label_49.setFont(font1)
        self.label_49.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_18.addWidget(self.label_49, 3, 3, 1, 1)

        self.label_37 = QLabel(self.frame_fluid_info)
        self.label_37.setObjectName(u"label_37")
        self.label_37.setMinimumSize(QSize(200, 28))
        self.label_37.setMaximumSize(QSize(200, 28))
        self.label_37.setFont(font1)
        self.label_37.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_18.addWidget(self.label_37, 1, 1, 1, 1)

        self.lineEdit_fluid_identifier = QLineEdit(self.frame_fluid_info)
        self.lineEdit_fluid_identifier.setObjectName(u"lineEdit_fluid_identifier")
        self.lineEdit_fluid_identifier.setEnabled(False)
        self.lineEdit_fluid_identifier.setMinimumSize(QSize(160, 28))
        self.lineEdit_fluid_identifier.setMaximumSize(QSize(200, 28))
        self.lineEdit_fluid_identifier.setFont(font1)
        self.lineEdit_fluid_identifier.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.lineEdit_fluid_identifier.setStyleSheet(u"")
        self.lineEdit_fluid_identifier.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_18.addWidget(self.lineEdit_fluid_identifier, 1, 2, 1, 1)


        self.gridLayout_12.addWidget(self.frame_fluid_info, 1, 0, 1, 1)

        self.frame_5 = QFrame(self.scrollAreaWidgetContents)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setMaximumSize(QSize(16777215, 48))
        self.frame_5.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_10 = QGridLayout(self.frame_5)
        self.gridLayout_10.setSpacing(4)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(4, 4, 4, 4)
        self.label_2 = QLabel(self.frame_5)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(340, 30))
        self.label_2.setMaximumSize(QSize(340, 30))
        self.label_2.setFrameShape(QFrame.Shape.Box)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_10.addWidget(self.label_2, 0, 0, 1, 1)


        self.gridLayout_12.addWidget(self.frame_5, 0, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_6.addWidget(self.scrollArea, 1, 0, 1, 1)

        self.tabWidget_perforated_plate_models.addTab(self.tab_circular_holes_setup, "")

        self.gridLayout_5.addWidget(self.tabWidget_perforated_plate_models, 0, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_setup, "")
        self.tab_edit = QWidget()
        self.tab_edit.setObjectName(u"tab_edit")
        self.gridLayout_13 = QGridLayout(self.tab_edit)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.edit_tabWidget = QTabWidget(self.tab_edit)
        self.edit_tabWidget.setObjectName(u"edit_tabWidget")
        self.tab_circular_holes_edit = QWidget()
        self.tab_circular_holes_edit.setObjectName(u"tab_circular_holes_edit")
        self.gridLayout_14 = QGridLayout(self.tab_circular_holes_edit)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.edit_tableWidget = QTableWidget(self.tab_circular_holes_edit)
        if (self.edit_tableWidget.rowCount() < 13):
            self.edit_tableWidget.setRowCount(13)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setTextAlignment(Qt.AlignCenter);
        self.edit_tableWidget.setVerticalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setTextAlignment(Qt.AlignCenter);
        self.edit_tableWidget.setVerticalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        __qtablewidgetitem2.setTextAlignment(Qt.AlignCenter);
        self.edit_tableWidget.setVerticalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        __qtablewidgetitem3.setTextAlignment(Qt.AlignCenter);
        self.edit_tableWidget.setVerticalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        __qtablewidgetitem4.setTextAlignment(Qt.AlignCenter);
        self.edit_tableWidget.setVerticalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        __qtablewidgetitem5.setTextAlignment(Qt.AlignCenter);
        self.edit_tableWidget.setVerticalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        __qtablewidgetitem6.setTextAlignment(Qt.AlignCenter);
        self.edit_tableWidget.setVerticalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        __qtablewidgetitem7.setTextAlignment(Qt.AlignCenter);
        self.edit_tableWidget.setVerticalHeaderItem(7, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        __qtablewidgetitem8.setTextAlignment(Qt.AlignCenter);
        self.edit_tableWidget.setVerticalHeaderItem(8, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        __qtablewidgetitem9.setTextAlignment(Qt.AlignCenter);
        self.edit_tableWidget.setVerticalHeaderItem(9, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        __qtablewidgetitem10.setTextAlignment(Qt.AlignCenter);
        self.edit_tableWidget.setVerticalHeaderItem(10, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        __qtablewidgetitem11.setTextAlignment(Qt.AlignCenter);
        self.edit_tableWidget.setVerticalHeaderItem(11, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        __qtablewidgetitem12.setTextAlignment(Qt.AlignCenter);
        self.edit_tableWidget.setVerticalHeaderItem(12, __qtablewidgetitem12)
        self.edit_tableWidget.setObjectName(u"edit_tableWidget")
        self.edit_tableWidget.horizontalHeader().setVisible(False)

        self.gridLayout_14.addWidget(self.edit_tableWidget, 0, 0, 1, 1)

        self.edit_tabWidget.addTab(self.tab_circular_holes_edit, "")

        self.gridLayout_13.addWidget(self.edit_tabWidget, 0, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_edit, "")
        self.tab_list = QWidget()
        self.tab_list.setObjectName(u"tab_list")
        self.gridLayout_16 = QGridLayout(self.tab_list)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.gridLayout_16.setContentsMargins(9, -1, -1, -1)
        self.treeWidget_perforated_plate_model = QTreeWidget(self.tab_list)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter);
        self.treeWidget_perforated_plate_model.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_perforated_plate_model.setObjectName(u"treeWidget_perforated_plate_model")
        self.treeWidget_perforated_plate_model.setMinimumSize(QSize(320, 100))
        self.treeWidget_perforated_plate_model.setMaximumSize(QSize(16777215, 240))
        font3 = QFont()
        font3.setFamilies([u"MS Shell Dlg 2"])
        font3.setPointSize(10)
        font3.setItalic(False)
        self.treeWidget_perforated_plate_model.setFont(font3)
        self.treeWidget_perforated_plate_model.setIndentation(1)
        self.treeWidget_perforated_plate_model.setHeaderHidden(False)
        self.treeWidget_perforated_plate_model.header().setHighlightSections(False)
        self.treeWidget_perforated_plate_model.header().setProperty(u"showSortIndicator", False)
        self.treeWidget_perforated_plate_model.header().setStretchLastSection(True)

        self.gridLayout_16.addWidget(self.treeWidget_perforated_plate_model, 0, 0, 1, 1)

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
        self.pushButton_reset.setAutoDefault(False)

        self.gridLayout_15.addWidget(self.pushButton_reset, 0, 0, 1, 1)

        self.pushButton_remove = QPushButton(self.frame_3)
        self.pushButton_remove.setObjectName(u"pushButton_remove")
        self.pushButton_remove.setMinimumSize(QSize(100, 28))
        self.pushButton_remove.setMaximumSize(QSize(100, 28))
        self.pushButton_remove.setFont(font4)
        self.pushButton_remove.setStyleSheet(u"")
        self.pushButton_remove.setAutoDefault(False)

        self.gridLayout_15.addWidget(self.pushButton_remove, 0, 1, 1, 1)


        self.gridLayout_16.addWidget(self.frame_3, 1, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_list, "")

        self.gridLayout_3.addWidget(self.tabWidget_main, 1, 0, 1, 1)


        self.gridLayout.addWidget(self.frame, 1, 0, 1, 1)

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
        font5 = QFont()
        font5.setPointSize(11)
        self.label.setFont(font5)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_top, 0, 0, 1, 1)

        self.frame_buttons = QFrame(Dialog)
        self.frame_buttons.setObjectName(u"frame_buttons")
        self.frame_buttons.setMinimumSize(QSize(0, 48))
        self.frame_buttons.setMaximumSize(QSize(16777215, 48))
        self.frame_buttons.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_buttons.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_17 = QGridLayout(self.frame_buttons)
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.gridLayout_17.setVerticalSpacing(0)
        self.gridLayout_17.setContentsMargins(6, 0, 6, 0)
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

        self.gridLayout_17.addWidget(self.pushButton_apply_and_close, 0, 3, 1, 1)

        self.pushButton_apply = QPushButton(self.frame_buttons)
        self.pushButton_apply.setObjectName(u"pushButton_apply")
        self.pushButton_apply.setMinimumSize(QSize(72, 30))
        self.pushButton_apply.setMaximumSize(QSize(72, 30))
        self.pushButton_apply.setFont(font6)
        self.pushButton_apply.setStyleSheet(u"")
        self.pushButton_apply.setAutoDefault(False)
        self.pushButton_apply.setFlat(False)

        self.gridLayout_17.addWidget(self.pushButton_apply, 0, 2, 1, 1)

        self.pushButton_cancel = QPushButton(self.frame_buttons)
        self.pushButton_cancel.setObjectName(u"pushButton_cancel")
        self.pushButton_cancel.setMinimumSize(QSize(72, 30))
        self.pushButton_cancel.setMaximumSize(QSize(72, 30))
        self.pushButton_cancel.setFont(font6)
        self.pushButton_cancel.setStyleSheet(u"")
        self.pushButton_cancel.setAutoDefault(False)
        self.pushButton_cancel.setFlat(False)

        self.gridLayout_17.addWidget(self.pushButton_cancel, 0, 0, 1, 1)

        self.horizontalSpacer_17 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_17.addItem(self.horizontalSpacer_17, 0, 1, 1, 1)


        self.gridLayout.addWidget(self.frame_buttons, 2, 0, 1, 1)


        self.retranslateUi(Dialog)

        self.tabWidget_main.setCurrentIndex(0)
        self.tabWidget_perforated_plate_models.setCurrentIndex(0)
        self.edit_tabWidget.setCurrentIndex(0)
        self.pushButton_apply_and_close.setDefault(False)
        self.pushButton_apply.setDefault(False)
        self.pushButton_cancel.setDefault(False)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Perforated plate model setup", None))
        self.label_selection_A.setText(QCoreApplication.translate("Dialog", u"Selected surfaces:", None))
        self.lineEdit_selection_id.setText("")
        self.comboBox_plot_type.setItemText(0, QCoreApplication.translate("Dialog", u"Acoustic impedance", None))

        self.pushButton_plot_data.setText(QCoreApplication.translate("Dialog", u"Plot data", None))
        self.label_18.setText(QCoreApplication.translate("Dialog", u"Plot selector:", None))
        self.label_23.setText("")
        self.pushButton_load_path.setText("")
#if QT_CONFIG(tooltip)
        self.lineEdit_user_defined_transfer_impedance_path.setToolTip(QCoreApplication.translate("Dialog", u"User-defined normalized transfer impedance table path", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_user_defined_transfer_impedance_path.setText("")
#if QT_CONFIG(tooltip)
        self.lineEdit_non_linear_correction_factor.setToolTip(QCoreApplication.translate("Dialog", u"Non-linear correction factor", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_non_linear_correction_factor.setText(QCoreApplication.translate("Dialog", u"1.00", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_non_linear_discharge_coefficient.setToolTip(QCoreApplication.translate("Dialog", u"Non-linear discharge coefficient", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_non_linear_discharge_coefficient.setText(QCoreApplication.translate("Dialog", u"0.76", None))
        self.label_14.setText(QCoreApplication.translate("Dialog", u"Non-linear correction factor:", None))
        self.comboBox_include_effects.setItemText(0, QCoreApplication.translate("Dialog", u"None", None))
        self.comboBox_include_effects.setItemText(1, QCoreApplication.translate("Dialog", u"Non-linear", None))
        self.comboBox_include_effects.setItemText(2, QCoreApplication.translate("Dialog", u"User-defined", None))
        self.comboBox_include_effects.setItemText(3, QCoreApplication.translate("Dialog", u"Non-linear + User-defined", None))

        self.label_11.setText(QCoreApplication.translate("Dialog", u"Non-linear discharge coefficient:", None))
        self.label_15.setText(QCoreApplication.translate("Dialog", u"Include effects:", None))
        self.label_17.setText(QCoreApplication.translate("Dialog", u"User-defined transfer impedance:", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Advanced options for perforated plate model", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"Hole diameter:", None))
        self.label_20.setText(QCoreApplication.translate("Dialog", u"[--]", None))
        self.lineEdit_porosity.setText(QCoreApplication.translate("Dialog", u"0.23", None))
        self.label_21.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.label_19.setText(QCoreApplication.translate("Dialog", u"[--]", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"Porosity:", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_linear_discharge_coefficient.setToolTip(QCoreApplication.translate("Dialog", u"Linear discharge coefficient", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_linear_discharge_coefficient.setText(QCoreApplication.translate("Dialog", u"1.00", None))
        self.lineEdit_hole_diameter.setText(QCoreApplication.translate("Dialog", u"0.005", None))
        self.label_10.setText(QCoreApplication.translate("Dialog", u"Linear discharge coefficient:", None))
        self.label_13.setText(QCoreApplication.translate("Dialog", u"Plate thickness:", None))
        self.label_22.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.lineEdit_plate_thickness.setText(QCoreApplication.translate("Dialog", u"0.003", None))
        self.pushButton_clean_inputs.setText("")
        self.pushButton_get_fluid.setText(QCoreApplication.translate("Dialog", u"Get fluid", None))
        self.label_36.setText(QCoreApplication.translate("Dialog", u"Fluid density", None))
        self.lineEdit_selected_fluid.setText("")
        self.lineEdit_speed_of_sound.setText("")
        self.lineEdit_fluid_density.setText("")
        self.label_31.setText(QCoreApplication.translate("Dialog", u"Selected fluid:", None))
        self.label_48.setText(QCoreApplication.translate("Dialog", u"[kg/m\u00b3]", None))
        self.label_47.setText(QCoreApplication.translate("Dialog", u"Speed of sound:", None))
        self.label_49.setText(QCoreApplication.translate("Dialog", u"[m/s]", None))
        self.label_37.setText(QCoreApplication.translate("Dialog", u"Fluid identifier:", None))
        self.lineEdit_fluid_identifier.setText("")
        self.label_2.setText(QCoreApplication.translate("Dialog", u"General options for perforate plate model", None))
        self.tabWidget_perforated_plate_models.setTabText(self.tabWidget_perforated_plate_models.indexOf(self.tab_circular_holes_setup), QCoreApplication.translate("Dialog", u"Circular holes", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_setup), QCoreApplication.translate("Dialog", u"Setup", None))
        ___qtablewidgetitem = self.edit_tableWidget.verticalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Dialog", u"Perforated Plate ID", None));
        ___qtablewidgetitem1 = self.edit_tableWidget.verticalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Dialog", u"Fluid", None));
        ___qtablewidgetitem2 = self.edit_tableWidget.verticalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Dialog", u"Fuid identifier", None));
        ___qtablewidgetitem3 = self.edit_tableWidget.verticalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Dialog", u"Fluid density", None));
        ___qtablewidgetitem4 = self.edit_tableWidget.verticalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Dialog", u"Speed of sound", None));
        ___qtablewidgetitem5 = self.edit_tableWidget.verticalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Dialog", u"Plate thickness", None));
        ___qtablewidgetitem6 = self.edit_tableWidget.verticalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("Dialog", u"Hole diameter", None));
        ___qtablewidgetitem7 = self.edit_tableWidget.verticalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("Dialog", u"Porosity", None));
        ___qtablewidgetitem8 = self.edit_tableWidget.verticalHeaderItem(8)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("Dialog", u"Linear discharge coefficient", None));
        ___qtablewidgetitem9 = self.edit_tableWidget.verticalHeaderItem(9)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("Dialog", u"Include effects", None));
        ___qtablewidgetitem10 = self.edit_tableWidget.verticalHeaderItem(10)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("Dialog", u"Non-linear discharge coefficient", None));
        ___qtablewidgetitem11 = self.edit_tableWidget.verticalHeaderItem(11)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("Dialog", u"Non-linear correction factor", None));
        ___qtablewidgetitem12 = self.edit_tableWidget.verticalHeaderItem(12)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("Dialog", u"User-defined transfer impedance file", None));
        self.edit_tabWidget.setTabText(self.edit_tabWidget.indexOf(self.tab_circular_holes_edit), QCoreApplication.translate("Dialog", u"Circular holes", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_edit), QCoreApplication.translate("Dialog", u"Edit", None))
        ___qtreewidgetitem = self.treeWidget_perforated_plate_model.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"Model ID", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Surfaces", None));
#if QT_CONFIG(tooltip)
        self.treeWidget_perforated_plate_model.setToolTip(QCoreApplication.translate("Dialog", u"Select a face to remove the previously attributed boundary condition.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_reset.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.pushButton_remove.setText(QCoreApplication.translate("Dialog", u"Remove", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_list), QCoreApplication.translate("Dialog", u"List", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Perforated plate model setup", None))
        self.pushButton_apply_and_close.setText(QCoreApplication.translate("Dialog", u"Ok", None))
        self.pushButton_apply.setText(QCoreApplication.translate("Dialog", u"Apply", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
    # retranslateUi



class PerforatedPlateModelInputs_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame: QFrame
                    - (Layout): QGridLayout
                            - frame_6: QFrame
                                - (Layout): QGridLayout
                                        - label_selection_A: QLabel
                                        - lineEdit_selection_id: QLineEdit
                            - tabWidget_main: QTabWidget
                                - tab_setup: QWidget
                                    - (Layout): QGridLayout
                                            - tabWidget_perforated_plate_models: QTabWidget
                                                - tab_circular_holes_setup: QWidget
                                                    - (Layout): QGridLayout
                                                            - scrollArea: QScrollArea
                                                                - scrollAreaWidgetContents: QWidget
                                                                    - (Layout): QGridLayout
                                                                            - frame_plot_buttons: QFrame
                                                                                - (Layout): QGridLayout
                                                                                        - comboBox_plot_type: QComboBox
                                                                                        - pushButton_plot_data: QPushButton
                                                                                        - label_18: QLabel
                                                                            - frame_2: QFrame
                                                                                - (Layout): QGridLayout
                                                                                        - label_23: QLabel
                                                                                        - pushButton_load_path: QPushButton
                                                                                        - lineEdit_user_defined_transfer_impedance_path: QLineEdit
                                                                                        - lineEdit_non_linear_correction_factor: QLineEdit
                                                                                        - lineEdit_non_linear_discharge_coefficient: QLineEdit
                                                                                        - label_14: QLabel
                                                                                        - comboBox_include_effects: QComboBox
                                                                                        - label_11: QLabel
                                                                                        - label_15: QLabel
                                                                                        - label_17: QLabel
                                                                            - frame_4: QFrame
                                                                                - (Layout): QGridLayout
                                                                                        - label_3: QLabel
                                                                            - frame_7: QFrame
                                                                                - (Layout): QGridLayout
                                                                                        - label_8: QLabel
                                                                                        - label_20: QLabel
                                                                                        - lineEdit_porosity: QLineEdit
                                                                                        - label_21: QLabel
                                                                                        - label_19: QLabel
                                                                                        - label_7: QLabel
                                                                                        - lineEdit_linear_discharge_coefficient: QLineEdit
                                                                                        - lineEdit_hole_diameter: QLineEdit
                                                                                        - label_10: QLabel
                                                                                        - label_13: QLabel
                                                                                        - label_22: QLabel
                                                                                        - lineEdit_plate_thickness: QLineEdit
                                                                                        - pushButton_clean_inputs: QPushButton
                                                                            - frame_fluid_info: QFrame
                                                                                - (Layout): QGridLayout
                                                                                        - pushButton_get_fluid: QPushButton
                                                                                        - label_36: QLabel
                                                                                        - lineEdit_selected_fluid: QLineEdit
                                                                                        - lineEdit_speed_of_sound: QLineEdit
                                                                                        - lineEdit_fluid_density: QLineEdit
                                                                                        - label_31: QLabel
                                                                                        - label_48: QLabel
                                                                                        - label_47: QLabel
                                                                                        - label_49: QLabel
                                                                                        - label_37: QLabel
                                                                                        - lineEdit_fluid_identifier: QLineEdit
                                                                            - frame_5: QFrame
                                                                                - (Layout): QGridLayout
                                                                                        - label_2: QLabel
                                - tab_edit: QWidget
                                    - (Layout): QGridLayout
                                            - edit_tabWidget: QTabWidget
                                                - tab_circular_holes_edit: QWidget
                                                    - (Layout): QGridLayout
                                                            - edit_tableWidget: QTableWidget
                                - tab_list: QWidget
                                    - (Layout): QGridLayout
                                            - treeWidget_perforated_plate_model: QTreeWidget
                                            - frame_3: QFrame
                                                - (Layout): QGridLayout
                                                        - pushButton_reset: QPushButton
                                                        - pushButton_remove: QPushButton
                - frame_top: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
                - frame_buttons: QFrame
                    - (Layout): QGridLayout
                            - pushButton_apply_and_close: QPushButton
                            - pushButton_apply: QPushButton
                            - pushButton_cancel: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
