# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'advanced_element_options_input.ui'
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
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.tabWidget_main = QTabWidget(self.frame)
        self.tabWidget_main.setObjectName(u"tabWidget_main")
        self.tab_hex8 = QWidget()
        self.tab_hex8.setObjectName(u"tab_hex8")
        self.gridLayout_4 = QGridLayout(self.tab_hex8)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.label_18 = QLabel(self.tab_hex8)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setMinimumSize(QSize(120, 20))
        self.label_18.setMaximumSize(QSize(160, 16777215))
        font = QFont()
        font.setPointSize(10)
        self.label_18.setFont(font)
        self.label_18.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_18, 2, 1, 1, 1)

        self.comboBox_extra_shape_functions = QComboBox(self.tab_hex8)
        self.comboBox_extra_shape_functions.addItem("")
        self.comboBox_extra_shape_functions.addItem("")
        self.comboBox_extra_shape_functions.setObjectName(u"comboBox_extra_shape_functions")
        self.comboBox_extra_shape_functions.setMinimumSize(QSize(100, 0))
        self.comboBox_extra_shape_functions.setMaximumSize(QSize(16777215, 28))
        self.comboBox_extra_shape_functions.setFont(font)

        self.gridLayout_4.addWidget(self.comboBox_extra_shape_functions, 0, 2, 1, 1)

        self.label_17 = QLabel(self.tab_hex8)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setMinimumSize(QSize(120, 20))
        self.label_17.setMaximumSize(QSize(160, 16777215))
        self.label_17.setFont(font)
        self.label_17.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_17, 1, 1, 1, 1)

        self.comboBox_option2 = QComboBox(self.tab_hex8)
        self.comboBox_option2.setObjectName(u"comboBox_option2")
        self.comboBox_option2.setMinimumSize(QSize(100, 0))
        self.comboBox_option2.setMaximumSize(QSize(16777215, 28))
        self.comboBox_option2.setFont(font)

        self.gridLayout_4.addWidget(self.comboBox_option2, 1, 2, 1, 1)

        self.comboBox_option3 = QComboBox(self.tab_hex8)
        self.comboBox_option3.setObjectName(u"comboBox_option3")
        self.comboBox_option3.setMinimumSize(QSize(100, 0))
        self.comboBox_option3.setMaximumSize(QSize(16777215, 28))
        self.comboBox_option3.setFont(font)

        self.gridLayout_4.addWidget(self.comboBox_option3, 2, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer, 0, 3, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_2, 0, 0, 1, 1)

        self.label_16 = QLabel(self.tab_hex8)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setMinimumSize(QSize(120, 20))
        self.label_16.setMaximumSize(QSize(160, 16777215))
        self.label_16.setFont(font)
        self.label_16.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

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

        self.frame_title = QFrame(Dialog)
        self.frame_title.setObjectName(u"frame_title")
        self.frame_title.setMinimumSize(QSize(0, 48))
        self.frame_title.setMaximumSize(QSize(16777215, 48))
        self.frame_title.setFrameShape(QFrame.Box)
        self.frame_title.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_title)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label = QLabel(self.frame_title)
        self.label.setObjectName(u"label")
        font1 = QFont()
        font1.setPointSize(11)
        self.label.setFont(font1)
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_title, 0, 0, 1, 1)

        self.frame_buttons = QFrame(Dialog)
        self.frame_buttons.setObjectName(u"frame_buttons")
        self.frame_buttons.setMinimumSize(QSize(0, 48))
        self.frame_buttons.setMaximumSize(QSize(16777215, 48))
        self.frame_buttons.setFrameShape(QFrame.NoFrame)
        self.frame_buttons.setFrameShadow(QFrame.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_buttons)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(4, 4, 4, 4)
        self.pushButton_exit = QPushButton(self.frame_buttons)
        self.pushButton_exit.setObjectName(u"pushButton_exit")
        self.pushButton_exit.setMinimumSize(QSize(120, 30))
        self.pushButton_exit.setMaximumSize(QSize(120, 30))
        self.pushButton_exit.setFont(font)
        self.pushButton_exit.setAutoDefault(False)

        self.gridLayout_5.addWidget(self.pushButton_exit, 0, 0, 1, 1)

        self.pushButton_confirm = QPushButton(self.frame_buttons)
        self.pushButton_confirm.setObjectName(u"pushButton_confirm")
        self.pushButton_confirm.setMinimumSize(QSize(120, 30))
        self.pushButton_confirm.setMaximumSize(QSize(120, 30))
        self.pushButton_confirm.setFont(font)
        self.pushButton_confirm.setAutoDefault(True)

        self.gridLayout_5.addWidget(self.pushButton_confirm, 0, 1, 1, 1)


        self.gridLayout.addWidget(self.frame_buttons, 2, 0, 1, 1)


        self.retranslateUi(Dialog)

        self.tabWidget_main.setCurrentIndex(0)
        self.pushButton_exit.setDefault(False)
        self.pushButton_confirm.setDefault(False)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_18.setText(QCoreApplication.translate("Dialog", u"Option #3:", None))
        self.comboBox_extra_shape_functions.setItemText(0, QCoreApplication.translate("Dialog", u"disabled", None))
        self.comboBox_extra_shape_functions.setItemText(1, QCoreApplication.translate("Dialog", u"enabled", None))

        self.label_17.setText(QCoreApplication.translate("Dialog", u"Option #2:", None))
        self.label_16.setText(QCoreApplication.translate("Dialog", u"Extra shape functions:", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_hex8), QCoreApplication.translate("Dialog", u"Hex8", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_hex20), QCoreApplication.translate("Dialog", u"Hex20", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_tet4), QCoreApplication.translate("Dialog", u"Tet4", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_tet10), QCoreApplication.translate("Dialog", u"Tet10", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Advanced element options", None))
        self.pushButton_exit.setText(QCoreApplication.translate("Dialog", u"Exit", None))
        self.pushButton_confirm.setText(QCoreApplication.translate("Dialog", u"Confirm", None))
    # retranslateUi



class AdvancedElementOptionsInput_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame: QFrame
                    - (Layout): QGridLayout
                            - tabWidget_main: QTabWidget
                                - tab_hex8: QWidget
                                    - (Layout): QGridLayout
                                            - label_18: QLabel
                                            - comboBox_extra_shape_functions: QComboBox
                                            - label_17: QLabel
                                            - comboBox_option2: QComboBox
                                            - comboBox_option3: QComboBox
                                            - label_16: QLabel
                                - tab_hex20: QWidget
                                - tab_tet4: QWidget
                                - tab_tet10: QWidget
                - frame_title: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
                - frame_buttons: QFrame
                    - (Layout): QGridLayout
                            - pushButton_exit: QPushButton
                            - pushButton_confirm: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
