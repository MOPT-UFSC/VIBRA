# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'distributed_loads_input.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFrame,
    QGridLayout, QHeaderView, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QTabWidget,
    QTreeWidget, QTreeWidgetItem, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setWindowModality(Qt.WindowModal)
        Dialog.resize(460, 440)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(460, 420))
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
        self.tab_constant_values = QWidget()
        self.tab_constant_values.setObjectName(u"tab_constant_values")
        self.gridLayout_12 = QGridLayout(self.tab_constant_values)
        self.gridLayout_12.setSpacing(2)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setContentsMargins(2, 2, 2, 2)
        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_12.addItem(self.verticalSpacer_2, 3, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_12.addItem(self.verticalSpacer, 0, 0, 1, 1)

        self.frame_8 = QFrame(self.tab_constant_values)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setMinimumSize(QSize(340, 0))
        self.frame_8.setMaximumSize(QSize(16777215, 320))
        font4 = QFont()
        font4.setPointSize(11)
        self.frame_8.setFont(font4)
        self.frame_8.setFrameShape(QFrame.NoFrame)
        self.frame_8.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame_8)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(8)
        self.gridLayout.setVerticalSpacing(6)
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.lineEdit_real_Fx = QLineEdit(self.frame_8)
        self.lineEdit_real_Fx.setObjectName(u"lineEdit_real_Fx")
        self.lineEdit_real_Fx.setMinimumSize(QSize(80, 26))
        self.lineEdit_real_Fx.setMaximumSize(QSize(80, 26))
        self.lineEdit_real_Fx.setFont(font2)
        self.lineEdit_real_Fx.setStyleSheet(u"")
        self.lineEdit_real_Fx.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_real_Fx, 3, 2, 1, 1)

        self.lineEdit_imag_Fx = QLineEdit(self.frame_8)
        self.lineEdit_imag_Fx.setObjectName(u"lineEdit_imag_Fx")
        self.lineEdit_imag_Fx.setMinimumSize(QSize(80, 26))
        self.lineEdit_imag_Fx.setMaximumSize(QSize(80, 26))
        self.lineEdit_imag_Fx.setFont(font2)
        self.lineEdit_imag_Fx.setStyleSheet(u"")
        self.lineEdit_imag_Fx.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_imag_Fx, 3, 3, 1, 1)

        self.label_20 = QLabel(self.frame_8)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setMinimumSize(QSize(80, 26))
        self.label_20.setMaximumSize(QSize(80, 26))
        self.label_20.setFont(font2)
        self.label_20.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_20, 2, 3, 1, 1)

        self.label_4 = QLabel(self.frame_8)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(80, 26))
        self.label_4.setMaximumSize(QSize(80, 26))
        self.label_4.setFont(font2)
        self.label_4.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_4, 2, 2, 1, 1)

        self.label_constant_Fx = QLabel(self.frame_8)
        self.label_constant_Fx.setObjectName(u"label_constant_Fx")
        self.label_constant_Fx.setMinimumSize(QSize(70, 26))
        self.label_constant_Fx.setMaximumSize(QSize(100, 26))
        self.label_constant_Fx.setFont(font2)
        self.label_constant_Fx.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_constant_Fx, 3, 1, 1, 1)

        self.label_unit_Fx = QLabel(self.frame_8)
        self.label_unit_Fx.setObjectName(u"label_unit_Fx")
        self.label_unit_Fx.setMinimumSize(QSize(50, 26))
        self.label_unit_Fx.setMaximumSize(QSize(50, 26))
        self.label_unit_Fx.setFont(font2)
        self.label_unit_Fx.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_unit_Fx, 3, 4, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 3, 5, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 3, 0, 1, 1)

        self.lineEdit_real_Fy = QLineEdit(self.frame_8)
        self.lineEdit_real_Fy.setObjectName(u"lineEdit_real_Fy")
        self.lineEdit_real_Fy.setMinimumSize(QSize(80, 26))
        self.lineEdit_real_Fy.setMaximumSize(QSize(80, 26))
        self.lineEdit_real_Fy.setFont(font2)
        self.lineEdit_real_Fy.setStyleSheet(u"")
        self.lineEdit_real_Fy.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_real_Fy, 4, 2, 1, 1)

        self.label_unit_Fy = QLabel(self.frame_8)
        self.label_unit_Fy.setObjectName(u"label_unit_Fy")
        self.label_unit_Fy.setMinimumSize(QSize(50, 26))
        self.label_unit_Fy.setMaximumSize(QSize(50, 26))
        self.label_unit_Fy.setFont(font2)
        self.label_unit_Fy.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_unit_Fy, 4, 4, 1, 1)

        self.lineEdit_imag_Fy = QLineEdit(self.frame_8)
        self.lineEdit_imag_Fy.setObjectName(u"lineEdit_imag_Fy")
        self.lineEdit_imag_Fy.setMinimumSize(QSize(80, 26))
        self.lineEdit_imag_Fy.setMaximumSize(QSize(80, 26))
        self.lineEdit_imag_Fy.setFont(font2)
        self.lineEdit_imag_Fy.setStyleSheet(u"")
        self.lineEdit_imag_Fy.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_imag_Fy, 4, 3, 1, 1)

        self.lineEdit_real_Fz = QLineEdit(self.frame_8)
        self.lineEdit_real_Fz.setObjectName(u"lineEdit_real_Fz")
        self.lineEdit_real_Fz.setMinimumSize(QSize(80, 26))
        self.lineEdit_real_Fz.setMaximumSize(QSize(80, 26))
        self.lineEdit_real_Fz.setFont(font2)
        self.lineEdit_real_Fz.setStyleSheet(u"")
        self.lineEdit_real_Fz.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_real_Fz, 5, 2, 1, 1)

        self.lineEdit_imag_Fz = QLineEdit(self.frame_8)
        self.lineEdit_imag_Fz.setObjectName(u"lineEdit_imag_Fz")
        self.lineEdit_imag_Fz.setMinimumSize(QSize(80, 26))
        self.lineEdit_imag_Fz.setMaximumSize(QSize(80, 26))
        self.lineEdit_imag_Fz.setFont(font2)
        self.lineEdit_imag_Fz.setStyleSheet(u"")
        self.lineEdit_imag_Fz.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_imag_Fz, 5, 3, 1, 1)

        self.label_unit_Fz = QLabel(self.frame_8)
        self.label_unit_Fz.setObjectName(u"label_unit_Fz")
        self.label_unit_Fz.setMinimumSize(QSize(50, 26))
        self.label_unit_Fz.setMaximumSize(QSize(50, 26))
        self.label_unit_Fz.setFont(font2)
        self.label_unit_Fz.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_unit_Fz, 5, 4, 1, 1)

        self.label_constant_Fy = QLabel(self.frame_8)
        self.label_constant_Fy.setObjectName(u"label_constant_Fy")
        self.label_constant_Fy.setMinimumSize(QSize(70, 26))
        self.label_constant_Fy.setMaximumSize(QSize(100, 26))
        self.label_constant_Fy.setFont(font2)
        self.label_constant_Fy.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_constant_Fy, 4, 1, 1, 1)

        self.label_constant_Fz = QLabel(self.frame_8)
        self.label_constant_Fz.setObjectName(u"label_constant_Fz")
        self.label_constant_Fz.setMinimumSize(QSize(70, 26))
        self.label_constant_Fz.setMaximumSize(QSize(100, 26))
        self.label_constant_Fz.setFont(font2)
        self.label_constant_Fz.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_constant_Fz, 5, 1, 1, 1)


        self.gridLayout_12.addWidget(self.frame_8, 1, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_constant_values, "")
        self.tab_load_tables = QWidget()
        self.tab_load_tables.setObjectName(u"tab_load_tables")
        self.gridLayout_10 = QGridLayout(self.tab_load_tables)
        self.gridLayout_10.setSpacing(2)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(2, 2, 2, 2)
        self.frame_9 = QFrame(self.tab_load_tables)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setFrameShape(QFrame.NoFrame)
        self.frame_9.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_9)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setHorizontalSpacing(4)
        self.gridLayout_3.setVerticalSpacing(7)
        self.gridLayout_3.setContentsMargins(4, 4, 4, 2)
        self.lineEdit_path_table_Fx = QLineEdit(self.frame_9)
        self.lineEdit_path_table_Fx.setObjectName(u"lineEdit_path_table_Fx")
        self.lineEdit_path_table_Fx.setEnabled(False)
        self.lineEdit_path_table_Fx.setMinimumSize(QSize(210, 26))
        self.lineEdit_path_table_Fx.setMaximumSize(QSize(240, 26))
        self.lineEdit_path_table_Fx.setStyleSheet(u"")
        self.lineEdit_path_table_Fx.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.lineEdit_path_table_Fx, 0, 1, 1, 1)

        self.label_table_Fx = QLabel(self.frame_9)
        self.label_table_Fx.setObjectName(u"label_table_Fx")
        self.label_table_Fx.setEnabled(True)
        self.label_table_Fx.setMinimumSize(QSize(0, 26))
        self.label_table_Fx.setMaximumSize(QSize(80, 26))
        self.label_table_Fx.setFont(font3)
        self.label_table_Fx.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_table_Fx, 0, 0, 1, 1)

        self.pushButton_load_Fx_table = QPushButton(self.frame_9)
        self.pushButton_load_Fx_table.setObjectName(u"pushButton_load_Fx_table")
        self.pushButton_load_Fx_table.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton_load_Fx_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_Fx_table.setSizePolicy(sizePolicy1)
        self.pushButton_load_Fx_table.setMinimumSize(QSize(62, 26))
        self.pushButton_load_Fx_table.setMaximumSize(QSize(62, 26))
        self.pushButton_load_Fx_table.setFont(font3)
        self.pushButton_load_Fx_table.setStyleSheet(u"")

        self.gridLayout_3.addWidget(self.pushButton_load_Fx_table, 0, 2, 1, 1)

        self.label_table_Fy = QLabel(self.frame_9)
        self.label_table_Fy.setObjectName(u"label_table_Fy")
        self.label_table_Fy.setEnabled(True)
        self.label_table_Fy.setMinimumSize(QSize(0, 26))
        self.label_table_Fy.setMaximumSize(QSize(80, 26))
        self.label_table_Fy.setFont(font3)
        self.label_table_Fy.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_table_Fy, 1, 0, 1, 1)

        self.label_table_Fz = QLabel(self.frame_9)
        self.label_table_Fz.setObjectName(u"label_table_Fz")
        self.label_table_Fz.setEnabled(True)
        self.label_table_Fz.setMinimumSize(QSize(0, 26))
        self.label_table_Fz.setMaximumSize(QSize(80, 26))
        self.label_table_Fz.setFont(font3)
        self.label_table_Fz.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_table_Fz, 2, 0, 1, 1)

        self.lineEdit_path_table_Fy = QLineEdit(self.frame_9)
        self.lineEdit_path_table_Fy.setObjectName(u"lineEdit_path_table_Fy")
        self.lineEdit_path_table_Fy.setEnabled(False)
        self.lineEdit_path_table_Fy.setMinimumSize(QSize(210, 26))
        self.lineEdit_path_table_Fy.setMaximumSize(QSize(240, 26))
        self.lineEdit_path_table_Fy.setStyleSheet(u"")
        self.lineEdit_path_table_Fy.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.lineEdit_path_table_Fy, 1, 1, 1, 1)

        self.lineEdit_path_table_Fz = QLineEdit(self.frame_9)
        self.lineEdit_path_table_Fz.setObjectName(u"lineEdit_path_table_Fz")
        self.lineEdit_path_table_Fz.setEnabled(False)
        self.lineEdit_path_table_Fz.setMinimumSize(QSize(210, 26))
        self.lineEdit_path_table_Fz.setMaximumSize(QSize(240, 26))
        self.lineEdit_path_table_Fz.setStyleSheet(u"")
        self.lineEdit_path_table_Fz.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.lineEdit_path_table_Fz, 2, 1, 1, 1)

        self.pushButton_load_Fy_table = QPushButton(self.frame_9)
        self.pushButton_load_Fy_table.setObjectName(u"pushButton_load_Fy_table")
        self.pushButton_load_Fy_table.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.pushButton_load_Fy_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_Fy_table.setSizePolicy(sizePolicy1)
        self.pushButton_load_Fy_table.setMinimumSize(QSize(62, 26))
        self.pushButton_load_Fy_table.setMaximumSize(QSize(62, 26))
        self.pushButton_load_Fy_table.setFont(font3)
        self.pushButton_load_Fy_table.setStyleSheet(u"")

        self.gridLayout_3.addWidget(self.pushButton_load_Fy_table, 1, 2, 1, 1)

        self.pushButton_load_Fz_table = QPushButton(self.frame_9)
        self.pushButton_load_Fz_table.setObjectName(u"pushButton_load_Fz_table")
        self.pushButton_load_Fz_table.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.pushButton_load_Fz_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_Fz_table.setSizePolicy(sizePolicy1)
        self.pushButton_load_Fz_table.setMinimumSize(QSize(62, 26))
        self.pushButton_load_Fz_table.setMaximumSize(QSize(62, 26))
        self.pushButton_load_Fz_table.setFont(font3)
        self.pushButton_load_Fz_table.setStyleSheet(u"")

        self.gridLayout_3.addWidget(self.pushButton_load_Fz_table, 2, 2, 1, 1)


        self.gridLayout_10.addWidget(self.frame_9, 1, 0, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_10.addItem(self.verticalSpacer_4, 0, 0, 1, 1)

        self.verticalSpacer_8 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_10.addItem(self.verticalSpacer_8, 3, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_load_tables, "")
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
        self.treeWidget_distributed_loads = QTreeWidget(self.frame_5)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(2, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter);
        self.treeWidget_distributed_loads.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_distributed_loads.setObjectName(u"treeWidget_distributed_loads")
        self.treeWidget_distributed_loads.setMinimumSize(QSize(320, 0))
        self.treeWidget_distributed_loads.setMaximumSize(QSize(380, 200))
        font5 = QFont()
        font5.setFamilies([u"MS Shell Dlg 2"])
        font5.setPointSize(10)
        font5.setItalic(False)
        self.treeWidget_distributed_loads.setFont(font5)
        self.treeWidget_distributed_loads.setIndentation(1)
        self.treeWidget_distributed_loads.setHeaderHidden(False)
        self.treeWidget_distributed_loads.header().setHighlightSections(False)
        self.treeWidget_distributed_loads.header().setProperty(u"showSortIndicator", False)
        self.treeWidget_distributed_loads.header().setStretchLastSection(True)

        self.gridLayout_2.addWidget(self.treeWidget_distributed_loads, 0, 0, 1, 1)


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

        self.gridLayout_8.addWidget(self.pushButton_reset, 0, 0, 1, 1)

        self.pushButton_remove = QPushButton(self.frame_3)
        self.pushButton_remove.setObjectName(u"pushButton_remove")
        self.pushButton_remove.setMinimumSize(QSize(100, 28))
        self.pushButton_remove.setMaximumSize(QSize(100, 28))
        self.pushButton_remove.setFont(font2)
        self.pushButton_remove.setStyleSheet(u"")

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
        self.pushButton_attribute.setDefault(True)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Set distributed loads", None))
#if QT_CONFIG(whatsthis)
        Dialog.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.label.setText(QCoreApplication.translate("Dialog", u"Set distributed loads", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Selection ID:", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Element type:", None))
        self.comboBox_element_type.setItemText(0, QCoreApplication.translate("Dialog", u" Face element", None))
        self.comboBox_element_type.setItemText(1, QCoreApplication.translate("Dialog", u" Solid element", None))

        self.comboBox_attribution_type.setItemText(0, QCoreApplication.translate("Dialog", u"Selected faces", None))
        self.comboBox_attribution_type.setItemText(1, QCoreApplication.translate("Dialog", u"Selected lines", None))

        self.lineEdit_real_Fx.setText("")
        self.label_20.setText(QCoreApplication.translate("Dialog", u"Imaginary", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Real", None))
        self.label_constant_Fx.setText(QCoreApplication.translate("Dialog", u"Fx / area:", None))
        self.label_unit_Fx.setText(QCoreApplication.translate("Dialog", u"[N/m\u00b2]", None))
        self.lineEdit_real_Fy.setText("")
        self.label_unit_Fy.setText(QCoreApplication.translate("Dialog", u"[N/m\u00b2]", None))
        self.lineEdit_real_Fz.setText("")
        self.label_unit_Fz.setText(QCoreApplication.translate("Dialog", u"[N/m\u00b2]", None))
        self.label_constant_Fy.setText(QCoreApplication.translate("Dialog", u"Fy / area:", None))
        self.label_constant_Fz.setText(QCoreApplication.translate("Dialog", u"Fz / area:", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_constant_values), QCoreApplication.translate("Dialog", u"Constant values", None))
        self.label_table_Fx.setText(QCoreApplication.translate("Dialog", u"Fx / A:", None))
        self.pushButton_load_Fx_table.setText(QCoreApplication.translate("Dialog", u"Search", None))
        self.label_table_Fy.setText(QCoreApplication.translate("Dialog", u"Fy / A:", None))
        self.label_table_Fz.setText(QCoreApplication.translate("Dialog", u"Fz / A:", None))
        self.pushButton_load_Fy_table.setText(QCoreApplication.translate("Dialog", u"Search", None))
        self.pushButton_load_Fz_table.setText(QCoreApplication.translate("Dialog", u"Search", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_load_tables), QCoreApplication.translate("Dialog", u"Load tables", None))
        ___qtreewidgetitem = self.treeWidget_distributed_loads.headerItem()
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("Dialog", u"Pressure load", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"Selection type", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"ID", None));
#if QT_CONFIG(tooltip)
        self.treeWidget_distributed_loads.setToolTip(QCoreApplication.translate("Dialog", u"Select a node to remove the attributed boundary condition.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_reset.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.pushButton_remove.setText(QCoreApplication.translate("Dialog", u"Remove", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_list), QCoreApplication.translate("Dialog", u"List", None))
        self.pushButton_exit.setText(QCoreApplication.translate("Dialog", u"Exit", None))
        self.pushButton_attribute.setText(QCoreApplication.translate("Dialog", u"Attribute", None))
    # retranslateUi



class DistributedLoadsInput_UI(QDialog, Ui_Dialog):
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
                                            - tab_constant_values: QWidget
                                                - (Layout): QGridLayout
                                                        - frame_8: QFrame
                                                            - (Layout): QGridLayout
                                                                    - lineEdit_real_Fx: QLineEdit
                                                                    - lineEdit_imag_Fx: QLineEdit
                                                                    - label_20: QLabel
                                                                    - label_4: QLabel
                                                                    - label_constant_Fx: QLabel
                                                                    - label_unit_Fx: QLabel
                                                                    - lineEdit_real_Fy: QLineEdit
                                                                    - label_unit_Fy: QLabel
                                                                    - lineEdit_imag_Fy: QLineEdit
                                                                    - lineEdit_real_Fz: QLineEdit
                                                                    - lineEdit_imag_Fz: QLineEdit
                                                                    - label_unit_Fz: QLabel
                                                                    - label_constant_Fy: QLabel
                                                                    - label_constant_Fz: QLabel
                                            - tab_load_tables: QWidget
                                                - (Layout): QGridLayout
                                                        - frame_9: QFrame
                                                            - (Layout): QGridLayout
                                                                    - lineEdit_path_table_Fx: QLineEdit
                                                                    - label_table_Fx: QLabel
                                                                    - pushButton_load_Fx_table: QPushButton
                                                                    - label_table_Fy: QLabel
                                                                    - label_table_Fz: QLabel
                                                                    - lineEdit_path_table_Fy: QLineEdit
                                                                    - lineEdit_path_table_Fz: QLineEdit
                                                                    - pushButton_load_Fy_table: QPushButton
                                                                    - pushButton_load_Fz_table: QPushButton
                                            - tab_list: QWidget
                                                - (Layout): QGridLayout
                                                        - frame_5: QFrame
                                                            - (Layout): QGridLayout
                                                                    - treeWidget_distributed_loads: QTreeWidget
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
