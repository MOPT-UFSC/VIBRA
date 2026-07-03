# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mass_source_inputs.ui'
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
        Dialog.resize(420, 440)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(420, 440))
        Dialog.setMaximumSize(QSize(420, 440))
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
        self.frame.setMaximumSize(QSize(420, 48))
        self.frame.setFrameShape(QFrame.Shape.Box)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
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
        self.label.setTextFormat(Qt.TextFormat.AutoText)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_6.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout_7.addWidget(self.frame, 0, 0, 1, 1)

        self.frame_2 = QFrame(Dialog)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(380, 280))
        self.frame_2.setMaximumSize(QSize(420, 480))
        self.frame_2.setFrameShape(QFrame.Shape.Box)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.tabWidget_main = QTabWidget(self.frame_2)
        self.tabWidget_main.setObjectName(u"tabWidget_main")
        self.tabWidget_main.setMinimumSize(QSize(360, 0))
        self.tabWidget_main.setMaximumSize(QSize(380, 16777215))
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
        self.frame_8.setMaximumSize(QSize(400, 160))
        self.frame_8.setFont(font2)
        self.frame_8.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_8.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.frame_8)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(0)
        self.gridLayout.setVerticalSpacing(2)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_imag_value = QLineEdit(self.frame_8)
        self.lineEdit_imag_value.setObjectName(u"lineEdit_imag_value")
        self.lineEdit_imag_value.setMinimumSize(QSize(80, 28))
        self.lineEdit_imag_value.setMaximumSize(QSize(80, 28))
        font3 = QFont()
        font3.setFamilies([u"MS Shell Dlg 2"])
        font3.setPointSize(10)
        font3.setBold(False)
        font3.setItalic(False)
        self.lineEdit_imag_value.setFont(font3)
        self.lineEdit_imag_value.setStyleSheet(u"")
        self.lineEdit_imag_value.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_imag_value, 1, 2, 1, 1)

        self.label_mass_source_unit = QLabel(self.frame_8)
        self.label_mass_source_unit.setObjectName(u"label_mass_source_unit")
        self.label_mass_source_unit.setMinimumSize(QSize(60, 28))
        self.label_mass_source_unit.setMaximumSize(QSize(60, 28))
        self.label_mass_source_unit.setFont(font3)
        self.label_mass_source_unit.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_mass_source_unit, 1, 3, 1, 1)

        self.label_18 = QLabel(self.frame_8)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setMinimumSize(QSize(120, 28))
        self.label_18.setMaximumSize(QSize(120, 28))
        self.label_18.setFont(font3)
        self.label_18.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_18, 1, 0, 1, 1)

        self.label_4 = QLabel(self.frame_8)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(80, 26))
        self.label_4.setMaximumSize(QSize(80, 26))
        self.label_4.setFont(font3)
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_4, 0, 1, 1, 1)

        self.label_20 = QLabel(self.frame_8)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setMinimumSize(QSize(80, 26))
        self.label_20.setMaximumSize(QSize(80, 26))
        self.label_20.setFont(font3)
        self.label_20.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_20, 0, 2, 1, 1)

        self.lineEdit_real_value = QLineEdit(self.frame_8)
        self.lineEdit_real_value.setObjectName(u"lineEdit_real_value")
        self.lineEdit_real_value.setMinimumSize(QSize(80, 28))
        self.lineEdit_real_value.setMaximumSize(QSize(80, 28))
        self.lineEdit_real_value.setFont(font3)
        self.lineEdit_real_value.setStyleSheet(u"")
        self.lineEdit_real_value.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_real_value, 1, 1, 1, 1)


        self.gridLayout_12.addWidget(self.frame_8, 1, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_12.addItem(self.verticalSpacer, 0, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_12.addItem(self.verticalSpacer_2, 2, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_constant_data, "")
        self.tab_tabular_data = QWidget()
        self.tab_tabular_data.setObjectName(u"tab_tabular_data")
        self.gridLayout_3 = QGridLayout(self.tab_tabular_data)
        self.gridLayout_3.setSpacing(2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(2, 6, 2, 6)
        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer_4, 3, 0, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer_3, 0, 0, 1, 1)

        self.frame_9 = QFrame(self.tab_tabular_data)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setMinimumSize(QSize(260, 0))
        self.frame_9.setMaximumSize(QSize(400, 100))
        self.frame_9.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_9.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_9)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setHorizontalSpacing(6)
        self.gridLayout_2.setVerticalSpacing(2)
        self.gridLayout_2.setContentsMargins(0, 4, 0, 0)
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
        self.pushButton_load_table.setFont(font3)
        self.pushButton_load_table.setStyleSheet(u"")
        icon = Icon(u":/icons/document_search_blue.png")
        self.pushButton_load_table.setIcon(icon)
        self.pushButton_load_table.setIconSize(QSize(20, 20))
        self.pushButton_load_table.setAutoDefault(False)

        self.gridLayout_2.addWidget(self.pushButton_load_table, 1, 2, 1, 1)

        self.label_11 = QLabel(self.frame_9)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMinimumSize(QSize(0, 28))
        self.label_11.setMaximumSize(QSize(16777215, 28))
        self.label_11.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.label_11, 0, 1, 1, 1)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_12, 1, 4, 1, 1)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_11, 1, 0, 1, 1)

        self.lineEdit_table_path = QLineEdit(self.frame_9)
        self.lineEdit_table_path.setObjectName(u"lineEdit_table_path")
        self.lineEdit_table_path.setEnabled(True)
        self.lineEdit_table_path.setMinimumSize(QSize(280, 26))
        self.lineEdit_table_path.setMaximumSize(QSize(280, 26))
        font4 = QFont()
        font4.setPointSize(9)
        font4.setBold(False)
        self.lineEdit_table_path.setFont(font4)
        self.lineEdit_table_path.setStyleSheet(u"")
        self.lineEdit_table_path.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_table_path, 1, 1, 1, 1)


        self.gridLayout_3.addWidget(self.frame_9, 1, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_tabular_data, "")
        self.tab_advanced_search = QWidget()
        self.tab_advanced_search.setObjectName(u"tab_advanced_search")
        self.gridLayout_11 = QGridLayout(self.tab_advanced_search)
        self.gridLayout_11.setSpacing(4)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setContentsMargins(4, 4, 4, 4)
        self.frame_7 = QFrame(self.tab_advanced_search)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_7.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_15 = QGridLayout(self.frame_7)
        self.gridLayout_15.setSpacing(6)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.gridLayout_15.setContentsMargins(6, 6, 6, 6)
        self.label_8 = QLabel(self.frame_7)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMinimumSize(QSize(90, 28))
        self.label_8.setMaximumSize(QSize(90, 28))
        self.label_8.setFont(font3)
        self.label_8.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_15.addWidget(self.label_8, 0, 0, 1, 1)

        self.lineEdit_nearest_node_id = QLineEdit(self.frame_7)
        self.lineEdit_nearest_node_id.setObjectName(u"lineEdit_nearest_node_id")
        self.lineEdit_nearest_node_id.setMinimumSize(QSize(0, 28))
        self.lineEdit_nearest_node_id.setMaximumSize(QSize(300, 28))
        self.lineEdit_nearest_node_id.setFont(font3)
        self.lineEdit_nearest_node_id.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.lineEdit_nearest_node_id.setStyleSheet(u"")
        self.lineEdit_nearest_node_id.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_15.addWidget(self.lineEdit_nearest_node_id, 0, 1, 1, 1)

        self.pushButton_get_nearest_node = QPushButton(self.frame_7)
        self.pushButton_get_nearest_node.setObjectName(u"pushButton_get_nearest_node")
        self.pushButton_get_nearest_node.setMinimumSize(QSize(80, 28))
        self.pushButton_get_nearest_node.setMaximumSize(QSize(80, 28))
        self.pushButton_get_nearest_node.setFont(font3)
        self.pushButton_get_nearest_node.setStyleSheet(u"")
        self.pushButton_get_nearest_node.setAutoDefault(False)

        self.gridLayout_15.addWidget(self.pushButton_get_nearest_node, 0, 2, 1, 1)


        self.gridLayout_11.addWidget(self.frame_7, 1, 0, 1, 1)

        self.frame_5 = QFrame(self.tab_advanced_search)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_10 = QGridLayout(self.frame_5)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(6, 6, 6, 6)
        self.label_5 = QLabel(self.frame_5)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(0, 20))
        self.label_5.setMaximumSize(QSize(100, 28))
        self.label_5.setFont(font3)
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_10.addWidget(self.label_5, 0, 1, 1, 1)

        self.label_6 = QLabel(self.frame_5)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(0, 20))
        self.label_6.setMaximumSize(QSize(100, 28))
        self.label_6.setFont(font3)
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_10.addWidget(self.label_6, 0, 2, 1, 1)

        self.label_7 = QLabel(self.frame_5)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(0, 20))
        self.label_7.setMaximumSize(QSize(100, 28))
        self.label_7.setFont(font3)
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_10.addWidget(self.label_7, 0, 3, 1, 1)

        self.lineEdit_point_coord_x = QLineEdit(self.frame_5)
        self.lineEdit_point_coord_x.setObjectName(u"lineEdit_point_coord_x")
        self.lineEdit_point_coord_x.setMinimumSize(QSize(80, 24))
        self.lineEdit_point_coord_x.setMaximumSize(QSize(80, 28))
        self.lineEdit_point_coord_x.setFont(font2)
        self.lineEdit_point_coord_x.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_10.addWidget(self.lineEdit_point_coord_x, 1, 1, 1, 1)

        self.lineEdit_point_coord_y = QLineEdit(self.frame_5)
        self.lineEdit_point_coord_y.setObjectName(u"lineEdit_point_coord_y")
        self.lineEdit_point_coord_y.setMinimumSize(QSize(80, 24))
        self.lineEdit_point_coord_y.setMaximumSize(QSize(80, 28))
        self.lineEdit_point_coord_y.setFont(font2)
        self.lineEdit_point_coord_y.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_10.addWidget(self.lineEdit_point_coord_y, 1, 2, 1, 1)

        self.lineEdit_point_coord_z = QLineEdit(self.frame_5)
        self.lineEdit_point_coord_z.setObjectName(u"lineEdit_point_coord_z")
        self.lineEdit_point_coord_z.setMinimumSize(QSize(80, 24))
        self.lineEdit_point_coord_z.setMaximumSize(QSize(80, 28))
        self.lineEdit_point_coord_z.setFont(font2)
        self.lineEdit_point_coord_z.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_10.addWidget(self.lineEdit_point_coord_z, 1, 3, 1, 1)

        self.label_9 = QLabel(self.frame_5)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMinimumSize(QSize(90, 28))
        self.label_9.setMaximumSize(QSize(90, 28))
        self.label_9.setFont(font3)
        self.label_9.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_9, 2, 0, 1, 1)

        self.lineEdit_node_coord_x = QLineEdit(self.frame_5)
        self.lineEdit_node_coord_x.setObjectName(u"lineEdit_node_coord_x")
        self.lineEdit_node_coord_x.setMinimumSize(QSize(80, 24))
        self.lineEdit_node_coord_x.setMaximumSize(QSize(80, 28))
        self.lineEdit_node_coord_x.setFont(font2)
        self.lineEdit_node_coord_x.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_10.addWidget(self.lineEdit_node_coord_x, 2, 1, 1, 1)

        self.lineEdit_node_coord_y = QLineEdit(self.frame_5)
        self.lineEdit_node_coord_y.setObjectName(u"lineEdit_node_coord_y")
        self.lineEdit_node_coord_y.setMinimumSize(QSize(80, 24))
        self.lineEdit_node_coord_y.setMaximumSize(QSize(80, 28))
        self.lineEdit_node_coord_y.setFont(font2)
        self.lineEdit_node_coord_y.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_10.addWidget(self.lineEdit_node_coord_y, 2, 2, 1, 1)

        self.lineEdit_node_coord_z = QLineEdit(self.frame_5)
        self.lineEdit_node_coord_z.setObjectName(u"lineEdit_node_coord_z")
        self.lineEdit_node_coord_z.setMinimumSize(QSize(80, 24))
        self.lineEdit_node_coord_z.setMaximumSize(QSize(80, 28))
        self.lineEdit_node_coord_z.setFont(font2)
        self.lineEdit_node_coord_z.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_10.addWidget(self.lineEdit_node_coord_z, 2, 3, 1, 1)

        self.label_3 = QLabel(self.frame_5)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(90, 28))
        self.label_3.setMaximumSize(QSize(90, 28))
        self.label_3.setFont(font3)
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_3, 1, 0, 1, 1)


        self.gridLayout_11.addWidget(self.frame_5, 0, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_advanced_search, "")
        self.tab_list = QWidget()
        self.tab_list.setObjectName(u"tab_list")
        self.gridLayout_9 = QGridLayout(self.tab_list)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setHorizontalSpacing(2)
        self.gridLayout_9.setVerticalSpacing(8)
        self.gridLayout_9.setContentsMargins(10, 10, 10, 4)
        self.frame_3 = QFrame(self.tab_list)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(320, 40))
        self.frame_3.setMaximumSize(QSize(16777215, 40))
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

        self.treeWidget_mass_source = QTreeWidget(self.tab_list)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(2, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter);
        self.treeWidget_mass_source.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_mass_source.setObjectName(u"treeWidget_mass_source")
        self.treeWidget_mass_source.setMinimumSize(QSize(320, 0))
        self.treeWidget_mass_source.setMaximumSize(QSize(16777215, 200))
        self.treeWidget_mass_source.setFont(font3)
        self.treeWidget_mass_source.setIndentation(1)
        self.treeWidget_mass_source.setHeaderHidden(False)
        self.treeWidget_mass_source.header().setHighlightSections(False)
        self.treeWidget_mass_source.header().setProperty(u"showSortIndicator", False)
        self.treeWidget_mass_source.header().setStretchLastSection(True)

        self.gridLayout_9.addWidget(self.treeWidget_mass_source, 0, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_list, "")

        self.gridLayout_4.addWidget(self.tabWidget_main, 2, 0, 1, 1)

        self.frame_4 = QFrame(self.frame_2)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(360, 40))
        self.frame_4.setMaximumSize(QSize(380, 120))
        self.frame_4.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
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
        self.lineEdit_selection_id.setFont(font3)
        self.lineEdit_selection_id.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.lineEdit_selection_id.setStyleSheet(u"")
        self.lineEdit_selection_id.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.lineEdit_selection_id, 0, 2, 1, 1)

        self.label_2 = QLabel(self.frame_4)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(100, 28))
        self.label_2.setMaximumSize(QSize(100, 28))
        self.label_2.setFont(font3)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_2, 0, 1, 1, 1)

        self.comboBox_attribution_type = QComboBox(self.frame_4)
        self.comboBox_attribution_type.addItem("")
        self.comboBox_attribution_type.addItem("")
        self.comboBox_attribution_type.addItem("")
        self.comboBox_attribution_type.addItem("")
        self.comboBox_attribution_type.addItem("")
        self.comboBox_attribution_type.setObjectName(u"comboBox_attribution_type")
        self.comboBox_attribution_type.setMinimumSize(QSize(0, 28))
        self.comboBox_attribution_type.setMaximumSize(QSize(16777215, 28))
        self.comboBox_attribution_type.setFont(font2)

        self.gridLayout_5.addWidget(self.comboBox_attribution_type, 0, 3, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_2, 0, 4, 1, 1)


        self.gridLayout_4.addWidget(self.frame_4, 0, 0, 1, 1)

        self.frame_inherit_fluid = QFrame(self.frame_2)
        self.frame_inherit_fluid.setObjectName(u"frame_inherit_fluid")
        self.frame_inherit_fluid.setMinimumSize(QSize(0, 40))
        self.frame_inherit_fluid.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_inherit_fluid.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_13 = QGridLayout(self.frame_inherit_fluid)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_13.setVerticalSpacing(2)
        self.gridLayout_13.setContentsMargins(2, 2, 2, 2)
        self.label_10 = QLabel(self.frame_inherit_fluid)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(100, 28))
        self.label_10.setMaximumSize(QSize(200, 28))
        self.label_10.setFont(font3)
        self.label_10.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_13.addWidget(self.label_10, 0, 1, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_13.addItem(self.horizontalSpacer_3, 0, 0, 1, 1)

        self.comboBox_inherit_fluid_from = QComboBox(self.frame_inherit_fluid)
        self.comboBox_inherit_fluid_from.setObjectName(u"comboBox_inherit_fluid_from")
        self.comboBox_inherit_fluid_from.setMinimumSize(QSize(140, 28))
        self.comboBox_inherit_fluid_from.setMaximumSize(QSize(16777215, 28))

        self.gridLayout_13.addWidget(self.comboBox_inherit_fluid_from, 0, 2, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_13.addItem(self.horizontalSpacer_4, 0, 3, 1, 1)


        self.gridLayout_4.addWidget(self.frame_inherit_fluid, 1, 0, 1, 1)


        self.gridLayout_7.addWidget(self.frame_2, 1, 0, 1, 1)

        self.frame_buttons = QFrame(Dialog)
        self.frame_buttons.setObjectName(u"frame_buttons")
        self.frame_buttons.setMinimumSize(QSize(0, 48))
        self.frame_buttons.setMaximumSize(QSize(16777215, 48))
        self.frame_buttons.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_buttons.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_14 = QGridLayout(self.frame_buttons)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.gridLayout_14.setVerticalSpacing(0)
        self.gridLayout_14.setContentsMargins(6, 0, 6, 0)
        self.pushButton_apply_and_close = QPushButton(self.frame_buttons)
        self.pushButton_apply_and_close.setObjectName(u"pushButton_apply_and_close")
        self.pushButton_apply_and_close.setMinimumSize(QSize(72, 30))
        self.pushButton_apply_and_close.setMaximumSize(QSize(72, 30))
        font5 = QFont()
        font5.setPointSize(10)
        font5.setBold(False)
        font5.setItalic(False)
        self.pushButton_apply_and_close.setFont(font5)
        self.pushButton_apply_and_close.setStyleSheet(u"")
        self.pushButton_apply_and_close.setAutoDefault(False)
        self.pushButton_apply_and_close.setFlat(False)

        self.gridLayout_14.addWidget(self.pushButton_apply_and_close, 0, 3, 1, 1)

        self.pushButton_apply = QPushButton(self.frame_buttons)
        self.pushButton_apply.setObjectName(u"pushButton_apply")
        self.pushButton_apply.setMinimumSize(QSize(72, 30))
        self.pushButton_apply.setMaximumSize(QSize(72, 30))
        self.pushButton_apply.setFont(font5)
        self.pushButton_apply.setStyleSheet(u"")
        self.pushButton_apply.setAutoDefault(False)
        self.pushButton_apply.setFlat(False)

        self.gridLayout_14.addWidget(self.pushButton_apply, 0, 2, 1, 1)

        self.pushButton_cancel = QPushButton(self.frame_buttons)
        self.pushButton_cancel.setObjectName(u"pushButton_cancel")
        self.pushButton_cancel.setMinimumSize(QSize(72, 30))
        self.pushButton_cancel.setMaximumSize(QSize(72, 30))
        self.pushButton_cancel.setFont(font5)
        self.pushButton_cancel.setStyleSheet(u"")
        self.pushButton_cancel.setAutoDefault(False)
        self.pushButton_cancel.setFlat(False)

        self.gridLayout_14.addWidget(self.pushButton_cancel, 0, 0, 1, 1)

        self.horizontalSpacer_17 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_14.addItem(self.horizontalSpacer_17, 0, 1, 1, 1)


        self.gridLayout_7.addWidget(self.frame_buttons, 2, 0, 1, 1)


        self.retranslateUi(Dialog)

        self.tabWidget_main.setCurrentIndex(0)
        self.comboBox_attribution_type.setCurrentIndex(1)
        self.pushButton_apply_and_close.setDefault(False)
        self.pushButton_apply.setDefault(False)
        self.pushButton_cancel.setDefault(False)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Set mass source acoustic excitation", None))
#if QT_CONFIG(whatsthis)
        Dialog.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.label.setText(QCoreApplication.translate("Dialog", u"Mass source setup", None))
        self.label_mass_source_unit.setText(QCoreApplication.translate("Dialog", u"[kg/s]", None))
        self.label_18.setText(QCoreApplication.translate("Dialog", u"Mass source:", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Real", None))
        self.label_20.setText(QCoreApplication.translate("Dialog", u"Imaginary", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_constant_data), QCoreApplication.translate("Dialog", u"Constant data", None))
        self.pushButton_load_table.setText("")
        self.label_11.setText(QCoreApplication.translate("Dialog", u"Choose a table file to import the data", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_tabular_data), QCoreApplication.translate("Dialog", u"Tabular data", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"Node ID:", None))
#if QT_CONFIG(tooltip)
        self.pushButton_get_nearest_node.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Get the nearest Node ID</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_get_nearest_node.setText(QCoreApplication.translate("Dialog", u"Get node", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"x", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"y", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"z", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", u"Node coords:", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Point coords:", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_advanced_search), QCoreApplication.translate("Dialog", u"Advanced search", None))
        self.pushButton_reset.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.pushButton_remove.setText(QCoreApplication.translate("Dialog", u"Remove", None))
        ___qtreewidgetitem = self.treeWidget_mass_source.headerItem()
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("Dialog", u"Values", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"Selection type", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Selection ID", None));
#if QT_CONFIG(tooltip)
        self.treeWidget_mass_source.setToolTip(QCoreApplication.translate("Dialog", u"Select a face to remove the previously attributed boundary condition.", None))
#endif // QT_CONFIG(tooltip)
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_list), QCoreApplication.translate("Dialog", u"List", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Selection ID:", None))
        self.comboBox_attribution_type.setItemText(0, QCoreApplication.translate("Dialog", u"Selected nodes", None))
        self.comboBox_attribution_type.setItemText(1, QCoreApplication.translate("Dialog", u"Selected points", None))
        self.comboBox_attribution_type.setItemText(2, QCoreApplication.translate("Dialog", u"Selected lines", None))
        self.comboBox_attribution_type.setItemText(3, QCoreApplication.translate("Dialog", u"Selected faces", None))
        self.comboBox_attribution_type.setItemText(4, QCoreApplication.translate("Dialog", u"Selected volumes", None))

        self.label_10.setText(QCoreApplication.translate("Dialog", u"Inherit fluid from:", None))
        self.pushButton_apply_and_close.setText(QCoreApplication.translate("Dialog", u"Ok", None))
        self.pushButton_apply.setText(QCoreApplication.translate("Dialog", u"Apply", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
    # retranslateUi



class MassSourceInputs_UI(QDialog, Ui_Dialog):
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
                                                        - lineEdit_imag_value: QLineEdit
                                                        - label_mass_source_unit: QLabel
                                                        - label_18: QLabel
                                                        - label_4: QLabel
                                                        - label_20: QLabel
                                                        - lineEdit_real_value: QLineEdit
                                - tab_tabular_data: QWidget
                                    - (Layout): QGridLayout
                                            - frame_9: QFrame
                                                - (Layout): QGridLayout
                                                        - pushButton_load_table: QPushButton
                                                        - label_11: QLabel
                                                        - lineEdit_table_path: QLineEdit
                                - tab_advanced_search: QWidget
                                    - (Layout): QGridLayout
                                            - frame_7: QFrame
                                                - (Layout): QGridLayout
                                                        - label_8: QLabel
                                                        - lineEdit_nearest_node_id: QLineEdit
                                                        - pushButton_get_nearest_node: QPushButton
                                            - frame_5: QFrame
                                                - (Layout): QGridLayout
                                                        - label_5: QLabel
                                                        - label_6: QLabel
                                                        - label_7: QLabel
                                                        - lineEdit_point_coord_x: QLineEdit
                                                        - lineEdit_point_coord_y: QLineEdit
                                                        - lineEdit_point_coord_z: QLineEdit
                                                        - label_9: QLabel
                                                        - lineEdit_node_coord_x: QLineEdit
                                                        - lineEdit_node_coord_y: QLineEdit
                                                        - lineEdit_node_coord_z: QLineEdit
                                                        - label_3: QLabel
                                - tab_list: QWidget
                                    - (Layout): QGridLayout
                                            - frame_3: QFrame
                                                - (Layout): QGridLayout
                                                        - pushButton_reset: QPushButton
                                                        - pushButton_remove: QPushButton
                                            - treeWidget_mass_source: QTreeWidget
                            - frame_4: QFrame
                                - (Layout): QGridLayout
                                        - lineEdit_selection_id: QLineEdit
                                        - label_2: QLabel
                                        - comboBox_attribution_type: QComboBox
                            - frame_inherit_fluid: QFrame
                                - (Layout): QGridLayout
                                        - label_10: QLabel
                                        - comboBox_inherit_fluid_from: QComboBox
                - frame_buttons: QFrame
                    - (Layout): QGridLayout
                            - pushButton_apply_and_close: QPushButton
                            - pushButton_apply: QPushButton
                            - pushButton_cancel: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
