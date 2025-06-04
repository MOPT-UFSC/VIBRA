# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'transmission_loss_inputs.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
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

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(400, 352)
        self.gridLayout_2 = QGridLayout(Form)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setHorizontalSpacing(6)
        self.gridLayout_2.setVerticalSpacing(4)
        self.gridLayout_2.setContentsMargins(4, 4, 4, 4)
        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(0, 30))
        self.label.setMaximumSize(QSize(452, 30))
        font = QFont()
        font.setFamilies([u"MS Shell Dlg 2"])
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        self.label.setFont(font)
        self.label.setTextFormat(Qt.AutoText)
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 1)

        self.frame_2 = QFrame(Form)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(0, 0))
        self.frame_2.setMaximumSize(QSize(520, 460))
        self.frame_2.setFrameShape(QFrame.Box)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_2)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(4, 4, 4, 4)
        self.frame_4 = QFrame(self.frame_2)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(0, 52))
        self.frame_4.setMaximumSize(QSize(16777215, 52))
        self.frame_4.setFrameShape(QFrame.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame_4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(6)
        self.gridLayout.setVerticalSpacing(2)
        self.gridLayout.setContentsMargins(2, 2, 2, 2)
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_3, 0, 0, 1, 1)

        self.label_10 = QLabel(self.frame_4)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(80, 30))
        self.label_10.setMaximumSize(QSize(80, 30))
        font1 = QFont()
        font1.setFamilies([u"MS Shell Dlg 2"])
        font1.setPointSize(10)
        font1.setBold(False)
        font1.setItalic(False)
        self.label_10.setFont(font1)
        self.label_10.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_10, 0, 1, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_4, 0, 4, 1, 1)

        self.lineEdit_output_surface_id = QLineEdit(self.frame_4)
        self.lineEdit_output_surface_id.setObjectName(u"lineEdit_output_surface_id")
        self.lineEdit_output_surface_id.setMinimumSize(QSize(140, 30))
        self.lineEdit_output_surface_id.setMaximumSize(QSize(140, 30))
        font2 = QFont()
        font2.setFamilies([u"Arial"])
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        self.lineEdit_output_surface_id.setFont(font2)
        self.lineEdit_output_surface_id.setStyleSheet(u"")
        self.lineEdit_output_surface_id.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_output_surface_id, 0, 2, 1, 1)

        self.pushButton_export_data = QPushButton(self.frame_4)
        self.pushButton_export_data.setObjectName(u"pushButton_export_data")
        self.pushButton_export_data.setMinimumSize(QSize(40, 30))
        self.pushButton_export_data.setMaximumSize(QSize(40, 30))
        font3 = QFont()
        font3.setFamilies([u"MS Shell Dlg 2"])
        font3.setPointSize(11)
        font3.setBold(True)
        font3.setItalic(False)
        self.pushButton_export_data.setFont(font3)
        self.pushButton_export_data.setStyleSheet(u"")
        icon = QIcon()
        icon.addFile(u":/icons/save_as.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_export_data.setIcon(icon)
        self.pushButton_export_data.setIconSize(QSize(20, 20))
        self.pushButton_export_data.setFlat(False)

        self.gridLayout.addWidget(self.pushButton_export_data, 0, 3, 1, 1)


        self.gridLayout_3.addWidget(self.frame_4, 0, 0, 1, 1)

        self.frame_3 = QFrame(self.frame_2)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(0, 52))
        self.frame_3.setMaximumSize(QSize(16777215, 52))
        self.frame_3.setFrameShape(QFrame.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.gridLayout_47 = QGridLayout(self.frame_3)
        self.gridLayout_47.setSpacing(2)
        self.gridLayout_47.setObjectName(u"gridLayout_47")
        self.gridLayout_47.setContentsMargins(2, 2, 2, 2)
        self.pushButton_plot_data = QPushButton(self.frame_3)
        self.pushButton_plot_data.setObjectName(u"pushButton_plot_data")
        self.pushButton_plot_data.setMinimumSize(QSize(120, 32))
        self.pushButton_plot_data.setMaximumSize(QSize(120, 32))
        self.pushButton_plot_data.setFont(font1)
        self.pushButton_plot_data.setStyleSheet(u"")
        self.pushButton_plot_data.setFlat(False)

        self.gridLayout_47.addWidget(self.pushButton_plot_data, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_3, 5, 0, 1, 1)

        self.frame_5 = QFrame(self.frame_2)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setMinimumSize(QSize(0, 52))
        self.frame_5.setMaximumSize(QSize(16777215, 52))
        self.frame_5.setFrameShape(QFrame.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.gridLayout_6 = QGridLayout(self.frame_5)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setHorizontalSpacing(6)
        self.gridLayout_6.setVerticalSpacing(2)
        self.gridLayout_6.setContentsMargins(2, 2, 2, 2)
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_5, 1, 4, 1, 1)

        self.comboBox_processing_selector = QComboBox(self.frame_5)
        self.comboBox_processing_selector.addItem("")
        self.comboBox_processing_selector.addItem("")
        self.comboBox_processing_selector.setObjectName(u"comboBox_processing_selector")
        self.comboBox_processing_selector.setMinimumSize(QSize(140, 30))
        self.comboBox_processing_selector.setMaximumSize(QSize(140, 30))
        font4 = QFont()
        font4.setPointSize(10)
        font4.setBold(False)
        font4.setItalic(False)
        self.comboBox_processing_selector.setFont(font4)
        self.comboBox_processing_selector.setStyleSheet(u"QComboBox::hover{border-radius: 4px; border-color: rgb(0, 170, 255); border-style: ridge; border-width: 2px}")

        self.gridLayout_6.addWidget(self.comboBox_processing_selector, 1, 2, 1, 1)

        self.label_2 = QLabel(self.frame_5)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(80, 30))
        self.label_2.setMaximumSize(QSize(80, 30))
        font5 = QFont()
        font5.setPointSize(10)
        self.label_2.setFont(font5)
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_2, 1, 1, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_6, 1, 0, 1, 1)

        self.frame_7 = QFrame(self.frame_5)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setMinimumSize(QSize(40, 30))
        self.frame_7.setMaximumSize(QSize(40, 30))
        self.frame_7.setFrameShape(QFrame.NoFrame)
        self.frame_7.setFrameShadow(QFrame.Raised)

        self.gridLayout_6.addWidget(self.frame_7, 1, 3, 1, 1)


        self.gridLayout_3.addWidget(self.frame_5, 3, 0, 1, 1)

        self.frame_8 = QFrame(self.frame_2)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setMinimumSize(QSize(0, 52))
        self.frame_8.setMaximumSize(QSize(16777215, 52))
        self.frame_8.setFrameShape(QFrame.NoFrame)
        self.frame_8.setFrameShadow(QFrame.Raised)
        self.gridLayout_15 = QGridLayout(self.frame_8)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.gridLayout_15.setHorizontalSpacing(6)
        self.gridLayout_15.setVerticalSpacing(2)
        self.gridLayout_15.setContentsMargins(2, 2, 2, 2)
        self.lineEdit_input_surface_id = QLineEdit(self.frame_8)
        self.lineEdit_input_surface_id.setObjectName(u"lineEdit_input_surface_id")
        self.lineEdit_input_surface_id.setMinimumSize(QSize(140, 30))
        self.lineEdit_input_surface_id.setMaximumSize(QSize(140, 30))
        self.lineEdit_input_surface_id.setFont(font2)
        self.lineEdit_input_surface_id.setStyleSheet(u"")
        self.lineEdit_input_surface_id.setAlignment(Qt.AlignCenter)

        self.gridLayout_15.addWidget(self.lineEdit_input_surface_id, 0, 2, 1, 1)

        self.label_15 = QLabel(self.frame_8)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setMinimumSize(QSize(80, 30))
        self.label_15.setMaximumSize(QSize(80, 30))
        self.label_15.setFont(font1)
        self.label_15.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_15.addWidget(self.label_15, 0, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_15.addItem(self.horizontalSpacer, 0, 4, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_15.addItem(self.horizontalSpacer_2, 0, 0, 1, 1)

        self.pushButton_flip_selection = QPushButton(self.frame_8)
        self.pushButton_flip_selection.setObjectName(u"pushButton_flip_selection")
        self.pushButton_flip_selection.setMinimumSize(QSize(40, 30))
        self.pushButton_flip_selection.setMaximumSize(QSize(40, 30))
        self.pushButton_flip_selection.setFont(font3)
        self.pushButton_flip_selection.setStyleSheet(u"")
        icon1 = QIcon()
        icon1.addFile(u":/icons/invert_icon.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_flip_selection.setIcon(icon1)
        self.pushButton_flip_selection.setIconSize(QSize(22, 22))
        self.pushButton_flip_selection.setFlat(False)

        self.gridLayout_15.addWidget(self.pushButton_flip_selection, 0, 3, 1, 1)


        self.gridLayout_3.addWidget(self.frame_8, 1, 0, 1, 1)

        self.frame_6 = QFrame(self.frame_2)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setMinimumSize(QSize(0, 52))
        self.frame_6.setMaximumSize(QSize(16777215, 52))
        self.frame_6.setFrameShape(QFrame.NoFrame)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.gridLayout_9 = QGridLayout(self.frame_6)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setHorizontalSpacing(6)
        self.gridLayout_9.setVerticalSpacing(2)
        self.gridLayout_9.setContentsMargins(2, 2, 2, 2)
        self.comboBox_integration_method = QComboBox(self.frame_6)
        self.comboBox_integration_method.addItem("")
        self.comboBox_integration_method.addItem("")
        self.comboBox_integration_method.setObjectName(u"comboBox_integration_method")
        self.comboBox_integration_method.setMinimumSize(QSize(140, 30))
        self.comboBox_integration_method.setMaximumSize(QSize(140, 30))
        self.comboBox_integration_method.setFont(font4)
        self.comboBox_integration_method.setStyleSheet(u"QComboBox::hover{border-radius: 4px; border-color: rgb(0, 170, 255); border-style: ridge; border-width: 2px}")

        self.gridLayout_9.addWidget(self.comboBox_integration_method, 1, 2, 1, 1)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer_11, 1, 4, 1, 1)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer_12, 1, 0, 1, 1)

        self.label_integration_method = QLabel(self.frame_6)
        self.label_integration_method.setObjectName(u"label_integration_method")
        self.label_integration_method.setMinimumSize(QSize(80, 30))
        self.label_integration_method.setMaximumSize(QSize(80, 30))
        self.label_integration_method.setFont(font5)
        self.label_integration_method.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_9.addWidget(self.label_integration_method, 1, 1, 1, 1)

        self.frame_9 = QFrame(self.frame_6)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setMinimumSize(QSize(40, 30))
        self.frame_9.setMaximumSize(QSize(40, 30))
        self.frame_9.setFrameShape(QFrame.NoFrame)
        self.frame_9.setFrameShadow(QFrame.Raised)

        self.gridLayout_9.addWidget(self.frame_9, 1, 3, 1, 1)


        self.gridLayout_3.addWidget(self.frame_6, 4, 0, 1, 1)


        self.gridLayout_2.addWidget(self.frame_2, 1, 0, 1, 1)


        self.retranslateUi(Form)

        self.comboBox_processing_selector.setCurrentIndex(0)
        self.comboBox_integration_method.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"Plot the transmission loss or noise reduction", None))
        self.label_10.setText(QCoreApplication.translate("Form", u"Output ID: ", None))
        self.lineEdit_output_surface_id.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_export_data.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-size:10pt; font-weight:400;\">Press to export the current transmission loss or noise reduction</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_export_data.setText("")
        self.pushButton_plot_data.setText(QCoreApplication.translate("Form", u"Plot data", None))
        self.comboBox_processing_selector.setItemText(0, QCoreApplication.translate("Form", u"Transmission loss", None))
        self.comboBox_processing_selector.setItemText(1, QCoreApplication.translate("Form", u"Noise reduction", None))

        self.label_2.setText(QCoreApplication.translate("Form", u"Plot type: ", None))
        self.lineEdit_input_surface_id.setText("")
        self.label_15.setText(QCoreApplication.translate("Form", u"Input ID: ", None))
