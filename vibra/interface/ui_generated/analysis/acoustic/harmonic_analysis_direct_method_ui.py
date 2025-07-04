# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'harmonic_analysis_direct_method.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
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
    QTabWidget, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setWindowModality(Qt.NonModal)
        Dialog.resize(440, 339)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(440, 339))
        Dialog.setMaximumSize(QSize(600, 450))
        Dialog.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.gridLayout_3 = QGridLayout(Dialog)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(4, 4, 4, 4)
        self.frame_2 = QFrame(Dialog)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(400, 239))
        self.frame_2.setMaximumSize(QSize(430, 260))
        self.frame_2.setFrameShape(QFrame.Box)
        self.frame_2.setFrameShadow(QFrame.Plain)
        self.gridLayout_6 = QGridLayout(self.frame_2)
        self.gridLayout_6.setSpacing(4)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(4, 8, 4, 4)
        self.tabWidget = QTabWidget(self.frame_2)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setMaximumSize(QSize(360, 16777215))
        font = QFont()
        font.setFamilies([u"MS Shell Dlg 2"])
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        self.tabWidget.setFont(font)
        self.tabWidget.setStyleSheet(u"")
        self.tab_setup = QWidget()
        self.tab_setup.setObjectName(u"tab_setup")
        self.gridLayout = QGridLayout(self.tab_setup)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(6)
        self.gridLayout.setVerticalSpacing(2)
        self.gridLayout.setContentsMargins(2, 2, 2, 2)
        self.label_24 = QLabel(self.tab_setup)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setMinimumSize(QSize(60, 28))
        self.label_24.setMaximumSize(QSize(60, 28))
        self.label_24.setFont(font)
        self.label_24.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_24, 0, 3, 1, 1)

        self.lineEdit_fmin = QLineEdit(self.tab_setup)
        self.lineEdit_fmin.setObjectName(u"lineEdit_fmin")
        self.lineEdit_fmin.setMinimumSize(QSize(100, 28))
        self.lineEdit_fmin.setMaximumSize(QSize(100, 28))
        self.lineEdit_fmin.setFont(font)
        self.lineEdit_fmin.setStyleSheet(u"")
        self.lineEdit_fmin.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_fmin, 0, 2, 1, 1)

        self.lineEdit_fstep = QLineEdit(self.tab_setup)
        self.lineEdit_fstep.setObjectName(u"lineEdit_fstep")
        self.lineEdit_fstep.setMinimumSize(QSize(100, 28))
        self.lineEdit_fstep.setMaximumSize(QSize(100, 28))
        self.lineEdit_fstep.setFont(font)
        self.lineEdit_fstep.setStyleSheet(u"")
        self.lineEdit_fstep.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_fstep, 2, 2, 1, 1)

        self.lineEdit_fmax = QLineEdit(self.tab_setup)
        self.lineEdit_fmax.setObjectName(u"lineEdit_fmax")
        self.lineEdit_fmax.setMinimumSize(QSize(100, 28))
        self.lineEdit_fmax.setMaximumSize(QSize(100, 28))
        self.lineEdit_fmax.setFont(font)
        self.lineEdit_fmax.setStyleSheet(u"")
        self.lineEdit_fmax.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_fmax, 1, 2, 1, 1)

        self.label_25 = QLabel(self.tab_setup)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setMinimumSize(QSize(60, 28))
        self.label_25.setMaximumSize(QSize(60, 28))
        self.label_25.setFont(font)
        self.label_25.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_25, 1, 3, 1, 1)

        self.label_22 = QLabel(self.tab_setup)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setMinimumSize(QSize(112, 28))
        self.label_22.setMaximumSize(QSize(112, 28))
        self.label_22.setFont(font)
        self.label_22.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_22, 0, 1, 1, 1)

        self.label_23 = QLabel(self.tab_setup)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setMinimumSize(QSize(112, 28))
        self.label_23.setMaximumSize(QSize(112, 28))
        self.label_23.setFont(font)
        self.label_23.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_23, 1, 1, 1, 1)

        self.label_21 = QLabel(self.tab_setup)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setMinimumSize(QSize(112, 28))
        self.label_21.setMaximumSize(QSize(112, 28))
        self.label_21.setFont(font)
        self.label_21.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_21, 2, 1, 1, 1)

        self.label_26 = QLabel(self.tab_setup)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setMinimumSize(QSize(60, 28))
        self.label_26.setMaximumSize(QSize(60, 28))
        self.label_26.setFont(font)
        self.label_26.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_26, 2, 3, 1, 1)

        self.frame_4 = QFrame(self.tab_setup)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Raised)

        self.gridLayout.addWidget(self.frame_4, 0, 0, 1, 1)

        self.frame_5 = QFrame(self.tab_setup)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Raised)

        self.gridLayout.addWidget(self.frame_5, 0, 4, 1, 1)

        self.tabWidget.addTab(self.tab_setup, "")

        self.gridLayout_6.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.frame_6 = QFrame(self.frame_2)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setMinimumSize(QSize(0, 48))
        self.frame_6.setMaximumSize(QSize(16777215, 48))
        self.frame_6.setFrameShape(QFrame.NoFrame)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_6)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setHorizontalSpacing(8)
        self.gridLayout_5.setVerticalSpacing(2)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.pushButton_enter_setup = QPushButton(self.frame_6)
        self.pushButton_enter_setup.setObjectName(u"pushButton_enter_setup")
        self.pushButton_enter_setup.setMinimumSize(QSize(120, 32))
        self.pushButton_enter_setup.setMaximumSize(QSize(120, 32))
        self.pushButton_enter_setup.setFont(font)
        self.pushButton_enter_setup.setStyleSheet(u"")

        self.gridLayout_5.addWidget(self.pushButton_enter_setup, 0, 0, 1, 1)

        self.pushButton_run_analysis = QPushButton(self.frame_6)
        self.pushButton_run_analysis.setObjectName(u"pushButton_run_analysis")
        self.pushButton_run_analysis.setMinimumSize(QSize(120, 32))
        self.pushButton_run_analysis.setMaximumSize(QSize(120, 32))
        self.pushButton_run_analysis.setFont(font)
        self.pushButton_run_analysis.setStyleSheet(u"")

        self.gridLayout_5.addWidget(self.pushButton_run_analysis, 0, 1, 1, 1)


        self.gridLayout_6.addWidget(self.frame_6, 1, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_2, 1, 0, 1, 1)

        self.frame_3 = QFrame(Dialog)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMaximumSize(QSize(16777215, 80))
        self.frame_3.setFrameShape(QFrame.Box)
        self.frame_3.setFrameShadow(QFrame.Plain)
        self.frame_3.setLineWidth(1)
        self.gridLayout_2 = QGridLayout(self.frame_3)
        self.gridLayout_2.setSpacing(2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_title = QLabel(self.frame_3)
        self.label_title.setObjectName(u"label_title")
        font1 = QFont()
        font1.setFamilies([u"MS Shell Dlg 2"])
        font1.setPointSize(11)
        font1.setBold(False)
        font1.setItalic(False)
        self.label_title.setFont(font1)
        self.label_title.setTextFormat(Qt.AutoText)
        self.label_title.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label_title, 0, 0, 1, 1)

        self.label_subtitle = QLabel(self.frame_3)
        self.label_subtitle.setObjectName(u"label_subtitle")
        self.label_subtitle.setFont(font1)
        self.label_subtitle.setTextFormat(Qt.AutoText)
        self.label_subtitle.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label_subtitle, 1, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_3, 0, 0, 1, 1)

        QWidget.setTabOrder(self.tabWidget, self.lineEdit_fmin)
        QWidget.setTabOrder(self.lineEdit_fmin, self.lineEdit_fmax)
        QWidget.setTabOrder(self.lineEdit_fmax, self.lineEdit_fstep)
        QWidget.setTabOrder(self.lineEdit_fstep, self.pushButton_run_analysis)
        QWidget.setTabOrder(self.pushButton_run_analysis, self.pushButton_enter_setup)

        self.retranslateUi(Dialog)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Harmonic analysis setup", None))
