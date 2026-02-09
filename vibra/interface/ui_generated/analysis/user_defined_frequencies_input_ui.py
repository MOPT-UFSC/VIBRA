# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'user_defined_solution_steps_input.ui'
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
    QSizePolicy, QSpacerItem, QTabWidget, QTableWidget,
    QTableWidgetItem, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(500, 666)
        self.gridLayout_2 = QGridLayout(Dialog)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(4, 4, 4, 4)
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.tabWidget = QTabWidget(self.frame)
        self.tabWidget.setObjectName(u"tabWidget")
        font = QFont()
        font.setPointSize(10)
        self.tabWidget.setFont(font)
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.gridLayout_8 = QGridLayout(self.tab_2)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.tableWidget_frequencies_2 = QTableWidget(self.tab_2)
        if (self.tableWidget_frequencies_2.columnCount() < 3):
            self.tableWidget_frequencies_2.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget_frequencies_2.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget_frequencies_2.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget_frequencies_2.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.tableWidget_frequencies_2.setObjectName(u"tableWidget_frequencies_2")
        self.tableWidget_frequencies_2.horizontalHeader().setVisible(False)
        self.tableWidget_frequencies_2.verticalHeader().setVisible(False)

        self.gridLayout_8.addWidget(self.tableWidget_frequencies_2, 1, 0, 1, 1)

        self.frame_4 = QFrame(self.tab_2)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.gridLayout_9 = QGridLayout(self.frame_4)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.label_28 = QLabel(self.frame_4)
        self.label_28.setObjectName(u"label_28")
        self.label_28.setMinimumSize(QSize(80, 28))
        self.label_28.setMaximumSize(QSize(120, 28))
        font1 = QFont()
        font1.setPointSize(10)
        font1.setItalic(False)
        font1.setKerning(False)
        self.label_28.setFont(font1)
        self.label_28.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_9.addWidget(self.label_28, 1, 1, 1, 1)

        self.label_29 = QLabel(self.frame_4)
        self.label_29.setObjectName(u"label_29")
        self.label_29.setMinimumSize(QSize(0, 28))
        self.label_29.setMaximumSize(QSize(32, 28))
        font2 = QFont()
        font2.setPointSize(10)
        font2.setItalic(False)
        self.label_29.setFont(font2)
        self.label_29.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_9.addWidget(self.label_29, 1, 4, 1, 1)

        self.pushButton_add_2 = QPushButton(self.frame_4)
        self.pushButton_add_2.setObjectName(u"pushButton_add_2")
        self.pushButton_add_2.setMinimumSize(QSize(40, 28))
        self.pushButton_add_2.setMaximumSize(QSize(40, 28))
        font3 = QFont()
        font3.setFamilies([u"MS Shell Dlg 2"])
        font3.setPointSize(10)
        font3.setBold(False)
        font3.setItalic(False)
        self.pushButton_add_2.setFont(font3)
        self.pushButton_add_2.setStyleSheet(u"")
        icon = QIcon()
        icon.addFile(u":/icons/plus-thick.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_add_2.setIcon(icon)
        self.pushButton_add_2.setIconSize(QSize(18, 18))
        self.pushButton_add_2.setAutoDefault(False)

        self.gridLayout_9.addWidget(self.pushButton_add_2, 1, 5, 1, 1)

        self.lineEdit_fstep_2 = QLineEdit(self.frame_4)
        self.lineEdit_fstep_2.setObjectName(u"lineEdit_fstep_2")
        self.lineEdit_fstep_2.setMinimumSize(QSize(140, 28))
        self.lineEdit_fstep_2.setMaximumSize(QSize(180, 28))
        self.lineEdit_fstep_2.setFont(font3)
        self.lineEdit_fstep_2.setStyleSheet(u"")
        self.lineEdit_fstep_2.setAlignment(Qt.AlignCenter)

        self.gridLayout_9.addWidget(self.lineEdit_fstep_2, 1, 2, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer_5, 1, 6, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer_4, 1, 0, 1, 1)


        self.gridLayout_8.addWidget(self.frame_4, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.gridLayout_6 = QGridLayout(self.tab)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.tableWidget_frequencies = QTableWidget(self.tab)
        if (self.tableWidget_frequencies.columnCount() < 3):
            self.tableWidget_frequencies.setColumnCount(3)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget_frequencies.setHorizontalHeaderItem(0, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget_frequencies.setHorizontalHeaderItem(1, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget_frequencies.setHorizontalHeaderItem(2, __qtablewidgetitem5)
        self.tableWidget_frequencies.setObjectName(u"tableWidget_frequencies")
        self.tableWidget_frequencies.horizontalHeader().setVisible(False)
        self.tableWidget_frequencies.verticalHeader().setVisible(False)

        self.gridLayout_6.addWidget(self.tableWidget_frequencies, 2, 0, 1, 1)

        self.frame_3 = QFrame(self.tab)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.gridLayout_7 = QGridLayout(self.frame_3)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.label_24 = QLabel(self.frame_3)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setMinimumSize(QSize(0, 28))
        self.label_24.setMaximumSize(QSize(32, 28))
        self.label_24.setFont(font2)
        self.label_24.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_24, 0, 4, 1, 1)

        self.label_21 = QLabel(self.frame_3)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setMinimumSize(QSize(80, 28))
        self.label_21.setMaximumSize(QSize(100, 28))
        self.label_21.setFont(font1)
        self.label_21.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_21, 2, 1, 1, 1)

        self.label_26 = QLabel(self.frame_3)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setMinimumSize(QSize(0, 28))
        self.label_26.setMaximumSize(QSize(32, 28))
        self.label_26.setFont(font2)
        self.label_26.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_26, 2, 4, 1, 1)

        self.label_22 = QLabel(self.frame_3)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setMinimumSize(QSize(80, 28))
        self.label_22.setMaximumSize(QSize(100, 28))
        self.label_22.setFont(font1)
        self.label_22.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_22, 0, 1, 1, 1)

        self.label_23 = QLabel(self.frame_3)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setMinimumSize(QSize(80, 28))
        self.label_23.setMaximumSize(QSize(100, 28))
        self.label_23.setFont(font1)
        self.label_23.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_23, 1, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_2, 0, 0, 1, 1)

        self.lineEdit_fmax = QLineEdit(self.frame_3)
        self.lineEdit_fmax.setObjectName(u"lineEdit_fmax")
        self.lineEdit_fmax.setMinimumSize(QSize(140, 28))
        self.lineEdit_fmax.setMaximumSize(QSize(180, 28))
        self.lineEdit_fmax.setFont(font3)
        self.lineEdit_fmax.setStyleSheet(u"")
        self.lineEdit_fmax.setAlignment(Qt.AlignCenter)

        self.gridLayout_7.addWidget(self.lineEdit_fmax, 1, 2, 1, 1)

        self.label_25 = QLabel(self.frame_3)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setMinimumSize(QSize(0, 28))
        self.label_25.setMaximumSize(QSize(32, 28))
        self.label_25.setFont(font2)
        self.label_25.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_25, 1, 4, 1, 1)

        self.lineEdit_fstep = QLineEdit(self.frame_3)
        self.lineEdit_fstep.setObjectName(u"lineEdit_fstep")
        self.lineEdit_fstep.setMinimumSize(QSize(140, 28))
        self.lineEdit_fstep.setMaximumSize(QSize(180, 28))
        self.lineEdit_fstep.setFont(font3)
        self.lineEdit_fstep.setStyleSheet(u"")
        self.lineEdit_fstep.setAlignment(Qt.AlignCenter)

        self.gridLayout_7.addWidget(self.lineEdit_fstep, 2, 2, 1, 1)

        self.lineEdit_fmin = QLineEdit(self.frame_3)
        self.lineEdit_fmin.setObjectName(u"lineEdit_fmin")
        self.lineEdit_fmin.setMinimumSize(QSize(140, 28))
        self.lineEdit_fmin.setMaximumSize(QSize(180, 28))
        self.lineEdit_fmin.setFont(font3)
        self.lineEdit_fmin.setStyleSheet(u"")
        self.lineEdit_fmin.setAlignment(Qt.AlignCenter)

        self.gridLayout_7.addWidget(self.lineEdit_fmin, 0, 2, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_3, 0, 7, 1, 1)

        self.pushButton_add = QPushButton(self.frame_3)
        self.pushButton_add.setObjectName(u"pushButton_add")
        self.pushButton_add.setMinimumSize(QSize(40, 28))
        self.pushButton_add.setMaximumSize(QSize(40, 28))
        self.pushButton_add.setFont(font3)
        self.pushButton_add.setStyleSheet(u"")
        icon1 = QIcon()
        icon1.addFile(u":/icons/add.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_add.setIcon(icon1)
        self.pushButton_add.setIconSize(QSize(20, 20))
        self.pushButton_add.setAutoDefault(False)

        self.gridLayout_7.addWidget(self.pushButton_add, 2, 5, 1, 1)


        self.gridLayout_6.addWidget(self.frame_3, 0, 0, 1, 1)

        self.frame_2 = QFrame(self.tab)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_2)
        self.gridLayout_5.setSpacing(4)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(4, 4, 0, 4)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.pushButton_select_unselect_all = QPushButton(self.frame_2)
        self.pushButton_select_unselect_all.setObjectName(u"pushButton_select_unselect_all")
        self.pushButton_select_unselect_all.setMinimumSize(QSize(90, 30))
        self.pushButton_select_unselect_all.setMaximumSize(QSize(100, 30))
        self.pushButton_select_unselect_all.setFont(font3)
        self.pushButton_select_unselect_all.setStyleSheet(u"")
        self.pushButton_select_unselect_all.setAutoDefault(False)

        self.gridLayout_5.addWidget(self.pushButton_select_unselect_all, 0, 1, 1, 1)


        self.gridLayout_6.addWidget(self.frame_2, 1, 0, 1, 1)

        self.tabWidget.addTab(self.tab, "")

        self.gridLayout_4.addWidget(self.tabWidget, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.frame, 1, 0, 1, 1)

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
        self.pushButton_exit.setFont(font3)
        self.pushButton_exit.setStyleSheet(u"")
        self.pushButton_exit.setAutoDefault(False)

        self.gridLayout_3.addWidget(self.pushButton_exit, 0, 0, 1, 1)

        self.pushButton_confirm = QPushButton(self.frame_buttons)
        self.pushButton_confirm.setObjectName(u"pushButton_confirm")
        self.pushButton_confirm.setMinimumSize(QSize(100, 30))
        self.pushButton_confirm.setMaximumSize(QSize(100, 30))
        self.pushButton_confirm.setFont(font3)
        self.pushButton_confirm.setStyleSheet(u"")
        self.pushButton_confirm.setAutoDefault(False)

        self.gridLayout_3.addWidget(self.pushButton_confirm, 0, 1, 1, 1)


        self.gridLayout_2.addWidget(self.frame_buttons, 2, 0, 1, 1)

        self.frame_title_2 = QFrame(Dialog)
        self.frame_title_2.setObjectName(u"frame_title_2")
        self.frame_title_2.setMinimumSize(QSize(0, 60))
        self.frame_title_2.setMaximumSize(QSize(16777215, 60))
        self.frame_title_2.setFrameShape(QFrame.Box)
        self.frame_title_2.setFrameShadow(QFrame.Raised)
        self.frame_title_2.setLineWidth(1)
        self.gridLayout_11 = QGridLayout(self.frame_title_2)
        self.gridLayout_11.setSpacing(2)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setContentsMargins(2, 2, 2, 2)
        self.label_title_3 = QLabel(self.frame_title_2)
        self.label_title_3.setObjectName(u"label_title_3")
        font4 = QFont()
        font4.setFamilies([u"MS Shell Dlg 2"])
        font4.setPointSize(11)
        font4.setBold(False)
        font4.setItalic(False)
        self.label_title_3.setFont(font4)
        self.label_title_3.setTextFormat(Qt.AutoText)
        self.label_title_3.setAlignment(Qt.AlignCenter)

        self.gridLayout_11.addWidget(self.label_title_3, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.frame_title_2, 0, 0, 1, 1)


        self.retranslateUi(Dialog)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        ___qtablewidgetitem = self.tableWidget_frequencies_2.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Dialog", u"Index", None));
        ___qtablewidgetitem1 = self.tableWidget_frequencies_2.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Dialog", u"Frequency [Hz]", None));
        ___qtablewidgetitem2 = self.tableWidget_frequencies_2.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Dialog", u"Remove", None));
        self.label_28.setText(QCoreApplication.translate("Dialog", u"Solution step:", None))
        self.label_29.setText(QCoreApplication.translate("Dialog", u"[Hz]", None))
        self.pushButton_add_2.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Dialog", u"Manual", None))
        ___qtablewidgetitem3 = self.tableWidget_frequencies.horizontalHeaderItem(0)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Dialog", u"Index", None));
        ___qtablewidgetitem4 = self.tableWidget_frequencies.horizontalHeaderItem(1)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Dialog", u"Frequency [Hz]", None));
        ___qtablewidgetitem5 = self.tableWidget_frequencies.horizontalHeaderItem(2)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Dialog", u"Select", None));
        self.label_24.setText(QCoreApplication.translate("Dialog", u"[Hz]", None))
        self.label_21.setText(QCoreApplication.translate("Dialog", u"Freq. step:", None))
        self.label_26.setText(QCoreApplication.translate("Dialog", u"[Hz]", None))
        self.label_22.setText(QCoreApplication.translate("Dialog", u"Freq. min:", None))
        self.label_23.setText(QCoreApplication.translate("Dialog", u"Freq. max:", None))
        self.label_25.setText(QCoreApplication.translate("Dialog", u"[Hz]", None))
        self.pushButton_add.setText("")
        self.pushButton_select_unselect_all.setText(QCoreApplication.translate("Dialog", u"Deselect all", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Dialog", u"Tabular", None))
        self.pushButton_exit.setText(QCoreApplication.translate("Dialog", u"Exit", None))
        self.pushButton_confirm.setText(QCoreApplication.translate("Dialog", u"Confirm", None))
        self.label_title_3.setText(QCoreApplication.translate("Dialog", u"List of solution steps", None))
    # retranslateUi



class UserDefinedFrequenciesInput_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame: QFrame
                    - (Layout): QGridLayout
                            - tabWidget: QTabWidget
                                - tab_2: QWidget
                                    - (Layout): QGridLayout
                                            - tableWidget_frequencies_2: QTableWidget
                                            - frame_4: QFrame
                                                - (Layout): QGridLayout
                                                        - label_28: QLabel
                                                        - label_29: QLabel
                                                        - pushButton_add_2: QPushButton
                                                        - lineEdit_fstep_2: QLineEdit
                                - tab: QWidget
                                    - (Layout): QGridLayout
                                            - tableWidget_frequencies: QTableWidget
                                            - frame_3: QFrame
                                                - (Layout): QGridLayout
                                                        - label_24: QLabel
                                                        - label_21: QLabel
                                                        - label_26: QLabel
                                                        - label_22: QLabel
                                                        - label_23: QLabel
                                                        - lineEdit_fmax: QLineEdit
                                                        - label_25: QLabel
                                                        - lineEdit_fstep: QLineEdit
                                                        - lineEdit_fmin: QLineEdit
                                                        - pushButton_add: QPushButton
                                            - frame_2: QFrame
                                                - (Layout): QGridLayout
                                                        - pushButton_select_unselect_all: QPushButton
                - frame_buttons: QFrame
                    - (Layout): QGridLayout
                            - pushButton_exit: QPushButton
                            - pushButton_confirm: QPushButton
                - frame_title_2: QFrame
                    - (Layout): QGridLayout
                            - label_title_3: QLabel
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
