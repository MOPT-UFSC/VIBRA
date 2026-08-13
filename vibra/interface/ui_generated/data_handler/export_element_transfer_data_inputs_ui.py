# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'export_element_transfer_data_inputs.ui'
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
    QGridLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QWidget)

from vibra.interface.formatters.icons import Icon

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setWindowModality(Qt.NonModal)
        Dialog.resize(400, 320)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(400, 320))
        Dialog.setMaximumSize(QSize(400, 320))
        Dialog.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.gridLayout_4 = QGridLayout(Dialog)
        self.gridLayout_4.setSpacing(4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(4, 4, 4, 4)
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 48))
        self.frame.setMaximumSize(QSize(520, 48))
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setFrameShadow(QFrame.Raised)
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
        font.setFamilies([u"MS Shell Dlg 2"])
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        self.label.setFont(font)
        self.label.setTextFormat(Qt.AutoText)
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout_4.addWidget(self.frame, 0, 0, 1, 1)

        self.frame_2 = QFrame(Dialog)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(0, 0))
        self.frame_2.setMaximumSize(QSize(520, 460))
        self.frame_2.setFrameShape(QFrame.Box)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setHorizontalSpacing(4)
        self.gridLayout_3.setVerticalSpacing(2)
        self.gridLayout_3.setContentsMargins(4, 4, 4, 4)
        self.frame_8 = QFrame(self.frame_2)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setMinimumSize(QSize(0, 52))
        self.frame_8.setMaximumSize(QSize(16777215, 16777215))
        self.frame_8.setFrameShape(QFrame.NoFrame)
        self.frame_8.setFrameShadow(QFrame.Raised)
        self.gridLayout_15 = QGridLayout(self.frame_8)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.gridLayout_15.setHorizontalSpacing(6)
        self.gridLayout_15.setVerticalSpacing(2)
        self.gridLayout_15.setContentsMargins(2, 2, 2, 2)
        self.pushButton_invert_selection = QPushButton(self.frame_8)
        self.pushButton_invert_selection.setObjectName(u"pushButton_invert_selection")
        self.pushButton_invert_selection.setMinimumSize(QSize(40, 30))
        self.pushButton_invert_selection.setMaximumSize(QSize(40, 30))
        font1 = QFont()
        font1.setFamilies([u"MS Shell Dlg 2"])
        font1.setPointSize(11)
        font1.setBold(True)
        font1.setItalic(False)
        self.pushButton_invert_selection.setFont(font1)
        self.pushButton_invert_selection.setStyleSheet(u"")
        icon = Icon(u":/icons/invert_icon.png")
        self.pushButton_invert_selection.setIcon(icon)
        self.pushButton_invert_selection.setIconSize(QSize(22, 22))
        self.pushButton_invert_selection.setFlat(False)

        self.gridLayout_15.addWidget(self.pushButton_invert_selection, 2, 3, 1, 1)

        self.label_15 = QLabel(self.frame_8)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setMinimumSize(QSize(120, 30))
        self.label_15.setMaximumSize(QSize(140, 30))
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        self.label_15.setFont(font2)
        self.label_15.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_15.addWidget(self.label_15, 3, 1, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_15.addItem(self.horizontalSpacer_3, 2, 4, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_15.addItem(self.horizontalSpacer_4, 2, 0, 1, 1)

        self.lineEdit_input_selected_id = QLineEdit(self.frame_8)
        self.lineEdit_input_selected_id.setObjectName(u"lineEdit_input_selected_id")
        self.lineEdit_input_selected_id.setMinimumSize(QSize(140, 30))
        self.lineEdit_input_selected_id.setMaximumSize(QSize(140, 30))
        font3 = QFont()
        font3.setPointSize(10)
        font3.setBold(False)
        font3.setItalic(False)
        self.lineEdit_input_selected_id.setFont(font3)
        self.lineEdit_input_selected_id.setStyleSheet(u"")
        self.lineEdit_input_selected_id.setAlignment(Qt.AlignCenter)

        self.gridLayout_15.addWidget(self.lineEdit_input_selected_id, 3, 2, 1, 1)

        self.lineEdit_output_selected_id = QLineEdit(self.frame_8)
        self.lineEdit_output_selected_id.setObjectName(u"lineEdit_output_selected_id")
        self.lineEdit_output_selected_id.setMinimumSize(QSize(140, 30))
        self.lineEdit_output_selected_id.setMaximumSize(QSize(140, 30))
        font4 = QFont()
        font4.setPointSize(10)
        self.lineEdit_output_selected_id.setFont(font4)
        self.lineEdit_output_selected_id.setStyleSheet(u"")
        self.lineEdit_output_selected_id.setAlignment(Qt.AlignCenter)

        self.gridLayout_15.addWidget(self.lineEdit_output_selected_id, 2, 2, 1, 1)

        self.label_10 = QLabel(self.frame_8)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(120, 30))
        self.label_10.setMaximumSize(QSize(140, 30))
        self.label_10.setFont(font2)
        self.label_10.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_15.addWidget(self.label_10, 2, 1, 1, 1)

        self.label_11 = QLabel(self.frame_8)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMinimumSize(QSize(120, 30))
        self.label_11.setMaximumSize(QSize(140, 30))
        self.label_11.setFont(font2)
        self.label_11.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_15.addWidget(self.label_11, 1, 1, 1, 1)

        self.comboBox_excitation_surface = QComboBox(self.frame_8)
        self.comboBox_excitation_surface.addItem("")
        self.comboBox_excitation_surface.addItem("")
        self.comboBox_excitation_surface.setObjectName(u"comboBox_excitation_surface")
        self.comboBox_excitation_surface.setMinimumSize(QSize(140, 30))
        self.comboBox_excitation_surface.setMaximumSize(QSize(140, 30))
        self.comboBox_excitation_surface.setFont(font4)
        self.comboBox_excitation_surface.setStyleSheet(u"")

        self.gridLayout_15.addWidget(self.comboBox_excitation_surface, 1, 2, 1, 1)


        self.gridLayout_3.addWidget(self.frame_8, 1, 0, 1, 1)

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
        self.pushButton_export_data = QPushButton(self.frame_3)
        self.pushButton_export_data.setObjectName(u"pushButton_export_data")
        self.pushButton_export_data.setMinimumSize(QSize(120, 32))
        self.pushButton_export_data.setMaximumSize(QSize(120, 32))
        self.pushButton_export_data.setFont(font2)
        self.pushButton_export_data.setStyleSheet(u"")
        self.pushButton_export_data.setIconSize(QSize(20, 20))
        self.pushButton_export_data.setFlat(False)

        self.gridLayout_47.addWidget(self.pushButton_export_data, 0, 1, 1, 1)

        self.pushButton_exit = QPushButton(self.frame_3)
        self.pushButton_exit.setObjectName(u"pushButton_exit")
        self.pushButton_exit.setMinimumSize(QSize(120, 32))
        self.pushButton_exit.setMaximumSize(QSize(120, 32))
        self.pushButton_exit.setFont(font2)
        self.pushButton_exit.setStyleSheet(u"")
        self.pushButton_exit.setIconSize(QSize(20, 20))
        self.pushButton_exit.setFlat(False)

        self.gridLayout_47.addWidget(self.pushButton_exit, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_3, 2, 0, 1, 1)

        self.frame_9 = QFrame(self.frame_2)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setMinimumSize(QSize(260, 68))
        self.frame_9.setMaximumSize(QSize(16777215, 68))
        self.frame_9.setFrameShape(QFrame.NoFrame)
        self.frame_9.setFrameShadow(QFrame.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_9)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setHorizontalSpacing(4)
        self.gridLayout_5.setVerticalSpacing(2)
        self.gridLayout_5.setContentsMargins(0, 4, 0, 0)
        self.pushButton_search = QPushButton(self.frame_9)
        self.pushButton_search.setObjectName(u"pushButton_search")
        self.pushButton_search.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton_search.sizePolicy().hasHeightForWidth())
        self.pushButton_search.setSizePolicy(sizePolicy1)
        self.pushButton_search.setMinimumSize(QSize(40, 30))
        self.pushButton_search.setMaximumSize(QSize(40, 30))
        self.pushButton_search.setFont(font2)
        self.pushButton_search.setStyleSheet(u"")
        icon1 = Icon(u":/icons/new_file.png")
        self.pushButton_search.setIcon(icon1)
        self.pushButton_search.setIconSize(QSize(20, 20))

        self.gridLayout_5.addWidget(self.pushButton_search, 1, 2, 1, 1)

        self.lineEdit_spreadsheet_path = QLineEdit(self.frame_9)
        self.lineEdit_spreadsheet_path.setObjectName(u"lineEdit_spreadsheet_path")
        self.lineEdit_spreadsheet_path.setEnabled(False)
        self.lineEdit_spreadsheet_path.setMinimumSize(QSize(280, 30))
        self.lineEdit_spreadsheet_path.setMaximumSize(QSize(280, 30))
        font5 = QFont()
        font5.setPointSize(9)
        font5.setBold(False)
        self.lineEdit_spreadsheet_path.setFont(font5)
        self.lineEdit_spreadsheet_path.setStyleSheet(u"")
        self.lineEdit_spreadsheet_path.setAlignment(Qt.AlignCenter)

        self.gridLayout_5.addWidget(self.lineEdit_spreadsheet_path, 1, 1, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_8, 1, 3, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_7, 1, 0, 1, 1)

        self.label_12 = QLabel(self.frame_9)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setMinimumSize(QSize(120, 20))
        self.label_12.setMaximumSize(QSize(800, 30))
        self.label_12.setFont(font2)
        self.label_12.setAlignment(Qt.AlignCenter)

        self.gridLayout_5.addWidget(self.label_12, 0, 1, 1, 1)


        self.gridLayout_3.addWidget(self.frame_9, 0, 0, 1, 1)


        self.gridLayout_4.addWidget(self.frame_2, 1, 0, 1, 1)

        QWidget.setTabOrder(self.lineEdit_input_selected_id, self.pushButton_export_data)

        self.retranslateUi(Dialog)

        self.comboBox_excitation_surface.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Plot frequency response", None))
