# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'allowable_pulsations_for_reciprocating_compressor_inputs.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QGridLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QTabWidget, QWidget)

from vibra.interface.formatters.icons import Icon

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(408, 580)
        Form.setMinimumSize(QSize(0, 580))
        Form.setMaximumSize(QSize(16777215, 640))
        self.gridLayout_4 = QGridLayout(Form)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setVerticalSpacing(4)
        self.gridLayout_4.setContentsMargins(4, 4, 4, 4)
        self.frame_2 = QFrame(Form)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(0, 0))
        self.frame_2.setMaximumSize(QSize(520, 600))
        self.frame_2.setFrameShape(QFrame.Shape.Box)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_2)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(4, 4, 4, 4)
        self.frame_3 = QFrame(self.frame_2)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(0, 52))
        self.frame_3.setMaximumSize(QSize(16777215, 52))
        self.frame_3.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_47 = QGridLayout(self.frame_3)
        self.gridLayout_47.setSpacing(2)
        self.gridLayout_47.setObjectName(u"gridLayout_47")
        self.gridLayout_47.setContentsMargins(2, 2, 2, 2)
        self.pushButton_plot_data = QPushButton(self.frame_3)
        self.pushButton_plot_data.setObjectName(u"pushButton_plot_data")
        self.pushButton_plot_data.setMinimumSize(QSize(100, 32))
        self.pushButton_plot_data.setMaximumSize(QSize(100, 32))
        font = QFont()
        font.setPointSize(10)
        self.pushButton_plot_data.setFont(font)
        self.pushButton_plot_data.setStyleSheet(u"")
        self.pushButton_plot_data.setFlat(False)

        self.gridLayout_47.addWidget(self.pushButton_plot_data, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_3, 4, 0, 1, 1)

        self.frame_4 = QFrame(self.frame_2)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(0, 0))
        self.frame_4.setMaximumSize(QSize(16777215, 200))
        self.frame_4.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.frame_4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(6)
        self.gridLayout.setVerticalSpacing(4)
        self.gridLayout.setContentsMargins(2, 2, 2, 2)
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 0, 4, 1, 1)

        self.comboBox_selector_filter = QComboBox(self.frame_4)
        self.comboBox_selector_filter.addItem("")
        self.comboBox_selector_filter.addItem("")
        self.comboBox_selector_filter.addItem("")
        self.comboBox_selector_filter.addItem("")
        self.comboBox_selector_filter.setObjectName(u"comboBox_selector_filter")
        self.comboBox_selector_filter.setMinimumSize(QSize(130, 28))
        self.comboBox_selector_filter.setMaximumSize(QSize(130, 28))
        self.comboBox_selector_filter.setFont(font)
        self.comboBox_selector_filter.setStyleSheet(u"")

        self.gridLayout.addWidget(self.comboBox_selector_filter, 1, 2, 1, 1)

        self.pushButton_get_fluid = QPushButton(self.frame_4)
        self.pushButton_get_fluid.setObjectName(u"pushButton_get_fluid")
        self.pushButton_get_fluid.setMinimumSize(QSize(44, 0))
        self.pushButton_get_fluid.setMaximumSize(QSize(44, 28))
        self.pushButton_get_fluid.setFont(font)
        icon = Icon(u":/icons/get_fluid_blue.png")
        self.pushButton_get_fluid.setIcon(icon)
        self.pushButton_get_fluid.setIconSize(QSize(20, 20))

        self.gridLayout.addWidget(self.pushButton_get_fluid, 2, 3, 1, 1)

        self.label_31 = QLabel(self.frame_4)
        self.label_31.setObjectName(u"label_31")
        self.label_31.setMinimumSize(QSize(110, 0))
        self.label_31.setMaximumSize(QSize(110, 16777215))
        self.label_31.setFont(font)
        self.label_31.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_31, 2, 1, 1, 1)

        self.lineEdit_selected_fluid = QLineEdit(self.frame_4)
        self.lineEdit_selected_fluid.setObjectName(u"lineEdit_selected_fluid")
        self.lineEdit_selected_fluid.setEnabled(False)
        self.lineEdit_selected_fluid.setMinimumSize(QSize(130, 28))
        self.lineEdit_selected_fluid.setMaximumSize(QSize(130, 28))
        font1 = QFont()
        font1.setPointSize(8)
        self.lineEdit_selected_fluid.setFont(font1)
        self.lineEdit_selected_fluid.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.lineEdit_selected_fluid.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_selected_fluid, 2, 2, 1, 1)

        self.lineEdit_selection_id = QLineEdit(self.frame_4)
        self.lineEdit_selection_id.setObjectName(u"lineEdit_selection_id")
        self.lineEdit_selection_id.setMinimumSize(QSize(130, 28))
        self.lineEdit_selection_id.setMaximumSize(QSize(130, 28))
        self.lineEdit_selection_id.setFont(font)
        self.lineEdit_selection_id.setStyleSheet(u"")
        self.lineEdit_selection_id.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_selection_id, 0, 2, 1, 1)

        self.label_2 = QLabel(self.frame_4)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(110, 28))
        self.label_2.setMaximumSize(QSize(110, 28))
        self.label_2.setFont(font)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_2, 1, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.label_10 = QLabel(self.frame_4)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(110, 28))
        self.label_10.setMaximumSize(QSize(110, 28))
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        self.label_10.setFont(font2)
        self.label_10.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_10, 0, 1, 1, 1)

        self.pushButton_export_data = QPushButton(self.frame_4)
        self.pushButton_export_data.setObjectName(u"pushButton_export_data")
        self.pushButton_export_data.setMinimumSize(QSize(44, 28))
        self.pushButton_export_data.setMaximumSize(QSize(44, 28))
        font3 = QFont()
        font3.setFamilies([u"MS Shell Dlg 2"])
        font3.setPointSize(11)
        font3.setBold(True)
        font3.setItalic(False)
        self.pushButton_export_data.setFont(font3)
        self.pushButton_export_data.setStyleSheet(u"")
        icon1 = Icon(u":/icons/save_as.png")
        self.pushButton_export_data.setIcon(icon1)
        self.pushButton_export_data.setIconSize(QSize(20, 20))
        self.pushButton_export_data.setFlat(False)

        self.gridLayout.addWidget(self.pushButton_export_data, 0, 3, 1, 1)


        self.gridLayout_3.addWidget(self.frame_4, 0, 0, 1, 1)

        self.tabWidget_main = QTabWidget(self.frame_2)
        self.tabWidget_main.setObjectName(u"tabWidget_main")
        self.tabWidget_main.setFont(font)
        self.tab_unfiltered_criteria = QWidget()
        self.tab_unfiltered_criteria.setObjectName(u"tab_unfiltered_criteria")
        self.gridLayout_12 = QGridLayout(self.tab_unfiltered_criteria)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setVerticalSpacing(10)
        self.gridLayout_12.setContentsMargins(4, 4, 4, 4)
        self.frame_11 = QFrame(self.tab_unfiltered_criteria)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_11.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_11 = QGridLayout(self.frame_11)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.lineEdit_pressure_ratio = QLineEdit(self.frame_11)
        self.lineEdit_pressure_ratio.setObjectName(u"lineEdit_pressure_ratio")
        self.lineEdit_pressure_ratio.setEnabled(True)
        self.lineEdit_pressure_ratio.setMinimumSize(QSize(100, 28))
        self.lineEdit_pressure_ratio.setMaximumSize(QSize(100, 28))
        self.lineEdit_pressure_ratio.setFont(font)
        self.lineEdit_pressure_ratio.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.lineEdit_pressure_ratio.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.lineEdit_pressure_ratio, 0, 2, 1, 1)

        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_11.addItem(self.horizontalSpacer_14, 0, 4, 1, 1)

        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_11.addItem(self.horizontalSpacer_13, 0, 0, 1, 1)

        self.label_6 = QLabel(self.frame_11)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(30, 0))
        self.label_6.setMaximumSize(QSize(30, 16777215))
        self.label_6.setFont(font)
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_11.addWidget(self.label_6, 0, 3, 1, 1)

        self.label_8 = QLabel(self.frame_11)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMinimumSize(QSize(140, 0))
        self.label_8.setMaximumSize(QSize(140, 16777215))
        self.label_8.setFont(font)
        self.label_8.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_11.addWidget(self.label_8, 0, 1, 1, 1)

        self.label_9 = QLabel(self.frame_11)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMinimumSize(QSize(140, 0))
        self.label_9.setMaximumSize(QSize(140, 16777215))
        self.label_9.setFont(font)
        self.label_9.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_11.addWidget(self.label_9, 1, 1, 1, 1)

        self.lineEdit_unfiltered_criterion = QLineEdit(self.frame_11)
        self.lineEdit_unfiltered_criterion.setObjectName(u"lineEdit_unfiltered_criterion")
        self.lineEdit_unfiltered_criterion.setEnabled(False)
        self.lineEdit_unfiltered_criterion.setMinimumSize(QSize(100, 28))
        self.lineEdit_unfiltered_criterion.setMaximumSize(QSize(100, 28))
        self.lineEdit_unfiltered_criterion.setFont(font)
        self.lineEdit_unfiltered_criterion.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.lineEdit_unfiltered_criterion.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.lineEdit_unfiltered_criterion, 1, 2, 1, 1)

        self.label_7 = QLabel(self.frame_11)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(30, 0))
        self.label_7.setMaximumSize(QSize(30, 16777215))
        self.label_7.setFont(font)
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_11.addWidget(self.label_7, 1, 3, 1, 1)


        self.gridLayout_12.addWidget(self.frame_11, 2, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_12.addItem(self.verticalSpacer, 3, 0, 1, 1)

        self.frame_13 = QFrame(self.tab_unfiltered_criteria)
        self.frame_13.setObjectName(u"frame_13")
        self.frame_13.setMinimumSize(QSize(0, 40))
        self.frame_13.setMaximumSize(QSize(16777215, 16777215))
        self.frame_13.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_13.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_14 = QGridLayout(self.frame_13)
        self.gridLayout_14.setSpacing(2)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.gridLayout_14.setContentsMargins(2, 2, 2, 2)
        self.label_11 = QLabel(self.frame_13)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMaximumSize(QSize(16777215, 16777215))
        self.label_11.setFont(font)
        self.label_11.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_11.setWordWrap(True)

        self.gridLayout_14.addWidget(self.label_11, 0, 0, 1, 1)


        self.gridLayout_12.addWidget(self.frame_13, 1, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_12.addItem(self.verticalSpacer_2, 0, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_unfiltered_criteria, "")
        self.tab_filtered_criteria = QWidget()
        self.tab_filtered_criteria.setObjectName(u"tab_filtered_criteria")
        self.gridLayout_10 = QGridLayout(self.tab_filtered_criteria)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(4, 4, 4, 4)
        self.frame_9 = QFrame(self.tab_filtered_criteria)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_9.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_8 = QGridLayout(self.frame_9)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(0, 0, 0, 0)

        self.gridLayout_10.addWidget(self.frame_9, 5, 0, 1, 1)

        self.frame_16 = QFrame(self.tab_filtered_criteria)
        self.frame_16.setObjectName(u"frame_16")
        self.frame_16.setMinimumSize(QSize(0, 40))
        self.frame_16.setMaximumSize(QSize(16777215, 16777215))
        self.frame_16.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_16.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_15 = QGridLayout(self.frame_16)
        self.gridLayout_15.setSpacing(2)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.gridLayout_15.setContentsMargins(2, 2, 2, 2)
        self.label_12 = QLabel(self.frame_16)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setMinimumSize(QSize(0, 32))
        self.label_12.setMaximumSize(QSize(16777215, 32))
        self.label_12.setFont(font)
        self.label_12.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_12.setWordWrap(False)

        self.gridLayout_15.addWidget(self.label_12, 0, 0, 1, 1)


        self.gridLayout_10.addWidget(self.frame_16, 0, 0, 1, 1)

        self.frame_14 = QFrame(self.tab_filtered_criteria)
        self.frame_14.setObjectName(u"frame_14")
        self.frame_14.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_14.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_16 = QGridLayout(self.frame_14)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.horizontalSpacer_18 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_16.addItem(self.horizontalSpacer_18, 0, 2, 1, 1)

        self.horizontalSpacer_17 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_16.addItem(self.horizontalSpacer_17, 0, 0, 1, 1)

        self.checkBox_prestudy_analysis = QCheckBox(self.frame_14)
        self.checkBox_prestudy_analysis.setObjectName(u"checkBox_prestudy_analysis")

        self.gridLayout_16.addWidget(self.checkBox_prestudy_analysis, 0, 1, 1, 1)


        self.gridLayout_10.addWidget(self.frame_14, 6, 0, 1, 1)

        self.frame_8 = QFrame(self.tab_filtered_criteria)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_8.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_7 = QGridLayout(self.frame_8)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.frame_8)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(60, 0))
        self.label_3.setMaximumSize(QSize(60, 16777215))
        self.label_3.setFont(font)
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_3, 0, 3, 1, 1)

        self.lineEdit_speed_of_sound = QLineEdit(self.frame_8)
        self.lineEdit_speed_of_sound.setObjectName(u"lineEdit_speed_of_sound")
        self.lineEdit_speed_of_sound.setEnabled(False)
        self.lineEdit_speed_of_sound.setMinimumSize(QSize(90, 28))
        self.lineEdit_speed_of_sound.setMaximumSize(QSize(100, 28))
        font4 = QFont()
        font4.setPointSize(9)
        self.lineEdit_speed_of_sound.setFont(font4)
        self.lineEdit_speed_of_sound.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.lineEdit_speed_of_sound.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_7.addWidget(self.lineEdit_speed_of_sound, 1, 2, 1, 1)

        self.label_32 = QLabel(self.frame_8)
        self.label_32.setObjectName(u"label_32")
        self.label_32.setMinimumSize(QSize(140, 0))
        self.label_32.setMaximumSize(QSize(140, 16777215))
        self.label_32.setFont(font)
        self.label_32.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_32, 0, 1, 1, 1)

        self.label_5 = QLabel(self.frame_8)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(60, 0))
        self.label_5.setMaximumSize(QSize(60, 16777215))
        self.label_5.setFont(font)
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_5, 1, 3, 1, 1)

        self.lineEdit_average_line_pressure = QLineEdit(self.frame_8)
        self.lineEdit_average_line_pressure.setObjectName(u"lineEdit_average_line_pressure")
        self.lineEdit_average_line_pressure.setEnabled(False)
        self.lineEdit_average_line_pressure.setMinimumSize(QSize(90, 28))
        self.lineEdit_average_line_pressure.setMaximumSize(QSize(100, 28))
        self.lineEdit_average_line_pressure.setFont(font4)
        self.lineEdit_average_line_pressure.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.lineEdit_average_line_pressure.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_7.addWidget(self.lineEdit_average_line_pressure, 0, 2, 1, 1)

        self.label_34 = QLabel(self.frame_8)
        self.label_34.setObjectName(u"label_34")
        self.label_34.setMinimumSize(QSize(140, 0))
        self.label_34.setMaximumSize(QSize(140, 16777215))
        self.label_34.setFont(font)
        self.label_34.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_34, 1, 1, 1, 1)

        self.label_33 = QLabel(self.frame_8)
        self.label_33.setObjectName(u"label_33")
        self.label_33.setMinimumSize(QSize(140, 0))
        self.label_33.setMaximumSize(QSize(140, 16777215))
        self.label_33.setFont(font)
        self.label_33.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_33, 2, 1, 1, 1)

        self.lineEdit_inside_diameter = QLineEdit(self.frame_8)
        self.lineEdit_inside_diameter.setObjectName(u"lineEdit_inside_diameter")
        self.lineEdit_inside_diameter.setEnabled(True)
        self.lineEdit_inside_diameter.setMinimumSize(QSize(90, 28))
        self.lineEdit_inside_diameter.setMaximumSize(QSize(100, 28))
        self.lineEdit_inside_diameter.setFont(font4)
        self.lineEdit_inside_diameter.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.lineEdit_inside_diameter.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_7.addWidget(self.lineEdit_inside_diameter, 2, 2, 1, 1)

        self.label_4 = QLabel(self.frame_8)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(60, 0))
        self.label_4.setMaximumSize(QSize(60, 16777215))
        self.label_4.setFont(font)
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_4, 2, 3, 1, 1)

        self.pushButton_get_internal_diameter_from_selection = QPushButton(self.frame_8)
        self.pushButton_get_internal_diameter_from_selection.setObjectName(u"pushButton_get_internal_diameter_from_selection")
        self.pushButton_get_internal_diameter_from_selection.setMinimumSize(QSize(32, 28))
        self.pushButton_get_internal_diameter_from_selection.setMaximumSize(QSize(32, 28))
        icon2 = Icon(u":/icons/arrow_circle_down_blue.png")
        self.pushButton_get_internal_diameter_from_selection.setIcon(icon2)
        self.pushButton_get_internal_diameter_from_selection.setIconSize(QSize(20, 20))

        self.gridLayout_7.addWidget(self.pushButton_get_internal_diameter_from_selection, 2, 0, 1, 1)


        self.gridLayout_10.addWidget(self.frame_8, 2, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_filtered_criteria, "")

        self.gridLayout_3.addWidget(self.tabWidget_main, 3, 0, 1, 1)


        self.gridLayout_4.addWidget(self.frame_2, 2, 0, 1, 1)

        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 40))
        self.frame.setMaximumSize(QSize(520, 40))
        self.frame.setFrameShape(QFrame.Shape.Box)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.frame.setLineWidth(1)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(0, 30))
        self.label.setMaximumSize(QSize(452, 30))
        font5 = QFont()
        font5.setFamilies([u"Segoe UI"])
        font5.setPointSize(10)
        font5.setBold(False)
        font5.setItalic(False)
        self.label.setFont(font5)
        self.label.setTextFormat(Qt.TextFormat.AutoText)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout_4.addWidget(self.frame, 0, 0, 1, 1)

        self.frame_ifft_controls = QFrame(Form)
        self.frame_ifft_controls.setObjectName(u"frame_ifft_controls")
        self.frame_ifft_controls.setMinimumSize(QSize(0, 120))
        self.frame_ifft_controls.setMaximumSize(QSize(16777215, 16777215))
        self.frame_ifft_controls.setFrameShape(QFrame.Shape.Box)
        self.frame_ifft_controls.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_4.addWidget(self.frame_ifft_controls, 1, 0, 1, 1)


        self.retranslateUi(Form)

        self.comboBox_selector_filter.setCurrentIndex(0)
        self.tabWidget_main.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.pushButton_plot_data.setText(QCoreApplication.translate("Form", u"Plot data", None))
        self.comboBox_selector_filter.setItemText(0, QCoreApplication.translate("Form", u"Surfaces", None))
        self.comboBox_selector_filter.setItemText(1, QCoreApplication.translate("Form", u"Lines", None))
        self.comboBox_selector_filter.setItemText(2, QCoreApplication.translate("Form", u"Points", None))
        self.comboBox_selector_filter.setItemText(3, QCoreApplication.translate("Form", u"Nodes", None))

