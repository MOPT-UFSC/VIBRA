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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QDoubleSpinBox,
    QFrame, QGridLayout, QHeaderView, QLabel,
    QLineEdit, QPushButton, QScrollArea, QSizePolicy,
    QSpacerItem, QTabWidget, QTableWidget, QTableWidgetItem,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(596, 603)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setVerticalSpacing(4)
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.frame_main = QFrame(Dialog)
        self.frame_main.setObjectName(u"frame_main")
        self.frame_main.setFrameShape(QFrame.Box)
        self.frame_main.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_main)
        self.gridLayout_4.setSpacing(2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(2, 2, 2, 2)
        self.frame_element_formulation = QFrame(self.frame_main)
        self.frame_element_formulation.setObjectName(u"frame_element_formulation")
        self.frame_element_formulation.setFrameShape(QFrame.NoFrame)
        self.frame_element_formulation.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_element_formulation)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setHorizontalSpacing(6)
        self.gridLayout_2.setContentsMargins(4, 4, 4, 4)
        self.comboBox_element_type = QComboBox(self.frame_element_formulation)
        self.comboBox_element_type.addItem("")
        self.comboBox_element_type.addItem("")
        self.comboBox_element_type.setObjectName(u"comboBox_element_type")
        self.comboBox_element_type.setMinimumSize(QSize(120, 28))
        self.comboBox_element_type.setMaximumSize(QSize(140, 16777215))
        font = QFont()
        font.setPointSize(10)
        self.comboBox_element_type.setFont(font)

        self.gridLayout_2.addWidget(self.comboBox_element_type, 0, 2, 1, 1)

        self.label_10 = QLabel(self.frame_element_formulation)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(180, 20))
        self.label_10.setMaximumSize(QSize(240, 16777215))
        self.label_10.setFont(font)
        self.label_10.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_10, 1, 1, 1, 1)

        self.label_19 = QLabel(self.frame_element_formulation)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setMinimumSize(QSize(180, 20))
        self.label_19.setMaximumSize(QSize(240, 16777215))
        self.label_19.setFont(font)
        self.label_19.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_19, 2, 1, 1, 1)

        self.comboBox_shape_function = QComboBox(self.frame_element_formulation)
        self.comboBox_shape_function.addItem("")
        self.comboBox_shape_function.addItem("")
        self.comboBox_shape_function.setObjectName(u"comboBox_shape_function")
        self.comboBox_shape_function.setMinimumSize(QSize(120, 28))
        self.comboBox_shape_function.setMaximumSize(QSize(140, 16777215))
        self.comboBox_shape_function.setFont(font)

        self.gridLayout_2.addWidget(self.comboBox_shape_function, 1, 2, 1, 1)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_9, 1, 3, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 1, 0, 1, 1)

        self.label_20 = QLabel(self.frame_element_formulation)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setMinimumSize(QSize(180, 20))
        self.label_20.setMaximumSize(QSize(240, 16777215))
        self.label_20.setFont(font)
        self.label_20.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_20, 3, 1, 1, 1)

        self.label_16 = QLabel(self.frame_element_formulation)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setMinimumSize(QSize(180, 20))
        self.label_16.setMaximumSize(QSize(240, 16777215))
        self.label_16.setFont(font)
        self.label_16.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_16, 0, 1, 1, 1)

        self.comboBox_mesh_quality_metrics = QComboBox(self.frame_element_formulation)
        self.comboBox_mesh_quality_metrics.addItem("")
        self.comboBox_mesh_quality_metrics.addItem("")
        self.comboBox_mesh_quality_metrics.setObjectName(u"comboBox_mesh_quality_metrics")
        self.comboBox_mesh_quality_metrics.setMinimumSize(QSize(120, 28))
        self.comboBox_mesh_quality_metrics.setMaximumSize(QSize(140, 16777215))
        self.comboBox_mesh_quality_metrics.setFont(font)

        self.gridLayout_2.addWidget(self.comboBox_mesh_quality_metrics, 2, 2, 1, 1)

        self.comboBox_volumes_interface_behavior = QComboBox(self.frame_element_formulation)
        self.comboBox_volumes_interface_behavior.addItem("")
        self.comboBox_volumes_interface_behavior.addItem("")
        self.comboBox_volumes_interface_behavior.setObjectName(u"comboBox_volumes_interface_behavior")
        self.comboBox_volumes_interface_behavior.setMinimumSize(QSize(120, 28))
        self.comboBox_volumes_interface_behavior.setMaximumSize(QSize(140, 16777215))
        self.comboBox_volumes_interface_behavior.setFont(font)
        self.comboBox_volumes_interface_behavior.setMinimumContentsLength(0)

        self.gridLayout_2.addWidget(self.comboBox_volumes_interface_behavior, 3, 2, 1, 1)


        self.gridLayout_4.addWidget(self.frame_element_formulation, 0, 0, 1, 1)

        self.frame_tab_widgets = QFrame(self.frame_main)
        self.frame_tab_widgets.setObjectName(u"frame_tab_widgets")
        self.frame_tab_widgets.setMinimumSize(QSize(0, 300))
        self.frame_tab_widgets.setFrameShape(QFrame.NoFrame)
        self.frame_tab_widgets.setFrameShadow(QFrame.Raised)
        self.gridLayout_14 = QGridLayout(self.frame_tab_widgets)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.tabWidget_main = QTabWidget(self.frame_tab_widgets)
        self.tabWidget_main.setObjectName(u"tabWidget_main")
        self.tabWidget_main.setEnabled(True)
        font1 = QFont()
        font1.setPointSize(9)
        self.tabWidget_main.setFont(font1)
        self.tabWidget_main.setTabShape(QTabWidget.Rounded)
        self.tabWidget_main.setTabBarAutoHide(False)
        self.tab_global_settings = QWidget()
        self.tab_global_settings.setObjectName(u"tab_global_settings")
        self.gridLayout_9 = QGridLayout(self.tab_global_settings)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(6, 6, 6, 6)
        self.tabWidget_global_settings = QTabWidget(self.tab_global_settings)
        self.tabWidget_global_settings.setObjectName(u"tabWidget_global_settings")
        self.tab_main = QWidget()
        self.tab_main.setObjectName(u"tab_main")
        self.gridLayout_6 = QGridLayout(self.tab_main)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.frame_6 = QFrame(self.tab_main)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setMinimumSize(QSize(0, 62))
        self.frame_6.setMaximumSize(QSize(16777215, 180))
        self.frame_6.setFrameShape(QFrame.NoFrame)
        self.gridLayout_10 = QGridLayout(self.frame_6)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setHorizontalSpacing(6)
        self.gridLayout_10.setContentsMargins(4, 4, 4, 4)
        self.doubleSpinBox_minimum_element_size = QDoubleSpinBox(self.frame_6)
        self.doubleSpinBox_minimum_element_size.setObjectName(u"doubleSpinBox_minimum_element_size")
        self.doubleSpinBox_minimum_element_size.setMinimumSize(QSize(140, 28))
        self.doubleSpinBox_minimum_element_size.setMaximumSize(QSize(140, 16777215))
        self.doubleSpinBox_minimum_element_size.setFont(font)
        self.doubleSpinBox_minimum_element_size.setAlignment(Qt.AlignCenter)
        self.doubleSpinBox_minimum_element_size.setDecimals(2)
        self.doubleSpinBox_minimum_element_size.setMinimum(0.010000000000000)
        self.doubleSpinBox_minimum_element_size.setMaximum(2000.000000000000000)
        self.doubleSpinBox_minimum_element_size.setSingleStep(2.000000000000000)
        self.doubleSpinBox_minimum_element_size.setValue(50.000000000000000)

        self.gridLayout_10.addWidget(self.doubleSpinBox_minimum_element_size, 2, 2, 1, 1)

        self.doubleSpinBox_size_factor = QDoubleSpinBox(self.frame_6)
        self.doubleSpinBox_size_factor.setObjectName(u"doubleSpinBox_size_factor")
        self.doubleSpinBox_size_factor.setMinimumSize(QSize(140, 28))
        self.doubleSpinBox_size_factor.setMaximumSize(QSize(140, 16777215))
        self.doubleSpinBox_size_factor.setFont(font)
        self.doubleSpinBox_size_factor.setAlignment(Qt.AlignCenter)
        self.doubleSpinBox_size_factor.setDecimals(2)
        self.doubleSpinBox_size_factor.setMinimum(0.000000000000000)
        self.doubleSpinBox_size_factor.setMaximum(2.000000000000000)
        self.doubleSpinBox_size_factor.setSingleStep(0.100000000000000)
        self.doubleSpinBox_size_factor.setValue(0.000000000000000)

        self.gridLayout_10.addWidget(self.doubleSpinBox_size_factor, 3, 2, 1, 1)

        self.doubleSpinBox_maximum_element_size = QDoubleSpinBox(self.frame_6)
        self.doubleSpinBox_maximum_element_size.setObjectName(u"doubleSpinBox_maximum_element_size")
        self.doubleSpinBox_maximum_element_size.setMinimumSize(QSize(140, 28))
        self.doubleSpinBox_maximum_element_size.setMaximumSize(QSize(140, 16777215))
        self.doubleSpinBox_maximum_element_size.setFont(font)
        self.doubleSpinBox_maximum_element_size.setAlignment(Qt.AlignCenter)
        self.doubleSpinBox_maximum_element_size.setDecimals(2)
        self.doubleSpinBox_maximum_element_size.setMinimum(0.010000000000000)
        self.doubleSpinBox_maximum_element_size.setMaximum(2000.000000000000000)
        self.doubleSpinBox_maximum_element_size.setSingleStep(2.000000000000000)
        self.doubleSpinBox_maximum_element_size.setValue(50.000000000000000)

        self.gridLayout_10.addWidget(self.doubleSpinBox_maximum_element_size, 1, 2, 1, 1)

        self.lineEdit_geometry_tolerance = QLineEdit(self.frame_6)
        self.lineEdit_geometry_tolerance.setObjectName(u"lineEdit_geometry_tolerance")
        self.lineEdit_geometry_tolerance.setMinimumSize(QSize(140, 28))
        self.lineEdit_geometry_tolerance.setMaximumSize(QSize(140, 16777215))
        self.lineEdit_geometry_tolerance.setFont(font)
        self.lineEdit_geometry_tolerance.setAlignment(Qt.AlignCenter)

        self.gridLayout_10.addWidget(self.lineEdit_geometry_tolerance, 4, 2, 1, 1)

        self.label_3 = QLabel(self.frame_6)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(140, 20))
        self.label_3.setMaximumSize(QSize(240, 16777215))
        self.label_3.setFont(font)
        self.label_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_3, 1, 1, 1, 1)

        self.label_5 = QLabel(self.frame_6)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(40, 0))
        self.label_5.setMaximumSize(QSize(48, 16777215))
        self.label_5.setFont(font)

        self.gridLayout_10.addWidget(self.label_5, 4, 3, 1, 1)

        self.label_4 = QLabel(self.frame_6)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(40, 0))
        self.label_4.setMaximumSize(QSize(48, 16777215))
        self.label_4.setFont(font)

        self.gridLayout_10.addWidget(self.label_4, 1, 3, 1, 1)

        self.label_9 = QLabel(self.frame_6)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMinimumSize(QSize(140, 20))
        self.label_9.setMaximumSize(QSize(240, 16777215))
        self.label_9.setFont(font)
        self.label_9.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_9, 3, 1, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_10.addItem(self.horizontalSpacer_8, 1, 0, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_10.addItem(self.horizontalSpacer_7, 1, 5, 1, 1)

        self.label_18 = QLabel(self.frame_6)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setMinimumSize(QSize(40, 0))
        self.label_18.setMaximumSize(QSize(48, 16777215))
        self.label_18.setFont(font)

        self.gridLayout_10.addWidget(self.label_18, 2, 3, 1, 1)

        self.label_17 = QLabel(self.frame_6)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setMinimumSize(QSize(140, 20))
        self.label_17.setMaximumSize(QSize(240, 16777215))
        self.label_17.setFont(font)
        self.label_17.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_17, 2, 1, 1, 1)

        self.pushButton_syncrhonize = QPushButton(self.frame_6)
        self.pushButton_syncrhonize.setObjectName(u"pushButton_syncrhonize")
        icon = QIcon()
        icon.addFile(u":/icons/sync_enabled.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_syncrhonize.setIcon(icon)
        self.pushButton_syncrhonize.setIconSize(QSize(20, 20))
        self.pushButton_syncrhonize.setAutoDefault(False)

        self.gridLayout_10.addWidget(self.pushButton_syncrhonize, 1, 4, 1, 1)

        self.label_2 = QLabel(self.frame_6)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(140, 20))
        self.label_2.setMaximumSize(QSize(240, 16777215))
        self.label_2.setFont(font)
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_2, 4, 1, 1, 1)


        self.gridLayout_6.addWidget(self.frame_6, 0, 0, 1, 1)

        self.tabWidget_global_settings.addTab(self.tab_main, "")
        self.tab_advanced_controls = QWidget()
        self.tab_advanced_controls.setObjectName(u"tab_advanced_controls")
        self.gridLayout_11 = QGridLayout(self.tab_advanced_controls)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setContentsMargins(6, 6, 6, 6)
        self.scrollArea = QScrollArea(self.tab_advanced_controls)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setFrameShape(QFrame.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 526, 247))
        self.gridLayout_17 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.label_15 = QLabel(self.scrollAreaWidgetContents)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setMinimumSize(QSize(210, 20))
        self.label_15.setMaximumSize(QSize(300, 16777215))
        self.label_15.setFont(font)
        self.label_15.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_17.addWidget(self.label_15, 5, 1, 1, 1)

        self.comboBox_second_order_incomplete = QComboBox(self.scrollAreaWidgetContents)
        self.comboBox_second_order_incomplete.addItem("")
        self.comboBox_second_order_incomplete.addItem("")
        self.comboBox_second_order_incomplete.setObjectName(u"comboBox_second_order_incomplete")
        self.comboBox_second_order_incomplete.setMinimumSize(QSize(200, 28))
        self.comboBox_second_order_incomplete.setMaximumSize(QSize(200, 16777215))
        self.comboBox_second_order_incomplete.setFont(font)

        self.gridLayout_17.addWidget(self.comboBox_second_order_incomplete, 5, 2, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_17.addItem(self.horizontalSpacer_5, 0, 3, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_17.addItem(self.horizontalSpacer_6, 0, 0, 1, 1)

        self.label_14 = QLabel(self.scrollAreaWidgetContents)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setMinimumSize(QSize(210, 20))
        self.label_14.setMaximumSize(QSize(300, 16777215))
        self.label_14.setFont(font)
        self.label_14.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_17.addWidget(self.label_14, 4, 1, 1, 1)

        self.label_6 = QLabel(self.scrollAreaWidgetContents)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(210, 20))
        self.label_6.setMaximumSize(QSize(300, 16777215))
        self.label_6.setFont(font)
        self.label_6.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_17.addWidget(self.label_6, 0, 1, 1, 1)

        self.comboBox_2d_algorithm = QComboBox(self.scrollAreaWidgetContents)
        self.comboBox_2d_algorithm.addItem("")
        self.comboBox_2d_algorithm.addItem("")
        self.comboBox_2d_algorithm.addItem("")
        self.comboBox_2d_algorithm.addItem("")
        self.comboBox_2d_algorithm.addItem("")
        self.comboBox_2d_algorithm.addItem("")
        self.comboBox_2d_algorithm.setObjectName(u"comboBox_2d_algorithm")
        self.comboBox_2d_algorithm.setMinimumSize(QSize(200, 28))
        self.comboBox_2d_algorithm.setMaximumSize(QSize(200, 16777215))
        self.comboBox_2d_algorithm.setFont(font)

        self.gridLayout_17.addWidget(self.comboBox_2d_algorithm, 0, 2, 1, 1)

        self.comboBox_3d_algorithm = QComboBox(self.scrollAreaWidgetContents)
        self.comboBox_3d_algorithm.addItem("")
        self.comboBox_3d_algorithm.addItem("")
        self.comboBox_3d_algorithm.addItem("")
        self.comboBox_3d_algorithm.setObjectName(u"comboBox_3d_algorithm")
        self.comboBox_3d_algorithm.setMinimumSize(QSize(200, 28))
        self.comboBox_3d_algorithm.setMaximumSize(QSize(200, 16777215))
        self.comboBox_3d_algorithm.setFont(font)

        self.gridLayout_17.addWidget(self.comboBox_3d_algorithm, 1, 2, 1, 1)

        self.label_13 = QLabel(self.scrollAreaWidgetContents)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setMinimumSize(QSize(210, 20))
        self.label_13.setMaximumSize(QSize(300, 16777215))
        self.label_13.setFont(font)
        self.label_13.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_17.addWidget(self.label_13, 2, 1, 1, 1)

        self.comboBox_recombine_all = QComboBox(self.scrollAreaWidgetContents)
        self.comboBox_recombine_all.addItem("")
        self.comboBox_recombine_all.addItem("")
        self.comboBox_recombine_all.setObjectName(u"comboBox_recombine_all")
        self.comboBox_recombine_all.setMinimumSize(QSize(200, 28))
        self.comboBox_recombine_all.setMaximumSize(QSize(200, 16777215))
        self.comboBox_recombine_all.setFont(font)

        self.gridLayout_17.addWidget(self.comboBox_recombine_all, 4, 2, 1, 1)

        self.label_11 = QLabel(self.scrollAreaWidgetContents)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMinimumSize(QSize(210, 20))
        self.label_11.setMaximumSize(QSize(300, 16777215))
        self.label_11.setFont(font)
        self.label_11.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_17.addWidget(self.label_11, 1, 1, 1, 1)

        self.comboBox_recombination_algorithm = QComboBox(self.scrollAreaWidgetContents)
        self.comboBox_recombination_algorithm.addItem("")
        self.comboBox_recombination_algorithm.addItem("")
        self.comboBox_recombination_algorithm.addItem("")
        self.comboBox_recombination_algorithm.addItem("")
        self.comboBox_recombination_algorithm.setObjectName(u"comboBox_recombination_algorithm")
        self.comboBox_recombination_algorithm.setMinimumSize(QSize(200, 28))
        self.comboBox_recombination_algorithm.setMaximumSize(QSize(200, 16777215))
        self.comboBox_recombination_algorithm.setFont(font)

        self.gridLayout_17.addWidget(self.comboBox_recombination_algorithm, 2, 2, 1, 1)

        self.label_12 = QLabel(self.scrollAreaWidgetContents)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setMinimumSize(QSize(210, 20))
        self.label_12.setMaximumSize(QSize(300, 16777215))
        self.label_12.setFont(font)
        self.label_12.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_17.addWidget(self.label_12, 3, 1, 1, 1)

        self.comboBox_subdivision_algorithm = QComboBox(self.scrollAreaWidgetContents)
        self.comboBox_subdivision_algorithm.addItem("")
        self.comboBox_subdivision_algorithm.addItem("")
        self.comboBox_subdivision_algorithm.addItem("")
        self.comboBox_subdivision_algorithm.setObjectName(u"comboBox_subdivision_algorithm")
        self.comboBox_subdivision_algorithm.setMinimumSize(QSize(200, 28))
        self.comboBox_subdivision_algorithm.setMaximumSize(QSize(200, 16777215))
        self.comboBox_subdivision_algorithm.setFont(font)

        self.gridLayout_17.addWidget(self.comboBox_subdivision_algorithm, 3, 2, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_11.addWidget(self.scrollArea, 0, 0, 1, 1)

        self.tabWidget_global_settings.addTab(self.tab_advanced_controls, "")

        self.gridLayout_9.addWidget(self.tabWidget_global_settings, 0, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_global_settings, "")
        self.tab_local_refining = QWidget()
        self.tab_local_refining.setObjectName(u"tab_local_refining")
        self.gridLayout_7 = QGridLayout(self.tab_local_refining)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.tableWidget_refining_mesh_data = QTableWidget(self.tab_local_refining)
        if (self.tableWidget_refining_mesh_data.columnCount() < 3):
            self.tableWidget_refining_mesh_data.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget_refining_mesh_data.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget_refining_mesh_data.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget_refining_mesh_data.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.tableWidget_refining_mesh_data.setObjectName(u"tableWidget_refining_mesh_data")
        self.tableWidget_refining_mesh_data.setMaximumSize(QSize(16777215, 16777215))
        self.tableWidget_refining_mesh_data.setShowGrid(False)
        self.tableWidget_refining_mesh_data.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_refining_mesh_data.verticalHeader().setVisible(False)
        self.tableWidget_refining_mesh_data.verticalHeader().setStretchLastSection(False)

        self.gridLayout_7.addWidget(self.tableWidget_refining_mesh_data, 2, 1, 1, 1)

        self.frame_11 = QFrame(self.tab_local_refining)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setMinimumSize(QSize(0, 48))
        self.frame_11.setFrameShape(QFrame.NoFrame)
        self.gridLayout_12 = QGridLayout(self.frame_11)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setContentsMargins(4, 4, 4, 4)
        self.pushButton_add = QPushButton(self.frame_11)
        self.pushButton_add.setObjectName(u"pushButton_add")
        self.pushButton_add.setMinimumSize(QSize(68, 28))
        self.pushButton_add.setMaximumSize(QSize(140, 16777215))
        self.pushButton_add.setFont(font)
        self.pushButton_add.setAutoDefault(False)

        self.gridLayout_12.addWidget(self.pushButton_add, 0, 1, 1, 1)

        self.pushButton_delete = QPushButton(self.frame_11)
        self.pushButton_delete.setObjectName(u"pushButton_delete")
        self.pushButton_delete.setMinimumSize(QSize(68, 28))
        self.pushButton_delete.setMaximumSize(QSize(140, 16777215))
        self.pushButton_delete.setFont(font)
        self.pushButton_delete.setAutoDefault(False)

        self.gridLayout_12.addWidget(self.pushButton_delete, 0, 0, 1, 1)


        self.gridLayout_7.addWidget(self.frame_11, 3, 1, 1, 1)

        self.frame_13 = QFrame(self.tab_local_refining)
        self.frame_13.setObjectName(u"frame_13")
        self.frame_13.setMinimumSize(QSize(0, 68))
        self.frame_13.setFrameShape(QFrame.NoFrame)
        self.gridLayout_8 = QGridLayout(self.frame_13)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setHorizontalSpacing(6)
        self.gridLayout_8.setContentsMargins(4, 4, 4, 4)
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_3, 2, 0, 1, 1)

        self.label_7 = QLabel(self.frame_13)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(160, 20))
        self.label_7.setMaximumSize(QSize(16777215, 160))
        self.label_7.setFont(font)
        self.label_7.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_7, 2, 1, 1, 1)

        self.doubleSpinBox_refined_element_size = QDoubleSpinBox(self.frame_13)
        self.doubleSpinBox_refined_element_size.setObjectName(u"doubleSpinBox_refined_element_size")
        self.doubleSpinBox_refined_element_size.setMinimumSize(QSize(0, 28))
        self.doubleSpinBox_refined_element_size.setMaximumSize(QSize(200, 16777215))
        self.doubleSpinBox_refined_element_size.setFont(font)
        self.doubleSpinBox_refined_element_size.setAlignment(Qt.AlignCenter)
        self.doubleSpinBox_refined_element_size.setDecimals(2)
        self.doubleSpinBox_refined_element_size.setMinimum(0.010000000000000)
        self.doubleSpinBox_refined_element_size.setMaximum(2000.000000000000000)
        self.doubleSpinBox_refined_element_size.setSingleStep(1.000000000000000)
        self.doubleSpinBox_refined_element_size.setValue(10.000000000000000)

        self.gridLayout_8.addWidget(self.doubleSpinBox_refined_element_size, 2, 2, 1, 1)

        self.label_8 = QLabel(self.frame_13)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMinimumSize(QSize(0, 20))
        self.label_8.setFont(font)

        self.gridLayout_8.addWidget(self.label_8, 2, 3, 1, 1)

        self.label_selected_ids = QLabel(self.frame_13)
        self.label_selected_ids.setObjectName(u"label_selected_ids")
        self.label_selected_ids.setMinimumSize(QSize(160, 20))
        self.label_selected_ids.setMaximumSize(QSize(16777215, 160))
        self.label_selected_ids.setFont(font)
        self.label_selected_ids.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_selected_ids, 1, 1, 1, 1)

        self.lineEdit_selected_ids = QLineEdit(self.frame_13)
        self.lineEdit_selected_ids.setObjectName(u"lineEdit_selected_ids")
        self.lineEdit_selected_ids.setMinimumSize(QSize(0, 28))
        self.lineEdit_selected_ids.setMaximumSize(QSize(200, 16777215))
        self.lineEdit_selected_ids.setFont(font)

        self.gridLayout_8.addWidget(self.lineEdit_selected_ids, 1, 2, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_4, 2, 4, 1, 1)


        self.gridLayout_7.addWidget(self.frame_13, 0, 1, 1, 1)

        self.tabWidget_main.addTab(self.tab_local_refining, "")
        self.tab_mesh_quality = QWidget()
        self.tab_mesh_quality.setObjectName(u"tab_mesh_quality")
        self.tab_mesh_quality.setEnabled(True)
        self.gridLayout_16 = QGridLayout(self.tab_mesh_quality)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.tableWidget_mesh_quality = QTableWidget(self.tab_mesh_quality)
        if (self.tableWidget_mesh_quality.columnCount() < 5):
            self.tableWidget_mesh_quality.setColumnCount(5)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget_mesh_quality.setHorizontalHeaderItem(0, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget_mesh_quality.setHorizontalHeaderItem(1, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget_mesh_quality.setHorizontalHeaderItem(2, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableWidget_mesh_quality.setHorizontalHeaderItem(3, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableWidget_mesh_quality.setHorizontalHeaderItem(4, __qtablewidgetitem7)
        self.tableWidget_mesh_quality.setObjectName(u"tableWidget_mesh_quality")
        self.tableWidget_mesh_quality.setMaximumSize(QSize(654654, 16777215))
        self.tableWidget_mesh_quality.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_mesh_quality.verticalHeader().setVisible(False)
        self.tableWidget_mesh_quality.verticalHeader().setStretchLastSection(False)

        self.gridLayout_16.addWidget(self.tableWidget_mesh_quality, 0, 0, 1, 1)

        self.frame_7 = QFrame(self.tab_mesh_quality)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.NoFrame)
        self.frame_7.setFrameShadow(QFrame.Raised)
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

        self.frame_title = QFrame(Dialog)
        self.frame_title.setObjectName(u"frame_title")
        self.frame_title.setMinimumSize(QSize(0, 48))
        self.frame_title.setMaximumSize(QSize(16777215, 48))
        self.frame_title.setFrameShape(QFrame.Box)
        self.frame_title.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_title)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label = QLabel(self.frame_title)
        self.label.setObjectName(u"label")
        font2 = QFont()
        font2.setPointSize(11)
        self.label.setFont(font2)
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_title, 0, 0, 1, 1)

        self.frame_buttons = QFrame(Dialog)
        self.frame_buttons.setObjectName(u"frame_buttons")
        self.frame_buttons.setMinimumSize(QSize(0, 48))
        self.frame_buttons.setMaximumSize(QSize(16777215, 48))
        self.frame_buttons.setFrameShape(QFrame.NoFrame)
        self.frame_buttons.setFrameShadow(QFrame.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_buttons)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(4, 4, 4, 4)
        self.pushButton_exit = QPushButton(self.frame_buttons)
        self.pushButton_exit.setObjectName(u"pushButton_exit")
        self.pushButton_exit.setMinimumSize(QSize(140, 30))
        self.pushButton_exit.setMaximumSize(QSize(140, 30))
        self.pushButton_exit.setFont(font)
        self.pushButton_exit.setAutoDefault(False)

        self.gridLayout_5.addWidget(self.pushButton_exit, 0, 0, 1, 1)

        self.pushButton_generate_mesh = QPushButton(self.frame_buttons)
        self.pushButton_generate_mesh.setObjectName(u"pushButton_generate_mesh")
        self.pushButton_generate_mesh.setMinimumSize(QSize(140, 30))
        self.pushButton_generate_mesh.setMaximumSize(QSize(140, 30))
        self.pushButton_generate_mesh.setFont(font)
        self.pushButton_generate_mesh.setAutoDefault(True)

        self.gridLayout_5.addWidget(self.pushButton_generate_mesh, 0, 1, 1, 1)


        self.gridLayout.addWidget(self.frame_buttons, 3, 0, 1, 1)

        QWidget.setTabOrder(self.comboBox_element_type, self.comboBox_shape_function)
        QWidget.setTabOrder(self.comboBox_shape_function, self.comboBox_mesh_quality_metrics)
        QWidget.setTabOrder(self.comboBox_mesh_quality_metrics, self.comboBox_volumes_interface_behavior)
        QWidget.setTabOrder(self.comboBox_volumes_interface_behavior, self.tabWidget_main)
        QWidget.setTabOrder(self.tabWidget_main, self.tabWidget_global_settings)
        QWidget.setTabOrder(self.tabWidget_global_settings, self.doubleSpinBox_maximum_element_size)
        QWidget.setTabOrder(self.doubleSpinBox_maximum_element_size, self.doubleSpinBox_minimum_element_size)
        QWidget.setTabOrder(self.doubleSpinBox_minimum_element_size, self.doubleSpinBox_size_factor)
        QWidget.setTabOrder(self.doubleSpinBox_size_factor, self.lineEdit_geometry_tolerance)
        QWidget.setTabOrder(self.lineEdit_geometry_tolerance, self.pushButton_generate_mesh)
        QWidget.setTabOrder(self.pushButton_generate_mesh, self.pushButton_exit)
        QWidget.setTabOrder(self.pushButton_exit, self.pushButton_syncrhonize)
        QWidget.setTabOrder(self.pushButton_syncrhonize, self.comboBox_2d_algorithm)
        QWidget.setTabOrder(self.comboBox_2d_algorithm, self.comboBox_3d_algorithm)
        QWidget.setTabOrder(self.comboBox_3d_algorithm, self.comboBox_recombination_algorithm)
        QWidget.setTabOrder(self.comboBox_recombination_algorithm, self.comboBox_subdivision_algorithm)
        QWidget.setTabOrder(self.comboBox_subdivision_algorithm, self.comboBox_recombine_all)
        QWidget.setTabOrder(self.comboBox_recombine_all, self.comboBox_second_order_incomplete)
        QWidget.setTabOrder(self.comboBox_second_order_incomplete, self.lineEdit_selected_ids)
        QWidget.setTabOrder(self.lineEdit_selected_ids, self.doubleSpinBox_refined_element_size)
        QWidget.setTabOrder(self.doubleSpinBox_refined_element_size, self.pushButton_add)
        QWidget.setTabOrder(self.pushButton_add, self.pushButton_delete)
        QWidget.setTabOrder(self.pushButton_delete, self.pushButton_show_bad_elements)
        QWidget.setTabOrder(self.pushButton_show_bad_elements, self.pushButton_plot_histogram)
        QWidget.setTabOrder(self.pushButton_plot_histogram, self.tableWidget_mesh_quality)
        QWidget.setTabOrder(self.tableWidget_mesh_quality, self.scrollArea)
        QWidget.setTabOrder(self.scrollArea, self.tableWidget_refining_mesh_data)

        self.retranslateUi(Dialog)

        self.comboBox_volumes_interface_behavior.setCurrentIndex(1)
        self.tabWidget_main.setCurrentIndex(0)
        self.tabWidget_global_settings.setCurrentIndex(0)
        self.comboBox_3d_algorithm.setCurrentIndex(0)
        self.pushButton_exit.setDefault(False)
        self.pushButton_generate_mesh.setDefault(False)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.comboBox_element_type.setItemText(0, QCoreApplication.translate("Dialog", u"Tetrahedral", None))
        self.comboBox_element_type.setItemText(1, QCoreApplication.translate("Dialog", u"Hexahedral", None))

        self.label_10.setText(QCoreApplication.translate("Dialog", u"Shape function:", None))
        self.label_19.setText(QCoreApplication.translate("Dialog", u"Mesh quality metrics:", None))
        self.comboBox_shape_function.setItemText(0, QCoreApplication.translate("Dialog", u"Linear", None))
        self.comboBox_shape_function.setItemText(1, QCoreApplication.translate("Dialog", u"Quadratic", None))

        self.label_20.setText(QCoreApplication.translate("Dialog", u"Volumes interface behavior:", None))
        self.label_16.setText(QCoreApplication.translate("Dialog", u"Element type:", None))
        self.comboBox_mesh_quality_metrics.setItemText(0, QCoreApplication.translate("Dialog", u"Disabled", None))
        self.comboBox_mesh_quality_metrics.setItemText(1, QCoreApplication.translate("Dialog", u"Enabled", None))

        self.comboBox_volumes_interface_behavior.setItemText(0, QCoreApplication.translate("Dialog", u"Disconnect nodes", None))
        self.comboBox_volumes_interface_behavior.setItemText(1, QCoreApplication.translate("Dialog", u"Merge nodes", None))

        self.lineEdit_geometry_tolerance.setText(QCoreApplication.translate("Dialog", u"1e-6", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Max. element size:", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"[mm]", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"[mm]", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", u"Size factor:", None))
        self.label_18.setText(QCoreApplication.translate("Dialog", u"[mm]", None))
        self.label_17.setText(QCoreApplication.translate("Dialog", u"Min. element size:", None))
#if QT_CONFIG(tooltip)
        self.pushButton_syncrhonize.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Synchronize the minimum and maximum sizes</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_syncrhonize.setText("")
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Geometry tolerance:", None))
        self.tabWidget_global_settings.setTabText(self.tabWidget_global_settings.indexOf(self.tab_main), QCoreApplication.translate("Dialog", u"Main", None))
        self.label_15.setText(QCoreApplication.translate("Dialog", u"Second order incomplete", None))
        self.comboBox_second_order_incomplete.setItemText(0, QCoreApplication.translate("Dialog", u"No", None))
        self.comboBox_second_order_incomplete.setItemText(1, QCoreApplication.translate("Dialog", u"Yes", None))

        self.label_14.setText(QCoreApplication.translate("Dialog", u"Recombine all triangular meshes:", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"2D algorithm:", None))
        self.comboBox_2d_algorithm.setItemText(0, QCoreApplication.translate("Dialog", u"MeshAdapt", None))
        self.comboBox_2d_algorithm.setItemText(1, QCoreApplication.translate("Dialog", u"Automatic", None))
        self.comboBox_2d_algorithm.setItemText(2, QCoreApplication.translate("Dialog", u"Initial Mesh Only", None))
        self.comboBox_2d_algorithm.setItemText(3, QCoreApplication.translate("Dialog", u"Delaunay", None))
        self.comboBox_2d_algorithm.setItemText(4, QCoreApplication.translate("Dialog", u"Frontal-Delaunay", None))
        self.comboBox_2d_algorithm.setItemText(5, QCoreApplication.translate("Dialog", u"Quasi Structured Quads", None))

        self.comboBox_3d_algorithm.setItemText(0, QCoreApplication.translate("Dialog", u"Delaunay", None))
        self.comboBox_3d_algorithm.setItemText(1, QCoreApplication.translate("Dialog", u"Frontal-Delaunay", None))
        self.comboBox_3d_algorithm.setItemText(2, QCoreApplication.translate("Dialog", u"HXT_3D", None))

        self.label_13.setText(QCoreApplication.translate("Dialog", u"Recombination algorithm:", None))
        self.comboBox_recombine_all.setItemText(0, QCoreApplication.translate("Dialog", u"No", None))
        self.comboBox_recombine_all.setItemText(1, QCoreApplication.translate("Dialog", u"Yes", None))

        self.label_11.setText(QCoreApplication.translate("Dialog", u"3D algorithm:", None))
        self.comboBox_recombination_algorithm.setItemText(0, QCoreApplication.translate("Dialog", u"Simple", None))
        self.comboBox_recombination_algorithm.setItemText(1, QCoreApplication.translate("Dialog", u"Blossom", None))
        self.comboBox_recombination_algorithm.setItemText(2, QCoreApplication.translate("Dialog", u"Simple Full-Quad", None))
        self.comboBox_recombination_algorithm.setItemText(3, QCoreApplication.translate("Dialog", u"Blossom Full-Quad", None))

        self.label_12.setText(QCoreApplication.translate("Dialog", u"Subdivision algorithm:", None))
        self.comboBox_subdivision_algorithm.setItemText(0, QCoreApplication.translate("Dialog", u"None", None))
        self.comboBox_subdivision_algorithm.setItemText(1, QCoreApplication.translate("Dialog", u"All quads", None))
        self.comboBox_subdivision_algorithm.setItemText(2, QCoreApplication.translate("Dialog", u"All hexas", None))

        self.tabWidget_global_settings.setTabText(self.tabWidget_global_settings.indexOf(self.tab_advanced_controls), QCoreApplication.translate("Dialog", u"Advanced controls", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_global_settings), QCoreApplication.translate("Dialog", u"Global settings", None))
        ___qtablewidgetitem = self.tableWidget_refining_mesh_data.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Dialog", u"Element size [mm]", None));
        ___qtablewidgetitem1 = self.tableWidget_refining_mesh_data.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Dialog", u"Selection type", None));
        ___qtablewidgetitem2 = self.tableWidget_refining_mesh_data.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Dialog", u"Selection ID", None));
        self.pushButton_add.setText(QCoreApplication.translate("Dialog", u"Add", None))
        self.pushButton_delete.setText(QCoreApplication.translate("Dialog", u"Delete", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"Refined element size: ", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"[mm]", None))
        self.label_selected_ids.setText(QCoreApplication.translate("Dialog", u"Selected ID:", None))
        self.lineEdit_selected_ids.setText("")
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_local_refining), QCoreApplication.translate("Dialog", u"Local refining", None))
        ___qtablewidgetitem3 = self.tableWidget_mesh_quality.horizontalHeaderItem(0)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Dialog", u"Parameter", None));
        ___qtablewidgetitem4 = self.tableWidget_mesh_quality.horizontalHeaderItem(1)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Dialog", u"Worst Value", None));
        ___qtablewidgetitem5 = self.tableWidget_mesh_quality.horizontalHeaderItem(2)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Dialog", u"Average", None));
        ___qtablewidgetitem6 = self.tableWidget_mesh_quality.horizontalHeaderItem(3)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("Dialog", u"Std. Deviation", None));
        ___qtablewidgetitem7 = self.tableWidget_mesh_quality.horizontalHeaderItem(4)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("Dialog", u"Bad elements", None));
        self.pushButton_plot_histogram.setText(QCoreApplication.translate("Dialog", u"Plot Histogram", None))
        self.pushButton_show_bad_elements.setText(QCoreApplication.translate("Dialog", u"Show bad elements", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_mesh_quality), QCoreApplication.translate("Dialog", u"Mesh quality", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Mesher setup", None))
        self.pushButton_exit.setText(QCoreApplication.translate("Dialog", u"Exit", None))
        self.pushButton_generate_mesh.setText(QCoreApplication.translate("Dialog", u"Generate mesh", None))
    # retranslateUi



class MesherSetupInputs_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame_main: QFrame
                    - (Layout): QGridLayout
                            - frame_element_formulation: QFrame
                                - (Layout): QGridLayout
                                        - comboBox_element_type: QComboBox
                                        - label_10: QLabel
                                        - label_19: QLabel
                                        - comboBox_shape_function: QComboBox
                                        - label_20: QLabel
                                        - label_16: QLabel
                                        - comboBox_mesh_quality_metrics: QComboBox
                                        - comboBox_volumes_interface_behavior: QComboBox
                            - frame_tab_widgets: QFrame
                                - (Layout): QGridLayout
                                        - tabWidget_main: QTabWidget
                                            - tab_global_settings: QWidget
                                                - (Layout): QGridLayout
                                                        - tabWidget_global_settings: QTabWidget
                                                            - tab_main: QWidget
                                                                - (Layout): QGridLayout
                                                                        - frame_6: QFrame
                                                                            - (Layout): QGridLayout
                                                                                    - doubleSpinBox_minimum_element_size: QDoubleSpinBox
                                                                                    - doubleSpinBox_size_factor: QDoubleSpinBox
                                                                                    - doubleSpinBox_maximum_element_size: QDoubleSpinBox
                                                                                    - lineEdit_geometry_tolerance: QLineEdit
                                                                                    - label_3: QLabel
                                                                                    - label_5: QLabel
                                                                                    - label_4: QLabel
                                                                                    - label_9: QLabel
                                                                                    - label_18: QLabel
                                                                                    - label_17: QLabel
                                                                                    - pushButton_syncrhonize: QPushButton
                                                                                    - label_2: QLabel
                                                            - tab_advanced_controls: QWidget
                                                                - (Layout): QGridLayout
                                                                        - scrollArea: QScrollArea
                                                                            - scrollAreaWidgetContents: QWidget
                                                                                - (Layout): QGridLayout
                                                                                        - label_15: QLabel
                                                                                        - comboBox_second_order_incomplete: QComboBox
                                                                                        - label_14: QLabel
                                                                                        - label_6: QLabel
                                                                                        - comboBox_2d_algorithm: QComboBox
                                                                                        - comboBox_3d_algorithm: QComboBox
                                                                                        - label_13: QLabel
                                                                                        - comboBox_recombine_all: QComboBox
                                                                                        - label_11: QLabel
                                                                                        - comboBox_recombination_algorithm: QComboBox
                                                                                        - label_12: QLabel
                                                                                        - comboBox_subdivision_algorithm: QComboBox
                                            - tab_local_refining: QWidget
                                                - (Layout): QGridLayout
                                                        - tableWidget_refining_mesh_data: QTableWidget
                                                        - frame_11: QFrame
                                                            - (Layout): QGridLayout
                                                                    - pushButton_add: QPushButton
                                                                    - pushButton_delete: QPushButton
                                                        - frame_13: QFrame
                                                            - (Layout): QGridLayout
                                                                    - label_7: QLabel
                                                                    - doubleSpinBox_refined_element_size: QDoubleSpinBox
                                                                    - label_8: QLabel
                                                                    - label_selected_ids: QLabel
                                                                    - lineEdit_selected_ids: QLineEdit
                                            - tab_mesh_quality: QWidget
                                                - (Layout): QGridLayout
                                                        - tableWidget_mesh_quality: QTableWidget
                                                        - frame_7: QFrame
                                                            - (Layout): QGridLayout
                                                                    - pushButton_plot_histogram: QPushButton
                                                                    - pushButton_show_bad_elements: QPushButton
                - frame_title: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
                - frame_buttons: QFrame
                    - (Layout): QGridLayout
                            - pushButton_exit: QPushButton
                            - pushButton_generate_mesh: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
