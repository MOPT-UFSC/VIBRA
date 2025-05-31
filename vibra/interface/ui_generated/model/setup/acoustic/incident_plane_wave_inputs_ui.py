# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'incident_plane_wave_inputs.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
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
        Dialog.resize(460, 460)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(420, 360))
        Dialog.setMaximumSize(QSize(460, 460))
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
        self.frame_2.setMinimumSize(QSize(380, 0))
        self.frame_2.setMaximumSize(QSize(16777215, 480))
        self.frame_2.setFrameShape(QFrame.Box)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.tabWidget_main = QTabWidget(self.frame_2)
        self.tabWidget_main.setObjectName(u"tabWidget_main")
        self.tabWidget_main.setMinimumSize(QSize(360, 240))
        self.tabWidget_main.setMaximumSize(QSize(16777215, 240))
        font1 = QFont()
        font1.setPointSize(10)
        self.tabWidget_main.setFont(font1)
        self.tab_constant_values = QWidget()
        self.tab_constant_values.setObjectName(u"tab_constant_values")
        self.gridLayout_12 = QGridLayout(self.tab_constant_values)
        self.gridLayout_12.setSpacing(2)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setContentsMargins(2, 6, 2, 6)
        self.frame_8 = QFrame(self.tab_constant_values)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setMinimumSize(QSize(340, 80))
        self.frame_8.setMaximumSize(QSize(16777215, 240))
        font2 = QFont()
        font2.setPointSize(11)
        self.frame_8.setFont(font2)
        self.frame_8.setFrameShape(QFrame.NoFrame)
        self.frame_8.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame_8)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.label_21 = QLabel(self.frame_8)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setMinimumSize(QSize(40, 28))
        self.label_21.setMaximumSize(QSize(60, 28))
        font3 = QFont()
        font3.setFamilies([u"MS Shell Dlg 2"])
        font3.setPointSize(10)
        font3.setBold(False)
        font3.setItalic(False)
        self.label_21.setFont(font3)
        self.label_21.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_21, 3, 4, 1, 1)

        self.label_4 = QLabel(self.frame_8)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(80, 26))
        self.label_4.setMaximumSize(QSize(80, 26))
        self.label_4.setFont(font3)
        self.label_4.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_4, 2, 2, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_4, 3, 5, 1, 1)

        self.lineEdit_real_value_x = QLineEdit(self.frame_8)
        self.lineEdit_real_value_x.setObjectName(u"lineEdit_real_value_x")
        self.lineEdit_real_value_x.setMinimumSize(QSize(80, 28))
        self.lineEdit_real_value_x.setMaximumSize(QSize(80, 28))
        self.lineEdit_real_value_x.setFont(font3)
        self.lineEdit_real_value_x.setStyleSheet(u"")
        self.lineEdit_real_value_x.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_real_value_x, 3, 2, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_3, 3, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 0, 2, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_2, 6, 2, 1, 1)

        self.label_component_x = QLabel(self.frame_8)
        self.label_component_x.setObjectName(u"label_component_x")
        self.label_component_x.setMinimumSize(QSize(100, 28))
        self.label_component_x.setMaximumSize(QSize(140, 28))
        self.label_component_x.setFont(font3)
        self.label_component_x.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_component_x, 3, 1, 1, 1)

        self.lineEdit_imag_value_x = QLineEdit(self.frame_8)
        self.lineEdit_imag_value_x.setObjectName(u"lineEdit_imag_value_x")
        self.lineEdit_imag_value_x.setMinimumSize(QSize(80, 28))
        self.lineEdit_imag_value_x.setMaximumSize(QSize(80, 28))
        self.lineEdit_imag_value_x.setFont(font3)
        self.lineEdit_imag_value_x.setStyleSheet(u"")
        self.lineEdit_imag_value_x.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_imag_value_x, 3, 3, 1, 1)

        self.label_5 = QLabel(self.frame_8)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(80, 26))
        self.label_5.setMaximumSize(QSize(80, 26))
        self.label_5.setFont(font3)
        self.label_5.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_5, 2, 3, 1, 1)

        self.lineEdit_real_value_y = QLineEdit(self.frame_8)
        self.lineEdit_real_value_y.setObjectName(u"lineEdit_real_value_y")
        self.lineEdit_real_value_y.setMinimumSize(QSize(80, 28))
        self.lineEdit_real_value_y.setMaximumSize(QSize(80, 28))
        self.lineEdit_real_value_y.setFont(font3)
        self.lineEdit_real_value_y.setStyleSheet(u"")
        self.lineEdit_real_value_y.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_real_value_y, 4, 2, 1, 1)

        self.lineEdit_imag_value_y = QLineEdit(self.frame_8)
        self.lineEdit_imag_value_y.setObjectName(u"lineEdit_imag_value_y")
        self.lineEdit_imag_value_y.setMinimumSize(QSize(80, 28))
        self.lineEdit_imag_value_y.setMaximumSize(QSize(80, 28))
        self.lineEdit_imag_value_y.setFont(font3)
        self.lineEdit_imag_value_y.setStyleSheet(u"")
        self.lineEdit_imag_value_y.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_imag_value_y, 4, 3, 1, 1)

        self.label_22 = QLabel(self.frame_8)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setMinimumSize(QSize(40, 28))
        self.label_22.setMaximumSize(QSize(60, 28))
        self.label_22.setFont(font3)
        self.label_22.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_22, 4, 4, 1, 1)

        self.label_24 = QLabel(self.frame_8)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setMinimumSize(QSize(40, 28))
        self.label_24.setMaximumSize(QSize(60, 28))
        self.label_24.setFont(font3)
        self.label_24.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_24, 5, 4, 1, 1)

        self.label_component_y = QLabel(self.frame_8)
        self.label_component_y.setObjectName(u"label_component_y")
        self.label_component_y.setMinimumSize(QSize(100, 28))
        self.label_component_y.setMaximumSize(QSize(140, 28))
        self.label_component_y.setFont(font3)
        self.label_component_y.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_component_y, 4, 1, 1, 1)

        self.lineEdit_real_value_z = QLineEdit(self.frame_8)
        self.lineEdit_real_value_z.setObjectName(u"lineEdit_real_value_z")
        self.lineEdit_real_value_z.setMinimumSize(QSize(80, 28))
        self.lineEdit_real_value_z.setMaximumSize(QSize(80, 28))
        self.lineEdit_real_value_z.setFont(font3)
        self.lineEdit_real_value_z.setStyleSheet(u"")
        self.lineEdit_real_value_z.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_real_value_z, 5, 2, 1, 1)

        self.label_component_z = QLabel(self.frame_8)
        self.label_component_z.setObjectName(u"label_component_z")
        self.label_component_z.setMinimumSize(QSize(100, 28))
        self.label_component_z.setMaximumSize(QSize(140, 28))
        self.label_component_z.setFont(font3)
        self.label_component_z.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_component_z, 5, 1, 1, 1)

        self.lineEdit_imag_value_z = QLineEdit(self.frame_8)
        self.lineEdit_imag_value_z.setObjectName(u"lineEdit_imag_value_z")
        self.lineEdit_imag_value_z.setMinimumSize(QSize(80, 28))
        self.lineEdit_imag_value_z.setMaximumSize(QSize(80, 28))
        self.lineEdit_imag_value_z.setFont(font3)
        self.lineEdit_imag_value_z.setStyleSheet(u"")
        self.lineEdit_imag_value_z.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_imag_value_z, 5, 3, 1, 1)


        self.gridLayout_12.addWidget(self.frame_8, 0, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_constant_values, "")
        self.tab_load_tables = QWidget()
        self.tab_load_tables.setObjectName(u"tab_load_tables")
        self.gridLayout_3 = QGridLayout(self.tab_load_tables)
        self.gridLayout_3.setSpacing(2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(2, 6, 2, 6)
        self.frame_9 = QFrame(self.tab_load_tables)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setMinimumSize(QSize(260, 0))
        self.frame_9.setMaximumSize(QSize(600, 200))
        self.frame_9.setFrameShape(QFrame.NoFrame)
        self.frame_9.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_9)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setHorizontalSpacing(4)
        self.gridLayout_2.setVerticalSpacing(6)
        self.gridLayout_2.setContentsMargins(0, 4, 0, 0)
        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_8, 1, 0, 1, 1)

        self.pushButton_load_table_x = QPushButton(self.frame_9)
        self.pushButton_load_table_x.setObjectName(u"pushButton_load_table_x")
        self.pushButton_load_table_x.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton_load_table_x.sizePolicy().hasHeightForWidth())
        self.pushButton_load_table_x.setSizePolicy(sizePolicy1)
        self.pushButton_load_table_x.setMinimumSize(QSize(62, 26))
        self.pushButton_load_table_x.setMaximumSize(QSize(62, 26))
        self.pushButton_load_table_x.setFont(font3)
        self.pushButton_load_table_x.setStyleSheet(u"")

        self.gridLayout_2.addWidget(self.pushButton_load_table_x, 1, 3, 1, 1)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_9, 1, 5, 1, 1)

        self.lineEdit_table_path_x = QLineEdit(self.frame_9)
        self.lineEdit_table_path_x.setObjectName(u"lineEdit_table_path_x")
        self.lineEdit_table_path_x.setEnabled(True)
        self.lineEdit_table_path_x.setMinimumSize(QSize(220, 26))
        self.lineEdit_table_path_x.setMaximumSize(QSize(240, 26))
        font4 = QFont()
        font4.setPointSize(9)
        font4.setBold(False)
        self.lineEdit_table_path_x.setFont(font4)
        self.lineEdit_table_path_x.setStyleSheet(u"")
        self.lineEdit_table_path_x.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_table_path_x, 1, 2, 1, 1)

        self.pushButton_load_table_y = QPushButton(self.frame_9)
        self.pushButton_load_table_y.setObjectName(u"pushButton_load_table_y")
        self.pushButton_load_table_y.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.pushButton_load_table_y.sizePolicy().hasHeightForWidth())
        self.pushButton_load_table_y.setSizePolicy(sizePolicy1)
        self.pushButton_load_table_y.setMinimumSize(QSize(62, 26))
        self.pushButton_load_table_y.setMaximumSize(QSize(62, 26))
        self.pushButton_load_table_y.setFont(font3)
        self.pushButton_load_table_y.setStyleSheet(u"")

        self.gridLayout_2.addWidget(self.pushButton_load_table_y, 2, 3, 1, 1)

        self.lineEdit_table_path_z = QLineEdit(self.frame_9)
        self.lineEdit_table_path_z.setObjectName(u"lineEdit_table_path_z")
        self.lineEdit_table_path_z.setEnabled(True)
        self.lineEdit_table_path_z.setMinimumSize(QSize(220, 26))
        self.lineEdit_table_path_z.setMaximumSize(QSize(240, 26))
        self.lineEdit_table_path_z.setFont(font4)
        self.lineEdit_table_path_z.setStyleSheet(u"")
        self.lineEdit_table_path_z.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_table_path_z, 3, 2, 1, 1)

        self.lineEdit_table_path_y = QLineEdit(self.frame_9)
        self.lineEdit_table_path_y.setObjectName(u"lineEdit_table_path_y")
        self.lineEdit_table_path_y.setEnabled(True)
        self.lineEdit_table_path_y.setMinimumSize(QSize(220, 26))
        self.lineEdit_table_path_y.setMaximumSize(QSize(240, 26))
        self.lineEdit_table_path_y.setFont(font4)
        self.lineEdit_table_path_y.setStyleSheet(u"")
        self.lineEdit_table_path_y.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_table_path_y, 2, 2, 1, 1)

        self.pushButton_load_table_z = QPushButton(self.frame_9)
        self.pushButton_load_table_z.setObjectName(u"pushButton_load_table_z")
        self.pushButton_load_table_z.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.pushButton_load_table_z.sizePolicy().hasHeightForWidth())
        self.pushButton_load_table_z.setSizePolicy(sizePolicy1)
        self.pushButton_load_table_z.setMinimumSize(QSize(62, 26))
        self.pushButton_load_table_z.setMaximumSize(QSize(62, 26))
        self.pushButton_load_table_z.setFont(font3)
        self.pushButton_load_table_z.setStyleSheet(u"")

        self.gridLayout_2.addWidget(self.pushButton_load_table_z, 3, 3, 1, 1)

        self.label_component_x_2 = QLabel(self.frame_9)
        self.label_component_x_2.setObjectName(u"label_component_x_2")
        self.label_component_x_2.setMinimumSize(QSize(100, 28))
        self.label_component_x_2.setMaximumSize(QSize(140, 28))
        self.label_component_x_2.setFont(font3)
        self.label_component_x_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_component_x_2, 1, 1, 1, 1)

        self.label_component_x_4 = QLabel(self.frame_9)
        self.label_component_x_4.setObjectName(u"label_component_x_4")
        self.label_component_x_4.setMinimumSize(QSize(100, 28))
        self.label_component_x_4.setMaximumSize(QSize(140, 28))
        self.label_component_x_4.setFont(font3)
        self.label_component_x_4.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_component_x_4, 3, 1, 1, 1)

        self.label_component_x_3 = QLabel(self.frame_9)
        self.label_component_x_3.setObjectName(u"label_component_x_3")
        self.label_component_x_3.setMinimumSize(QSize(100, 28))
        self.label_component_x_3.setMaximumSize(QSize(140, 28))
        self.label_component_x_3.setFont(font3)
        self.label_component_x_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_component_x_3, 2, 1, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer_3, 4, 2, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer_4, 0, 2, 1, 1)


        self.gridLayout_3.addWidget(self.frame_9, 0, 0, 1, 1)

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
        self.frame_3.setMaximumSize(QSize(480, 40))
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
        self.pushButton_reset.setFont(font3)
        self.pushButton_reset.setStyleSheet(u"")

        self.gridLayout_8.addWidget(self.pushButton_reset, 0, 0, 1, 1)

        self.pushButton_remove = QPushButton(self.frame_3)
        self.pushButton_remove.setObjectName(u"pushButton_remove")
        self.pushButton_remove.setMinimumSize(QSize(100, 28))
        self.pushButton_remove.setMaximumSize(QSize(100, 28))
        self.pushButton_remove.setFont(font3)
        self.pushButton_remove.setStyleSheet(u"")

        self.gridLayout_8.addWidget(self.pushButton_remove, 0, 1, 1, 1)


        self.gridLayout_9.addWidget(self.frame_3, 1, 0, 1, 1)

        self.treeWidget_incident_plane_wave = QTreeWidget(self.tab_list)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter);
        self.treeWidget_incident_plane_wave.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_incident_plane_wave.setObjectName(u"treeWidget_incident_plane_wave")
        self.treeWidget_incident_plane_wave.setMinimumSize(QSize(320, 100))
        self.treeWidget_incident_plane_wave.setMaximumSize(QSize(400, 200))
        font5 = QFont()
        font5.setFamilies([u"MS Shell Dlg 2"])
        font5.setPointSize(9)
        font5.setItalic(False)
        self.treeWidget_incident_plane_wave.setFont(font5)
        self.treeWidget_incident_plane_wave.setIndentation(1)
        self.treeWidget_incident_plane_wave.setHeaderHidden(False)
        self.treeWidget_incident_plane_wave.header().setHighlightSections(False)
        self.treeWidget_incident_plane_wave.header().setProperty(u"showSortIndicator", False)
        self.treeWidget_incident_plane_wave.header().setStretchLastSection(True)

        self.gridLayout_9.addWidget(self.treeWidget_incident_plane_wave, 0, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_list, "")

        self.gridLayout_4.addWidget(self.tabWidget_main, 2, 0, 1, 1)

        self.frame_4 = QFrame(self.frame_2)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(360, 40))
        self.frame_4.setMaximumSize(QSize(16777215, 80))
        self.frame_4.setFrameShape(QFrame.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_4)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setHorizontalSpacing(6)
        self.gridLayout_5.setVerticalSpacing(2)
        self.gridLayout_5.setContentsMargins(2, 2, 2, 2)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer, 0, 3, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_2, 0, 0, 1, 1)

        self.label_2 = QLabel(self.frame_4)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(80, 28))
        self.label_2.setMaximumSize(QSize(120, 28))
        self.label_2.setFont(font1)
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_2, 0, 1, 1, 1)

        self.lineEdit_selection_id = QLineEdit(self.frame_4)
        self.lineEdit_selection_id.setObjectName(u"lineEdit_selection_id")
        self.lineEdit_selection_id.setMinimumSize(QSize(120, 28))
        self.lineEdit_selection_id.setMaximumSize(QSize(120, 28))
        self.lineEdit_selection_id.setFont(font3)
        self.lineEdit_selection_id.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_selection_id.setStyleSheet(u"")
        self.lineEdit_selection_id.setAlignment(Qt.AlignCenter)

        self.gridLayout_5.addWidget(self.lineEdit_selection_id, 0, 2, 1, 1)

        self.label_19 = QLabel(self.frame_4)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setMinimumSize(QSize(80, 28))
        self.label_19.setMaximumSize(QSize(120, 28))
        self.label_19.setFont(font3)
        self.label_19.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_19, 1, 1, 1, 1)

        self.comboBox_wave_direction = QComboBox(self.frame_4)
        self.comboBox_wave_direction.addItem("")
        self.comboBox_wave_direction.addItem("")
        self.comboBox_wave_direction.setObjectName(u"comboBox_wave_direction")
        self.comboBox_wave_direction.setMinimumSize(QSize(120, 28))
        self.comboBox_wave_direction.setMaximumSize(QSize(16777215, 28))
        self.comboBox_wave_direction.setFont(font1)

        self.gridLayout_5.addWidget(self.comboBox_wave_direction, 1, 2, 1, 1)


        self.gridLayout_4.addWidget(self.frame_4, 0, 0, 2, 1)


        self.gridLayout_7.addWidget(self.frame_2, 1, 0, 1, 1)

        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(380, 48))
        self.frame.setMaximumSize(QSize(16777215, 48))
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setLineWidth(1)
        self.gridLayout_6 = QGridLayout(self.frame)
        self.gridLayout_6.setSpacing(4)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(4, 4, 4, 4)
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        font6 = QFont()
        font6.setFamilies([u"MS Shell Dlg 2"])
        font6.setPointSize(11)
        font6.setBold(False)
        font6.setItalic(False)
        self.label.setFont(font6)
        self.label.setTextFormat(Qt.AutoText)
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout_6.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout_7.addWidget(self.frame, 0, 0, 1, 1)

        self.frame_11 = QFrame(Dialog)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setMinimumSize(QSize(340, 48))
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
        self.pushButton_attribute.setFont(font3)
        self.pushButton_attribute.setStyleSheet(u"")

        self.gridLayout_14.addWidget(self.pushButton_attribute, 0, 1, 1, 1)

        self.pushButton_exit = QPushButton(self.frame_11)
        self.pushButton_exit.setObjectName(u"pushButton_exit")
        self.pushButton_exit.setMinimumSize(QSize(100, 28))
        self.pushButton_exit.setMaximumSize(QSize(100, 28))
        self.pushButton_exit.setFont(font3)
        self.pushButton_exit.setStyleSheet(u"")

        self.gridLayout_14.addWidget(self.pushButton_exit, 0, 0, 1, 1)


        self.gridLayout_7.addWidget(self.frame_11, 2, 0, 1, 1)


        self.retranslateUi(Dialog)

        self.tabWidget_main.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Set incident plane wave", None))
