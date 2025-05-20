# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'analysis_type_input.ui'
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
        Dialog.setWindowModality(Qt.NonModal)
        Dialog.resize(360, 380)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(360, 380))
        Dialog.setMaximumSize(QSize(360, 380))
        Dialog.setContextMenuPolicy(Qt.DefaultContextMenu)
        icon = QIcon()
        icon.addFile(u"../../../../../Downloads/load - Copia.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        Dialog.setWindowIcon(icon)
        self.gridLayout_2 = QGridLayout(Dialog)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(4, 4, 4, 4)
        self.frame_title = QFrame(Dialog)
        self.frame_title.setObjectName(u"frame_title")
        self.frame_title.setMinimumSize(QSize(0, 48))
        self.frame_title.setMaximumSize(QSize(420, 48))
        self.frame_title.setFrameShape(QFrame.Box)
        self.frame_title.setFrameShadow(QFrame.Plain)
        self.frame_title.setLineWidth(1)
        self.gridLayout = QGridLayout(self.frame_title)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(self.frame_title)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setFamilies([u"MS Shell Dlg 2"])
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        self.label.setFont(font)
        self.label.setTextFormat(Qt.AutoText)
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.frame_title, 0, 0, 1, 1)

        self.frame_2 = QFrame(Dialog)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setEnabled(True)
        self.frame_2.setMinimumSize(QSize(0, 0))
        self.frame_2.setMaximumSize(QSize(420, 400))
        self.frame_2.setFrameShape(QFrame.Box)
        self.frame_2.setFrameShadow(QFrame.Plain)
        self.gridLayout_3 = QGridLayout(self.frame_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.pushButton_harmonic_structural = QPushButton(self.frame_2)
        self.pushButton_harmonic_structural.setObjectName(u"pushButton_harmonic_structural")
        self.pushButton_harmonic_structural.setEnabled(True)
        self.pushButton_harmonic_structural.setMinimumSize(QSize(240, 36))
        self.pushButton_harmonic_structural.setMaximumSize(QSize(240, 36))
        font1 = QFont()
        font1.setFamilies([u"MS Shell Dlg 2"])
        font1.setPointSize(10)
        font1.setBold(False)
        font1.setItalic(False)
        self.pushButton_harmonic_structural.setFont(font1)
        self.pushButton_harmonic_structural.setStyleSheet(u"")
        icon1 = QIcon()
        icon1.addFile(u"../../../../../Downloads/load.png", QSize(), QIcon.Mode.Active, QIcon.State.On)
        self.pushButton_harmonic_structural.setIcon(icon1)
        self.pushButton_harmonic_structural.setAutoDefault(True)
        self.pushButton_harmonic_structural.setFlat(False)

        self.gridLayout_3.addWidget(self.pushButton_harmonic_structural, 0, 0, 1, 1)

        self.pushButton_harmonic_acoustic = QPushButton(self.frame_2)
        self.pushButton_harmonic_acoustic.setObjectName(u"pushButton_harmonic_acoustic")
        self.pushButton_harmonic_acoustic.setMinimumSize(QSize(240, 36))
        self.pushButton_harmonic_acoustic.setMaximumSize(QSize(240, 36))
        self.pushButton_harmonic_acoustic.setFont(font1)
        self.pushButton_harmonic_acoustic.setStyleSheet(u"")

        self.gridLayout_3.addWidget(self.pushButton_harmonic_acoustic, 1, 0, 1, 1)

        self.pushButton_harmonic_coupled = QPushButton(self.frame_2)
        self.pushButton_harmonic_coupled.setObjectName(u"pushButton_harmonic_coupled")
        self.pushButton_harmonic_coupled.setMinimumSize(QSize(240, 36))
        self.pushButton_harmonic_coupled.setMaximumSize(QSize(240, 36))
        self.pushButton_harmonic_coupled.setFont(font1)
        self.pushButton_harmonic_coupled.setStyleSheet(u"")

        self.gridLayout_3.addWidget(self.pushButton_harmonic_coupled, 2, 0, 1, 1)

        self.line = QFrame(self.frame_2)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_3.addWidget(self.line, 3, 0, 1, 1)

        self.pushButton_modal_structural = QPushButton(self.frame_2)
        self.pushButton_modal_structural.setObjectName(u"pushButton_modal_structural")
        self.pushButton_modal_structural.setMinimumSize(QSize(240, 36))
        self.pushButton_modal_structural.setMaximumSize(QSize(240, 36))
        self.pushButton_modal_structural.setFont(font1)
        self.pushButton_modal_structural.setStyleSheet(u"")

        self.gridLayout_3.addWidget(self.pushButton_modal_structural, 4, 0, 1, 1)

        self.pushButton_modal_acoustic = QPushButton(self.frame_2)
        self.pushButton_modal_acoustic.setObjectName(u"pushButton_modal_acoustic")
        self.pushButton_modal_acoustic.setMinimumSize(QSize(240, 36))
        self.pushButton_modal_acoustic.setMaximumSize(QSize(240, 36))
        self.pushButton_modal_acoustic.setFont(font1)
        self.pushButton_modal_acoustic.setStyleSheet(u"")

        self.gridLayout_3.addWidget(self.pushButton_modal_acoustic, 5, 0, 1, 1)


        self.gridLayout_2.addWidget(self.frame_2, 1, 0, 1, 1)


        self.retranslateUi(Dialog)

        self.pushButton_harmonic_structural.setDefault(False)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Select analysis type ", None))
#if QT_CONFIG(whatsthis)
        Dialog.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.label.setText(QCoreApplication.translate("Dialog", u"Select the analysis type", None))
        self.pushButton_harmonic_structural.setText(QCoreApplication.translate("Dialog", u"Harmonic Analysis - Structural", None))
#if QT_CONFIG(shortcut)
        self.pushButton_harmonic_structural.setShortcut("")
#endif // QT_CONFIG(shortcut)
        self.pushButton_harmonic_acoustic.setText(QCoreApplication.translate("Dialog", u"Harmonic Analysis - Acoustic", None))
        self.pushButton_harmonic_coupled.setText(QCoreApplication.translate("Dialog", u"Harmonic Analysis - Coupled", None))
        self.pushButton_modal_structural.setText(QCoreApplication.translate("Dialog", u"Modal Analysis - Structural", None))
        self.pushButton_modal_acoustic.setText(QCoreApplication.translate("Dialog", u"Modal Analysis - Acoustic", None))
    # retranslateUi



class AnalysisTypeInput_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame_title: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
                - frame_2: QFrame
                    - (Layout): QGridLayout
                            - pushButton_harmonic_structural: QPushButton
                            - pushButton_harmonic_acoustic: QPushButton
                            - pushButton_harmonic_coupled: QPushButton
                            - line: Line
                            - pushButton_modal_structural: QPushButton
                            - pushButton_modal_acoustic: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
