# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'user_defined_solution_steps_from_tabular_data_input.ui'
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
    QHeaderView, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QTableWidget, QTableWidgetItem,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(443, 643)
        self.gridLayout_2 = QGridLayout(Dialog)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(4, 4, 4, 4)
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.Box)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.frame_3 = QFrame(self.frame)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_7 = QGridLayout(self.frame_3)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.lineEdit_fmin = QLineEdit(self.frame_3)
        self.lineEdit_fmin.setObjectName(u"lineEdit_fmin")
        self.lineEdit_fmin.setMinimumSize(QSize(140, 28))
        self.lineEdit_fmin.setMaximumSize(QSize(180, 28))
        font = QFont()
        font.setFamilies([u"MS Shell Dlg 2"])
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        self.lineEdit_fmin.setFont(font)
        self.lineEdit_fmin.setStyleSheet(u"")
        self.lineEdit_fmin.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_7.addWidget(self.lineEdit_fmin, 0, 2, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_3, 0, 6, 1, 1)

        self.lineEdit_fstep = QLineEdit(self.frame_3)
        self.lineEdit_fstep.setObjectName(u"lineEdit_fstep")
        self.lineEdit_fstep.setMinimumSize(QSize(140, 28))
        self.lineEdit_fstep.setMaximumSize(QSize(180, 28))
        self.lineEdit_fstep.setFont(font)
        self.lineEdit_fstep.setStyleSheet(u"")
        self.lineEdit_fstep.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_7.addWidget(self.lineEdit_fstep, 2, 2, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_2, 0, 0, 1, 1)

        self.label_23 = QLabel(self.frame_3)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setMinimumSize(QSize(80, 28))
        self.label_23.setMaximumSize(QSize(100, 28))
        font1 = QFont()
        font1.setPointSize(10)
        font1.setItalic(False)
        font1.setKerning(False)
        self.label_23.setFont(font1)
        self.label_23.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_23, 1, 1, 1, 1)

        self.label_26 = QLabel(self.frame_3)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setMinimumSize(QSize(0, 28))
        self.label_26.setMaximumSize(QSize(32, 28))
        font2 = QFont()
        font2.setPointSize(10)
        font2.setItalic(False)
        self.label_26.setFont(font2)
        self.label_26.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_26, 2, 4, 1, 1)

        self.label_22 = QLabel(self.frame_3)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setMinimumSize(QSize(80, 28))
        self.label_22.setMaximumSize(QSize(100, 28))
        self.label_22.setFont(font1)
        self.label_22.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_22, 0, 1, 1, 1)

        self.label_25 = QLabel(self.frame_3)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setMinimumSize(QSize(0, 28))
        self.label_25.setMaximumSize(QSize(32, 28))
        self.label_25.setFont(font2)
        self.label_25.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_25, 1, 4, 1, 1)

        self.lineEdit_fmax = QLineEdit(self.frame_3)
        self.lineEdit_fmax.setObjectName(u"lineEdit_fmax")
        self.lineEdit_fmax.setMinimumSize(QSize(140, 28))
        self.lineEdit_fmax.setMaximumSize(QSize(180, 28))
        self.lineEdit_fmax.setFont(font)
        self.lineEdit_fmax.setStyleSheet(u"")
        self.lineEdit_fmax.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_7.addWidget(self.lineEdit_fmax, 1, 2, 1, 1)

        self.label_24 = QLabel(self.frame_3)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setMinimumSize(QSize(0, 28))
        self.label_24.setMaximumSize(QSize(32, 28))
        self.label_24.setFont(font2)
        self.label_24.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_24, 0, 4, 1, 1)

        self.label_21 = QLabel(self.frame_3)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setMinimumSize(QSize(80, 28))
        self.label_21.setMaximumSize(QSize(100, 28))
        self.label_21.setFont(font1)
        self.label_21.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_21, 2, 1, 1, 1)


        self.gridLayout_4.addWidget(self.frame_3, 0, 0, 1, 1)

        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_2)
        self.gridLayout_5.setSpacing(4)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(4, 4, 0, 4)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.pushButton_select_unselect_all = QPushButton(self.frame_2)
        self.pushButton_select_unselect_all.setObjectName(u"pushButton_select_unselect_all")
        self.pushButton_select_unselect_all.setMinimumSize(QSize(110, 30))
        self.pushButton_select_unselect_all.setMaximumSize(QSize(110, 30))
        self.pushButton_select_unselect_all.setFont(font)
        self.pushButton_select_unselect_all.setStyleSheet(u"")
        self.pushButton_select_unselect_all.setAutoDefault(False)

        self.gridLayout_5.addWidget(self.pushButton_select_unselect_all, 0, 1, 1, 1)


        self.gridLayout_4.addWidget(self.frame_2, 1, 0, 1, 1)

        self.tableWidget_frequencies = QTableWidget(self.frame)
        if (self.tableWidget_frequencies.columnCount() < 3):
            self.tableWidget_frequencies.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget_frequencies.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget_frequencies.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget_frequencies.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.tableWidget_frequencies.setObjectName(u"tableWidget_frequencies")
        self.tableWidget_frequencies.horizontalHeader().setVisible(True)
        self.tableWidget_frequencies.verticalHeader().setVisible(False)

        self.gridLayout_4.addWidget(self.tableWidget_frequencies, 2, 0, 1, 1)


        self.gridLayout_2.addWidget(self.frame, 1, 0, 1, 1)

        self.frame_buttons = QFrame(Dialog)
        self.frame_buttons.setObjectName(u"frame_buttons")
        self.frame_buttons.setMinimumSize(QSize(0, 48))
        self.frame_buttons.setMaximumSize(QSize(16777215, 48))
        self.frame_buttons.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_buttons.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_buttons)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setHorizontalSpacing(12)
        self.gridLayout_3.setVerticalSpacing(4)
        self.gridLayout_3.setContentsMargins(4, 4, 4, 4)
        self.pushButton_cancel = QPushButton(self.frame_buttons)
        self.pushButton_cancel.setObjectName(u"pushButton_cancel")
        self.pushButton_cancel.setMinimumSize(QSize(100, 30))
        self.pushButton_cancel.setMaximumSize(QSize(100, 30))
        self.pushButton_cancel.setFont(font)
        self.pushButton_cancel.setStyleSheet(u"")
        self.pushButton_cancel.setAutoDefault(False)

        self.gridLayout_3.addWidget(self.pushButton_cancel, 0, 0, 1, 1)

        self.pushButton_okay = QPushButton(self.frame_buttons)
        self.pushButton_okay.setObjectName(u"pushButton_okay")
        self.pushButton_okay.setMinimumSize(QSize(100, 30))
        self.pushButton_okay.setMaximumSize(QSize(100, 30))
        self.pushButton_okay.setFont(font)
        self.pushButton_okay.setStyleSheet(u"")
        self.pushButton_okay.setAutoDefault(False)

        self.gridLayout_3.addWidget(self.pushButton_okay, 0, 1, 1, 1)


        self.gridLayout_2.addWidget(self.frame_buttons, 2, 0, 1, 1)

        self.frame_title_2 = QFrame(Dialog)
        self.frame_title_2.setObjectName(u"frame_title_2")
        self.frame_title_2.setMinimumSize(QSize(0, 60))
        self.frame_title_2.setMaximumSize(QSize(16777215, 60))
        self.frame_title_2.setFrameShape(QFrame.Shape.Box)
        self.frame_title_2.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_title_2.setLineWidth(1)
        self.gridLayout_11 = QGridLayout(self.frame_title_2)
        self.gridLayout_11.setSpacing(2)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setContentsMargins(2, 2, 2, 2)
        self.label_title_3 = QLabel(self.frame_title_2)
        self.label_title_3.setObjectName(u"label_title_3")
        font3 = QFont()
        font3.setFamilies([u"MS Shell Dlg 2"])
        font3.setPointSize(11)
        font3.setBold(False)
        font3.setItalic(False)
        self.label_title_3.setFont(font3)
        self.label_title_3.setTextFormat(Qt.TextFormat.AutoText)
        self.label_title_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.label_title_3, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.frame_title_2, 0, 0, 1, 1)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_23.setText(QCoreApplication.translate("Dialog", u"Freq. max:", None))
        self.label_26.setText(QCoreApplication.translate("Dialog", u"[Hz]", None))
        self.label_22.setText(QCoreApplication.translate("Dialog", u"Freq. min:", None))
        self.label_25.setText(QCoreApplication.translate("Dialog", u"[Hz]", None))
        self.label_24.setText(QCoreApplication.translate("Dialog", u"[Hz]", None))
        self.label_21.setText(QCoreApplication.translate("Dialog", u"Freq. step:", None))
        self.pushButton_select_unselect_all.setText(QCoreApplication.translate("Dialog", u"Deselect all", None))
        ___qtablewidgetitem = self.tableWidget_frequencies.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Dialog", u"Index", None));
        ___qtablewidgetitem1 = self.tableWidget_frequencies.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Dialog", u"Frequency [Hz]", None));
        ___qtablewidgetitem2 = self.tableWidget_frequencies.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Dialog", u"Select", None));
        self.pushButton_cancel.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
        self.pushButton_okay.setText(QCoreApplication.translate("Dialog", u"Ok", None))
        self.label_title_3.setText(QCoreApplication.translate("Dialog", u"Solution steps configurator", None))
    # retranslateUi



class UserDefinedSolutionStepsFromTabularDataInput_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame: QFrame
                    - (Layout): QGridLayout
                            - frame_3: QFrame
                                - (Layout): QGridLayout
                                        - lineEdit_fmin: QLineEdit
                                        - lineEdit_fstep: QLineEdit
                                        - label_23: QLabel
                                        - label_26: QLabel
                                        - label_22: QLabel
                                        - label_25: QLabel
                                        - lineEdit_fmax: QLineEdit
                                        - label_24: QLabel
                                        - label_21: QLabel
                            - frame_2: QFrame
                                - (Layout): QGridLayout
                                        - pushButton_select_unselect_all: QPushButton
                            - tableWidget_frequencies: QTableWidget
                - frame_buttons: QFrame
                    - (Layout): QGridLayout
                            - pushButton_cancel: QPushButton
                            - pushButton_okay: QPushButton
                - frame_title_2: QFrame
                    - (Layout): QGridLayout
                            - label_title_3: QLabel
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
