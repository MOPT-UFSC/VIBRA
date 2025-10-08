# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'chose_propertyto_delete.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QGridLayout,
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(400, 150)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(400, 150))
        Dialog.setMaximumSize(QSize(400, 150))
        self.gridLayout_2 = QGridLayout(Dialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.horizontalSpacer = QSpacerItem(20, 10, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_2, 0, 3, 1, 1)

        self.property_comboBox = QComboBox(Dialog)
        self.property_comboBox.setObjectName(u"property_comboBox")

        self.gridLayout_2.addWidget(self.property_comboBox, 0, 2, 1, 1)

        self.confirm_pushButton = QPushButton(Dialog)
        self.confirm_pushButton.setObjectName(u"confirm_pushButton")

        self.gridLayout_2.addWidget(self.confirm_pushButton, 1, 2, 1, 1)

        self.cancel_pushButton = QPushButton(Dialog)
        self.cancel_pushButton.setObjectName(u"cancel_pushButton")

        self.gridLayout_2.addWidget(self.cancel_pushButton, 1, 1, 1, 1)

        self.message_label = QLabel(Dialog)
        self.message_label.setObjectName(u"message_label")

        self.gridLayout_2.addWidget(self.message_label, 0, 1, 1, 1)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.confirm_pushButton.setText(QCoreApplication.translate("Dialog", u"PushButton", None))
        self.cancel_pushButton.setText(QCoreApplication.translate("Dialog", u"PushButton", None))
        self.message_label.setText(QCoreApplication.translate("Dialog", u"TextLabel", None))
    # retranslateUi



class ChosePropertytoDelete_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - property_comboBox: QComboBox
                - confirm_pushButton: QPushButton
                - cancel_pushButton: QPushButton
                - message_label: QLabel
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
