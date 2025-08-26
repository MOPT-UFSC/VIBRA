# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'call_double_confirmation_input.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QGridLayout,
    QLabel, QPushButton, QSizePolicy, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(520, 320)
        Dialog.setMinimumSize(QSize(520, 320))
        Dialog.setMaximumSize(QSize(650, 600))
        Dialog.setModal(True)
        self.gridLayout_3 = QGridLayout(Dialog)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setHorizontalSpacing(2)
        self.gridLayout_3.setVerticalSpacing(4)
        self.gridLayout_3.setContentsMargins(8, 8, 8, 8)
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(500, 42))
        self.frame.setMaximumSize(QSize(630, 42))
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setSpacing(2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_title = QLabel(self.frame)
        self.label_title.setObjectName(u"label_title")
        self.label_title.setMinimumSize(QSize(500, 40))
        self.label_title.setMaximumSize(QSize(630, 40))
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        self.label_title.setFont(font)
        self.label_title.setStyleSheet(u"font: 75  bold 12pt \"Arial\";")
        self.label_title.setFrameShape(QFrame.Box)
        self.label_title.setFrameShadow(QFrame.Raised)
        self.label_title.setLineWidth(1)
        self.label_title.setTextFormat(Qt.AutoText)
        self.label_title.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label_title, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame, 0, 0, 1, 1)

        self.label_message = QLabel(Dialog)
        self.label_message.setObjectName(u"label_message")
        self.label_message.setMinimumSize(QSize(500, 200))
        self.label_message.setMaximumSize(QSize(630, 500))
        font1 = QFont()
        font1.setFamilies([u"MS Shell Dlg 2"])
        font1.setPointSize(12)
        font1.setBold(True)
        font1.setItalic(False)
        self.label_message.setFont(font1)
        self.label_message.setFrameShape(QFrame.Box)
        self.label_message.setFrameShadow(QFrame.Raised)
        self.label_message.setLineWidth(1)
        self.label_message.setTextFormat(Qt.AutoText)
        self.label_message.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.label_message, 1, 0, 1, 1)

        self.frame_3 = QFrame(Dialog)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(500, 52))
        self.frame_3.setMaximumSize(QSize(630, 52))
        self.frame_3.setSizeIncrement(QSize(0, 0))
        self.frame_3.setFrameShape(QFrame.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame_3)
        self.gridLayout.setSpacing(2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(2, 2, 2, 0)
        self.pushButton_leftButton = QPushButton(self.frame_3)
        self.pushButton_leftButton.setObjectName(u"pushButton_leftButton")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_leftButton.sizePolicy().hasHeightForWidth())
        self.pushButton_leftButton.setSizePolicy(sizePolicy)
        self.pushButton_leftButton.setMinimumSize(QSize(160, 36))
        self.pushButton_leftButton.setMaximumSize(QSize(120, 36))
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        font2.setPointSize(11)
        font2.setBold(True)
        font2.setItalic(False)
        self.pushButton_leftButton.setFont(font2)
        self.pushButton_leftButton.setStyleSheet(u"QPushButton{border-radius: 16px; border-color: rgb(150, 150, 150); border-style: ridge; border-width: 2px; color: rgb(0, 0, 0); background-color: rgb(240, 240, 240); font: 75 bold 11pt \"MS Shell Dlg 2\"}\n"
"QPushButton:hover{border-radius: 16px; border-color: rgb(0, 170, 255); border-style: ridge; border-width: 2px; color: rgb(0, 0, 0); background-color: rgba(174, 213, 255, 100); font: 75 bold 11pt \"MS Shell Dlg 2\"}\n"
"QPushButton:pressed{border-radius: 16px; border-color: rgb(0, 170, 255); border-style: ridge; border-width: 3px; color: rgb(0, 0, 0); background-color: rgb(174, 213, 255); font: 75 bold 11pt \"MS Shell Dlg 2\"}")
        self.pushButton_leftButton.setAutoDefault(False)
        self.pushButton_leftButton.setFlat(False)

        self.gridLayout.addWidget(self.pushButton_leftButton, 0, 0, 1, 1)

        self.pushButton_rightButton = QPushButton(self.frame_3)
        self.pushButton_rightButton.setObjectName(u"pushButton_rightButton")
        self.pushButton_rightButton.setMinimumSize(QSize(160, 36))
        self.pushButton_rightButton.setMaximumSize(QSize(120, 36))
        self.pushButton_rightButton.setFont(font2)
        self.pushButton_rightButton.setStyleSheet(u"QPushButton{border-radius: 16px; border-color: rgb(150, 150, 150); border-style: ridge; border-width: 2px; color: rgb(0, 0, 0); background-color: rgb(240, 240, 240); font: 75 bold 11pt \"MS Shell Dlg 2\"}\n"
"QPushButton:hover{border-radius: 16px; border-color: rgb(0, 170, 255); border-style: ridge; border-width: 2px; color: rgb(0, 0, 0); background-color: rgba(174, 213, 255, 100); font: 75 bold 11pt \"MS Shell Dlg 2\"}\n"
"QPushButton:pressed{border-radius: 16px; border-color: rgb(0, 170, 255); border-style: ridge; border-width: 3px; color: rgb(0, 0, 0); background-color: rgb(174, 213, 255); font: 75 bold 11pt \"MS Shell Dlg 2\"}")
        self.pushButton_rightButton.setAutoDefault(True)
        self.pushButton_rightButton.setFlat(False)

        self.gridLayout.addWidget(self.pushButton_rightButton, 0, 1, 1, 1)


        self.gridLayout_3.addWidget(self.frame_3, 2, 0, 1, 1)


        self.retranslateUi(Dialog)

        self.pushButton_leftButton.setDefault(False)
        self.pushButton_rightButton.setDefault(False)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Message", None))
        self.label_title.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\"><span style=\" font-size:14pt;\">TITLE</span></p></body></html>", None))
        self.label_message.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\">Confirmation message...</p></body></html>", None))
        self.pushButton_leftButton.setText(QCoreApplication.translate("Dialog", u"Left button", None))
        self.pushButton_rightButton.setText(QCoreApplication.translate("Dialog", u"Right button", None))
    # retranslateUi



class CallDoubleConfirmationInput_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame: QFrame
                    - (Layout): QGridLayout
                            - label_title: QLabel
                - label_message: QLabel
                - frame_3: QFrame
                    - (Layout): QGridLayout
                            - pushButton_leftButton: QPushButton
                            - pushButton_rightButton: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
