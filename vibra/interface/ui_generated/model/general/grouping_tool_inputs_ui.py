# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'grouping_tool_inputs.ui'
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
    QGridLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QWidget)

from vibra.interface.formatters.icons import Icon

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
        self.frame.setMinimumSize(QSize(0, 40))
        self.frame.setMaximumSize(QSize(520, 40))
        self.frame.setFrameShape(QFrame.Shape.Box)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.frame.setLineWidth(1)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(0, 30))
        self.label.setMaximumSize(QSize(452, 30))
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        self.label.setFont(font)
        self.label.setTextFormat(Qt.TextFormat.AutoText)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

        self.frame_2 = QFrame(Dialog)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(0, 0))
        self.frame_2.setMaximumSize(QSize(520, 460))
        self.frame_2.setFrameShape(QFrame.Shape.Box)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_2)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(4, 4, 4, 4)
        self.frame_3 = QFrame(self.frame_2)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(0, 48))
        self.frame_3.setMaximumSize(QSize(16777215, 48))
        self.frame_3.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_47 = QGridLayout(self.frame_3)
        self.gridLayout_47.setSpacing(2)
        self.gridLayout_47.setObjectName(u"gridLayout_47")
        self.gridLayout_47.setContentsMargins(2, 2, 2, 2)
        self.pushButton_select_all = QPushButton(self.frame_3)
        self.pushButton_select_all.setObjectName(u"pushButton_select_all")
        self.pushButton_select_all.setMinimumSize(QSize(120, 32))
        self.pushButton_select_all.setMaximumSize(QSize(120, 32))
        font1 = QFont()
        font1.setPointSize(10)
        self.pushButton_select_all.setFont(font1)
        self.pushButton_select_all.setStyleSheet(u"")
        self.pushButton_select_all.setAutoDefault(False)
        self.pushButton_select_all.setFlat(False)

        self.gridLayout_47.addWidget(self.pushButton_select_all, 0, 1, 1, 1)

        self.pushButton_select_by_size = QPushButton(self.frame_3)
        self.pushButton_select_by_size.setObjectName(u"pushButton_select_by_size")
        self.pushButton_select_by_size.setMinimumSize(QSize(120, 32))
        self.pushButton_select_by_size.setMaximumSize(QSize(120, 32))
        self.pushButton_select_by_size.setFont(font1)
        self.pushButton_select_by_size.setStyleSheet(u"")
        self.pushButton_select_by_size.setAutoDefault(False)
        self.pushButton_select_by_size.setFlat(False)

        self.gridLayout_47.addWidget(self.pushButton_select_by_size, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_3, 1, 0, 1, 1)

        self.frame_5 = QFrame(self.frame_2)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setMinimumSize(QSize(0, 48))
        self.frame_5.setMaximumSize(QSize(16777215, 200))
        self.frame_5.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_6 = QGridLayout(self.frame_5)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setHorizontalSpacing(6)
        self.gridLayout_6.setVerticalSpacing(2)
        self.gridLayout_6.setContentsMargins(2, 6, 2, 2)
        self.label_3 = QLabel(self.frame_5)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(160, 30))
        self.label_3.setMaximumSize(QSize(160, 30))
        self.label_3.setFont(font1)
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_3, 1, 1, 1, 1)

        self.frame_6 = QFrame(self.frame_5)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setMinimumSize(QSize(40, 30))
        self.frame_6.setMaximumSize(QSize(40, 30))
        self.frame_6.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_6.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_6.addWidget(self.frame_6, 0, 3, 1, 1)

        self.lineEdit_group_label = QLineEdit(self.frame_5)
        self.lineEdit_group_label.setObjectName(u"lineEdit_group_label")
        self.lineEdit_group_label.setMinimumSize(QSize(110, 30))
        self.lineEdit_group_label.setMaximumSize(QSize(110, 30))
        self.lineEdit_group_label.setFont(font1)
        self.lineEdit_group_label.setStyleSheet(u"")
        self.lineEdit_group_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_6.addWidget(self.lineEdit_group_label, 2, 2, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_4, 0, 4, 1, 1)

        self.comboBox_domain_filter = QComboBox(self.frame_5)
        self.comboBox_domain_filter.addItem("")
        self.comboBox_domain_filter.addItem("")
        self.comboBox_domain_filter.addItem("")
        self.comboBox_domain_filter.setObjectName(u"comboBox_domain_filter")
        self.comboBox_domain_filter.setMinimumSize(QSize(110, 30))
        self.comboBox_domain_filter.setMaximumSize(QSize(110, 30))
        self.comboBox_domain_filter.setFont(font1)
        self.comboBox_domain_filter.setStyleSheet(u"")

        self.gridLayout_6.addWidget(self.comboBox_domain_filter, 1, 2, 1, 1)

        self.pushButton_create_group = QPushButton(self.frame_5)
        self.pushButton_create_group.setObjectName(u"pushButton_create_group")
        self.pushButton_create_group.setMinimumSize(QSize(40, 30))
        self.pushButton_create_group.setMaximumSize(QSize(40, 30))
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        font2.setPointSize(11)
        font2.setBold(True)
        font2.setItalic(False)
        self.pushButton_create_group.setFont(font2)
        self.pushButton_create_group.setStyleSheet(u"")
        icon = Icon(u":/icons/plus-thick.png")
        self.pushButton_create_group.setIcon(icon)
        self.pushButton_create_group.setIconSize(QSize(20, 20))
        self.pushButton_create_group.setAutoDefault(False)
        self.pushButton_create_group.setFlat(False)

        self.gridLayout_6.addWidget(self.pushButton_create_group, 2, 3, 1, 1)

        self.label_10 = QLabel(self.frame_5)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(160, 30))
        self.label_10.setMaximumSize(QSize(160, 30))
        font3 = QFont()
        font3.setFamilies([u"MS Shell Dlg 2"])
        font3.setPointSize(10)
        font3.setBold(False)
        font3.setItalic(False)
        self.label_10.setFont(font3)
        self.label_10.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_10, 2, 1, 1, 1)

        self.label_2 = QLabel(self.frame_5)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(160, 30))
        self.label_2.setMaximumSize(QSize(160, 30))
        self.label_2.setFont(font1)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_2, 0, 1, 1, 1)

        self.comboBox_selector_filter = QComboBox(self.frame_5)
        self.comboBox_selector_filter.addItem("")
        self.comboBox_selector_filter.addItem("")
        self.comboBox_selector_filter.addItem("")
        self.comboBox_selector_filter.setObjectName(u"comboBox_selector_filter")
        self.comboBox_selector_filter.setMinimumSize(QSize(110, 30))
        self.comboBox_selector_filter.setMaximumSize(QSize(110, 30))
        self.comboBox_selector_filter.setFont(font1)
        self.comboBox_selector_filter.setStyleSheet(u"")

        self.gridLayout_6.addWidget(self.comboBox_selector_filter, 0, 2, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_3, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_5, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_2, 1, 0, 1, 1)


        self.retranslateUi(Dialog)

        self.comboBox_domain_filter.setCurrentIndex(0)
        self.comboBox_selector_filter.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Grouping tool", None))
        self.pushButton_select_all.setText(QCoreApplication.translate("Dialog", u"Select all", None))
        self.pushButton_select_by_size.setText(QCoreApplication.translate("Dialog", u"Select by size", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Domain filter: ", None))
        self.lineEdit_group_label.setText("")
        self.comboBox_domain_filter.setItemText(0, QCoreApplication.translate("Dialog", u"None", None))
        self.comboBox_domain_filter.setItemText(1, QCoreApplication.translate("Dialog", u"Acoustic", None))
        self.comboBox_domain_filter.setItemText(2, QCoreApplication.translate("Dialog", u"Structural", None))

#if QT_CONFIG(tooltip)
        self.pushButton_create_group.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:10pt; font-weight:400;\">Press to export the current response function</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_create_group.setText("")
        self.label_10.setText(QCoreApplication.translate("Dialog", u"Group label: ", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Selector filter: ", None))
        self.comboBox_selector_filter.setItemText(0, QCoreApplication.translate("Dialog", u"Volumes", None))
        self.comboBox_selector_filter.setItemText(1, QCoreApplication.translate("Dialog", u"Surfaces", None))
        self.comboBox_selector_filter.setItemText(2, QCoreApplication.translate("Dialog", u"Lines", None))

    # retranslateUi



class GroupingToolInputs_UI(QDialog, Ui_Dialog):
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
                                        - pushButton_select_all: QPushButton
                                        - pushButton_select_by_size: QPushButton
                            - frame_5: QFrame
                                - (Layout): QGridLayout
                                        - label_3: QLabel
                                        - frame_6: QFrame
                                        - lineEdit_group_label: QLineEdit
                                        - comboBox_domain_filter: QComboBox
                                        - pushButton_create_group: QPushButton
                                        - label_10: QLabel
                                        - label_2: QLabel
                                        - comboBox_selector_filter: QComboBox
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
