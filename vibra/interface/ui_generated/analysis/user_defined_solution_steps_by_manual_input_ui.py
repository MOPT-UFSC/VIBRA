# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'user_defined_solution_steps_by_manual_input.ui'
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

from vibra.interface.formatters.icons import themed_icon

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(448, 644)
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
        self.gridLayout_4.setContentsMargins(4, 4, 4, 4)
        self.frame_4 = QFrame(self.frame)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_9 = QGridLayout(self.frame_4)
        self.gridLayout_9.setSpacing(4)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(4, 4, 4, 4)
        self.pushButton_reset = QPushButton(self.frame_4)
        self.pushButton_reset.setObjectName(u"pushButton_reset")
        self.pushButton_reset.setMinimumSize(QSize(36, 28))
        self.pushButton_reset.setMaximumSize(QSize(36, 28))
        font = QFont()
        font.setFamilies([u"MS Shell Dlg 2"])
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        self.pushButton_reset.setFont(font)
        self.pushButton_reset.setStyleSheet(u"")
        icon = themed_icon(u":/icons/reset_settings.png")
        self.pushButton_reset.setIcon(icon)
        self.pushButton_reset.setIconSize(QSize(20, 20))
        self.pushButton_reset.setAutoDefault(False)

        self.gridLayout_9.addWidget(self.pushButton_reset, 1, 7, 1, 1)

        self.label_28 = QLabel(self.frame_4)
        self.label_28.setObjectName(u"label_28")
        self.label_28.setMinimumSize(QSize(96, 28))
        self.label_28.setMaximumSize(QSize(96, 28))
        font1 = QFont()
        font1.setPointSize(10)
        font1.setItalic(False)
        font1.setKerning(False)
        self.label_28.setFont(font1)
        self.label_28.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_9.addWidget(self.label_28, 1, 1, 1, 1)

        self.lineEdit_solution_step = QLineEdit(self.frame_4)
        self.lineEdit_solution_step.setObjectName(u"lineEdit_solution_step")
        self.lineEdit_solution_step.setMinimumSize(QSize(180, 28))
        self.lineEdit_solution_step.setMaximumSize(QSize(180, 28))
        self.lineEdit_solution_step.setFont(font)
        self.lineEdit_solution_step.setStyleSheet(u"")
        self.lineEdit_solution_step.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_9.addWidget(self.lineEdit_solution_step, 1, 2, 1, 1)

        self.label_29 = QLabel(self.frame_4)
        self.label_29.setObjectName(u"label_29")
        self.label_29.setMinimumSize(QSize(0, 28))
        self.label_29.setMaximumSize(QSize(32, 28))
        font2 = QFont()
        font2.setPointSize(10)
        font2.setItalic(False)
        self.label_29.setFont(font2)
        self.label_29.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_9.addWidget(self.label_29, 1, 4, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer_4, 1, 0, 1, 1)

        self.pushButton_add = QPushButton(self.frame_4)
        self.pushButton_add.setObjectName(u"pushButton_add")
        self.pushButton_add.setMinimumSize(QSize(36, 28))
        self.pushButton_add.setMaximumSize(QSize(36, 28))
        self.pushButton_add.setFont(font)
        self.pushButton_add.setStyleSheet(u"")
        icon1 = themed_icon(u":/icons/add_notes.png")
        self.pushButton_add.setIcon(icon1)
        self.pushButton_add.setIconSize(QSize(20, 20))
        self.pushButton_add.setAutoDefault(False)

        self.gridLayout_9.addWidget(self.pushButton_add, 1, 6, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer, 1, 5, 1, 1)


        self.gridLayout_4.addWidget(self.frame_4, 0, 0, 1, 1)

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
        self.pushButton_okay = QPushButton(self.frame_buttons)
        self.pushButton_okay.setObjectName(u"pushButton_okay")
        self.pushButton_okay.setMinimumSize(QSize(100, 30))
        self.pushButton_okay.setMaximumSize(QSize(100, 30))
        self.pushButton_okay.setFont(font)
        self.pushButton_okay.setStyleSheet(u"")
        self.pushButton_okay.setCheckable(False)
        self.pushButton_okay.setAutoDefault(False)

        self.gridLayout_3.addWidget(self.pushButton_okay, 0, 1, 1, 1)

        self.pushButton_cancel = QPushButton(self.frame_buttons)
        self.pushButton_cancel.setObjectName(u"pushButton_cancel")
        self.pushButton_cancel.setMinimumSize(QSize(100, 30))
        self.pushButton_cancel.setMaximumSize(QSize(100, 30))
        self.pushButton_cancel.setFont(font)
        self.pushButton_cancel.setStyleSheet(u"")
        self.pushButton_cancel.setAutoDefault(False)

        self.gridLayout_3.addWidget(self.pushButton_cancel, 0, 0, 1, 1)


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
#if QT_CONFIG(tooltip)
        self.pushButton_reset.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Remove all solution steps</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_reset.setText("")
        self.label_28.setText(QCoreApplication.translate("Dialog", u"Solution step:", None))
        self.label_29.setText(QCoreApplication.translate("Dialog", u"[Hz]", None))
#if QT_CONFIG(tooltip)
        self.pushButton_add.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Add the solution step</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_add.setText("")
        ___qtablewidgetitem = self.tableWidget_frequencies.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Dialog", u"Index", None));
        ___qtablewidgetitem1 = self.tableWidget_frequencies.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Dialog", u"Frequency [Hz]", None));
        ___qtablewidgetitem2 = self.tableWidget_frequencies.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Dialog", u"Remove", None));
        self.pushButton_okay.setText(QCoreApplication.translate("Dialog", u"Ok", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
        self.label_title_3.setText(QCoreApplication.translate("Dialog", u"Solution steps configurator", None))
    # retranslateUi



class UserDefinedSolutionStepsByManualInput_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame: QFrame
                    - (Layout): QGridLayout
                            - frame_4: QFrame
                                - (Layout): QGridLayout
                                        - pushButton_reset: QPushButton
                                        - label_28: QLabel
                                        - lineEdit_solution_step: QLineEdit
                                        - label_29: QLabel
                                        - pushButton_add: QPushButton
                            - tableWidget_frequencies: QTableWidget
                - frame_buttons: QFrame
                    - (Layout): QGridLayout
                            - pushButton_okay: QPushButton
                            - pushButton_cancel: QPushButton
                - frame_title_2: QFrame
                    - (Layout): QGridLayout
                            - label_title_3: QLabel
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
