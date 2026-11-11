# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'grouping_assistant_inputs.ui'
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
        Dialog.resize(490, 440)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.frame_2 = QFrame(Dialog)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(0, 0))
        self.frame_2.setMaximumSize(QSize(16777215, 460))
        self.frame_2.setFrameShape(QFrame.Shape.Box)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_2)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(4, 4, 4, 4)
        self.tabWidget_main = QTabWidget(self.frame_2)
        self.tabWidget_main.setObjectName(u"tabWidget_main")
        font = QFont()
        font.setPointSize(10)
        self.tabWidget_main.setFont(font)
        self.tab_main = QWidget()
        self.tab_main.setObjectName(u"tab_main")
        self.gridLayout_5 = QGridLayout(self.tab_main)
        self.gridLayout_5.setSpacing(4)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(4, 4, 4, 4)
        self.frame_4 = QFrame(self.tab_main)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMaximumSize(QSize(16777215, 84))
        self.frame_4.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer, 1, 3, 1, 1)

        self.lineEdit_selected_ids = QLineEdit(self.frame_4)
        self.lineEdit_selected_ids.setObjectName(u"lineEdit_selected_ids")
        self.lineEdit_selected_ids.setMinimumSize(QSize(320, 30))
        self.lineEdit_selected_ids.setMaximumSize(QSize(16777215, 30))
        self.lineEdit_selected_ids.setFont(font)
        self.lineEdit_selected_ids.setStyleSheet(u"")
        self.lineEdit_selected_ids.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.lineEdit_selected_ids, 0, 2, 1, 1)

        self.label_selected_ids = QLabel(self.frame_4)
        self.label_selected_ids.setObjectName(u"label_selected_ids")
        self.label_selected_ids.setMinimumSize(QSize(100, 30))
        self.label_selected_ids.setMaximumSize(QSize(100, 30))
        font1 = QFont()
        font1.setFamilies([u"MS Shell Dlg 2"])
        font1.setPointSize(10)
        font1.setBold(False)
        font1.setItalic(False)
        self.label_selected_ids.setFont(font1)
        self.label_selected_ids.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_selected_ids, 0, 1, 1, 1)

        self.label_10 = QLabel(self.frame_4)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(100, 30))
        self.label_10.setMaximumSize(QSize(100, 30))
        self.label_10.setFont(font1)
        self.label_10.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_10, 1, 1, 1, 1)

        self.lineEdit_group_label = QLineEdit(self.frame_4)
        self.lineEdit_group_label.setObjectName(u"lineEdit_group_label")
        self.lineEdit_group_label.setMinimumSize(QSize(320, 30))
        self.lineEdit_group_label.setMaximumSize(QSize(16777215, 30))
        self.lineEdit_group_label.setFont(font)
        self.lineEdit_group_label.setStyleSheet(u"")
        self.lineEdit_group_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.lineEdit_group_label, 1, 2, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_2, 1, 0, 1, 1)


        self.gridLayout_5.addWidget(self.frame_4, 2, 0, 1, 1)

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
        self.label_domain_filter = QLabel(self.frame_5)
        self.label_domain_filter.setObjectName(u"label_domain_filter")
        self.label_domain_filter.setMinimumSize(QSize(120, 30))
        self.label_domain_filter.setMaximumSize(QSize(120, 30))
        self.label_domain_filter.setFont(font)
        self.label_domain_filter.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_domain_filter, 2, 1, 1, 1)

        self.comboBox_selection_mode = QComboBox(self.frame_5)
        self.comboBox_selection_mode.addItem("")
        self.comboBox_selection_mode.addItem("")
        self.comboBox_selection_mode.addItem("")
        self.comboBox_selection_mode.setObjectName(u"comboBox_selection_mode")
        self.comboBox_selection_mode.setMinimumSize(QSize(120, 30))
        self.comboBox_selection_mode.setMaximumSize(QSize(120, 30))
        self.comboBox_selection_mode.setFont(font)
        self.comboBox_selection_mode.setStyleSheet(u"")

        self.gridLayout_6.addWidget(self.comboBox_selection_mode, 3, 2, 1, 1)

        self.pushButton_select = QPushButton(self.frame_5)
        self.pushButton_select.setObjectName(u"pushButton_select")
        self.pushButton_select.setMinimumSize(QSize(40, 30))
        self.pushButton_select.setMaximumSize(QSize(40, 30))
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        font2.setPointSize(11)
        font2.setBold(True)
        font2.setItalic(False)
        self.pushButton_select.setFont(font2)
        self.pushButton_select.setStyleSheet(u"")
        icon = Icon(u":/icons/selection_icon.png")
        self.pushButton_select.setIcon(icon)
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
        self.comboBox_selector_filter.setFont(font)
        self.comboBox_selector_filter.setStyleSheet(u"")

        self.gridLayout_6.addWidget(self.comboBox_selector_filter, 1, 2, 1, 1)

        self.label_selection_mode = QLabel(self.frame_5)
        self.label_selection_mode.setObjectName(u"label_selection_mode")
        self.label_selection_mode.setMinimumSize(QSize(120, 30))
        self.label_selection_mode.setMaximumSize(QSize(120, 30))
        self.label_selection_mode.setFont(font)
        self.label_selection_mode.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_selection_mode, 3, 1, 1, 1)

        self.label_selector_filter = QLabel(self.frame_5)
        self.label_selector_filter.setObjectName(u"label_selector_filter")
        self.label_selector_filter.setMinimumSize(QSize(120, 30))
        self.label_selector_filter.setMaximumSize(QSize(120, 30))
        self.label_selector_filter.setFont(font)
        self.label_selector_filter.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_selector_filter, 1, 1, 1, 1)

        self.comboBox_domain_filter = QComboBox(self.frame_5)
        self.comboBox_domain_filter.addItem("")
        self.comboBox_domain_filter.addItem("")
        self.comboBox_domain_filter.addItem("")
        self.comboBox_domain_filter.setObjectName(u"comboBox_domain_filter")
        self.comboBox_domain_filter.setMinimumSize(QSize(120, 30))
        self.comboBox_domain_filter.setMaximumSize(QSize(120, 30))
        self.comboBox_domain_filter.setFont(font)
        self.comboBox_domain_filter.setStyleSheet(u"")

        self.gridLayout_6.addWidget(self.comboBox_domain_filter, 2, 2, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_4, 3, 4, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_3, 3, 0, 1, 1)

        self.pushButton_invert_selection = QPushButton(self.frame_5)
        self.pushButton_invert_selection.setObjectName(u"pushButton_invert_selection")
        self.pushButton_invert_selection.setMinimumSize(QSize(40, 30))
        self.pushButton_invert_selection.setMaximumSize(QSize(40, 30))
        self.pushButton_invert_selection.setFont(font2)
        self.pushButton_invert_selection.setStyleSheet(u"")
        icon1 = Icon(u":/icons/invert_icon.png")
        self.pushButton_invert_selection.setIcon(icon1)
        self.pushButton_invert_selection.setIconSize(QSize(22, 22))
        self.pushButton_invert_selection.setAutoDefault(False)
        self.pushButton_invert_selection.setFlat(False)

        self.gridLayout_6.addWidget(self.pushButton_invert_selection, 1, 3, 1, 1)


        self.gridLayout_5.addWidget(self.frame_5, 0, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_main, "")
        self.tab_list = QWidget()
        self.tab_list.setObjectName(u"tab_list")
        self.gridLayout_7 = QGridLayout(self.tab_list)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.treeWidget_group_info = QTreeWidget(self.tab_list)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(3, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(2, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter);
        self.treeWidget_group_info.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_group_info.setObjectName(u"treeWidget_group_info")
        font3 = QFont()
        font3.setPointSize(9)
        self.treeWidget_group_info.setFont(font3)
        self.treeWidget_group_info.setIndentation(0)

        self.gridLayout_7.addWidget(self.treeWidget_group_info, 0, 0, 1, 1)

        self.frame_reset_remove_buttons = QFrame(self.tab_list)
        self.frame_reset_remove_buttons.setObjectName(u"frame_reset_remove_buttons")
        self.frame_reset_remove_buttons.setMinimumSize(QSize(320, 40))
        self.frame_reset_remove_buttons.setMaximumSize(QSize(16777215, 40))
        self.frame_reset_remove_buttons.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_reset_remove_buttons.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_8 = QGridLayout(self.frame_reset_remove_buttons)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setHorizontalSpacing(12)
        self.gridLayout_8.setContentsMargins(4, 4, 4, 4)
        self.pushButton_reset = QPushButton(self.frame_reset_remove_buttons)
        self.pushButton_reset.setObjectName(u"pushButton_reset")
        self.pushButton_reset.setMinimumSize(QSize(100, 28))
        self.pushButton_reset.setMaximumSize(QSize(100, 28))
        self.pushButton_reset.setFont(font1)
        self.pushButton_reset.setStyleSheet(u"")
        self.pushButton_reset.setAutoDefault(False)

        self.gridLayout_8.addWidget(self.pushButton_reset, 0, 0, 1, 1)

        self.pushButton_remove = QPushButton(self.frame_reset_remove_buttons)
        self.pushButton_remove.setObjectName(u"pushButton_remove")
        self.pushButton_remove.setMinimumSize(QSize(100, 28))
        self.pushButton_remove.setMaximumSize(QSize(100, 28))
        self.pushButton_remove.setFont(font1)
        self.pushButton_remove.setStyleSheet(u"")
        self.pushButton_remove.setAutoDefault(False)

        self.gridLayout_8.addWidget(self.pushButton_remove, 0, 1, 1, 1)


        self.gridLayout_7.addWidget(self.frame_reset_remove_buttons, 1, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_list, "")

        self.gridLayout_3.addWidget(self.tabWidget_main, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_2, 1, 0, 1, 1)

        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 48))
        self.frame.setMaximumSize(QSize(16777215, 48))
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
        font4 = QFont()
        font4.setFamilies([u"Segoe UI"])
        font4.setPointSize(10)
        font4.setBold(False)
        font4.setItalic(False)
        self.label.setFont(font4)
        self.label.setTextFormat(Qt.TextFormat.AutoText)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

        self.frame_apply_buttons = QFrame(Dialog)
        self.frame_apply_buttons.setObjectName(u"frame_apply_buttons")
        self.frame_apply_buttons.setMinimumSize(QSize(0, 48))
        self.frame_apply_buttons.setMaximumSize(QSize(16777215, 48))
        self.frame_apply_buttons.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_apply_buttons.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_11 = QGridLayout(self.frame_apply_buttons)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setVerticalSpacing(0)
        self.gridLayout_11.setContentsMargins(6, 0, 6, 0)
        self.pushButton_apply_and_close = QPushButton(self.frame_apply_buttons)
        self.pushButton_apply_and_close.setObjectName(u"pushButton_apply_and_close")
        self.pushButton_apply_and_close.setMinimumSize(QSize(72, 30))
        self.pushButton_apply_and_close.setMaximumSize(QSize(72, 30))
        font5 = QFont()
        font5.setPointSize(10)
        font5.setBold(False)
        font5.setItalic(False)
        self.pushButton_apply_and_close.setFont(font5)
        self.pushButton_apply_and_close.setStyleSheet(u"")
        self.pushButton_apply_and_close.setAutoDefault(False)
        self.pushButton_apply_and_close.setFlat(False)

        self.gridLayout_11.addWidget(self.pushButton_apply_and_close, 0, 3, 1, 1)

        self.pushButton_apply = QPushButton(self.frame_apply_buttons)
        self.pushButton_apply.setObjectName(u"pushButton_apply")
        self.pushButton_apply.setMinimumSize(QSize(72, 30))
        self.pushButton_apply.setMaximumSize(QSize(72, 30))
        self.pushButton_apply.setFont(font5)
        self.pushButton_apply.setStyleSheet(u"")
        self.pushButton_apply.setAutoDefault(False)
        self.pushButton_apply.setFlat(False)

        self.gridLayout_11.addWidget(self.pushButton_apply, 0, 2, 1, 1)

        self.pushButton_cancel = QPushButton(self.frame_apply_buttons)
        self.pushButton_cancel.setObjectName(u"pushButton_cancel")
        self.pushButton_cancel.setMinimumSize(QSize(72, 30))
        self.pushButton_cancel.setMaximumSize(QSize(72, 30))
        self.pushButton_cancel.setFont(font5)
        self.pushButton_cancel.setStyleSheet(u"")
        self.pushButton_cancel.setAutoDefault(False)
        self.pushButton_cancel.setFlat(False)

        self.gridLayout_11.addWidget(self.pushButton_cancel, 0, 0, 1, 1)

        self.horizontalSpacer_17 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_11.addItem(self.horizontalSpacer_17, 0, 1, 1, 1)


        self.gridLayout.addWidget(self.frame_apply_buttons, 2, 0, 1, 1)


        self.retranslateUi(Dialog)

        self.tabWidget_main.setCurrentIndex(0)
        self.comboBox_selection_mode.setCurrentIndex(0)
        self.comboBox_selector_filter.setCurrentIndex(0)
        self.comboBox_domain_filter.setCurrentIndex(0)
        self.pushButton_apply_and_close.setDefault(False)
        self.pushButton_apply.setDefault(False)
        self.pushButton_cancel.setDefault(False)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Grouping assistant", None))
        self.lineEdit_selected_ids.setText("")
        self.label_selected_ids.setText(QCoreApplication.translate("Dialog", u"Selected IDs: ", None))
        self.label_10.setText(QCoreApplication.translate("Dialog", u"Group label: ", None))
        self.lineEdit_group_label.setText("")
        self.label_domain_filter.setText(QCoreApplication.translate("Dialog", u"Domain filter: ", None))
        self.comboBox_selection_mode.setItemText(0, QCoreApplication.translate("Dialog", u"Manual", None))
        self.comboBox_selection_mode.setItemText(1, QCoreApplication.translate("Dialog", u"Select all", None))
        self.comboBox_selection_mode.setItemText(2, QCoreApplication.translate("Dialog", u"Select by size", None))

