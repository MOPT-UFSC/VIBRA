# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dof_constraint_inputs.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
    QFrame, QGridLayout, QHeaderView, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QTabWidget, QTreeWidget, QTreeWidgetItem, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setWindowModality(Qt.WindowModal)
        Dialog.resize(460, 460)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(460, 460))
        Dialog.setMaximumSize(QSize(460, 540))
        font = QFont()
        font.setPointSize(11)
        font.setBold(False)
        Dialog.setFont(font)
        Dialog.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.gridLayout_7 = QGridLayout(Dialog)
        self.gridLayout_7.setSpacing(4)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(4, 4, 4, 4)
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(380, 48))
        self.frame.setMaximumSize(QSize(16777215, 48))
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setLineWidth(1)
        self.gridLayout_6 = QGridLayout(self.frame)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        font1 = QFont()
        font1.setFamilies([u"MS Shell Dlg 2"])
        font1.setPointSize(11)
        font1.setBold(False)
        font1.setItalic(False)
        self.label.setFont(font1)
        self.label.setTextFormat(Qt.AutoText)
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout_6.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout_7.addWidget(self.frame, 0, 0, 1, 1)

        self.frame_2 = QFrame(Dialog)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(380, 0))
        self.frame_2.setMaximumSize(QSize(16777215, 480))
        self.frame_2.setFrameShape(QFrame.Box)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_2)
        self.gridLayout_4.setSpacing(2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(2, 4, 2, 2)
        self.frame_4 = QFrame(self.frame_2)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(360, 72))
        self.frame_4.setMaximumSize(QSize(16777215, 72))
        self.frame_4.setFrameShape(QFrame.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_4)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setHorizontalSpacing(6)
        self.gridLayout_5.setVerticalSpacing(2)
        self.gridLayout_5.setContentsMargins(2, 2, 2, 2)
        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_6, 0, 0, 1, 1)

        self.lineEdit_selection_id = QLineEdit(self.frame_4)
        self.lineEdit_selection_id.setObjectName(u"lineEdit_selection_id")
        self.lineEdit_selection_id.setMinimumSize(QSize(120, 28))
        self.lineEdit_selection_id.setMaximumSize(QSize(140, 28))
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        self.lineEdit_selection_id.setFont(font2)
        self.lineEdit_selection_id.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_selection_id.setStyleSheet(u"")
        self.lineEdit_selection_id.setAlignment(Qt.AlignCenter)

        self.gridLayout_5.addWidget(self.lineEdit_selection_id, 0, 2, 1, 1)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_9, 0, 4, 1, 1)

        self.label_2 = QLabel(self.frame_4)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(100, 28))
        self.label_2.setMaximumSize(QSize(100, 28))
        self.label_2.setFont(font2)
        self.label_2.setAlignment(Qt.AlignCenter)

        self.gridLayout_5.addWidget(self.label_2, 0, 1, 1, 1)

        self.label_3 = QLabel(self.frame_4)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(100, 28))
        self.label_3.setMaximumSize(QSize(100, 28))
        self.label_3.setFont(font2)
        self.label_3.setAlignment(Qt.AlignCenter)

        self.gridLayout_5.addWidget(self.label_3, 1, 1, 1, 1)

        self.comboBox_element_type = QComboBox(self.frame_4)
        self.comboBox_element_type.addItem("")
        self.comboBox_element_type.addItem("")
        self.comboBox_element_type.setObjectName(u"comboBox_element_type")
        self.comboBox_element_type.setMinimumSize(QSize(120, 28))
        self.comboBox_element_type.setMaximumSize(QSize(140, 28))
        font3 = QFont()
        font3.setPointSize(10)
        self.comboBox_element_type.setFont(font3)

        self.gridLayout_5.addWidget(self.comboBox_element_type, 1, 2, 1, 1)

        self.comboBox_attribution_type = QComboBox(self.frame_4)
        self.comboBox_attribution_type.addItem("")
        self.comboBox_attribution_type.addItem("")
        self.comboBox_attribution_type.addItem("")
        self.comboBox_attribution_type.addItem("")
        self.comboBox_attribution_type.setObjectName(u"comboBox_attribution_type")
        self.comboBox_attribution_type.setMinimumSize(QSize(0, 28))
        self.comboBox_attribution_type.setMaximumSize(QSize(16777215, 28))
        self.comboBox_attribution_type.setFont(font3)

        self.gridLayout_5.addWidget(self.comboBox_attribution_type, 0, 3, 1, 1)


        self.gridLayout_4.addWidget(self.frame_4, 0, 0, 1, 1)

        self.frame_6 = QFrame(self.frame_2)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.NoFrame)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.gridLayout_13 = QGridLayout(self.frame_6)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_13.setContentsMargins(4, 4, 4, 8)
        self.tabWidget_main = QTabWidget(self.frame_6)
        self.tabWidget_main.setObjectName(u"tabWidget_main")
        self.tabWidget_main.setMinimumSize(QSize(360, 0))
        self.tabWidget_main.setMaximumSize(QSize(420, 16777215))
        self.tabWidget_main.setFont(font3)
        self.tab_constant_data = QWidget()
        self.tab_constant_data.setObjectName(u"tab_constant_data")
        self.gridLayout_12 = QGridLayout(self.tab_constant_data)
        self.gridLayout_12.setSpacing(2)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setContentsMargins(2, 2, 2, 2)
        self.frame_9 = QFrame(self.tab_constant_data)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setMinimumSize(QSize(0, 48))
        self.frame_9.setMaximumSize(QSize(16777215, 48))
        self.frame_9.setFrameShape(QFrame.NoFrame)
        self.frame_9.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_9)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.pushButton_fixed_support = QPushButton(self.frame_9)
        self.pushButton_fixed_support.setObjectName(u"pushButton_fixed_support")
        self.pushButton_fixed_support.setMinimumSize(QSize(100, 28))
        self.pushButton_fixed_support.setMaximumSize(QSize(120, 28))
        self.pushButton_fixed_support.setFont(font3)
        self.pushButton_fixed_support.setStyleSheet(u"")
        self.pushButton_fixed_support.setAutoDefault(False)

        self.gridLayout_3.addWidget(self.pushButton_fixed_support, 0, 0, 1, 1)


        self.gridLayout_12.addWidget(self.frame_9, 1, 0, 1, 1)

        self.frame_8 = QFrame(self.tab_constant_data)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setMinimumSize(QSize(340, 120))
        self.frame_8.setMaximumSize(QSize(16777215, 140))
        font4 = QFont()
        font4.setPointSize(11)
        self.frame_8.setFont(font4)
        self.frame_8.setFrameShape(QFrame.NoFrame)
        self.frame_8.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame_8)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(14)
        self.gridLayout.setVerticalSpacing(6)
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 2, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 2, 5, 1, 1)

        self.checkBox_constrain_ux = QCheckBox(self.frame_8)
        self.checkBox_constrain_ux.setObjectName(u"checkBox_constrain_ux")
        self.checkBox_constrain_ux.setMinimumSize(QSize(0, 28))
        self.checkBox_constrain_ux.setMaximumSize(QSize(16777215, 28))
        self.checkBox_constrain_ux.setFont(font3)
        self.checkBox_constrain_ux.setChecked(False)

        self.gridLayout.addWidget(self.checkBox_constrain_ux, 2, 2, 1, 1)

        self.checkBox_constrain_uy = QCheckBox(self.frame_8)
        self.checkBox_constrain_uy.setObjectName(u"checkBox_constrain_uy")
        self.checkBox_constrain_uy.setMinimumSize(QSize(0, 28))
        self.checkBox_constrain_uy.setMaximumSize(QSize(16777215, 28))
        self.checkBox_constrain_uy.setFont(font3)
        self.checkBox_constrain_uy.setChecked(False)

        self.gridLayout.addWidget(self.checkBox_constrain_uy, 3, 2, 1, 1)

        self.checkBox_constrain_uz = QCheckBox(self.frame_8)
        self.checkBox_constrain_uz.setObjectName(u"checkBox_constrain_uz")
        self.checkBox_constrain_uz.setMinimumSize(QSize(0, 28))
        self.checkBox_constrain_uz.setMaximumSize(QSize(16777215, 28))
        self.checkBox_constrain_uz.setFont(font3)
        self.checkBox_constrain_uz.setChecked(False)

        self.gridLayout.addWidget(self.checkBox_constrain_uz, 4, 2, 1, 1)

        self.checkBox_constrain_rz = QCheckBox(self.frame_8)
        self.checkBox_constrain_rz.setObjectName(u"checkBox_constrain_rz")
        self.checkBox_constrain_rz.setMinimumSize(QSize(0, 28))
        self.checkBox_constrain_rz.setMaximumSize(QSize(16777215, 28))
        self.checkBox_constrain_rz.setFont(font3)
        self.checkBox_constrain_rz.setChecked(False)

        self.gridLayout.addWidget(self.checkBox_constrain_rz, 4, 3, 1, 1)

        self.checkBox_constrain_rx = QCheckBox(self.frame_8)
        self.checkBox_constrain_rx.setObjectName(u"checkBox_constrain_rx")
        self.checkBox_constrain_rx.setMinimumSize(QSize(0, 28))
        self.checkBox_constrain_rx.setMaximumSize(QSize(16777215, 28))
        self.checkBox_constrain_rx.setFont(font3)
        self.checkBox_constrain_rx.setChecked(False)

        self.gridLayout.addWidget(self.checkBox_constrain_rx, 2, 3, 1, 1)

        self.checkBox_constrain_ry = QCheckBox(self.frame_8)
        self.checkBox_constrain_ry.setObjectName(u"checkBox_constrain_ry")
        self.checkBox_constrain_ry.setMinimumSize(QSize(0, 28))
        self.checkBox_constrain_ry.setMaximumSize(QSize(16777215, 28))
        self.checkBox_constrain_ry.setFont(font3)
        self.checkBox_constrain_ry.setChecked(False)

        self.gridLayout.addWidget(self.checkBox_constrain_ry, 3, 3, 1, 1)

        self.pushButton_unselect_all = QPushButton(self.frame_8)
        self.pushButton_unselect_all.setObjectName(u"pushButton_unselect_all")
        self.pushButton_unselect_all.setMinimumSize(QSize(40, 28))
        self.pushButton_unselect_all.setMaximumSize(QSize(40, 28))
        self.pushButton_unselect_all.setFont(font3)
        self.pushButton_unselect_all.setStyleSheet(u"")
        icon = QIcon()
        icon.addFile(u":/icons/reset_icon.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_unselect_all.setIcon(icon)
        self.pushButton_unselect_all.setIconSize(QSize(22, 22))
        self.pushButton_unselect_all.setAutoDefault(False)

        self.gridLayout.addWidget(self.pushButton_unselect_all, 2, 4, 1, 1)

        self.frame_10 = QFrame(self.frame_8)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setMinimumSize(QSize(40, 28))
        self.frame_10.setMaximumSize(QSize(40, 28))
        self.frame_10.setFrameShape(QFrame.NoFrame)
        self.frame_10.setFrameShadow(QFrame.Raised)

        self.gridLayout.addWidget(self.frame_10, 2, 1, 1, 1)


        self.gridLayout_12.addWidget(self.frame_8, 0, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_constant_data, "")
        self.tab_list = QWidget()
        self.tab_list.setObjectName(u"tab_list")
        self.gridLayout_9 = QGridLayout(self.tab_list)
        self.gridLayout_9.setSpacing(2)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(2, 2, 2, 2)
        self.frame_5 = QFrame(self.tab_list)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_5)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.treeWidget_prescribed_dofs = QTreeWidget(self.frame_5)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(2, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter);
        self.treeWidget_prescribed_dofs.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_prescribed_dofs.setObjectName(u"treeWidget_prescribed_dofs")
        self.treeWidget_prescribed_dofs.setMinimumSize(QSize(320, 0))
        self.treeWidget_prescribed_dofs.setMaximumSize(QSize(380, 200))
        font5 = QFont()
        font5.setFamilies([u"MS Shell Dlg 2"])
        font5.setPointSize(10)
        font5.setItalic(False)
        self.treeWidget_prescribed_dofs.setFont(font5)
        self.treeWidget_prescribed_dofs.setIndentation(1)
        self.treeWidget_prescribed_dofs.setHeaderHidden(False)
        self.treeWidget_prescribed_dofs.header().setHighlightSections(False)
        self.treeWidget_prescribed_dofs.header().setProperty(u"showSortIndicator", False)
        self.treeWidget_prescribed_dofs.header().setStretchLastSection(True)

        self.gridLayout_2.addWidget(self.treeWidget_prescribed_dofs, 0, 0, 1, 1)


        self.gridLayout_9.addWidget(self.frame_5, 0, 0, 1, 1)

        self.frame_3 = QFrame(self.tab_list)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(320, 48))
        self.frame_3.setMaximumSize(QSize(16777215, 48))
        self.frame_3.setFrameShape(QFrame.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.gridLayout_8 = QGridLayout(self.frame_3)
        self.gridLayout_8.setSpacing(4)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
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


        self.gridLayout_9.addWidget(self.frame_3, 1, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_list, "")

        self.gridLayout_13.addWidget(self.tabWidget_main, 0, 0, 1, 1)


        self.gridLayout_4.addWidget(self.frame_6, 1, 0, 1, 1)


        self.gridLayout_7.addWidget(self.frame_2, 1, 0, 1, 1)

        self.frame_7 = QFrame(Dialog)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setMinimumSize(QSize(340, 48))
        self.frame_7.setMaximumSize(QSize(16777215, 48))
        self.frame_7.setFrameShape(QFrame.NoFrame)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.gridLayout_11 = QGridLayout(self.frame_7)
        self.gridLayout_11.setSpacing(0)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setContentsMargins(0, 0, 0, 0)
        self.pushButton_exit = QPushButton(self.frame_7)
        self.pushButton_exit.setObjectName(u"pushButton_exit")
        self.pushButton_exit.setMinimumSize(QSize(100, 28))
        self.pushButton_exit.setMaximumSize(QSize(100, 28))
        self.pushButton_exit.setFont(font3)
        self.pushButton_exit.setStyleSheet(u"")
        self.pushButton_exit.setAutoDefault(False)

        self.gridLayout_11.addWidget(self.pushButton_exit, 0, 0, 1, 1)

        self.pushButton_attribute = QPushButton(self.frame_7)
        self.pushButton_attribute.setObjectName(u"pushButton_attribute")
        self.pushButton_attribute.setMinimumSize(QSize(100, 28))
        self.pushButton_attribute.setMaximumSize(QSize(100, 28))
        self.pushButton_attribute.setFont(font3)
        self.pushButton_attribute.setStyleSheet(u"")
        self.pushButton_attribute.setAutoDefault(False)

        self.gridLayout_11.addWidget(self.pushButton_attribute, 0, 1, 1, 1)


        self.gridLayout_7.addWidget(self.frame_7, 2, 0, 1, 1)


        self.retranslateUi(Dialog)

        self.tabWidget_main.setCurrentIndex(0)
        self.pushButton_attribute.setDefault(False)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Set a boundary condition", None))
#if QT_CONFIG(whatsthis)
        Dialog.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.label.setText(QCoreApplication.translate("Dialog", u"Degrees of freedom constraint setup", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Selection ID:", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Element type:", None))
        self.comboBox_element_type.setItemText(0, QCoreApplication.translate("Dialog", u" Face element", None))
        self.comboBox_element_type.setItemText(1, QCoreApplication.translate("Dialog", u" Solid element", None))

        self.comboBox_attribution_type.setItemText(0, QCoreApplication.translate("Dialog", u"Selected faces", None))
        self.comboBox_attribution_type.setItemText(1, QCoreApplication.translate("Dialog", u"Selected lines", None))
        self.comboBox_attribution_type.setItemText(2, QCoreApplication.translate("Dialog", u"Selected points", None))
        self.comboBox_attribution_type.setItemText(3, QCoreApplication.translate("Dialog", u"Selected nodes", None))

        self.pushButton_fixed_support.setText(QCoreApplication.translate("Dialog", u"Fixed support", None))
        self.checkBox_constrain_ux.setText(QCoreApplication.translate("Dialog", u"Constrain Ux", None))
        self.checkBox_constrain_uy.setText(QCoreApplication.translate("Dialog", u"Constrain Uy", None))
        self.checkBox_constrain_uz.setText(QCoreApplication.translate("Dialog", u"Constrain Uz", None))
        self.checkBox_constrain_rz.setText(QCoreApplication.translate("Dialog", u"Constrain Rz", None))
        self.checkBox_constrain_rx.setText(QCoreApplication.translate("Dialog", u"Constrain Rx", None))
        self.checkBox_constrain_ry.setText(QCoreApplication.translate("Dialog", u"Constrain Ry", None))
        self.pushButton_unselect_all.setText("")
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_constant_data), QCoreApplication.translate("Dialog", u"Setup", None))
        ___qtreewidgetitem = self.treeWidget_prescribed_dofs.headerItem()
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("Dialog", u"Element type", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"Constrained DOF", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Selection-ID", None));
#if QT_CONFIG(tooltip)
        self.treeWidget_prescribed_dofs.setToolTip(QCoreApplication.translate("Dialog", u"Select a node to remove the attributed boundary condition.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_reset.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.pushButton_remove.setText(QCoreApplication.translate("Dialog", u"Remove", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_list), QCoreApplication.translate("Dialog", u"List", None))
        self.pushButton_exit.setText(QCoreApplication.translate("Dialog", u"Exit", None))
        self.pushButton_attribute.setText(QCoreApplication.translate("Dialog", u"Attribute", None))
    # retranslateUi



class DofConstraintInputs_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
                - frame_2: QFrame
                    - (Layout): QGridLayout
                            - frame_4: QFrame
                                - (Layout): QGridLayout
                                        - lineEdit_selection_id: QLineEdit
                                        - label_2: QLabel
                                        - label_3: QLabel
                                        - comboBox_element_type: QComboBox
                                        - comboBox_attribution_type: QComboBox
                            - frame_6: QFrame
                                - (Layout): QGridLayout
                                        - tabWidget_main: QTabWidget
                                            - tab_constant_data: QWidget
                                                - (Layout): QGridLayout
                                                        - frame_9: QFrame
                                                            - (Layout): QGridLayout
                                                                    - pushButton_fixed_support: QPushButton
                                                        - frame_8: QFrame
                                                            - (Layout): QGridLayout
                                                                    - checkBox_constrain_ux: QCheckBox
                                                                    - checkBox_constrain_uy: QCheckBox
                                                                    - checkBox_constrain_uz: QCheckBox
                                                                    - checkBox_constrain_rz: QCheckBox
                                                                    - checkBox_constrain_rx: QCheckBox
                                                                    - checkBox_constrain_ry: QCheckBox
                                                                    - pushButton_unselect_all: QPushButton
                                                                    - frame_10: QFrame
                                            - tab_list: QWidget
                                                - (Layout): QGridLayout
                                                        - frame_5: QFrame
                                                            - (Layout): QGridLayout
                                                                    - treeWidget_prescribed_dofs: QTreeWidget
                                                        - frame_3: QFrame
                                                            - (Layout): QGridLayout
                                                                    - pushButton_reset: QPushButton
                                                                    - pushButton_remove: QPushButton
                - frame_7: QFrame
                    - (Layout): QGridLayout
                            - pushButton_exit: QPushButton
                            - pushButton_attribute: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