#if QT_CONFIG(whatsthis)
        Dialog.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.label.setText(QCoreApplication.translate("Dialog", u"Export element transfer data", None))
#if QT_CONFIG(tooltip)
        self.pushButton_invert_selection.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:10pt; font-weight:400;\">Press to invert the selected IDs</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_invert_selection.setText("")
        self.label_15.setText(QCoreApplication.translate("Dialog", u"Input surface ID: ", None))
        self.lineEdit_input_selected_id.setText("")
        self.lineEdit_output_selected_id.setText("")
        self.label_10.setText(QCoreApplication.translate("Dialog", u"Output surface ID: ", None))
        self.label_11.setText(QCoreApplication.translate("Dialog", u"Excitation at: ", None))
        self.comboBox_excitation_surface.setItemText(0, QCoreApplication.translate("Dialog", u" Input surface ID", None))
        self.comboBox_excitation_surface.setItemText(1, QCoreApplication.translate("Dialog", u" Output surface ID", None))

#if QT_CONFIG(tooltip)
        self.comboBox_excitation_surface.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Choose the particle velocity component to export</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_export_data.setText(QCoreApplication.translate("Dialog", u"Export data", None))
        self.pushButton_exit.setText(QCoreApplication.translate("Dialog", u"Exit", None))
#if QT_CONFIG(tooltip)
        self.pushButton_search.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Choose a spreadsheet file to append data</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_search.setText("")
#if QT_CONFIG(tooltip)
        self.lineEdit_spreadsheet_path.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Spreadsheet file path to append data</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_12.setText(QCoreApplication.translate("Dialog", u"Choose an existing file to append data", None))
    # retranslateUi



class ExportElementTransferDataInputs_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
                - frame_2: QFrame
                    - (Layout): QGridLayout
                            - frame_8: QFrame
                                - (Layout): QGridLayout
                                        - pushButton_invert_selection: QPushButton
                                        - label_15: QLabel
                                        - lineEdit_input_selected_id: QLineEdit
                                        - lineEdit_output_selected_id: QLineEdit
                                        - label_10: QLabel
                                        - label_11: QLabel
                                        - comboBox_excitation_surface: QComboBox
                            - frame_3: QFrame
                                - (Layout): QGridLayout
                                        - pushButton_export_data: QPushButton
                                        - pushButton_exit: QPushButton
                            - frame_9: QFrame
                                - (Layout): QGridLayout
                                        - pushButton_search: QPushButton
                                        - lineEdit_spreadsheet_path: QLineEdit
                                        - label_12: QLabel
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
