# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'normal_pressure_load_inputs.ui'
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
        Dialog.setWindowModality(Qt.WindowModality.WindowModal)
        Dialog.resize(500, 468)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(500, 420))
        Dialog.setMaximumSize(QSize(500, 540))
        font = QFont()
        font.setPointSize(11)
        font.setBold(False)
        Dialog.setFont(font)
        Dialog.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        self.gridLayout_7 = QGridLayout(Dialog)
        self.gridLayout_7.setSpacing(4)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(4, 4, 4, 4)
        self.frame_2 = QFrame(Dialog)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(380, 0))
        self.frame_2.setMaximumSize(QSize(16777215, 480))
        self.frame_2.setFrameShape(QFrame.Shape.Box)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_2)
        self.gridLayout_4.setSpacing(2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(2, 4, 2, 2)
        self.frame_4 = QFrame(self.frame_2)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(360, 100))
        self.frame_4.setMaximumSize(QSize(16777215, 140))
        self.frame_4.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_4)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setHorizontalSpacing(6)
        self.gridLayout_5.setVerticalSpacing(2)
        self.gridLayout_5.setContentsMargins(2, 2, 2, 2)
        self.lineEdit_selection_id = QLineEdit(self.frame_4)
        self.lineEdit_selection_id.setObjectName(u"lineEdit_selection_id")
        self.lineEdit_selection_id.setMinimumSize(QSize(150, 28))
        self.lineEdit_selection_id.setMaximumSize(QSize(150, 28))
        font1 = QFont()
        font1.setFamilies([u"MS Shell Dlg 2"])
        font1.setPointSize(10)
        font1.setBold(False)
        font1.setItalic(False)
        self.lineEdit_selection_id.setFont(font1)
        self.lineEdit_selection_id.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.lineEdit_selection_id.setStyleSheet(u"")
        self.lineEdit_selection_id.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.lineEdit_selection_id, 0, 2, 1, 1)

        self.comboBox_element_type = QComboBox(self.frame_4)
        self.comboBox_element_type.addItem("")
        self.comboBox_element_type.addItem("")
        self.comboBox_element_type.setObjectName(u"comboBox_element_type")
        self.comboBox_element_type.setMinimumSize(QSize(150, 28))
        self.comboBox_element_type.setMaximumSize(QSize(150, 28))
        font2 = QFont()
        font2.setPointSize(10)
        font2.setBold(False)
        self.comboBox_element_type.setFont(font2)

        self.gridLayout_5.addWidget(self.comboBox_element_type, 1, 2, 1, 1)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_9, 0, 4, 1, 1)

        self.comboBox_assignment_type = QComboBox(self.frame_4)
        self.comboBox_assignment_type.addItem("")
        self.comboBox_assignment_type.setObjectName(u"comboBox_assignment_type")
        self.comboBox_assignment_type.setMinimumSize(QSize(120, 28))
        self.comboBox_assignment_type.setMaximumSize(QSize(120, 28))
        self.comboBox_assignment_type.setFont(font2)

        self.gridLayout_5.addWidget(self.comboBox_assignment_type, 0, 3, 1, 1)

        self.label_2 = QLabel(self.frame_4)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(120, 28))
        self.label_2.setMaximumSize(QSize(120, 28))
        self.label_2.setFont(font1)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_2, 0, 1, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_6, 0, 0, 1, 1)

        self.label_3 = QLabel(self.frame_4)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(120, 28))
        self.label_3.setMaximumSize(QSize(120, 28))
        self.label_3.setFont(font1)
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_3, 1, 1, 1, 1)

        self.comboBox_data_type = QComboBox(self.frame_4)
        self.comboBox_data_type.addItem("")
        self.comboBox_data_type.addItem("")
        self.comboBox_data_type.setObjectName(u"comboBox_data_type")
        self.comboBox_data_type.setMinimumSize(QSize(150, 28))
        self.comboBox_data_type.setMaximumSize(QSize(150, 28))
        self.comboBox_data_type.setFont(font2)

        self.gridLayout_5.addWidget(self.comboBox_data_type, 2, 2, 1, 1)

        self.label_5 = QLabel(self.frame_4)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(120, 28))
        self.label_5.setMaximumSize(QSize(120, 28))
        self.label_5.setFont(font1)
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_5, 2, 1, 1, 1)


        self.gridLayout_4.addWidget(self.frame_4, 0, 0, 1, 1)

        self.frame_6 = QFrame(self.frame_2)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_6.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_13 = QGridLayout(self.frame_6)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_13.setContentsMargins(4, 4, 4, 8)
        self.tabWidget_main = QTabWidget(self.frame_6)
        self.tabWidget_main.setObjectName(u"tabWidget_main")
        self.tabWidget_main.setMinimumSize(QSize(360, 0))
        self.tabWidget_main.setMaximumSize(QSize(16777215, 16777215))
        self.tabWidget_main.setFont(font2)
        self.tab_constant_data = QWidget()
        self.tab_constant_data.setObjectName(u"tab_constant_data")
        self.gridLayout_12 = QGridLayout(self.tab_constant_data)
        self.gridLayout_12.setSpacing(2)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setContentsMargins(2, 2, 2, 2)
        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_12.addItem(self.verticalSpacer_2, 2, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_12.addItem(self.verticalSpacer, 0, 0, 1, 1)

        self.frame_8 = QFrame(self.tab_constant_data)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setMinimumSize(QSize(340, 0))
        self.frame_8.setMaximumSize(QSize(16777215, 320))
        self.frame_8.setFont(font)
        self.frame_8.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_8.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.frame_8)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(8)
        self.gridLayout.setVerticalSpacing(6)
        self.gridLayout.setContentsMargins(2, 4, 2, 4)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 3, 5, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 3, 0, 1, 1)

        self.label_dtype_right = QLabel(self.frame_8)
        self.label_dtype_right.setObjectName(u"label_dtype_right")
        self.label_dtype_right.setMinimumSize(QSize(80, 26))
        self.label_dtype_right.setMaximumSize(QSize(16777215, 26))
        self.label_dtype_right.setFont(font1)
        self.label_dtype_right.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_dtype_right, 2, 3, 1, 1)

        self.label_dtype_left = QLabel(self.frame_8)
        self.label_dtype_left.setObjectName(u"label_dtype_left")
        self.label_dtype_left.setMinimumSize(QSize(80, 26))
        self.label_dtype_left.setMaximumSize(QSize(16777215, 26))
        self.label_dtype_left.setFont(font1)
        self.label_dtype_left.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_dtype_left, 2, 2, 1, 1)

        self.lineEdit_right_value = QLineEdit(self.frame_8)
        self.lineEdit_right_value.setObjectName(u"lineEdit_right_value")
        self.lineEdit_right_value.setMinimumSize(QSize(120, 26))
        self.lineEdit_right_value.setMaximumSize(QSize(120, 26))
        self.lineEdit_right_value.setFont(font1)
        self.lineEdit_right_value.setStyleSheet(u"")
        self.lineEdit_right_value.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_right_value, 3, 3, 1, 1)

        self.lineEdit_left_value = QLineEdit(self.frame_8)
        self.lineEdit_left_value.setObjectName(u"lineEdit_left_value")
        self.lineEdit_left_value.setMinimumSize(QSize(120, 26))
        self.lineEdit_left_value.setMaximumSize(QSize(120, 26))
        self.lineEdit_left_value.setFont(font1)
        self.lineEdit_left_value.setStyleSheet(u"")
        self.lineEdit_left_value.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_left_value, 3, 2, 1, 1)

        self.label_constant = QLabel(self.frame_8)
        self.label_constant.setObjectName(u"label_constant")
        self.label_constant.setMinimumSize(QSize(70, 26))
        self.label_constant.setMaximumSize(QSize(70, 26))
        self.label_constant.setFont(font1)
        self.label_constant.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_constant, 3, 1, 1, 1)

        self.label_unit = QLabel(self.frame_8)
        self.label_unit.setObjectName(u"label_unit")
        self.label_unit.setMinimumSize(QSize(80, 26))
        self.label_unit.setMaximumSize(QSize(80, 26))
        self.label_unit.setFont(font1)
        self.label_unit.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_unit, 3, 4, 1, 1)


        self.gridLayout_12.addWidget(self.frame_8, 1, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_constant_data, "")
        self.tab_tabular_data = QWidget()
        self.tab_tabular_data.setObjectName(u"tab_tabular_data")
        self.gridLayout_10 = QGridLayout(self.tab_tabular_data)
        self.gridLayout_10.setSpacing(2)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(2, 2, 2, 2)
        self.frame_9 = QFrame(self.tab_tabular_data)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_9.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_9)
        self.gridLayout_3.setSpacing(6)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(4, 4, 4, 2)
        self.label_table = QLabel(self.frame_9)
        self.label_table.setObjectName(u"label_table")
        self.label_table.setEnabled(True)
        self.label_table.setMinimumSize(QSize(0, 26))
        self.label_table.setMaximumSize(QSize(80, 26))
        self.label_table.setFont(font2)
        self.label_table.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_table, 0, 1, 1, 1)

        self.lineEdit_table_path = QLineEdit(self.frame_9)
        self.lineEdit_table_path.setObjectName(u"lineEdit_table_path")
        self.lineEdit_table_path.setEnabled(False)
        self.lineEdit_table_path.setMinimumSize(QSize(280, 26))
        self.lineEdit_table_path.setMaximumSize(QSize(280, 26))
        self.lineEdit_table_path.setStyleSheet(u"")
        self.lineEdit_table_path.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.lineEdit_table_path, 0, 2, 1, 1)

        self.pushButton_load_table = QPushButton(self.frame_9)
        self.pushButton_load_table.setObjectName(u"pushButton_load_table")
        self.pushButton_load_table.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton_load_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_table.setSizePolicy(sizePolicy1)
        self.pushButton_load_table.setMinimumSize(QSize(40, 26))
        self.pushButton_load_table.setMaximumSize(QSize(40, 26))
        self.pushButton_load_table.setFont(font2)
        self.pushButton_load_table.setStyleSheet(u"")
        icon = Icon(u":/icons/document_search_blue.png")
        self.pushButton_load_table.setIcon(icon)
        self.pushButton_load_table.setIconSize(QSize(20, 20))
        self.pushButton_load_table.setAutoDefault(False)

        self.gridLayout_3.addWidget(self.pushButton_load_table, 0, 3, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_3, 0, 4, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_4, 0, 0, 1, 1)


        self.gridLayout_10.addWidget(self.frame_9, 1, 0, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_10.addItem(self.verticalSpacer_4, 0, 0, 1, 1)

        self.verticalSpacer_8 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_10.addItem(self.verticalSpacer_8, 2, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_tabular_data, "")
        self.tab_list = QWidget()
        self.tab_list.setObjectName(u"tab_list")
        self.gridLayout_9 = QGridLayout(self.tab_list)
        self.gridLayout_9.setSpacing(2)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(2, 2, 2, 2)
        self.frame_5 = QFrame(self.tab_list)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_5)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.treeWidget_normal_pressure_loads = QTreeWidget(self.frame_5)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(2, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter);
        self.treeWidget_normal_pressure_loads.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_normal_pressure_loads.setObjectName(u"treeWidget_normal_pressure_loads")
        self.treeWidget_normal_pressure_loads.setMinimumSize(QSize(320, 0))
        self.treeWidget_normal_pressure_loads.setMaximumSize(QSize(16777215, 200))
        self.treeWidget_normal_pressure_loads.setFont(font1)
        self.treeWidget_normal_pressure_loads.setIndentation(1)
        self.treeWidget_normal_pressure_loads.setHeaderHidden(False)
        self.treeWidget_normal_pressure_loads.header().setHighlightSections(False)
        self.treeWidget_normal_pressure_loads.header().setProperty(u"showSortIndicator", False)
        self.treeWidget_normal_pressure_loads.header().setStretchLastSection(True)

        self.gridLayout_2.addWidget(self.treeWidget_normal_pressure_loads, 0, 0, 1, 1)


        self.gridLayout_9.addWidget(self.frame_5, 0, 0, 1, 1)

        self.frame_3 = QFrame(self.tab_list)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(320, 48))
        self.frame_3.setMaximumSize(QSize(16777215, 48))
        self.frame_3.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_8 = QGridLayout(self.frame_3)
        self.gridLayout_8.setSpacing(4)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
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

        self.tabWidget_main.addTab(self.tab_list, "")

        self.gridLayout_13.addWidget(self.tabWidget_main, 0, 0, 1, 1)


        self.gridLayout_4.addWidget(self.frame_6, 1, 0, 1, 1)


        self.gridLayout_7.addWidget(self.frame_2, 1, 0, 1, 1)

        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(380, 48))
        self.frame.setMaximumSize(QSize(16777215, 48))
        self.frame.setFrameShape(QFrame.Shape.Box)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.frame.setLineWidth(1)
        self.gridLayout_6 = QGridLayout(self.frame)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        font3 = QFont()
        font3.setFamilies([u"MS Shell Dlg 2"])
        font3.setPointSize(11)
        font3.setBold(False)
        font3.setItalic(False)
        self.label.setFont(font3)
        self.label.setTextFormat(Qt.TextFormat.AutoText)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_6.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout_7.addWidget(self.frame, 0, 0, 1, 1)

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
        font4 = QFont()
        font4.setPointSize(10)
        font4.setBold(False)
        font4.setItalic(False)
        self.pushButton_apply_and_close.setFont(font4)
        self.pushButton_apply_and_close.setStyleSheet(u"")
        self.pushButton_apply_and_close.setAutoDefault(False)
        self.pushButton_apply_and_close.setFlat(False)

        self.gridLayout_11.addWidget(self.pushButton_apply_and_close, 0, 3, 1, 1)

        self.pushButton_apply = QPushButton(self.frame_buttons)
        self.pushButton_apply.setObjectName(u"pushButton_apply")
        self.pushButton_apply.setMinimumSize(QSize(72, 30))
        self.pushButton_apply.setMaximumSize(QSize(72, 30))
        self.pushButton_apply.setFont(font4)
        self.pushButton_apply.setStyleSheet(u"")
        self.pushButton_apply.setAutoDefault(False)
        self.pushButton_apply.setFlat(False)

        self.gridLayout_11.addWidget(self.pushButton_apply, 0, 2, 1, 1)

        self.pushButton_cancel = QPushButton(self.frame_buttons)
        self.pushButton_cancel.setObjectName(u"pushButton_cancel")
        self.pushButton_cancel.setMinimumSize(QSize(72, 30))
        self.pushButton_cancel.setMaximumSize(QSize(72, 30))
        self.pushButton_cancel.setFont(font4)
        self.pushButton_cancel.setStyleSheet(u"")
        self.pushButton_cancel.setAutoDefault(False)
        self.pushButton_cancel.setFlat(False)

        self.gridLayout_11.addWidget(self.pushButton_cancel, 0, 0, 1, 1)

        self.horizontalSpacer_17 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_11.addItem(self.horizontalSpacer_17, 0, 1, 1, 1)


        self.gridLayout_7.addWidget(self.frame_buttons, 2, 0, 1, 1)


        self.retranslateUi(Dialog)

        self.tabWidget_main.setCurrentIndex(0)
        self.pushButton_apply_and_close.setDefault(False)
        self.pushButton_apply.setDefault(False)
        self.pushButton_cancel.setDefault(False)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Set normal pressure load", None))
