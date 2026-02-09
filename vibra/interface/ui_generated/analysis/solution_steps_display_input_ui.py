# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'solution_steps_display_input.ui'
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
    QHeaderView, QLabel, QPushButton, QSizePolicy,
    QTableWidget, QTableWidgetItem, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(460, 420)
        self.gridLayout_2 = QGridLayout(Dialog)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(4, 4, 4, 4)
        self.frame_solution_steps_table = QFrame(Dialog)
        self.frame_solution_steps_table.setObjectName(u"frame_solution_steps_table")
        self.frame_solution_steps_table.setFrameShape(QFrame.Box)
        self.frame_solution_steps_table.setFrameShadow(QFrame.Raised)
        self.gridLayout_11 = QGridLayout(self.frame_solution_steps_table)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setContentsMargins(8, 8, 8, 8)
        self.tableWidget_solution_steps = QTableWidget(self.frame_solution_steps_table)
        if (self.tableWidget_solution_steps.columnCount() < 3):
            self.tableWidget_solution_steps.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget_solution_steps.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget_solution_steps.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget_solution_steps.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.tableWidget_solution_steps.setObjectName(u"tableWidget_solution_steps")
        self.tableWidget_solution_steps.verticalHeader().setVisible(False)

        self.gridLayout_11.addWidget(self.tableWidget_solution_steps, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.frame_solution_steps_table, 1, 0, 1, 1)

        self.frame_title = QFrame(Dialog)
        self.frame_title.setObjectName(u"frame_title")
        self.frame_title.setMinimumSize(QSize(0, 48))
        self.frame_title.setMaximumSize(QSize(16777215, 48))
        self.frame_title.setFrameShape(QFrame.Box)
        self.frame_title.setFrameShadow(QFrame.Raised)
        self.frame_title.setLineWidth(1)
        self.gridLayout = QGridLayout(self.frame_title)
        self.gridLayout.setSpacing(2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(2, 2, 2, 2)
        self.label_title = QLabel(self.frame_title)
        self.label_title.setObjectName(u"label_title")
        font = QFont()
        font.setFamilies([u"MS Shell Dlg 2"])
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        self.label_title.setFont(font)
        self.label_title.setTextFormat(Qt.AutoText)
        self.label_title.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_title, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.frame_title, 0, 0, 1, 1)

        self.frame_buttons = QFrame(Dialog)
        self.frame_buttons.setObjectName(u"frame_buttons")
        self.frame_buttons.setMinimumSize(QSize(0, 48))
        self.frame_buttons.setMaximumSize(QSize(16777215, 48))
        self.frame_buttons.setFrameShape(QFrame.NoFrame)
        self.frame_buttons.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_buttons)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setHorizontalSpacing(12)
        self.gridLayout_3.setVerticalSpacing(4)
        self.gridLayout_3.setContentsMargins(4, 4, 4, 4)
        self.pushButton_exit = QPushButton(self.frame_buttons)
        self.pushButton_exit.setObjectName(u"pushButton_exit")
        self.pushButton_exit.setMinimumSize(QSize(100, 30))
        self.pushButton_exit.setMaximumSize(QSize(100, 30))
        font1 = QFont()
        font1.setFamilies([u"MS Shell Dlg 2"])
        font1.setPointSize(10)
        font1.setBold(False)
        font1.setItalic(False)
        self.pushButton_exit.setFont(font1)
        self.pushButton_exit.setStyleSheet(u"")
        self.pushButton_exit.setAutoDefault(False)

        self.gridLayout_3.addWidget(self.pushButton_exit, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.frame_buttons, 2, 0, 1, 1)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        ___qtablewidgetitem = self.tableWidget_solution_steps.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Dialog", u"Solution step", None));
        ___qtablewidgetitem1 = self.tableWidget_solution_steps.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Dialog", u"Frequency [Hz]", None));
        ___qtablewidgetitem2 = self.tableWidget_solution_steps.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Dialog", u"Frequency spacing", None));
        self.label_title.setText(QCoreApplication.translate("Dialog", u"Table of solution steps", None))
        self.pushButton_exit.setText(QCoreApplication.translate("Dialog", u"Exit", None))
    # retranslateUi



class SolutionStepsDisplayInput_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame_solution_steps_table: QFrame
                    - (Layout): QGridLayout
                            - tableWidget_solution_steps: QTableWidget
                - frame_title: QFrame
                    - (Layout): QGridLayout
                            - label_title: QLabel
                - frame_buttons: QFrame
                    - (Layout): QGridLayout
                            - pushButton_exit: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
