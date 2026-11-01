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
    QGridLayout, QHeaderView, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QTabWidget,
    QTreeWidget, QTreeWidgetItem, QWidget)

from vibra.interface.formatters.icons import Icon

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(400, 327)
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
        self.tabWidget = QTabWidget(self.frame_2)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab_main = QWidget()
        self.tab_main.setObjectName(u"tab_main")
        self.gridLayout_5 = QGridLayout(self.tab_main)
        self.gridLayout_5.setSpacing(4)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(4, 4, 4, 4)
        self.frame_4 = QFrame(self.tab_main)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMaximumSize(QSize(16777215, 48))
        self.frame_4.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.lineEdit_group_label = QLineEdit(self.frame_4)
        self.lineEdit_group_label.setObjectName(u"lineEdit_group_label")
        self.lineEdit_group_label.setMinimumSize(QSize(160, 30))
        self.lineEdit_group_label.setMaximumSize(QSize(160, 30))
        font1 = QFont()
        font1.setPointSize(10)
        self.lineEdit_group_label.setFont(font1)
        self.lineEdit_group_label.setStyleSheet(u"")
        self.lineEdit_group_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.lineEdit_group_label, 0, 2, 1, 1)

        self.label_10 = QLabel(self.frame_4)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(100, 30))
        self.label_10.setMaximumSize(QSize(100, 30))
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        self.label_10.setFont(font2)
        self.label_10.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_10, 0, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer, 0, 4, 1, 1)

        self.pushButton_create_group = QPushButton(self.frame_4)
        self.pushButton_create_group.setObjectName(u"pushButton_create_group")
        self.pushButton_create_group.setMinimumSize(QSize(40, 30))
        self.pushButton_create_group.setMaximumSize(QSize(40, 30))
        font3 = QFont()
        font3.setFamilies([u"MS Shell Dlg 2"])
        font3.setPointSize(11)
        font3.setBold(True)
        font3.setItalic(False)
        self.pushButton_create_group.setFont(font3)
        self.pushButton_create_group.setStyleSheet(u"")
        icon = Icon(u":/icons/plus-thick.png")
        self.pushButton_create_group.setIcon(icon)
        self.pushButton_create_group.setIconSize(QSize(20, 20))
        self.pushButton_create_group.setAutoDefault(False)
        self.pushButton_create_group.setFlat(False)

        self.gridLayout_4.addWidget(self.pushButton_create_group, 0, 3, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_2, 0, 0, 1, 1)


        self.gridLayout_5.addWidget(self.frame_4, 1, 0, 1, 1)

        self.frame_5 = QFrame(self.tab_main)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setMinimumSize(QSize(0, 80))
        self.frame_5.setMaximumSize(QSize(16777215, 120))
        self.frame_5.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_6 = QGridLayout(self.frame_5)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setHorizontalSpacing(6)
        self.gridLayout_6.setVerticalSpacing(2)
        self.gridLayout_6.setContentsMargins(2, 6, 2, 2)
        self.label_3 = QLabel(self.frame_5)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(110, 30))
        self.label_3.setMaximumSize(QSize(110, 30))
        self.label_3.setFont(font1)
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_3, 2, 1, 1, 1)

        self.comboBox_mode = QComboBox(self.frame_5)
        self.comboBox_mode.addItem("")
        self.comboBox_mode.addItem("")
        self.comboBox_mode.setObjectName(u"comboBox_mode")
        self.comboBox_mode.setMinimumSize(QSize(120, 30))
        self.comboBox_mode.setMaximumSize(QSize(120, 30))
        self.comboBox_mode.setFont(font1)
        self.comboBox_mode.setStyleSheet(u"")

        self.gridLayout_6.addWidget(self.comboBox_mode, 3, 2, 1, 1)

        self.pushButton_select = QPushButton(self.frame_5)
        self.pushButton_select.setObjectName(u"pushButton_select")
        self.pushButton_select.setMinimumSize(QSize(40, 30))
        self.pushButton_select.setMaximumSize(QSize(40, 30))
        self.pushButton_select.setFont(font3)
        self.pushButton_select.setStyleSheet(u"")
        icon1 = Icon(u":/icons/selection_icon.png")
        self.pushButton_select.setIcon(icon1)
        self.pushButton_select.setIconSize(QSize(20, 20))
        self.pushButton_select.setAutoDefault(False)
        self.pushButton_select.setFlat(False)

        self.gridLayout_6.addWidget(self.pushButton_select, 3, 3, 1, 1)

        self.comboBox_selector_filter = QComboBox(self.frame_5)
        self.comboBox_selector_filter.addItem("")
        self.comboBox_selector_filter.addItem("")
        self.comboBox_selector_filter.addItem("")
        self.comboBox_selector_filter.setObjectName(u"comboBox_selector_filter")
        self.comboBox_selector_filter.setMinimumSize(QSize(120, 30))
        self.comboBox_selector_filter.setMaximumSize(QSize(120, 30))
        self.comboBox_selector_filter.setFont(font1)
        self.comboBox_selector_filter.setStyleSheet(u"")

        self.gridLayout_6.addWidget(self.comboBox_selector_filter, 1, 2, 1, 1)

        self.label_4 = QLabel(self.frame_5)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(110, 30))
        self.label_4.setMaximumSize(QSize(110, 30))
        self.label_4.setFont(font1)
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_4, 3, 1, 1, 1)

        self.label_2 = QLabel(self.frame_5)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(110, 30))
        self.label_2.setMaximumSize(QSize(110, 30))
        self.label_2.setFont(font1)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_2, 1, 1, 1, 1)

        self.comboBox_domain_filter = QComboBox(self.frame_5)
        self.comboBox_domain_filter.addItem("")
        self.comboBox_domain_filter.addItem("")
        self.comboBox_domain_filter.addItem("")
        self.comboBox_domain_filter.setObjectName(u"comboBox_domain_filter")
        self.comboBox_domain_filter.setMinimumSize(QSize(120, 30))
        self.comboBox_domain_filter.setMaximumSize(QSize(120, 30))
        self.comboBox_domain_filter.setFont(font1)
        self.comboBox_domain_filter.setStyleSheet(u"")

        self.gridLayout_6.addWidget(self.comboBox_domain_filter, 2, 2, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_4, 3, 4, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_3, 3, 0, 1, 1)


        self.gridLayout_5.addWidget(self.frame_5, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_main, "")
        self.tab_list = QWidget()
        self.tab_list.setObjectName(u"tab_list")
        self.gridLayout_7 = QGridLayout(self.tab_list)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.treeWidget_main = QTreeWidget(self.tab_list)
        self.treeWidget_main.setObjectName(u"treeWidget_main")

        self.gridLayout_7.addWidget(self.treeWidget_main, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_list, "")

        self.gridLayout_3.addWidget(self.tabWidget, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_2, 1, 0, 1, 1)


        self.retranslateUi(Dialog)

        self.tabWidget.setCurrentIndex(0)
        self.comboBox_mode.setCurrentIndex(0)
        self.comboBox_selector_filter.setCurrentIndex(0)
        self.comboBox_domain_filter.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Grouping tool", None))
        self.lineEdit_group_label.setText("")
        self.label_10.setText(QCoreApplication.translate("Dialog", u"Group label: ", None))
