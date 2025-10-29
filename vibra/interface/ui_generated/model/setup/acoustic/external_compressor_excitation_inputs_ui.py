# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'external_compressor_excitation_inputs.ui'
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
        Dialog.setWindowModality(Qt.WindowModal)
        Dialog.resize(480, 660)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(480, 660))
        Dialog.setMaximumSize(QSize(480, 660))
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

        self.frame_11 = QFrame(Dialog)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setMinimumSize(QSize(340, 40))
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
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        self.pushButton_attribute.setFont(font2)
        self.pushButton_attribute.setStyleSheet(u"")
        self.pushButton_attribute.setAutoDefault(False)

        self.gridLayout_14.addWidget(self.pushButton_attribute, 0, 1, 1, 1)

        self.pushButton_exit = QPushButton(self.frame_11)
        self.pushButton_exit.setObjectName(u"pushButton_exit")
        self.pushButton_exit.setMinimumSize(QSize(100, 28))
        self.pushButton_exit.setMaximumSize(QSize(100, 28))
        self.pushButton_exit.setFont(font2)
        self.pushButton_exit.setStyleSheet(u"")
        self.pushButton_exit.setAutoDefault(False)

        self.gridLayout_14.addWidget(self.pushButton_exit, 0, 0, 1, 1)


        self.gridLayout_7.addWidget(self.frame_11, 2, 0, 1, 1)

        self.frame_2 = QFrame(Dialog)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(380, 280))
        self.frame_2.setMaximumSize(QSize(16777215, 600))
        self.frame_2.setFrameShape(QFrame.Box)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.frame_4 = QFrame(self.frame_2)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(360, 40))
        self.frame_4.setMaximumSize(QSize(16777215, 40))
        self.frame_4.setFrameShape(QFrame.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_4)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setHorizontalSpacing(6)
        self.gridLayout_5.setVerticalSpacing(2)
        self.gridLayout_5.setContentsMargins(2, 2, 2, 2)
        self.lineEdit_selection_id = QLineEdit(self.frame_4)
        self.lineEdit_selection_id.setObjectName(u"lineEdit_selection_id")
        self.lineEdit_selection_id.setMinimumSize(QSize(120, 28))
        self.lineEdit_selection_id.setMaximumSize(QSize(120, 28))
        self.lineEdit_selection_id.setFont(font2)
        self.lineEdit_selection_id.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_selection_id.setStyleSheet(u"")
        self.lineEdit_selection_id.setAlignment(Qt.AlignCenter)

        self.gridLayout_5.addWidget(self.lineEdit_selection_id, 0, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.label_2 = QLabel(self.frame_4)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(80, 28))
        self.label_2.setMaximumSize(QSize(100, 28))
        self.label_2.setFont(font2)
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_2, 0, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_2, 0, 3, 1, 1)


        self.gridLayout_4.addWidget(self.frame_4, 0, 0, 1, 1)

        self.tabWidget_main = QTabWidget(self.frame_2)
        self.tabWidget_main.setObjectName(u"tabWidget_main")
        self.tabWidget_main.setMinimumSize(QSize(360, 0))
        self.tabWidget_main.setMaximumSize(QSize(16777215, 16777215))
        font3 = QFont()
        font3.setPointSize(10)
        self.tabWidget_main.setFont(font3)
        self.tab_tabular_data = QWidget()
        self.tab_tabular_data.setObjectName(u"tab_tabular_data")
        self.gridLayout_3 = QGridLayout(self.tab_tabular_data)
        self.gridLayout_3.setSpacing(2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(2, 6, 2, 6)
        self.frame_5 = QFrame(self.tab_tabular_data)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.gridLayout_11 = QGridLayout(self.frame_5)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.label_9 = QLabel(self.frame_5)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMinimumSize(QSize(140, 28))
        self.label_9.setMaximumSize(QSize(16777215, 28))
        self.label_9.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_11.addWidget(self.label_9, 9, 1, 1, 1)

        self.lineEdit_maximum_frequency = QLineEdit(self.frame_5)
        self.lineEdit_maximum_frequency.setObjectName(u"lineEdit_maximum_frequency")
        self.lineEdit_maximum_frequency.setMinimumSize(QSize(200, 28))
        self.lineEdit_maximum_frequency.setMaximumSize(QSize(16777215, 28))
        self.lineEdit_maximum_frequency.setAlignment(Qt.AlignCenter)

        self.gridLayout_11.addWidget(self.lineEdit_maximum_frequency, 9, 2, 1, 1)

        self.label_11 = QLabel(self.frame_5)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout_11.addWidget(self.label_11, 9, 3, 1, 1)

        self.label_10 = QLabel(self.frame_5)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_11.addWidget(self.label_10, 10, 3, 1, 1)

        self.lineEdit_frequency_resolution_required = QLineEdit(self.frame_5)
        self.lineEdit_frequency_resolution_required.setObjectName(u"lineEdit_frequency_resolution_required")
        self.lineEdit_frequency_resolution_required.setMinimumSize(QSize(200, 28))
        self.lineEdit_frequency_resolution_required.setMaximumSize(QSize(16777215, 28))
        self.lineEdit_frequency_resolution_required.setAlignment(Qt.AlignCenter)

        self.gridLayout_11.addWidget(self.lineEdit_frequency_resolution_required, 10, 2, 1, 1)

        self.label_14 = QLabel(self.frame_5)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setMinimumSize(QSize(140, 28))
        self.label_14.setMaximumSize(QSize(16777215, 28))
        self.label_14.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_11.addWidget(self.label_14, 7, 1, 1, 1)

        self.comboBox_single_revolution = QComboBox(self.frame_5)
        self.comboBox_single_revolution.addItem("")
        self.comboBox_single_revolution.addItem("")
        self.comboBox_single_revolution.setObjectName(u"comboBox_single_revolution")
        self.comboBox_single_revolution.setMinimumSize(QSize(200, 28))
        self.comboBox_single_revolution.setMaximumSize(QSize(16777215, 28))

        self.gridLayout_11.addWidget(self.comboBox_single_revolution, 7, 2, 1, 1)

        self.comboBox_normal_velocity_axis = QComboBox(self.frame_5)
        self.comboBox_normal_velocity_axis.addItem("")
        self.comboBox_normal_velocity_axis.addItem("")
        self.comboBox_normal_velocity_axis.addItem("")
        self.comboBox_normal_velocity_axis.addItem("")
        self.comboBox_normal_velocity_axis.addItem("")
        self.comboBox_normal_velocity_axis.addItem("")
        self.comboBox_normal_velocity_axis.setObjectName(u"comboBox_normal_velocity_axis")
        self.comboBox_normal_velocity_axis.setMinimumSize(QSize(200, 28))
        self.comboBox_normal_velocity_axis.setMaximumSize(QSize(16777215, 28))

        self.gridLayout_11.addWidget(self.comboBox_normal_velocity_axis, 6, 2, 1, 1)

        self.label_normal_velocity_axis = QLabel(self.frame_5)
        self.label_normal_velocity_axis.setObjectName(u"label_normal_velocity_axis")
        self.label_normal_velocity_axis.setMinimumSize(QSize(140, 28))
        self.label_normal_velocity_axis.setMaximumSize(QSize(16777215, 28))
        self.label_normal_velocity_axis.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_11.addWidget(self.label_normal_velocity_axis, 6, 1, 1, 1)

        self.label_6 = QLabel(self.frame_5)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(140, 28))
        self.label_6.setMaximumSize(QSize(16777215, 28))
        self.label_6.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_11.addWidget(self.label_6, 8, 1, 1, 1)

        self.label_7 = QLabel(self.frame_5)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_11.addWidget(self.label_7, 8, 3, 1, 1)

        self.comboBox_data_source = QComboBox(self.frame_5)
        self.comboBox_data_source.addItem("")
        self.comboBox_data_source.addItem("")
        self.comboBox_data_source.addItem("")
        self.comboBox_data_source.setObjectName(u"comboBox_data_source")
        self.comboBox_data_source.setMinimumSize(QSize(200, 28))
        self.comboBox_data_source.setMaximumSize(QSize(16777215, 28))

        self.gridLayout_11.addWidget(self.comboBox_data_source, 1, 2, 1, 1)

        self.label_5 = QLabel(self.frame_5)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(140, 28))
        self.label_5.setMaximumSize(QSize(16777215, 28))
        self.label_5.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_11.addWidget(self.label_5, 1, 1, 1, 1)

        self.label_excitation_mapping = QLabel(self.frame_5)
        self.label_excitation_mapping.setObjectName(u"label_excitation_mapping")
        self.label_excitation_mapping.setMinimumSize(QSize(140, 28))
        self.label_excitation_mapping.setMaximumSize(QSize(16777215, 28))
        self.label_excitation_mapping.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_11.addWidget(self.label_excitation_mapping, 5, 1, 1, 1)

        self.comboBox_excitation_mapping = QComboBox(self.frame_5)
        self.comboBox_excitation_mapping.addItem("")
        self.comboBox_excitation_mapping.addItem("")
        self.comboBox_excitation_mapping.setObjectName(u"comboBox_excitation_mapping")
        self.comboBox_excitation_mapping.setMinimumSize(QSize(200, 28))
        self.comboBox_excitation_mapping.setMaximumSize(QSize(16777215, 28))

        self.gridLayout_11.addWidget(self.comboBox_excitation_mapping, 5, 2, 1, 1)

        self.label_15 = QLabel(self.frame_5)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setMinimumSize(QSize(140, 28))
        self.label_15.setMaximumSize(QSize(16777215, 28))
        self.label_15.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_11.addWidget(self.label_15, 3, 1, 1, 1)

        self.comboBox_connection_type = QComboBox(self.frame_5)
        self.comboBox_connection_type.addItem("")
        self.comboBox_connection_type.addItem("")
        self.comboBox_connection_type.setObjectName(u"comboBox_connection_type")
        self.comboBox_connection_type.setMinimumSize(QSize(200, 28))
        self.comboBox_connection_type.setMaximumSize(QSize(16777215, 28))

        self.gridLayout_11.addWidget(self.comboBox_connection_type, 3, 2, 1, 1)

        self.lineEdit_angular_resolution = QLineEdit(self.frame_5)
        self.lineEdit_angular_resolution.setObjectName(u"lineEdit_angular_resolution")
        self.lineEdit_angular_resolution.setMinimumSize(QSize(200, 28))
        self.lineEdit_angular_resolution.setMaximumSize(QSize(16777215, 28))
        self.lineEdit_angular_resolution.setAlignment(Qt.AlignCenter)

        self.gridLayout_11.addWidget(self.lineEdit_angular_resolution, 8, 2, 1, 1)

        self.label_8 = QLabel(self.frame_5)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMinimumSize(QSize(140, 28))
        self.label_8.setMaximumSize(QSize(16777215, 28))
        self.label_8.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_11.addWidget(self.label_8, 10, 1, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_11.addItem(self.horizontalSpacer_6, 12, 0, 1, 1)

        self.label_16 = QLabel(self.frame_5)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setMinimumSize(QSize(140, 28))
        self.label_16.setMaximumSize(QSize(16777215, 28))
        self.label_16.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_11.addWidget(self.label_16, 2, 1, 1, 1)

        self.lineEdit_frequency_resolution = QLineEdit(self.frame_5)
        self.lineEdit_frequency_resolution.setObjectName(u"lineEdit_frequency_resolution")
        self.lineEdit_frequency_resolution.setEnabled(False)
        self.lineEdit_frequency_resolution.setMinimumSize(QSize(200, 28))
        self.lineEdit_frequency_resolution.setMaximumSize(QSize(16777215, 28))
        self.lineEdit_frequency_resolution.setAlignment(Qt.AlignCenter)

        self.gridLayout_11.addWidget(self.lineEdit_frequency_resolution, 12, 2, 1, 1)

        self.label_13 = QLabel(self.frame_5)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout_11.addWidget(self.label_13, 12, 3, 1, 1)

        self.label_12 = QLabel(self.frame_5)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setMinimumSize(QSize(140, 28))
        self.label_12.setMaximumSize(QSize(16777215, 28))
        self.label_12.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_11.addWidget(self.label_12, 12, 1, 1, 1)

        self.comboBox_compressor_type = QComboBox(self.frame_5)
        self.comboBox_compressor_type.addItem("")
        self.comboBox_compressor_type.addItem("")
        self.comboBox_compressor_type.addItem("")
        self.comboBox_compressor_type.setObjectName(u"comboBox_compressor_type")
        self.comboBox_compressor_type.setMinimumSize(QSize(200, 28))
        self.comboBox_compressor_type.setMaximumSize(QSize(16777215, 28))

        self.gridLayout_11.addWidget(self.comboBox_compressor_type, 2, 2, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_11.addItem(self.horizontalSpacer_7, 12, 4, 1, 1)

        self.label_17 = QLabel(self.frame_5)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setMinimumSize(QSize(140, 28))
        self.label_17.setMaximumSize(QSize(16777215, 28))
        self.label_17.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_11.addWidget(self.label_17, 4, 1, 1, 1)

        self.comboBox_excitation_type = QComboBox(self.frame_5)
        self.comboBox_excitation_type.addItem("")
        self.comboBox_excitation_type.addItem("")
        self.comboBox_excitation_type.addItem("")
        self.comboBox_excitation_type.setObjectName(u"comboBox_excitation_type")
        self.comboBox_excitation_type.setMinimumSize(QSize(200, 28))
        self.comboBox_excitation_type.setMaximumSize(QSize(16777215, 28))

        self.gridLayout_11.addWidget(self.comboBox_excitation_type, 4, 2, 1, 1)


        self.gridLayout_3.addWidget(self.frame_5, 3, 0, 1, 1)

        self.frame_9 = QFrame(self.tab_tabular_data)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setMinimumSize(QSize(260, 0))
        self.frame_9.setMaximumSize(QSize(16777215, 200))
        self.frame_9.setFrameShape(QFrame.NoFrame)
        self.frame_9.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_9)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setHorizontalSpacing(6)
        self.gridLayout_2.setVerticalSpacing(2)
        self.gridLayout_2.setContentsMargins(0, 4, 0, 0)
        self.lineEdit_table_path = QLineEdit(self.frame_9)
        self.lineEdit_table_path.setObjectName(u"lineEdit_table_path")
        self.lineEdit_table_path.setEnabled(True)
        self.lineEdit_table_path.setMinimumSize(QSize(360, 28))
        self.lineEdit_table_path.setMaximumSize(QSize(600, 28))
        font4 = QFont()
        font4.setPointSize(9)
        font4.setBold(False)
        self.lineEdit_table_path.setFont(font4)
        self.lineEdit_table_path.setStyleSheet(u"")
        self.lineEdit_table_path.setAlignment(Qt.AlignCenter)
        self.lineEdit_table_path.setClearButtonEnabled(True)

        self.gridLayout_2.addWidget(self.lineEdit_table_path, 0, 1, 1, 1)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_11, 0, 0, 1, 1)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_12, 0, 4, 1, 1)

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
        self.pushButton_load_table.setFont(font2)
        self.pushButton_load_table.setStyleSheet(u"")
        icon = QIcon()
        icon.addFile(u":/icons/document_search_blue.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_load_table.setIcon(icon)
        self.pushButton_load_table.setIconSize(QSize(20, 20))
        self.pushButton_load_table.setAutoDefault(False)

        self.gridLayout_2.addWidget(self.pushButton_load_table, 0, 2, 1, 1)


        self.gridLayout_3.addWidget(self.frame_9, 1, 0, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer_3, 4, 0, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer_4, 0, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer, 2, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_tabular_data, "")
        self.tab_list = QWidget()
        self.tab_list.setObjectName(u"tab_list")
        self.gridLayout_9 = QGridLayout(self.tab_list)
        self.gridLayout_9.setSpacing(2)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(6, 8, 6, 2)
        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_9.addItem(self.verticalSpacer_5, 3, 0, 1, 1)

        self.frame_3 = QFrame(self.tab_list)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(320, 40))
        self.frame_3.setMaximumSize(QSize(1000, 40))
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


        self.gridLayout_9.addWidget(self.frame_3, 2, 0, 1, 1)

        self.treeWidget_surface_velocity = QTreeWidget(self.tab_list)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(2, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter);
        self.treeWidget_surface_velocity.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_surface_velocity.setObjectName(u"treeWidget_surface_velocity")
        self.treeWidget_surface_velocity.setMinimumSize(QSize(320, 100))
        self.treeWidget_surface_velocity.setMaximumSize(QSize(1000, 200))
        font5 = QFont()
        font5.setFamilies([u"MS Shell Dlg 2"])
        font5.setPointSize(9)
        font5.setItalic(False)
        self.treeWidget_surface_velocity.setFont(font5)
        self.treeWidget_surface_velocity.setIndentation(1)
        self.treeWidget_surface_velocity.setHeaderHidden(False)
        self.treeWidget_surface_velocity.header().setHighlightSections(False)
        self.treeWidget_surface_velocity.header().setProperty(u"showSortIndicator", False)
        self.treeWidget_surface_velocity.header().setStretchLastSection(True)

        self.gridLayout_9.addWidget(self.treeWidget_surface_velocity, 1, 0, 1, 1)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_9.addItem(self.verticalSpacer_6, 0, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_list, "")

        self.gridLayout_4.addWidget(self.tabWidget_main, 1, 0, 1, 1)


        self.gridLayout_7.addWidget(self.frame_2, 1, 0, 1, 1)


        self.retranslateUi(Dialog)

        self.tabWidget_main.setCurrentIndex(0)
        self.comboBox_single_revolution.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Set surface velocity acoustic excitation", None))
