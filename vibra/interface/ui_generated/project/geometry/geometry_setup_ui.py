# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'geometry_setup.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFrame,
    QGridLayout, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(353, 241)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.frame_2 = QFrame(Dialog)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Box)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.comboBox_length_units = QComboBox(self.frame_2)
        self.comboBox_length_units.addItem("")
        self.comboBox_length_units.addItem("")
        self.comboBox_length_units.addItem("")
        self.comboBox_length_units.setObjectName(u"comboBox_length_units")
        self.comboBox_length_units.setMinimumSize(QSize(120, 26))
        self.comboBox_length_units.setMaximumSize(QSize(16777215, 26))
        font = QFont()
        font.setPointSize(10)
        self.comboBox_length_units.setFont(font)

        self.gridLayout_4.addWidget(self.comboBox_length_units, 0, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.label_2 = QLabel(self.frame_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(0, 26))
        self.label_2.setMaximumSize(QSize(16777215, 26))
        self.label_2.setFont(font)
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_2, 0, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_2, 0, 3, 1, 1)

        self.label_3 = QLabel(self.frame_2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(0, 26))
        self.label_3.setMaximumSize(QSize(16777215, 26))
        self.label_3.setFont(font)
        self.label_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_3, 1, 1, 1, 1)

        self.comboBox_geometry_quality = QComboBox(self.frame_2)
        self.comboBox_geometry_quality.addItem("")
        self.comboBox_geometry_quality.addItem("")
        self.comboBox_geometry_quality.addItem("")
        self.comboBox_geometry_quality.setObjectName(u"comboBox_geometry_quality")
        self.comboBox_geometry_quality.setMinimumSize(QSize(120, 26))
        self.comboBox_geometry_quality.setMaximumSize(QSize(16777215, 26))
        self.comboBox_geometry_quality.setFont(font)

        self.gridLayout_4.addWidget(self.comboBox_geometry_quality, 1, 2, 1, 1)


        self.gridLayout.addWidget(self.frame_2, 1, 0, 1, 1)

        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 48))
        self.frame.setMaximumSize(QSize(16777215, 48))
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        font1 = QFont()
        font1.setPointSize(11)
        self.label.setFont(font1)
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

        self.frame_3 = QFrame(Dialog)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(0, 48))
        self.frame_3.setMaximumSize(QSize(16777215, 48))
        self.frame_3.setFrameShape(QFrame.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_3)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(4, 4, 4, 4)
        self.pushButton_proceed = QPushButton(self.frame_3)
        self.pushButton_proceed.setObjectName(u"pushButton_proceed")
        self.pushButton_proceed.setMinimumSize(QSize(100, 27))
        self.pushButton_proceed.setMaximumSize(QSize(100, 28))
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        self.pushButton_proceed.setFont(font2)
        self.pushButton_proceed.setStyleSheet(u"")

        self.gridLayout_3.addWidget(self.pushButton_proceed, 0, 1, 1, 1)

        self.pushButton_exit = QPushButton(self.frame_3)
        self.pushButton_exit.setObjectName(u"pushButton_exit")
        self.pushButton_exit.setMinimumSize(QSize(100, 27))
        self.pushButton_exit.setMaximumSize(QSize(100, 28))
        self.pushButton_exit.setFont(font2)
        self.pushButton_exit.setStyleSheet(u"")

        self.gridLayout_3.addWidget(self.pushButton_exit, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_3, 2, 0, 1, 1)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.comboBox_length_units.setItemText(0, QCoreApplication.translate("Dialog", u"millimeter", None))
        self.comboBox_length_units.setItemText(1, QCoreApplication.translate("Dialog", u"meter", None))
        self.comboBox_length_units.setItemText(2, QCoreApplication.translate("Dialog", u"inch", None))

        self.label_2.setText(QCoreApplication.translate("Dialog", u"Length unit:", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Geometry quality:", None))
        self.comboBox_geometry_quality.setItemText(0, QCoreApplication.translate("Dialog", u"automatic", None))
        self.comboBox_geometry_quality.setItemText(1, QCoreApplication.translate("Dialog", u"fine", None))
        self.comboBox_geometry_quality.setItemText(2, QCoreApplication.translate("Dialog", u"coarse", None))

        self.label.setText(QCoreApplication.translate("Dialog", u"Geometry setup", None))
#if QT_CONFIG(tooltip)
        self.pushButton_proceed.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_proceed.setText(QCoreApplication.translate("Dialog", u"Proceed", None))
#if QT_CONFIG(tooltip)
        self.pushButton_exit.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_exit.setText(QCoreApplication.translate("Dialog", u"Exit", None))
    # retranslateUi



class GeometrySetup_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame_2: QFrame
                    - (Layout): QGridLayout
                            - comboBox_length_units: QComboBox
                            - label_2: QLabel
                            - label_3: QLabel
                            - comboBox_geometry_quality: QComboBox
                - frame: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
                - frame_3: QFrame
                    - (Layout): QGridLayout
                            - pushButton_proceed: QPushButton
                            - pushButton_exit: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