#if QT_CONFIG(whatsthis)
        Dialog.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.comboBox_element_type.setItemText(0, QCoreApplication.translate("Dialog", u"Face element", None))
        self.comboBox_element_type.setItemText(1, QCoreApplication.translate("Dialog", u"Solid element", None))

        self.comboBox_assignment_type.setItemText(0, QCoreApplication.translate("Dialog", u"Selected faces", None))

        self.label_2.setText(QCoreApplication.translate("Dialog", u"Selection ID:", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Element type:", None))
        self.comboBox_data_type.setItemText(0, QCoreApplication.translate("Dialog", u"Real and imaginary", None))
        self.comboBox_data_type.setItemText(1, QCoreApplication.translate("Dialog", u"Amplitude and phase", None))

        self.label_5.setText(QCoreApplication.translate("Dialog", u"Data type:", None))
        self.label_dtype_right.setText(QCoreApplication.translate("Dialog", u"Imaginary", None))
        self.label_dtype_left.setText(QCoreApplication.translate("Dialog", u"Real", None))
        self.lineEdit_left_value.setText("")
        self.label_constant.setText(QCoreApplication.translate("Dialog", u"Pressure:", None))
        self.label_unit.setText(QCoreApplication.translate("Dialog", u"[N/m\u00b2]", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_constant_data), QCoreApplication.translate("Dialog", u"Constant data", None))
        self.label_table.setText(QCoreApplication.translate("Dialog", u"Pressure:", None))
        self.pushButton_load_table.setText("")
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_tabular_data), QCoreApplication.translate("Dialog", u"Tabular data", None))
        ___qtreewidgetitem = self.treeWidget_normal_pressure_loads.headerItem()
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("Dialog", u"Value (N/m\u00b2)", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"Entity", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"ID", None));
#if QT_CONFIG(tooltip)
        self.treeWidget_normal_pressure_loads.setToolTip(QCoreApplication.translate("Dialog", u"Select a node to remove the attributed boundary condition.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_reset.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.pushButton_remove.setText(QCoreApplication.translate("Dialog", u"Remove", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_list), QCoreApplication.translate("Dialog", u"List", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Set normal pressure load", None))
        self.pushButton_apply_and_close.setText(QCoreApplication.translate("Dialog", u"Ok", None))
        self.pushButton_apply.setText(QCoreApplication.translate("Dialog", u"Apply", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
    # retranslateUi



class NormalPressureLoadInputs_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame_2: QFrame
                    - (Layout): QGridLayout
                            - frame_4: QFrame
                                - (Layout): QGridLayout
                                        - lineEdit_selection_id: QLineEdit
                                        - comboBox_element_type: QComboBox
                                        - comboBox_assignment_type: QComboBox
                                        - label_2: QLabel
                                        - label_3: QLabel
                                        - comboBox_data_type: QComboBox
                                        - label_5: QLabel
                            - frame_6: QFrame
                                - (Layout): QGridLayout
                                        - tabWidget_main: QTabWidget
                                            - tab_constant_data: QWidget
                                                - (Layout): QGridLayout
                                                        - frame_8: QFrame
                                                            - (Layout): QGridLayout
                                                                    - label_dtype_right: QLabel
                                                                    - label_dtype_left: QLabel
                                                                    - lineEdit_right_value: QLineEdit
                                                                    - lineEdit_left_value: QLineEdit
                                                                    - label_constant: QLabel
                                                                    - label_unit: QLabel
                                            - tab_tabular_data: QWidget
                                                - (Layout): QGridLayout
                                                        - frame_9: QFrame
                                                            - (Layout): QGridLayout
                                                                    - label_table: QLabel
                                                                    - lineEdit_table_path: QLineEdit
                                                                    - pushButton_load_table: QPushButton
                                            - tab_list: QWidget
                                                - (Layout): QGridLayout
                                                        - frame_5: QFrame
                                                            - (Layout): QGridLayout
                                                                    - treeWidget_normal_pressure_loads: QTreeWidget
                                                        - frame_3: QFrame
                                                            - (Layout): QGridLayout
                                                                    - pushButton_reset: QPushButton
                                                                    - pushButton_remove: QPushButton
                - frame: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
                - frame_buttons: QFrame
                    - (Layout): QGridLayout
                            - pushButton_apply_and_close: QPushButton
                            - pushButton_apply: QPushButton
                            - pushButton_cancel: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
