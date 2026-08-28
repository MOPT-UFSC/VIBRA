# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'allowable_pulsations_2d_for_screw_compressor_inputs.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QTabWidget, QWidget)

from vibra.interface.formatters.icons import Icon

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(408, 480)
        Form.setMinimumSize(QSize(0, 480))
        Form.setMaximumSize(QSize(16777215, 480))
        self.gridLayout_4 = QGridLayout(Form)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setVerticalSpacing(4)
        self.gridLayout_4.setContentsMargins(4, 4, 4, 4)
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
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        self.label.setFont(font)
        self.label.setTextFormat(Qt.TextFormat.AutoText)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout_4.addWidget(self.frame, 0, 0, 1, 1)

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
        font1 = QFont()
        font1.setPointSize(10)
        self.pushButton_plot_data.setFont(font1)
        self.pushButton_plot_data.setStyleSheet(u"")
        self.pushButton_plot_data.setFlat(False)

        self.gridLayout_47.addWidget(self.pushButton_plot_data, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_3, 5, 0, 1, 1)

        self.frame_4 = QFrame(self.frame_2)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(0, 110))
        self.frame_4.setMaximumSize(QSize(16777215, 120))
        self.frame_4.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.frame_4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(6)
        self.gridLayout.setVerticalSpacing(8)
        self.gridLayout.setContentsMargins(2, 6, 2, 6)
        self.comboBox_selector_filter = QComboBox(self.frame_4)
        self.comboBox_selector_filter.addItem("")
        self.comboBox_selector_filter.addItem("")
        self.comboBox_selector_filter.addItem("")
        self.comboBox_selector_filter.addItem("")
        self.comboBox_selector_filter.setObjectName(u"comboBox_selector_filter")
        self.comboBox_selector_filter.setMinimumSize(QSize(130, 28))
        self.comboBox_selector_filter.setMaximumSize(QSize(130, 28))
        self.comboBox_selector_filter.setFont(font1)
        self.comboBox_selector_filter.setStyleSheet(u"")

        self.gridLayout.addWidget(self.comboBox_selector_filter, 1, 2, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 0, 4, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.lineEdit_selection_id = QLineEdit(self.frame_4)
        self.lineEdit_selection_id.setObjectName(u"lineEdit_selection_id")
        self.lineEdit_selection_id.setMinimumSize(QSize(130, 28))
        self.lineEdit_selection_id.setMaximumSize(QSize(130, 28))
        self.lineEdit_selection_id.setFont(font1)
        self.lineEdit_selection_id.setStyleSheet(u"")
        self.lineEdit_selection_id.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_selection_id, 0, 2, 1, 1)

        self.pushButton_export_data = QPushButton(self.frame_4)
        self.pushButton_export_data.setObjectName(u"pushButton_export_data")
        self.pushButton_export_data.setMinimumSize(QSize(44, 28))
        self.pushButton_export_data.setMaximumSize(QSize(44, 28))
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        font2.setPointSize(11)
        font2.setBold(True)
        font2.setItalic(False)
        self.pushButton_export_data.setFont(font2)
        self.pushButton_export_data.setStyleSheet(u"")
        icon = Icon(u":/icons/save_as.png")
        self.pushButton_export_data.setIcon(icon)
        self.pushButton_export_data.setIconSize(QSize(20, 20))
        self.pushButton_export_data.setFlat(False)

        self.gridLayout.addWidget(self.pushButton_export_data, 0, 3, 1, 1)

        self.label_10 = QLabel(self.frame_4)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(110, 28))
        self.label_10.setMaximumSize(QSize(110, 28))
        font3 = QFont()
        font3.setFamilies([u"MS Shell Dlg 2"])
        font3.setPointSize(10)
        font3.setBold(False)
        font3.setItalic(False)
        self.label_10.setFont(font3)
        self.label_10.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_10, 0, 1, 1, 1)

        self.label_2 = QLabel(self.frame_4)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(110, 28))
        self.label_2.setMaximumSize(QSize(110, 28))
        self.label_2.setFont(font1)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_2, 1, 1, 1, 1)

        self.lineEdit_selected_fluid = QLineEdit(self.frame_4)
        self.lineEdit_selected_fluid.setObjectName(u"lineEdit_selected_fluid")
        self.lineEdit_selected_fluid.setEnabled(False)
        self.lineEdit_selected_fluid.setMinimumSize(QSize(130, 28))
        self.lineEdit_selected_fluid.setMaximumSize(QSize(130, 28))
        font4 = QFont()
        font4.setPointSize(8)
        self.lineEdit_selected_fluid.setFont(font4)
        self.lineEdit_selected_fluid.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.lineEdit_selected_fluid.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_selected_fluid, 2, 2, 1, 1)

        self.pushButton_get_fluid = QPushButton(self.frame_4)
        self.pushButton_get_fluid.setObjectName(u"pushButton_get_fluid")
        self.pushButton_get_fluid.setMinimumSize(QSize(44, 0))
        self.pushButton_get_fluid.setMaximumSize(QSize(44, 28))
        self.pushButton_get_fluid.setFont(font1)
        icon1 = Icon(u":/icons/get_fluid_blue.png")
        self.pushButton_get_fluid.setIcon(icon1)
        self.pushButton_get_fluid.setIconSize(QSize(20, 20))

        self.gridLayout.addWidget(self.pushButton_get_fluid, 2, 3, 1, 1)

        self.label_31 = QLabel(self.frame_4)
        self.label_31.setObjectName(u"label_31")
        self.label_31.setMinimumSize(QSize(110, 0))
        self.label_31.setMaximumSize(QSize(110, 16777215))
        self.label_31.setFont(font1)
        self.label_31.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_31, 2, 1, 1, 1)


        self.gridLayout_3.addWidget(self.frame_4, 0, 0, 1, 1)

        self.frame_5 = QFrame(self.frame_2)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setMaximumSize(QSize(16777215, 40))
        self.frame_5.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_6 = QGridLayout(self.frame_5)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setHorizontalSpacing(6)
        self.gridLayout_6.setVerticalSpacing(2)
        self.gridLayout_6.setContentsMargins(2, 2, 2, 2)

        self.gridLayout_3.addWidget(self.frame_5, 2, 0, 1, 1)

        self.tabWidget_main = QTabWidget(self.frame_2)
        self.tabWidget_main.setObjectName(u"tabWidget_main")
        self.tabWidget_main.setFont(font1)
        self.tab_allowable_pulsation = QWidget()
        self.tab_allowable_pulsation.setObjectName(u"tab_allowable_pulsation")
        self.gridLayout_10 = QGridLayout(self.tab_allowable_pulsation)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(4, 4, 4, 4)
        self.frame_16 = QFrame(self.tab_allowable_pulsation)
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
        self.label_12.setFont(font1)
        self.label_12.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_12.setWordWrap(False)

        self.gridLayout_15.addWidget(self.label_12, 0, 0, 1, 1)


        self.gridLayout_10.addWidget(self.frame_16, 1, 0, 1, 1)

        self.frame_8 = QFrame(self.tab_allowable_pulsation)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_8.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_7 = QGridLayout(self.frame_8)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setVerticalSpacing(10)
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_average_line_pressure = QLineEdit(self.frame_8)
        self.lineEdit_average_line_pressure.setObjectName(u"lineEdit_average_line_pressure")
        self.lineEdit_average_line_pressure.setEnabled(False)
        self.lineEdit_average_line_pressure.setMinimumSize(QSize(90, 28))
        self.lineEdit_average_line_pressure.setMaximumSize(QSize(100, 28))
        font5 = QFont()
        font5.setPointSize(9)
        self.lineEdit_average_line_pressure.setFont(font5)
        self.lineEdit_average_line_pressure.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.lineEdit_average_line_pressure.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_7.addWidget(self.lineEdit_average_line_pressure, 0, 2, 1, 1)

        self.label_5 = QLabel(self.frame_8)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(60, 0))
        self.label_5.setMaximumSize(QSize(60, 16777215))
        self.label_5.setFont(font1)
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_5, 1, 3, 1, 1)

        self.label_32 = QLabel(self.frame_8)
        self.label_32.setObjectName(u"label_32")
        self.label_32.setMinimumSize(QSize(140, 0))
        self.label_32.setMaximumSize(QSize(140, 16777215))
        self.label_32.setFont(font1)
        self.label_32.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_32, 0, 1, 1, 1)

        self.label_3 = QLabel(self.frame_8)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(60, 0))
        self.label_3.setMaximumSize(QSize(60, 16777215))
        self.label_3.setFont(font1)
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_3, 0, 3, 1, 1)

        self.label_34 = QLabel(self.frame_8)
        self.label_34.setObjectName(u"label_34")
        self.label_34.setMinimumSize(QSize(140, 0))
        self.label_34.setMaximumSize(QSize(140, 16777215))
        self.label_34.setFont(font1)
        self.label_34.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_34, 1, 1, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_7, 0, 0, 1, 1)

        self.lineEdit_speed_of_sound = QLineEdit(self.frame_8)
        self.lineEdit_speed_of_sound.setObjectName(u"lineEdit_speed_of_sound")
        self.lineEdit_speed_of_sound.setEnabled(False)
        self.lineEdit_speed_of_sound.setMinimumSize(QSize(90, 28))
        self.lineEdit_speed_of_sound.setMaximumSize(QSize(100, 28))
        self.lineEdit_speed_of_sound.setFont(font5)
        self.lineEdit_speed_of_sound.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.lineEdit_speed_of_sound.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_7.addWidget(self.lineEdit_speed_of_sound, 1, 2, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_8, 0, 4, 1, 1)

        self.comboBox_penalization_factor = QComboBox(self.frame_8)
        self.comboBox_penalization_factor.setObjectName(u"comboBox_penalization_factor")
        self.comboBox_penalization_factor.setMinimumSize(QSize(0, 26))
        self.comboBox_penalization_factor.setMaximumSize(QSize(16777215, 26))

        self.gridLayout_7.addWidget(self.comboBox_penalization_factor, 2, 2, 1, 1)

        self.label_penalization_factor = QLabel(self.frame_8)
        self.label_penalization_factor.setObjectName(u"label_penalization_factor")
        self.label_penalization_factor.setMinimumSize(QSize(120, 26))
        self.label_penalization_factor.setMaximumSize(QSize(140, 26))
        self.label_penalization_factor.setFont(font1)
        self.label_penalization_factor.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_penalization_factor, 2, 1, 1, 1)

        self.label_8 = QLabel(self.frame_8)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMinimumSize(QSize(0, 26))
        self.label_8.setMaximumSize(QSize(16777215, 26))
        self.label_8.setFont(font1)
        self.label_8.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_8, 2, 3, 1, 1)


        self.gridLayout_10.addWidget(self.frame_8, 3, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_10.addItem(self.verticalSpacer, 0, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_10.addItem(self.verticalSpacer_2, 4, 0, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_10.addItem(self.verticalSpacer_3, 2, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_allowable_pulsation, "")

        self.gridLayout_3.addWidget(self.tabWidget_main, 3, 0, 1, 1)


        self.gridLayout_4.addWidget(self.frame_2, 1, 0, 1, 1)


        self.retranslateUi(Form)

        self.comboBox_selector_filter.setCurrentIndex(0)
        self.tabWidget_main.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"Allowable pulsations for screw compressor", None))
        self.pushButton_plot_data.setText(QCoreApplication.translate("Form", u"Plot data", None))
        self.comboBox_selector_filter.setItemText(0, QCoreApplication.translate("Form", u"Surfaces", None))
        self.comboBox_selector_filter.setItemText(1, QCoreApplication.translate("Form", u"Lines", None))
        self.comboBox_selector_filter.setItemText(2, QCoreApplication.translate("Form", u"Points", None))
        self.comboBox_selector_filter.setItemText(3, QCoreApplication.translate("Form", u"Nodes", None))

        self.lineEdit_selection_id.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_export_data.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-size:10pt; font-weight:400;\">Press to export the current response function</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_export_data.setText("")
        self.label_10.setText(QCoreApplication.translate("Form", u"Selected ID: ", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Selector filter: ", None))
        self.lineEdit_selected_fluid.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_get_fluid.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Get fluid from library</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_get_fluid.setText("")
        self.label_31.setText(QCoreApplication.translate("Form", u"Selected fluid:", None))
#if QT_CONFIG(tooltip)
        self.label_12.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Allowable peak-to-peak pulsation levels as a percentage of the absolute mean line pressure in kPa.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_12.setText(QCoreApplication.translate("Form", u"<html><head/><body><p>P<span style=\" vertical-align:sub;\">p-p</span> = min{2; 28.6 / P<span style=\" vertical-align:sub;\">AM</span><span style=\" vertical-align:super;\">1/3</span>} [%]</p></body></html>", None))
        self.lineEdit_average_line_pressure.setText("")
        self.label_5.setText(QCoreApplication.translate("Form", u"[m/s]", None))
        self.label_32.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"right\">Avg. line pressure P<span style=\" vertical-align:sub;\">AM</span>:</p></body></html>", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"[kPa (a)]", None))
        self.label_34.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"right\">Speed of sound C<span style=\" vertical-align:sub;\">0</span>:</p></body></html>", None))
        self.lineEdit_speed_of_sound.setText("")
        self.label_penalization_factor.setText(QCoreApplication.translate("Form", u"Penalization factor:", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"[%]", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_allowable_pulsation), QCoreApplication.translate("Form", u"Allowable pulsation levels", None))
    # retranslateUi



