# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mesh_quality_histogram_plot.ui'
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
from PySide6.QtWidgets import (QApplication, QButtonGroup, QDialog, QFrame,
    QGridLayout, QLabel, QSizePolicy, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(1000, 723)
        Dialog.setMinimumSize(QSize(900, 600))
        Dialog.setStyleSheet(u"")
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.frame_lower = QFrame(Dialog)
        self.frame_lower.setObjectName(u"frame_lower")
        self.frame_lower.setMinimumSize(QSize(0, 200))
        self.frame_lower.setFrameShape(QFrame.Shape.Box)
        self.frame_lower.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_20 = QGridLayout(self.frame_lower)
        self.gridLayout_20.setSpacing(2)
        self.gridLayout_20.setObjectName(u"gridLayout_20")
        self.gridLayout_20.setContentsMargins(2, 2, 2, 2)
        self.frame_left = QFrame(self.frame_lower)
        self.frame_left.setObjectName(u"frame_left")
        self.frame_left.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_left.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_left)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(4, 4, 4, 4)
        self.widget_plot = QWidget(self.frame_left)
        self.widget_plot.setObjectName(u"widget_plot")

        self.gridLayout_2.addWidget(self.widget_plot, 0, 1, 1, 1)


        self.gridLayout_20.addWidget(self.frame_left, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_lower, 1, 0, 1, 2)

        self.frame_3 = QFrame(Dialog)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(0, 48))
        self.frame_3.setMaximumSize(QSize(16777215, 48))
        self.frame_3.setFrameShape(QFrame.Shape.Box)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_7 = QGridLayout(self.frame_3)
        self.gridLayout_7.setSpacing(2)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(2, 2, 2, 2)
        self.label_14 = QLabel(self.frame_3)
        self.label_14.setObjectName(u"label_14")
        font = QFont()
        font.setPointSize(12)
        font.setBold(False)
        self.label_14.setFont(font)
        self.label_14.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_7.addWidget(self.label_14, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_3, 0, 0, 1, 2)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_14.setText(QCoreApplication.translate("Dialog", u"Mesh qualilty histogram plotter", None))
    # retranslateUi



class MeshQualityHistogramPlot_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame_lower: QFrame
                    - (Layout): QGridLayout
                            - frame_left: QFrame
                                - (Layout): QGridLayout
                                        - widget_plot: QWidget
                - frame_3: QFrame
                    - (Layout): QGridLayout
                            - label_14: QLabel
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
