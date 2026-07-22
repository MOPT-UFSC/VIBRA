# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'incident_plane_wave_inputs.ui'
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setWindowModality(Qt.WindowModality.WindowModal)
        Dialog.resize(446, 500)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(420, 360))
        Dialog.setMaximumSize(QSize(460, 500))
        font = QFont()
        font.setPointSize(11)
        font.setBold(False)
        Dialog.setFont(font)
        Dialog.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        self.gridLayout_7 = QGridLayout(Dialog)
        self.gridLayout_7.setSpacing(4)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(4, 4, 4, 4)
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(380, 48))
        self.frame.setMaximumSize(QSize(16777215, 48))
        self.frame.setFrameShape(QFrame.Shape.Box)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.frame.setLineWidth(1)
        self.gridLayout_6 = QGridLayout(self.frame)
        self.gridLayout_6.setSpacing(4)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(4, 4, 4, 4)
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        font1 = QFont()
        font1.setFamilies([u"MS Shell Dlg 2"])
        font1.setPointSize(11)
        font1.setBold(False)
        font1.setItalic(False)
        self.label.setFont(font1)
        self.label.setTextFormat(Qt.TextFormat.AutoText)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_6.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout_7.addWidget(self.frame, 0, 0, 1, 1)

        self.frame_2 = QFrame(Dialog)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(380, 0))
        self.frame_2.setMaximumSize(QSize(16777215, 480))
        self.frame_2.setFrameShape(QFrame.Shape.Box)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setVerticalSpacing(4)
        self.gridLayout_4.setContentsMargins(4, 4, 4, 4)
        self.tabWidget_main = QTabWidget(self.frame_2)
        self.tabWidget_main.setObjectName(u"tabWidget_main")
        self.tabWidget_main.setMinimumSize(QSize(360, 200))
        self.tabWidget_main.setMaximumSize(QSize(16777215, 200))
        font2 = QFont()
        font2.setPointSize(10)
        font2.setBold(False)
        self.tabWidget_main.setFont(font2)
        self.tab_constant_data = QWidget()
        self.tab_constant_data.setObjectName(u"tab_constant_data")
        self.gridLayout_12 = QGridLayout(self.tab_constant_data)
        self.gridLayout_12.setSpacing(2)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setContentsMargins(2, 6, 2, 6)
        self.frame_8 = QFrame(self.tab_constant_data)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setMinimumSize(QSize(340, 80))
        self.frame_8.setMaximumSize(QSize(16777215, 240))
        self.frame_8.setFont(font)
        self.frame_8.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_8.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.frame_8)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.label_pinc0_unit = QLabel(self.frame_8)
        self.label_pinc0_unit.setObjectName(u"label_pinc0_unit")
        self.label_pinc0_unit.setMinimumSize(QSize(40, 26))
        self.label_pinc0_unit.setMaximumSize(QSize(40, 26))
        font3 = QFont()
        font3.setFamilies([u"MS Shell Dlg 2"])
        font3.setPointSize(10)
        font3.setBold(False)
        font3.setItalic(False)
        self.label_pinc0_unit.setFont(font3)
        self.label_pinc0_unit.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_pinc0_unit, 3, 3, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 0, 2, 1, 1)

        self.lineEdit_incident_pressure_real = QLineEdit(self.frame_8)
        self.lineEdit_incident_pressure_real.setObjectName(u"lineEdit_incident_pressure_real")
        self.lineEdit_incident_pressure_real.setMinimumSize(QSize(100, 28))
        self.lineEdit_incident_pressure_real.setMaximumSize(QSize(100, 28))
        self.lineEdit_incident_pressure_real.setFont(font3)
        self.lineEdit_incident_pressure_real.setStyleSheet(u"")
        self.lineEdit_incident_pressure_real.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_incident_pressure_real, 3, 2, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_3, 3, 0, 1, 1)

        self.label_pinc1_constant = QLabel(self.frame_8)
        self.label_pinc1_constant.setObjectName(u"label_pinc1_constant")
        self.label_pinc1_constant.setMinimumSize(QSize(170, 28))
        self.label_pinc1_constant.setMaximumSize(QSize(180, 28))
        self.label_pinc1_constant.setFont(font3)
        self.label_pinc1_constant.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_pinc1_constant, 4, 1, 1, 1)

        self.label_pinc1_unit = QLabel(self.frame_8)
        self.label_pinc1_unit.setObjectName(u"label_pinc1_unit")
        self.label_pinc1_unit.setMinimumSize(QSize(40, 26))
        self.label_pinc1_unit.setMaximumSize(QSize(40, 26))
        self.label_pinc1_unit.setFont(font3)
        self.label_pinc1_unit.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_pinc1_unit, 4, 3, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_4, 3, 4, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_2, 5, 2, 1, 1)

        self.label_pinc0_constant = QLabel(self.frame_8)
        self.label_pinc0_constant.setObjectName(u"label_pinc0_constant")
        self.label_pinc0_constant.setMinimumSize(QSize(170, 28))
        self.label_pinc0_constant.setMaximumSize(QSize(180, 28))
        self.label_pinc0_constant.setFont(font3)
        self.label_pinc0_constant.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_pinc0_constant, 3, 1, 1, 1)

        self.lineEdit_incident_pressure_imag = QLineEdit(self.frame_8)
        self.lineEdit_incident_pressure_imag.setObjectName(u"lineEdit_incident_pressure_imag")
        self.lineEdit_incident_pressure_imag.setMinimumSize(QSize(100, 28))
        self.lineEdit_incident_pressure_imag.setMaximumSize(QSize(100, 28))
        self.lineEdit_incident_pressure_imag.setFont(font3)
        self.lineEdit_incident_pressure_imag.setStyleSheet(u"")
        self.lineEdit_incident_pressure_imag.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_incident_pressure_imag, 4, 2, 1, 1)

        self.frame_5 = QFrame(self.frame_8)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setMinimumSize(QSize(0, 36))
        self.frame_5.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_13 = QGridLayout(self.frame_5)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_13.setContentsMargins(-1, 2, -1, 2)
        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_13.addItem(self.horizontalSpacer_7, 0, 3, 1, 1)

        self.comboBox_input_mode = QComboBox(self.frame_5)
        self.comboBox_input_mode.addItem("")
        self.comboBox_input_mode.addItem("")
        self.comboBox_input_mode.setObjectName(u"comboBox_input_mode")
        self.comboBox_input_mode.setFont(font2)

        self.gridLayout_13.addWidget(self.comboBox_input_mode, 0, 2, 1, 1)

        self.label_incident_pressure_input_mode = QLabel(self.frame_5)
        self.label_incident_pressure_input_mode.setObjectName(u"label_incident_pressure_input_mode")
        self.label_incident_pressure_input_mode.setMinimumSize(QSize(110, 28))
        self.label_incident_pressure_input_mode.setMaximumSize(QSize(140, 28))
        self.label_incident_pressure_input_mode.setFont(font3)
        self.label_incident_pressure_input_mode.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_13.addWidget(self.label_incident_pressure_input_mode, 0, 1, 1, 1)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_13.addItem(self.horizontalSpacer_10, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_5, 1, 0, 1, 5)


        self.gridLayout_12.addWidget(self.frame_8, 1, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_constant_data, "")
        self.tab_tabular_data = QWidget()
        self.tab_tabular_data.setObjectName(u"tab_tabular_data")
        self.gridLayout_3 = QGridLayout(self.tab_tabular_data)
        self.gridLayout_3.setSpacing(2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(2, 6, 2, 6)
        self.frame_9 = QFrame(self.tab_tabular_data)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setMinimumSize(QSize(260, 0))
        self.frame_9.setMaximumSize(QSize(600, 200))
        self.frame_9.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_9.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_9)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 4, 0, 0)
        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_8, 2, 0, 1, 1)

        self.lineEdit_table_path = QLineEdit(self.frame_9)
        self.lineEdit_table_path.setObjectName(u"lineEdit_table_path")
        self.lineEdit_table_path.setEnabled(True)
        self.lineEdit_table_path.setMinimumSize(QSize(280, 28))
        self.lineEdit_table_path.setMaximumSize(QSize(280, 28))
        font4 = QFont()
        font4.setPointSize(8)
        font4.setBold(False)
        self.lineEdit_table_path.setFont(font4)
        self.lineEdit_table_path.setStyleSheet(u"")
        self.lineEdit_table_path.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_table_path, 2, 1, 1, 1)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_9, 2, 4, 1, 1)

        self.pushButton_load_table = QPushButton(self.frame_9)
        self.pushButton_load_table.setObjectName(u"pushButton_load_table")
        self.pushButton_load_table.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton_load_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_table.setSizePolicy(sizePolicy1)
        self.pushButton_load_table.setMinimumSize(QSize(40, 28))
        self.pushButton_load_table.setMaximumSize(QSize(40, 28))
        self.pushButton_load_table.setFont(font3)
        self.pushButton_load_table.setStyleSheet(u"")
        icon = QIcon()
        icon.addFile(u":/icons/document_search_blue.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_load_table.setIcon(icon)
        self.pushButton_load_table.setIconSize(QSize(20, 20))
        self.pushButton_load_table.setAutoDefault(False)

        self.gridLayout_2.addWidget(self.pushButton_load_table, 2, 2, 1, 1)

        self.label_3 = QLabel(self.frame_9)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(0, 28))
        self.label_3.setMaximumSize(QSize(16777215, 28))
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.label_3, 1, 1, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer_3, 3, 1, 1, 1)


        self.gridLayout_3.addWidget(self.frame_9, 1, 0, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer_4, 0, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_tabular_data, "")
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
        self.frame_3.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
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
        self.pushButton_reset.setAutoDefault(False)

        self.gridLayout_8.addWidget(self.pushButton_reset, 0, 0, 1, 1)

        self.pushButton_remove = QPushButton(self.frame_3)
        self.pushButton_remove.setObjectName(u"pushButton_remove")
        self.pushButton_remove.setMinimumSize(QSize(100, 28))
        self.pushButton_remove.setMaximumSize(QSize(100, 28))
        self.pushButton_remove.setFont(font3)
        self.pushButton_remove.setStyleSheet(u"")
        self.pushButton_remove.setAutoDefault(False)

        self.gridLayout_8.addWidget(self.pushButton_remove, 0, 1, 1, 1)


        self.gridLayout_9.addWidget(self.frame_3, 1, 0, 1, 1)

        self.treeWidget_incident_plane_wave = QTreeWidget(self.tab_list)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(2, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter);
        self.treeWidget_incident_plane_wave.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_incident_plane_wave.setObjectName(u"treeWidget_incident_plane_wave")
        self.treeWidget_incident_plane_wave.setMinimumSize(QSize(320, 100))
        self.treeWidget_incident_plane_wave.setMaximumSize(QSize(400, 200))
        font5 = QFont()
        font5.setFamilies([u"MS Shell Dlg 2"])
        font5.setPointSize(9)
        font5.setBold(False)
        font5.setItalic(False)
        self.treeWidget_incident_plane_wave.setFont(font5)
        self.treeWidget_incident_plane_wave.setIndentation(1)
        self.treeWidget_incident_plane_wave.setHeaderHidden(False)
        self.treeWidget_incident_plane_wave.header().setHighlightSections(False)
        self.treeWidget_incident_plane_wave.header().setProperty(u"showSortIndicator", False)
        self.treeWidget_incident_plane_wave.header().setStretchLastSection(True)

        self.gridLayout_9.addWidget(self.treeWidget_incident_plane_wave, 0, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_list, "")

        self.gridLayout_4.addWidget(self.tabWidget_main, 3, 0, 1, 1)

        self.frame_incident_wave_vector = QFrame(self.frame_2)
        self.frame_incident_wave_vector.setObjectName(u"frame_incident_wave_vector")
        self.frame_incident_wave_vector.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_incident_wave_vector.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_10 = QGridLayout(self.frame_incident_wave_vector)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setVerticalSpacing(2)
        self.gridLayout_10.setContentsMargins(4, 4, 4, 4)
        self.lineEdit_component_z = QLineEdit(self.frame_incident_wave_vector)
        self.lineEdit_component_z.setObjectName(u"lineEdit_component_z")
        self.lineEdit_component_z.setMinimumSize(QSize(80, 28))
        self.lineEdit_component_z.setMaximumSize(QSize(80, 28))
        self.lineEdit_component_z.setFont(font3)
        self.lineEdit_component_z.setStyleSheet(u"")
        self.lineEdit_component_z.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_10.addWidget(self.lineEdit_component_z, 1, 4, 1, 1)

        self.lineEdit_component_y = QLineEdit(self.frame_incident_wave_vector)
        self.lineEdit_component_y.setObjectName(u"lineEdit_component_y")
        self.lineEdit_component_y.setMinimumSize(QSize(80, 28))
        self.lineEdit_component_y.setMaximumSize(QSize(80, 28))
        self.lineEdit_component_y.setFont(font3)
        self.lineEdit_component_y.setStyleSheet(u"")
        self.lineEdit_component_y.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_10.addWidget(self.lineEdit_component_y, 1, 3, 1, 1)

        self.label_component_x = QLabel(self.frame_incident_wave_vector)
        self.label_component_x.setObjectName(u"label_component_x")
        self.label_component_x.setMinimumSize(QSize(80, 22))
        self.label_component_x.setMaximumSize(QSize(80, 22))
        self.label_component_x.setFont(font3)
        self.label_component_x.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_10.addWidget(self.label_component_x, 0, 2, 1, 1)

        self.lineEdit_component_x = QLineEdit(self.frame_incident_wave_vector)
        self.lineEdit_component_x.setObjectName(u"lineEdit_component_x")
        self.lineEdit_component_x.setMinimumSize(QSize(80, 28))
        self.lineEdit_component_x.setMaximumSize(QSize(80, 28))
        self.lineEdit_component_x.setFont(font3)
        self.lineEdit_component_x.setStyleSheet(u"")
        self.lineEdit_component_x.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_10.addWidget(self.lineEdit_component_x, 1, 2, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_10.addItem(self.horizontalSpacer_6, 1, 0, 1, 1)

        self.label_component_z = QLabel(self.frame_incident_wave_vector)
        self.label_component_z.setObjectName(u"label_component_z")
        self.label_component_z.setMinimumSize(QSize(80, 22))
        self.label_component_z.setMaximumSize(QSize(80, 22))
        self.label_component_z.setFont(font3)
        self.label_component_z.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_10.addWidget(self.label_component_z, 0, 4, 1, 1)

        self.label_component_y = QLabel(self.frame_incident_wave_vector)
        self.label_component_y.setObjectName(u"label_component_y")
        self.label_component_y.setMinimumSize(QSize(80, 22))
        self.label_component_y.setMaximumSize(QSize(80, 22))
        self.label_component_y.setFont(font3)
        self.label_component_y.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_10.addWidget(self.label_component_y, 0, 3, 1, 1)

        self.label_wave_vector = QLabel(self.frame_incident_wave_vector)
        self.label_wave_vector.setObjectName(u"label_wave_vector")
        self.label_wave_vector.setMinimumSize(QSize(100, 28))
        self.label_wave_vector.setMaximumSize(QSize(140, 28))
        self.label_wave_vector.setFont(font3)
        self.label_wave_vector.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_wave_vector, 1, 1, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_10.addItem(self.horizontalSpacer_5, 1, 5, 1, 1)

        self.label_wave_vector_2 = QLabel(self.frame_incident_wave_vector)
        self.label_wave_vector_2.setObjectName(u"label_wave_vector_2")
        self.label_wave_vector_2.setEnabled(False)
        self.label_wave_vector_2.setMinimumSize(QSize(100, 28))
        self.label_wave_vector_2.setMaximumSize(QSize(140, 28))
        self.label_wave_vector_2.setFont(font3)
        self.label_wave_vector_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_wave_vector_2, 2, 1, 1, 1)

        self.lineEdit_normal_x = QLineEdit(self.frame_incident_wave_vector)
        self.lineEdit_normal_x.setObjectName(u"lineEdit_normal_x")
        self.lineEdit_normal_x.setEnabled(False)
        self.lineEdit_normal_x.setMinimumSize(QSize(80, 28))
        self.lineEdit_normal_x.setMaximumSize(QSize(80, 28))
        self.lineEdit_normal_x.setFont(font3)
        self.lineEdit_normal_x.setStyleSheet(u"")
        self.lineEdit_normal_x.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_10.addWidget(self.lineEdit_normal_x, 2, 2, 1, 1)

        self.lineEdit_normal_y = QLineEdit(self.frame_incident_wave_vector)
        self.lineEdit_normal_y.setObjectName(u"lineEdit_normal_y")
        self.lineEdit_normal_y.setEnabled(False)
        self.lineEdit_normal_y.setMinimumSize(QSize(80, 28))
        self.lineEdit_normal_y.setMaximumSize(QSize(80, 28))
        self.lineEdit_normal_y.setFont(font3)
        self.lineEdit_normal_y.setStyleSheet(u"")
        self.lineEdit_normal_y.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_10.addWidget(self.lineEdit_normal_y, 2, 3, 1, 1)

        self.lineEdit_normal_z = QLineEdit(self.frame_incident_wave_vector)
        self.lineEdit_normal_z.setObjectName(u"lineEdit_normal_z")
        self.lineEdit_normal_z.setEnabled(False)
        self.lineEdit_normal_z.setMinimumSize(QSize(80, 28))
        self.lineEdit_normal_z.setMaximumSize(QSize(80, 28))
        self.lineEdit_normal_z.setFont(font3)
        self.lineEdit_normal_z.setStyleSheet(u"")
        self.lineEdit_normal_z.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_10.addWidget(self.lineEdit_normal_z, 2, 4, 1, 1)


        self.gridLayout_4.addWidget(self.frame_incident_wave_vector, 2, 0, 1, 1)

        self.frame_4 = QFrame(self.frame_2)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(360, 68))
        self.frame_4.setMaximumSize(QSize(16777215, 68))
        self.frame_4.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_4)
        self.gridLayout_5.setSpacing(6)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(4, 4, 4, 4)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer, 0, 3, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_2, 0, 0, 1, 1)

        self.label_2 = QLabel(self.frame_4)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(80, 28))
        self.label_2.setMaximumSize(QSize(120, 28))
        self.label_2.setFont(font2)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_2, 0, 1, 1, 1)

        self.lineEdit_selection_id = QLineEdit(self.frame_4)
        self.lineEdit_selection_id.setObjectName(u"lineEdit_selection_id")
        self.lineEdit_selection_id.setMinimumSize(QSize(120, 28))
        self.lineEdit_selection_id.setMaximumSize(QSize(120, 28))
        self.lineEdit_selection_id.setFont(font3)
        self.lineEdit_selection_id.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.lineEdit_selection_id.setStyleSheet(u"")
        self.lineEdit_selection_id.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.lineEdit_selection_id, 0, 2, 1, 1)

        self.label_19 = QLabel(self.frame_4)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setMinimumSize(QSize(80, 28))
        self.label_19.setMaximumSize(QSize(120, 28))
        self.label_19.setFont(font3)
        self.label_19.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_19, 1, 1, 1, 1)

        self.comboBox_wave_direction = QComboBox(self.frame_4)
        self.comboBox_wave_direction.addItem("")
        self.comboBox_wave_direction.addItem("")
        self.comboBox_wave_direction.setObjectName(u"comboBox_wave_direction")
        self.comboBox_wave_direction.setMinimumSize(QSize(120, 28))
        self.comboBox_wave_direction.setMaximumSize(QSize(16777215, 28))
        self.comboBox_wave_direction.setFont(font2)

        self.gridLayout_5.addWidget(self.comboBox_wave_direction, 1, 2, 1, 1)


        self.gridLayout_4.addWidget(self.frame_4, 0, 0, 1, 1)


        self.gridLayout_7.addWidget(self.frame_2, 1, 0, 1, 1)

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
        font6 = QFont()
        font6.setPointSize(10)
        font6.setBold(False)
        font6.setItalic(False)
        self.pushButton_apply_and_close.setFont(font6)
        self.pushButton_apply_and_close.setStyleSheet(u"")
        self.pushButton_apply_and_close.setAutoDefault(False)
        self.pushButton_apply_and_close.setFlat(False)

        self.gridLayout_11.addWidget(self.pushButton_apply_and_close, 0, 3, 1, 1)

        self.pushButton_apply = QPushButton(self.frame_buttons)
        self.pushButton_apply.setObjectName(u"pushButton_apply")
        self.pushButton_apply.setMinimumSize(QSize(72, 30))
        self.pushButton_apply.setMaximumSize(QSize(72, 30))
        self.pushButton_apply.setFont(font6)
        self.pushButton_apply.setStyleSheet(u"")
        self.pushButton_apply.setAutoDefault(False)
        self.pushButton_apply.setFlat(False)

        self.gridLayout_11.addWidget(self.pushButton_apply, 0, 2, 1, 1)

        self.pushButton_cancel = QPushButton(self.frame_buttons)
        self.pushButton_cancel.setObjectName(u"pushButton_cancel")
        self.pushButton_cancel.setMinimumSize(QSize(72, 30))
        self.pushButton_cancel.setMaximumSize(QSize(72, 30))
        self.pushButton_cancel.setFont(font6)
        self.pushButton_cancel.setStyleSheet(u"")
        self.pushButton_cancel.setAutoDefault(False)
        self.pushButton_cancel.setFlat(False)

        self.gridLayout_11.addWidget(self.pushButton_cancel, 0, 0, 1, 1)

        self.horizontalSpacer_17 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_11.addItem(self.horizontalSpacer_17, 0, 1, 1, 1)


        self.gridLayout_7.addWidget(self.frame_buttons, 2, 0, 1, 1)

        QWidget.setTabOrder(self.comboBox_wave_direction, self.tabWidget_main)
        QWidget.setTabOrder(self.tabWidget_main, self.lineEdit_incident_pressure_real)
        QWidget.setTabOrder(self.lineEdit_incident_pressure_real, self.lineEdit_component_x)
        QWidget.setTabOrder(self.lineEdit_component_x, self.lineEdit_component_y)
        QWidget.setTabOrder(self.lineEdit_component_y, self.lineEdit_component_z)
        QWidget.setTabOrder(self.lineEdit_component_z, self.pushButton_remove)
        QWidget.setTabOrder(self.pushButton_remove, self.pushButton_reset)
        QWidget.setTabOrder(self.pushButton_reset, self.treeWidget_incident_plane_wave)
        QWidget.setTabOrder(self.treeWidget_incident_plane_wave, self.lineEdit_table_path)
        QWidget.setTabOrder(self.lineEdit_table_path, self.pushButton_load_table)

        self.retranslateUi(Dialog)

        self.tabWidget_main.setCurrentIndex(0)
        self.pushButton_apply_and_close.setDefault(False)
        self.pushButton_apply.setDefault(False)
        self.pushButton_cancel.setDefault(False)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Set incident plane wave", None))
