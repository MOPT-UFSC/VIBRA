# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'harmonic_analysis_input.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFrame,
    QLabel, QPushButton, QSizePolicy, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setWindowModality(Qt.NonModal)
        Dialog.resize(400, 217)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(400, 217))
        Dialog.setMaximumSize(QSize(400, 217))
        Dialog.setContextMenuPolicy(Qt.DefaultContextMenu)
        icon = QIcon()
        icon.addFile(u"../../../../Downloads/load - Copia.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        Dialog.setWindowIcon(icon)
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(0, 0, 400, 47))
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(12)
        font.setBold(True)
        self.frame.setFont(font)
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setFrameShadow(QFrame.Plain)
        self.frame.setLineWidth(1)
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(34, 8, 333, 32))
        font1 = QFont()
        font1.setFamilies([u"Segoe UI"])
        font1.setPointSize(14)
        font1.setBold(False)
        font1.setItalic(False)
        self.label.setFont(font1)
        self.label.setStyleSheet(u"font: 14pt \"Segoe UI\";")
        self.label.setTextFormat(Qt.AutoText)
        self.label.setAlignment(Qt.AlignCenter)
        self.frame_2 = QFrame(Dialog)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setGeometry(QRect(0, 46, 400, 171))
        self.frame_2.setFont(font)
        self.frame_2.setFrameShape(QFrame.Box)
        self.frame_2.setFrameShadow(QFrame.Plain)
        self.comboBox = QComboBox(self.frame_2)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(128, 74, 190, 30))
        self.comboBox.setMinimumSize(QSize(190, 30))
        self.comboBox.setMaximumSize(QSize(190, 30))
        font2 = QFont()
        font2.setFamilies([u"Segoe UI"])
        font2.setPointSize(13)
        font2.setBold(False)
        font2.setItalic(False)
        self.comboBox.setFont(font2)
        self.comboBox.setStyleSheet(u"font: 13pt \"Segoe UI\";")
        self.comboBox.setInputMethodHints(Qt.ImhNoAutoUppercase)
        self.comboBox.setInsertPolicy(QComboBox.NoInsert)
        self.pushButton_2 = QPushButton(self.frame_2)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(80, 126, 240, 32))
        self.pushButton_2.setMinimumSize(QSize(240, 32))
        self.pushButton_2.setMaximumSize(QSize(240, 32))
        self.pushButton_2.setFont(font2)
        self.pushButton_2.setStyleSheet(u"font: 13pt \"Segoe UI\";")
        self.label_2 = QLabel(self.frame_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(44, 76, 83, 26))
        self.label_2.setFont(font2)
        self.label_2.setStyleSheet(u"font: 13pt \"Segoe UI\";")
        self.label_2.setAlignment(Qt.AlignCenter)
        self.label_3 = QLabel(self.frame_2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(38, 20, 325, 32))
        self.label_3.setFont(font2)
        self.label_3.setStyleSheet(u"font: 13pt \"Segoe UI\";")
        self.label_3.setFrameShape(QFrame.Box)
        self.label_3.setFrameShadow(QFrame.Sunken)
        self.label_3.setTextFormat(Qt.AutoText)
        self.label_3.setAlignment(Qt.AlignCenter)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Harmonic analysis: method selection", None))
#if QT_CONFIG(whatsthis)
        Dialog.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.label.setText(QCoreApplication.translate("Dialog", u"SELECT THE ANALYSIS METHOD", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("Dialog", u"Direct", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("Dialog", u"Mode Superposition", None))

        self.pushButton_2.setText(QCoreApplication.translate("Dialog", u"Go to Analysis setup", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Method:", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Harmonic Analysis - Structural", None))
    # retranslateUi



class HarmonicAnalysisInput_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - frame: QFrame
            - label: QLabel
        - frame_2: QFrame
            - comboBox: QComboBox
            - pushButton_2: QPushButton
            - label_2: QLabel
            - label_3: QLabel
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
