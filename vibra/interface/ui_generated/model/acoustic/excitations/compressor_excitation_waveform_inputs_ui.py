# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'compressor_excitation_waveform_inputs.ui'
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
    QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
    QSpinBox, QTabWidget, QTreeWidget, QTreeWidgetItem,
    QWidget)

from vibra.interface.formatters.icons import Icon

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setWindowModality(Qt.WindowModality.WindowModal)
        Dialog.resize(500, 736)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(500, 480))
        Dialog.setMaximumSize(QSize(560, 800))
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
        self.frame_2.setMaximumSize(QSize(16777215, 16777215))
        self.frame_2.setFrameShape(QFrame.Shape.Box)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.tabWidget_main = QTabWidget(self.frame_2)
        self.tabWidget_main.setObjectName(u"tabWidget_main")
        self.tabWidget_main.setMinimumSize(QSize(360, 0))
        self.tabWidget_main.setMaximumSize(QSize(16777215, 16777215))
        font2 = QFont()
        font2.setPointSize(10)
        font2.setBold(False)
        self.tabWidget_main.setFont(font2)
        self.tab_setup = QWidget()
        self.tab_setup.setObjectName(u"tab_setup")
        self.gridLayout_3 = QGridLayout(self.tab_setup)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(4, 4, 4, 4)
        self.scrollArea_setup = QScrollArea(self.tab_setup)
        self.scrollArea_setup.setObjectName(u"scrollArea_setup")
        self.scrollArea_setup.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollArea_setup.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 456, 510))
        self.gridLayout = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName(u"gridLayout")
        self.frame_5 = QFrame(self.scrollAreaWidgetContents)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_11 = QGridLayout(self.frame_5)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.comboBox_data_source = QComboBox(self.frame_5)
        self.comboBox_data_source.addItem("")
        self.comboBox_data_source.addItem("")
        self.comboBox_data_source.addItem("")
        self.comboBox_data_source.setObjectName(u"comboBox_data_source")
        self.comboBox_data_source.setMinimumSize(QSize(200, 28))
        self.comboBox_data_source.setMaximumSize(QSize(16777215, 28))

        self.gridLayout_11.addWidget(self.comboBox_data_source, 1, 2, 1, 1)

        self.label_7 = QLabel(self.frame_5)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_11.addWidget(self.label_7, 8, 3, 1, 1)

        self.label_normal_velocity_axis = QLabel(self.frame_5)
        self.label_normal_velocity_axis.setObjectName(u"label_normal_velocity_axis")
        self.label_normal_velocity_axis.setMinimumSize(QSize(140, 28))
        self.label_normal_velocity_axis.setMaximumSize(QSize(16777215, 28))
        self.label_normal_velocity_axis.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_11.addWidget(self.label_normal_velocity_axis, 6, 1, 1, 1)

        self.label_6 = QLabel(self.frame_5)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(140, 28))
        self.label_6.setMaximumSize(QSize(16777215, 28))
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_11.addWidget(self.label_6, 8, 1, 1, 1)

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

        self.label_9 = QLabel(self.frame_5)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMinimumSize(QSize(140, 28))
        self.label_9.setMaximumSize(QSize(16777215, 28))
        self.label_9.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_11.addWidget(self.label_9, 9, 1, 1, 1)

        self.lineEdit_maximum_frequency = QLineEdit(self.frame_5)
        self.lineEdit_maximum_frequency.setObjectName(u"lineEdit_maximum_frequency")
        self.lineEdit_maximum_frequency.setMinimumSize(QSize(200, 28))
        self.lineEdit_maximum_frequency.setMaximumSize(QSize(16777215, 28))
        self.lineEdit_maximum_frequency.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.lineEdit_maximum_frequency, 9, 2, 1, 1)

        self.lineEdit_frequency_resolution_required = QLineEdit(self.frame_5)
        self.lineEdit_frequency_resolution_required.setObjectName(u"lineEdit_frequency_resolution_required")
        self.lineEdit_frequency_resolution_required.setMinimumSize(QSize(200, 28))
        self.lineEdit_frequency_resolution_required.setMaximumSize(QSize(16777215, 28))
        self.lineEdit_frequency_resolution_required.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.lineEdit_frequency_resolution_required, 10, 2, 1, 1)

        self.label_10 = QLabel(self.frame_5)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_11.addWidget(self.label_10, 10, 3, 1, 1)

        self.label_11 = QLabel(self.frame_5)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout_11.addWidget(self.label_11, 9, 3, 1, 1)

        self.comboBox_single_revolution = QComboBox(self.frame_5)
        self.comboBox_single_revolution.addItem("")
        self.comboBox_single_revolution.addItem("")
        self.comboBox_single_revolution.setObjectName(u"comboBox_single_revolution")
        self.comboBox_single_revolution.setMinimumSize(QSize(200, 28))
        self.comboBox_single_revolution.setMaximumSize(QSize(16777215, 28))

        self.gridLayout_11.addWidget(self.comboBox_single_revolution, 7, 2, 1, 1)

        self.label_14 = QLabel(self.frame_5)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setMinimumSize(QSize(140, 28))
        self.label_14.setMaximumSize(QSize(16777215, 28))
        self.label_14.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_11.addWidget(self.label_14, 7, 1, 1, 1)

        self.comboBox_excitation_mapping = QComboBox(self.frame_5)
        self.comboBox_excitation_mapping.addItem("")
        self.comboBox_excitation_mapping.addItem("")
        self.comboBox_excitation_mapping.setObjectName(u"comboBox_excitation_mapping")
        self.comboBox_excitation_mapping.setMinimumSize(QSize(200, 28))
        self.comboBox_excitation_mapping.setMaximumSize(QSize(16777215, 28))

        self.gridLayout_11.addWidget(self.comboBox_excitation_mapping, 5, 2, 1, 1)

        self.label_5 = QLabel(self.frame_5)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(140, 28))
        self.label_5.setMaximumSize(QSize(16777215, 28))
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_11.addWidget(self.label_5, 1, 1, 1, 1)

        self.label_15 = QLabel(self.frame_5)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setMinimumSize(QSize(140, 28))
        self.label_15.setMaximumSize(QSize(16777215, 28))
        self.label_15.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_11.addWidget(self.label_15, 3, 1, 1, 1)

        self.label_excitation_mapping = QLabel(self.frame_5)
        self.label_excitation_mapping.setObjectName(u"label_excitation_mapping")
        self.label_excitation_mapping.setMinimumSize(QSize(140, 28))
        self.label_excitation_mapping.setMaximumSize(QSize(16777215, 28))
        self.label_excitation_mapping.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_11.addWidget(self.label_excitation_mapping, 5, 1, 1, 1)

        self.label_8 = QLabel(self.frame_5)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMinimumSize(QSize(140, 28))
        self.label_8.setMaximumSize(QSize(16777215, 28))
        self.label_8.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_11.addWidget(self.label_8, 10, 1, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_11.addItem(self.horizontalSpacer_6, 12, 0, 1, 1)

        self.comboBox_connection_type = QComboBox(self.frame_5)
        self.comboBox_connection_type.addItem("")
        self.comboBox_connection_type.addItem("")
        self.comboBox_connection_type.setObjectName(u"comboBox_connection_type")
        self.comboBox_connection_type.setMinimumSize(QSize(200, 28))
        self.comboBox_connection_type.setMaximumSize(QSize(16777215, 28))

        self.gridLayout_11.addWidget(self.comboBox_connection_type, 3, 2, 1, 1)

        self.label_16 = QLabel(self.frame_5)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setMinimumSize(QSize(140, 28))
        self.label_16.setMaximumSize(QSize(16777215, 28))
        self.label_16.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_11.addWidget(self.label_16, 2, 1, 1, 1)

        self.lineEdit_angular_resolution = QLineEdit(self.frame_5)
        self.lineEdit_angular_resolution.setObjectName(u"lineEdit_angular_resolution")
        self.lineEdit_angular_resolution.setMinimumSize(QSize(200, 28))
        self.lineEdit_angular_resolution.setMaximumSize(QSize(16777215, 28))
        self.lineEdit_angular_resolution.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.lineEdit_angular_resolution, 8, 2, 1, 1)

        self.comboBox_compressor_type = QComboBox(self.frame_5)
        self.comboBox_compressor_type.addItem("")
        self.comboBox_compressor_type.addItem("")
        self.comboBox_compressor_type.addItem("")
        self.comboBox_compressor_type.setObjectName(u"comboBox_compressor_type")
        self.comboBox_compressor_type.setMinimumSize(QSize(200, 28))
        self.comboBox_compressor_type.setMaximumSize(QSize(16777215, 28))

        self.gridLayout_11.addWidget(self.comboBox_compressor_type, 2, 2, 1, 1)

        self.label_12 = QLabel(self.frame_5)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setMinimumSize(QSize(140, 28))
        self.label_12.setMaximumSize(QSize(16777215, 28))
        self.label_12.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_11.addWidget(self.label_12, 12, 1, 1, 1)

        self.lineEdit_frequency_resolution = QLineEdit(self.frame_5)
        self.lineEdit_frequency_resolution.setObjectName(u"lineEdit_frequency_resolution")
        self.lineEdit_frequency_resolution.setEnabled(False)
        self.lineEdit_frequency_resolution.setMinimumSize(QSize(200, 28))
        self.lineEdit_frequency_resolution.setMaximumSize(QSize(16777215, 28))
        self.lineEdit_frequency_resolution.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.lineEdit_frequency_resolution, 12, 2, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_11.addItem(self.horizontalSpacer_7, 12, 4, 1, 1)

        self.label_13 = QLabel(self.frame_5)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout_11.addWidget(self.label_13, 12, 3, 1, 1)

        self.comboBox_excitation_type = QComboBox(self.frame_5)
        self.comboBox_excitation_type.addItem("")
        self.comboBox_excitation_type.addItem("")
        self.comboBox_excitation_type.addItem("")
        self.comboBox_excitation_type.setObjectName(u"comboBox_excitation_type")
        self.comboBox_excitation_type.setMinimumSize(QSize(200, 28))
        self.comboBox_excitation_type.setMaximumSize(QSize(16777215, 28))

        self.gridLayout_11.addWidget(self.comboBox_excitation_type, 4, 2, 1, 1)

        self.label_17 = QLabel(self.frame_5)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setMinimumSize(QSize(140, 28))
        self.label_17.setMaximumSize(QSize(16777215, 28))
        self.label_17.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_11.addWidget(self.label_17, 4, 1, 1, 1)


        self.gridLayout.addWidget(self.frame_5, 1, 0, 1, 1)

        self.frame_9 = QFrame(self.scrollAreaWidgetContents)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setMinimumSize(QSize(260, 72))
        self.frame_9.setMaximumSize(QSize(16777215, 72))
        self.frame_9.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_9.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_9)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(4, 4, 4, 4)
        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_11, 1, 0, 1, 1)

        self.lineEdit_table_path = QLineEdit(self.frame_9)
        self.lineEdit_table_path.setObjectName(u"lineEdit_table_path")
        self.lineEdit_table_path.setEnabled(True)
        self.lineEdit_table_path.setMinimumSize(QSize(360, 28))
        self.lineEdit_table_path.setMaximumSize(QSize(600, 28))
        font3 = QFont()
        font3.setPointSize(9)
        font3.setBold(False)
        self.lineEdit_table_path.setFont(font3)
        self.lineEdit_table_path.setStyleSheet(u"")
        self.lineEdit_table_path.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_table_path.setClearButtonEnabled(True)

        self.gridLayout_2.addWidget(self.lineEdit_table_path, 1, 1, 1, 1)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_12, 1, 4, 1, 1)

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
        font4 = QFont()
        font4.setFamilies([u"MS Shell Dlg 2"])
        font4.setPointSize(10)
        font4.setBold(False)
        font4.setItalic(False)
        self.pushButton_load_table.setFont(font4)
        self.pushButton_load_table.setStyleSheet(u"")
        icon = Icon(u":/icons/document_search_blue.png")
        self.pushButton_load_table.setIcon(icon)
        self.pushButton_load_table.setIconSize(QSize(20, 20))
        self.pushButton_load_table.setAutoDefault(False)

        self.gridLayout_2.addWidget(self.pushButton_load_table, 1, 2, 1, 1)

        self.label_4 = QLabel(self.frame_9)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(0, 32))
        self.label_4.setMaximumSize(QSize(16777215, 32))
        self.label_4.setFrameShape(QFrame.Shape.NoFrame)
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.label_4, 0, 1, 1, 1)


        self.gridLayout.addWidget(self.frame_9, 0, 0, 1, 1)

        self.scrollArea_setup.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_3.addWidget(self.scrollArea_setup, 0, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_setup, "")
        self.tab_signals = QWidget()
        self.tab_signals.setObjectName(u"tab_signals")
        self.gridLayout_13 = QGridLayout(self.tab_signals)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_13.setContentsMargins(4, 4, 4, 4)
        self.scrollArea_plots = QScrollArea(self.tab_signals)
        self.scrollArea_plots.setObjectName(u"scrollArea_plots")
        self.scrollArea_plots.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollArea_plots.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 424, 268))
        self.gridLayout_17 = QGridLayout(self.scrollAreaWidgetContents_2)
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.gridLayout_17.setContentsMargins(4, 4, 4, 4)
        self.frame_6 = QFrame(self.scrollAreaWidgetContents_2)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setMinimumSize(QSize(0, 260))
        self.frame_6.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_6.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_15 = QGridLayout(self.frame_6)
        self.gridLayout_15.setSpacing(4)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.gridLayout_15.setContentsMargins(4, 4, 4, 4)
        self.label_18 = QLabel(self.frame_6)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setMinimumSize(QSize(0, 40))
        self.label_18.setMaximumSize(QSize(16777215, 40))
        self.label_18.setFrameShape(QFrame.Shape.StyledPanel)
        self.label_18.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_15.addWidget(self.label_18, 0, 0, 1, 1)

        self.frame_8 = QFrame(self.frame_6)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_16 = QGridLayout(self.frame_8)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.gridLayout_16.setContentsMargins(4, 4, 4, 4)
        self.label_26 = QLabel(self.frame_8)
        self.label_26.setObjectName(u"label_26")

        self.gridLayout_16.addWidget(self.label_26, 0, 3, 1, 1)

        self.lineEdit_time_increment = QLineEdit(self.frame_8)
        self.lineEdit_time_increment.setObjectName(u"lineEdit_time_increment")
        self.lineEdit_time_increment.setEnabled(False)
        self.lineEdit_time_increment.setMinimumSize(QSize(200, 28))
        self.lineEdit_time_increment.setMaximumSize(QSize(16777215, 28))
        self.lineEdit_time_increment.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_16.addWidget(self.lineEdit_time_increment, 0, 2, 1, 1)

        self.label_27 = QLabel(self.frame_8)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setMinimumSize(QSize(140, 28))
        self.label_27.setMaximumSize(QSize(16777215, 28))
        self.label_27.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_16.addWidget(self.label_27, 6, 1, 1, 1)

        self.lineEdit_sampling_frequency = QLineEdit(self.frame_8)
        self.lineEdit_sampling_frequency.setObjectName(u"lineEdit_sampling_frequency")
        self.lineEdit_sampling_frequency.setEnabled(False)
        self.lineEdit_sampling_frequency.setMinimumSize(QSize(200, 28))
        self.lineEdit_sampling_frequency.setMaximumSize(QSize(16777215, 28))
        self.lineEdit_sampling_frequency.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_16.addWidget(self.lineEdit_sampling_frequency, 6, 2, 1, 1)

        self.pushButton_waveform_data = QPushButton(self.frame_8)
        self.pushButton_waveform_data.setObjectName(u"pushButton_waveform_data")
        self.pushButton_waveform_data.setMinimumSize(QSize(200, 28))
        self.pushButton_waveform_data.setMaximumSize(QSize(16777215, 28))
        self.pushButton_waveform_data.setFont(font2)
        self.pushButton_waveform_data.setAutoDefault(False)

        self.gridLayout_16.addWidget(self.pushButton_waveform_data, 14, 2, 1, 1)

        self.label_data_to_be_plotted = QLabel(self.frame_8)
        self.label_data_to_be_plotted.setObjectName(u"label_data_to_be_plotted")
        self.label_data_to_be_plotted.setMinimumSize(QSize(140, 28))
        self.label_data_to_be_plotted.setMaximumSize(QSize(16777215, 28))
        self.label_data_to_be_plotted.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_16.addWidget(self.label_data_to_be_plotted, 12, 1, 1, 1)

        self.label_28 = QLabel(self.frame_8)
        self.label_28.setObjectName(u"label_28")

        self.gridLayout_16.addWidget(self.label_28, 6, 3, 1, 1)

        self.label_34 = QLabel(self.frame_8)
        self.label_34.setObjectName(u"label_34")
        self.label_34.setMinimumSize(QSize(140, 28))
        self.label_34.setMaximumSize(QSize(16777215, 28))
        self.label_34.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_16.addWidget(self.label_34, 15, 1, 1, 1)

        self.lineEdit_number_of_revolutions = QLineEdit(self.frame_8)
        self.lineEdit_number_of_revolutions.setObjectName(u"lineEdit_number_of_revolutions")
        self.lineEdit_number_of_revolutions.setEnabled(False)
        self.lineEdit_number_of_revolutions.setMinimumSize(QSize(200, 28))
        self.lineEdit_number_of_revolutions.setMaximumSize(QSize(16777215, 28))
        self.lineEdit_number_of_revolutions.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_16.addWidget(self.lineEdit_number_of_revolutions, 4, 2, 1, 1)

        self.label_31 = QLabel(self.frame_8)
        self.label_31.setObjectName(u"label_31")
        self.label_31.setMinimumSize(QSize(140, 28))
        self.label_31.setMaximumSize(QSize(16777215, 28))
        self.label_31.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_16.addWidget(self.label_31, 4, 1, 1, 1)

        self.label_35 = QLabel(self.frame_8)
        self.label_35.setObjectName(u"label_35")
        self.label_35.setMinimumSize(QSize(140, 28))
        self.label_35.setMaximumSize(QSize(16777215, 28))
        self.label_35.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_16.addWidget(self.label_35, 14, 1, 1, 1)

        self.label_30 = QLabel(self.frame_8)
        self.label_30.setObjectName(u"label_30")

        self.gridLayout_16.addWidget(self.label_30, 5, 3, 1, 1)

        self.label_33 = QLabel(self.frame_8)
        self.label_33.setObjectName(u"label_33")

        self.gridLayout_16.addWidget(self.label_33, 3, 3, 1, 1)

        self.comboBox_window_type = QComboBox(self.frame_8)
        self.comboBox_window_type.addItem("")
        self.comboBox_window_type.addItem("")
        self.comboBox_window_type.addItem("")
        self.comboBox_window_type.addItem("")
        self.comboBox_window_type.setObjectName(u"comboBox_window_type")
        self.comboBox_window_type.setMinimumSize(QSize(0, 28))
        self.comboBox_window_type.setMaximumSize(QSize(16777215, 28))

        self.gridLayout_16.addWidget(self.comboBox_window_type, 10, 2, 1, 1)

        self.lineEdit_revolution_time = QLineEdit(self.frame_8)
        self.lineEdit_revolution_time.setObjectName(u"lineEdit_revolution_time")
        self.lineEdit_revolution_time.setEnabled(False)
        self.lineEdit_revolution_time.setMinimumSize(QSize(200, 28))
        self.lineEdit_revolution_time.setMaximumSize(QSize(16777215, 28))
        self.lineEdit_revolution_time.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_16.addWidget(self.lineEdit_revolution_time, 3, 2, 1, 1)

        self.lineEdit_sampling_time_block = QLineEdit(self.frame_8)
        self.lineEdit_sampling_time_block.setObjectName(u"lineEdit_sampling_time_block")
        self.lineEdit_sampling_time_block.setEnabled(False)
        self.lineEdit_sampling_time_block.setMinimumSize(QSize(200, 28))
        self.lineEdit_sampling_time_block.setMaximumSize(QSize(16777215, 28))
        self.lineEdit_sampling_time_block.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_16.addWidget(self.lineEdit_sampling_time_block, 5, 2, 1, 1)

        self.label_data_to_be_plotted_2 = QLabel(self.frame_8)
        self.label_data_to_be_plotted_2.setObjectName(u"label_data_to_be_plotted_2")
        self.label_data_to_be_plotted_2.setMinimumSize(QSize(140, 28))
        self.label_data_to_be_plotted_2.setMaximumSize(QSize(16777215, 28))
        self.label_data_to_be_plotted_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_16.addWidget(self.label_data_to_be_plotted_2, 10, 1, 1, 1)

        self.label_19 = QLabel(self.frame_8)
        self.label_19.setObjectName(u"label_19")

        self.gridLayout_16.addWidget(self.label_19, 8, 3, 1, 1)

        self.label_21 = QLabel(self.frame_8)
        self.label_21.setObjectName(u"label_21")

        self.gridLayout_16.addWidget(self.label_21, 9, 3, 1, 1)

        self.label_25 = QLabel(self.frame_8)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setMinimumSize(QSize(140, 28))
        self.label_25.setMaximumSize(QSize(16777215, 28))
        self.label_25.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_16.addWidget(self.label_25, 0, 1, 1, 1)

        self.comboBox_data_to_plot = QComboBox(self.frame_8)
        self.comboBox_data_to_plot.addItem("")
        self.comboBox_data_to_plot.addItem("")
        self.comboBox_data_to_plot.addItem("")
        self.comboBox_data_to_plot.setObjectName(u"comboBox_data_to_plot")
        self.comboBox_data_to_plot.setMinimumSize(QSize(0, 28))
        self.comboBox_data_to_plot.setMaximumSize(QSize(16777215, 28))

        self.gridLayout_16.addWidget(self.comboBox_data_to_plot, 12, 2, 1, 1)

        self.pushButton_spectrum_data = QPushButton(self.frame_8)
        self.pushButton_spectrum_data.setObjectName(u"pushButton_spectrum_data")
        self.pushButton_spectrum_data.setMinimumSize(QSize(200, 28))
        self.pushButton_spectrum_data.setMaximumSize(QSize(16777215, 28))
        self.pushButton_spectrum_data.setFont(font2)
        self.pushButton_spectrum_data.setAutoDefault(False)

        self.gridLayout_16.addWidget(self.pushButton_spectrum_data, 15, 2, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_16.addItem(self.horizontalSpacer_4, 0, 4, 1, 1)

        self.spinBox_maximum_frequency = QSpinBox(self.frame_8)
        self.spinBox_maximum_frequency.setObjectName(u"spinBox_maximum_frequency")
        self.spinBox_maximum_frequency.setMinimumSize(QSize(0, 28))
        self.spinBox_maximum_frequency.setMaximumSize(QSize(16777215, 28))
        self.spinBox_maximum_frequency.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spinBox_maximum_frequency.setMinimum(1000)
        self.spinBox_maximum_frequency.setMaximum(20000)
        self.spinBox_maximum_frequency.setSingleStep(100)
        self.spinBox_maximum_frequency.setValue(2000)

        self.gridLayout_16.addWidget(self.spinBox_maximum_frequency, 9, 2, 1, 1)

        self.label_23 = QLabel(self.frame_8)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setMinimumSize(QSize(140, 28))
        self.label_23.setMaximumSize(QSize(16777215, 28))
        self.label_23.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_16.addWidget(self.label_23, 9, 1, 1, 1)

        self.lineEdit_frequency_resolution_plot = QLineEdit(self.frame_8)
        self.lineEdit_frequency_resolution_plot.setObjectName(u"lineEdit_frequency_resolution_plot")
        self.lineEdit_frequency_resolution_plot.setEnabled(False)
        self.lineEdit_frequency_resolution_plot.setMinimumSize(QSize(200, 28))
        self.lineEdit_frequency_resolution_plot.setMaximumSize(QSize(16777215, 28))
        self.lineEdit_frequency_resolution_plot.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_16.addWidget(self.lineEdit_frequency_resolution_plot, 8, 2, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_16.addItem(self.horizontalSpacer_3, 0, 0, 1, 1)

        self.label_24 = QLabel(self.frame_8)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setMinimumSize(QSize(140, 28))
        self.label_24.setMaximumSize(QSize(16777215, 28))
        self.label_24.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_16.addWidget(self.label_24, 8, 1, 1, 1)

        self.comboBox_correction_type = QComboBox(self.frame_8)
        self.comboBox_correction_type.addItem("")
        self.comboBox_correction_type.addItem("")
        self.comboBox_correction_type.setObjectName(u"comboBox_correction_type")
        self.comboBox_correction_type.setMinimumSize(QSize(0, 28))
        self.comboBox_correction_type.setMaximumSize(QSize(16777215, 28))

        self.gridLayout_16.addWidget(self.comboBox_correction_type, 11, 2, 1, 1)

        self.label_29 = QLabel(self.frame_8)
        self.label_29.setObjectName(u"label_29")
        self.label_29.setMinimumSize(QSize(140, 28))
        self.label_29.setMaximumSize(QSize(16777215, 28))
        self.label_29.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_16.addWidget(self.label_29, 3, 1, 1, 1)

        self.label_data_to_be_plotted_3 = QLabel(self.frame_8)
        self.label_data_to_be_plotted_3.setObjectName(u"label_data_to_be_plotted_3")
        self.label_data_to_be_plotted_3.setMinimumSize(QSize(140, 28))
        self.label_data_to_be_plotted_3.setMaximumSize(QSize(16777215, 28))
        self.label_data_to_be_plotted_3.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_16.addWidget(self.label_data_to_be_plotted_3, 11, 1, 1, 1)

        self.label_32 = QLabel(self.frame_8)
        self.label_32.setObjectName(u"label_32")
        self.label_32.setMinimumSize(QSize(140, 28))
        self.label_32.setMaximumSize(QSize(16777215, 28))
        self.label_32.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_16.addWidget(self.label_32, 5, 1, 1, 1)

        self.pushButton_reproduce_audio = QPushButton(self.frame_8)
        self.pushButton_reproduce_audio.setObjectName(u"pushButton_reproduce_audio")
        self.pushButton_reproduce_audio.setMinimumSize(QSize(0, 28))
        self.pushButton_reproduce_audio.setMaximumSize(QSize(16777215, 28))
        self.pushButton_reproduce_audio.setFont(font2)
        icon1 = Icon(u":/icons/model_configuration/play_audio.png")
        self.pushButton_reproduce_audio.setIcon(icon1)
        self.pushButton_reproduce_audio.setIconSize(QSize(22, 22))
        self.pushButton_reproduce_audio.setAutoDefault(False)

        self.gridLayout_16.addWidget(self.pushButton_reproduce_audio, 12, 3, 1, 1)


        self.gridLayout_15.addWidget(self.frame_8, 1, 0, 1, 1)


        self.gridLayout_17.addWidget(self.frame_6, 0, 0, 1, 1)

        self.scrollArea_plots.setWidget(self.scrollAreaWidgetContents_2)

        self.gridLayout_13.addWidget(self.scrollArea_plots, 0, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_signals, "")
        self.tab_list = QWidget()
        self.tab_list.setObjectName(u"tab_list")
        self.gridLayout_9 = QGridLayout(self.tab_list)
        self.gridLayout_9.setSpacing(2)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(6, 8, 6, 2)
        self.frame_7 = QFrame(self.tab_list)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_7.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_10 = QGridLayout(self.frame_7)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(4, 4, 4, 4)
        self.treeWidget_surface_velocity = QTreeWidget(self.frame_7)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(2, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter);
        self.treeWidget_surface_velocity.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_surface_velocity.setObjectName(u"treeWidget_surface_velocity")
        self.treeWidget_surface_velocity.setMinimumSize(QSize(320, 100))
        self.treeWidget_surface_velocity.setMaximumSize(QSize(1000, 600))
        font5 = QFont()
        font5.setFamilies([u"MS Shell Dlg 2"])
        font5.setPointSize(9)
        font5.setBold(False)
        font5.setItalic(False)
        self.treeWidget_surface_velocity.setFont(font5)
        self.treeWidget_surface_velocity.setIndentation(1)
        self.treeWidget_surface_velocity.setHeaderHidden(False)
        self.treeWidget_surface_velocity.header().setHighlightSections(False)
        self.treeWidget_surface_velocity.header().setProperty(u"showSortIndicator", False)
        self.treeWidget_surface_velocity.header().setStretchLastSection(True)

        self.gridLayout_10.addWidget(self.treeWidget_surface_velocity, 0, 0, 1, 1)

        self.frame_3 = QFrame(self.frame_7)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(320, 40))
        self.frame_3.setMaximumSize(QSize(1000, 40))
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
        self.pushButton_reset.setFont(font4)
        self.pushButton_reset.setStyleSheet(u"")
        self.pushButton_reset.setAutoDefault(False)

        self.gridLayout_8.addWidget(self.pushButton_reset, 0, 0, 1, 1)

        self.pushButton_remove = QPushButton(self.frame_3)
        self.pushButton_remove.setObjectName(u"pushButton_remove")
        self.pushButton_remove.setMinimumSize(QSize(100, 28))
        self.pushButton_remove.setMaximumSize(QSize(100, 28))
        self.pushButton_remove.setFont(font4)
        self.pushButton_remove.setStyleSheet(u"")
        self.pushButton_remove.setAutoDefault(False)

        self.gridLayout_8.addWidget(self.pushButton_remove, 0, 1, 1, 1)


        self.gridLayout_10.addWidget(self.frame_3, 1, 0, 1, 1)


        self.gridLayout_9.addWidget(self.frame_7, 0, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_list, "")

        self.gridLayout_4.addWidget(self.tabWidget_main, 1, 0, 1, 1)

        self.frame_4 = QFrame(self.frame_2)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(360, 48))
        self.frame_4.setMaximumSize(QSize(16777215, 48))
        self.frame_4.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_4)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setHorizontalSpacing(6)
        self.gridLayout_5.setVerticalSpacing(2)
        self.gridLayout_5.setContentsMargins(2, 2, 2, 2)
        self.lineEdit_selection_id = QLineEdit(self.frame_4)
        self.lineEdit_selection_id.setObjectName(u"lineEdit_selection_id")
        self.lineEdit_selection_id.setMinimumSize(QSize(140, 28))
        self.lineEdit_selection_id.setMaximumSize(QSize(140, 28))
        self.lineEdit_selection_id.setFont(font4)
        self.lineEdit_selection_id.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.lineEdit_selection_id.setStyleSheet(u"")
        self.lineEdit_selection_id.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.lineEdit_selection_id, 0, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.label_2 = QLabel(self.frame_4)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(100, 28))
        self.label_2.setMaximumSize(QSize(100, 28))
        self.label_2.setFont(font4)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_2, 0, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_2, 0, 3, 1, 1)


        self.gridLayout_4.addWidget(self.frame_4, 0, 0, 1, 1)


        self.gridLayout_7.addWidget(self.frame_2, 1, 0, 1, 1)

        self.frame_buttons = QFrame(Dialog)
        self.frame_buttons.setObjectName(u"frame_buttons")
        self.frame_buttons.setMinimumSize(QSize(0, 48))
        self.frame_buttons.setMaximumSize(QSize(16777215, 48))
        self.frame_buttons.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_buttons.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_12 = QGridLayout(self.frame_buttons)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setVerticalSpacing(0)
        self.gridLayout_12.setContentsMargins(6, 0, 6, 0)
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

        self.gridLayout_12.addWidget(self.pushButton_apply_and_close, 0, 3, 1, 1)

        self.pushButton_apply = QPushButton(self.frame_buttons)
        self.pushButton_apply.setObjectName(u"pushButton_apply")
        self.pushButton_apply.setMinimumSize(QSize(72, 30))
        self.pushButton_apply.setMaximumSize(QSize(72, 30))
        self.pushButton_apply.setFont(font6)
        self.pushButton_apply.setStyleSheet(u"")
        self.pushButton_apply.setAutoDefault(False)
        self.pushButton_apply.setFlat(False)

        self.gridLayout_12.addWidget(self.pushButton_apply, 0, 2, 1, 1)

        self.pushButton_cancel = QPushButton(self.frame_buttons)
        self.pushButton_cancel.setObjectName(u"pushButton_cancel")
        self.pushButton_cancel.setMinimumSize(QSize(72, 30))
        self.pushButton_cancel.setMaximumSize(QSize(72, 30))
        self.pushButton_cancel.setFont(font6)
        self.pushButton_cancel.setStyleSheet(u"")
        self.pushButton_cancel.setAutoDefault(False)
        self.pushButton_cancel.setFlat(False)

        self.gridLayout_12.addWidget(self.pushButton_cancel, 0, 0, 1, 1)

        self.horizontalSpacer_17 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_12.addItem(self.horizontalSpacer_17, 0, 1, 1, 1)


        self.gridLayout_7.addWidget(self.frame_buttons, 2, 0, 1, 1)


        self.retranslateUi(Dialog)

        self.tabWidget_main.setCurrentIndex(0)
        self.comboBox_single_revolution.setCurrentIndex(0)
        self.pushButton_apply_and_close.setDefault(False)
        self.pushButton_apply.setDefault(False)
        self.pushButton_cancel.setDefault(False)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Set surface velocity acoustic excitation", None))
