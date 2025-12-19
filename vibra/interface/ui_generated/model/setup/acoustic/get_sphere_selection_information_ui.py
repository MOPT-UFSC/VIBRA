# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'get_sphere_selection_information.ui'
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
    QLabel, QLineEdit, QSizePolicy, QSpacerItem,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(420, 320)
        Dialog.setMinimumSize(QSize(420, 320))
        Dialog.setMaximumSize(QSize(420, 320))
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setMaximumSize(QSize(16777215, 48))
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

        self.frame_2 = QFrame(Dialog)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Box)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_2)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(4, 4, 4, 4)
        self.frame_3 = QFrame(self.frame_2)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_3)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(6, 6, 6, 6)
        self.label_2 = QLabel(self.frame_3)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(160, 0))
        self.label_2.setMaximumSize(QSize(160, 16777215))
        font1 = QFont()
        font1.setPointSize(10)
        self.label_2.setFont(font1)
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_2, 3, 1, 1, 1)

        self.lineEdit_coordinate_x = QLineEdit(self.frame_3)
        self.lineEdit_coordinate_x.setObjectName(u"lineEdit_coordinate_x")
        self.lineEdit_coordinate_x.setMinimumSize(QSize(0, 0))
        self.lineEdit_coordinate_x.setMaximumSize(QSize(140, 26))
        self.lineEdit_coordinate_x.setFont(font1)
        self.lineEdit_coordinate_x.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.lineEdit_coordinate_x, 0, 2, 1, 1)

        self.label_10 = QLabel(self.frame_3)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(160, 0))
        self.label_10.setMaximumSize(QSize(160, 16777215))
        self.label_10.setFont(font1)
        self.label_10.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_10, 0, 1, 1, 1)

        self.label_11 = QLabel(self.frame_3)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMinimumSize(QSize(34, 0))
        self.label_11.setMaximumSize(QSize(40, 16777215))
        self.label_11.setFont(font1)

        self.gridLayout_4.addWidget(self.label_11, 0, 3, 1, 1)

        self.label_14 = QLabel(self.frame_3)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setMinimumSize(QSize(160, 0))
        self.label_14.setMaximumSize(QSize(160, 16777215))
        self.label_14.setFont(font1)
        self.label_14.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_14, 2, 1, 1, 1)

        self.label_12 = QLabel(self.frame_3)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setMinimumSize(QSize(160, 0))
        self.label_12.setMaximumSize(QSize(160, 16777215))
        self.label_12.setFont(font1)
        self.label_12.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_12, 1, 1, 1, 1)

        self.label_15 = QLabel(self.frame_3)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setMinimumSize(QSize(34, 0))
        self.label_15.setMaximumSize(QSize(40, 16777215))
        self.label_15.setFont(font1)

        self.gridLayout_4.addWidget(self.label_15, 2, 3, 1, 1)

        self.label_13 = QLabel(self.frame_3)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setMinimumSize(QSize(34, 0))
        self.label_13.setMaximumSize(QSize(40, 16777215))
        self.label_13.setFont(font1)

        self.gridLayout_4.addWidget(self.label_13, 1, 3, 1, 1)

        self.lineEdit_selection_radius = QLineEdit(self.frame_3)
        self.lineEdit_selection_radius.setObjectName(u"lineEdit_selection_radius")
        self.lineEdit_selection_radius.setMaximumSize(QSize(140, 26))
        self.lineEdit_selection_radius.setFont(font1)
        self.lineEdit_selection_radius.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.lineEdit_selection_radius, 3, 2, 1, 1)

        self.label_3 = QLabel(self.frame_3)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(160, 0))
        self.label_3.setMaximumSize(QSize(160, 16777215))
        self.label_3.setFont(font1)
        self.label_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_3, 4, 1, 1, 1)

        self.label_4 = QLabel(self.frame_3)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMaximumSize(QSize(40, 16777215))
        self.label_4.setFont(font1)

        self.gridLayout_4.addWidget(self.label_4, 3, 3, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.lineEdit_coordinate_y = QLineEdit(self.frame_3)
        self.lineEdit_coordinate_y.setObjectName(u"lineEdit_coordinate_y")
        self.lineEdit_coordinate_y.setMinimumSize(QSize(0, 0))
        self.lineEdit_coordinate_y.setMaximumSize(QSize(140, 26))
        self.lineEdit_coordinate_y.setFont(font1)
        self.lineEdit_coordinate_y.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.lineEdit_coordinate_y, 1, 2, 1, 1)

        self.lineEdit_coordinate_z = QLineEdit(self.frame_3)
        self.lineEdit_coordinate_z.setObjectName(u"lineEdit_coordinate_z")
        self.lineEdit_coordinate_z.setMinimumSize(QSize(0, 0))
        self.lineEdit_coordinate_z.setMaximumSize(QSize(140, 26))
        self.lineEdit_coordinate_z.setFont(font1)
        self.lineEdit_coordinate_z.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.lineEdit_coordinate_z, 2, 2, 1, 1)

        self.label_6 = QLabel(self.frame_3)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(160, 0))
        self.label_6.setMaximumSize(QSize(160, 16777215))
        self.label_6.setFont(font1)
        self.label_6.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_6, 5, 1, 1, 1)

        self.lineEdit_number_of_elements = QLineEdit(self.frame_3)
        self.lineEdit_number_of_elements.setObjectName(u"lineEdit_number_of_elements")
        self.lineEdit_number_of_elements.setMaximumSize(QSize(140, 26))
        self.lineEdit_number_of_elements.setFont(font1)
        self.lineEdit_number_of_elements.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.lineEdit_number_of_elements, 4, 2, 1, 1)

        self.lineEdit_number_of_nodes = QLineEdit(self.frame_3)
        self.lineEdit_number_of_nodes.setObjectName(u"lineEdit_number_of_nodes")
        self.lineEdit_number_of_nodes.setMaximumSize(QSize(140, 26))
        self.lineEdit_number_of_nodes.setFont(font1)
        self.lineEdit_number_of_nodes.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.lineEdit_number_of_nodes, 5, 2, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_2, 0, 4, 1, 1)


        self.gridLayout_3.addWidget(self.frame_3, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_2, 1, 0, 1, 1)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Selection information", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Selection radius:", None))
        self.label_10.setText(QCoreApplication.translate("Dialog", u"Center coordinate x:", None))
        self.label_11.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.label_14.setText(QCoreApplication.translate("Dialog", u"Center coordinate z:", None))
        self.label_12.setText(QCoreApplication.translate("Dialog", u"Center coordinate y:", None))
        self.label_15.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.label_13.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Number of elements:", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"Number of nodes:", None))
    # retranslateUi



class GetSphereSelectionInformation_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
                - frame_2: QFrame
                    - (Layout): QGridLayout
                            - frame_3: QFrame
                                - (Layout): QGridLayout
                                        - label_2: QLabel
                                        - lineEdit_coordinate_x: QLineEdit
                                        - label_10: QLabel
                                        - label_11: QLabel
                                        - label_14: QLabel
                                        - label_12: QLabel
                                        - label_15: QLabel
                                        - label_13: QLabel
                                        - lineEdit_selection_radius: QLineEdit
                                        - label_3: QLabel
                                        - label_4: QLabel
                                        - lineEdit_coordinate_y: QLineEdit
                                        - lineEdit_coordinate_z: QLineEdit
                                        - label_6: QLabel
                                        - lineEdit_number_of_elements: QLineEdit
                                        - lineEdit_number_of_nodes: QLineEdit
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