#if QT_CONFIG(whatsthis)
        Dialog.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.label.setText(QCoreApplication.translate("Dialog", u"External compressor excitation", None))
        self.pushButton_attribute.setText(QCoreApplication.translate("Dialog", u"Attribute", None))
        self.pushButton_exit.setText(QCoreApplication.translate("Dialog", u"Exit", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Selection ID:", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", u"Maximum frequency:", None))
        self.lineEdit_maximum_frequency.setText(QCoreApplication.translate("Dialog", u"1500", None))
        self.label_11.setText(QCoreApplication.translate("Dialog", u"[Hz]", None))
        self.label_10.setText(QCoreApplication.translate("Dialog", u"[Hz]", None))
        self.lineEdit_frequency_resolution_required.setText(QCoreApplication.translate("Dialog", u"10", None))
        self.label_14.setText(QCoreApplication.translate("Dialog", u"Single revolution?:", None))
        self.comboBox_single_revolution.setItemText(0, QCoreApplication.translate("Dialog", u"Yes", None))
        self.comboBox_single_revolution.setItemText(1, QCoreApplication.translate("Dialog", u"No", None))

        self.comboBox_normal_velocity_axis.setItemText(0, QCoreApplication.translate("Dialog", u"x-axis (+)", None))
        self.comboBox_normal_velocity_axis.setItemText(1, QCoreApplication.translate("Dialog", u"y-axis (+)", None))
        self.comboBox_normal_velocity_axis.setItemText(2, QCoreApplication.translate("Dialog", u"z-axis (+)", None))
        self.comboBox_normal_velocity_axis.setItemText(3, QCoreApplication.translate("Dialog", u"x-axis (-)", None))
        self.comboBox_normal_velocity_axis.setItemText(4, QCoreApplication.translate("Dialog", u"y-axis (-)", None))
        self.comboBox_normal_velocity_axis.setItemText(5, QCoreApplication.translate("Dialog", u"z-axis (-)", None))

        self.label_normal_velocity_axis.setText(QCoreApplication.translate("Dialog", u"Normal velocity axis:", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"Angular resolution:", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"[deg]", None))
        self.comboBox_data_source.setItemText(0, QCoreApplication.translate("Dialog", u"SCORG", None))
        self.comboBox_data_source.setItemText(1, QCoreApplication.translate("Dialog", u"CFD", None))
        self.comboBox_data_source.setItemText(2, QCoreApplication.translate("Dialog", u"Other", None))

        self.label_5.setText(QCoreApplication.translate("Dialog", u"Data source:", None))
        self.label_excitation_mapping.setText(QCoreApplication.translate("Dialog", u"Excitation mapping:", None))
        self.comboBox_excitation_mapping.setItemText(0, QCoreApplication.translate("Dialog", u"Surface averaged", None))
        self.comboBox_excitation_mapping.setItemText(1, QCoreApplication.translate("Dialog", u"Nodal mapping", None))

        self.label_15.setText(QCoreApplication.translate("Dialog", u"Connection type:", None))
        self.comboBox_connection_type.setItemText(0, QCoreApplication.translate("Dialog", u"Discharge", None))
        self.comboBox_connection_type.setItemText(1, QCoreApplication.translate("Dialog", u"Suction", None))

        self.lineEdit_angular_resolution.setText("")
        self.label_8.setText(QCoreApplication.translate("Dialog", u"Freq. step (req.):", None))
        self.label_16.setText(QCoreApplication.translate("Dialog", u"Compressor type:", None))
        self.lineEdit_frequency_resolution.setText(QCoreApplication.translate("Dialog", u"not calculated", None))
        self.label_13.setText(QCoreApplication.translate("Dialog", u"[Hz]", None))
        self.label_12.setText(QCoreApplication.translate("Dialog", u"Freq. step (final):", None))
        self.comboBox_compressor_type.setItemText(0, QCoreApplication.translate("Dialog", u"Screw", None))
        self.comboBox_compressor_type.setItemText(1, QCoreApplication.translate("Dialog", u"Centrifugal", None))
        self.comboBox_compressor_type.setItemText(2, QCoreApplication.translate("Dialog", u"Reciprocating", None))

        self.label_17.setText(QCoreApplication.translate("Dialog", u"Excitation type:", None))
        self.comboBox_excitation_type.setItemText(0, QCoreApplication.translate("Dialog", u"Mass flow rate -> kg/s", None))
        self.comboBox_excitation_type.setItemText(1, QCoreApplication.translate("Dialog", u"Surface velocity -> m/s", None))
        self.comboBox_excitation_type.setItemText(2, QCoreApplication.translate("Dialog", u"Volumetric flow rate -> m\u00b3/s", None))

        self.pushButton_load_table.setText("")
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_tabular_data), QCoreApplication.translate("Dialog", u"Setup", None))
        self.pushButton_reset.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.pushButton_remove.setText(QCoreApplication.translate("Dialog", u"Remove", None))
        ___qtreewidgetitem = self.treeWidget_surface_velocity.headerItem()
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("Dialog", u"Angular resolution [deg]", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"Source", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Surface ID", None));
#if QT_CONFIG(tooltip)
        self.treeWidget_surface_velocity.setToolTip(QCoreApplication.translate("Dialog", u"Select a face to remove the previously attributed boundary condition.", None))
#endif // QT_CONFIG(tooltip)
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_list), QCoreApplication.translate("Dialog", u"List", None))
    # retranslateUi