#if QT_CONFIG(whatsthis)
        Dialog.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.label.setText(QCoreApplication.translate("Dialog", u"Compressor excitation (time domain)", None))
        self.comboBox_data_source.setItemText(0, QCoreApplication.translate("Dialog", u"SCORG", None))
        self.comboBox_data_source.setItemText(1, QCoreApplication.translate("Dialog", u"CFD", None))
        self.comboBox_data_source.setItemText(2, QCoreApplication.translate("Dialog", u"Other", None))

        self.label_7.setText(QCoreApplication.translate("Dialog", u"[deg]", None))
        self.label_normal_velocity_axis.setText(QCoreApplication.translate("Dialog", u"Normal velocity axis:", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"Angular resolution:", None))
        self.comboBox_normal_velocity_axis.setItemText(0, QCoreApplication.translate("Dialog", u"x-axis (+)", None))
        self.comboBox_normal_velocity_axis.setItemText(1, QCoreApplication.translate("Dialog", u"y-axis (+)", None))
        self.comboBox_normal_velocity_axis.setItemText(2, QCoreApplication.translate("Dialog", u"z-axis (+)", None))
        self.comboBox_normal_velocity_axis.setItemText(3, QCoreApplication.translate("Dialog", u"x-axis (-)", None))
        self.comboBox_normal_velocity_axis.setItemText(4, QCoreApplication.translate("Dialog", u"y-axis (-)", None))
        self.comboBox_normal_velocity_axis.setItemText(5, QCoreApplication.translate("Dialog", u"z-axis (-)", None))

        self.label_9.setText(QCoreApplication.translate("Dialog", u"Maximum frequency:", None))
        self.lineEdit_maximum_frequency.setText(QCoreApplication.translate("Dialog", u"1500", None))
        self.lineEdit_frequency_resolution_required.setText(QCoreApplication.translate("Dialog", u"10", None))
        self.label_10.setText(QCoreApplication.translate("Dialog", u"[Hz]", None))
        self.label_11.setText(QCoreApplication.translate("Dialog", u"[Hz]", None))
        self.comboBox_single_revolution.setItemText(0, QCoreApplication.translate("Dialog", u"yes", None))
        self.comboBox_single_revolution.setItemText(1, QCoreApplication.translate("Dialog", u"no", None))

        self.label_14.setText(QCoreApplication.translate("Dialog", u"Single revolution?:", None))
        self.comboBox_excitation_mapping.setItemText(0, QCoreApplication.translate("Dialog", u"surface averaged", None))
        self.comboBox_excitation_mapping.setItemText(1, QCoreApplication.translate("Dialog", u"nodal mapping", None))

        self.label_5.setText(QCoreApplication.translate("Dialog", u"Data source:", None))
        self.label_15.setText(QCoreApplication.translate("Dialog", u"Connection type:", None))
        self.label_excitation_mapping.setText(QCoreApplication.translate("Dialog", u"Excitation mapping:", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"Freq. step (req.):", None))
        self.comboBox_connection_type.setItemText(0, QCoreApplication.translate("Dialog", u"discharge", None))
        self.comboBox_connection_type.setItemText(1, QCoreApplication.translate("Dialog", u"suction", None))

        self.label_16.setText(QCoreApplication.translate("Dialog", u"Compressor type:", None))
        self.lineEdit_angular_resolution.setText("")
        self.comboBox_compressor_type.setItemText(0, QCoreApplication.translate("Dialog", u"screw", None))
        self.comboBox_compressor_type.setItemText(1, QCoreApplication.translate("Dialog", u"centrifugal", None))
        self.comboBox_compressor_type.setItemText(2, QCoreApplication.translate("Dialog", u"reciprocating", None))

        self.label_12.setText(QCoreApplication.translate("Dialog", u"Freq. step (final):", None))
        self.lineEdit_frequency_resolution.setText(QCoreApplication.translate("Dialog", u"not calculated", None))
        self.label_13.setText(QCoreApplication.translate("Dialog", u"[Hz]", None))
        self.comboBox_excitation_type.setItemText(0, QCoreApplication.translate("Dialog", u"mass flow rate -> kg/s", None))
        self.comboBox_excitation_type.setItemText(1, QCoreApplication.translate("Dialog", u"surface velocity -> m/s", None))
        self.comboBox_excitation_type.setItemText(2, QCoreApplication.translate("Dialog", u"volumetric flow rate -> m\u00b3/s", None))

        self.label_17.setText(QCoreApplication.translate("Dialog", u"Excitation type:", None))
        self.pushButton_load_table.setText("")
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Choose the file to import compressor excitation data", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_setup), QCoreApplication.translate("Dialog", u"Setup", None))
        self.label_18.setText(QCoreApplication.translate("Dialog", u"Signals' processing parameters", None))
        self.label_26.setText(QCoreApplication.translate("Dialog", u"[s]", None))
        self.lineEdit_time_increment.setText(QCoreApplication.translate("Dialog", u"--", None))
        self.label_27.setText(QCoreApplication.translate("Dialog", u"Sampling frequency:", None))
        self.lineEdit_sampling_frequency.setText(QCoreApplication.translate("Dialog", u"--", None))
        self.pushButton_waveform_data.setText(QCoreApplication.translate("Dialog", u"Plot waveform data", None))
        self.label_data_to_be_plotted.setText(QCoreApplication.translate("Dialog", u"Data to plot:", None))
        self.label_28.setText(QCoreApplication.translate("Dialog", u"[Hz]", None))
        self.label_34.setText(QCoreApplication.translate("Dialog", u"Frequency domain plot:", None))
        self.lineEdit_number_of_revolutions.setText(QCoreApplication.translate("Dialog", u"--", None))
        self.label_31.setText(QCoreApplication.translate("Dialog", u"Number of revolutions:", None))
        self.label_35.setText(QCoreApplication.translate("Dialog", u"Time domain plot:", None))
        self.label_30.setText(QCoreApplication.translate("Dialog", u"[s]", None))
        self.label_33.setText(QCoreApplication.translate("Dialog", u"[s]", None))
        self.comboBox_window_type.setItemText(0, QCoreApplication.translate("Dialog", u"rectangular", None))
        self.comboBox_window_type.setItemText(1, QCoreApplication.translate("Dialog", u"hann", None))
        self.comboBox_window_type.setItemText(2, QCoreApplication.translate("Dialog", u"flattop", None))
        self.comboBox_window_type.setItemText(3, QCoreApplication.translate("Dialog", u"hamming", None))

        self.lineEdit_revolution_time.setText(QCoreApplication.translate("Dialog", u"--", None))
        self.lineEdit_sampling_time_block.setText(QCoreApplication.translate("Dialog", u"--", None))
        self.label_data_to_be_plotted_2.setText(QCoreApplication.translate("Dialog", u"Window type:", None))
        self.label_19.setText(QCoreApplication.translate("Dialog", u"[Hz]", None))
        self.label_21.setText(QCoreApplication.translate("Dialog", u"[Hz]", None))
        self.label_25.setText(QCoreApplication.translate("Dialog", u"Time increment:", None))
        self.comboBox_data_to_plot.setItemText(0, QCoreApplication.translate("Dialog", u"mass flow rate -> kg/s", None))
        self.comboBox_data_to_plot.setItemText(1, QCoreApplication.translate("Dialog", u"surface velocity -> m/s", None))
        self.comboBox_data_to_plot.setItemText(2, QCoreApplication.translate("Dialog", u"volumetric flow rate -> m\u00b3/s", None))

        self.pushButton_spectrum_data.setText(QCoreApplication.translate("Dialog", u"Plot spectrum data", None))
        self.label_23.setText(QCoreApplication.translate("Dialog", u"Freq. max:", None))
        self.lineEdit_frequency_resolution_plot.setText(QCoreApplication.translate("Dialog", u"--", None))
        self.label_24.setText(QCoreApplication.translate("Dialog", u"Freq. step:", None))
        self.comboBox_correction_type.setItemText(0, QCoreApplication.translate("Dialog", u"amplitude", None))
        self.comboBox_correction_type.setItemText(1, QCoreApplication.translate("Dialog", u"energy", None))

        self.label_29.setText(QCoreApplication.translate("Dialog", u"Revolution time:", None))
        self.label_data_to_be_plotted_3.setText(QCoreApplication.translate("Dialog", u"Correction type:", None))
        self.label_32.setText(QCoreApplication.translate("Dialog", u"Sampling time block:", None))
        self.pushButton_reproduce_audio.setText("")
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_signals), QCoreApplication.translate("Dialog", u"Signals", None))
        ___qtreewidgetitem = self.treeWidget_surface_velocity.headerItem()
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("Dialog", u"Angular resolution [deg]", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"Source", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Surface ID", None));
#if QT_CONFIG(tooltip)
        self.treeWidget_surface_velocity.setToolTip(QCoreApplication.translate("Dialog", u"Select a face to remove the previously attributed boundary condition.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_reset.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.pushButton_remove.setText(QCoreApplication.translate("Dialog", u"Remove", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_list), QCoreApplication.translate("Dialog", u"List", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Selection ID:", None))
        self.pushButton_apply_and_close.setText(QCoreApplication.translate("Dialog", u"Ok", None))
        self.pushButton_apply.setText(QCoreApplication.translate("Dialog", u"Apply", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
    # retranslateUi



class CompressorExcitationWaveformInputs_UI(QDialog, Ui_Dialog):
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
                                - tab_setup: QWidget
                                    - (Layout): QGridLayout
                                            - scrollArea_setup: QScrollArea
                                                - scrollAreaWidgetContents: QWidget
                                                    - (Layout): QGridLayout
                                                            - frame_5: QFrame
                                                                - (Layout): QGridLayout
                                                                        - comboBox_data_source: QComboBox
                                                                        - label_7: QLabel
                                                                        - label_normal_velocity_axis: QLabel
                                                                        - label_6: QLabel
                                                                        - comboBox_normal_velocity_axis: QComboBox
                                                                        - label_9: QLabel
                                                                        - lineEdit_maximum_frequency: QLineEdit
                                                                        - lineEdit_frequency_resolution_required: QLineEdit
                                                                        - label_10: QLabel
                                                                        - label_11: QLabel
                                                                        - comboBox_single_revolution: QComboBox
                                                                        - label_14: QLabel
                                                                        - comboBox_excitation_mapping: QComboBox
                                                                        - label_5: QLabel
                                                                        - label_15: QLabel
                                                                        - label_excitation_mapping: QLabel
                                                                        - label_8: QLabel
                                                                        - comboBox_connection_type: QComboBox
                                                                        - label_16: QLabel
                                                                        - lineEdit_angular_resolution: QLineEdit
                                                                        - comboBox_compressor_type: QComboBox
                                                                        - label_12: QLabel
                                                                        - lineEdit_frequency_resolution: QLineEdit
                                                                        - label_13: QLabel
                                                                        - comboBox_excitation_type: QComboBox
                                                                        - label_17: QLabel
                                                            - frame_9: QFrame
                                                                - (Layout): QGridLayout
                                                                        - lineEdit_table_path: QLineEdit
                                                                        - pushButton_load_table: QPushButton
                                                                        - label_4: QLabel
                                - tab_signals: QWidget
                                    - (Layout): QGridLayout
                                            - scrollArea_plots: QScrollArea
                                                - scrollAreaWidgetContents_2: QWidget
                                                    - (Layout): QGridLayout
                                                            - frame_6: QFrame
                                                                - (Layout): QGridLayout
                                                                        - label_18: QLabel
                                                                        - frame_8: QFrame
                                                                            - (Layout): QGridLayout
                                                                                    - label_26: QLabel
                                                                                    - lineEdit_time_increment: QLineEdit
                                                                                    - label_27: QLabel
                                                                                    - lineEdit_sampling_frequency: QLineEdit
                                                                                    - pushButton_waveform_data: QPushButton
                                                                                    - label_data_to_be_plotted: QLabel
                                                                                    - label_28: QLabel
                                                                                    - label_34: QLabel
                                                                                    - lineEdit_number_of_revolutions: QLineEdit
                                                                                    - label_31: QLabel
                                                                                    - label_35: QLabel
                                                                                    - label_30: QLabel
                                                                                    - label_33: QLabel
                                                                                    - comboBox_window_type: QComboBox
                                                                                    - lineEdit_revolution_time: QLineEdit
                                                                                    - lineEdit_sampling_time_block: QLineEdit
                                                                                    - label_data_to_be_plotted_2: QLabel
                                                                                    - label_19: QLabel
                                                                                    - label_21: QLabel
                                                                                    - label_25: QLabel
                                                                                    - comboBox_data_to_plot: QComboBox
                                                                                    - pushButton_spectrum_data: QPushButton
                                                                                    - spinBox_maximum_frequency: QSpinBox
                                                                                    - label_23: QLabel
                                                                                    - lineEdit_frequency_resolution_plot: QLineEdit
                                                                                    - label_24: QLabel
                                                                                    - comboBox_correction_type: QComboBox
                                                                                    - label_29: QLabel
                                                                                    - label_data_to_be_plotted_3: QLabel
                                                                                    - label_32: QLabel
                                                                                    - pushButton_reproduce_audio: QPushButton
                                - tab_list: QWidget
                                    - (Layout): QGridLayout
                                            - frame_7: QFrame
                                                - (Layout): QGridLayout
                                                        - treeWidget_surface_velocity: QTreeWidget
                                                        - frame_3: QFrame
                                                            - (Layout): QGridLayout
                                                                    - pushButton_reset: QPushButton
                                                                    - pushButton_remove: QPushButton
                            - frame_4: QFrame
                                - (Layout): QGridLayout
                                        - lineEdit_selection_id: QLineEdit
                                        - label_2: QLabel
                - frame_buttons: QFrame
                    - (Layout): QGridLayout
                            - pushButton_apply_and_close: QPushButton
                            - pushButton_apply: QPushButton
                            - pushButton_cancel: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
