# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mesher_setup.ui'
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
    QDoubleSpinBox, QFrame, QGridLayout, QHeaderView,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QTabWidget, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(540, 560)
        Dialog.setMinimumSize(QSize(540, 560))
        Dialog.setMaximumSize(QSize(540, 560))
        self.gridLayout_7 = QGridLayout(Dialog)
        self.gridLayout_7.setSpacing(4)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(4, 4, 4, 4)
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 0))
        self.frame.setMaximumSize(QSize(16777215, 16777215))
        font = QFont()
        font.setPointSize(8)
        self.frame.setFont(font)
        self.frame.setFrameShape(QFrame.Shape.Box)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_6 = QGridLayout(self.frame)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(4, 4, 4, 4)
        self.frame_8 = QFrame(self.frame)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setMaximumSize(QSize(16777215, 150))
        self.frame_8.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_8.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_8)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.label_16 = QLabel(self.frame_8)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setMinimumSize(QSize(0, 20))
        self.label_16.setMaximumSize(QSize(240, 16777215))
        font1 = QFont()
        font1.setPointSize(10)
        self.label_16.setFont(font1)
        self.label_16.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_16, 0, 1, 1, 1)

        self.label_10 = QLabel(self.frame_8)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(0, 20))
        self.label_10.setMaximumSize(QSize(240, 16777215))
        self.label_10.setFont(font1)
        self.label_10.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_10, 1, 1, 1, 1)

        self.frame_13 = QFrame(self.frame_8)
        self.frame_13.setObjectName(u"frame_13")
        self.frame_13.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_13.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_5.addWidget(self.frame_13, 0, 3, 1, 1)

        self.frame_14 = QFrame(self.frame_8)
        self.frame_14.setObjectName(u"frame_14")
        self.frame_14.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_14.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_5.addWidget(self.frame_14, 0, 0, 1, 1)

        self.checkBox_mesh_connection = QCheckBox(self.frame_8)
        self.checkBox_mesh_connection.setObjectName(u"checkBox_mesh_connection")
        self.checkBox_mesh_connection.setMinimumSize(QSize(0, 28))
        self.checkBox_mesh_connection.setFont(font1)
        self.checkBox_mesh_connection.setChecked(True)

        self.gridLayout_5.addWidget(self.checkBox_mesh_connection, 2, 1, 1, 2)

        self.comboBox_element_type = QComboBox(self.frame_8)
        self.comboBox_element_type.addItem("")
        self.comboBox_element_type.addItem("")
        self.comboBox_element_type.setObjectName(u"comboBox_element_type")
        self.comboBox_element_type.setMinimumSize(QSize(0, 28))
        self.comboBox_element_type.setMaximumSize(QSize(120, 16777215))
        self.comboBox_element_type.setFont(font1)

        self.gridLayout_5.addWidget(self.comboBox_element_type, 0, 2, 1, 1)

        self.comboBox_shape_function = QComboBox(self.frame_8)
        self.comboBox_shape_function.addItem("")
        self.comboBox_shape_function.addItem("")
        self.comboBox_shape_function.setObjectName(u"comboBox_shape_function")
        self.comboBox_shape_function.setMinimumSize(QSize(0, 28))
        self.comboBox_shape_function.setMaximumSize(QSize(120, 16777215))
        self.comboBox_shape_function.setFont(font1)

        self.gridLayout_5.addWidget(self.comboBox_shape_function, 1, 2, 1, 1)


        self.gridLayout_6.addWidget(self.frame_8, 0, 1, 1, 1)

        self.tabWidget_main = QTabWidget(self.frame)
        self.tabWidget_main.setObjectName(u"tabWidget_main")
        self.tabWidget_main.setEnabled(True)
        font2 = QFont()
        font2.setPointSize(9)
        self.tabWidget_main.setFont(font2)
        self.tabWidget_main.setTabShape(QTabWidget.TabShape.Rounded)
        self.tabWidget_main.setTabBarAutoHide(False)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.gridLayout_9 = QGridLayout(self.tab)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.tabWidget_global_settings = QTabWidget(self.tab)
        self.tabWidget_global_settings.setObjectName(u"tabWidget_global_settings")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.gridLayout_2 = QGridLayout(self.tab_3)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.frame_2 = QFrame(self.tab_3)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(0, 62))
        self.frame_2.setMaximumSize(QSize(16777215, 150))
        self.frame_2.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_10 = QGridLayout(self.frame_2)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setHorizontalSpacing(6)
        self.gridLayout_10.setContentsMargins(4, 4, 4, 4)
        self.frame_12 = QFrame(self.frame_2)
        self.frame_12.setObjectName(u"frame_12")
        self.frame_12.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_12.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_10.addWidget(self.frame_12, 1, 0, 1, 1)

        self.frame_5 = QFrame(self.frame_2)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_10.addWidget(self.frame_5, 1, 4, 1, 1)

        self.lineEdit_geometry_tolerance = QLineEdit(self.frame_2)
        self.lineEdit_geometry_tolerance.setObjectName(u"lineEdit_geometry_tolerance")
        self.lineEdit_geometry_tolerance.setMinimumSize(QSize(140, 28))
        self.lineEdit_geometry_tolerance.setMaximumSize(QSize(140, 16777215))
        self.lineEdit_geometry_tolerance.setFont(font1)
        self.lineEdit_geometry_tolerance.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_10.addWidget(self.lineEdit_geometry_tolerance, 3, 2, 1, 1)

        self.doubleSpinBox_minimum_element_size_factor = QDoubleSpinBox(self.frame_2)
        self.doubleSpinBox_minimum_element_size_factor.setObjectName(u"doubleSpinBox_minimum_element_size_factor")
        self.doubleSpinBox_minimum_element_size_factor.setMinimumSize(QSize(140, 28))
        self.doubleSpinBox_minimum_element_size_factor.setMaximumSize(QSize(140, 16777215))
        self.doubleSpinBox_minimum_element_size_factor.setFont(font1)
        self.doubleSpinBox_minimum_element_size_factor.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.doubleSpinBox_minimum_element_size_factor.setDecimals(1)
        self.doubleSpinBox_minimum_element_size_factor.setMinimum(0.100000000000000)
        self.doubleSpinBox_minimum_element_size_factor.setMaximum(1.000000000000000)
        self.doubleSpinBox_minimum_element_size_factor.setSingleStep(0.100000000000000)
        self.doubleSpinBox_minimum_element_size_factor.setValue(0.900000000000000)

        self.gridLayout_10.addWidget(self.doubleSpinBox_minimum_element_size_factor, 2, 2, 1, 1)

        self.doubleSpinBox_maximum_element_size = QDoubleSpinBox(self.frame_2)
        self.doubleSpinBox_maximum_element_size.setObjectName(u"doubleSpinBox_maximum_element_size")
        self.doubleSpinBox_maximum_element_size.setMinimumSize(QSize(140, 28))
        self.doubleSpinBox_maximum_element_size.setMaximumSize(QSize(140, 16777215))
        self.doubleSpinBox_maximum_element_size.setFont(font1)
        self.doubleSpinBox_maximum_element_size.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.doubleSpinBox_maximum_element_size.setDecimals(2)
        self.doubleSpinBox_maximum_element_size.setMinimum(0.010000000000000)
        self.doubleSpinBox_maximum_element_size.setMaximum(2000.000000000000000)
        self.doubleSpinBox_maximum_element_size.setSingleStep(2.000000000000000)
        self.doubleSpinBox_maximum_element_size.setValue(50.000000000000000)

        self.gridLayout_10.addWidget(self.doubleSpinBox_maximum_element_size, 1, 2, 1, 1)

        self.label_2 = QLabel(self.frame_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(120, 20))
        self.label_2.setMaximumSize(QSize(240, 16777215))
        self.label_2.setFont(font1)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_2, 3, 1, 1, 1)

        self.label_9 = QLabel(self.frame_2)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMinimumSize(QSize(120, 20))
        self.label_9.setMaximumSize(QSize(240, 16777215))
        self.label_9.setFont(font1)
        self.label_9.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_9, 2, 1, 1, 1)

        self.label = QLabel(self.frame_2)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(120, 20))
        self.label.setMaximumSize(QSize(240, 16777215))
        self.label.setFont(font1)
        self.label.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_10.addWidget(self.label, 1, 1, 1, 1)

        self.label_3 = QLabel(self.frame_2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(50, 0))
        self.label_3.setMaximumSize(QSize(50, 16777215))
        self.label_3.setFont(font1)

        self.gridLayout_10.addWidget(self.label_3, 1, 3, 1, 1)

        self.label_4 = QLabel(self.frame_2)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(50, 0))
        self.label_4.setMaximumSize(QSize(50, 16777215))
        self.label_4.setFont(font1)

        self.gridLayout_10.addWidget(self.label_4, 3, 3, 1, 1)


        self.gridLayout_2.addWidget(self.frame_2, 0, 0, 1, 1)

        self.tabWidget_global_settings.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.gridLayout_11 = QGridLayout(self.tab_4)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.frame_9 = QFrame(self.tab_4)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setMinimumSize(QSize(0, 62))
        self.frame_9.setMaximumSize(QSize(16777215, 300))
        self.frame_9.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_9.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_13 = QGridLayout(self.frame_9)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_13.setHorizontalSpacing(6)
        self.gridLayout_13.setContentsMargins(4, 4, 4, 4)
        self.frame_10 = QFrame(self.frame_9)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_10.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_13.addWidget(self.frame_10, 0, 0, 1, 1)

        self.frame_7 = QFrame(self.frame_9)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_7.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_13.addWidget(self.frame_7, 0, 3, 1, 1)

        self.comboBox_recombination_algorithm = QComboBox(self.frame_9)
        self.comboBox_recombination_algorithm.addItem("")
        self.comboBox_recombination_algorithm.addItem("")
        self.comboBox_recombination_algorithm.addItem("")
        self.comboBox_recombination_algorithm.addItem("")
        self.comboBox_recombination_algorithm.setObjectName(u"comboBox_recombination_algorithm")
        self.comboBox_recombination_algorithm.setMinimumSize(QSize(200, 28))
        self.comboBox_recombination_algorithm.setMaximumSize(QSize(200, 16777215))
        self.comboBox_recombination_algorithm.setFont(font1)

        self.gridLayout_13.addWidget(self.comboBox_recombination_algorithm, 3, 2, 1, 1)

        self.comboBox_subdivision_algorithm = QComboBox(self.frame_9)
        self.comboBox_subdivision_algorithm.addItem("")
        self.comboBox_subdivision_algorithm.addItem("")
        self.comboBox_subdivision_algorithm.addItem("")
        self.comboBox_subdivision_algorithm.setObjectName(u"comboBox_subdivision_algorithm")
        self.comboBox_subdivision_algorithm.setMinimumSize(QSize(200, 28))
        self.comboBox_subdivision_algorithm.setMaximumSize(QSize(200, 16777215))
        self.comboBox_subdivision_algorithm.setFont(font1)

        self.gridLayout_13.addWidget(self.comboBox_subdivision_algorithm, 4, 2, 1, 1)

        self.label_11 = QLabel(self.frame_9)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMinimumSize(QSize(160, 20))
        self.label_11.setMaximumSize(QSize(300, 16777215))
        self.label_11.setFont(font1)
        self.label_11.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_13.addWidget(self.label_11, 1, 1, 1, 1)

        self.label_12 = QLabel(self.frame_9)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setMinimumSize(QSize(160, 20))
        self.label_12.setMaximumSize(QSize(300, 16777215))
        self.label_12.setFont(font1)
        self.label_12.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_13.addWidget(self.label_12, 4, 1, 1, 1)

        self.label_5 = QLabel(self.frame_9)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(160, 20))
        self.label_5.setMaximumSize(QSize(300, 16777215))
        self.label_5.setFont(font1)
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_13.addWidget(self.label_5, 0, 1, 1, 1)

        self.label_15 = QLabel(self.frame_9)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setMinimumSize(QSize(160, 20))
        self.label_15.setMaximumSize(QSize(300, 16777215))
        self.label_15.setFont(font1)
        self.label_15.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_13.addWidget(self.label_15, 6, 1, 1, 1)

        self.comboBox_second_order_incomplete = QComboBox(self.frame_9)
        self.comboBox_second_order_incomplete.addItem("")
        self.comboBox_second_order_incomplete.addItem("")
        self.comboBox_second_order_incomplete.setObjectName(u"comboBox_second_order_incomplete")
        self.comboBox_second_order_incomplete.setMinimumSize(QSize(200, 28))
        self.comboBox_second_order_incomplete.setMaximumSize(QSize(200, 16777215))
        self.comboBox_second_order_incomplete.setFont(font1)

        self.gridLayout_13.addWidget(self.comboBox_second_order_incomplete, 6, 2, 1, 1)

        self.comboBox_3d_algorithm = QComboBox(self.frame_9)
        self.comboBox_3d_algorithm.addItem("")
        self.comboBox_3d_algorithm.addItem("")
        self.comboBox_3d_algorithm.addItem("")
        self.comboBox_3d_algorithm.setObjectName(u"comboBox_3d_algorithm")
        self.comboBox_3d_algorithm.setMinimumSize(QSize(200, 28))
        self.comboBox_3d_algorithm.setMaximumSize(QSize(200, 16777215))
        self.comboBox_3d_algorithm.setFont(font1)

        self.gridLayout_13.addWidget(self.comboBox_3d_algorithm, 1, 2, 1, 1)

        self.label_13 = QLabel(self.frame_9)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setMinimumSize(QSize(160, 20))
        self.label_13.setMaximumSize(QSize(300, 16777215))
        self.label_13.setFont(font1)
        self.label_13.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_13.addWidget(self.label_13, 3, 1, 1, 1)

        self.comboBox_recombine_all = QComboBox(self.frame_9)
        self.comboBox_recombine_all.addItem("")
        self.comboBox_recombine_all.addItem("")
        self.comboBox_recombine_all.setObjectName(u"comboBox_recombine_all")
        self.comboBox_recombine_all.setMinimumSize(QSize(200, 28))
        self.comboBox_recombine_all.setMaximumSize(QSize(200, 16777215))
        self.comboBox_recombine_all.setFont(font1)

        self.gridLayout_13.addWidget(self.comboBox_recombine_all, 5, 2, 1, 1)

        self.label_14 = QLabel(self.frame_9)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setMinimumSize(QSize(160, 20))
        self.label_14.setMaximumSize(QSize(300, 16777215))
        self.label_14.setFont(font1)
        self.label_14.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_13.addWidget(self.label_14, 5, 1, 1, 1)

        self.comboBox_2d_algorithm = QComboBox(self.frame_9)
        self.comboBox_2d_algorithm.addItem("")
        self.comboBox_2d_algorithm.addItem("")
        self.comboBox_2d_algorithm.addItem("")
        self.comboBox_2d_algorithm.addItem("")
        self.comboBox_2d_algorithm.addItem("")
        self.comboBox_2d_algorithm.addItem("")
        self.comboBox_2d_algorithm.setObjectName(u"comboBox_2d_algorithm")
        self.comboBox_2d_algorithm.setMinimumSize(QSize(200, 28))
        self.comboBox_2d_algorithm.setMaximumSize(QSize(200, 16777215))
        self.comboBox_2d_algorithm.setFont(font1)

        self.gridLayout_13.addWidget(self.comboBox_2d_algorithm, 0, 2, 1, 1)


        self.gridLayout_11.addWidget(self.frame_9, 0, 0, 1, 1)

        self.tabWidget_global_settings.addTab(self.tab_4, "")

        self.gridLayout_9.addWidget(self.tabWidget_global_settings, 0, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.gridLayout = QGridLayout(self.tab_2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.tableWidget_refining_mesh_data = QTableWidget(self.tab_2)
        if (self.tableWidget_refining_mesh_data.columnCount() < 3):
            self.tableWidget_refining_mesh_data.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget_refining_mesh_data.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget_refining_mesh_data.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget_refining_mesh_data.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.tableWidget_refining_mesh_data.setObjectName(u"tableWidget_refining_mesh_data")
        self.tableWidget_refining_mesh_data.setShowGrid(False)
        self.tableWidget_refining_mesh_data.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_refining_mesh_data.verticalHeader().setVisible(False)
        self.tableWidget_refining_mesh_data.verticalHeader().setStretchLastSection(False)

        self.gridLayout.addWidget(self.tableWidget_refining_mesh_data, 2, 1, 1, 1)

        self.frame_11 = QFrame(self.tab_2)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_11.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_12 = QGridLayout(self.frame_11)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setContentsMargins(4, 4, 4, 4)
        self.pushButton_add = QPushButton(self.frame_11)
        self.pushButton_add.setObjectName(u"pushButton_add")
        self.pushButton_add.setMinimumSize(QSize(68, 28))
        self.pushButton_add.setMaximumSize(QSize(140, 16777215))
        self.pushButton_add.setFont(font1)
        self.pushButton_add.setAutoDefault(False)

        self.gridLayout_12.addWidget(self.pushButton_add, 0, 1, 1, 1)

        self.pushButton_delete = QPushButton(self.frame_11)
        self.pushButton_delete.setObjectName(u"pushButton_delete")
        self.pushButton_delete.setMinimumSize(QSize(68, 28))
        self.pushButton_delete.setMaximumSize(QSize(140, 16777215))
        self.pushButton_delete.setFont(font1)
        self.pushButton_delete.setAutoDefault(False)

        self.gridLayout_12.addWidget(self.pushButton_delete, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_11, 3, 1, 1, 1)

        self.frame_3 = QFrame(self.tab_2)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(0, 62))
        self.frame_3.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_3)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setHorizontalSpacing(6)
        self.gridLayout_3.setContentsMargins(4, 4, 4, 4)
        self.label_6 = QLabel(self.frame_3)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(0, 20))
        self.label_6.setFont(font1)

        self.gridLayout_3.addWidget(self.label_6, 2, 1, 1, 1)

        self.doubleSpinBox_refined_element_size = QDoubleSpinBox(self.frame_3)
        self.doubleSpinBox_refined_element_size.setObjectName(u"doubleSpinBox_refined_element_size")
        self.doubleSpinBox_refined_element_size.setMinimumSize(QSize(0, 28))
        self.doubleSpinBox_refined_element_size.setMaximumSize(QSize(200, 16777215))
        self.doubleSpinBox_refined_element_size.setFont(font1)
        self.doubleSpinBox_refined_element_size.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.doubleSpinBox_refined_element_size.setDecimals(2)
        self.doubleSpinBox_refined_element_size.setMinimum(0.010000000000000)
        self.doubleSpinBox_refined_element_size.setMaximum(2000.000000000000000)
        self.doubleSpinBox_refined_element_size.setSingleStep(1.000000000000000)
        self.doubleSpinBox_refined_element_size.setValue(10.000000000000000)

        self.gridLayout_3.addWidget(self.doubleSpinBox_refined_element_size, 2, 2, 1, 1)

        self.label_selected_ids = QLabel(self.frame_3)
        self.label_selected_ids.setObjectName(u"label_selected_ids")
        self.label_selected_ids.setMinimumSize(QSize(0, 20))
        self.label_selected_ids.setFont(font1)
        self.label_selected_ids.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_selected_ids, 1, 1, 1, 1)

        self.label_7 = QLabel(self.frame_3)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(0, 20))
        self.label_7.setFont(font1)

        self.gridLayout_3.addWidget(self.label_7, 2, 3, 1, 1)

        self.lineEdit_selected_ids = QLineEdit(self.frame_3)
        self.lineEdit_selected_ids.setObjectName(u"lineEdit_selected_ids")
        self.lineEdit_selected_ids.setMinimumSize(QSize(0, 28))
        self.lineEdit_selected_ids.setMaximumSize(QSize(200, 16777215))
        self.lineEdit_selected_ids.setFont(font1)
        self.lineEdit_selected_ids.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.lineEdit_selected_ids, 1, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer, 2, 0, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_2, 2, 4, 1, 1)


        self.gridLayout.addWidget(self.frame_3, 0, 1, 1, 1)

        self.tabWidget_main.addTab(self.tab_2, "")
        self.tab_5 = QWidget()
        self.tab_5.setObjectName(u"tab_5")
        self.verticalLayout = QVBoxLayout(self.tab_5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tableWidget_mesh_quality = QTableWidget(self.tab_5)
        if (self.tableWidget_mesh_quality.columnCount() < 2):
            self.tableWidget_mesh_quality.setColumnCount(2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget_mesh_quality.setHorizontalHeaderItem(0, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget_mesh_quality.setHorizontalHeaderItem(1, __qtablewidgetitem4)
        self.tableWidget_mesh_quality.setObjectName(u"tableWidget_mesh_quality")
        self.tableWidget_mesh_quality.setMaximumSize(QSize(654654, 16777215))
        self.tableWidget_mesh_quality.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_mesh_quality.verticalHeader().setVisible(False)
        self.tableWidget_mesh_quality.verticalHeader().setStretchLastSection(False)

        self.verticalLayout.addWidget(self.tableWidget_mesh_quality)

        self.pushButton_plot_parameter = QPushButton(self.tab_5)
        self.pushButton_plot_parameter.setObjectName(u"pushButton_plot_parameter")
        self.pushButton_plot_parameter.setEnabled(True)
        self.pushButton_plot_parameter.setMinimumSize(QSize(140, 30))
        self.pushButton_plot_parameter.setMaximumSize(QSize(140, 16777215))
        self.pushButton_plot_parameter.setAutoDefault(False)

        self.verticalLayout.addWidget(self.pushButton_plot_parameter, 0, Qt.AlignmentFlag.AlignHCenter)

        self.tabWidget_main.addTab(self.tab_5, "")

        self.gridLayout_6.addWidget(self.tabWidget_main, 1, 1, 1, 1)


        self.gridLayout_7.addWidget(self.frame, 1, 0, 1, 1)

        self.frame_6 = QFrame(Dialog)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setMinimumSize(QSize(400, 48))
        self.frame_6.setMaximumSize(QSize(16777215, 48))
        self.frame_6.setFrameShape(QFrame.Shape.Box)
        self.frame_6.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_6.setLineWidth(1)
        self.gridLayout_8 = QGridLayout(self.frame_6)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(6, 6, 6, 6)
        self.label_8 = QLabel(self.frame_6)
        self.label_8.setObjectName(u"label_8")
        font3 = QFont()
        font3.setFamilies([u"MS Shell Dlg 2"])
        font3.setPointSize(11)
        font3.setBold(False)
        self.label_8.setFont(font3)
        self.label_8.setTextFormat(Qt.TextFormat.AutoText)
        self.label_8.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_8.addWidget(self.label_8, 0, 0, 1, 1)


        self.gridLayout_7.addWidget(self.frame_6, 0, 0, 1, 1)

        self.frame_4 = QFrame(Dialog)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(0, 48))
        self.frame_4.setMaximumSize(QSize(16777215, 48))
        self.frame_4.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(4, 4, 4, 4)
        self.pushButton_generate_mesh = QPushButton(self.frame_4)
        self.pushButton_generate_mesh.setObjectName(u"pushButton_generate_mesh")
        self.pushButton_generate_mesh.setMinimumSize(QSize(140, 30))
        self.pushButton_generate_mesh.setMaximumSize(QSize(140, 30))
        self.pushButton_generate_mesh.setFont(font1)
        self.pushButton_generate_mesh.setAutoDefault(True)

        self.gridLayout_4.addWidget(self.pushButton_generate_mesh, 0, 1, 1, 1)

        self.pushButton_exit = QPushButton(self.frame_4)
        self.pushButton_exit.setObjectName(u"pushButton_exit")
        self.pushButton_exit.setMinimumSize(QSize(140, 30))
        self.pushButton_exit.setMaximumSize(QSize(140, 30))
        self.pushButton_exit.setFont(font1)
        self.pushButton_exit.setAutoDefault(False)

        self.gridLayout_4.addWidget(self.pushButton_exit, 0, 0, 1, 1)


        self.gridLayout_7.addWidget(self.frame_4, 2, 0, 1, 1)


        self.retranslateUi(Dialog)

        self.tabWidget_main.setCurrentIndex(2)
        self.tabWidget_global_settings.setCurrentIndex(0)
        self.comboBox_3d_algorithm.setCurrentIndex(0)
        self.pushButton_generate_mesh.setDefault(False)
        self.pushButton_exit.setDefault(False)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_16.setText(QCoreApplication.translate("Dialog", u"Element type:", None))
        self.label_10.setText(QCoreApplication.translate("Dialog", u"Shape function:", None))
        self.checkBox_mesh_connection.setText(QCoreApplication.translate("Dialog", u"Merge nodes from connected volumes", None))
        self.comboBox_element_type.setItemText(0, QCoreApplication.translate("Dialog", u"Tetrahedral", None))
        self.comboBox_element_type.setItemText(1, QCoreApplication.translate("Dialog", u"Hexahedral", None))

        self.comboBox_shape_function.setItemText(0, QCoreApplication.translate("Dialog", u"Linear", None))
        self.comboBox_shape_function.setItemText(1, QCoreApplication.translate("Dialog", u"Quadratic", None))

        self.lineEdit_geometry_tolerance.setText(QCoreApplication.translate("Dialog", u"1e-6", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Geometry tolerance:", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", u"Min. element size factor:", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Max. element size:", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"[mm]", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"[mm]", None))
        self.tabWidget_global_settings.setTabText(self.tabWidget_global_settings.indexOf(self.tab_3), QCoreApplication.translate("Dialog", u"Main", None))
        self.comboBox_recombination_algorithm.setItemText(0, QCoreApplication.translate("Dialog", u"Simple", None))
        self.comboBox_recombination_algorithm.setItemText(1, QCoreApplication.translate("Dialog", u"Blossom", None))
        self.comboBox_recombination_algorithm.setItemText(2, QCoreApplication.translate("Dialog", u"Simple Full-Quad", None))
        self.comboBox_recombination_algorithm.setItemText(3, QCoreApplication.translate("Dialog", u"Blossom Full-Quad", None))

        self.comboBox_subdivision_algorithm.setItemText(0, QCoreApplication.translate("Dialog", u"None", None))
        self.comboBox_subdivision_algorithm.setItemText(1, QCoreApplication.translate("Dialog", u"All quads", None))
        self.comboBox_subdivision_algorithm.setItemText(2, QCoreApplication.translate("Dialog", u"All hexas", None))

        self.label_11.setText(QCoreApplication.translate("Dialog", u"3D algorithm:", None))
        self.label_12.setText(QCoreApplication.translate("Dialog", u"Subdivision algorithm:", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"2D algorithm:", None))
        self.label_15.setText(QCoreApplication.translate("Dialog", u"Second order incomplete", None))
        self.comboBox_second_order_incomplete.setItemText(0, QCoreApplication.translate("Dialog", u"No", None))
        self.comboBox_second_order_incomplete.setItemText(1, QCoreApplication.translate("Dialog", u"Yes", None))

        self.comboBox_3d_algorithm.setItemText(0, QCoreApplication.translate("Dialog", u"Delaunay", None))
        self.comboBox_3d_algorithm.setItemText(1, QCoreApplication.translate("Dialog", u"Frontal-Delaunay", None))
        self.comboBox_3d_algorithm.setItemText(2, QCoreApplication.translate("Dialog", u"HXT_3D", None))

        self.label_13.setText(QCoreApplication.translate("Dialog", u"Recombination algorithm:", None))
        self.comboBox_recombine_all.setItemText(0, QCoreApplication.translate("Dialog", u"No", None))
        self.comboBox_recombine_all.setItemText(1, QCoreApplication.translate("Dialog", u"Yes", None))

        self.label_14.setText(QCoreApplication.translate("Dialog", u"Recombine all triangular meshes:", None))
        self.comboBox_2d_algorithm.setItemText(0, QCoreApplication.translate("Dialog", u"MeshAdapt", None))
        self.comboBox_2d_algorithm.setItemText(1, QCoreApplication.translate("Dialog", u"Automatic", None))
        self.comboBox_2d_algorithm.setItemText(2, QCoreApplication.translate("Dialog", u"Initial Mesh Only", None))
        self.comboBox_2d_algorithm.setItemText(3, QCoreApplication.translate("Dialog", u"Delaunay", None))
        self.comboBox_2d_algorithm.setItemText(4, QCoreApplication.translate("Dialog", u"Frontal-Delaunay", None))
        self.comboBox_2d_algorithm.setItemText(5, QCoreApplication.translate("Dialog", u"Quasi Structured Quads", None))

        self.tabWidget_global_settings.setTabText(self.tabWidget_global_settings.indexOf(self.tab_4), QCoreApplication.translate("Dialog", u"Advanced controls", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab), QCoreApplication.translate("Dialog", u"Global settings", None))
        ___qtablewidgetitem = self.tableWidget_refining_mesh_data.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Dialog", u"Element size [mm]", None));
        ___qtablewidgetitem1 = self.tableWidget_refining_mesh_data.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Dialog", u"Selection type", None));
        ___qtablewidgetitem2 = self.tableWidget_refining_mesh_data.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Dialog", u"Surface IDs", None));
        self.pushButton_add.setText(QCoreApplication.translate("Dialog", u"Add", None))
        self.pushButton_delete.setText(QCoreApplication.translate("Dialog", u"Delete", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"Refined element size: ", None))
        self.label_selected_ids.setText(QCoreApplication.translate("Dialog", u"Selected surface IDs:", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"[mm]", None))
        self.lineEdit_selected_ids.setText("")
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_2), QCoreApplication.translate("Dialog", u"Local refining", None))
        ___qtablewidgetitem3 = self.tableWidget_mesh_quality.horizontalHeaderItem(0)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Dialog", u"Parameter", None));
        ___qtablewidgetitem4 = self.tableWidget_mesh_quality.horizontalHeaderItem(1)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Dialog", u"Minimum value", None));
        self.pushButton_plot_parameter.setText(QCoreApplication.translate("Dialog", u"Plot parameter", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_5), QCoreApplication.translate("Dialog", u"Mesh quality", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"Mesh configuration", None))
        self.pushButton_generate_mesh.setText(QCoreApplication.translate("Dialog", u"Generate mesh", None))
        self.pushButton_exit.setText(QCoreApplication.translate("Dialog", u"Exit", None))
    # retranslateUi



class MesherSetup_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame: QFrame
                    - (Layout): QGridLayout
                            - frame_8: QFrame
                                - (Layout): QGridLayout
                                        - label_16: QLabel
                                        - label_10: QLabel
                                        - frame_13: QFrame
                                        - frame_14: QFrame
                                        - checkBox_mesh_connection: QCheckBox
                                        - comboBox_element_type: QComboBox
                                        - comboBox_shape_function: QComboBox
                            - tabWidget_main: QTabWidget
                                - tab: QWidget
                                    - (Layout): QGridLayout
                                            - tabWidget_global_settings: QTabWidget
                                                - tab_3: QWidget
                                                    - (Layout): QGridLayout
                                                            - frame_2: QFrame
                                                                - (Layout): QGridLayout
                                                                        - frame_12: QFrame
                                                                        - frame_5: QFrame
                                                                        - lineEdit_geometry_tolerance: QLineEdit
                                                                        - doubleSpinBox_minimum_element_size_factor: QDoubleSpinBox
                                                                        - doubleSpinBox_maximum_element_size: QDoubleSpinBox
                                                                        - label_2: QLabel
                                                                        - label_9: QLabel
                                                                        - label: QLabel
                                                                        - label_3: QLabel
                                                                        - label_4: QLabel
                                                - tab_4: QWidget
                                                    - (Layout): QGridLayout
                                                            - frame_9: QFrame
                                                                - (Layout): QGridLayout
                                                                        - frame_10: QFrame
                                                                        - frame_7: QFrame
                                                                        - comboBox_recombination_algorithm: QComboBox
                                                                        - comboBox_subdivision_algorithm: QComboBox
                                                                        - label_11: QLabel
                                                                        - label_12: QLabel
                                                                        - label_5: QLabel
                                                                        - label_15: QLabel
                                                                        - comboBox_second_order_incomplete: QComboBox
                                                                        - comboBox_3d_algorithm: QComboBox
                                                                        - label_13: QLabel
                                                                        - comboBox_recombine_all: QComboBox
                                                                        - label_14: QLabel
                                                                        - comboBox_2d_algorithm: QComboBox
                                - tab_2: QWidget
                                    - (Layout): QGridLayout
                                            - tableWidget_refining_mesh_data: QTableWidget
                                            - frame_11: QFrame
                                                - (Layout): QGridLayout
                                                        - pushButton_add: QPushButton
                                                        - pushButton_delete: QPushButton
                                            - frame_3: QFrame
                                                - (Layout): QGridLayout
                                                        - label_6: QLabel
                                                        - doubleSpinBox_refined_element_size: QDoubleSpinBox
                                                        - label_selected_ids: QLabel
                                                        - label_7: QLabel
                                                        - lineEdit_selected_ids: QLineEdit
                                - tab_5: QWidget
                                    - (Layout): QVBoxLayout
                                            - tableWidget_mesh_quality: QTableWidget
                                            - pushButton_plot_parameter: QPushButton
                - frame_6: QFrame
                    - (Layout): QGridLayout
                            - label_8: QLabel
                - frame_4: QFrame
                    - (Layout): QGridLayout
                            - pushButton_generate_mesh: QPushButton
                            - pushButton_exit: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
