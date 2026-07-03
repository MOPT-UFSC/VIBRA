# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'export_model_results.ui'
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
    QWidget)

from vibra.interface.formatters.icons import Icon

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(540, 400)
        Dialog.setMinimumSize(QSize(540, 400))
        Dialog.setMaximumSize(QSize(540, 400))
        self.gridLayout_2 = QGridLayout(Dialog)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(4, 4, 4, 4)
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 48))
        self.frame.setMaximumSize(QSize(16777215, 48))
        self.frame.setSizeIncrement(QSize(0, 0))
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setLineWidth(1)
        self.gridLayout_4 = QGridLayout(self.frame)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(452, 30))
        self.label.setMaximumSize(QSize(452, 30))
        font = QFont()
        font.setFamilies([u"MS Shell Dlg 2"])
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setKerning(False)
        self.label.setFont(font)
        self.label.setTextFormat(Qt.AutoText)
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 1)

        self.frame_lower = QFrame(Dialog)
        self.frame_lower.setObjectName(u"frame_lower")
        self.frame_lower.setFrameShape(QFrame.Box)
        self.frame_lower.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_lower)
        self.gridLayout_3.setSpacing(2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(2, 2, 2, 2)
        self.frame_6 = QFrame(self.frame_lower)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.NoFrame)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.gridLayout_14 = QGridLayout(self.frame_6)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.gridLayout_14.setContentsMargins(12, -1, 12, -1)
        self.frame_17 = QFrame(self.frame_6)
        self.frame_17.setObjectName(u"frame_17")
        self.frame_17.setMinimumSize(QSize(0, 40))
        self.frame_17.setMaximumSize(QSize(16777215, 40))
        self.frame_17.setFrameShape(QFrame.NoFrame)
        self.frame_17.setFrameShadow(QFrame.Raised)
        self.gridLayout_12 = QGridLayout(self.frame_17)
        self.gridLayout_12.setSpacing(2)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setContentsMargins(2, 2, 2, 2)
        self.label_7 = QLabel(self.frame_17)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(125, 30))
        self.label_7.setMaximumSize(QSize(180, 30))
        font1 = QFont()
        font1.setFamilies([u"MS Shell Dlg 2"])
        font1.setPointSize(11)
        font1.setBold(False)
        font1.setItalic(False)
        self.label_7.setFont(font1)
        self.label_7.setFrameShape(QFrame.Box)
        self.label_7.setFrameShadow(QFrame.Raised)
        self.label_7.setAlignment(Qt.AlignCenter)

        self.gridLayout_12.addWidget(self.label_7, 0, 0, 1, 1)


        self.gridLayout_14.addWidget(self.frame_17, 1, 0, 1, 1)

        self.frame_13 = QFrame(self.frame_6)
        self.frame_13.setObjectName(u"frame_13")
        self.frame_13.setMinimumSize(QSize(0, 40))
        self.frame_13.setMaximumSize(QSize(16777215, 40))
        self.frame_13.setFrameShape(QFrame.NoFrame)
        self.frame_13.setFrameShadow(QFrame.Raised)
        self.gridLayout_11 = QGridLayout(self.frame_13)
        self.gridLayout_11.setSpacing(2)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setContentsMargins(2, 2, 2, 2)
        self.label_5 = QLabel(self.frame_13)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(125, 30))
        self.label_5.setMaximumSize(QSize(180, 30))
        self.label_5.setFont(font1)
        self.label_5.setFrameShape(QFrame.Box)
        self.label_5.setFrameShadow(QFrame.Raised)
        self.label_5.setAlignment(Qt.AlignCenter)

        self.gridLayout_11.addWidget(self.label_5, 0, 0, 1, 1)


        self.gridLayout_14.addWidget(self.frame_13, 3, 0, 1, 1)

        self.frame_14 = QFrame(self.frame_6)
        self.frame_14.setObjectName(u"frame_14")
        self.frame_14.setMaximumSize(QSize(16777215, 48))
        self.frame_14.setFrameShape(QFrame.NoFrame)
        self.frame_14.setFrameShadow(QFrame.Raised)
        self.gridLayout_15 = QGridLayout(self.frame_14)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.gridLayout_15.setContentsMargins(2, 2, 2, 2)
        self.lineEdit_save_results_path = QLineEdit(self.frame_14)
        self.lineEdit_save_results_path.setObjectName(u"lineEdit_save_results_path")
        self.lineEdit_save_results_path.setMinimumSize(QSize(0, 30))
        self.lineEdit_save_results_path.setMaximumSize(QSize(16777215, 30))
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        font2.setPointSize(8)
        font2.setBold(False)
        font2.setItalic(False)
        self.lineEdit_save_results_path.setFont(font2)
        self.lineEdit_save_results_path.setLayoutDirection(Qt.LeftToRight)
        self.lineEdit_save_results_path.setAlignment(Qt.AlignCenter)

        self.gridLayout_15.addWidget(self.lineEdit_save_results_path, 0, 1, 1, 1)

        self.pushButton_choose_folder_export = QPushButton(self.frame_14)
        self.pushButton_choose_folder_export.setObjectName(u"pushButton_choose_folder_export")
        self.pushButton_choose_folder_export.setMinimumSize(QSize(40, 30))
        self.pushButton_choose_folder_export.setMaximumSize(QSize(40, 30))
        font3 = QFont()
        font3.setFamilies([u"MS Shell Dlg 2"])
        font3.setPointSize(10)
        font3.setBold(False)
        font3.setItalic(False)
        self.pushButton_choose_folder_export.setFont(font3)
        self.pushButton_choose_folder_export.setStyleSheet(u"")
        icon = Icon(u":/icons/import.png")
        self.pushButton_choose_folder_export.setIcon(icon)
        self.pushButton_choose_folder_export.setIconSize(QSize(20, 20))

        self.gridLayout_15.addWidget(self.pushButton_choose_folder_export, 0, 2, 1, 1)

        self.frame_24 = QFrame(self.frame_14)
        self.frame_24.setObjectName(u"frame_24")
        self.frame_24.setMinimumSize(QSize(20, 0))
        self.frame_24.setFrameShape(QFrame.NoFrame)
        self.frame_24.setFrameShadow(QFrame.Raised)

        self.gridLayout_15.addWidget(self.frame_24, 0, 0, 1, 1)


        self.gridLayout_14.addWidget(self.frame_14, 4, 0, 1, 1)

        self.frame_23 = QFrame(self.frame_6)
        self.frame_23.setObjectName(u"frame_23")
        self.frame_23.setMaximumSize(QSize(16777215, 48))
        self.frame_23.setFrameShape(QFrame.NoFrame)
        self.frame_23.setFrameShadow(QFrame.Raised)
        self.gridLayout_13 = QGridLayout(self.frame_23)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_13.setContentsMargins(2, 2, 2, 2)
        self.frame_29 = QFrame(self.frame_23)
        self.frame_29.setObjectName(u"frame_29")
        self.frame_29.setMinimumSize(QSize(20, 0))
        self.frame_29.setFrameShape(QFrame.NoFrame)
        self.frame_29.setFrameShadow(QFrame.Raised)

        self.gridLayout_13.addWidget(self.frame_29, 0, 0, 1, 1)

        self.lineEdit_file_name = QLineEdit(self.frame_23)
        self.lineEdit_file_name.setObjectName(u"lineEdit_file_name")
        self.lineEdit_file_name.setMinimumSize(QSize(0, 30))
        self.lineEdit_file_name.setMaximumSize(QSize(16777215, 30))
        self.lineEdit_file_name.setFont(font3)
        self.lineEdit_file_name.setLayoutDirection(Qt.LeftToRight)
        self.lineEdit_file_name.setAlignment(Qt.AlignCenter)
        self.lineEdit_file_name.setClearButtonEnabled(True)

        self.gridLayout_13.addWidget(self.lineEdit_file_name, 0, 1, 1, 1)

        self.frame_3 = QFrame(self.frame_23)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(40, 30))
        self.frame_3.setMaximumSize(QSize(40, 30))
        self.frame_3.setFrameShape(QFrame.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Raised)

        self.gridLayout_13.addWidget(self.frame_3, 0, 2, 1, 1)


        self.gridLayout_14.addWidget(self.frame_23, 2, 0, 1, 1)

        self.frame_15 = QFrame(self.frame_6)
        self.frame_15.setObjectName(u"frame_15")
        self.frame_15.setMinimumSize(QSize(0, 48))
        self.frame_15.setMaximumSize(QSize(16777215, 48))
        self.frame_15.setFrameShape(QFrame.NoFrame)
        self.frame_15.setFrameShadow(QFrame.Raised)
        self.gridLayout_16 = QGridLayout(self.frame_15)
        self.gridLayout_16.setSpacing(2)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.gridLayout_16.setContentsMargins(2, 2, 2, 2)
        self.pushButton_export_results = QPushButton(self.frame_15)
        self.pushButton_export_results.setObjectName(u"pushButton_export_results")
        self.pushButton_export_results.setMinimumSize(QSize(132, 32))
        self.pushButton_export_results.setMaximumSize(QSize(140, 32))
        self.pushButton_export_results.setFont(font3)
        self.pushButton_export_results.setStyleSheet(u"")

        self.gridLayout_16.addWidget(self.pushButton_export_results, 0, 0, 1, 1)


        self.gridLayout_14.addWidget(self.frame_15, 5, 0, 1, 1)

        self.frame_2 = QFrame(self.frame_6)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame_2)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.label_data_information = QLabel(self.frame_2)
        self.label_data_information.setObjectName(u"label_data_information")
        self.label_data_information.setMaximumSize(QSize(460, 16777215))
        font4 = QFont()
        font4.setPointSize(11)
        self.label_data_information.setFont(font4)
        self.label_data_information.setFrameShape(QFrame.StyledPanel)
        self.label_data_information.setAlignment(Qt.AlignCenter)
        self.label_data_information.setWordWrap(True)
        self.label_data_information.setMargin(2)

        self.gridLayout.addWidget(self.label_data_information, 0, 0, 1, 1)


        self.gridLayout_14.addWidget(self.frame_2, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_6, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.frame_lower, 1, 0, 1, 1)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Export selected model result", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Export selected model result", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"Insert a file name", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"Choose a folder", None))