#if QT_CONFIG(whatsthis)
        Dialog.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.label.setText(QCoreApplication.translate("Dialog", u"Incident plane wave setup", None))
        self.label_pinc0_unit.setText(QCoreApplication.translate("Dialog", u"[Pa]", None))
        self.label_pinc1_constant.setText(QCoreApplication.translate("Dialog", u"Incident pressure (imag.):", None))
        self.label_pinc1_unit.setText(QCoreApplication.translate("Dialog", u"[Pa]", None))
        self.label_pinc0_constant.setText(QCoreApplication.translate("Dialog", u"Incident pressure (real):", None))
        self.comboBox_input_mode.setItemText(0, QCoreApplication.translate("Dialog", u"Real and imaginary", None))
        self.comboBox_input_mode.setItemText(1, QCoreApplication.translate("Dialog", u"Amplitude and phase", None))

        self.label_incident_pressure_input_mode.setText(QCoreApplication.translate("Dialog", u"Input mode:", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_constant_data), QCoreApplication.translate("Dialog", u"Constant data", None))
        self.pushButton_load_table.setText("")
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Choose a table file to import the data", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_tabular_data), QCoreApplication.translate("Dialog", u"Tabular data", None))
        self.pushButton_reset.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.pushButton_remove.setText(QCoreApplication.translate("Dialog", u"Remove", None))
        ___qtreewidgetitem = self.treeWidget_incident_plane_wave.headerItem()
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("Dialog", u"Values", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"Wave vector", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Surface ID", None));
#if QT_CONFIG(tooltip)
        self.treeWidget_incident_plane_wave.setToolTip(QCoreApplication.translate("Dialog", u"Select a face to remove the previously attributed boundary condition.", None))
#endif // QT_CONFIG(tooltip)
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_list), QCoreApplication.translate("Dialog", u"List", None))
        self.label_component_x.setText(QCoreApplication.translate("Dialog", u"Comp. x", None))
        self.label_component_z.setText(QCoreApplication.translate("Dialog", u"Comp. z", None))
        self.label_component_y.setText(QCoreApplication.translate("Dialog", u"Comp. y", None))
        self.label_wave_vector.setText(QCoreApplication.translate("Dialog", u"Wave vector:", None))
        self.label_wave_vector_2.setText(QCoreApplication.translate("Dialog", u"Normal vector:", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Selection ID:", None))
        self.label_19.setText(QCoreApplication.translate("Dialog", u"Wave direction:", None))
        self.comboBox_wave_direction.setItemText(0, QCoreApplication.translate("Dialog", u"Normal", None))
        self.comboBox_wave_direction.setItemText(1, QCoreApplication.translate("Dialog", u"Components", None))

        self.pushButton_apply_and_close.setText(QCoreApplication.translate("Dialog", u"Ok", None))
        self.pushButton_apply.setText(QCoreApplication.translate("Dialog", u"Apply", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
    # retranslateUi



class IncidentPlaneWaveInputs_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
                - frame_2: QFrame
                    - (Layout): QGridLayout
                            - tabWidget_main: QTabWidget
                                - tab_constant_data: QWidget
                                    - (Layout): QGridLayout
                                            - frame_8: QFrame
                                                - (Layout): QGridLayout
                                                        - label_pinc0_unit: QLabel
                                                        - lineEdit_incident_pressure_real: QLineEdit
                                                        - label_pinc1_constant: QLabel
                                                        - label_pinc1_unit: QLabel
                                                        - label_pinc0_constant: QLabel
                                                        - lineEdit_incident_pressure_imag: QLineEdit
                                                        - frame_5: QFrame
                                                            - (Layout): QGridLayout
                                                                    - comboBox_input_mode: QComboBox
                                                                    - label_incident_pressure_input_mode: QLabel
                                - tab_tabular_data: QWidget
                                    - (Layout): QGridLayout
                                            - frame_9: QFrame
                                                - (Layout): QGridLayout
                                                        - lineEdit_table_path: QLineEdit
                                                        - pushButton_load_table: QPushButton
                                                        - label_3: QLabel
                                - tab_list: QWidget
                                    - (Layout): QGridLayout
                                            - frame_3: QFrame
                                                - (Layout): QGridLayout
                                                        - pushButton_reset: QPushButton
                                                        - pushButton_remove: QPushButton
                                            - treeWidget_incident_plane_wave: QTreeWidget
                            - frame_incident_wave_vector: QFrame
                                - (Layout): QGridLayout
                                        - lineEdit_component_z: QLineEdit
                                        - lineEdit_component_y: QLineEdit
                                        - label_component_x: QLabel
                                        - lineEdit_component_x: QLineEdit
                                        - label_component_z: QLabel
                                        - label_component_y: QLabel
                                        - label_wave_vector: QLabel
                                        - label_wave_vector_2: QLabel
                                        - lineEdit_normal_x: QLineEdit
                                        - lineEdit_normal_y: QLineEdit
                                        - lineEdit_normal_z: QLineEdit
                            - frame_4: QFrame
                                - (Layout): QGridLayout
                                        - label_2: QLabel
                                        - lineEdit_selection_id: QLineEdit
                                        - label_19: QLabel
                                        - comboBox_wave_direction: QComboBox
                - frame_buttons: QFrame
                    - (Layout): QGridLayout
                            - pushButton_apply_and_close: QPushButton
                            - pushButton_apply: QPushButton
                            - pushButton_cancel: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
