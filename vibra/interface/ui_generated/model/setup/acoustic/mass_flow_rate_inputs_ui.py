# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mass_flow_rate_inputs.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QFrame,
    QGridLayout, QHeaderView, QLabel, QLineEdit,
    QPushButton, QRadioButton, QSizePolicy, QSpacerItem,
    QTabWidget, QTreeWidget, QTreeWidgetItem, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setWindowModality(Qt.WindowModal)
        Dialog.resize(420, 400)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(420, 400))
        Dialog.setMaximumSize(QSize(420, 400))
        font = QFont()
        font.setPointSize(11)
        font.setBold(False)
        Dialog.setFont(font)
        Dialog.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.gridLayout_7 = QGridLayout(Dialog)
        self.gridLayout_7.setSpacing(4)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(4, 4, 4, 4)
        self.frame_2 = QFrame(Dialog)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(380, 280))
        self.frame_2.setMaximumSize(QSize(420, 480))
        self.frame_2.setFrameShape(QFrame.Box)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.frame_4 = QFrame(self.frame_2)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(360, 40))
        self.frame_4.setMaximumSize(QSize(380, 40))
        self.frame_4.setFrameShape(QFrame.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_4)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setHorizontalSpacing(6)
        self.gridLayout_5.setVerticalSpacing(2)
        self.gridLayout_5.setContentsMargins(2, 2, 2, 2)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.lineEdit_selection_id = QLineEdit(self.frame_4)
        self.lineEdit_selection_id.setObjectName(u"lineEdit_selection_id")
        self.lineEdit_selection_id.setMinimumSize(QSize(120, 28))
        self.lineEdit_selection_id.setMaximumSize(QSize(120, 28))
        font1 = QFont()
        font1.setFamilies([u"MS Shell Dlg 2"])
        font1.setPointSize(10)
        font1.setBold(False)
        font1.setItalic(False)
        self.lineEdit_selection_id.setFont(font1)
        self.lineEdit_selection_id.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_selection_id.setStyleSheet(u"")
        self.lineEdit_selection_id.setAlignment(Qt.AlignCenter)

        self.gridLayout_5.addWidget(self.lineEdit_selection_id, 0, 2, 1, 1)

        self.label_2 = QLabel(self.frame_4)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(100, 28))
        self.label_2.setMaximumSize(QSize(100, 28))
        self.label_2.setFont(font1)
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_2, 0, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_2, 0, 3, 1, 1)


        self.gridLayout_4.addWidget(self.frame_4, 0, 0, 1, 1)

        self.tabWidget_main = QTabWidget(self.frame_2)
        self.tabWidget_main.setObjectName(u"tabWidget_main")
        self.tabWidget_main.setMinimumSize(QSize(360, 0))
        self.tabWidget_main.setMaximumSize(QSize(380, 16777215))
        font2 = QFont()
        font2.setPointSize(10)
        self.tabWidget_main.setFont(font2)
        self.tab_constant_values = QWidget()
        self.tab_constant_values.setObjectName(u"tab_constant_values")
        self.gridLayout_12 = QGridLayout(self.tab_constant_values)
        self.gridLayout_12.setSpacing(2)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setContentsMargins(2, 6, 2, 6)
        self.frame_8 = QFrame(self.tab_constant_values)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setMinimumSize(QSize(340, 80))
        self.frame_8.setMaximumSize(QSize(400, 160))
        self.frame_8.setFont(font2)
        self.frame_8.setFrameShape(QFrame.NoFrame)
        self.frame_8.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame_8)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(0)
        self.gridLayout.setVerticalSpacing(2)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_imag_value = QLineEdit(self.frame_8)
        self.lineEdit_imag_value.setObjectName(u"lineEdit_imag_value")
        self.lineEdit_imag_value.setMinimumSize(QSize(80, 28))
        self.lineEdit_imag_value.setMaximumSize(QSize(80, 28))
        self.lineEdit_imag_value.setFont(font1)
        self.lineEdit_imag_value.setStyleSheet(u"")
        self.lineEdit_imag_value.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_imag_value, 1, 2, 1, 1)

        self.label_21 = QLabel(self.frame_8)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setMinimumSize(QSize(60, 28))
        self.label_21.setMaximumSize(QSize(60, 28))
        self.label_21.setFont(font1)
        self.label_21.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_21, 1, 3, 1, 1)

        self.label_18 = QLabel(self.frame_8)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setMinimumSize(QSize(120, 28))
        self.label_18.setMaximumSize(QSize(120, 28))
        self.label_18.setFont(font1)
        self.label_18.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_18, 1, 0, 1, 1)

        self.label_4 = QLabel(self.frame_8)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(80, 26))
        self.label_4.setMaximumSize(QSize(80, 26))
        self.label_4.setFont(font1)
        self.label_4.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_4, 0, 1, 1, 1)

        self.label_20 = QLabel(self.frame_8)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setMinimumSize(QSize(80, 26))
        self.label_20.setMaximumSize(QSize(80, 26))
        self.label_20.setFont(font1)
        self.label_20.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_20, 0, 2, 1, 1)

        self.lineEdit_real_value = QLineEdit(self.frame_8)
        self.lineEdit_real_value.setObjectName(u"lineEdit_real_value")
        self.lineEdit_real_value.setMinimumSize(QSize(80, 28))
        self.lineEdit_real_value.setMaximumSize(QSize(80, 28))
        self.lineEdit_real_value.setFont(font1)
        self.lineEdit_real_value.setStyleSheet(u"")
        self.lineEdit_real_value.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_real_value, 1, 1, 1, 1)


        self.gridLayout_12.addWidget(self.frame_8, 0, 0, 1, 1)

        self.frame_20 = QFrame(self.tab_constant_values)
        self.frame_20.setObjectName(u"frame_20")
        self.frame_20.setFrameShape(QFrame.NoFrame)
        self.frame_20.setFrameShadow(QFrame.Raised)
        self.gridLayout_10 = QGridLayout(self.frame_20)
        self.gridLayout_10.setSpacing(0)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(0, 0, 0, 0)
        self.checkBox_averaged_constant_values = QCheckBox(self.frame_20)
        self.checkBox_averaged_constant_values.setObjectName(u"checkBox_averaged_constant_values")
        self.checkBox_averaged_constant_values.setMinimumSize(QSize(0, 28))
        self.checkBox_averaged_constant_values.setMaximumSize(QSize(220, 28))
        self.checkBox_averaged_constant_values.setFont(font2)
        self.checkBox_averaged_constant_values.setChecked(True)

        self.gridLayout_10.addWidget(self.checkBox_averaged_constant_values, 0, 0, 1, 1)


        self.gridLayout_12.addWidget(self.frame_20, 2, 0, 1, 1)

        self.frame_24 = QFrame(self.tab_constant_values)
        self.frame_24.setObjectName(u"frame_24")
        self.frame_24.setFrameShape(QFrame.NoFrame)
        self.frame_24.setFrameShadow(QFrame.Raised)
        self.gridLayout_16 = QGridLayout(self.frame_24)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.gridLayout_16.setContentsMargins(0, 0, 0, 0)
        self.radioButton_element_integration_constant = QRadioButton(self.frame_24)
        self.radioButton_element_integration_constant.setObjectName(u"radioButton_element_integration_constant")
        self.radioButton_element_integration_constant.setMinimumSize(QSize(0, 28))
        self.radioButton_element_integration_constant.setMaximumSize(QSize(16777215, 28))
        self.radioButton_element_integration_constant.setFont(font2)

        self.gridLayout_16.addWidget(self.radioButton_element_integration_constant, 0, 3, 1, 1)

        self.radioButton_nodal_attribution_constant = QRadioButton(self.frame_24)
        self.radioButton_nodal_attribution_constant.setObjectName(u"radioButton_nodal_attribution_constant")
        self.radioButton_nodal_attribution_constant.setMinimumSize(QSize(0, 28))
        self.radioButton_nodal_attribution_constant.setMaximumSize(QSize(16777215, 28))
        self.radioButton_nodal_attribution_constant.setFont(font2)
        self.radioButton_nodal_attribution_constant.setChecked(True)

        self.gridLayout_16.addWidget(self.radioButton_nodal_attribution_constant, 0, 1, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_16.addItem(self.horizontalSpacer_3, 0, 0, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_16.addItem(self.horizontalSpacer_4, 0, 2, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_16.addItem(self.horizontalSpacer_5, 0, 4, 1, 1)


        self.gridLayout_12.addWidget(self.frame_24, 1, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_constant_values, "")
        self.tab_load_tables = QWidget()
        self.tab_load_tables.setObjectName(u"tab_load_tables")
        self.gridLayout_3 = QGridLayout(self.tab_load_tables)
        self.gridLayout_3.setSpacing(2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(2, 6, 2, 6)
        self.frame_21 = QFrame(self.tab_load_tables)
        self.frame_21.setObjectName(u"frame_21")
        self.frame_21.setFrameShape(QFrame.NoFrame)
        self.frame_21.setFrameShadow(QFrame.Raised)
        self.gridLayout_17 = QGridLayout(self.frame_21)
        self.gridLayout_17.setSpacing(0)
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.gridLayout_17.setContentsMargins(0, 0, 0, 0)
        self.checkBox_averaged_table_values = QCheckBox(self.frame_21)
        self.checkBox_averaged_table_values.setObjectName(u"checkBox_averaged_table_values")
        self.checkBox_averaged_table_values.setMinimumSize(QSize(0, 28))
        self.checkBox_averaged_table_values.setMaximumSize(QSize(220, 28))
        self.checkBox_averaged_table_values.setFont(font2)
        self.checkBox_averaged_table_values.setChecked(True)

        self.gridLayout_17.addWidget(self.checkBox_averaged_table_values, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_21, 2, 0, 1, 1)

        self.frame_9 = QFrame(self.tab_load_tables)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setMinimumSize(QSize(260, 0))
        self.frame_9.setMaximumSize(QSize(400, 100))
        self.frame_9.setFrameShape(QFrame.NoFrame)
        self.frame_9.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_9)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setHorizontalSpacing(6)
        self.gridLayout_2.setVerticalSpacing(2)
        self.gridLayout_2.setContentsMargins(0, 4, 0, 0)
        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_12, 0, 4, 1, 1)

        self.lineEdit_table_path = QLineEdit(self.frame_9)
        self.lineEdit_table_path.setObjectName(u"lineEdit_table_path")
        self.lineEdit_table_path.setEnabled(True)
        self.lineEdit_table_path.setMinimumSize(QSize(240, 26))
        self.lineEdit_table_path.setMaximumSize(QSize(260, 26))
        font3 = QFont()
        font3.setPointSize(9)
        font3.setBold(False)
        self.lineEdit_table_path.setFont(font3)
        self.lineEdit_table_path.setStyleSheet(u"")
        self.lineEdit_table_path.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_table_path, 0, 1, 1, 1)

        self.pushButton_load_table = QPushButton(self.frame_9)
        self.pushButton_load_table.setObjectName(u"pushButton_load_table")
        self.pushButton_load_table.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton_load_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_table.setSizePolicy(sizePolicy1)
        self.pushButton_load_table.setMinimumSize(QSize(62, 26))
        self.pushButton_load_table.setMaximumSize(QSize(62, 26))
        self.pushButton_load_table.setFont(font1)
        self.pushButton_load_table.setStyleSheet(u"")

        self.gridLayout_2.addWidget(self.pushButton_load_table, 0, 2, 1, 1)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_11, 0, 0, 1, 1)

        self.pushButton_change_frequency_setup = QPushButton(self.frame_9)
        self.pushButton_change_frequency_setup.setObjectName(u"pushButton_change_frequency_setup")
        self.pushButton_change_frequency_setup.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.pushButton_change_frequency_setup.sizePolicy().hasHeightForWidth())
        self.pushButton_change_frequency_setup.setSizePolicy(sizePolicy1)
        self.pushButton_change_frequency_setup.setMinimumSize(QSize(40, 28))
        self.pushButton_change_frequency_setup.setMaximumSize(QSize(40, 28))
        self.pushButton_change_frequency_setup.setFont(font1)
        self.pushButton_change_frequency_setup.setStyleSheet(u"")
        icon = QIcon()
        icon.addFile(u":/icons/recent.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_change_frequency_setup.setIcon(icon)
        self.pushButton_change_frequency_setup.setIconSize(QSize(20, 20))

        self.gridLayout_2.addWidget(self.pushButton_change_frequency_setup, 0, 3, 1, 1)


        self.gridLayout_3.addWidget(self.frame_9, 0, 0, 1, 1)

        self.frame_16 = QFrame(self.tab_load_tables)
        self.frame_16.setObjectName(u"frame_16")
        self.frame_16.setFrameShape(QFrame.NoFrame)
        self.frame_16.setFrameShadow(QFrame.Raised)
        self.gridLayout_15 = QGridLayout(self.frame_16)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.gridLayout_15.setContentsMargins(0, 0, 0, 0)
        self.radioButton_nodal_attribution_table = QRadioButton(self.frame_16)
        self.radioButton_nodal_attribution_table.setObjectName(u"radioButton_nodal_attribution_table")
        self.radioButton_nodal_attribution_table.setMinimumSize(QSize(0, 28))
        self.radioButton_nodal_attribution_table.setMaximumSize(QSize(16777215, 28))
        self.radioButton_nodal_attribution_table.setFont(font2)
        self.radioButton_nodal_attribution_table.setChecked(True)

        self.gridLayout_15.addWidget(self.radioButton_nodal_attribution_table, 0, 1, 1, 1)

        self.radioButton_element_integration_table = QRadioButton(self.frame_16)
        self.radioButton_element_integration_table.setObjectName(u"radioButton_element_integration_table")
        self.radioButton_element_integration_table.setMinimumSize(QSize(0, 28))
        self.radioButton_element_integration_table.setMaximumSize(QSize(16777215, 28))
        self.radioButton_element_integration_table.setFont(font2)

        self.gridLayout_15.addWidget(self.radioButton_element_integration_table, 0, 3, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_15.addItem(self.horizontalSpacer_8, 0, 0, 1, 1)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_15.addItem(self.horizontalSpacer_9, 0, 2, 1, 1)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_15.addItem(self.horizontalSpacer_10, 0, 4, 1, 1)


        self.gridLayout_3.addWidget(self.frame_16, 1, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_load_tables, "")
        self.tab_list = QWidget()
        self.tab_list.setObjectName(u"tab_list")
        self.gridLayout_9 = QGridLayout(self.tab_list)
        self.gridLayout_9.setSpacing(2)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(2, 8, 2, 2)
        self.frame_3 = QFrame(self.tab_list)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(320, 40))
        self.frame_3.setMaximumSize(QSize(320, 40))
        self.frame_3.setFrameShape(QFrame.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.gridLayout_8 = QGridLayout(self.frame_3)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setHorizontalSpacing(12)
        self.gridLayout_8.setContentsMargins(4, 4, 4, 4)
        self.pushButton_reset = QPushButton(self.frame_3)
        self.pushButton_reset.setObjectName(u"pushButton_reset")
        self.pushButton_reset.setMinimumSize(QSize(100, 28))
        self.pushButton_reset.setMaximumSize(QSize(100, 28))
        self.pushButton_reset.setFont(font1)
        self.pushButton_reset.setStyleSheet(u"")

        self.gridLayout_8.addWidget(self.pushButton_reset, 0, 0, 1, 1)

        self.pushButton_remove = QPushButton(self.frame_3)
        self.pushButton_remove.setObjectName(u"pushButton_remove")
        self.pushButton_remove.setMinimumSize(QSize(100, 28))
        self.pushButton_remove.setMaximumSize(QSize(100, 28))
        self.pushButton_remove.setFont(font1)
        self.pushButton_remove.setStyleSheet(u"")

        self.gridLayout_8.addWidget(self.pushButton_remove, 0, 1, 1, 1)


        self.gridLayout_9.addWidget(self.frame_3, 1, 0, 1, 1)

        self.treeWidget_mass_flow_rate = QTreeWidget(self.tab_list)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter);
        self.treeWidget_mass_flow_rate.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_mass_flow_rate.setObjectName(u"treeWidget_mass_flow_rate")
        self.treeWidget_mass_flow_rate.setMinimumSize(QSize(320, 100))
        self.treeWidget_mass_flow_rate.setMaximumSize(QSize(320, 200))
        font4 = QFont()
        font4.setFamilies([u"MS Shell Dlg 2"])
        font4.setPointSize(10)
        font4.setItalic(False)
        self.treeWidget_mass_flow_rate.setFont(font4)
        self.treeWidget_mass_flow_rate.setIndentation(1)
        self.treeWidget_mass_flow_rate.setHeaderHidden(False)
        self.treeWidget_mass_flow_rate.header().setHighlightSections(False)
        self.treeWidget_mass_flow_rate.header().setProperty(u"showSortIndicator", False)
        self.treeWidget_mass_flow_rate.header().setStretchLastSection(True)

        self.gridLayout_9.addWidget(self.treeWidget_mass_flow_rate, 0, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_list, "")

        self.gridLayout_4.addWidget(self.tabWidget_main, 1, 0, 1, 1)


        self.gridLayout_7.addWidget(self.frame_2, 1, 0, 1, 1)

        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(380, 48))
        self.frame.setMaximumSize(QSize(420, 48))
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setLineWidth(1)
        self.gridLayout_6 = QGridLayout(self.frame)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        font5 = QFont()
        font5.setFamilies([u"MS Shell Dlg 2"])
        font5.setPointSize(11)
        font5.setBold(False)
        font5.setItalic(False)
        self.label.setFont(font5)
        self.label.setTextFormat(Qt.AutoText)
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout_6.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout_7.addWidget(self.frame, 0, 0, 1, 1)

        self.frame_11 = QFrame(Dialog)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setMinimumSize(QSize(340, 40))
        self.frame_11.setMaximumSize(QSize(16777215, 100))
        self.frame_11.setFrameShape(QFrame.NoFrame)
        self.frame_11.setFrameShadow(QFrame.Raised)
        self.gridLayout_14 = QGridLayout(self.frame_11)
        self.gridLayout_14.setSpacing(0)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.gridLayout_14.setContentsMargins(0, 0, 0, 0)
        self.pushButton_attribute = QPushButton(self.frame_11)
        self.pushButton_attribute.setObjectName(u"pushButton_attribute")
        self.pushButton_attribute.setMinimumSize(QSize(100, 28))
        self.pushButton_attribute.setMaximumSize(QSize(100, 28))
        self.pushButton_attribute.setFont(font1)
        self.pushButton_attribute.setStyleSheet(u"")

        self.gridLayout_14.addWidget(self.pushButton_attribute, 0, 1, 1, 1)

        self.pushButton_exit = QPushButton(self.frame_11)
        self.pushButton_exit.setObjectName(u"pushButton_exit")
        self.pushButton_exit.setMinimumSize(QSize(100, 28))
        self.pushButton_exit.setMaximumSize(QSize(100, 28))
        self.pushButton_exit.setFont(font1)
        self.pushButton_exit.setStyleSheet(u"")

        self.gridLayout_14.addWidget(self.pushButton_exit, 0, 0, 1, 1)


        self.gridLayout_7.addWidget(self.frame_11, 2, 0, 1, 1)


        self.retranslateUi(Dialog)

        self.tabWidget_main.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Set mass flow rate acoustic excitation", None))
