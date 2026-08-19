# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mesher_setup_inputs.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QDialog,
    QDoubleSpinBox, QFrame, QGridLayout, QHeaderView,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QTabWidget, QTableWidget, QTableWidgetItem,
    QWidget)

from vibra.interface.formatters.icons import Icon

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(596, 603)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setVerticalSpacing(4)
        self.gridLayout.setContentsMargins(4, 4, 4, -1)
        self.frame_title = QFrame(Dialog)
        self.frame_title.setObjectName(u"frame_title")
        self.frame_title.setMinimumSize(QSize(0, 48))
        self.frame_title.setMaximumSize(QSize(16777215, 48))
        self.frame_title.setFrameShape(QFrame.Shape.Box)
        self.frame_title.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_title)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label = QLabel(self.frame_title)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_title, 0, 0, 1, 1)

        self.frame_main = QFrame(Dialog)
        self.frame_main.setObjectName(u"frame_main")
        self.frame_main.setFrameShape(QFrame.Shape.Box)
        self.frame_main.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_main)
        self.gridLayout_4.setSpacing(2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(2, 2, 2, 2)
        self.frame_element_formulation = QFrame(self.frame_main)
        self.frame_element_formulation.setObjectName(u"frame_element_formulation")
        self.frame_element_formulation.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_element_formulation.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_element_formulation)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setHorizontalSpacing(6)
        self.gridLayout_2.setContentsMargins(4, 4, 4, 4)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 1, 0, 1, 1)

        self.comboBox_element_order = QComboBox(self.frame_element_formulation)
        self.comboBox_element_order.addItem("")
        self.comboBox_element_order.addItem("")
        self.comboBox_element_order.setObjectName(u"comboBox_element_order")
        self.comboBox_element_order.setMinimumSize(QSize(120, 28))
        self.comboBox_element_order.setMaximumSize(QSize(140, 16777215))
        font1 = QFont()
        font1.setPointSize(10)
        self.comboBox_element_order.setFont(font1)

        self.gridLayout_2.addWidget(self.comboBox_element_order, 1, 2, 1, 1)

        self.label_20 = QLabel(self.frame_element_formulation)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setMinimumSize(QSize(180, 20))
        self.label_20.setMaximumSize(QSize(240, 16777215))
        self.label_20.setFont(font1)
        self.label_20.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_20, 3, 1, 1, 1)

        self.horizontalSpacer1 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer1, 0, 0, 1, 1)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_9, 1, 3, 1, 1)

        self.comboBox_element_geometry = QComboBox(self.frame_element_formulation)
        self.comboBox_element_geometry.addItem("")
        self.comboBox_element_geometry.addItem("")
        self.comboBox_element_geometry.setObjectName(u"comboBox_element_geometry")
        self.comboBox_element_geometry.setMinimumSize(QSize(120, 28))
        self.comboBox_element_geometry.setMaximumSize(QSize(140, 16777215))
        self.comboBox_element_geometry.setFont(font1)

        self.gridLayout_2.addWidget(self.comboBox_element_geometry, 0, 2, 1, 1)

        self.label_16 = QLabel(self.frame_element_formulation)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setMinimumSize(QSize(180, 20))
        self.label_16.setMaximumSize(QSize(240, 16777215))
        self.label_16.setFont(font1)
        self.label_16.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_16, 0, 1, 1, 1)

        self.label_19 = QLabel(self.frame_element_formulation)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setMinimumSize(QSize(180, 20))
        self.label_19.setMaximumSize(QSize(240, 16777215))
        self.label_19.setFont(font1)
        self.label_19.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_19, 2, 1, 1, 1)

        self.comboBox_volumes_interface_behavior = QComboBox(self.frame_element_formulation)
        self.comboBox_volumes_interface_behavior.addItem("")
        self.comboBox_volumes_interface_behavior.addItem("")
        self.comboBox_volumes_interface_behavior.setObjectName(u"comboBox_volumes_interface_behavior")
        self.comboBox_volumes_interface_behavior.setMinimumSize(QSize(120, 28))
        self.comboBox_volumes_interface_behavior.setMaximumSize(QSize(140, 16777215))
        self.comboBox_volumes_interface_behavior.setFont(font1)
        self.comboBox_volumes_interface_behavior.setMinimumContentsLength(0)

        self.gridLayout_2.addWidget(self.comboBox_volumes_interface_behavior, 3, 2, 1, 1)

        self.label_10 = QLabel(self.frame_element_formulation)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(180, 20))
        self.label_10.setMaximumSize(QSize(240, 16777215))
        self.label_10.setFont(font1)
        self.label_10.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_10, 1, 1, 1, 1)

        self.label_21 = QLabel(self.frame_element_formulation)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setMinimumSize(QSize(180, 20))
        self.label_21.setMaximumSize(QSize(240, 16777215))
        self.label_21.setFont(font1)
        self.label_21.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_21, 4, 1, 1, 1)

        self.label_201 = QLabel(self.frame_element_formulation)
        self.label_201.setObjectName(u"label_201")
        self.label_201.setMinimumSize(QSize(180, 20))
        self.label_201.setMaximumSize(QSize(240, 16777215))
        self.label_201.setFont(font1)
        self.label_201.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_201, 3, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_2, 0, 3, 1, 1)

        self.comboBox_mesh_quality_metrics = QComboBox(self.frame_element_formulation)
        self.comboBox_mesh_quality_metrics.addItem("")
        self.comboBox_mesh_quality_metrics.addItem("")
        self.comboBox_mesh_quality_metrics.setObjectName(u"comboBox_mesh_quality_metrics")
        self.comboBox_mesh_quality_metrics.setMinimumSize(QSize(120, 28))
        self.comboBox_mesh_quality_metrics.setMaximumSize(QSize(140, 16777215))
        self.comboBox_mesh_quality_metrics.setFont(font1)

        self.gridLayout_2.addWidget(self.comboBox_mesh_quality_metrics, 2, 2, 1, 1)

        self.pushButton_suppress_volumes = QPushButton(self.frame_element_formulation)
        self.pushButton_suppress_volumes.setObjectName(u"pushButton_suppress_volumes")
        self.pushButton_suppress_volumes.setMinimumSize(QSize(120, 30))
        self.pushButton_suppress_volumes.setMaximumSize(QSize(16000, 30))
        font2 = QFont()
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        self.pushButton_suppress_volumes.setFont(font2)
        self.pushButton_suppress_volumes.setAutoDefault(False)
        self.pushButton_suppress_volumes.setFlat(False)

        self.gridLayout_2.addWidget(self.pushButton_suppress_volumes, 4, 2, 1, 1)

        self.label_suppressed_volume_count = QLabel(self.frame_element_formulation)
        self.label_suppressed_volume_count.setObjectName(u"label_suppressed_volume_count")
        self.label_suppressed_volume_count.setFont(font1)

        self.gridLayout_2.addWidget(self.label_suppressed_volume_count, 4, 3, 1, 1)


        self.gridLayout_4.addWidget(self.frame_element_formulation, 0, 0, 1, 1)

        self.frame_tab_widgets = QFrame(self.frame_main)
        self.frame_tab_widgets.setObjectName(u"frame_tab_widgets")
        self.frame_tab_widgets.setMinimumSize(QSize(0, 300))
        self.frame_tab_widgets.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_tab_widgets.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_14 = QGridLayout(self.frame_tab_widgets)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.tabWidget_main = QTabWidget(self.frame_tab_widgets)
        self.tabWidget_main.setObjectName(u"tabWidget_main")
        self.tabWidget_main.setEnabled(True)
        font3 = QFont()
        font3.setPointSize(9)
        self.tabWidget_main.setFont(font3)
        self.tabWidget_main.setTabShape(QTabWidget.TabShape.Rounded)
        self.tabWidget_main.setTabBarAutoHide(False)
        self.tab_global_settings = QWidget()
        self.tab_global_settings.setObjectName(u"tab_global_settings")
        self.gridLayout_9 = QGridLayout(self.tab_global_settings)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(6, 6, 6, 6)
        self.frame_6 = QFrame(self.tab_global_settings)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setMinimumSize(QSize(0, 62))
        self.frame_6.setMaximumSize(QSize(16777215, 180))
        self.frame_6.setFrameShape(QFrame.Shape.NoFrame)
        self.gridLayout_17 = QGridLayout(self.frame_6)
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.gridLayout_17.setHorizontalSpacing(6)
        self.gridLayout_17.setContentsMargins(4, 4, 4, 4)
        self.label_28 = QLabel(self.frame_6)
        self.label_28.setObjectName(u"label_28")
        self.label_28.setMinimumSize(QSize(140, 20))
        self.label_28.setMaximumSize(QSize(240, 16777215))
        self.label_28.setFont(font1)
        self.label_28.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_17.addWidget(self.label_28, 2, 1, 1, 1)

        self.label_29 = QLabel(self.frame_6)
        self.label_29.setObjectName(u"label_29")
        self.label_29.setMinimumSize(QSize(40, 0))
        self.label_29.setMaximumSize(QSize(48, 16777215))
        self.label_29.setFont(font1)

        self.gridLayout_17.addWidget(self.label_29, 2, 3, 1, 1)

        self.doubleSpinBox_minimum_element_size = QDoubleSpinBox(self.frame_6)
        self.doubleSpinBox_minimum_element_size.setObjectName(u"doubleSpinBox_minimum_element_size")
        self.doubleSpinBox_minimum_element_size.setMinimumSize(QSize(140, 28))
        self.doubleSpinBox_minimum_element_size.setMaximumSize(QSize(140, 16777215))
        self.doubleSpinBox_minimum_element_size.setFont(font1)
        self.doubleSpinBox_minimum_element_size.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.doubleSpinBox_minimum_element_size.setDecimals(2)
        self.doubleSpinBox_minimum_element_size.setMinimum(0.010000000000000)
        self.doubleSpinBox_minimum_element_size.setMaximum(2000.000000000000000)
        self.doubleSpinBox_minimum_element_size.setSingleStep(2.000000000000000)
        self.doubleSpinBox_minimum_element_size.setValue(50.000000000000000)

        self.gridLayout_17.addWidget(self.doubleSpinBox_minimum_element_size, 2, 2, 1, 1)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_17.addItem(self.horizontalSpacer_12, 1, 5, 1, 1)

        self.label_30 = QLabel(self.frame_6)
        self.label_30.setObjectName(u"label_30")
        self.label_30.setMinimumSize(QSize(140, 20))
        self.label_30.setMaximumSize(QSize(240, 16777215))
        self.label_30.setFont(font1)
        self.label_30.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_17.addWidget(self.label_30, 1, 1, 1, 1)

        self.label_31 = QLabel(self.frame_6)
        self.label_31.setObjectName(u"label_31")
        self.label_31.setMinimumSize(QSize(140, 20))
        self.label_31.setMaximumSize(QSize(240, 16777215))
        self.label_31.setFont(font1)
        self.label_31.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_17.addWidget(self.label_31, 3, 1, 1, 1)

        self.doubleSpinBox_size_factor = QDoubleSpinBox(self.frame_6)
        self.doubleSpinBox_size_factor.setObjectName(u"doubleSpinBox_size_factor")
        self.doubleSpinBox_size_factor.setMinimumSize(QSize(140, 28))
        self.doubleSpinBox_size_factor.setMaximumSize(QSize(140, 16777215))
        self.doubleSpinBox_size_factor.setFont(font1)
        self.doubleSpinBox_size_factor.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.doubleSpinBox_size_factor.setDecimals(2)
        self.doubleSpinBox_size_factor.setMinimum(0.000000000000000)
        self.doubleSpinBox_size_factor.setMaximum(2.000000000000000)
        self.doubleSpinBox_size_factor.setSingleStep(0.100000000000000)
        self.doubleSpinBox_size_factor.setValue(0.000000000000000)

        self.gridLayout_17.addWidget(self.doubleSpinBox_size_factor, 3, 2, 1, 1)

        self.doubleSpinBox_maximum_element_size = QDoubleSpinBox(self.frame_6)
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

        self.gridLayout_17.addWidget(self.doubleSpinBox_maximum_element_size, 1, 2, 1, 1)

        self.label_32 = QLabel(self.frame_6)
        self.label_32.setObjectName(u"label_32")
        self.label_32.setMinimumSize(QSize(40, 0))
        self.label_32.setMaximumSize(QSize(48, 16777215))
        self.label_32.setFont(font1)

        self.gridLayout_17.addWidget(self.label_32, 4, 3, 1, 1)

        self.lineEdit_geometry_tolerance = QLineEdit(self.frame_6)
        self.lineEdit_geometry_tolerance.setObjectName(u"lineEdit_geometry_tolerance")
        self.lineEdit_geometry_tolerance.setMinimumSize(QSize(140, 28))
        self.lineEdit_geometry_tolerance.setMaximumSize(QSize(140, 16777215))
        self.lineEdit_geometry_tolerance.setFont(font1)
        self.lineEdit_geometry_tolerance.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_17.addWidget(self.lineEdit_geometry_tolerance, 4, 2, 1, 1)

        self.label_33 = QLabel(self.frame_6)
        self.label_33.setObjectName(u"label_33")
        self.label_33.setMinimumSize(QSize(140, 20))
        self.label_33.setMaximumSize(QSize(240, 16777215))
        self.label_33.setFont(font1)
        self.label_33.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_17.addWidget(self.label_33, 4, 1, 1, 1)

        self.pushButton_syncrhonize = QPushButton(self.frame_6)
        self.pushButton_syncrhonize.setObjectName(u"pushButton_syncrhonize")
        icon = Icon(u":/icons/sync_enabled.png")
        self.pushButton_syncrhonize.setIcon(icon)
        self.pushButton_syncrhonize.setIconSize(QSize(20, 20))
        self.pushButton_syncrhonize.setAutoDefault(False)

        self.gridLayout_17.addWidget(self.pushButton_syncrhonize, 1, 4, 1, 1)

        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_17.addItem(self.horizontalSpacer_13, 1, 0, 1, 1)

        self.label_34 = QLabel(self.frame_6)
        self.label_34.setObjectName(u"label_34")
        self.label_34.setMinimumSize(QSize(40, 0))
        self.label_34.setMaximumSize(QSize(48, 16777215))
        self.label_34.setFont(font1)

        self.gridLayout_17.addWidget(self.label_34, 1, 3, 1, 1)


        self.gridLayout_9.addWidget(self.frame_6, 0, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_global_settings, "")
        self.tab_local_mesh_size_control = QWidget()
        self.tab_local_mesh_size_control.setObjectName(u"tab_local_mesh_size_control")
        self.gridLayout_7 = QGridLayout(self.tab_local_mesh_size_control)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.frame_11 = QFrame(self.tab_local_mesh_size_control)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setMinimumSize(QSize(0, 48))
        self.frame_11.setFrameShape(QFrame.Shape.NoFrame)
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


        self.gridLayout_7.addWidget(self.frame_11, 3, 1, 1, 1)

        self.tableWidget_local_mesh_size_control_data = QTableWidget(self.tab_local_mesh_size_control)
        if (self.tableWidget_local_mesh_size_control_data.columnCount() < 3):
            self.tableWidget_local_mesh_size_control_data.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget_local_mesh_size_control_data.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget_local_mesh_size_control_data.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget_local_mesh_size_control_data.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.tableWidget_local_mesh_size_control_data.setObjectName(u"tableWidget_local_mesh_size_control_data")
        self.tableWidget_local_mesh_size_control_data.setMaximumSize(QSize(16777215, 16777215))
        self.tableWidget_local_mesh_size_control_data.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableWidget_local_mesh_size_control_data.setShowGrid(False)
        self.tableWidget_local_mesh_size_control_data.horizontalHeader().setDefaultSectionSize(160)
        self.tableWidget_local_mesh_size_control_data.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_local_mesh_size_control_data.verticalHeader().setVisible(False)
        self.tableWidget_local_mesh_size_control_data.verticalHeader().setStretchLastSection(False)

        self.gridLayout_7.addWidget(self.tableWidget_local_mesh_size_control_data, 2, 1, 1, 1)

        self.frame_13 = QFrame(self.tab_local_mesh_size_control)
        self.frame_13.setObjectName(u"frame_13")
        self.frame_13.setMinimumSize(QSize(0, 68))
        self.frame_13.setFrameShape(QFrame.Shape.NoFrame)
        self.gridLayout_8 = QGridLayout(self.frame_13)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setHorizontalSpacing(6)
        self.gridLayout_8.setContentsMargins(4, 4, 4, 4)
        self.lineEdit_selected_ids = QLineEdit(self.frame_13)
        self.lineEdit_selected_ids.setObjectName(u"lineEdit_selected_ids")
        self.lineEdit_selected_ids.setMinimumSize(QSize(0, 28))
        self.lineEdit_selected_ids.setMaximumSize(QSize(200, 16777215))
        self.lineEdit_selected_ids.setFont(font1)
        self.lineEdit_selected_ids.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_8.addWidget(self.lineEdit_selected_ids, 1, 2, 1, 1)

        self.label_7 = QLabel(self.frame_13)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(160, 20))
        self.label_7.setMaximumSize(QSize(16777215, 160))
        self.label_7.setFont(font1)
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_7, 2, 1, 1, 1)

        self.doubleSpinBox_local_mesh_size_control_element_size = QDoubleSpinBox(self.frame_13)
        self.doubleSpinBox_local_mesh_size_control_element_size.setObjectName(u"doubleSpinBox_local_mesh_size_control_element_size")
        self.doubleSpinBox_local_mesh_size_control_element_size.setMinimumSize(QSize(0, 28))
        self.doubleSpinBox_local_mesh_size_control_element_size.setMaximumSize(QSize(200, 16777215))
        self.doubleSpinBox_local_mesh_size_control_element_size.setFont(font1)
        self.doubleSpinBox_local_mesh_size_control_element_size.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.doubleSpinBox_local_mesh_size_control_element_size.setDecimals(2)
        self.doubleSpinBox_local_mesh_size_control_element_size.setMinimum(0.010000000000000)
        self.doubleSpinBox_local_mesh_size_control_element_size.setMaximum(2000.000000000000000)
        self.doubleSpinBox_local_mesh_size_control_element_size.setSingleStep(1.000000000000000)
        self.doubleSpinBox_local_mesh_size_control_element_size.setValue(10.000000000000000)

        self.gridLayout_8.addWidget(self.doubleSpinBox_local_mesh_size_control_element_size, 2, 2, 1, 1)

        self.label_8 = QLabel(self.frame_13)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMinimumSize(QSize(0, 20))
        self.label_8.setFont(font1)

        self.gridLayout_8.addWidget(self.label_8, 2, 3, 1, 1)

        self.label_selected_ids = QLabel(self.frame_13)
        self.label_selected_ids.setObjectName(u"label_selected_ids")
        self.label_selected_ids.setMinimumSize(QSize(160, 20))
        self.label_selected_ids.setMaximumSize(QSize(16777215, 160))
        self.label_selected_ids.setFont(font1)
        self.label_selected_ids.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_selected_ids, 1, 1, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_3, 2, 0, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_4, 2, 4, 1, 1)

        self.comboBox_local_mesh_size_control_entity_type = QComboBox(self.frame_13)
        self.comboBox_local_mesh_size_control_entity_type.addItem("")
        self.comboBox_local_mesh_size_control_entity_type.addItem("")
        self.comboBox_local_mesh_size_control_entity_type.setObjectName(u"comboBox_local_mesh_size_control_entity_type")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_local_mesh_size_control_entity_type.sizePolicy().hasHeightForWidth())
        self.comboBox_local_mesh_size_control_entity_type.setSizePolicy(sizePolicy)
        self.comboBox_local_mesh_size_control_entity_type.setMinimumSize(QSize(1, 28))
        self.comboBox_local_mesh_size_control_entity_type.setMaximumSize(QSize(90, 16777215))
        self.comboBox_local_mesh_size_control_entity_type.setFont(font1)
        self.comboBox_local_mesh_size_control_entity_type.setMinimumContentsLength(0)

        self.gridLayout_8.addWidget(self.comboBox_local_mesh_size_control_entity_type, 1, 3, 1, 2)


        self.gridLayout_7.addWidget(self.frame_13, 0, 1, 1, 1)

        self.tabWidget_main.addTab(self.tab_local_mesh_size_control, "")
        self.tab_advanced_controls = QWidget()
        self.tab_advanced_controls.setObjectName(u"tab_advanced_controls")
        self.gridLayout_13 = QGridLayout(self.tab_advanced_controls)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.label_13 = QLabel(self.tab_advanced_controls)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setMinimumSize(QSize(210, 20))
        self.label_13.setMaximumSize(QSize(300, 16777215))
        self.label_13.setFont(font1)
        self.label_13.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_13.addWidget(self.label_13, 2, 0, 1, 1)

        self.label_12 = QLabel(self.tab_advanced_controls)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setMinimumSize(QSize(210, 20))
        self.label_12.setMaximumSize(QSize(300, 16777215))
        self.label_12.setFont(font1)
        self.label_12.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_13.addWidget(self.label_12, 3, 0, 1, 1)

        self.label_6 = QLabel(self.tab_advanced_controls)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(210, 20))
        self.label_6.setMaximumSize(QSize(300, 16777215))
        self.label_6.setFont(font1)
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_13.addWidget(self.label_6, 0, 0, 1, 1)

        self.comboBox_2d_algorithm = QComboBox(self.tab_advanced_controls)
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

        self.gridLayout_13.addWidget(self.comboBox_2d_algorithm, 0, 1, 1, 1)

        self.label_11 = QLabel(self.tab_advanced_controls)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMinimumSize(QSize(210, 20))
        self.label_11.setMaximumSize(QSize(300, 16777215))
        self.label_11.setFont(font1)
        self.label_11.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_13.addWidget(self.label_11, 1, 0, 1, 1)

        self.comboBox_recombination_algorithm = QComboBox(self.tab_advanced_controls)
        self.comboBox_recombination_algorithm.addItem("")
        self.comboBox_recombination_algorithm.addItem("")
        self.comboBox_recombination_algorithm.addItem("")
        self.comboBox_recombination_algorithm.addItem("")
        self.comboBox_recombination_algorithm.setObjectName(u"comboBox_recombination_algorithm")
        self.comboBox_recombination_algorithm.setMinimumSize(QSize(200, 28))
        self.comboBox_recombination_algorithm.setMaximumSize(QSize(200, 16777215))
        self.comboBox_recombination_algorithm.setFont(font1)

        self.gridLayout_13.addWidget(self.comboBox_recombination_algorithm, 2, 1, 1, 1)

        self.comboBox_3d_algorithm = QComboBox(self.tab_advanced_controls)
        self.comboBox_3d_algorithm.addItem("")
        self.comboBox_3d_algorithm.addItem("")
        self.comboBox_3d_algorithm.addItem("")
        self.comboBox_3d_algorithm.setObjectName(u"comboBox_3d_algorithm")
        self.comboBox_3d_algorithm.setMinimumSize(QSize(200, 28))
        self.comboBox_3d_algorithm.setMaximumSize(QSize(200, 16777215))
        self.comboBox_3d_algorithm.setFont(font1)

        self.gridLayout_13.addWidget(self.comboBox_3d_algorithm, 1, 1, 1, 1)

        self.comboBox_subdivision_algorithm = QComboBox(self.tab_advanced_controls)
        self.comboBox_subdivision_algorithm.addItem("")
        self.comboBox_subdivision_algorithm.addItem("")
        self.comboBox_subdivision_algorithm.addItem("")
        self.comboBox_subdivision_algorithm.setObjectName(u"comboBox_subdivision_algorithm")
        self.comboBox_subdivision_algorithm.setMinimumSize(QSize(200, 28))
        self.comboBox_subdivision_algorithm.setMaximumSize(QSize(200, 16777215))
        self.comboBox_subdivision_algorithm.setFont(font1)

        self.gridLayout_13.addWidget(self.comboBox_subdivision_algorithm, 3, 1, 1, 1)

        self.label_14 = QLabel(self.tab_advanced_controls)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setMinimumSize(QSize(210, 20))
        self.label_14.setMaximumSize(QSize(300, 16777215))
        self.label_14.setFont(font1)
        self.label_14.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_13.addWidget(self.label_14, 4, 0, 1, 1)

        self.label_15 = QLabel(self.tab_advanced_controls)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setMinimumSize(QSize(210, 20))
        self.label_15.setMaximumSize(QSize(300, 16777215))
        self.label_15.setFont(font1)
        self.label_15.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_13.addWidget(self.label_15, 5, 0, 1, 1)

        self.comboBox_recombine_all = QComboBox(self.tab_advanced_controls)
        self.comboBox_recombine_all.addItem("")
        self.comboBox_recombine_all.addItem("")
        self.comboBox_recombine_all.setObjectName(u"comboBox_recombine_all")
        self.comboBox_recombine_all.setMinimumSize(QSize(200, 28))
        self.comboBox_recombine_all.setMaximumSize(QSize(200, 16777215))
        self.comboBox_recombine_all.setFont(font1)

        self.gridLayout_13.addWidget(self.comboBox_recombine_all, 4, 1, 1, 1)

        self.comboBox_second_order_incomplete = QComboBox(self.tab_advanced_controls)
        self.comboBox_second_order_incomplete.addItem("")
        self.comboBox_second_order_incomplete.addItem("")
        self.comboBox_second_order_incomplete.setObjectName(u"comboBox_second_order_incomplete")
        self.comboBox_second_order_incomplete.setMinimumSize(QSize(200, 28))
        self.comboBox_second_order_incomplete.setMaximumSize(QSize(200, 16777215))
        self.comboBox_second_order_incomplete.setFont(font1)

        self.gridLayout_13.addWidget(self.comboBox_second_order_incomplete, 5, 1, 1, 1)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_13.addItem(self.horizontalSpacer_10, 0, 2, 1, 1)

        self.tabWidget_main.addTab(self.tab_advanced_controls, "")
        self.tab_mesh_quality = QWidget()
        self.tab_mesh_quality.setObjectName(u"tab_mesh_quality")
        self.tab_mesh_quality.setEnabled(True)
        self.gridLayout_16 = QGridLayout(self.tab_mesh_quality)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.tableWidget_mesh_quality = QTableWidget(self.tab_mesh_quality)
        if (self.tableWidget_mesh_quality.columnCount() < 4):
            self.tableWidget_mesh_quality.setColumnCount(4)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget_mesh_quality.setHorizontalHeaderItem(0, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget_mesh_quality.setHorizontalHeaderItem(1, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget_mesh_quality.setHorizontalHeaderItem(2, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableWidget_mesh_quality.setHorizontalHeaderItem(3, __qtablewidgetitem6)
        if (self.tableWidget_mesh_quality.rowCount() < 4):
            self.tableWidget_mesh_quality.setRowCount(4)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableWidget_mesh_quality.setVerticalHeaderItem(0, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tableWidget_mesh_quality.setVerticalHeaderItem(1, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.tableWidget_mesh_quality.setVerticalHeaderItem(2, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.tableWidget_mesh_quality.setVerticalHeaderItem(3, __qtablewidgetitem10)
        self.tableWidget_mesh_quality.setObjectName(u"tableWidget_mesh_quality")
        self.tableWidget_mesh_quality.setMaximumSize(QSize(654654, 16777215))
        self.tableWidget_mesh_quality.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget_mesh_quality.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_mesh_quality.verticalHeader().setVisible(True)
        self.tableWidget_mesh_quality.verticalHeader().setStretchLastSection(False)

        self.gridLayout_16.addWidget(self.tableWidget_mesh_quality, 0, 0, 1, 1)

        self.frame_7 = QFrame(self.tab_mesh_quality)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_7.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_15 = QGridLayout(self.frame_7)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.pushButton_plot_histogram = QPushButton(self.frame_7)
        self.pushButton_plot_histogram.setObjectName(u"pushButton_plot_histogram")
        self.pushButton_plot_histogram.setEnabled(True)
        self.pushButton_plot_histogram.setMinimumSize(QSize(140, 30))
        self.pushButton_plot_histogram.setMaximumSize(QSize(150, 16777215))
        self.pushButton_plot_histogram.setAutoDefault(False)

        self.gridLayout_15.addWidget(self.pushButton_plot_histogram, 0, 0, 1, 1)

        self.pushButton_show_bad_elements = QPushButton(self.frame_7)
        self.pushButton_show_bad_elements.setObjectName(u"pushButton_show_bad_elements")
        self.pushButton_show_bad_elements.setEnabled(True)
        self.pushButton_show_bad_elements.setMinimumSize(QSize(140, 30))
        self.pushButton_show_bad_elements.setMaximumSize(QSize(150, 16777215))
        self.pushButton_show_bad_elements.setAutoDefault(False)

        self.gridLayout_15.addWidget(self.pushButton_show_bad_elements, 0, 1, 1, 1)


        self.gridLayout_16.addWidget(self.frame_7, 1, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_mesh_quality, "")

        self.gridLayout_14.addWidget(self.tabWidget_main, 0, 0, 1, 1)


        self.gridLayout_4.addWidget(self.frame_tab_widgets, 1, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_main, 1, 0, 1, 1)

        self.frame_buttons_2 = QFrame(Dialog)
        self.frame_buttons_2.setObjectName(u"frame_buttons_2")
        self.frame_buttons_2.setMinimumSize(QSize(0, 48))
        self.frame_buttons_2.setMaximumSize(QSize(16777215, 48))
        self.frame_buttons_2.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_buttons_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_11 = QGridLayout(self.frame_buttons_2)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setVerticalSpacing(0)
        self.gridLayout_11.setContentsMargins(6, 0, 6, 0)
        self.pushButton_apply_and_close = QPushButton(self.frame_buttons_2)
        self.pushButton_apply_and_close.setObjectName(u"pushButton_apply_and_close")
        self.pushButton_apply_and_close.setMinimumSize(QSize(72, 30))
        self.pushButton_apply_and_close.setMaximumSize(QSize(72, 30))
        self.pushButton_apply_and_close.setFont(font2)
        self.pushButton_apply_and_close.setStyleSheet(u"")
        self.pushButton_apply_and_close.setAutoDefault(False)
        self.pushButton_apply_and_close.setFlat(False)

        self.gridLayout_11.addWidget(self.pushButton_apply_and_close, 0, 3, 1, 1)

        self.pushButton_apply = QPushButton(self.frame_buttons_2)
        self.pushButton_apply.setObjectName(u"pushButton_apply")
        self.pushButton_apply.setMinimumSize(QSize(72, 30))
        self.pushButton_apply.setMaximumSize(QSize(72, 30))
        self.pushButton_apply.setFont(font2)
        self.pushButton_apply.setStyleSheet(u"")
        self.pushButton_apply.setAutoDefault(False)
        self.pushButton_apply.setFlat(False)

        self.gridLayout_11.addWidget(self.pushButton_apply, 0, 2, 1, 1)

        self.pushButton_cancel = QPushButton(self.frame_buttons_2)
        self.pushButton_cancel.setObjectName(u"pushButton_cancel")
        self.pushButton_cancel.setMinimumSize(QSize(72, 30))
        self.pushButton_cancel.setMaximumSize(QSize(72, 30))
        self.pushButton_cancel.setFont(font2)
        self.pushButton_cancel.setStyleSheet(u"")
        self.pushButton_cancel.setAutoDefault(False)
        self.pushButton_cancel.setFlat(False)

        self.gridLayout_11.addWidget(self.pushButton_cancel, 0, 0, 1, 1)

        self.horizontalSpacer_17 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_11.addItem(self.horizontalSpacer_17, 0, 1, 1, 1)


        self.gridLayout.addWidget(self.frame_buttons_2, 2, 0, 1, 1)

        QWidget.setTabOrder(self.comboBox_element_geometry, self.comboBox_element_order)
        QWidget.setTabOrder(self.comboBox_element_order, self.comboBox_volumes_interface_behavior)
        QWidget.setTabOrder(self.comboBox_volumes_interface_behavior, self.tabWidget_main)
        QWidget.setTabOrder(self.tabWidget_main, self.lineEdit_selected_ids)
        QWidget.setTabOrder(self.lineEdit_selected_ids, self.doubleSpinBox_local_mesh_size_control_element_size)
        QWidget.setTabOrder(self.doubleSpinBox_local_mesh_size_control_element_size, self.tableWidget_local_mesh_size_control_data)
        QWidget.setTabOrder(self.tableWidget_local_mesh_size_control_data, self.pushButton_delete)
        QWidget.setTabOrder(self.pushButton_delete, self.pushButton_add)
        QWidget.setTabOrder(self.pushButton_add, self.tableWidget_mesh_quality)
        QWidget.setTabOrder(self.tableWidget_mesh_quality, self.pushButton_plot_histogram)
        QWidget.setTabOrder(self.pushButton_plot_histogram, self.pushButton_show_bad_elements)
        QWidget.setTabOrder(self.pushButton_show_bad_elements, self.comboBox_volumes_interface_behavior)

        self.retranslateUi(Dialog)

        self.comboBox_volumes_interface_behavior.setCurrentIndex(1)
        self.pushButton_suppress_volumes.setDefault(False)
        self.tabWidget_main.setCurrentIndex(0)
        self.comboBox_local_mesh_size_control_entity_type.setCurrentIndex(0)
        self.comboBox_3d_algorithm.setCurrentIndex(0)
        self.pushButton_apply_and_close.setDefault(False)
        self.pushButton_apply.setDefault(False)
        self.pushButton_cancel.setDefault(False)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Mesher setup", None))
        self.comboBox_element_order.setItemText(0, QCoreApplication.translate("Dialog", u"Linear", None))
        self.comboBox_element_order.setItemText(1, QCoreApplication.translate("Dialog", u"Quadratic", None))

        self.label_20.setText(QCoreApplication.translate("Dialog", u"Volumes interface behavior:", None))
        self.comboBox_element_geometry.setItemText(0, QCoreApplication.translate("Dialog", u"Tetrahedral", None))
        self.comboBox_element_geometry.setItemText(1, QCoreApplication.translate("Dialog", u"Hexahedral", None))

        self.label_16.setText(QCoreApplication.translate("Dialog", u"Element geometry:", None))
        self.label_19.setText(QCoreApplication.translate("Dialog", u"Mesh quality metrics:", None))
        self.comboBox_volumes_interface_behavior.setItemText(0, QCoreApplication.translate("Dialog", u"Disconnect nodes", None))
        self.comboBox_volumes_interface_behavior.setItemText(1, QCoreApplication.translate("Dialog", u"Merge nodes", None))

        self.label_10.setText(QCoreApplication.translate("Dialog", u"Element order:", None))
        self.label_21.setText(QCoreApplication.translate("Dialog", u"Volumes to suppress:", None))
        self.label_201.setText(QCoreApplication.translate("Dialog", u"Volumes interface behavior:", None))
        self.comboBox_mesh_quality_metrics.setItemText(0, QCoreApplication.translate("Dialog", u"Disabled", None))
        self.comboBox_mesh_quality_metrics.setItemText(1, QCoreApplication.translate("Dialog", u"Enabled", None))

        self.pushButton_suppress_volumes.setText(QCoreApplication.translate("Dialog", u"Add volumes", None))
        self.label_suppressed_volume_count.setText("")
        self.label_28.setText(QCoreApplication.translate("Dialog", u"Min. element size:", None))
        self.label_29.setText(QCoreApplication.translate("Dialog", u"[mm]", None))
        self.label_30.setText(QCoreApplication.translate("Dialog", u"Max. element size:", None))
        self.label_31.setText(QCoreApplication.translate("Dialog", u"Size factor:", None))
        self.label_32.setText(QCoreApplication.translate("Dialog", u"[mm]", None))
        self.lineEdit_geometry_tolerance.setText(QCoreApplication.translate("Dialog", u"1e-6", None))
        self.label_33.setText(QCoreApplication.translate("Dialog", u"Geometry tolerance:", None))
#if QT_CONFIG(tooltip)
        self.pushButton_syncrhonize.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Synchronize the minimum and maximum sizes</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_syncrhonize.setText("")
        self.label_34.setText(QCoreApplication.translate("Dialog", u"[mm]", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_global_settings), QCoreApplication.translate("Dialog", u"Global settings", None))
        self.pushButton_add.setText(QCoreApplication.translate("Dialog", u"Add", None))
        self.pushButton_delete.setText(QCoreApplication.translate("Dialog", u"Delete", None))
        ___qtablewidgetitem = self.tableWidget_local_mesh_size_control_data.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Dialog", u"Element size [mm]", None));
        ___qtablewidgetitem1 = self.tableWidget_local_mesh_size_control_data.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Dialog", u"Selection type", None));
        ___qtablewidgetitem2 = self.tableWidget_local_mesh_size_control_data.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Dialog", u"Selection ID", None));
        self.lineEdit_selected_ids.setText("")
        self.label_7.setText(QCoreApplication.translate("Dialog", u"Element size: ", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"[mm]", None))
        self.label_selected_ids.setText(QCoreApplication.translate("Dialog", u"Selected entities ID:", None))
        self.comboBox_local_mesh_size_control_entity_type.setItemText(0, QCoreApplication.translate("Dialog", u"Surfaces", None))
        self.comboBox_local_mesh_size_control_entity_type.setItemText(1, QCoreApplication.translate("Dialog", u"Volumes", None))

        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_local_mesh_size_control), QCoreApplication.translate("Dialog", u"Local size control", None))
        self.label_13.setText(QCoreApplication.translate("Dialog", u"Recombination algorithm:", None))
        self.label_12.setText(QCoreApplication.translate("Dialog", u"Subdivision algorithm:", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"2D algorithm:", None))
        self.comboBox_2d_algorithm.setItemText(0, QCoreApplication.translate("Dialog", u"MeshAdapt", None))
        self.comboBox_2d_algorithm.setItemText(1, QCoreApplication.translate("Dialog", u"Automatic", None))
        self.comboBox_2d_algorithm.setItemText(2, QCoreApplication.translate("Dialog", u"Initial Mesh Only", None))
        self.comboBox_2d_algorithm.setItemText(3, QCoreApplication.translate("Dialog", u"Delaunay", None))
        self.comboBox_2d_algorithm.setItemText(4, QCoreApplication.translate("Dialog", u"Frontal-Delaunay", None))
        self.comboBox_2d_algorithm.setItemText(5, QCoreApplication.translate("Dialog", u"Quasi Structured Quads", None))

        self.label_11.setText(QCoreApplication.translate("Dialog", u"3D algorithm:", None))
        self.comboBox_recombination_algorithm.setItemText(0, QCoreApplication.translate("Dialog", u"Simple", None))
        self.comboBox_recombination_algorithm.setItemText(1, QCoreApplication.translate("Dialog", u"Blossom", None))
        self.comboBox_recombination_algorithm.setItemText(2, QCoreApplication.translate("Dialog", u"Simple Full-Quad", None))
        self.comboBox_recombination_algorithm.setItemText(3, QCoreApplication.translate("Dialog", u"Blossom Full-Quad", None))

        self.comboBox_3d_algorithm.setItemText(0, QCoreApplication.translate("Dialog", u"Delaunay", None))
        self.comboBox_3d_algorithm.setItemText(1, QCoreApplication.translate("Dialog", u"Frontal-Delaunay", None))
        self.comboBox_3d_algorithm.setItemText(2, QCoreApplication.translate("Dialog", u"HXT_3D", None))

        self.comboBox_subdivision_algorithm.setItemText(0, QCoreApplication.translate("Dialog", u"None", None))
        self.comboBox_subdivision_algorithm.setItemText(1, QCoreApplication.translate("Dialog", u"All quads", None))
        self.comboBox_subdivision_algorithm.setItemText(2, QCoreApplication.translate("Dialog", u"All hexas", None))

        self.label_14.setText(QCoreApplication.translate("Dialog", u"Recombine all triangular meshes:", None))
        self.label_15.setText(QCoreApplication.translate("Dialog", u"Second order incomplete", None))
        self.comboBox_recombine_all.setItemText(0, QCoreApplication.translate("Dialog", u"No", None))
        self.comboBox_recombine_all.setItemText(1, QCoreApplication.translate("Dialog", u"Yes", None))

        self.comboBox_second_order_incomplete.setItemText(0, QCoreApplication.translate("Dialog", u"No", None))
        self.comboBox_second_order_incomplete.setItemText(1, QCoreApplication.translate("Dialog", u"Yes", None))

        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_advanced_controls), QCoreApplication.translate("Dialog", u"Advanced Controls", None))
        ___qtablewidgetitem3 = self.tableWidget_mesh_quality.horizontalHeaderItem(0)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Dialog", u"Worst Value", None));
        ___qtablewidgetitem4 = self.tableWidget_mesh_quality.horizontalHeaderItem(1)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Dialog", u"Average", None));
        ___qtablewidgetitem5 = self.tableWidget_mesh_quality.horizontalHeaderItem(2)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Dialog", u"Std. Deviation", None));
        ___qtablewidgetitem6 = self.tableWidget_mesh_quality.horizontalHeaderItem(3)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("Dialog", u"Bad elements", None));
        ___qtablewidgetitem7 = self.tableWidget_mesh_quality.verticalHeaderItem(0)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("Dialog", u"Gamma", None));
        ___qtablewidgetitem8 = self.tableWidget_mesh_quality.verticalHeaderItem(1)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("Dialog", u"Volume", None));
        ___qtablewidgetitem9 = self.tableWidget_mesh_quality.verticalHeaderItem(2)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("Dialog", u"Min SJ", None));
        ___qtablewidgetitem10 = self.tableWidget_mesh_quality.verticalHeaderItem(3)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("Dialog", u"Aspect Ratio", None));
        self.pushButton_plot_histogram.setText(QCoreApplication.translate("Dialog", u"Plot Histogram", None))
        self.pushButton_show_bad_elements.setText(QCoreApplication.translate("Dialog", u"Show bad elements", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_mesh_quality), QCoreApplication.translate("Dialog", u"Mesh quality", None))
        self.pushButton_apply_and_close.setText(QCoreApplication.translate("Dialog", u"Ok", None))
        self.pushButton_apply.setText(QCoreApplication.translate("Dialog", u"Apply", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
    # retranslateUi



class MesherSetupInputs_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame_title: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
                - frame_main: QFrame
                    - (Layout): QGridLayout
                            - frame_element_formulation: QFrame
                                - (Layout): QGridLayout
                                        - comboBox_element_order: QComboBox
                                        - label_20: QLabel
                                        - comboBox_element_geometry: QComboBox
                                        - label_16: QLabel
                                        - label_19: QLabel
                                        - comboBox_volumes_interface_behavior: QComboBox
                                        - label_10: QLabel
                                        - label_21: QLabel
                                        - label_20: QLabel
                                        - comboBox_mesh_quality_metrics: QComboBox
                                        - pushButton_suppress_volumes: QPushButton
                                        - label_suppressed_volume_count: QLabel
                            - frame_tab_widgets: QFrame
                                - (Layout): QGridLayout
                                        - tabWidget_main: QTabWidget
                                            - tab_global_settings: QWidget
                                                - (Layout): QGridLayout
                                                        - frame_6: QFrame
                                                            - (Layout): QGridLayout
                                                                    - label_28: QLabel
                                                                    - label_29: QLabel
                                                                    - doubleSpinBox_minimum_element_size: QDoubleSpinBox
                                                                    - label_30: QLabel
                                                                    - label_31: QLabel
                                                                    - doubleSpinBox_size_factor: QDoubleSpinBox
                                                                    - doubleSpinBox_maximum_element_size: QDoubleSpinBox
                                                                    - label_32: QLabel
                                                                    - lineEdit_geometry_tolerance: QLineEdit
                                                                    - label_33: QLabel
                                                                    - pushButton_syncrhonize: QPushButton
                                                                    - label_34: QLabel
                                            - tab_local_mesh_size_control: QWidget
                                                - (Layout): QGridLayout
                                                        - frame_11: QFrame
                                                            - (Layout): QGridLayout
                                                                    - pushButton_add: QPushButton
                                                                    - pushButton_delete: QPushButton
                                                        - tableWidget_local_mesh_size_control_data: QTableWidget
                                                        - frame_13: QFrame
                                                            - (Layout): QGridLayout
                                                                    - lineEdit_selected_ids: QLineEdit
                                                                    - label_7: QLabel
                                                                    - doubleSpinBox_local_mesh_size_control_element_size: QDoubleSpinBox
                                                                    - label_8: QLabel
                                                                    - label_selected_ids: QLabel
                                                                    - comboBox_local_mesh_size_control_entity_type: QComboBox
                                            - tab_advanced_controls: QWidget
                                                - (Layout): QGridLayout
                                                        - label_13: QLabel
                                                        - label_12: QLabel
                                                        - label_6: QLabel
                                                        - comboBox_2d_algorithm: QComboBox
                                                        - label_11: QLabel
                                                        - comboBox_recombination_algorithm: QComboBox
                                                        - comboBox_3d_algorithm: QComboBox
                                                        - comboBox_subdivision_algorithm: QComboBox
                                                        - label_14: QLabel
                                                        - label_15: QLabel
                                                        - comboBox_recombine_all: QComboBox
                                                        - comboBox_second_order_incomplete: QComboBox
                                            - tab_mesh_quality: QWidget
                                                - (Layout): QGridLayout
                                                        - tableWidget_mesh_quality: QTableWidget
                                                        - frame_7: QFrame
                                                            - (Layout): QGridLayout
                                                                    - pushButton_plot_histogram: QPushButton
                                                                    - pushButton_show_bad_elements: QPushButton
                - frame_buttons_2: QFrame
                    - (Layout): QGridLayout
                            - pushButton_apply_and_close: QPushButton
                            - pushButton_apply: QPushButton
                            - pushButton_cancel: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
