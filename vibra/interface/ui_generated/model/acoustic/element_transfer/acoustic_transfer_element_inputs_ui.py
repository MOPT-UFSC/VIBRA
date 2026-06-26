# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'acoustic_transfer_element_inputs.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QGridLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QTabWidget, QWidget)

from vibra.interface.formatters.icons import themed_icon

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setWindowModality(Qt.WindowModality.NonModal)
        Dialog.resize(400, 474)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(400, 440))
        Dialog.setMaximumSize(QSize(400, 480))
        Dialog.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        self.gridLayout_4 = QGridLayout(Dialog)
        self.gridLayout_4.setSpacing(4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(4, 4, 4, 4)
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 48))
        self.frame.setMaximumSize(QSize(520, 48))
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
        font.setFamilies([u"MS Shell Dlg 2"])
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        self.label.setFont(font)
        self.label.setTextFormat(Qt.TextFormat.AutoText)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout_4.addWidget(self.frame, 0, 0, 1, 1)

        self.frame_2 = QFrame(Dialog)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(0, 0))
        self.frame_2.setMaximumSize(QSize(520, 460))
        self.frame_2.setFrameShape(QFrame.Shape.Box)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setHorizontalSpacing(4)
        self.gridLayout_3.setVerticalSpacing(2)
        self.gridLayout_3.setContentsMargins(4, 4, 4, 4)
        self.tabWidget_main = QTabWidget(self.frame_2)
        self.tabWidget_main.setObjectName(u"tabWidget_main")
        font1 = QFont()
        font1.setPointSize(10)
        self.tabWidget_main.setFont(font1)
        self.tab_setup = QWidget()
        self.tab_setup.setObjectName(u"tab_setup")
        self.gridLayout_6 = QGridLayout(self.tab_setup)
        self.gridLayout_6.setSpacing(4)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(4, 4, 4, 4)
        self.frame_10 = QFrame(self.tab_setup)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setMinimumSize(QSize(260, 48))
        self.frame_10.setMaximumSize(QSize(16777215, 48))
        self.frame_10.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_10.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_7 = QGridLayout(self.frame_10)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setHorizontalSpacing(4)
        self.gridLayout_7.setVerticalSpacing(2)
        self.gridLayout_7.setContentsMargins(0, 4, 0, 0)
        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_9, 0, 0, 1, 1)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_10, 0, 3, 1, 1)

        self.lineEdit_spreadsheet_path = QLineEdit(self.frame_10)
        self.lineEdit_spreadsheet_path.setObjectName(u"lineEdit_spreadsheet_path")
        self.lineEdit_spreadsheet_path.setEnabled(False)
        self.lineEdit_spreadsheet_path.setMinimumSize(QSize(280, 30))
        self.lineEdit_spreadsheet_path.setMaximumSize(QSize(280, 30))
        font2 = QFont()
        font2.setPointSize(9)
        font2.setBold(False)
        self.lineEdit_spreadsheet_path.setFont(font2)
        self.lineEdit_spreadsheet_path.setStyleSheet(u"")
        self.lineEdit_spreadsheet_path.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_7.addWidget(self.lineEdit_spreadsheet_path, 0, 1, 1, 1)

        self.pushButton_search = QPushButton(self.frame_10)
        self.pushButton_search.setObjectName(u"pushButton_search")
        self.pushButton_search.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton_search.sizePolicy().hasHeightForWidth())
        self.pushButton_search.setSizePolicy(sizePolicy1)
        self.pushButton_search.setMinimumSize(QSize(40, 30))
        self.pushButton_search.setMaximumSize(QSize(40, 30))
        font3 = QFont()
        font3.setFamilies([u"MS Shell Dlg 2"])
        font3.setPointSize(10)
        font3.setBold(False)
        font3.setItalic(False)
        self.pushButton_search.setFont(font3)
        self.pushButton_search.setStyleSheet(u"")
        icon = themed_icon(u":/icons/new_file.png")
        self.pushButton_search.setIcon(icon)
        self.pushButton_search.setIconSize(QSize(20, 20))
        self.pushButton_search.setAutoDefault(False)

        self.gridLayout_7.addWidget(self.pushButton_search, 0, 2, 1, 1)


        self.gridLayout_6.addWidget(self.frame_10, 0, 0, 1, 1)

        self.frame_11 = QFrame(self.tab_setup)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setMinimumSize(QSize(0, 52))
        self.frame_11.setMaximumSize(QSize(16777215, 16777215))
        self.frame_11.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_11.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_16 = QGridLayout(self.frame_11)
        self.gridLayout_16.setSpacing(6)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.gridLayout_16.setContentsMargins(2, 2, 2, 2)
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_16.addItem(self.horizontalSpacer_4, 6, 5, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_16.addItem(self.horizontalSpacer_3, 6, 1, 1, 1)

        self.lineEdit_output_selected_id = QLineEdit(self.frame_11)
        self.lineEdit_output_selected_id.setObjectName(u"lineEdit_output_selected_id")
        self.lineEdit_output_selected_id.setMinimumSize(QSize(140, 30))
        self.lineEdit_output_selected_id.setMaximumSize(QSize(140, 30))
        self.lineEdit_output_selected_id.setFont(font1)
        self.lineEdit_output_selected_id.setStyleSheet(u"")
        self.lineEdit_output_selected_id.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_16.addWidget(self.lineEdit_output_selected_id, 2, 3, 1, 1)

        self.label_2 = QLabel(self.frame_11)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(0, 32))
        self.label_2.setMaximumSize(QSize(16777215, 32))
        font4 = QFont()
        font4.setPointSize(10)
        font4.setBold(False)
        self.label_2.setFont(font4)
        self.label_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_16.addWidget(self.label_2, 6, 2, 1, 3)

        self.label_11 = QLabel(self.frame_11)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMinimumSize(QSize(120, 30))
        self.label_11.setMaximumSize(QSize(140, 30))
        self.label_11.setFont(font3)
        self.label_11.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_16.addWidget(self.label_11, 2, 2, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_16.addItem(self.verticalSpacer, 5, 2, 1, 3)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_16.addItem(self.verticalSpacer_2, 8, 2, 1, 3)

        self.frame_3 = QFrame(self.frame_11)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.frame_3)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_22 = QLabel(self.frame_3)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setMinimumSize(QSize(100, 30))
        self.label_22.setMaximumSize(QSize(140, 30))
        self.label_22.setFont(font3)
        self.label_22.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_22, 0, 0, 1, 1)

        self.lineEdit_fmin = QLineEdit(self.frame_3)
        self.lineEdit_fmin.setObjectName(u"lineEdit_fmin")
        self.lineEdit_fmin.setMinimumSize(QSize(140, 30))
        self.lineEdit_fmin.setMaximumSize(QSize(140, 30))
        self.lineEdit_fmin.setFont(font3)
        self.lineEdit_fmin.setStyleSheet(u"")
        self.lineEdit_fmin.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_fmin, 0, 1, 1, 1)

        self.label_24 = QLabel(self.frame_3)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setMinimumSize(QSize(30, 30))
        self.label_24.setMaximumSize(QSize(60, 30))
        self.label_24.setFont(font3)
        self.label_24.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_24, 0, 2, 1, 1)

        self.label_23 = QLabel(self.frame_3)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setMinimumSize(QSize(100, 30))
        self.label_23.setMaximumSize(QSize(140, 30))
        self.label_23.setFont(font3)
        self.label_23.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_23, 1, 0, 1, 1)

        self.lineEdit_fmax = QLineEdit(self.frame_3)
        self.lineEdit_fmax.setObjectName(u"lineEdit_fmax")
        self.lineEdit_fmax.setMinimumSize(QSize(140, 30))
        self.lineEdit_fmax.setMaximumSize(QSize(140, 30))
        self.lineEdit_fmax.setFont(font3)
        self.lineEdit_fmax.setStyleSheet(u"")
        self.lineEdit_fmax.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_fmax, 1, 1, 1, 1)

        self.label_25 = QLabel(self.frame_3)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setMinimumSize(QSize(30, 30))
        self.label_25.setMaximumSize(QSize(60, 30))
        self.label_25.setFont(font3)
        self.label_25.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_25, 1, 2, 1, 1)

        self.label_21 = QLabel(self.frame_3)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setMinimumSize(QSize(100, 30))
        self.label_21.setMaximumSize(QSize(140, 30))
        self.label_21.setFont(font3)
        self.label_21.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_21, 2, 0, 1, 1)

        self.lineEdit_fstep = QLineEdit(self.frame_3)
        self.lineEdit_fstep.setObjectName(u"lineEdit_fstep")
        self.lineEdit_fstep.setMinimumSize(QSize(140, 30))
        self.lineEdit_fstep.setMaximumSize(QSize(140, 30))
        self.lineEdit_fstep.setFont(font3)
        self.lineEdit_fstep.setStyleSheet(u"")
        self.lineEdit_fstep.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_fstep, 2, 1, 1, 1)

        self.label_26 = QLabel(self.frame_3)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setMinimumSize(QSize(30, 30))
        self.label_26.setMaximumSize(QSize(60, 30))
        self.label_26.setFont(font3)
        self.label_26.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_26, 2, 2, 1, 1)


        self.gridLayout_16.addWidget(self.frame_3, 7, 2, 1, 3)

        self.label_16 = QLabel(self.frame_11)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setMinimumSize(QSize(120, 30))
        self.label_16.setMaximumSize(QSize(140, 30))
        self.label_16.setFont(font3)
        self.label_16.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_16.addWidget(self.label_16, 1, 2, 1, 1)

        self.lineEdit_input_selected_id = QLineEdit(self.frame_11)
        self.lineEdit_input_selected_id.setObjectName(u"lineEdit_input_selected_id")
        self.lineEdit_input_selected_id.setMinimumSize(QSize(140, 30))
        self.lineEdit_input_selected_id.setMaximumSize(QSize(140, 30))
        font5 = QFont()
        font5.setPointSize(10)
        font5.setBold(False)
        font5.setItalic(False)
        self.lineEdit_input_selected_id.setFont(font5)
        self.lineEdit_input_selected_id.setStyleSheet(u"")
        self.lineEdit_input_selected_id.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_16.addWidget(self.lineEdit_input_selected_id, 1, 3, 1, 1)

        self.pushButton_invert_selection = QPushButton(self.frame_11)
        self.pushButton_invert_selection.setObjectName(u"pushButton_invert_selection")
        self.pushButton_invert_selection.setMinimumSize(QSize(40, 30))
        self.pushButton_invert_selection.setMaximumSize(QSize(40, 30))
        font6 = QFont()
        font6.setFamilies([u"MS Shell Dlg 2"])
        font6.setPointSize(11)
        font6.setBold(True)
        font6.setItalic(False)
        self.pushButton_invert_selection.setFont(font6)
        self.pushButton_invert_selection.setStyleSheet(u"")
        icon1 = themed_icon(u":/icons/invert_icon.png")
        self.pushButton_invert_selection.setIcon(icon1)
        self.pushButton_invert_selection.setIconSize(QSize(22, 22))
        self.pushButton_invert_selection.setAutoDefault(False)
        self.pushButton_invert_selection.setFlat(False)

        self.gridLayout_16.addWidget(self.pushButton_invert_selection, 1, 4, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_16.addItem(self.horizontalSpacer_6, 1, 5, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_16.addItem(self.horizontalSpacer_5, 1, 1, 1, 1)


        self.gridLayout_6.addWidget(self.frame_11, 1, 0, 1, 1)

        self.frame_4 = QFrame(self.tab_setup)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(0, 52))
        self.frame_4.setMaximumSize(QSize(16777215, 52))
        self.frame_4.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_48 = QGridLayout(self.frame_4)
        self.gridLayout_48.setSpacing(2)
        self.gridLayout_48.setObjectName(u"gridLayout_48")
        self.gridLayout_48.setContentsMargins(2, 2, 2, 2)
        self.pushButton_process_data = QPushButton(self.frame_4)
        self.pushButton_process_data.setObjectName(u"pushButton_process_data")
        self.pushButton_process_data.setMinimumSize(QSize(120, 32))
        self.pushButton_process_data.setMaximumSize(QSize(120, 32))
        self.pushButton_process_data.setFont(font3)
        self.pushButton_process_data.setStyleSheet(u"")
        self.pushButton_process_data.setIconSize(QSize(20, 20))
        self.pushButton_process_data.setAutoDefault(False)
        self.pushButton_process_data.setFlat(False)

        self.gridLayout_48.addWidget(self.pushButton_process_data, 0, 1, 1, 1)

        self.pushButton_exit = QPushButton(self.frame_4)
        self.pushButton_exit.setObjectName(u"pushButton_exit")
        self.pushButton_exit.setMinimumSize(QSize(120, 32))
        self.pushButton_exit.setMaximumSize(QSize(120, 32))
        self.pushButton_exit.setFont(font3)
        self.pushButton_exit.setStyleSheet(u"")
        self.pushButton_exit.setIconSize(QSize(20, 20))
        self.pushButton_exit.setAutoDefault(False)
        self.pushButton_exit.setFlat(False)

        self.gridLayout_48.addWidget(self.pushButton_exit, 0, 0, 1, 1)


        self.gridLayout_6.addWidget(self.frame_4, 2, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_setup, "")
        self.tab_list = QWidget()
        self.tab_list.setObjectName(u"tab_list")
        self.tabWidget_main.addTab(self.tab_list, "")

        self.gridLayout_3.addWidget(self.tabWidget_main, 0, 0, 1, 1)


        self.gridLayout_4.addWidget(self.frame_2, 1, 0, 1, 1)

        QWidget.setTabOrder(self.lineEdit_output_selected_id, self.lineEdit_fmin)
        QWidget.setTabOrder(self.lineEdit_fmin, self.lineEdit_fmax)
        QWidget.setTabOrder(self.lineEdit_fmax, self.lineEdit_fstep)
        QWidget.setTabOrder(self.lineEdit_fstep, self.lineEdit_spreadsheet_path)
        QWidget.setTabOrder(self.lineEdit_spreadsheet_path, self.tabWidget_main)
        QWidget.setTabOrder(self.tabWidget_main, self.pushButton_search)
        QWidget.setTabOrder(self.pushButton_search, self.pushButton_process_data)
        QWidget.setTabOrder(self.pushButton_process_data, self.pushButton_exit)

        self.retranslateUi(Dialog)

        self.tabWidget_main.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Plot frequency response", None))
#if QT_CONFIG(whatsthis)
        Dialog.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.label.setText(QCoreApplication.translate("Dialog", u"Process acoustic transfer element data", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_spreadsheet_path.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Spreadsheet file path to append data</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.pushButton_search.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Choose a spreadsheet file to append data</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_search.setText("")
        self.lineEdit_output_selected_id.setText("")
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Harmonic analysis frequency setup", None))
        self.label_11.setText(QCoreApplication.translate("Dialog", u"Output surface ID:", None))
        self.label_22.setText(QCoreApplication.translate("Dialog", u"Freq. min:", None))
        self.lineEdit_fmin.setText(QCoreApplication.translate("Dialog", u"5", None))
        self.label_24.setText(QCoreApplication.translate("Dialog", u"[Hz]", None))
        self.label_23.setText(QCoreApplication.translate("Dialog", u"Freq. max:", None))
        self.lineEdit_fmax.setText(QCoreApplication.translate("Dialog", u"1400", None))
        self.label_25.setText(QCoreApplication.translate("Dialog", u"[Hz]", None))
        self.label_21.setText(QCoreApplication.translate("Dialog", u"Freq. step:", None))
        self.lineEdit_fstep.setText(QCoreApplication.translate("Dialog", u"5", None))
        self.label_26.setText(QCoreApplication.translate("Dialog", u"[Hz]", None))
        self.label_16.setText(QCoreApplication.translate("Dialog", u"Input surface ID:", None))
        self.lineEdit_input_selected_id.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_invert_selection.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:10pt; font-weight:400;\">Press to invert the selected IDs</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_invert_selection.setText("")
        self.pushButton_process_data.setText(QCoreApplication.translate("Dialog", u"Process data", None))
        self.pushButton_exit.setText(QCoreApplication.translate("Dialog", u"Exit", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_setup), QCoreApplication.translate("Dialog", u"Setup", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_list), QCoreApplication.translate("Dialog", u"List", None))
    # retranslateUi



class AcousticTransferElementInputs_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
                - frame_2: QFrame
                    - (Layout): QGridLayout
                            - tabWidget_main: QTabWidget
                                - tab_setup: QWidget
                                    - (Layout): QGridLayout
                                            - frame_10: QFrame
                                                - (Layout): QGridLayout
                                                        - lineEdit_spreadsheet_path: QLineEdit
                                                        - pushButton_search: QPushButton
                                            - frame_11: QFrame
                                                - (Layout): QGridLayout
                                                        - lineEdit_output_selected_id: QLineEdit
                                                        - label_2: QLabel
                                                        - label_11: QLabel
                                                        - frame_3: QFrame
                                                            - (Layout): QGridLayout
                                                                    - label_22: QLabel
                                                                    - lineEdit_fmin: QLineEdit
                                                                    - label_24: QLabel
                                                                    - label_23: QLabel
                                                                    - lineEdit_fmax: QLineEdit
                                                                    - label_25: QLabel
                                                                    - label_21: QLabel
                                                                    - lineEdit_fstep: QLineEdit
                                                                    - label_26: QLabel
                                                        - label_16: QLabel
                                                        - lineEdit_input_selected_id: QLineEdit
                                                        - pushButton_invert_selection: QPushButton
                                            - frame_4: QFrame
                                                - (Layout): QGridLayout
                                                        - pushButton_process_data: QPushButton
                                                        - pushButton_exit: QPushButton
                                - tab_list: QWidget
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
