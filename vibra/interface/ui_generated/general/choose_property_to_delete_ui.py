# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'choose_property_to_delete.ui'
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
        Dialog.resize(450, 150)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(450, 150))
        Dialog.setMaximumSize(QSize(600, 250))
        self.gridLayout_2 = QGridLayout(Dialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.message_label = QLabel(Dialog)
        self.message_label.setObjectName(u"message_label")
        self.message_label.setMinimumSize(QSize(0, 30))

        self.gridLayout_2.addWidget(self.message_label, 0, 1, 1, 1)

        self.property_comboBox = QComboBox(Dialog)
        self.property_comboBox.setObjectName(u"property_comboBox")

        self.gridLayout_2.addWidget(self.property_comboBox, 0, 2, 1, 2)

        self.confirm_pushButton = QPushButton(Dialog)
        self.confirm_pushButton.setObjectName(u"confirm_pushButton")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.confirm_pushButton.sizePolicy().hasHeightForWidth())
        self.confirm_pushButton.setSizePolicy(sizePolicy1)

        self.gridLayout_2.addWidget(self.confirm_pushButton, 1, 3, 1, 1)

        self.horizontalSpacer = QSpacerItem(20, 10, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_2, 0, 4, 1, 1)

        self.cancel_pushButton = QPushButton(Dialog)
        self.cancel_pushButton.setObjectName(u"cancel_pushButton")

        self.gridLayout_2.addWidget(self.cancel_pushButton, 1, 2, 1, 1)

        self.remove_all_pushButton = QPushButton(Dialog)
        self.remove_all_pushButton.setObjectName(u"remove_all_pushButton")

        self.gridLayout_2.addWidget(self.remove_all_pushButton, 1, 1, 1, 1)


        self.retranslateUi(Dialog)

        self.confirm_pushButton.setDefault(True)
        self.remove_all_pushButton.setDefault(False)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.message_label.setText(QCoreApplication.translate("Dialog", u"TextLabel", None))
        self.confirm_pushButton.setText(QCoreApplication.translate("Dialog", u"PushButton", None))
        self.cancel_pushButton.setText(QCoreApplication.translate("Dialog", u"PushButton", None))
        self.remove_all_pushButton.setText(QCoreApplication.translate("Dialog", u"PushButton", None))
    # retranslateUi



class ChoosePropertyToDelete_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - message_label: QLabel
                - property_comboBox: QComboBox
                - confirm_pushButton: QPushButton
                - cancel_pushButton: QPushButton
                - remove_all_pushButton: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
