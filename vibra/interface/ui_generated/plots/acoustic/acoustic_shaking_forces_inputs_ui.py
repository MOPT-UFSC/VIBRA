# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'acoustic_shaking_forces_inputs.ui'
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
    QSpacerItem, QWidget)

from vibra.interface.formatters.icons import Icon

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(410, 320)
        Form.setMinimumSize(QSize(0, 320))
        Form.setMaximumSize(QSize(16777215, 360))
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
        self.frame_2.setMaximumSize(QSize(520, 360))
        self.frame_2.setFrameShape(QFrame.Shape.Box)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_2)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(4, 4, 4, 4)
        self.frame_4 = QFrame(self.frame_2)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(0, 52))
        self.frame_4.setMaximumSize(QSize(16777215, 280))
        self.frame_4.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.frame_4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(6)
        self.gridLayout.setVerticalSpacing(8)
        self.gridLayout.setContentsMargins(2, 8, 2, 2)
        self.label_unit_line_edit = QLabel(self.frame_4)
        self.label_unit_line_edit.setObjectName(u"label_unit_line_edit")
        self.label_unit_line_edit.setMinimumSize(QSize(40, 30))
        self.label_unit_line_edit.setMaximumSize(QSize(40, 30))
        font1 = QFont()
        font1.setPointSize(10)
        self.label_unit_line_edit.setFont(font1)

        self.gridLayout.addWidget(self.label_unit_line_edit, 5, 3, 1, 1)

        self.label_unit_combo_box = QLabel(self.frame_4)
        self.label_unit_combo_box.setObjectName(u"label_unit_combo_box")
        self.label_unit_combo_box.setMinimumSize(QSize(40, 30))
        self.label_unit_combo_box.setMaximumSize(QSize(40, 30))
        self.label_unit_combo_box.setFont(font1)

        self.gridLayout.addWidget(self.label_unit_combo_box, 4, 3, 1, 1)

        self.lineEdit_selection_id = QLineEdit(self.frame_4)
        self.lineEdit_selection_id.setObjectName(u"lineEdit_selection_id")
        self.lineEdit_selection_id.setMinimumSize(QSize(140, 30))
        self.lineEdit_selection_id.setMaximumSize(QSize(140, 30))
        self.lineEdit_selection_id.setFont(font1)
        self.lineEdit_selection_id.setStyleSheet(u"")
        self.lineEdit_selection_id.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_selection_id, 0, 2, 1, 1)

        self.comboBox_cutoff_frequency_options = QComboBox(self.frame_4)
        self.comboBox_cutoff_frequency_options.addItem("")
        self.comboBox_cutoff_frequency_options.addItem("")
        self.comboBox_cutoff_frequency_options.addItem("")
        self.comboBox_cutoff_frequency_options.setObjectName(u"comboBox_cutoff_frequency_options")
        self.comboBox_cutoff_frequency_options.setMinimumSize(QSize(140, 30))
        self.comboBox_cutoff_frequency_options.setMaximumSize(QSize(140, 30))
        self.comboBox_cutoff_frequency_options.setFont(font1)

        self.gridLayout.addWidget(self.comboBox_cutoff_frequency_options, 3, 2, 1, 1)

        self.comboBox_selector_filter = QComboBox(self.frame_4)
        self.comboBox_selector_filter.addItem("")
        self.comboBox_selector_filter.addItem("")
        self.comboBox_selector_filter.setObjectName(u"comboBox_selector_filter")
        self.comboBox_selector_filter.setMinimumSize(QSize(140, 30))
        self.comboBox_selector_filter.setMaximumSize(QSize(140, 30))
        self.comboBox_selector_filter.setFont(font1)
        self.comboBox_selector_filter.setStyleSheet(u"")

        self.gridLayout.addWidget(self.comboBox_selector_filter, 1, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.label_10 = QLabel(self.frame_4)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(120, 30))
        self.label_10.setMaximumSize(QSize(140, 30))
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        self.label_10.setFont(font2)
        self.label_10.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_10, 0, 1, 1, 1)

        self.comboBox_cutoff_frequency = QComboBox(self.frame_4)
        self.comboBox_cutoff_frequency.setObjectName(u"comboBox_cutoff_frequency")
        self.comboBox_cutoff_frequency.setMinimumSize(QSize(140, 30))
        self.comboBox_cutoff_frequency.setMaximumSize(QSize(140, 30))
        self.comboBox_cutoff_frequency.setFont(font1)

        self.gridLayout.addWidget(self.comboBox_cutoff_frequency, 4, 2, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 0, 4, 1, 1)

        self.lineEdit_cutoff_frequency = QLineEdit(self.frame_4)
        self.lineEdit_cutoff_frequency.setObjectName(u"lineEdit_cutoff_frequency")
        self.lineEdit_cutoff_frequency.setEnabled(False)
        self.lineEdit_cutoff_frequency.setMinimumSize(QSize(140, 30))
        self.lineEdit_cutoff_frequency.setMaximumSize(QSize(140, 30))
        self.lineEdit_cutoff_frequency.setFont(font1)
        self.lineEdit_cutoff_frequency.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.lineEdit_cutoff_frequency.setStyleSheet(u"")
        self.lineEdit_cutoff_frequency.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_cutoff_frequency, 5, 2, 1, 1)

        self.label_cutoff_frequency = QLabel(self.frame_4)
        self.label_cutoff_frequency.setObjectName(u"label_cutoff_frequency")
        self.label_cutoff_frequency.setMinimumSize(QSize(120, 30))
        self.label_cutoff_frequency.setMaximumSize(QSize(140, 30))
        font3 = QFont()
        font3.setPointSize(10)
        font3.setBold(False)
        font3.setItalic(False)
        self.label_cutoff_frequency.setFont(font3)
        self.label_cutoff_frequency.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_cutoff_frequency, 3, 1, 1, 1)

        self.pushButton_export_data = QPushButton(self.frame_4)
        self.pushButton_export_data.setObjectName(u"pushButton_export_data")
        self.pushButton_export_data.setMinimumSize(QSize(40, 30))
        self.pushButton_export_data.setMaximumSize(QSize(40, 30))
        font4 = QFont()
        font4.setFamilies([u"MS Shell Dlg 2"])
        font4.setPointSize(11)
        font4.setBold(True)
        font4.setItalic(False)
        self.pushButton_export_data.setFont(font4)
        self.pushButton_export_data.setStyleSheet(u"")
        icon = Icon(u":/icons/save_as.png")
        self.pushButton_export_data.setIcon(icon)
        self.pushButton_export_data.setIconSize(QSize(20, 20))
        self.pushButton_export_data.setFlat(False)

        self.gridLayout.addWidget(self.pushButton_export_data, 0, 3, 1, 1)

        self.label_2 = QLabel(self.frame_4)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(120, 30))
        self.label_2.setMaximumSize(QSize(140, 30))
        self.label_2.setFont(font1)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_2, 1, 1, 1, 1)

        self.label_fc_line_edit = QLabel(self.frame_4)
        self.label_fc_line_edit.setObjectName(u"label_fc_line_edit")
        self.label_fc_line_edit.setMinimumSize(QSize(120, 30))
        self.label_fc_line_edit.setMaximumSize(QSize(140, 30))
        self.label_fc_line_edit.setFont(font3)
        self.label_fc_line_edit.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_fc_line_edit, 5, 1, 1, 1)

        self.label_fc_combo_box = QLabel(self.frame_4)
        self.label_fc_combo_box.setObjectName(u"label_fc_combo_box")
        self.label_fc_combo_box.setMinimumSize(QSize(120, 30))
        self.label_fc_combo_box.setMaximumSize(QSize(140, 30))
        self.label_fc_combo_box.setFont(font3)
        self.label_fc_combo_box.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_fc_combo_box, 4, 1, 1, 1)

        self.label_3 = QLabel(self.frame_4)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(120, 30))
        self.label_3.setMaximumSize(QSize(140, 30))
        self.label_3.setFont(font1)
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_3, 2, 1, 1, 1)

        self.comboBox_output_mode = QComboBox(self.frame_4)
        self.comboBox_output_mode.addItem("")
        self.comboBox_output_mode.addItem("")
        self.comboBox_output_mode.setObjectName(u"comboBox_output_mode")
        self.comboBox_output_mode.setMinimumSize(QSize(140, 30))
        self.comboBox_output_mode.setMaximumSize(QSize(140, 30))
        self.comboBox_output_mode.setFont(font1)
        self.comboBox_output_mode.setStyleSheet(u"")

        self.gridLayout.addWidget(self.comboBox_output_mode, 2, 2, 1, 1)


        self.gridLayout_3.addWidget(self.frame_4, 0, 0, 1, 1)

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
        self.pushButton_plot_data.setFont(font1)
        self.pushButton_plot_data.setStyleSheet(u"")
        self.pushButton_plot_data.setFlat(False)

        self.gridLayout_47.addWidget(self.pushButton_plot_data, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_3, 1, 0, 1, 1)


        self.gridLayout_4.addWidget(self.frame_2, 1, 0, 1, 1)


        self.retranslateUi(Form)

        self.comboBox_selector_filter.setCurrentIndex(1)
        self.comboBox_output_mode.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"Plot the acoustic shaking forces spectrum", None))
        self.label_unit_line_edit.setText(QCoreApplication.translate("Form", u"[Hz]", None))
        self.label_unit_combo_box.setText(QCoreApplication.translate("Form", u"[mm]", None))
        self.lineEdit_selection_id.setText("")
        self.comboBox_cutoff_frequency_options.setItemText(0, QCoreApplication.translate("Form", u"Disabled", None))
        self.comboBox_cutoff_frequency_options.setItemText(1, QCoreApplication.translate("Form", u"User-defined", None))
        self.comboBox_cutoff_frequency_options.setItemText(2, QCoreApplication.translate("Form", u"Automatic", None))

        self.comboBox_selector_filter.setItemText(0, QCoreApplication.translate("Form", u"All surfaces", None))
        self.comboBox_selector_filter.setItemText(1, QCoreApplication.translate("Form", u"Selected surfaces", None))

        self.label_10.setText(QCoreApplication.translate("Form", u"Selected ID: ", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_cutoff_frequency.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"center\">f<span style=\" vertical-align:sub;\">c</span> = 1.8412 x C<span style=\" vertical-align:sub;\">o </span>/ (\u03c0 * D<span style=\" vertical-align:sub;\">in</span>), </p><p align=\"justify\">where C<span style=\" vertical-align:sub;\">0</span> is the fluid speed of sound in m/s, and D<span style=\" vertical-align:sub;\">in</span> is the pipe's internal diameter in m.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_cutoff_frequency.setText(QCoreApplication.translate("Form", u"Cut-off frequency:", None))
#if QT_CONFIG(tooltip)
        self.pushButton_export_data.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-size:10pt; font-weight:400;\">Press to export the current response function</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_export_data.setText("")
        self.label_2.setText(QCoreApplication.translate("Form", u"Selector filter: ", None))
        self.label_fc_line_edit.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-size:11pt;\">f</span><span style=\" font-size:11pt; vertical-align:sub;\">c</span> (circular section):</p></body></html>", None))
        self.label_fc_combo_box.setText(QCoreApplication.translate("Form", u"<html><head/><body><p>Section diameter:</p></body></html>", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Output loads: ", None))
        self.comboBox_output_mode.setItemText(0, QCoreApplication.translate("Form", u"Resulting loads", None))
        self.comboBox_output_mode.setItemText(1, QCoreApplication.translate("Form", u"Individual loads", None))

        self.pushButton_plot_data.setText(QCoreApplication.translate("Form", u"Plot data", None))
    # retranslateUi



class AcousticShakingForcesInputs_UI(QWidget, Ui_Form):
    """
    Component Hierarchy:
    - Form: QWidget
        - (Layout): QGridLayout
                - frame: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
                - frame_2: QFrame
                    - (Layout): QGridLayout
                            - frame_4: QFrame
                                - (Layout): QGridLayout
                                        - label_unit_line_edit: QLabel
                                        - label_unit_combo_box: QLabel
                                        - lineEdit_selection_id: QLineEdit
                                        - comboBox_cutoff_frequency_options: QComboBox
                                        - comboBox_selector_filter: QComboBox
                                        - label_10: QLabel
                                        - comboBox_cutoff_frequency: QComboBox
                                        - lineEdit_cutoff_frequency: QLineEdit
                                        - label_cutoff_frequency: QLabel
                                        - pushButton_export_data: QPushButton
                                        - label_2: QLabel
                                        - label_fc_line_edit: QLabel
                                        - label_fc_combo_box: QLabel
                                        - label_3: QLabel
                                        - comboBox_output_mode: QComboBox
                            - frame_3: QFrame
                                - (Layout): QGridLayout
                                        - pushButton_plot_data: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
