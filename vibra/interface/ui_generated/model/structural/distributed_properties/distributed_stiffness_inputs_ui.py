# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'distributed_stiffness_inputs.ui'
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
        self.frame_4.setMinimumSize(QSize(360, 160))
        self.frame_4.setMaximumSize(QSize(16777215, 16777215))
        self.frame_4.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_4)
        self.gridLayout_5.setSpacing(6)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(2, 4, 2, 4)
        self.comboBox_direction_control = QComboBox(self.frame_4)
        self.comboBox_direction_control.addItem("")
        self.comboBox_direction_control.addItem("")
        self.comboBox_direction_control.setObjectName(u"comboBox_direction_control")
        self.comboBox_direction_control.setMinimumSize(QSize(0, 28))
        self.comboBox_direction_control.setMaximumSize(QSize(16777215, 28))
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(False)
        self.comboBox_direction_control.setFont(font1)

        self.gridLayout_5.addWidget(self.comboBox_direction_control, 3, 2, 1, 1)

        self.label_3 = QLabel(self.frame_4)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(120, 28))
        self.label_3.setMaximumSize(QSize(120, 28))
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        self.label_3.setFont(font2)
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_3, 1, 1, 1, 1)

        self.label_7 = QLabel(self.frame_4)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(120, 28))
        self.label_7.setMaximumSize(QSize(120, 28))
        self.label_7.setFont(font2)
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_7, 2, 1, 1, 1)

        self.comboBox_assignment_type = QComboBox(self.frame_4)
        self.comboBox_assignment_type.addItem("")
        self.comboBox_assignment_type.addItem("")
        self.comboBox_assignment_type.setObjectName(u"comboBox_assignment_type")
        self.comboBox_assignment_type.setMinimumSize(QSize(0, 28))
        self.comboBox_assignment_type.setMaximumSize(QSize(16777215, 28))
        self.comboBox_assignment_type.setFont(font1)

        self.gridLayout_5.addWidget(self.comboBox_assignment_type, 0, 3, 1, 1)

        self.label_2 = QLabel(self.frame_4)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(120, 28))
        self.label_2.setMaximumSize(QSize(120, 28))
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

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_9, 0, 4, 1, 1)

        self.label_8 = QLabel(self.frame_4)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMinimumSize(QSize(120, 28))
        self.label_8.setMaximumSize(QSize(120, 28))
        self.label_8.setFont(font2)
        self.label_8.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_8, 3, 1, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_6, 0, 0, 1, 1)

        self.comboBox_element_type = QComboBox(self.frame_4)
        self.comboBox_element_type.addItem("")
        self.comboBox_element_type.addItem("")
        self.comboBox_element_type.setObjectName(u"comboBox_element_type")
        self.comboBox_element_type.setMinimumSize(QSize(150, 28))
        self.comboBox_element_type.setMaximumSize(QSize(150, 28))
        self.comboBox_element_type.setFont(font1)

        self.gridLayout_5.addWidget(self.comboBox_element_type, 1, 2, 1, 1)

        self.comboBox_data_type = QComboBox(self.frame_4)
        self.comboBox_data_type.addItem("")
        self.comboBox_data_type.addItem("")
        self.comboBox_data_type.setObjectName(u"comboBox_data_type")
        self.comboBox_data_type.setMinimumSize(QSize(150, 28))
        self.comboBox_data_type.setMaximumSize(QSize(150, 28))
        self.comboBox_data_type.setFont(font1)

        self.gridLayout_5.addWidget(self.comboBox_data_type, 2, 2, 1, 1)

        self.label_9 = QLabel(self.frame_4)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMinimumSize(QSize(120, 28))
        self.label_9.setMaximumSize(QSize(120, 28))
        self.label_9.setFont(font2)
        self.label_9.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_9, 4, 1, 1, 1)

        self.comboBox_stiffness_input = QComboBox(self.frame_4)
        self.comboBox_stiffness_input.addItem("")
        self.comboBox_stiffness_input.addItem("")
        self.comboBox_stiffness_input.setObjectName(u"comboBox_stiffness_input")
        self.comboBox_stiffness_input.setMinimumSize(QSize(0, 28))
        self.comboBox_stiffness_input.setMaximumSize(QSize(16777215, 28))
        self.comboBox_stiffness_input.setFont(font1)

        self.gridLayout_5.addWidget(self.comboBox_stiffness_input, 4, 2, 1, 1)


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
        self.lineEdit_right_Ky = QLineEdit(self.frame_8)
        self.lineEdit_right_Ky.setObjectName(u"lineEdit_right_Ky")
        self.lineEdit_right_Ky.setMinimumSize(QSize(120, 26))
        self.lineEdit_right_Ky.setMaximumSize(QSize(120, 26))
        self.lineEdit_right_Ky.setFont(font2)
        self.lineEdit_right_Ky.setStyleSheet(u"")
        self.lineEdit_right_Ky.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_right_Ky, 4, 3, 1, 1)

        self.lineEdit_left_Ky = QLineEdit(self.frame_8)
        self.lineEdit_left_Ky.setObjectName(u"lineEdit_left_Ky")
        self.lineEdit_left_Ky.setMinimumSize(QSize(120, 26))
        self.lineEdit_left_Ky.setMaximumSize(QSize(120, 26))
        self.lineEdit_left_Ky.setFont(font2)
        self.lineEdit_left_Ky.setStyleSheet(u"")
        self.lineEdit_left_Ky.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_left_Ky, 4, 2, 1, 1)

        self.label_unit_Kx = QLabel(self.frame_8)
        self.label_unit_Kx.setObjectName(u"label_unit_Kx")
        self.label_unit_Kx.setMinimumSize(QSize(80, 26))
        self.label_unit_Kx.setMaximumSize(QSize(80, 26))
        self.label_unit_Kx.setFont(font2)
        self.label_unit_Kx.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_unit_Kx, 3, 4, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 3, 5, 1, 1)

        self.lineEdit_left_Kx = QLineEdit(self.frame_8)
        self.lineEdit_left_Kx.setObjectName(u"lineEdit_left_Kx")
        self.lineEdit_left_Kx.setMinimumSize(QSize(120, 26))
        self.lineEdit_left_Kx.setMaximumSize(QSize(120, 26))
        self.lineEdit_left_Kx.setFont(font2)
        self.lineEdit_left_Kx.setStyleSheet(u"")
        self.lineEdit_left_Kx.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_left_Kx, 3, 2, 1, 1)

        self.label_dtype_left = QLabel(self.frame_8)
        self.label_dtype_left.setObjectName(u"label_dtype_left")
        self.label_dtype_left.setMinimumSize(QSize(80, 26))
        self.label_dtype_left.setMaximumSize(QSize(16777215, 26))
        self.label_dtype_left.setFont(font2)
        self.label_dtype_left.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_dtype_left, 2, 2, 1, 1)

        self.lineEdit_right_Kx = QLineEdit(self.frame_8)
        self.lineEdit_right_Kx.setObjectName(u"lineEdit_right_Kx")
        self.lineEdit_right_Kx.setMinimumSize(QSize(120, 26))
        self.lineEdit_right_Kx.setMaximumSize(QSize(120, 26))
        self.lineEdit_right_Kx.setFont(font2)
        self.lineEdit_right_Kx.setStyleSheet(u"")
        self.lineEdit_right_Kx.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_right_Kx, 3, 3, 1, 1)

        self.label_unit_Kz = QLabel(self.frame_8)
        self.label_unit_Kz.setObjectName(u"label_unit_Kz")
        self.label_unit_Kz.setMinimumSize(QSize(80, 26))
        self.label_unit_Kz.setMaximumSize(QSize(80, 26))
        self.label_unit_Kz.setFont(font2)
        self.label_unit_Kz.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_unit_Kz, 5, 4, 1, 1)

        self.label_unit_Ky = QLabel(self.frame_8)
        self.label_unit_Ky.setObjectName(u"label_unit_Ky")
        self.label_unit_Ky.setMinimumSize(QSize(80, 26))
        self.label_unit_Ky.setMaximumSize(QSize(80, 26))
        self.label_unit_Ky.setFont(font2)
        self.label_unit_Ky.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_unit_Ky, 4, 4, 1, 1)

        self.label_dtype_right = QLabel(self.frame_8)
        self.label_dtype_right.setObjectName(u"label_dtype_right")
        self.label_dtype_right.setMinimumSize(QSize(80, 26))
        self.label_dtype_right.setMaximumSize(QSize(16777215, 26))
        self.label_dtype_right.setFont(font2)
        self.label_dtype_right.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_dtype_right, 2, 3, 1, 1)

        self.lineEdit_left_Kz = QLineEdit(self.frame_8)
        self.lineEdit_left_Kz.setObjectName(u"lineEdit_left_Kz")
        self.lineEdit_left_Kz.setMinimumSize(QSize(120, 26))
        self.lineEdit_left_Kz.setMaximumSize(QSize(120, 26))
        self.lineEdit_left_Kz.setFont(font2)
        self.lineEdit_left_Kz.setStyleSheet(u"")
        self.lineEdit_left_Kz.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_left_Kz, 5, 2, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 3, 0, 1, 1)

        self.label_constant_Ky = QLabel(self.frame_8)
        self.label_constant_Ky.setObjectName(u"label_constant_Ky")
        self.label_constant_Ky.setMinimumSize(QSize(60, 26))
        self.label_constant_Ky.setMaximumSize(QSize(60, 26))
        self.label_constant_Ky.setFont(font2)
        self.label_constant_Ky.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_constant_Ky, 4, 1, 1, 1)

        self.label_constant_Kz = QLabel(self.frame_8)
        self.label_constant_Kz.setObjectName(u"label_constant_Kz")
        self.label_constant_Kz.setMinimumSize(QSize(60, 26))
        self.label_constant_Kz.setMaximumSize(QSize(60, 26))
        self.label_constant_Kz.setFont(font2)
        self.label_constant_Kz.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_constant_Kz, 5, 1, 1, 1)

        self.lineEdit_right_Kz = QLineEdit(self.frame_8)
        self.lineEdit_right_Kz.setObjectName(u"lineEdit_right_Kz")
        self.lineEdit_right_Kz.setMinimumSize(QSize(120, 26))
        self.lineEdit_right_Kz.setMaximumSize(QSize(120, 26))
        self.lineEdit_right_Kz.setFont(font2)
        self.lineEdit_right_Kz.setStyleSheet(u"")
        self.lineEdit_right_Kz.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_right_Kz, 5, 3, 1, 1)

        self.label_constant_Kx = QLabel(self.frame_8)
        self.label_constant_Kx.setObjectName(u"label_constant_Kx")
        self.label_constant_Kx.setMinimumSize(QSize(60, 26))
        self.label_constant_Kx.setMaximumSize(QSize(60, 26))
        self.label_constant_Kx.setFont(font2)
        self.label_constant_Kx.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_constant_Kx, 3, 1, 1, 1)


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
        self.lineEdit_path_table_Ky = QLineEdit(self.frame_9)
        self.lineEdit_path_table_Ky.setObjectName(u"lineEdit_path_table_Ky")
        self.lineEdit_path_table_Ky.setEnabled(False)
        self.lineEdit_path_table_Ky.setMinimumSize(QSize(320, 26))
        self.lineEdit_path_table_Ky.setMaximumSize(QSize(320, 26))
        self.lineEdit_path_table_Ky.setStyleSheet(u"")
        self.lineEdit_path_table_Ky.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.lineEdit_path_table_Ky, 2, 2, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_3, 1, 4, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_4, 1, 0, 1, 1)

        self.pushButton_load_Kz_table = QPushButton(self.frame_9)
        self.pushButton_load_Kz_table.setObjectName(u"pushButton_load_Kz_table")
        self.pushButton_load_Kz_table.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton_load_Kz_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_Kz_table.setSizePolicy(sizePolicy1)
        self.pushButton_load_Kz_table.setMinimumSize(QSize(40, 26))
        self.pushButton_load_Kz_table.setMaximumSize(QSize(40, 26))
        self.pushButton_load_Kz_table.setFont(font1)
        self.pushButton_load_Kz_table.setStyleSheet(u"")
        icon = Icon(u":/icons/document_search_blue.png")
        self.pushButton_load_Kz_table.setIcon(icon)
        self.pushButton_load_Kz_table.setIconSize(QSize(20, 20))
        self.pushButton_load_Kz_table.setAutoDefault(False)

        self.gridLayout_3.addWidget(self.pushButton_load_Kz_table, 3, 3, 1, 1)

        self.pushButton_load_Kx_table = QPushButton(self.frame_9)
        self.pushButton_load_Kx_table.setObjectName(u"pushButton_load_Kx_table")
        self.pushButton_load_Kx_table.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.pushButton_load_Kx_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_Kx_table.setSizePolicy(sizePolicy1)
        self.pushButton_load_Kx_table.setMinimumSize(QSize(40, 26))
        self.pushButton_load_Kx_table.setMaximumSize(QSize(40, 26))
        self.pushButton_load_Kx_table.setFont(font1)
        self.pushButton_load_Kx_table.setStyleSheet(u"")
        self.pushButton_load_Kx_table.setIcon(icon)
        self.pushButton_load_Kx_table.setIconSize(QSize(20, 20))
        self.pushButton_load_Kx_table.setAutoDefault(False)

        self.gridLayout_3.addWidget(self.pushButton_load_Kx_table, 1, 3, 1, 1)

        self.label_table_Ky = QLabel(self.frame_9)
        self.label_table_Ky.setObjectName(u"label_table_Ky")
        self.label_table_Ky.setEnabled(True)
        self.label_table_Ky.setMinimumSize(QSize(0, 26))
        self.label_table_Ky.setMaximumSize(QSize(80, 26))
        self.label_table_Ky.setFont(font1)
        self.label_table_Ky.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_table_Ky, 2, 1, 1, 1)

        self.lineEdit_path_table_Kz = QLineEdit(self.frame_9)
        self.lineEdit_path_table_Kz.setObjectName(u"lineEdit_path_table_Kz")
        self.lineEdit_path_table_Kz.setEnabled(False)
        self.lineEdit_path_table_Kz.setMinimumSize(QSize(320, 26))
        self.lineEdit_path_table_Kz.setMaximumSize(QSize(320, 26))
        self.lineEdit_path_table_Kz.setStyleSheet(u"")
        self.lineEdit_path_table_Kz.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.lineEdit_path_table_Kz, 3, 2, 1, 1)

        self.label_table_Kx = QLabel(self.frame_9)
        self.label_table_Kx.setObjectName(u"label_table_Kx")
        self.label_table_Kx.setEnabled(True)
        self.label_table_Kx.setMinimumSize(QSize(0, 26))
        self.label_table_Kx.setMaximumSize(QSize(80, 26))
        self.label_table_Kx.setFont(font1)
        self.label_table_Kx.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_table_Kx, 1, 1, 1, 1)

        self.lineEdit_path_table_Kx = QLineEdit(self.frame_9)
        self.lineEdit_path_table_Kx.setObjectName(u"lineEdit_path_table_Kx")
        self.lineEdit_path_table_Kx.setEnabled(False)
        self.lineEdit_path_table_Kx.setMinimumSize(QSize(320, 26))
        self.lineEdit_path_table_Kx.setMaximumSize(QSize(320, 26))
        self.lineEdit_path_table_Kx.setStyleSheet(u"")
        self.lineEdit_path_table_Kx.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.lineEdit_path_table_Kx, 1, 2, 1, 1)

        self.pushButton_load_Ky_table = QPushButton(self.frame_9)
        self.pushButton_load_Ky_table.setObjectName(u"pushButton_load_Ky_table")
        self.pushButton_load_Ky_table.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.pushButton_load_Ky_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_Ky_table.setSizePolicy(sizePolicy1)
        self.pushButton_load_Ky_table.setMinimumSize(QSize(40, 26))
        self.pushButton_load_Ky_table.setMaximumSize(QSize(40, 26))
        self.pushButton_load_Ky_table.setFont(font1)
        self.pushButton_load_Ky_table.setStyleSheet(u"")
        self.pushButton_load_Ky_table.setIcon(icon)
        self.pushButton_load_Ky_table.setIconSize(QSize(20, 20))
        self.pushButton_load_Ky_table.setAutoDefault(False)

        self.gridLayout_3.addWidget(self.pushButton_load_Ky_table, 2, 3, 1, 1)

        self.label_table_Kz = QLabel(self.frame_9)
        self.label_table_Kz.setObjectName(u"label_table_Kz")
        self.label_table_Kz.setEnabled(True)
        self.label_table_Kz.setMinimumSize(QSize(0, 26))
        self.label_table_Kz.setMaximumSize(QSize(80, 26))
        self.label_table_Kz.setFont(font1)
        self.label_table_Kz.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_table_Kz, 3, 1, 1, 1)


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
        self.treeWidget_distributed_stiffness = QTreeWidget(self.frame_5)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(3, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(2, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter);
        self.treeWidget_distributed_stiffness.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_distributed_stiffness.setObjectName(u"treeWidget_distributed_stiffness")
        self.treeWidget_distributed_stiffness.setMinimumSize(QSize(320, 0))
        self.treeWidget_distributed_stiffness.setMaximumSize(QSize(16777215, 16777215))
        self.treeWidget_distributed_stiffness.setFont(font2)
        self.treeWidget_distributed_stiffness.setIndentation(1)
        self.treeWidget_distributed_stiffness.setHeaderHidden(False)
        self.treeWidget_distributed_stiffness.header().setHighlightSections(False)
        self.treeWidget_distributed_stiffness.header().setProperty(u"showSortIndicator", False)
        self.treeWidget_distributed_stiffness.header().setStretchLastSection(True)

        self.gridLayout_2.addWidget(self.treeWidget_distributed_stiffness, 0, 0, 1, 1)


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
        QWidget.setTabOrder(self.tabWidget_main, self.lineEdit_left_Kx)
        QWidget.setTabOrder(self.lineEdit_left_Kx, self.lineEdit_left_Ky)
        QWidget.setTabOrder(self.lineEdit_left_Ky, self.lineEdit_left_Kz)
        QWidget.setTabOrder(self.lineEdit_left_Kz, self.lineEdit_right_Kx)
        QWidget.setTabOrder(self.lineEdit_right_Kx, self.lineEdit_right_Ky)
        QWidget.setTabOrder(self.lineEdit_right_Ky, self.lineEdit_right_Kz)
        QWidget.setTabOrder(self.lineEdit_right_Kz, self.pushButton_apply_and_close)
        QWidget.setTabOrder(self.pushButton_apply_and_close, self.pushButton_apply)
        QWidget.setTabOrder(self.pushButton_apply, self.pushButton_cancel)
        QWidget.setTabOrder(self.pushButton_cancel, self.lineEdit_path_table_Kx)
        QWidget.setTabOrder(self.lineEdit_path_table_Kx, self.pushButton_load_Kx_table)
        QWidget.setTabOrder(self.pushButton_load_Kx_table, self.lineEdit_path_table_Ky)
        QWidget.setTabOrder(self.lineEdit_path_table_Ky, self.pushButton_load_Ky_table)
        QWidget.setTabOrder(self.pushButton_load_Ky_table, self.lineEdit_path_table_Kz)
        QWidget.setTabOrder(self.lineEdit_path_table_Kz, self.pushButton_load_Kz_table)
        QWidget.setTabOrder(self.pushButton_load_Kz_table, self.treeWidget_distributed_stiffness)
        QWidget.setTabOrder(self.treeWidget_distributed_stiffness, self.pushButton_remove)
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
        self.comboBox_direction_control.setItemText(0, QCoreApplication.translate("Dialog", u"By components", None))
        self.comboBox_direction_control.setItemText(1, QCoreApplication.translate("Dialog", u"By normal", None))

        self.label_3.setText(QCoreApplication.translate("Dialog", u"Element type:", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"Data type:", None))
        self.comboBox_assignment_type.setItemText(0, QCoreApplication.translate("Dialog", u"Selected faces", None))
        self.comboBox_assignment_type.setItemText(1, QCoreApplication.translate("Dialog", u"Selected lines", None))

        self.label_2.setText(QCoreApplication.translate("Dialog", u"Selection ID:", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"Direction control:", None))
        self.comboBox_element_type.setItemText(0, QCoreApplication.translate("Dialog", u"Face element", None))
        self.comboBox_element_type.setItemText(1, QCoreApplication.translate("Dialog", u"Solid element", None))

        self.comboBox_data_type.setItemText(0, QCoreApplication.translate("Dialog", u"Real and imaginary", None))
        self.comboBox_data_type.setItemText(1, QCoreApplication.translate("Dialog", u"Magnitude and phase", None))

        self.label_9.setText(QCoreApplication.translate("Dialog", u"Stiffness input:", None))
        self.comboBox_stiffness_input.setItemText(0, QCoreApplication.translate("Dialog", u"Direct", None))
        self.comboBox_stiffness_input.setItemText(1, QCoreApplication.translate("Dialog", u"Densities (K/A)", None))

        self.label_unit_Kx.setText(QCoreApplication.translate("Dialog", u"[N/m]", None))
        self.lineEdit_left_Kx.setText("")
        self.label_dtype_left.setText(QCoreApplication.translate("Dialog", u"Real", None))
        self.label_unit_Kz.setText(QCoreApplication.translate("Dialog", u"[N/m]", None))
        self.label_unit_Ky.setText(QCoreApplication.translate("Dialog", u"[N/m]", None))
        self.label_dtype_right.setText(QCoreApplication.translate("Dialog", u"Imaginary", None))
        self.label_constant_Ky.setText(QCoreApplication.translate("Dialog", u"Ky:", None))
        self.label_constant_Kz.setText(QCoreApplication.translate("Dialog", u"Kz:", None))
        self.label_constant_Kx.setText(QCoreApplication.translate("Dialog", u"Kx:", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_constant_data), QCoreApplication.translate("Dialog", u"Constant data", None))
        self.pushButton_load_Kz_table.setText("")
        self.pushButton_load_Kx_table.setText("")
        self.label_table_Ky.setText(QCoreApplication.translate("Dialog", u"Ky:", None))
        self.label_table_Kx.setText(QCoreApplication.translate("Dialog", u"Kx:", None))
        self.pushButton_load_Ky_table.setText("")
        self.label_table_Kz.setText(QCoreApplication.translate("Dialog", u"Kz:", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_tabular_data), QCoreApplication.translate("Dialog", u"Tabular data", None))
        ___qtreewidgetitem = self.treeWidget_distributed_stiffness.headerItem()
        ___qtreewidgetitem.setText(3, QCoreApplication.translate("Dialog", u"Label", None));
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("Dialog", u"Element type", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"Entity", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"ID", None));
#if QT_CONFIG(tooltip)
        self.treeWidget_distributed_stiffness.setToolTip(QCoreApplication.translate("Dialog", u"Select a node to remove the attributed boundary condition.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_reset.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.pushButton_remove.setText(QCoreApplication.translate("Dialog", u"Remove", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_list), QCoreApplication.translate("Dialog", u"List", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Set distributed stiffness", None))
        self.pushButton_apply_and_close.setText(QCoreApplication.translate("Dialog", u"Ok", None))
        self.pushButton_apply.setText(QCoreApplication.translate("Dialog", u"Apply", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
    # retranslateUi



class DistributedStiffnessInputs_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame_2: QFrame
                    - (Layout): QGridLayout
                            - frame_4: QFrame
                                - (Layout): QGridLayout
                                        - comboBox_direction_control: QComboBox
                                        - label_3: QLabel
                                        - label_7: QLabel
                                        - comboBox_assignment_type: QComboBox
                                        - label_2: QLabel
                                        - lineEdit_selection_id: QLineEdit
                                        - label_8: QLabel
                                        - comboBox_element_type: QComboBox
                                        - comboBox_data_type: QComboBox
                                        - label_9: QLabel
                                        - comboBox_stiffness_input: QComboBox
                            - frame_6: QFrame
                                - (Layout): QGridLayout
                                        - tabWidget_main: QTabWidget
                                            - tab_constant_data: QWidget
                                                - (Layout): QGridLayout
                                                        - frame_8: QFrame
                                                            - (Layout): QGridLayout
                                                                    - lineEdit_right_Ky: QLineEdit
                                                                    - lineEdit_left_Ky: QLineEdit
                                                                    - label_unit_Kx: QLabel
                                                                    - lineEdit_left_Kx: QLineEdit
                                                                    - label_dtype_left: QLabel
                                                                    - lineEdit_right_Kx: QLineEdit
                                                                    - label_unit_Kz: QLabel
                                                                    - label_unit_Ky: QLabel
                                                                    - label_dtype_right: QLabel
                                                                    - lineEdit_left_Kz: QLineEdit
                                                                    - label_constant_Ky: QLabel
                                                                    - label_constant_Kz: QLabel
                                                                    - lineEdit_right_Kz: QLineEdit
                                                                    - label_constant_Kx: QLabel
                                            - tab_tabular_data: QWidget
                                                - (Layout): QGridLayout
                                                        - frame_9: QFrame
                                                            - (Layout): QGridLayout
                                                                    - lineEdit_path_table_Ky: QLineEdit
                                                                    - pushButton_load_Kz_table: QPushButton
                                                                    - pushButton_load_Kx_table: QPushButton
                                                                    - label_table_Ky: QLabel
                                                                    - lineEdit_path_table_Kz: QLineEdit
                                                                    - label_table_Kx: QLabel
                                                                    - lineEdit_path_table_Kx: QLineEdit
                                                                    - pushButton_load_Ky_table: QPushButton
                                                                    - label_table_Kz: QLabel
                                            - tab_list: QWidget
                                                - (Layout): QGridLayout
                                                        - frame_5: QFrame
                                                            - (Layout): QGridLayout
                                                                    - treeWidget_distributed_stiffness: QTreeWidget
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
