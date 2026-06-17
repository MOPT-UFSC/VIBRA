# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'equations_for_DBM_porous_material_models.ui'
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
    QLabel, QPushButton, QSizePolicy, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(548, 487)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.frame_top = QFrame(Dialog)
        self.frame_top.setObjectName(u"frame_top")
        self.frame_top.setMinimumSize(QSize(0, 48))
        self.frame_top.setMaximumSize(QSize(16777215, 48))
        self.frame_top.setFrameShape(QFrame.Shape.Box)
        self.frame_top.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_top)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_3 = QLabel(self.frame_top)
        self.label_3.setObjectName(u"label_3")
        font = QFont()
        font.setPointSize(11)
        self.label_3.setFont(font)
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.label_3, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_top, 0, 0, 1, 1)

        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.Box)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_51 = QLabel(self.frame)
        self.label_51.setObjectName(u"label_51")
        self.label_51.setTextFormat(Qt.TextFormat.AutoText)
        self.label_51.setPixmap(QPixmap(u":/icons/figures/effective_acoustic_impedance_for_DBM_porous_material_models.png"))
        self.label_51.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.label_51, 3, 0, 1, 1)

        self.label_4 = QLabel(self.frame)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font)
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignJustify|Qt.AlignmentFlag.AlignVCenter)
        self.label_4.setWordWrap(True)

        self.gridLayout_2.addWidget(self.label_4, 6, 0, 1, 1)

        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(16777215, 48))
        self.label.setFont(font)

        self.gridLayout_2.addWidget(self.label, 2, 0, 1, 1)

        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMaximumSize(QSize(16777215, 48))
        self.label_2.setFont(font)

        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)

        self.label_52 = QLabel(self.frame)
        self.label_52.setObjectName(u"label_52")
        self.label_52.setTextFormat(Qt.TextFormat.AutoText)
        self.label_52.setPixmap(QPixmap(u":/icons/figures/effective_wavenumber_for_DBM_porous_material_models.png"))
        self.label_52.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.label_52, 1, 0, 1, 1)


        self.gridLayout.addWidget(self.frame, 1, 0, 1, 1)

        self.frame_bottom = QFrame(Dialog)
        self.frame_bottom.setObjectName(u"frame_bottom")
        self.frame_bottom.setMinimumSize(QSize(0, 48))
        self.frame_bottom.setMaximumSize(QSize(16777215, 48))
        self.frame_bottom.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_bottom.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_bottom)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.pushButton_exit = QPushButton(self.frame_bottom)
        self.pushButton_exit.setObjectName(u"pushButton_exit")
        self.pushButton_exit.setMinimumSize(QSize(100, 28))
        self.pushButton_exit.setMaximumSize(QSize(100, 28))
        font1 = QFont()
        font1.setPointSize(10)
        self.pushButton_exit.setFont(font1)

        self.gridLayout_4.addWidget(self.pushButton_exit, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_bottom, 2, 0, 1, 1)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Equations for Delany, Bazley and Miki porous material models ", None))
        self.label_51.setText("")
        self.label_4.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>where f is the frequency in Hz, \u03c3 is the flow resistivity in kg/m\u00b3.s, C<span style=\" vertical-align:sub;\">1</span> up to C<span style=\" vertical-align:sub;\">8</span> are the model constants, \u03c9 is the angular frequency in rad/s, \u03c1<span style=\" vertical-align:sub;\">0</span> is the medium density in kg/m\u00b3, and c<span style=\" vertical-align:sub;\">0</span> is the medium speed of sound in m/s.</p></body></html>", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>and acoustic impedance Z<span style=\" vertical-align:sub;\">eff</span></p></body></html>", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Effective complex wave number k<span style=\" vertical-align:sub;\">eff</span>:</p></body></html>", None))
        self.label_52.setText("")
        self.pushButton_exit.setText(QCoreApplication.translate("Dialog", u"Exit", None))
    # retranslateUi



class EquationsForDbmPorousMaterialModels_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame_top: QFrame
                    - (Layout): QGridLayout
                            - label_3: QLabel
                - frame: QFrame
                    - (Layout): QGridLayout
                            - label_51: QLabel
                            - label_4: QLabel
                            - label: QLabel
                            - label_2: QLabel
                            - label_52: QLabel
                - frame_bottom: QFrame
                    - (Layout): QGridLayout
                            - pushButton_exit: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
