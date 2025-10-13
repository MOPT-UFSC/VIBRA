# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'exception_message.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QTextBrowser, QTextEdit, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        Dialog.resize(562, 402)
        Dialog.setMaximumSize(QSize(600, 600))
        Dialog.setModal(True)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.title_label = QLabel(Dialog)
        self.title_label.setObjectName(u"title_label")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.title_label.sizePolicy().hasHeightForWidth())
        self.title_label.setSizePolicy(sizePolicy)
        self.title_label.setMaximumSize(QSize(16777215, 50))
        self.title_label.setBaseSize(QSize(0, 50))
        font = QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.title_label.setFont(font)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.title_label)

        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        font1 = QFont()
        font1.setPointSize(9)
        self.frame.setFont(font1)
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.error_message = QLabel(self.frame)
        self.error_message.setObjectName(u"error_message")
        sizePolicy.setHeightForWidth(self.error_message.sizePolicy().hasHeightForWidth())
        self.error_message.setSizePolicy(sizePolicy)
        font2 = QFont()
        font2.setPointSize(10)
        self.error_message.setFont(font2)
        self.error_message.setTextFormat(Qt.TextFormat.PlainText)
        self.error_message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_message.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.error_message)


        self.verticalLayout.addWidget(self.frame)

        self.stack_trace_text_browser = QTextBrowser(Dialog)
        self.stack_trace_text_browser.setObjectName(u"stack_trace_text_browser")
        self.stack_trace_text_browser.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.stack_trace_text_browser.sizePolicy().hasHeightForWidth())
        self.stack_trace_text_browser.setSizePolicy(sizePolicy1)
        font3 = QFont()
        font3.setFamilies([u"Courier"])
        font3.setPointSize(10)
        font3.setKerning(True)
        self.stack_trace_text_browser.setFont(font3)
        self.stack_trace_text_browser.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.stack_trace_text_browser.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)

        self.verticalLayout.addWidget(self.stack_trace_text_browser)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.ok_button = QPushButton(Dialog)
        self.ok_button.setObjectName(u"ok_button")
        self.ok_button.setMinimumSize(QSize(80, 0))
        self.ok_button.setBaseSize(QSize(0, 0))

        self.horizontalLayout.addWidget(self.ok_button)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.title_label.setText(QCoreApplication.translate("Dialog", u"Title", None))
        self.error_message.setText(QCoreApplication.translate("Dialog", u"Short message explaining the error", None))
        self.stack_trace_text_browser.setHtml(QCoreApplication.translate("Dialog", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Courier'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Cascadia Code'; font-size:9pt;\">Stack trace containing only the last few calls</span></p></body></html>", None))
        self.ok_button.setText(QCoreApplication.translate("Dialog", u"OK", None))
    # retranslateUi



class ExceptionMessage_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QVBoxLayout
                - title_label: QLabel
                - frame: QFrame
                    - (Layout): QVBoxLayout
                            - error_message: QLabel
                - stack_trace_text_browser: QTextBrowser
                - (Layout): QHBoxLayout
                        - ok_button: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
