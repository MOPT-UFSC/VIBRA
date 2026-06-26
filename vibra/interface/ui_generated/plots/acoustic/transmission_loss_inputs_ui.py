# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'transmission_loss_inputs.ui'
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

from vibra.interface.formatters.icons import themed_icon

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(400, 380)
        Form.setMinimumSize(QSize(0, 380))
        Form.setMaximumSize(QSize(16777215, 380))
        self.gridLayout_2 = QGridLayout(Form)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setHorizontalSpacing(6)
        self.gridLayout_2.setVerticalSpacing(4)
        self.gridLayout_2.setContentsMargins(4, 4, 4, 4)
        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 40))
        self.frame.setMaximumSize(QSize(16777215, 40))
        self.frame.setFrameShape(QFrame.Shape.Box)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
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

        self.gridLayout_4.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 1)

        self.frame_2 = QFrame(Form)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(0, 0))
        self.frame_2.setMaximumSize(QSize(520, 460))
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
        self.pushButton_plot_data.setMinimumSize(QSize(120, 32))
        self.pushButton_plot_data.setMaximumSize(QSize(120, 32))
        font1 = QFont()
        font1.setFamilies([u"MS Shell Dlg 2"])
        font1.setPointSize(10)
        font1.setBold(False)
        font1.setItalic(False)
        self.pushButton_plot_data.setFont(font1)
        self.pushButton_plot_data.setStyleSheet(u"")
        self.pushButton_plot_data.setFlat(False)

        self.gridLayout_47.addWidget(self.pushButton_plot_data, 1, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_3, 2, 0, 1, 1)

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
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_3, 0, 0, 1, 1)

        self.label_cutoff_frequency = QLabel(self.frame_4)
        self.label_cutoff_frequency.setObjectName(u"label_cutoff_frequency")
        self.label_cutoff_frequency.setMinimumSize(QSize(120, 30))
        self.label_cutoff_frequency.setMaximumSize(QSize(140, 30))
        font2 = QFont()
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        self.label_cutoff_frequency.setFont(font2)
        self.label_cutoff_frequency.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_cutoff_frequency, 4, 1, 1, 1)

        self.label_fc_line_edit = QLabel(self.frame_4)
        self.label_fc_line_edit.setObjectName(u"label_fc_line_edit")
        self.label_fc_line_edit.setMinimumSize(QSize(120, 30))
        self.label_fc_line_edit.setMaximumSize(QSize(140, 30))
        self.label_fc_line_edit.setFont(font2)
        self.label_fc_line_edit.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_fc_line_edit, 6, 1, 1, 1)

        self.label_unit_line_edit = QLabel(self.frame_4)
        self.label_unit_line_edit.setObjectName(u"label_unit_line_edit")
        self.label_unit_line_edit.setMinimumSize(QSize(40, 30))
        self.label_unit_line_edit.setMaximumSize(QSize(40, 30))
        font3 = QFont()
        font3.setPointSize(10)
        self.label_unit_line_edit.setFont(font3)

        self.gridLayout.addWidget(self.label_unit_line_edit, 6, 3, 1, 1)

        self.label_10 = QLabel(self.frame_4)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(120, 30))
        self.label_10.setMaximumSize(QSize(120, 30))
        self.label_10.setFont(font1)
        self.label_10.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_10, 0, 1, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_4, 0, 4, 1, 1)

        self.label_integration_method = QLabel(self.frame_4)
        self.label_integration_method.setObjectName(u"label_integration_method")
        self.label_integration_method.setMinimumSize(QSize(120, 30))
        self.label_integration_method.setMaximumSize(QSize(120, 30))
        self.label_integration_method.setFont(font3)
        self.label_integration_method.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_integration_method, 3, 1, 1, 1)

        self.lineEdit_cutoff_frequency = QLineEdit(self.frame_4)
        self.lineEdit_cutoff_frequency.setObjectName(u"lineEdit_cutoff_frequency")
        self.lineEdit_cutoff_frequency.setEnabled(False)
        self.lineEdit_cutoff_frequency.setMinimumSize(QSize(140, 30))
        self.lineEdit_cutoff_frequency.setMaximumSize(QSize(140, 30))
        self.lineEdit_cutoff_frequency.setFont(font3)
        self.lineEdit_cutoff_frequency.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.lineEdit_cutoff_frequency.setStyleSheet(u"")
        self.lineEdit_cutoff_frequency.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_cutoff_frequency, 6, 2, 1, 1)

        self.lineEdit_output_surface_id = QLineEdit(self.frame_4)
        self.lineEdit_output_surface_id.setObjectName(u"lineEdit_output_surface_id")
        self.lineEdit_output_surface_id.setMinimumSize(QSize(140, 30))
        self.lineEdit_output_surface_id.setMaximumSize(QSize(140, 30))
        font4 = QFont()
        font4.setFamilies([u"Arial"])
        font4.setPointSize(10)
        font4.setBold(False)
        font4.setItalic(False)
        self.lineEdit_output_surface_id.setFont(font4)
        self.lineEdit_output_surface_id.setStyleSheet(u"")
        self.lineEdit_output_surface_id.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_output_surface_id, 0, 2, 1, 1)

        self.comboBox_processing_selector = QComboBox(self.frame_4)
        self.comboBox_processing_selector.addItem("")
        self.comboBox_processing_selector.addItem("")
        self.comboBox_processing_selector.setObjectName(u"comboBox_processing_selector")
        self.comboBox_processing_selector.setMinimumSize(QSize(140, 30))
        self.comboBox_processing_selector.setMaximumSize(QSize(140, 30))
        self.comboBox_processing_selector.setFont(font2)
        self.comboBox_processing_selector.setStyleSheet(u"QComboBox::hover{border-radius: 4px; border-color: rgb(0, 170, 255); border-style: ridge; border-width: 2px}")

        self.gridLayout.addWidget(self.comboBox_processing_selector, 2, 2, 1, 1)

        self.lineEdit_input_surface_id = QLineEdit(self.frame_4)
        self.lineEdit_input_surface_id.setObjectName(u"lineEdit_input_surface_id")
        self.lineEdit_input_surface_id.setMinimumSize(QSize(140, 30))
        self.lineEdit_input_surface_id.setMaximumSize(QSize(140, 30))
        self.lineEdit_input_surface_id.setFont(font4)
        self.lineEdit_input_surface_id.setStyleSheet(u"")
        self.lineEdit_input_surface_id.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_input_surface_id, 1, 2, 1, 1)

        self.label_2 = QLabel(self.frame_4)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(120, 30))
        self.label_2.setMaximumSize(QSize(120, 30))
        self.label_2.setFont(font3)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_2, 2, 1, 1, 1)

        self.pushButton_export_data = QPushButton(self.frame_4)
        self.pushButton_export_data.setObjectName(u"pushButton_export_data")
        self.pushButton_export_data.setMinimumSize(QSize(40, 30))
        self.pushButton_export_data.setMaximumSize(QSize(40, 30))
        font5 = QFont()
        font5.setFamilies([u"MS Shell Dlg 2"])
        font5.setPointSize(11)
        font5.setBold(True)
        font5.setItalic(False)
        self.pushButton_export_data.setFont(font5)
        self.pushButton_export_data.setStyleSheet(u"")
        icon = themed_icon(u":/icons/save_as.png")
        self.pushButton_export_data.setIcon(icon)
        self.pushButton_export_data.setIconSize(QSize(20, 20))
        self.pushButton_export_data.setFlat(False)

        self.gridLayout.addWidget(self.pushButton_export_data, 0, 3, 1, 1)

        self.pushButton_flip_selection = QPushButton(self.frame_4)
        self.pushButton_flip_selection.setObjectName(u"pushButton_flip_selection")
        self.pushButton_flip_selection.setMinimumSize(QSize(40, 30))
        self.pushButton_flip_selection.setMaximumSize(QSize(40, 30))
        self.pushButton_flip_selection.setFont(font5)
        self.pushButton_flip_selection.setStyleSheet(u"")
        icon1 = themed_icon(u":/icons/invert_icon.png")
        self.pushButton_flip_selection.setIcon(icon1)
        self.pushButton_flip_selection.setIconSize(QSize(22, 22))
        self.pushButton_flip_selection.setFlat(False)

        self.gridLayout.addWidget(self.pushButton_flip_selection, 1, 3, 1, 1)

        self.comboBox_cutoff_frequency_options = QComboBox(self.frame_4)
        self.comboBox_cutoff_frequency_options.addItem("")
        self.comboBox_cutoff_frequency_options.addItem("")
        self.comboBox_cutoff_frequency_options.addItem("")
        self.comboBox_cutoff_frequency_options.setObjectName(u"comboBox_cutoff_frequency_options")
        self.comboBox_cutoff_frequency_options.setMinimumSize(QSize(140, 30))
        self.comboBox_cutoff_frequency_options.setMaximumSize(QSize(140, 30))
        self.comboBox_cutoff_frequency_options.setFont(font3)

        self.gridLayout.addWidget(self.comboBox_cutoff_frequency_options, 4, 2, 1, 1)

        self.comboBox_integration_method = QComboBox(self.frame_4)
        self.comboBox_integration_method.addItem("")
        self.comboBox_integration_method.addItem("")
        self.comboBox_integration_method.setObjectName(u"comboBox_integration_method")
        self.comboBox_integration_method.setMinimumSize(QSize(140, 30))
        self.comboBox_integration_method.setMaximumSize(QSize(140, 30))
        self.comboBox_integration_method.setFont(font2)
        self.comboBox_integration_method.setStyleSheet(u"QComboBox::hover{border-radius: 4px; border-color: rgb(0, 170, 255); border-style: ridge; border-width: 2px}")

        self.gridLayout.addWidget(self.comboBox_integration_method, 3, 2, 1, 1)

        self.label_15 = QLabel(self.frame_4)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setMinimumSize(QSize(120, 30))
        self.label_15.setMaximumSize(QSize(120, 30))
        self.label_15.setFont(font1)
        self.label_15.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_15, 1, 1, 1, 1)

        self.label_fc_combo_box = QLabel(self.frame_4)
        self.label_fc_combo_box.setObjectName(u"label_fc_combo_box")
        self.label_fc_combo_box.setMinimumSize(QSize(120, 30))
        self.label_fc_combo_box.setMaximumSize(QSize(140, 30))
        self.label_fc_combo_box.setFont(font2)
        self.label_fc_combo_box.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_fc_combo_box, 5, 1, 1, 1)

        self.comboBox_cutoff_frequency = QComboBox(self.frame_4)
        self.comboBox_cutoff_frequency.setObjectName(u"comboBox_cutoff_frequency")
        self.comboBox_cutoff_frequency.setMinimumSize(QSize(140, 30))
        self.comboBox_cutoff_frequency.setMaximumSize(QSize(140, 30))
        self.comboBox_cutoff_frequency.setFont(font3)

        self.gridLayout.addWidget(self.comboBox_cutoff_frequency, 5, 2, 1, 1)

        self.label_unit_combo_box = QLabel(self.frame_4)
        self.label_unit_combo_box.setObjectName(u"label_unit_combo_box")
        self.label_unit_combo_box.setMinimumSize(QSize(40, 30))
        self.label_unit_combo_box.setMaximumSize(QSize(40, 30))
        self.label_unit_combo_box.setFont(font3)

        self.gridLayout.addWidget(self.label_unit_combo_box, 5, 3, 1, 1)

        self.pushButton_help = QPushButton(self.frame_4)
        self.pushButton_help.setObjectName(u"pushButton_help")
        self.pushButton_help.setMinimumSize(QSize(40, 30))
        self.pushButton_help.setMaximumSize(QSize(40, 30))
        self.pushButton_help.setFont(font5)
        self.pushButton_help.setStyleSheet(u"")
        icon2 = themed_icon(u":/icons/help_icon.png")
        self.pushButton_help.setIcon(icon2)
        self.pushButton_help.setIconSize(QSize(22, 22))
        self.pushButton_help.setFlat(False)

        self.gridLayout.addWidget(self.pushButton_help, 2, 3, 1, 1)


        self.gridLayout_3.addWidget(self.frame_4, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.frame_2, 1, 0, 1, 1)


        self.retranslateUi(Form)

        self.comboBox_processing_selector.setCurrentIndex(0)
        self.comboBox_integration_method.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"Plot the transmission loss or noise reduction", None))
        self.pushButton_plot_data.setText(QCoreApplication.translate("Form", u"Plot data", None))
        self.label_cutoff_frequency.setText(QCoreApplication.translate("Form", u"Cut-off frequency:", None))
        self.label_fc_line_edit.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-size:11pt;\">f</span><span style=\" font-size:11pt; vertical-align:sub;\">c</span> (circular section):</p></body></html>", None))
        self.label_unit_line_edit.setText(QCoreApplication.translate("Form", u"[Hz]", None))
        self.label_10.setText(QCoreApplication.translate("Form", u"Output ID: ", None))
        self.label_integration_method.setText(QCoreApplication.translate("Form", u"Method: ", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_cutoff_frequency.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"center\">f<span style=\" vertical-align:sub;\">c</span> = 1.8412 x C<span style=\" vertical-align:sub;\">o </span>/ (\u03c0 * D<span style=\" vertical-align:sub;\">in</span>), </p><p align=\"justify\">where C<span style=\" vertical-align:sub;\">0</span> is the fluid speed of sound in m/s, and D<span style=\" vertical-align:sub;\">in</span> is the pipe's internal diameter in m.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_output_surface_id.setText("")
        self.comboBox_processing_selector.setItemText(0, QCoreApplication.translate("Form", u"Transmission loss", None))
        self.comboBox_processing_selector.setItemText(1, QCoreApplication.translate("Form", u"Noise reduction", None))

        self.lineEdit_input_surface_id.setText("")
        self.label_2.setText(QCoreApplication.translate("Form", u"Plot type: ", None))
#if QT_CONFIG(tooltip)
        self.pushButton_export_data.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-size:10pt; font-weight:400;\">Press to export the current transmission loss or noise reduction</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_export_data.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_flip_selection.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-size:10pt; font-weight:400;\">Press to invert the selected IDs</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_flip_selection.setText("")
        self.comboBox_cutoff_frequency_options.setItemText(0, QCoreApplication.translate("Form", u"Disabled", None))
        self.comboBox_cutoff_frequency_options.setItemText(1, QCoreApplication.translate("Form", u"User-defined", None))
        self.comboBox_cutoff_frequency_options.setItemText(2, QCoreApplication.translate("Form", u"Automatic", None))

        self.comboBox_integration_method.setItemText(0, QCoreApplication.translate("Form", u"Nodal areas", None))
        self.comboBox_integration_method.setItemText(1, QCoreApplication.translate("Form", u"Surface integration", None))

        self.label_15.setText(QCoreApplication.translate("Form", u"Input ID: ", None))
        self.label_fc_combo_box.setText(QCoreApplication.translate("Form", u"<html><head/><body><p>Section diameter:</p></body></html>", None))
        self.label_unit_combo_box.setText(QCoreApplication.translate("Form", u"[mm]", None))
#if QT_CONFIG(tooltip)
        self.pushButton_help.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-size:10pt; font-weight:400;\">Press to get some help about the transmission loss or noise reduction</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_help.setText("")
    # retranslateUi



class TransmissionLossInputs_UI(QWidget, Ui_Form):
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
                                        - label_cutoff_frequency: QLabel
                                        - label_fc_line_edit: QLabel
                                        - label_unit_line_edit: QLabel
                                        - label_10: QLabel
                                        - label_integration_method: QLabel
                                        - lineEdit_cutoff_frequency: QLineEdit
                                        - lineEdit_output_surface_id: QLineEdit
                                        - comboBox_processing_selector: QComboBox
                                        - lineEdit_input_surface_id: QLineEdit
                                        - label_2: QLabel
                                        - pushButton_export_data: QPushButton
                                        - pushButton_flip_selection: QPushButton
                                        - comboBox_cutoff_frequency_options: QComboBox
                                        - comboBox_integration_method: QComboBox
                                        - label_15: QLabel
                                        - label_fc_combo_box: QLabel
                                        - comboBox_cutoff_frequency: QComboBox
                                        - label_unit_combo_box: QLabel
                                        - pushButton_help: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