#if QT_CONFIG(whatsthis)
        self.pushButton_choose_folder_export.setWhatsThis(QCoreApplication.translate("Dialog", u"Choose a folder to export the model results.", None))
#endif // QT_CONFIG(whatsthis)
        self.pushButton_choose_folder_export.setText("")
        self.lineEdit_file_name.setText("")
        self.pushButton_export_results.setText(QCoreApplication.translate("Dialog", u"Export results", None))
        self.label_data_information.setText("")
    # retranslateUi



class ExportModelResults_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
                - frame_lower: QFrame
                    - (Layout): QGridLayout
                            - frame_6: QFrame
                                - (Layout): QGridLayout
                                        - frame_17: QFrame
                                            - (Layout): QGridLayout
                                                    - label_7: QLabel
                                        - frame_13: QFrame
                                            - (Layout): QGridLayout
                                                    - label_5: QLabel
                                        - frame_14: QFrame
                                            - (Layout): QGridLayout
                                                    - lineEdit_save_results_path: QLineEdit
                                                    - pushButton_choose_folder_export: QPushButton
                                                    - frame_24: QFrame
                                        - frame_23: QFrame
                                            - (Layout): QGridLayout
                                                    - frame_29: QFrame
                                                    - lineEdit_file_name: QLineEdit
                                                    - frame_3: QFrame
                                        - frame_15: QFrame
                                            - (Layout): QGridLayout
                                                    - pushButton_export_results: QPushButton
                                        - frame_2: QFrame
                                            - (Layout): QGridLayout
                                                    - label_data_information: QLabel
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
