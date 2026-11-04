# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'distributed_dampings_inputs.ui'
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
        Dialog.resize(500, 540)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(460, 420))
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
        self.frame_4.setMinimumSize(QSize(360, 140))
        self.frame_4.setMaximumSize(QSize(16777215, 16777215))
        self.frame_4.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_4)
        self.gridLayout_5.setSpacing(6)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(2, 4, 2, 4)
        self.comboBox_data_type = QComboBox(self.frame_4)
        self.comboBox_data_type.addItem("")
        self.comboBox_data_type.addItem("")
        self.comboBox_data_type.setObjectName(u"comboBox_data_type")
        self.comboBox_data_type.setMinimumSize(QSize(150, 28))
        self.comboBox_data_type.setMaximumSize(QSize(150, 28))
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(False)
        self.comboBox_data_type.setFont(font1)

        self.gridLayout_5.addWidget(self.comboBox_data_type, 2, 2, 1, 1)

        self.comboBox_assignment_type = QComboBox(self.frame_4)
        self.comboBox_assignment_type.addItem("")
        self.comboBox_assignment_type.addItem("")
        self.comboBox_assignment_type.setObjectName(u"comboBox_assignment_type")
        self.comboBox_assignment_type.setMinimumSize(QSize(0, 28))
        self.comboBox_assignment_type.setMaximumSize(QSize(16777215, 28))
        self.comboBox_assignment_type.setFont(font1)

        self.gridLayout_5.addWidget(self.comboBox_assignment_type, 0, 3, 1, 1)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_9, 0, 4, 1, 1)

        self.label_2 = QLabel(self.frame_4)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(100, 28))
        self.label_2.setMaximumSize(QSize(100, 28))
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        self.label_2.setFont(font2)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_2, 0, 1, 1, 1)

        self.lineEdit_selection_id = QLineEdit(self.frame_4)
        self.lineEdit_selection_id.setObjectName(u"lineEdit_selection_id")
        self.lineEdit_selection_id.setMinimumSize(QSize(150, 28))
        self.lineEdit_selection_id.setMaximumSize(QSize(150, 28))
        self.lineEdit_selection_id.setFont(font2)
        self.lineEdit_selection_id.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.lineEdit_selection_id.setStyleSheet(u"")
        self.lineEdit_selection_id.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.lineEdit_selection_id, 0, 2, 1, 1)

        self.label_3 = QLabel(self.frame_4)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(100, 28))
        self.label_3.setMaximumSize(QSize(100, 28))
        self.label_3.setFont(font2)
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_3, 1, 1, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_6, 0, 0, 1, 1)

        self.label_7 = QLabel(self.frame_4)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(120, 28))
        self.label_7.setMaximumSize(QSize(120, 28))
        self.label_7.setFont(font2)
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_7, 2, 1, 1, 1)

        self.comboBox_element_type = QComboBox(self.frame_4)
        self.comboBox_element_type.addItem("")
        self.comboBox_element_type.addItem("")
        self.comboBox_element_type.setObjectName(u"comboBox_element_type")
        self.comboBox_element_type.setMinimumSize(QSize(150, 28))
        self.comboBox_element_type.setMaximumSize(QSize(150, 28))
        self.comboBox_element_type.setFont(font1)

        self.gridLayout_5.addWidget(self.comboBox_element_type, 1, 2, 1, 1)

        self.comboBox_direction_control = QComboBox(self.frame_4)
        self.comboBox_direction_control.addItem("")
        self.comboBox_direction_control.addItem("")
        self.comboBox_direction_control.setObjectName(u"comboBox_direction_control")
        self.comboBox_direction_control.setMinimumSize(QSize(0, 28))
        self.comboBox_direction_control.setMaximumSize(QSize(16777215, 28))
        self.comboBox_direction_control.setFont(font1)

        self.gridLayout_5.addWidget(self.comboBox_direction_control, 3, 2, 1, 1)

        self.label_8 = QLabel(self.frame_4)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMinimumSize(QSize(120, 28))
        self.label_8.setMaximumSize(QSize(120, 28))
        self.label_8.setFont(font2)
        self.label_8.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_8, 3, 1, 1, 1)


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
        self.tabWidget_main.setMaximumSize(QSize(460, 16777215))
        self.tabWidget_main.setFont(font1)
        self.tab_constant_data = QWidget()
        self.tab_constant_data.setObjectName(u"tab_constant_data")
        self.gridLayout_12 = QGridLayout(self.tab_constant_data)
        self.gridLayout_12.setSpacing(2)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setContentsMargins(2, 2, 2, 2)
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_12.addItem(self.verticalSpacer, 0, 0, 1, 1)

        self.frame_8 = QFrame(self.tab_constant_data)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setMinimumSize(QSize(340, 0))
        self.frame_8.setMaximumSize(QSize(16777215, 16777215))
        self.frame_8.setFont(font)
        self.frame_8.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_8.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.frame_8)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(8)
        self.gridLayout.setVerticalSpacing(12)
        self.gridLayout.setContentsMargins(4, 4, 4, 6)
        self.lineEdit_right_Cy = QLineEdit(self.frame_8)
        self.lineEdit_right_Cy.setObjectName(u"lineEdit_right_Cy")
        self.lineEdit_right_Cy.setMinimumSize(QSize(120, 26))
        self.lineEdit_right_Cy.setMaximumSize(QSize(120, 26))
        self.lineEdit_right_Cy.setFont(font2)
        self.lineEdit_right_Cy.setStyleSheet(u"")
        self.lineEdit_right_Cy.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_right_Cy, 4, 3, 1, 1)

        self.lineEdit_left_Cy = QLineEdit(self.frame_8)
        self.lineEdit_left_Cy.setObjectName(u"lineEdit_left_Cy")
        self.lineEdit_left_Cy.setMinimumSize(QSize(120, 26))
        self.lineEdit_left_Cy.setMaximumSize(QSize(120, 26))
        self.lineEdit_left_Cy.setFont(font2)
        self.lineEdit_left_Cy.setStyleSheet(u"")
        self.lineEdit_left_Cy.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_left_Cy, 4, 2, 1, 1)

        self.label_unit_Cx = QLabel(self.frame_8)
        self.label_unit_Cx.setObjectName(u"label_unit_Cx")
        self.label_unit_Cx.setMinimumSize(QSize(90, 26))
        self.label_unit_Cx.setMaximumSize(QSize(90, 26))
        self.label_unit_Cx.setFont(font2)
        self.label_unit_Cx.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_unit_Cx, 3, 4, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 3, 5, 1, 1)

        self.lineEdit_left_Cx = QLineEdit(self.frame_8)
        self.lineEdit_left_Cx.setObjectName(u"lineEdit_left_Cx")
        self.lineEdit_left_Cx.setMinimumSize(QSize(120, 26))
        self.lineEdit_left_Cx.setMaximumSize(QSize(120, 26))
        self.lineEdit_left_Cx.setFont(font2)
        self.lineEdit_left_Cx.setStyleSheet(u"")
        self.lineEdit_left_Cx.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_left_Cx, 3, 2, 1, 1)

        self.label_dtype_left = QLabel(self.frame_8)
        self.label_dtype_left.setObjectName(u"label_dtype_left")
        self.label_dtype_left.setMinimumSize(QSize(80, 26))
        self.label_dtype_left.setMaximumSize(QSize(16777215, 26))
        self.label_dtype_left.setFont(font2)
        self.label_dtype_left.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_dtype_left, 2, 2, 1, 1)

        self.lineEdit_right_Cx = QLineEdit(self.frame_8)
        self.lineEdit_right_Cx.setObjectName(u"lineEdit_right_Cx")
        self.lineEdit_right_Cx.setMinimumSize(QSize(120, 26))
        self.lineEdit_right_Cx.setMaximumSize(QSize(120, 26))
        self.lineEdit_right_Cx.setFont(font2)
        self.lineEdit_right_Cx.setStyleSheet(u"")
        self.lineEdit_right_Cx.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_right_Cx, 3, 3, 1, 1)

        self.label_unit_Cz = QLabel(self.frame_8)
        self.label_unit_Cz.setObjectName(u"label_unit_Cz")
        self.label_unit_Cz.setMinimumSize(QSize(90, 26))
        self.label_unit_Cz.setMaximumSize(QSize(90, 26))
        self.label_unit_Cz.setFont(font2)
        self.label_unit_Cz.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_unit_Cz, 5, 4, 1, 1)

        self.label_unit_Cy = QLabel(self.frame_8)
        self.label_unit_Cy.setObjectName(u"label_unit_Cy")
        self.label_unit_Cy.setMinimumSize(QSize(90, 26))
        self.label_unit_Cy.setMaximumSize(QSize(90, 26))
        self.label_unit_Cy.setFont(font2)
        self.label_unit_Cy.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_unit_Cy, 4, 4, 1, 1)

        self.label_dtype_right = QLabel(self.frame_8)
        self.label_dtype_right.setObjectName(u"label_dtype_right")
        self.label_dtype_right.setMinimumSize(QSize(80, 26))
        self.label_dtype_right.setMaximumSize(QSize(16777215, 26))
        self.label_dtype_right.setFont(font2)
        self.label_dtype_right.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_dtype_right, 2, 3, 1, 1)

        self.lineEdit_left_Cz = QLineEdit(self.frame_8)
        self.lineEdit_left_Cz.setObjectName(u"lineEdit_left_Cz")
        self.lineEdit_left_Cz.setMinimumSize(QSize(120, 26))
        self.lineEdit_left_Cz.setMaximumSize(QSize(120, 26))
        self.lineEdit_left_Cz.setFont(font2)
        self.lineEdit_left_Cz.setStyleSheet(u"")
        self.lineEdit_left_Cz.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_left_Cz, 5, 2, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 3, 0, 1, 1)

        self.label_constant_Cy = QLabel(self.frame_8)
        self.label_constant_Cy.setObjectName(u"label_constant_Cy")
        self.label_constant_Cy.setMinimumSize(QSize(60, 26))
        self.label_constant_Cy.setMaximumSize(QSize(60, 26))
        self.label_constant_Cy.setFont(font2)
        self.label_constant_Cy.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_constant_Cy, 4, 1, 1, 1)

        self.label_constant_Cz = QLabel(self.frame_8)
        self.label_constant_Cz.setObjectName(u"label_constant_Cz")
        self.label_constant_Cz.setMinimumSize(QSize(60, 26))
        self.label_constant_Cz.setMaximumSize(QSize(60, 26))
        self.label_constant_Cz.setFont(font2)
        self.label_constant_Cz.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_constant_Cz, 5, 1, 1, 1)

        self.lineEdit_right_Cz = QLineEdit(self.frame_8)
        self.lineEdit_right_Cz.setObjectName(u"lineEdit_right_Cz")
        self.lineEdit_right_Cz.setMinimumSize(QSize(120, 26))
        self.lineEdit_right_Cz.setMaximumSize(QSize(120, 26))
        self.lineEdit_right_Cz.setFont(font2)
        self.lineEdit_right_Cz.setStyleSheet(u"")
        self.lineEdit_right_Cz.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_right_Cz, 5, 3, 1, 1)

        self.label_constant_Cx = QLabel(self.frame_8)
        self.label_constant_Cx.setObjectName(u"label_constant_Cx")
        self.label_constant_Cx.setMinimumSize(QSize(60, 26))
        self.label_constant_Cx.setMaximumSize(QSize(60, 26))
        self.label_constant_Cx.setFont(font2)
        self.label_constant_Cx.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_constant_Cx, 3, 1, 1, 1)


        self.gridLayout_12.addWidget(self.frame_8, 2, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_12.addItem(self.verticalSpacer_2, 3, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_constant_data, "")
        self.tab_tabular_data = QWidget()
        self.tab_tabular_data.setObjectName(u"tab_tabular_data")
        self.gridLayout_10 = QGridLayout(self.tab_tabular_data)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(2, 2, 2, 2)
        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_10.addItem(self.verticalSpacer_4, 2, 0, 1, 1)

        self.frame_9 = QFrame(self.tab_tabular_data)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_9.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_9)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setHorizontalSpacing(6)
        self.gridLayout_3.setVerticalSpacing(12)
        self.gridLayout_3.setContentsMargins(4, 4, 4, 2)
        self.lineEdit_path_table_Cy = QLineEdit(self.frame_9)
        self.lineEdit_path_table_Cy.setObjectName(u"lineEdit_path_table_Cy")
        self.lineEdit_path_table_Cy.setEnabled(False)
        self.lineEdit_path_table_Cy.setMinimumSize(QSize(320, 26))
        self.lineEdit_path_table_Cy.setMaximumSize(QSize(320, 26))
        self.lineEdit_path_table_Cy.setStyleSheet(u"")
        self.lineEdit_path_table_Cy.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.lineEdit_path_table_Cy, 2, 2, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_3, 1, 4, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_4, 1, 0, 1, 1)

        self.pushButton_load_Cz_table = QPushButton(self.frame_9)
        self.pushButton_load_Cz_table.setObjectName(u"pushButton_load_Cz_table")
        self.pushButton_load_Cz_table.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton_load_Cz_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_Cz_table.setSizePolicy(sizePolicy1)
        self.pushButton_load_Cz_table.setMinimumSize(QSize(40, 26))
        self.pushButton_load_Cz_table.setMaximumSize(QSize(40, 26))
        self.pushButton_load_Cz_table.setFont(font1)
        self.pushButton_load_Cz_table.setStyleSheet(u"")
        icon = Icon(u":/icons/document_search_blue.png")
        self.pushButton_load_Cz_table.setIcon(icon)
        self.pushButton_load_Cz_table.setIconSize(QSize(20, 20))
        self.pushButton_load_Cz_table.setAutoDefault(False)

        self.gridLayout_3.addWidget(self.pushButton_load_Cz_table, 3, 3, 1, 1)

        self.pushButton_load_Cx_table = QPushButton(self.frame_9)
        self.pushButton_load_Cx_table.setObjectName(u"pushButton_load_Cx_table")
        self.pushButton_load_Cx_table.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.pushButton_load_Cx_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_Cx_table.setSizePolicy(sizePolicy1)
        self.pushButton_load_Cx_table.setMinimumSize(QSize(40, 26))
        self.pushButton_load_Cx_table.setMaximumSize(QSize(40, 26))
        self.pushButton_load_Cx_table.setFont(font1)
        self.pushButton_load_Cx_table.setStyleSheet(u"")
        self.pushButton_load_Cx_table.setIcon(icon)
        self.pushButton_load_Cx_table.setIconSize(QSize(20, 20))
        self.pushButton_load_Cx_table.setAutoDefault(False)

        self.gridLayout_3.addWidget(self.pushButton_load_Cx_table, 1, 3, 1, 1)

        self.label_table_Cy = QLabel(self.frame_9)
        self.label_table_Cy.setObjectName(u"label_table_Cy")
        self.label_table_Cy.setEnabled(True)
        self.label_table_Cy.setMinimumSize(QSize(0, 26))
        self.label_table_Cy.setMaximumSize(QSize(80, 26))
        self.label_table_Cy.setFont(font1)
        self.label_table_Cy.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_table_Cy, 2, 1, 1, 1)

        self.lineEdit_path_table_Cz = QLineEdit(self.frame_9)
        self.lineEdit_path_table_Cz.setObjectName(u"lineEdit_path_table_Cz")
        self.lineEdit_path_table_Cz.setEnabled(False)
        self.lineEdit_path_table_Cz.setMinimumSize(QSize(320, 26))
        self.lineEdit_path_table_Cz.setMaximumSize(QSize(320, 26))
        self.lineEdit_path_table_Cz.setStyleSheet(u"")
        self.lineEdit_path_table_Cz.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.lineEdit_path_table_Cz, 3, 2, 1, 1)

        self.label_table_Cx = QLabel(self.frame_9)
        self.label_table_Cx.setObjectName(u"label_table_Cx")
        self.label_table_Cx.setEnabled(True)
        self.label_table_Cx.setMinimumSize(QSize(0, 26))
        self.label_table_Cx.setMaximumSize(QSize(80, 26))
        self.label_table_Cx.setFont(font1)
        self.label_table_Cx.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_table_Cx, 1, 1, 1, 1)

        self.lineEdit_path_table_Cx = QLineEdit(self.frame_9)
        self.lineEdit_path_table_Cx.setObjectName(u"lineEdit_path_table_Cx")
        self.lineEdit_path_table_Cx.setEnabled(False)
        self.lineEdit_path_table_Cx.setMinimumSize(QSize(320, 26))
        self.lineEdit_path_table_Cx.setMaximumSize(QSize(320, 26))
        self.lineEdit_path_table_Cx.setStyleSheet(u"")
        self.lineEdit_path_table_Cx.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.lineEdit_path_table_Cx, 1, 2, 1, 1)

        self.pushButton_load_Cy_table = QPushButton(self.frame_9)
        self.pushButton_load_Cy_table.setObjectName(u"pushButton_load_Cy_table")
        self.pushButton_load_Cy_table.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.pushButton_load_Cy_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_Cy_table.setSizePolicy(sizePolicy1)
        self.pushButton_load_Cy_table.setMinimumSize(QSize(40, 26))
        self.pushButton_load_Cy_table.setMaximumSize(QSize(40, 26))
        self.pushButton_load_Cy_table.setFont(font1)
        self.pushButton_load_Cy_table.setStyleSheet(u"")
        self.pushButton_load_Cy_table.setIcon(icon)
        self.pushButton_load_Cy_table.setIconSize(QSize(20, 20))
        self.pushButton_load_Cy_table.setAutoDefault(False)

        self.gridLayout_3.addWidget(self.pushButton_load_Cy_table, 2, 3, 1, 1)

        self.label_table_Cz = QLabel(self.frame_9)
        self.label_table_Cz.setObjectName(u"label_table_Cz")
        self.label_table_Cz.setEnabled(True)
        self.label_table_Cz.setMinimumSize(QSize(0, 26))
        self.label_table_Cz.setMaximumSize(QSize(80, 26))
        self.label_table_Cz.setFont(font1)
        self.label_table_Cz.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_table_Cz, 3, 1, 1, 1)


        self.gridLayout_10.addWidget(self.frame_9, 1, 0, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_10.addItem(self.verticalSpacer_3, 0, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_tabular_data, "")
        self.tab_list = QWidget()
        self.tab_list.setObjectName(u"tab_list")
        self.gridLayout_9 = QGridLayout(self.tab_list)
        self.gridLayout_9.setSpacing(2)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(2, 2, 2, 2)
        self.frame_5 = QFrame(self.tab_list)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_5)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.treeWidget_distributed_dampings = QTreeWidget(self.frame_5)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(3, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(2, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter);
        self.treeWidget_distributed_dampings.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_distributed_dampings.setObjectName(u"treeWidget_distributed_dampings")
        self.treeWidget_distributed_dampings.setMinimumSize(QSize(320, 0))
        self.treeWidget_distributed_dampings.setMaximumSize(QSize(16777215, 16777215))
        self.treeWidget_distributed_dampings.setFont(font2)
        self.treeWidget_distributed_dampings.setIndentation(1)
        self.treeWidget_distributed_dampings.setHeaderHidden(False)
        self.treeWidget_distributed_dampings.header().setHighlightSections(False)
        self.treeWidget_distributed_dampings.header().setProperty(u"showSortIndicator", False)
        self.treeWidget_distributed_dampings.header().setStretchLastSection(True)

        self.gridLayout_2.addWidget(self.treeWidget_distributed_dampings, 0, 0, 1, 1)


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

        QWidget.setTabOrder(self.comboBox_assignment_type, self.comboBox_element_type)
        QWidget.setTabOrder(self.comboBox_element_type, self.comboBox_data_type)
        QWidget.setTabOrder(self.comboBox_data_type, self.tabWidget_main)
        QWidget.setTabOrder(self.tabWidget_main, self.lineEdit_left_Cx)
        QWidget.setTabOrder(self.lineEdit_left_Cx, self.lineEdit_left_Cy)
        QWidget.setTabOrder(self.lineEdit_left_Cy, self.lineEdit_left_Cz)
        QWidget.setTabOrder(self.lineEdit_left_Cz, self.lineEdit_right_Cx)
        QWidget.setTabOrder(self.lineEdit_right_Cx, self.lineEdit_right_Cy)
        QWidget.setTabOrder(self.lineEdit_right_Cy, self.lineEdit_right_Cz)
        QWidget.setTabOrder(self.lineEdit_right_Cz, self.pushButton_apply_and_close)
        QWidget.setTabOrder(self.pushButton_apply_and_close, self.pushButton_apply)
        QWidget.setTabOrder(self.pushButton_apply, self.pushButton_cancel)
        QWidget.setTabOrder(self.pushButton_cancel, self.lineEdit_path_table_Cx)
        QWidget.setTabOrder(self.lineEdit_path_table_Cx, self.pushButton_load_Cx_table)
        QWidget.setTabOrder(self.pushButton_load_Cx_table, self.lineEdit_path_table_Cy)
        QWidget.setTabOrder(self.lineEdit_path_table_Cy, self.pushButton_load_Cy_table)
        QWidget.setTabOrder(self.pushButton_load_Cy_table, self.lineEdit_path_table_Cz)
        QWidget.setTabOrder(self.lineEdit_path_table_Cz, self.pushButton_load_Cz_table)
        QWidget.setTabOrder(self.pushButton_load_Cz_table, self.treeWidget_distributed_dampings)
        QWidget.setTabOrder(self.treeWidget_distributed_dampings, self.pushButton_remove)
        QWidget.setTabOrder(self.pushButton_remove, self.pushButton_reset)

        self.retranslateUi(Dialog)

        self.comboBox_element_type.setCurrentIndex(1)
        self.tabWidget_main.setCurrentIndex(0)
        self.pushButton_apply_and_close.setDefault(False)
        self.pushButton_apply.setDefault(False)
        self.pushButton_cancel.setDefault(False)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Set distributed mass", None))
#if QT_CONFIG(whatsthis)
        Dialog.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.comboBox_data_type.setItemText(0, QCoreApplication.translate("Dialog", u"Real and imaginary", None))
        self.comboBox_data_type.setItemText(1, QCoreApplication.translate("Dialog", u"Magnitude and phase", None))

        self.comboBox_assignment_type.setItemText(0, QCoreApplication.translate("Dialog", u"Selected faces", None))
        self.comboBox_assignment_type.setItemText(1, QCoreApplication.translate("Dialog", u"Selected lines", None))

        self.label_2.setText(QCoreApplication.translate("Dialog", u"Selection ID:", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Element type:", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"Data type:", None))
        self.comboBox_element_type.setItemText(0, QCoreApplication.translate("Dialog", u"Face element", None))
        self.comboBox_element_type.setItemText(1, QCoreApplication.translate("Dialog", u"Solid element", None))

        self.comboBox_direction_control.setItemText(0, QCoreApplication.translate("Dialog", u"By components", None))
        self.comboBox_direction_control.setItemText(1, QCoreApplication.translate("Dialog", u"By normal", None))

        self.label_8.setText(QCoreApplication.translate("Dialog", u"Direction control:", None))
        self.label_unit_Cx.setText(QCoreApplication.translate("Dialog", u"[N.s/m]", None))
        self.lineEdit_left_Cx.setText("")
        self.label_dtype_left.setText(QCoreApplication.translate("Dialog", u"Real", None))
        self.label_unit_Cz.setText(QCoreApplication.translate("Dialog", u"[N.s/m]", None))
        self.label_unit_Cy.setText(QCoreApplication.translate("Dialog", u"[N.s/m]", None))
        self.label_dtype_right.setText(QCoreApplication.translate("Dialog", u"Imaginary", None))
        self.label_constant_Cy.setText(QCoreApplication.translate("Dialog", u"Cy:", None))
        self.label_constant_Cz.setText(QCoreApplication.translate("Dialog", u"Cz:", None))
        self.label_constant_Cx.setText(QCoreApplication.translate("Dialog", u"Cx:", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_constant_data), QCoreApplication.translate("Dialog", u"Constant data", None))
        self.pushButton_load_Cz_table.setText("")
        self.pushButton_load_Cx_table.setText("")
        self.label_table_Cy.setText(QCoreApplication.translate("Dialog", u"Cy:", None))
        self.label_table_Cx.setText(QCoreApplication.translate("Dialog", u"Cx:", None))
        self.pushButton_load_Cy_table.setText("")
        self.label_table_Cz.setText(QCoreApplication.translate("Dialog", u"Cz:", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_tabular_data), QCoreApplication.translate("Dialog", u"Tabular data", None))
        ___qtreewidgetitem = self.treeWidget_distributed_dampings.headerItem()
        ___qtreewidgetitem.setText(3, QCoreApplication.translate("Dialog", u"Label", None));
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("Dialog", u"Element type", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"Entity", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"ID", None));
#if QT_CONFIG(tooltip)
        self.treeWidget_distributed_dampings.setToolTip(QCoreApplication.translate("Dialog", u"Select a node to remove the attributed boundary condition.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_reset.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.pushButton_remove.setText(QCoreApplication.translate("Dialog", u"Remove", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_list), QCoreApplication.translate("Dialog", u"List", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Set distributed dampings", None))
        self.pushButton_apply_and_close.setText(QCoreApplication.translate("Dialog", u"Ok", None))
        self.pushButton_apply.setText(QCoreApplication.translate("Dialog", u"Apply", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
    # retranslateUi



class DistributedDampingsInputs_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame_2: QFrame
                    - (Layout): QGridLayout
                            - frame_4: QFrame
                                - (Layout): QGridLayout
                                        - comboBox_data_type: QComboBox
                                        - comboBox_assignment_type: QComboBox
                                        - label_2: QLabel
                                        - lineEdit_selection_id: QLineEdit
                                        - label_3: QLabel
                                        - label_7: QLabel
                                        - comboBox_element_type: QComboBox
                                        - comboBox_direction_control: QComboBox
                                        - label_8: QLabel
                            - frame_6: QFrame
                                - (Layout): QGridLayout
                                        - tabWidget_main: QTabWidget
                                            - tab_constant_data: QWidget
                                                - (Layout): QGridLayout
                                                        - frame_8: QFrame
                                                            - (Layout): QGridLayout
                                                                    - lineEdit_right_Cy: QLineEdit
                                                                    - lineEdit_left_Cy: QLineEdit
                                                                    - label_unit_Cx: QLabel
                                                                    - lineEdit_left_Cx: QLineEdit
                                                                    - label_dtype_left: QLabel
                                                                    - lineEdit_right_Cx: QLineEdit
                                                                    - label_unit_Cz: QLabel
                                                                    - label_unit_Cy: QLabel
                                                                    - label_dtype_right: QLabel
                                                                    - lineEdit_left_Cz: QLineEdit
                                                                    - label_constant_Cy: QLabel
                                                                    - label_constant_Cz: QLabel
                                                                    - lineEdit_right_Cz: QLineEdit
                                                                    - label_constant_Cx: QLabel
                                            - tab_tabular_data: QWidget
                                                - (Layout): QGridLayout
                                                        - frame_9: QFrame
                                                            - (Layout): QGridLayout
                                                                    - lineEdit_path_table_Cy: QLineEdit
                                                                    - pushButton_load_Cz_table: QPushButton
                                                                    - pushButton_load_Cx_table: QPushButton
                                                                    - label_table_Cy: QLabel
                                                                    - lineEdit_path_table_Cz: QLineEdit
                                                                    - label_table_Cx: QLabel
                                                                    - lineEdit_path_table_Cx: QLineEdit
                                                                    - pushButton_load_Cy_table: QPushButton
                                                                    - label_table_Cz: QLabel
                                            - tab_list: QWidget
                                                - (Layout): QGridLayout
                                                        - frame_5: QFrame
                                                            - (Layout): QGridLayout
                                                                    - treeWidget_distributed_dampings: QTreeWidget
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
