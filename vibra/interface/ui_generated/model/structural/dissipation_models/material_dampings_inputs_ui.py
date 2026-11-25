# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'material_dampings_inputs.ui'
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
        Dialog.resize(520, 400)
        Dialog.setMinimumSize(QSize(520, 400))
        Dialog.setMaximumSize(QSize(520, 400))
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 48))
        self.frame.setMaximumSize(QSize(16777215, 48))
        self.frame.setFrameShape(QFrame.Shape.Box)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

        self.frame_2 = QFrame(Dialog)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(380, 280))
        self.frame_2.setMaximumSize(QSize(16777215, 480))
        self.frame_2.setFrameShape(QFrame.Shape.Box)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.tabWidget_main = QTabWidget(self.frame_2)
        self.tabWidget_main.setObjectName(u"tabWidget_main")
        self.tabWidget_main.setMinimumSize(QSize(360, 0))
        self.tabWidget_main.setMaximumSize(QSize(16777215, 16777215))
        font1 = QFont()
        font1.setPointSize(10)
        self.tabWidget_main.setFont(font1)
        self.tab_main = QWidget()
        self.tab_main.setObjectName(u"tab_main")
        self.gridLayout_12 = QGridLayout(self.tab_main)
        self.gridLayout_12.setSpacing(2)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setContentsMargins(2, 4, 2, 4)
        self.frame_dampings = QFrame(self.tab_main)
        self.frame_dampings.setObjectName(u"frame_dampings")
        self.frame_dampings.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_dampings.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_7 = QGridLayout(self.frame_dampings)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(4, 4, 4, 4)
        self.label_16 = QLabel(self.frame_dampings)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setMinimumSize(QSize(0, 26))
        self.label_16.setMaximumSize(QSize(16777215, 26))
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        self.label_16.setFont(font2)
        self.label_16.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_7.addWidget(self.label_16, 2, 4, 1, 1)

        self.lineEdit_constant_structural_coefficient = QLineEdit(self.frame_dampings)
        self.lineEdit_constant_structural_coefficient.setObjectName(u"lineEdit_constant_structural_coefficient")
        self.lineEdit_constant_structural_coefficient.setMinimumSize(QSize(80, 26))
        self.lineEdit_constant_structural_coefficient.setMaximumSize(QSize(100, 26))
        self.lineEdit_constant_structural_coefficient.setFont(font2)
        self.lineEdit_constant_structural_coefficient.setStyleSheet(u"")
        self.lineEdit_constant_structural_coefficient.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_7.addWidget(self.lineEdit_constant_structural_coefficient, 2, 3, 1, 1)

        self.label_9 = QLabel(self.frame_dampings)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMinimumSize(QSize(132, 0))
        self.label_9.setFont(font2)
        self.label_9.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_9.setWordWrap(True)

        self.gridLayout_7.addWidget(self.label_9, 2, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer, 0, 5, 1, 1)

        self.lineEdit_stiffness_multiplier = QLineEdit(self.frame_dampings)
        self.lineEdit_stiffness_multiplier.setObjectName(u"lineEdit_stiffness_multiplier")
        self.lineEdit_stiffness_multiplier.setMinimumSize(QSize(80, 26))
        self.lineEdit_stiffness_multiplier.setMaximumSize(QSize(100, 26))
        self.lineEdit_stiffness_multiplier.setFont(font2)
        self.lineEdit_stiffness_multiplier.setStyleSheet(u"")
        self.lineEdit_stiffness_multiplier.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_7.addWidget(self.lineEdit_stiffness_multiplier, 1, 3, 1, 1)

        self.label_10 = QLabel(self.frame_dampings)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(132, 0))
        self.label_10.setFont(font2)
        self.label_10.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_10.setWordWrap(True)

        self.gridLayout_7.addWidget(self.label_10, 1, 1, 1, 1)

        self.label_11 = QLabel(self.frame_dampings)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMinimumSize(QSize(20, 26))
        self.label_11.setMaximumSize(QSize(40, 26))
        font3 = QFont()
        font3.setFamilies([u"Arial"])
        font3.setPointSize(11)
        font3.setBold(False)
        font3.setItalic(False)
        self.label_11.setFont(font3)
        self.label_11.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_11, 1, 2, 1, 1)

        self.label_14 = QLabel(self.frame_dampings)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setMinimumSize(QSize(0, 26))
        self.label_14.setMaximumSize(QSize(16777215, 26))
        self.label_14.setFont(font2)
        self.label_14.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_7.addWidget(self.label_14, 1, 4, 1, 1)

        self.lineEdit_mass_multiplier = QLineEdit(self.frame_dampings)
        self.lineEdit_mass_multiplier.setObjectName(u"lineEdit_mass_multiplier")
        self.lineEdit_mass_multiplier.setMinimumSize(QSize(80, 26))
        self.lineEdit_mass_multiplier.setMaximumSize(QSize(100, 26))
        self.lineEdit_mass_multiplier.setFont(font2)
        self.lineEdit_mass_multiplier.setStyleSheet(u"")
        self.lineEdit_mass_multiplier.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_7.addWidget(self.lineEdit_mass_multiplier, 0, 3, 1, 1)

        self.label_12 = QLabel(self.frame_dampings)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setMinimumSize(QSize(20, 26))
        self.label_12.setMaximumSize(QSize(40, 26))
        self.label_12.setFont(font3)
        self.label_12.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_12, 0, 2, 1, 1)

        self.label_17 = QLabel(self.frame_dampings)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setMinimumSize(QSize(132, 0))
        self.label_17.setFont(font2)
        self.label_17.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_17.setWordWrap(True)

        self.gridLayout_7.addWidget(self.label_17, 0, 1, 1, 1)

        self.label_15 = QLabel(self.frame_dampings)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setMinimumSize(QSize(0, 26))
        self.label_15.setMaximumSize(QSize(16777215, 26))
        self.label_15.setFont(font2)
        self.label_15.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_7.addWidget(self.label_15, 0, 4, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_2, 0, 0, 1, 1)

        self.label_13 = QLabel(self.frame_dampings)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setMinimumSize(QSize(20, 26))
        self.label_13.setMaximumSize(QSize(40, 26))
        self.label_13.setFont(font3)
        self.label_13.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_13, 2, 2, 1, 1)

        self.label_12.raise_()
        self.label_16.raise_()
        self.lineEdit_constant_structural_coefficient.raise_()
        self.label_9.raise_()
        self.lineEdit_stiffness_multiplier.raise_()
        self.label_10.raise_()
        self.label_11.raise_()
        self.label_14.raise_()
        self.lineEdit_mass_multiplier.raise_()
        self.label_17.raise_()
        self.label_15.raise_()
        self.label_13.raise_()

        self.gridLayout_12.addWidget(self.frame_dampings, 0, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_main, "")
        self.tab_list = QWidget()
        self.tab_list.setObjectName(u"tab_list")
        self.gridLayout_6 = QGridLayout(self.tab_list)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.treeWidget_material_dampings = QTreeWidget(self.tab_list)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter);
        self.treeWidget_material_dampings.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_material_dampings.setObjectName(u"treeWidget_material_dampings")
        self.treeWidget_material_dampings.setMinimumSize(QSize(320, 100))
        self.treeWidget_material_dampings.setMaximumSize(QSize(16777215, 200))
        font4 = QFont()
        font4.setFamilies([u"MS Shell Dlg 2"])
        font4.setPointSize(10)
        font4.setItalic(False)
        self.treeWidget_material_dampings.setFont(font4)
        self.treeWidget_material_dampings.setIndentation(1)
        self.treeWidget_material_dampings.setHeaderHidden(False)
        self.treeWidget_material_dampings.header().setHighlightSections(False)
        self.treeWidget_material_dampings.header().setProperty(u"showSortIndicator", False)
        self.treeWidget_material_dampings.header().setStretchLastSection(True)

        self.gridLayout_6.addWidget(self.treeWidget_material_dampings, 0, 0, 1, 1)

        self.frame_3 = QFrame(self.tab_list)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(320, 40))
        self.frame_3.setMaximumSize(QSize(16777215, 40))
        self.frame_3.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_8 = QGridLayout(self.frame_3)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setHorizontalSpacing(12)
        self.gridLayout_8.setContentsMargins(4, 4, 4, 4)
        self.pushButton_reset = QPushButton(self.frame_3)
        self.pushButton_reset.setObjectName(u"pushButton_reset")
        self.pushButton_reset.setMinimumSize(QSize(100, 28))
        self.pushButton_reset.setMaximumSize(QSize(100, 28))
        self.pushButton_reset.setFont(font2)
        self.pushButton_reset.setStyleSheet(u"")
        self.pushButton_reset.setAutoDefault(False)

        self.gridLayout_8.addWidget(self.pushButton_reset, 0, 0, 1, 1)

        self.pushButton_remove = QPushButton(self.frame_3)
        self.pushButton_remove.setObjectName(u"pushButton_remove")
        self.pushButton_remove.setMinimumSize(QSize(100, 28))
        self.pushButton_remove.setMaximumSize(QSize(100, 28))
        self.pushButton_remove.setFont(font2)
        self.pushButton_remove.setStyleSheet(u"")
        self.pushButton_remove.setAutoDefault(False)

        self.gridLayout_8.addWidget(self.pushButton_remove, 0, 1, 1, 1)


        self.gridLayout_6.addWidget(self.frame_3, 1, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_list, "")

        self.gridLayout_4.addWidget(self.tabWidget_main, 1, 0, 1, 1)

        self.frame_4 = QFrame(self.frame_2)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(400, 40))
        self.frame_4.setMaximumSize(QSize(16777215, 40))
        self.frame_4.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_4.setLineWidth(1)
        self.gridLayout_5 = QGridLayout(self.frame_4)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(6, 2, 6, 2)
        self.label_2 = QLabel(self.frame_4)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(0, 30))
        self.label_2.setMaximumSize(QSize(120, 30))
        font5 = QFont()
        font5.setFamilies([u"MS Shell Dlg 2"])
        font5.setPointSize(10)
        font5.setBold(False)
        self.label_2.setFont(font5)
        self.label_2.setTextFormat(Qt.TextFormat.AutoText)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_2, 0, 1, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_4, 0, 0, 1, 1)

        self.lineEdit_selection_id = QLineEdit(self.frame_4)
        self.lineEdit_selection_id.setObjectName(u"lineEdit_selection_id")
        self.lineEdit_selection_id.setEnabled(True)
        self.lineEdit_selection_id.setMinimumSize(QSize(160, 28))
        self.lineEdit_selection_id.setMaximumSize(QSize(160, 28))
        self.lineEdit_selection_id.setFont(font1)
        self.lineEdit_selection_id.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.lineEdit_selection_id.setStyleSheet(u"")
        self.lineEdit_selection_id.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.lineEdit_selection_id, 0, 2, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_3, 0, 5, 1, 1)

        self.comboBox_attribution_type = QComboBox(self.frame_4)
        self.comboBox_attribution_type.addItem("")
        self.comboBox_attribution_type.addItem("")
        self.comboBox_attribution_type.setObjectName(u"comboBox_attribution_type")
        self.comboBox_attribution_type.setMinimumSize(QSize(0, 30))
        self.comboBox_attribution_type.setMaximumSize(QSize(16777215, 30))
        self.comboBox_attribution_type.setFont(font1)

        self.gridLayout_5.addWidget(self.comboBox_attribution_type, 0, 3, 1, 1)

        self.pushButton_select_group = QPushButton(self.frame_4)
        self.pushButton_select_group.setObjectName(u"pushButton_select_group")
        self.pushButton_select_group.setMinimumSize(QSize(40, 30))
        self.pushButton_select_group.setMaximumSize(QSize(40, 30))
        font6 = QFont()
        font6.setFamilies([u"MS Shell Dlg 2"])
        font6.setPointSize(11)
        font6.setBold(True)
        font6.setItalic(False)
        self.pushButton_select_group.setFont(font6)
        self.pushButton_select_group.setStyleSheet(u"")
        icon = Icon(u":/icons/selection_icon.png")
        self.pushButton_select_group.setIcon(icon)
        self.pushButton_select_group.setIconSize(QSize(20, 20))
        self.pushButton_select_group.setAutoDefault(False)
        self.pushButton_select_group.setFlat(False)

        self.gridLayout_5.addWidget(self.pushButton_select_group, 0, 4, 1, 1)


        self.gridLayout_4.addWidget(self.frame_4, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_2, 1, 0, 1, 1)

        self.frame_buttons = QFrame(Dialog)
        self.frame_buttons.setObjectName(u"frame_buttons")
        self.frame_buttons.setMinimumSize(QSize(0, 48))
        self.frame_buttons.setMaximumSize(QSize(16777215, 48))
        self.frame_buttons.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_buttons.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_11 = QGridLayout(self.frame_buttons)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setVerticalSpacing(0)
        self.gridLayout_11.setContentsMargins(6, 0, 6, 0)
        self.pushButton_apply_and_close = QPushButton(self.frame_buttons)
        self.pushButton_apply_and_close.setObjectName(u"pushButton_apply_and_close")
        self.pushButton_apply_and_close.setMinimumSize(QSize(72, 30))
        self.pushButton_apply_and_close.setMaximumSize(QSize(72, 30))
        font7 = QFont()
        font7.setPointSize(10)
        font7.setBold(False)
        font7.setItalic(False)
        self.pushButton_apply_and_close.setFont(font7)
        self.pushButton_apply_and_close.setStyleSheet(u"")
        self.pushButton_apply_and_close.setAutoDefault(False)
        self.pushButton_apply_and_close.setFlat(False)

        self.gridLayout_11.addWidget(self.pushButton_apply_and_close, 0, 3, 1, 1)

        self.pushButton_apply = QPushButton(self.frame_buttons)
        self.pushButton_apply.setObjectName(u"pushButton_apply")
        self.pushButton_apply.setMinimumSize(QSize(72, 30))
        self.pushButton_apply.setMaximumSize(QSize(72, 30))
        self.pushButton_apply.setFont(font7)
        self.pushButton_apply.setStyleSheet(u"")
        self.pushButton_apply.setAutoDefault(False)
        self.pushButton_apply.setFlat(False)

        self.gridLayout_11.addWidget(self.pushButton_apply, 0, 2, 1, 1)

        self.pushButton_cancel = QPushButton(self.frame_buttons)
        self.pushButton_cancel.setObjectName(u"pushButton_cancel")
        self.pushButton_cancel.setMinimumSize(QSize(72, 30))
        self.pushButton_cancel.setMaximumSize(QSize(72, 30))
        self.pushButton_cancel.setFont(font7)
        self.pushButton_cancel.setStyleSheet(u"")
        self.pushButton_cancel.setAutoDefault(False)
        self.pushButton_cancel.setFlat(False)

        self.gridLayout_11.addWidget(self.pushButton_cancel, 0, 0, 1, 1)

        self.horizontalSpacer_17 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_11.addItem(self.horizontalSpacer_17, 0, 1, 1, 1)


        self.gridLayout.addWidget(self.frame_buttons, 2, 0, 1, 1)


        self.retranslateUi(Dialog)

        self.tabWidget_main.setCurrentIndex(0)
        self.pushButton_apply_and_close.setDefault(False)
        self.pushButton_apply.setDefault(False)
        self.pushButton_cancel.setDefault(False)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Set material dampings", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Set material dampings", None))
        self.label_16.setText(QCoreApplication.translate("Dialog", u"[--]", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", u"Constant structural damping coefficient", None))
        self.label_10.setText(QCoreApplication.translate("Dialog", u"Stiffness matrix multiplier", None))
        self.label_11.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">\u03b2:</p></body></html>", None))
        self.label_14.setText(QCoreApplication.translate("Dialog", u"[s]", None))
        self.label_12.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">\u03b1:</p></body></html>", None))
        self.label_17.setText(QCoreApplication.translate("Dialog", u"Mass matrix multiplier", None))
        self.label_15.setText(QCoreApplication.translate("Dialog", u"[1/s]", None))
        self.label_13.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">\u03b7:</p></body></html>", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_main), QCoreApplication.translate("Dialog", u"Setup", None))
        ___qtreewidgetitem = self.treeWidget_material_dampings.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"Damping constants (\u03b1, \u03b2, \u03b7)", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Volumes", None));
        self.pushButton_reset.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.pushButton_remove.setText(QCoreApplication.translate("Dialog", u"Remove", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_list), QCoreApplication.translate("Dialog", u"List", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Selected IDs:", None))
        self.lineEdit_selection_id.setText("")
        self.comboBox_attribution_type.setItemText(0, QCoreApplication.translate("Dialog", u"All bodies", None))
        self.comboBox_attribution_type.setItemText(1, QCoreApplication.translate("Dialog", u"Selected bodies", None))

#if QT_CONFIG(tooltip)
        self.pushButton_select_group.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:10pt; font-weight:400;\">Show the created groups</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_select_group.setText("")
        self.pushButton_apply_and_close.setText(QCoreApplication.translate("Dialog", u"Ok", None))
        self.pushButton_apply.setText(QCoreApplication.translate("Dialog", u"Apply", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
    # retranslateUi



class MaterialDampingsInputs_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
                - frame_2: QFrame
                    - (Layout): QGridLayout
                            - tabWidget_main: QTabWidget
                                - tab_main: QWidget
                                    - (Layout): QGridLayout
                                            - frame_dampings: QFrame
                                                - (Layout): QGridLayout
                                                        - label_16: QLabel
                                                        - lineEdit_constant_structural_coefficient: QLineEdit
                                                        - label_9: QLabel
                                                        - lineEdit_stiffness_multiplier: QLineEdit
                                                        - label_10: QLabel
                                                        - label_11: QLabel
                                                        - label_14: QLabel
                                                        - lineEdit_mass_multiplier: QLineEdit
                                                        - label_12: QLabel
                                                        - label_17: QLabel
                                                        - label_15: QLabel
                                                        - label_13: QLabel
                                - tab_list: QWidget
                                    - (Layout): QGridLayout
                                            - treeWidget_material_dampings: QTreeWidget
                                            - frame_3: QFrame
                                                - (Layout): QGridLayout
                                                        - pushButton_reset: QPushButton
                                                        - pushButton_remove: QPushButton
                            - frame_4: QFrame
                                - (Layout): QGridLayout
                                        - label_2: QLabel
                                        - lineEdit_selection_id: QLineEdit
                                        - comboBox_attribution_type: QComboBox
                                        - pushButton_select_group: QPushButton
                - frame_buttons: QFrame
                    - (Layout): QGridLayout
                            - pushButton_apply_and_close: QPushButton
                            - pushButton_apply: QPushButton
                            - pushButton_cancel: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