class AllowablePulsations2dForScrewCompressorInputs_UI(QWidget, Ui_Form):
    """
    Component Hierarchy:
    - Form: QWidget
        - (Layout): QGridLayout
                - frame: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
                - frame_2: QFrame
                    - (Layout): QGridLayout
                            - frame_3: QFrame
                                - (Layout): QGridLayout
                                        - pushButton_plot_data: QPushButton
                            - frame_4: QFrame
                                - (Layout): QGridLayout
                                        - comboBox_selector_filter: QComboBox
                                        - lineEdit_selection_id: QLineEdit
                                        - pushButton_export_data: QPushButton
                                        - label_10: QLabel
                                        - label_2: QLabel
                                        - lineEdit_selected_fluid: QLineEdit
                                        - pushButton_get_fluid: QPushButton
                                        - label_31: QLabel
                            - frame_5: QFrame
                                - (Layout): QGridLayout
                            - tabWidget_main: QTabWidget
                                - tab_allowable_pulsation: QWidget
                                    - (Layout): QGridLayout
                                            - frame_16: QFrame
                                                - (Layout): QGridLayout
                                                        - label_12: QLabel
                                            - frame_8: QFrame
                                                - (Layout): QGridLayout
                                                        - lineEdit_average_line_pressure: QLineEdit
                                                        - label_5: QLabel
                                                        - label_32: QLabel
                                                        - label_3: QLabel
                                                        - label_34: QLabel
                                                        - lineEdit_speed_of_sound: QLineEdit
                                                        - comboBox_penalization_factor: QComboBox
                                                        - label_penalization_factor: QLabel
                                                        - label_8: QLabel
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