#if QT_CONFIG(tooltip)
        self.pushButton_flip_selection.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-size:10pt; font-weight:400;\">Press to invert the selected IDs</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_flip_selection.setText("")
        self.comboBox_integration_method.setItemText(0, QCoreApplication.translate("Form", u"Nodal areas", None))
        self.comboBox_integration_method.setItemText(1, QCoreApplication.translate("Form", u"Surface integration", None))

        self.label_integration_method.setText(QCoreApplication.translate("Form", u"Method: ", None))
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
                            - frame_4: QFrame
                                - (Layout): QGridLayout
                                        - label_10: QLabel
                                        - lineEdit_output_surface_id: QLineEdit
                                        - pushButton_export_data: QPushButton
                            - frame_3: QFrame
                                - (Layout): QGridLayout
                                        - pushButton_plot_data: QPushButton
                            - frame_5: QFrame
                                - (Layout): QGridLayout
                                        - comboBox_processing_selector: QComboBox
                                        - label_2: QLabel
                                        - frame_7: QFrame
                            - frame_8: QFrame
                                - (Layout): QGridLayout
                                        - lineEdit_input_surface_id: QLineEdit
                                        - label_15: QLabel
                                        - pushButton_flip_selection: QPushButton
                            - frame_6: QFrame
                                - (Layout): QGridLayout
                                        - comboBox_integration_method: QComboBox
                                        - label_integration_method: QLabel
                                        - frame_9: QFrame
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