#if QT_CONFIG(tooltip)
        self.pushButton_select.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:10pt; font-weight:400;\">Process the entities selection.</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_select.setText("")
        self.comboBox_selector_filter.setItemText(0, QCoreApplication.translate("Dialog", u"Volumes", None))
        self.comboBox_selector_filter.setItemText(1, QCoreApplication.translate("Dialog", u"Surfaces", None))
        self.comboBox_selector_filter.setItemText(2, QCoreApplication.translate("Dialog", u"Lines", None))

        self.label_selection_mode.setText(QCoreApplication.translate("Dialog", u"Selection mode: ", None))
        self.label_selector_filter.setText(QCoreApplication.translate("Dialog", u"Selector filter: ", None))
        self.comboBox_domain_filter.setItemText(0, QCoreApplication.translate("Dialog", u"None", None))
        self.comboBox_domain_filter.setItemText(1, QCoreApplication.translate("Dialog", u"Acoustic", None))
        self.comboBox_domain_filter.setItemText(2, QCoreApplication.translate("Dialog", u"Structural", None))

#if QT_CONFIG(tooltip)
        self.pushButton_invert_selection.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:10pt; font-weight:400;\">Invert entities selection</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_invert_selection.setText("")
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_main), QCoreApplication.translate("Dialog", u"Setup", None))
        ___qtreewidgetitem = self.treeWidget_group_info.headerItem()
        ___qtreewidgetitem.setText(3, QCoreApplication.translate("Dialog", u"Entities ID", None));
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("Dialog", u"Entity type", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"Group Label", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"ID", None));
        self.pushButton_reset.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.pushButton_remove.setText(QCoreApplication.translate("Dialog", u"Remove", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_list), QCoreApplication.translate("Dialog", u"List", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Grouping assistant", None))
        self.pushButton_apply_and_close.setText(QCoreApplication.translate("Dialog", u"Ok", None))
        self.pushButton_apply.setText(QCoreApplication.translate("Dialog", u"Apply", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
    # retranslateUi



class GroupingAssistantInputs_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame_2: QFrame
                    - (Layout): QGridLayout
                            - tabWidget_main: QTabWidget
                                - tab_main: QWidget
                                    - (Layout): QGridLayout
                                            - frame_4: QFrame
                                                - (Layout): QGridLayout
                                                        - lineEdit_selected_ids: QLineEdit
                                                        - label_selected_ids: QLabel
                                                        - label_10: QLabel
                                                        - lineEdit_group_label: QLineEdit
                                            - frame_5: QFrame
                                                - (Layout): QGridLayout
                                                        - label_domain_filter: QLabel
                                                        - comboBox_selection_mode: QComboBox
                                                        - pushButton_select: QPushButton
                                                        - comboBox_selector_filter: QComboBox
                                                        - label_selection_mode: QLabel
                                                        - label_selector_filter: QLabel
                                                        - comboBox_domain_filter: QComboBox
                                                        - pushButton_invert_selection: QPushButton
                                - tab_list: QWidget
                                    - (Layout): QGridLayout
                                            - treeWidget_group_info: QTreeWidget
                                            - frame_reset_remove_buttons: QFrame
                                                - (Layout): QGridLayout
                                                        - pushButton_reset: QPushButton
                                                        - pushButton_remove: QPushButton
                - frame: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
                - frame_apply_buttons: QFrame
                    - (Layout): QGridLayout
                            - pushButton_apply_and_close: QPushButton
                            - pushButton_apply: QPushButton
                            - pushButton_cancel: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
