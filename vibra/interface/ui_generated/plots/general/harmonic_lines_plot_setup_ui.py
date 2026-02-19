# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'harmonic_lines_plot_setup.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpinBox, QVBoxLayout,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(386, 293)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.title = QFrame(Dialog)
        self.title.setObjectName(u"title")
        self.title.setMaximumSize(QSize(16777215, 40))
        self.title.setFrameShape(QFrame.Shape.StyledPanel)
        self.title.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.title)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_title = QLabel(self.title)
        self.label_title.setObjectName(u"label_title")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_title.sizePolicy().hasHeightForWidth())
        self.label_title.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(10)
        self.label_title.setFont(font)
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_title)


        self.verticalLayout.addWidget(self.title)

        self.content = QFrame(Dialog)
        self.content.setObjectName(u"content")
        self.content.setFrameShape(QFrame.Shape.StyledPanel)
        self.content.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.content)
        self.gridLayout.setObjectName(u"gridLayout")
        self.lineEdit_fundamental_frequency = QLineEdit(self.content)
        self.lineEdit_fundamental_frequency.setObjectName(u"lineEdit_fundamental_frequency")
        self.lineEdit_fundamental_frequency.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_fundamental_frequency, 0, 1, 1, 1)

        self.label = QLabel(self.content)
        self.label.setObjectName(u"label")
        self.label.setFont(font)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1, Qt.AlignmentFlag.AlignRight)

        self.label_2 = QLabel(self.content)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.label_3 = QLabel(self.content)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)

        self.gridLayout.addWidget(self.label_3, 0, 2, 1, 1)

        self.spinBox_number_of_lines = QSpinBox(self.content)
        self.spinBox_number_of_lines.setObjectName(u"spinBox_number_of_lines")
        self.spinBox_number_of_lines.setWrapping(False)
        self.spinBox_number_of_lines.setFrame(True)
        self.spinBox_number_of_lines.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spinBox_number_of_lines.setMinimum(1)

        self.gridLayout.addWidget(self.spinBox_number_of_lines, 1, 1, 1, 1)

        self.label_4 = QLabel(self.content)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font)
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)

        self.checkBox_show_legend = QCheckBox(self.content)
        self.checkBox_show_legend.setObjectName(u"checkBox_show_legend")
        self.checkBox_show_legend.setAutoRepeat(False)
        self.checkBox_show_legend.setTristate(False)

        self.gridLayout.addWidget(self.checkBox_show_legend, 2, 1, 1, 1)


        self.verticalLayout.addWidget(self.content)

        self.title_2 = QFrame(Dialog)
        self.title_2.setObjectName(u"title_2")
        self.title_2.setMaximumSize(QSize(16777215, 48))
        self.title_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.title_2.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.title_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButton_cancel = QPushButton(self.title_2)
        self.pushButton_cancel.setObjectName(u"pushButton_cancel")
        self.pushButton_cancel.setMinimumSize(QSize(100, 30))
        self.pushButton_cancel.setMaximumSize(QSize(120, 16777215))
        self.pushButton_cancel.setFont(font)
        self.pushButton_cancel.setFlat(False)

        self.horizontalLayout_2.addWidget(self.pushButton_cancel)

        self.pushButton_confirm = QPushButton(self.title_2)
        self.pushButton_confirm.setObjectName(u"pushButton_confirm")
        self.pushButton_confirm.setMinimumSize(QSize(100, 30))
        self.pushButton_confirm.setMaximumSize(QSize(120, 30))
        self.pushButton_confirm.setFont(font)
        self.pushButton_confirm.setFlat(False)

        self.horizontalLayout_2.addWidget(self.pushButton_confirm)


        self.verticalLayout.addWidget(self.title_2)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_title.setText(QCoreApplication.translate("Dialog", u"Harmonic Lines Setup", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Fundamental frequency:", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Number of harmonic lines:", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"[Hz]", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Show legend:", None))
        self.checkBox_show_legend.setText("")
        self.pushButton_cancel.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
        self.pushButton_confirm.setText(QCoreApplication.translate("Dialog", u"Confirm", None))
    # retranslateUi



class HarmonicLinesPlotSetup_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QVBoxLayout
                - title: QFrame
                    - (Layout): QVBoxLayout
                            - label_title: QLabel
                - content: QFrame
                    - (Layout): QGridLayout
                            - lineEdit_fundamental_frequency: QLineEdit
                            - label: QLabel
                            - label_2: QLabel
                            - label_3: QLabel
                            - spinBox_number_of_lines: QSpinBox
                            - label_4: QLabel
                            - checkBox_show_legend: QCheckBox
                - title_2: QFrame
                    - (Layout): QHBoxLayout
                            - pushButton_cancel: QPushButton
                            - pushButton_confirm: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