#if QT_CONFIG(whatsthis)
        Dialog.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Selection ID:", None))
        self.label_21.setText(QCoreApplication.translate("Dialog", u"[kg/s]", None))
        self.label_18.setText(QCoreApplication.translate("Dialog", u"Mass flow rate:", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Real", None))
        self.label_20.setText(QCoreApplication.translate("Dialog", u"Imaginary", None))
        self.checkBox_averaged_constant_values.setText(QCoreApplication.translate("Dialog", u"Averaged value over all nodes", None))
        self.radioButton_element_integration_constant.setText(QCoreApplication.translate("Dialog", u"Element integration", None))
        self.radioButton_nodal_attribution_constant.setText(QCoreApplication.translate("Dialog", u"Nodal attribution", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_constant_values), QCoreApplication.translate("Dialog", u"Constant values", None))
        self.checkBox_averaged_table_values.setText(QCoreApplication.translate("Dialog", u"Average value over all nodes", None))
        self.pushButton_load_table.setText(QCoreApplication.translate("Dialog", u"Search", None))
#if QT_CONFIG(tooltip)
        self.pushButton_change_frequency_setup.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Filter the frequency range of interest</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_change_frequency_setup.setText("")
        self.radioButton_nodal_attribution_table.setText(QCoreApplication.translate("Dialog", u"Nodal attribution", None))
        self.radioButton_element_integration_table.setText(QCoreApplication.translate("Dialog", u"Element integration", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_load_tables), QCoreApplication.translate("Dialog", u"Load table", None))
        self.pushButton_reset.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.pushButton_remove.setText(QCoreApplication.translate("Dialog", u"Remove", None))
        ___qtreewidgetitem = self.treeWidget_mass_flow_rate.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"Values", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Nodes", None));
#if QT_CONFIG(tooltip)
        self.treeWidget_mass_flow_rate.setToolTip(QCoreApplication.translate("Dialog", u"Select a face to remove the previously attributed boundary condition.", None))
#endif // QT_CONFIG(tooltip)
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_list), QCoreApplication.translate("Dialog", u"List", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Set mass flow rate acoustic excitation", None))
        self.pushButton_attribute.setText(QCoreApplication.translate("Dialog", u"Attribute", None))
        self.pushButton_exit.setText(QCoreApplication.translate("Dialog", u"Exit", None))
    # retranslateUi



class MassFlowRateInputs_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame_2: QFrame
                    - (Layout): QGridLayout
                            - frame_4: QFrame
                                - (Layout): QGridLayout
                                        - lineEdit_selection_id: QLineEdit
                                        - label_2: QLabel
                            - tabWidget_main: QTabWidget
                                - tab_constant_values: QWidget
                                    - (Layout): QGridLayout
                                            - frame_8: QFrame
                                                - (Layout): QGridLayout
                                                        - lineEdit_imag_value: QLineEdit
                                                        - label_21: QLabel
                                                        - label_18: QLabel
                                                        - label_4: QLabel
                                                        - label_20: QLabel
                                                        - lineEdit_real_value: QLineEdit
                                            - frame_20: QFrame
                                                - (Layout): QGridLayout
                                                        - checkBox_averaged_constant_values: QCheckBox
                                            - frame_24: QFrame
                                                - (Layout): QGridLayout
                                                        - radioButton_element_integration_constant: QRadioButton
                                                        - radioButton_nodal_attribution_constant: QRadioButton
                                - tab_load_tables: QWidget
                                    - (Layout): QGridLayout
                                            - frame_21: QFrame
                                                - (Layout): QGridLayout
                                                        - checkBox_averaged_table_values: QCheckBox
                                            - frame_9: QFrame
                                                - (Layout): QGridLayout
                                                        - lineEdit_table_path: QLineEdit
                                                        - pushButton_load_table: QPushButton
                                                        - pushButton_change_frequency_setup: QPushButton
                                            - frame_16: QFrame
                                                - (Layout): QGridLayout
                                                        - radioButton_nodal_attribution_table: QRadioButton
                                                        - radioButton_element_integration_table: QRadioButton
                                - tab_list: QWidget
                                    - (Layout): QGridLayout
                                            - frame_3: QFrame
                                                - (Layout): QGridLayout
                                                        - pushButton_reset: QPushButton
                                                        - pushButton_remove: QPushButton
                                            - treeWidget_mass_flow_rate: QTreeWidget
                - frame: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
                - frame_11: QFrame
                    - (Layout): QGridLayout
                            - pushButton_attribute: QPushButton
                            - pushButton_exit: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