#if QT_CONFIG(tooltip)
        self.pushButton_get_fluid.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Get fluid from library</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_get_fluid.setText("")
        self.label_31.setText(QCoreApplication.translate("Form", u"Selected fluid:", None))
        self.lineEdit_selected_fluid.setText("")
        self.lineEdit_selection_id.setText("")
        self.label_2.setText(QCoreApplication.translate("Form", u"Selector filter: ", None))
        self.label_10.setText(QCoreApplication.translate("Form", u"Selected ID: ", None))
#if QT_CONFIG(tooltip)
        self.pushButton_export_data.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-size:10pt; font-weight:400;\">Press to export the current response function</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_export_data.setText("")
        self.lineEdit_pressure_ratio.setText("")
        self.label_6.setText(QCoreApplication.translate("Form", u"[--]", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"<html><head/><body><p>Pressure ratio R:</p></body></html>", None))
        self.label_9.setText(QCoreApplication.translate("Form", u"<html><head/><body><p>Unfiltered criteria P<span style=\" vertical-align:sub;\">cf</span>:</p></body></html>", None))
        self.lineEdit_unfiltered_criterion.setText("")
        self.label_7.setText(QCoreApplication.translate("Form", u"[%]", None))
        self.label_11.setText(QCoreApplication.translate("Form", u"<html><head/><body><p>P<span style=\" vertical-align:sub;\">cf</span> = min{3*R; 7}</p></body></html>", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_unfiltered_criteria), QCoreApplication.translate("Form", u"At cylinder flanges", None))
        self.label_12.setText(QCoreApplication.translate("Form", u"<html><head/><body><p>P<span style=\" vertical-align:sub;\">1</span> = (400 * C<span style=\" vertical-align:sub;\">0</span><span style=\" vertical-align:super;\">\u00bd</span>) / (350 * P<span style=\" vertical-align:sub;\">L </span>* D<span style=\" vertical-align:sub;\">in</span> * F<span style=\" vertical-align:sub;\">n</span>)<span style=\" vertical-align:super;\">\u00bd</span></p></body></html>", None))
        self.checkBox_prestudy_analysis.setText(QCoreApplication.translate("Form", u"Prestudy analysis", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"[bar (a)]", None))
        self.lineEdit_speed_of_sound.setText("")
        self.label_32.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"right\">Avg. line pressure P<span style=\" vertical-align:sub;\">L</span>:</p></body></html>", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"[m/s]", None))
        self.lineEdit_average_line_pressure.setText("")
        self.label_34.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"right\">Speed of sound C<span style=\" vertical-align:sub;\">0</span>:</p></body></html>", None))
        self.label_33.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"right\">Inside diameter D<span style=\" vertical-align:sub;\">in</span>:</p></body></html>", None))
        self.lineEdit_inside_diameter.setText("")
        self.label_4.setText(QCoreApplication.translate("Form", u"[mm]", None))