class ExternalCompressorExcitationInputs_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
                - frame_11: QFrame
                    - (Layout): QGridLayout
                            - pushButton_attribute: QPushButton
                            - pushButton_exit: QPushButton
                - frame_2: QFrame
                    - (Layout): QGridLayout
                            - frame_4: QFrame
                                - (Layout): QGridLayout
                                        - lineEdit_selection_id: QLineEdit
                                        - label_2: QLabel
                            - tabWidget_main: QTabWidget
                                - tab_tabular_data: QWidget
                                    - (Layout): QGridLayout
                                            - frame_5: QFrame
                                                - (Layout): QGridLayout
                                                        - label_9: QLabel
                                                        - lineEdit_maximum_frequency: QLineEdit
                                                        - label_11: QLabel
                                                        - label_10: QLabel
                                                        - lineEdit_frequency_resolution_required: QLineEdit
                                                        - label_14: QLabel
                                                        - comboBox_single_revolution: QComboBox
                                                        - comboBox_normal_velocity_axis: QComboBox
                                                        - label_normal_velocity_axis: QLabel
                                                        - label_6: QLabel
                                                        - label_7: QLabel
                                                        - comboBox_data_source: QComboBox
                                                        - label_5: QLabel
                                                        - label_excitation_mapping: QLabel
                                                        - comboBox_excitation_mapping: QComboBox
                                                        - label_15: QLabel
                                                        - comboBox_connection_type: QComboBox
                                                        - lineEdit_angular_resolution: QLineEdit
                                                        - label_8: QLabel
                                                        - label_16: QLabel
                                                        - lineEdit_frequency_resolution: QLineEdit
                                                        - label_13: QLabel
                                                        - label_12: QLabel
                                                        - comboBox_compressor_type: QComboBox
                                                        - label_17: QLabel
                                                        - comboBox_excitation_type: QComboBox
                                            - frame_9: QFrame
                                                - (Layout): QGridLayout
                                                        - lineEdit_table_path: QLineEdit
                                                        - pushButton_load_table: QPushButton
                                - tab_list: QWidget
                                    - (Layout): QGridLayout
                                            - frame_3: QFrame
                                                - (Layout): QGridLayout
                                                        - pushButton_reset: QPushButton
                                                        - pushButton_remove: QPushButton
                                            - treeWidget_surface_velocity: QTreeWidget
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
