# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'element_options_input.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFrame,
    QGridLayout, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QTabWidget, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(400, 300)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.frame_buttons_2 = QFrame(Dialog)
        self.frame_buttons_2.setObjectName(u"frame_buttons_2")
        self.frame_buttons_2.setMinimumSize(QSize(0, 48))
        self.frame_buttons_2.setMaximumSize(QSize(16777215, 48))
        self.frame_buttons_2.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_buttons_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_11 = QGridLayout(self.frame_buttons_2)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setVerticalSpacing(0)
        self.gridLayout_11.setContentsMargins(6, 0, 6, 0)
        self.pushButton_apply_and_close = QPushButton(self.frame_buttons_2)
        self.pushButton_apply_and_close.setObjectName(u"pushButton_apply_and_close")
        self.pushButton_apply_and_close.setMinimumSize(QSize(72, 30))
        self.pushButton_apply_and_close.setMaximumSize(QSize(72, 30))
        font = QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        self.pushButton_apply_and_close.setFont(font)
        self.pushButton_apply_and_close.setStyleSheet(u"")
        self.pushButton_apply_and_close.setAutoDefault(False)
        self.pushButton_apply_and_close.setFlat(False)

        self.gridLayout_11.addWidget(self.pushButton_apply_and_close, 0, 3, 1, 1)

        self.pushButton_apply = QPushButton(self.frame_buttons_2)
        self.pushButton_apply.setObjectName(u"pushButton_apply")
        self.pushButton_apply.setMinimumSize(QSize(72, 30))
        self.pushButton_apply.setMaximumSize(QSize(72, 30))
        self.pushButton_apply.setFont(font)
        self.pushButton_apply.setStyleSheet(u"")
        self.pushButton_apply.setAutoDefault(False)
        self.pushButton_apply.setFlat(False)

        self.gridLayout_11.addWidget(self.pushButton_apply, 0, 2, 1, 1)

        self.pushButton_cancel = QPushButton(self.frame_buttons_2)
        self.pushButton_cancel.setObjectName(u"pushButton_cancel")
        self.pushButton_cancel.setMinimumSize(QSize(72, 30))
        self.pushButton_cancel.setMaximumSize(QSize(72, 30))
        self.pushButton_cancel.setFont(font)
        self.pushButton_cancel.setStyleSheet(u"")
        self.pushButton_cancel.setAutoDefault(False)
        self.pushButton_cancel.setFlat(False)

        self.gridLayout_11.addWidget(self.pushButton_cancel, 0, 0, 1, 1)

        self.horizontalSpacer_17 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_11.addItem(self.horizontalSpacer_17, 0, 1, 1, 1)


        self.gridLayout.addWidget(self.frame_buttons_2, 2, 0, 1, 1)

        self.frame_title = QFrame(Dialog)
        self.frame_title.setObjectName(u"frame_title")
        self.frame_title.setMinimumSize(QSize(0, 48))
        self.frame_title.setMaximumSize(QSize(16777215, 48))
        self.frame_title.setFrameShape(QFrame.Shape.Box)
        self.frame_title.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_title)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label = QLabel(self.frame_title)
        self.label.setObjectName(u"label")
        font1 = QFont()
        font1.setPointSize(11)
        self.label.setFont(font1)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_title, 0, 0, 1, 1)

        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.Box)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.tabWidget_main = QTabWidget(self.frame)
        self.tabWidget_main.setObjectName(u"tabWidget_main")
        self.tab_hex8 = QWidget()
        self.tab_hex8.setObjectName(u"tab_hex8")
        self.gridLayout_4 = QGridLayout(self.tab_hex8)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.label_option_3 = QLabel(self.tab_hex8)
        self.label_option_3.setObjectName(u"label_option_3")
        self.label_option_3.setMinimumSize(QSize(120, 20))
        self.label_option_3.setMaximumSize(QSize(160, 16777215))
        font2 = QFont()
        font2.setPointSize(10)
        self.label_option_3.setFont(font2)
        self.label_option_3.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_option_3, 2, 1, 1, 1)

        self.comboBox_extra_shape_functions = QComboBox(self.tab_hex8)
        self.comboBox_extra_shape_functions.addItem("")
        self.comboBox_extra_shape_functions.addItem("")
        self.comboBox_extra_shape_functions.setObjectName(u"comboBox_extra_shape_functions")
        self.comboBox_extra_shape_functions.setMinimumSize(QSize(100, 0))
        self.comboBox_extra_shape_functions.setMaximumSize(QSize(16777215, 28))
        self.comboBox_extra_shape_functions.setFont(font2)

        self.gridLayout_4.addWidget(self.comboBox_extra_shape_functions, 0, 2, 1, 1)

        self.label_option_2 = QLabel(self.tab_hex8)
        self.label_option_2.setObjectName(u"label_option_2")
        self.label_option_2.setMinimumSize(QSize(120, 20))
        self.label_option_2.setMaximumSize(QSize(160, 16777215))
        self.label_option_2.setFont(font2)
        self.label_option_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_option_2, 1, 1, 1, 1)

        self.comboBox_option_2 = QComboBox(self.tab_hex8)
        self.comboBox_option_2.setObjectName(u"comboBox_option_2")
        self.comboBox_option_2.setMinimumSize(QSize(100, 0))
        self.comboBox_option_2.setMaximumSize(QSize(16777215, 28))
        self.comboBox_option_2.setFont(font2)

        self.gridLayout_4.addWidget(self.comboBox_option_2, 1, 2, 1, 1)

        self.comboBox_option_3 = QComboBox(self.tab_hex8)
        self.comboBox_option_3.setObjectName(u"comboBox_option_3")
        self.comboBox_option_3.setMinimumSize(QSize(100, 0))
        self.comboBox_option_3.setMaximumSize(QSize(16777215, 28))
        self.comboBox_option_3.setFont(font2)

        self.gridLayout_4.addWidget(self.comboBox_option_3, 2, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer, 0, 3, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_2, 0, 0, 1, 1)

        self.label_16 = QLabel(self.tab_hex8)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setMinimumSize(QSize(120, 20))
        self.label_16.setMaximumSize(QSize(160, 16777215))
        self.label_16.setFont(font2)
        self.label_16.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_16, 0, 1, 1, 1)

        self.tabWidget_main.addTab(self.tab_hex8, "")
        self.tab_hex20 = QWidget()
        self.tab_hex20.setObjectName(u"tab_hex20")
        self.tabWidget_main.addTab(self.tab_hex20, "")
        self.tab_tet4 = QWidget()
        self.tab_tet4.setObjectName(u"tab_tet4")
        self.tabWidget_main.addTab(self.tab_tet4, "")
        self.tab_tet10 = QWidget()
        self.tab_tet10.setObjectName(u"tab_tet10")
        self.tabWidget_main.addTab(self.tab_tet10, "")

        self.gridLayout_2.addWidget(self.tabWidget_main, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame, 1, 0, 1, 1)


        self.retranslateUi(Dialog)

        self.pushButton_apply_and_close.setDefault(False)
        self.pushButton_apply.setDefault(False)
        self.pushButton_cancel.setDefault(False)
        self.tabWidget_main.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.pushButton_apply_and_close.setText(QCoreApplication.translate("Dialog", u"Ok", None))
        self.pushButton_apply.setText(QCoreApplication.translate("Dialog", u"Apply", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Advanced element options", None))
        self.label_option_3.setText(QCoreApplication.translate("Dialog", u"Option #3:", None))
        self.comboBox_extra_shape_functions.setItemText(0, QCoreApplication.translate("Dialog", u"disabled", None))
        self.comboBox_extra_shape_functions.setItemText(1, QCoreApplication.translate("Dialog", u"enabled", None))

        self.label_option_2.setText(QCoreApplication.translate("Dialog", u"Option #2:", None))
        self.label_16.setText(QCoreApplication.translate("Dialog", u"Extra shape functions:", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_hex8), QCoreApplication.translate("Dialog", u"Hex8", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_hex20), QCoreApplication.translate("Dialog", u"Hex20", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_tet4), QCoreApplication.translate("Dialog", u"Tet4", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_tet10), QCoreApplication.translate("Dialog", u"Tet10", None))
    # retranslateUi



class ElementOptionsInput_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame_buttons_2: QFrame
                    - (Layout): QGridLayout
                            - pushButton_apply_and_close: QPushButton
                            - pushButton_apply: QPushButton
                            - pushButton_cancel: QPushButton
                - frame_title: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
                - frame: QFrame
                    - (Layout): QGridLayout
                            - tabWidget_main: QTabWidget
                                - tab_hex8: QWidget
                                    - (Layout): QGridLayout
                                            - label_option_3: QLabel
                                            - comboBox_extra_shape_functions: QComboBox
                                            - label_option_2: QLabel
                                            - comboBox_option_2: QComboBox
                                            - comboBox_option_3: QComboBox
                                            - label_16: QLabel
                                - tab_hex20: QWidget
                                - tab_tet4: QWidget
                                - tab_tet10: QWidget
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