#if QT_CONFIG(tooltip)
        self.pushButton_get_internal_diameter_from_selection.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Get the internal diameter of the selected surface</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_get_internal_diameter_from_selection.setText("")
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_filtered_criteria), QCoreApplication.translate("Form", u"At and beyond line-side of PSD", None))
        self.label.setText(QCoreApplication.translate("Form", u"Allowable pulsations for reciprocating compressor", None))
    # retranslateUi



class AllowablePulsationsForReciprocatingCompressorInputs_UI(QWidget, Ui_Form):
    """
    Component Hierarchy:
    - Form: QWidget
        - (Layout): QGridLayout
                - frame_2: QFrame
                    - (Layout): QGridLayout
                            - frame_3: QFrame
                                - (Layout): QGridLayout
                                        - pushButton_plot_data: QPushButton
                            - frame_4: QFrame
                                - (Layout): QGridLayout
                                        - comboBox_selector_filter: QComboBox
                                        - pushButton_get_fluid: QPushButton
                                        - label_31: QLabel
                                        - lineEdit_selected_fluid: QLineEdit
                                        - lineEdit_selection_id: QLineEdit
                                        - label_2: QLabel
                                        - label_10: QLabel
                                        - pushButton_export_data: QPushButton
                            - tabWidget_main: QTabWidget
                                - tab_unfiltered_criteria: QWidget
                                    - (Layout): QGridLayout
                                            - frame_11: QFrame
                                                - (Layout): QGridLayout
                                                        - lineEdit_pressure_ratio: QLineEdit
                                                        - label_6: QLabel
                                                        - label_8: QLabel
                                                        - label_9: QLabel
                                                        - lineEdit_unfiltered_criterion: QLineEdit
                                                        - label_7: QLabel
                                            - frame_13: QFrame
                                                - (Layout): QGridLayout
                                                        - label_11: QLabel
                                - tab_filtered_criteria: QWidget
                                    - (Layout): QGridLayout
                                            - frame_9: QFrame
                                                - (Layout): QGridLayout
                                            - frame_16: QFrame
                                                - (Layout): QGridLayout
                                                        - label_12: QLabel
                                            - frame_14: QFrame
                                                - (Layout): QGridLayout
                                                        - checkBox_prestudy_analysis: QCheckBox
                                            - frame_8: QFrame
                                                - (Layout): QGridLayout
                                                        - label_3: QLabel
                                                        - lineEdit_speed_of_sound: QLineEdit
                                                        - label_32: QLabel
                                                        - label_5: QLabel
                                                        - lineEdit_average_line_pressure: QLineEdit
                                                        - label_34: QLabel
                                                        - label_33: QLabel
                                                        - lineEdit_inside_diameter: QLineEdit
                                                        - label_4: QLabel
                                                        - pushButton_get_internal_diameter_from_selection: QPushButton
                - frame: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
                - frame_ifft_controls: QFrame
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
