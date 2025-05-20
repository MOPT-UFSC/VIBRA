# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'print_messages.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
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
        Dialog.resize(400, 260)
        Dialog.setMinimumSize(QSize(400, 260))
        Dialog.setMaximumSize(QSize(600, 600))
        self.gridLayout_3 = QGridLayout(Dialog)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setHorizontalSpacing(2)
        self.gridLayout_3.setVerticalSpacing(4)
        self.gridLayout_3.setContentsMargins(4, 4, 4, 4)
        self.frame_title = QFrame(Dialog)
        self.frame_title.setObjectName(u"frame_title")
        self.frame_title.setMinimumSize(QSize(360, 0))
        self.frame_title.setMaximumSize(QSize(580, 52))
        self.frame_title.setFrameShape(QFrame.NoFrame)
        self.frame_title.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame_title)
        self.gridLayout.setSpacing(2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.label_title = QLabel(self.frame_title)
        self.label_title.setObjectName(u"label_title")
        self.label_title.setMinimumSize(QSize(360, 36))
        self.label_title.setMaximumSize(QSize(580, 36))
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(13)
        font.setBold(True)
        font.setItalic(False)
        self.label_title.setFont(font)
        self.label_title.setFrameShape(QFrame.Box)
        self.label_title.setFrameShadow(QFrame.Raised)
        self.label_title.setTextFormat(Qt.AutoText)
        self.label_title.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_title, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_title, 0, 0, 1, 1)

        self.frame_button = QFrame(Dialog)
        self.frame_button.setObjectName(u"frame_button")
        self.frame_button.setMinimumSize(QSize(0, 50))
        self.frame_button.setMaximumSize(QSize(16777215, 52))
        self.frame_button.setFrameShape(QFrame.NoFrame)
        self.frame_button.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_button)
        self.gridLayout_2.setSpacing(2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.pushButton_close = QPushButton(self.frame_button)
        self.pushButton_close.setObjectName(u"pushButton_close")
        self.pushButton_close.setMinimumSize(QSize(120, 36))
        self.pushButton_close.setMaximumSize(QSize(120, 36))
        self.pushButton_close.setSizeIncrement(QSize(0, 0))
        font1 = QFont()
        font1.setFamilies([u"Arial"])
        font1.setPointSize(14)
        font1.setBold(True)
        font1.setItalic(True)
        self.pushButton_close.setFont(font1)
        self.pushButton_close.setStyleSheet(u"QPushButton{border-radius: 16px; border-color: rgb(150, 150, 150); border-style: ridge; border-width: 2px; color: rgb(0, 0, 0); background-color: rgb(240, 240, 240); font: 75 italic bold 14pt \"Arial\"}\n"
"QPushButton:hover{border-radius: 16px; border-color: rgb(0, 170, 255); border-style: ridge; border-width: 2px; color: rgb(0, 0, 0); background-color: rgba(174, 213, 255, 100); font: 75 italic bold 14pt \"Arial\"}\n"
"QPushButton:pressed{border-radius: 16px; border-color: rgb(0, 170, 255); border-style: ridge; border-width: 3px; color: rgb(0, 0, 0); background-color: rgb(174, 213, 255); font: 75 italic bold 14pt \"Arial\"}")
        self.pushButton_close.setFlat(False)

        self.gridLayout_2.addWidget(self.pushButton_close, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_button, 2, 0, 1, 1)

        self.frame_message = QFrame(Dialog)
        self.frame_message.setObjectName(u"frame_message")
        self.frame_message.setMinimumSize(QSize(360, 160))
        self.frame_message.setMaximumSize(QSize(580, 16777215))
        self.frame_message.setFrameShape(QFrame.Box)
        self.frame_message.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_message)
        self.gridLayout_4.setSpacing(4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(4, 4, 4, 4)
        self.label_message = QLabel(self.frame_message)
        self.label_message.setObjectName(u"label_message")
        self.label_message.setMinimumSize(QSize(340, 120))
        self.label_message.setMaximumSize(QSize(560, 280))
        self.label_message.setFont(font)
        self.label_message.setFrameShape(QFrame.NoFrame)
        self.label_message.setFrameShadow(QFrame.Raised)
        self.label_message.setTextFormat(Qt.AutoText)
        self.label_message.setAlignment(Qt.AlignJustify|Qt.AlignVCenter)
        self.label_message.setWordWrap(True)
        self.label_message.setMargin(10)
        self.label_message.setIndent(-1)

        self.gridLayout_4.addWidget(self.label_message, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_message, 1, 0, 1, 1)


        self.retranslateUi(Dialog)

        self.pushButton_close.setDefault(False)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_title.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">TITLE</span></p></body></html>", None))
        self.pushButton_close.setText(QCoreApplication.translate("Dialog", u"Close", None))
        self.label_message.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\"><span style=\" font-size:14pt;\">message</span></p></body></html>", None))
    # retranslateUi



class PrintMessages_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame_title: QFrame
                    - (Layout): QGridLayout
                            - label_title: QLabel
                - frame_button: QFrame
                    - (Layout): QGridLayout
                            - pushButton_close: QPushButton
                - frame_message: QFrame
                    - (Layout): QGridLayout
                            - label_message: QLabel
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