#if QT_CONFIG(whatsthis)
        Dialog.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.label_24.setText(QCoreApplication.translate("Dialog", u"[Hz]", None))
        self.lineEdit_fmin.setText(QCoreApplication.translate("Dialog", u"5", None))
        self.lineEdit_fstep.setText(QCoreApplication.translate("Dialog", u"5", None))
        self.lineEdit_fmax.setText(QCoreApplication.translate("Dialog", u"1400", None))
        self.label_25.setText(QCoreApplication.translate("Dialog", u"[Hz]", None))
        self.label_22.setText(QCoreApplication.translate("Dialog", u"Freq. min:", None))
        self.label_23.setText(QCoreApplication.translate("Dialog", u"Freq. max:", None))
        self.label_21.setText(QCoreApplication.translate("Dialog", u"Freq. step:", None))
        self.label_26.setText(QCoreApplication.translate("Dialog", u"[Hz]", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_setup), QCoreApplication.translate("Dialog", u"Frequency Setup", None))
        self.pushButton_enter_setup.setText(QCoreApplication.translate("Dialog", u"Enter setup", None))
        self.pushButton_run_analysis.setText(QCoreApplication.translate("Dialog", u"Run analysis", None))
        self.label_title.setText(QCoreApplication.translate("Dialog", u"Acoustic Harmonic Analysis Setup", None))
        self.label_subtitle.setText(QCoreApplication.translate("Dialog", u"Direct Method", None))
    # retranslateUi



class HarmonicAnalysisDirectMethod_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame_2: QFrame
                    - (Layout): QGridLayout
                            - tabWidget: QTabWidget
                                - tab_setup: QWidget
                                    - (Layout): QGridLayout
                                            - label_24: QLabel
                                            - lineEdit_fmin: QLineEdit
                                            - lineEdit_fstep: QLineEdit
                                            - lineEdit_fmax: QLineEdit
                                            - label_25: QLabel
                                            - label_22: QLabel
                                            - label_23: QLabel
                                            - label_21: QLabel
                                            - label_26: QLabel
                                            - frame_4: QFrame
                                            - frame_5: QFrame
                            - frame_6: QFrame
                                - (Layout): QGridLayout
                                        - pushButton_enter_setup: QPushButton
                                        - pushButton_run_analysis: QPushButton
                - frame_3: QFrame
                    - (Layout): QGridLayout
                            - label_title: QLabel
                            - label_subtitle: QLabel
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