#if QT_CONFIG(whatsthis)
        Dialog.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.label_21.setText(QCoreApplication.translate("Dialog", u"[Pa]", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Real", None))
        self.label_component_x.setText(QCoreApplication.translate("Dialog", u"Pressure (x-axis):", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"Imaginary", None))
        self.label_22.setText(QCoreApplication.translate("Dialog", u"[Pa]", None))
        self.label_24.setText(QCoreApplication.translate("Dialog", u"[Pa]", None))
        self.label_component_y.setText(QCoreApplication.translate("Dialog", u"Pressure (y-axis):", None))
        self.label_component_z.setText(QCoreApplication.translate("Dialog", u"Pressure (z-axis):", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_constant_values), QCoreApplication.translate("Dialog", u"Constant values", None))
        self.pushButton_load_table_x.setText(QCoreApplication.translate("Dialog", u"Search", None))
        self.pushButton_load_table_y.setText(QCoreApplication.translate("Dialog", u"Search", None))
        self.pushButton_load_table_z.setText(QCoreApplication.translate("Dialog", u"Search", None))
        self.label_component_x_2.setText(QCoreApplication.translate("Dialog", u"Pressure (x-axis):", None))
        self.label_component_x_4.setText(QCoreApplication.translate("Dialog", u"Pressure (z-axis):", None))
        self.label_component_x_3.setText(QCoreApplication.translate("Dialog", u"Pressure (y-axis):", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_load_tables), QCoreApplication.translate("Dialog", u"Load table", None))
        self.pushButton_reset.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.pushButton_remove.setText(QCoreApplication.translate("Dialog", u"Remove", None))
        ___qtreewidgetitem = self.treeWidget_incident_plane_wave.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"Values", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Surface ID", None));
#if QT_CONFIG(tooltip)
        self.treeWidget_incident_plane_wave.setToolTip(QCoreApplication.translate("Dialog", u"Select a face to remove the previously attributed boundary condition.", None))
#endif // QT_CONFIG(tooltip)
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_list), QCoreApplication.translate("Dialog", u"List", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Selection ID:", None))
        self.label_19.setText(QCoreApplication.translate("Dialog", u"Wave direction:", None))
        self.comboBox_wave_direction.setItemText(0, QCoreApplication.translate("Dialog", u"Normal", None))
        self.comboBox_wave_direction.setItemText(1, QCoreApplication.translate("Dialog", u"Components", None))

        self.label.setText(QCoreApplication.translate("Dialog", u"Incident plane wave setup", None))
        self.pushButton_attribute.setText(QCoreApplication.translate("Dialog", u"Attribute", None))
        self.pushButton_exit.setText(QCoreApplication.translate("Dialog", u"Exit", None))
    # retranslateUi



class IncidentPlaneWaveInputs_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame_2: QFrame
                    - (Layout): QGridLayout
                            - tabWidget_main: QTabWidget
                                - tab_constant_values: QWidget
                                    - (Layout): QGridLayout
                                            - frame_8: QFrame
                                                - (Layout): QGridLayout
                                                        - label_21: QLabel
                                                        - label_4: QLabel
                                                        - lineEdit_real_value_x: QLineEdit
                                                        - label_component_x: QLabel
                                                        - lineEdit_imag_value_x: QLineEdit
                                                        - label_5: QLabel
                                                        - lineEdit_real_value_y: QLineEdit
                                                        - lineEdit_imag_value_y: QLineEdit
                                                        - label_22: QLabel
                                                        - label_24: QLabel
                                                        - label_component_y: QLabel
                                                        - lineEdit_real_value_z: QLineEdit
                                                        - label_component_z: QLabel
                                                        - lineEdit_imag_value_z: QLineEdit
                                - tab_load_tables: QWidget
                                    - (Layout): QGridLayout
                                            - frame_9: QFrame
                                                - (Layout): QGridLayout
                                                        - pushButton_load_table_x: QPushButton
                                                        - lineEdit_table_path_x: QLineEdit
                                                        - pushButton_load_table_y: QPushButton
                                                        - lineEdit_table_path_z: QLineEdit
                                                        - lineEdit_table_path_y: QLineEdit
                                                        - pushButton_load_table_z: QPushButton
                                                        - label_component_x_2: QLabel
                                                        - label_component_x_4: QLabel
                                                        - label_component_x_3: QLabel
                                - tab_list: QWidget
                                    - (Layout): QGridLayout
                                            - frame_3: QFrame
                                                - (Layout): QGridLayout
                                                        - pushButton_reset: QPushButton
                                                        - pushButton_remove: QPushButton
                                            - treeWidget_incident_plane_wave: QTreeWidget
                            - frame_4: QFrame
                                - (Layout): QGridLayout
                                        - label_2: QLabel
                                        - lineEdit_selection_id: QLineEdit
                                        - label_19: QLabel
                                        - comboBox_wave_direction: QComboBox
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