#if QT_CONFIG(tooltip)
        self.pushButton_create_group.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:10pt; font-weight:400;\">Press to export the current response function</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_create_group.setText("")
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Domain filter: ", None))
        self.comboBox_mode.setItemText(0, QCoreApplication.translate("Dialog", u"Select all", None))
        self.comboBox_mode.setItemText(1, QCoreApplication.translate("Dialog", u"Select by side", None))

#if QT_CONFIG(tooltip)
        self.pushButton_select.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:10pt; font-weight:400;\">Press to export the current response function</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_select.setText("")
        self.comboBox_selector_filter.setItemText(0, QCoreApplication.translate("Dialog", u"Volumes", None))
        self.comboBox_selector_filter.setItemText(1, QCoreApplication.translate("Dialog", u"Surfaces", None))
        self.comboBox_selector_filter.setItemText(2, QCoreApplication.translate("Dialog", u"Lines", None))

        self.label_4.setText(QCoreApplication.translate("Dialog", u"Selection mode: ", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Selector filter: ", None))
        self.comboBox_domain_filter.setItemText(0, QCoreApplication.translate("Dialog", u"None", None))
        self.comboBox_domain_filter.setItemText(1, QCoreApplication.translate("Dialog", u"Acoustic", None))
        self.comboBox_domain_filter.setItemText(2, QCoreApplication.translate("Dialog", u"Structural", None))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_main), QCoreApplication.translate("Dialog", u"Main", None))
        ___qtreewidgetitem = self.treeWidget_main.headerItem()
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("Dialog", u"IDs", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"Entity type", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Group label", None));
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_list), QCoreApplication.translate("Dialog", u"List", None))
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
                            - tabWidget: QTabWidget
                                - tab_main: QWidget
                                    - (Layout): QGridLayout
                                            - frame_4: QFrame
                                                - (Layout): QGridLayout
                                                        - lineEdit_group_label: QLineEdit
                                                        - label_10: QLabel
                                                        - pushButton_create_group: QPushButton
                                            - frame_5: QFrame
                                                - (Layout): QGridLayout
                                                        - label_3: QLabel
                                                        - comboBox_mode: QComboBox
                                                        - pushButton_select: QPushButton
                                                        - comboBox_selector_filter: QComboBox
                                                        - label_4: QLabel
                                                        - label_2: QLabel
                                                        - comboBox_domain_filter: QComboBox
                                - tab_list: QWidget
                                    - (Layout): QGridLayout
                                            - treeWidget_main: QTreeWidget
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
