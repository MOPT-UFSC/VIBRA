# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'change_frequency_data_range_input.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QDoubleSpinBox, QFrame,
    QGridLayout, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(388, 300)
        Dialog.setMinimumSize(QSize(388, 300))
        Dialog.setMaximumSize(QSize(388, 300))
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(380, 48))
        self.frame.setMaximumSize(QSize(16777215, 48))
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setLineWidth(1)
        self.gridLayout_6 = QGridLayout(self.frame)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setFamilies([u"MS Shell Dlg 2"])
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        self.label.setFont(font)
        self.label.setTextFormat(Qt.AutoText)
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout_6.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

        self.frame_2 = QFrame(Dialog)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Box)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_2)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(4, 4, 4, 4)
        self.frame_3 = QFrame(self.frame_2)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_3)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.label_18 = QLabel(self.frame_3)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setMinimumSize(QSize(80, 28))
        self.label_18.setMaximumSize(QSize(80, 28))
        font1 = QFont()
        font1.setFamilies([u"MS Shell Dlg 2"])
        font1.setPointSize(10)
        font1.setBold(False)
        font1.setItalic(False)
        self.label_18.setFont(font1)
        self.label_18.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_18, 0, 1, 1, 1)

        self.doubleSpinBox_freq_min = QDoubleSpinBox(self.frame_3)
        self.doubleSpinBox_freq_min.setObjectName(u"doubleSpinBox_freq_min")
        self.doubleSpinBox_freq_min.setMinimumSize(QSize(100, 28))
        self.doubleSpinBox_freq_min.setMaximumSize(QSize(100, 28))
        font2 = QFont()
        font2.setPointSize(10)
        self.doubleSpinBox_freq_min.setFont(font2)
        self.doubleSpinBox_freq_min.setAlignment(Qt.AlignCenter)
        self.doubleSpinBox_freq_min.setMaximum(1000.000000000000000)

        self.gridLayout_4.addWidget(self.doubleSpinBox_freq_min, 0, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.label_19 = QLabel(self.frame_3)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setMinimumSize(QSize(60, 28))
        self.label_19.setMaximumSize(QSize(60, 28))
        self.label_19.setFont(font1)
        self.label_19.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_19, 0, 3, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_2, 0, 4, 1, 1)


        self.gridLayout_2.addWidget(self.frame_3, 0, 0, 1, 1)

        self.frame_6 = QFrame(self.frame_2)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.NoFrame)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_6)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.pushButton_confirm = QPushButton(self.frame_6)
        self.pushButton_confirm.setObjectName(u"pushButton_confirm")
        self.pushButton_confirm.setMinimumSize(QSize(100, 28))
        self.pushButton_confirm.setMaximumSize(QSize(100, 28))
        self.pushButton_confirm.setFont(font1)
        self.pushButton_confirm.setStyleSheet(u"")

        self.gridLayout_3.addWidget(self.pushButton_confirm, 0, 1, 1, 1)

        self.pushButton_exit = QPushButton(self.frame_6)
        self.pushButton_exit.setObjectName(u"pushButton_exit")
        self.pushButton_exit.setMinimumSize(QSize(100, 28))
        self.pushButton_exit.setMaximumSize(QSize(100, 28))
        self.pushButton_exit.setFont(font1)
        self.pushButton_exit.setStyleSheet(u"")

        self.gridLayout_3.addWidget(self.pushButton_exit, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.frame_6, 3, 0, 1, 1)

        self.frame_4 = QFrame(self.frame_2)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_4)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.label_20 = QLabel(self.frame_4)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setMinimumSize(QSize(80, 28))
        self.label_20.setMaximumSize(QSize(80, 28))
        self.label_20.setFont(font1)
        self.label_20.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_20, 0, 1, 1, 1)

        self.doubleSpinBox_freq_max = QDoubleSpinBox(self.frame_4)
        self.doubleSpinBox_freq_max.setObjectName(u"doubleSpinBox_freq_max")
        self.doubleSpinBox_freq_max.setMinimumSize(QSize(100, 28))
        self.doubleSpinBox_freq_max.setMaximumSize(QSize(100, 28))
        self.doubleSpinBox_freq_max.setFont(font2)
        self.doubleSpinBox_freq_max.setAlignment(Qt.AlignCenter)
        self.doubleSpinBox_freq_max.setMaximum(10000.000000000000000)
        self.doubleSpinBox_freq_max.setValue(500.000000000000000)

        self.gridLayout_5.addWidget(self.doubleSpinBox_freq_max, 0, 2, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_3, 0, 0, 1, 1)

        self.label_21 = QLabel(self.frame_4)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setMinimumSize(QSize(60, 28))
        self.label_21.setMaximumSize(QSize(60, 28))
        self.label_21.setFont(font1)
        self.label_21.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_21, 0, 3, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_4, 0, 4, 1, 1)


        self.gridLayout_2.addWidget(self.frame_4, 1, 0, 1, 1)

        self.frame_5 = QFrame(self.frame_2)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.gridLayout_8 = QGridLayout(self.frame_5)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.label_24 = QLabel(self.frame_5)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setMinimumSize(QSize(80, 28))
        self.label_24.setMaximumSize(QSize(80, 28))
        self.label_24.setFont(font1)
        self.label_24.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_24, 0, 1, 1, 1)

        self.doubleSpinBox_freq_step = QDoubleSpinBox(self.frame_5)
        self.doubleSpinBox_freq_step.setObjectName(u"doubleSpinBox_freq_step")
        self.doubleSpinBox_freq_step.setMinimumSize(QSize(100, 28))
        self.doubleSpinBox_freq_step.setMaximumSize(QSize(100, 28))
        self.doubleSpinBox_freq_step.setFont(font2)
        self.doubleSpinBox_freq_step.setAlignment(Qt.AlignCenter)
        self.doubleSpinBox_freq_step.setMaximum(10000.000000000000000)
        self.doubleSpinBox_freq_step.setValue(2.000000000000000)

        self.gridLayout_8.addWidget(self.doubleSpinBox_freq_step, 0, 2, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_7, 0, 0, 1, 1)

        self.label_25 = QLabel(self.frame_5)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setMinimumSize(QSize(60, 28))
        self.label_25.setMaximumSize(QSize(60, 28))
        self.label_25.setFont(font1)
        self.label_25.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_25, 0, 3, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_8, 0, 4, 1, 1)


        self.gridLayout_2.addWidget(self.frame_5, 2, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_2, 1, 0, 1, 1)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Change frequency data range", None))
        self.label_18.setText(QCoreApplication.translate("Dialog", u"Freq. min.:", None))
        self.label_19.setText(QCoreApplication.translate("Dialog", u"[Hz]", None))
        self.pushButton_confirm.setText(QCoreApplication.translate("Dialog", u"Confirm", None))
        self.pushButton_exit.setText(QCoreApplication.translate("Dialog", u"Exit", None))
        self.label_20.setText(QCoreApplication.translate("Dialog", u"Freq. max.:", None))
        self.label_21.setText(QCoreApplication.translate("Dialog", u"[Hz]", None))
        self.label_24.setText(QCoreApplication.translate("Dialog", u"Freq. step.:", None))
        self.label_25.setText(QCoreApplication.translate("Dialog", u"[Hz]", None))
    # retranslateUi



class ChangeFrequencyDataRangeInput_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
                - frame_2: QFrame
                    - (Layout): QGridLayout
                            - frame_3: QFrame
                                - (Layout): QGridLayout
                                        - label_18: QLabel
                                        - doubleSpinBox_freq_min: QDoubleSpinBox
                                        - label_19: QLabel
                            - frame_6: QFrame
                                - (Layout): QGridLayout
                                        - pushButton_confirm: QPushButton
                                        - pushButton_exit: QPushButton
                            - frame_4: QFrame
                                - (Layout): QGridLayout
                                        - label_20: QLabel
                                        - doubleSpinBox_freq_max: QDoubleSpinBox
                                        - label_21: QLabel
                            - frame_5: QFrame
                                - (Layout): QGridLayout
                                        - label_24: QLabel
                                        - doubleSpinBox_freq_step: QDoubleSpinBox
                                        - label_25: QLabel
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
