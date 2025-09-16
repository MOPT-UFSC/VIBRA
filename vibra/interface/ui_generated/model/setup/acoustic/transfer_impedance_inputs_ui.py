# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'transfer_impedance_inputs.ui'
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
        Dialog.resize(420, 477)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(420, 380))
        Dialog.setMaximumSize(QSize(420, 600))
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
        self.frame_2.setMaximumSize(QSize(420, 480))
        self.frame_2.setFrameShape(QFrame.Box)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.tabWidget_main = QTabWidget(self.frame_2)
        self.tabWidget_main.setObjectName(u"tabWidget_main")
        self.tabWidget_main.setMinimumSize(QSize(360, 0))
        self.tabWidget_main.setMaximumSize(QSize(16777215, 16777215))
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(False)
        self.tabWidget_main.setFont(font1)
        self.tab_constant_data = QWidget()
        self.tab_constant_data.setObjectName(u"tab_constant_data")
        self.gridLayout_12 = QGridLayout(self.tab_constant_data)
        self.gridLayout_12.setSpacing(2)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setContentsMargins(2, 6, 2, 6)
        self.frame_8 = QFrame(self.tab_constant_data)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setMinimumSize(QSize(340, 80))
        self.frame_8.setMaximumSize(QSize(400, 1000))
        self.frame_8.setFont(font)
        self.frame_8.setFrameShape(QFrame.NoFrame)
        self.frame_8.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame_8)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(6)
        self.gridLayout.setVerticalSpacing(2)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 2, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_2, 3, 2, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 0, 2, 1, 1)

        self.label_21 = QLabel(self.frame_8)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setMinimumSize(QSize(60, 28))
        self.label_21.setMaximumSize(QSize(60, 28))
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        self.label_21.setFont(font2)
        self.label_21.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_21, 2, 4, 1, 1)

        self.label_4 = QLabel(self.frame_8)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(80, 26))
        self.label_4.setMaximumSize(QSize(80, 26))
        self.label_4.setFont(font2)
        self.label_4.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_4, 1, 2, 1, 1)

        self.label_18 = QLabel(self.frame_8)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setMinimumSize(QSize(120, 28))
        self.label_18.setMaximumSize(QSize(120, 28))
        self.label_18.setFont(font2)
        self.label_18.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_18, 2, 1, 1, 1)

        self.lineEdit_real_value = QLineEdit(self.frame_8)
        self.lineEdit_real_value.setObjectName(u"lineEdit_real_value")
        self.lineEdit_real_value.setMinimumSize(QSize(80, 28))
        self.lineEdit_real_value.setMaximumSize(QSize(80, 28))
        self.lineEdit_real_value.setFont(font2)
        self.lineEdit_real_value.setStyleSheet(u"")
        self.lineEdit_real_value.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_real_value, 2, 2, 1, 1)

        self.label_20 = QLabel(self.frame_8)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setMinimumSize(QSize(80, 26))
        self.label_20.setMaximumSize(QSize(80, 26))
        self.label_20.setFont(font2)
        self.label_20.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_20, 1, 3, 1, 1)

        self.lineEdit_imag_value = QLineEdit(self.frame_8)
        self.lineEdit_imag_value.setObjectName(u"lineEdit_imag_value")
        self.lineEdit_imag_value.setMinimumSize(QSize(80, 28))
        self.lineEdit_imag_value.setMaximumSize(QSize(80, 28))
        self.lineEdit_imag_value.setFont(font2)
        self.lineEdit_imag_value.setStyleSheet(u"")
        self.lineEdit_imag_value.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_imag_value, 2, 3, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 2, 5, 1, 1)


        self.gridLayout_12.addWidget(self.frame_8, 0, 0, 1, 1)

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
        self.frame_9.setMaximumSize(QSize(400, 200))
        self.frame_9.setFrameShape(QFrame.NoFrame)
        self.frame_9.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_9)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setHorizontalSpacing(6)
        self.gridLayout_2.setVerticalSpacing(2)
        self.gridLayout_2.setContentsMargins(0, 4, 0, 0)
        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer_3, 0, 1, 1, 1)

        self.label_2 = QLabel(self.frame_9)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(0, 28))
        self.label_2.setMaximumSize(QSize(16777215, 28))
        self.label_2.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label_2, 1, 1, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_8, 2, 0, 1, 1)

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

        self.gridLayout_2.addWidget(self.pushButton_load_table, 2, 2, 1, 1)

        self.lineEdit_table_path = QLineEdit(self.frame_9)
        self.lineEdit_table_path.setObjectName(u"lineEdit_table_path")
        self.lineEdit_table_path.setEnabled(True)
        self.lineEdit_table_path.setMinimumSize(QSize(280, 26))
        self.lineEdit_table_path.setMaximumSize(QSize(280, 26))
        font3 = QFont()
        font3.setPointSize(9)
        font3.setBold(False)
        self.lineEdit_table_path.setFont(font3)
        self.lineEdit_table_path.setStyleSheet(u"")
        self.lineEdit_table_path.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_table_path, 2, 1, 1, 1)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_9, 2, 4, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer_4, 4, 1, 1, 1)

        self.pushButton_change_frequency_setup = QPushButton(self.frame_9)
        self.pushButton_change_frequency_setup.setObjectName(u"pushButton_change_frequency_setup")
        self.pushButton_change_frequency_setup.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.pushButton_change_frequency_setup.sizePolicy().hasHeightForWidth())
        self.pushButton_change_frequency_setup.setSizePolicy(sizePolicy1)
        self.pushButton_change_frequency_setup.setMinimumSize(QSize(40, 28))
        self.pushButton_change_frequency_setup.setMaximumSize(QSize(40, 28))
        self.pushButton_change_frequency_setup.setFont(font2)
        self.pushButton_change_frequency_setup.setStyleSheet(u"")
        icon1 = QIcon()
        icon1.addFile(u":/icons/recent.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_change_frequency_setup.setIcon(icon1)
        self.pushButton_change_frequency_setup.setIconSize(QSize(20, 20))

        self.gridLayout_2.addWidget(self.pushButton_change_frequency_setup, 3, 2, 1, 1)


        self.gridLayout_3.addWidget(self.frame_9, 0, 0, 1, 1)

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
        self.frame_3.setMaximumSize(QSize(320, 40))
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

        self.gridLayout_8.addWidget(self.pushButton_reset, 0, 0, 1, 1)

        self.pushButton_remove = QPushButton(self.frame_3)
        self.pushButton_remove.setObjectName(u"pushButton_remove")
        self.pushButton_remove.setMinimumSize(QSize(100, 28))
        self.pushButton_remove.setMaximumSize(QSize(100, 28))
        self.pushButton_remove.setFont(font2)
        self.pushButton_remove.setStyleSheet(u"")

        self.gridLayout_8.addWidget(self.pushButton_remove, 0, 1, 1, 1)


        self.gridLayout_9.addWidget(self.frame_3, 1, 0, 1, 1)

        self.treeWidget_transfer_impedance = QTreeWidget(self.tab_list)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter);
        self.treeWidget_transfer_impedance.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_transfer_impedance.setObjectName(u"treeWidget_transfer_impedance")
        self.treeWidget_transfer_impedance.setMinimumSize(QSize(320, 70))
        self.treeWidget_transfer_impedance.setMaximumSize(QSize(320, 200))
        font4 = QFont()
        font4.setFamilies([u"MS Shell Dlg 2"])
        font4.setPointSize(9)
        font4.setBold(False)
        font4.setItalic(False)
        self.treeWidget_transfer_impedance.setFont(font4)
        self.treeWidget_transfer_impedance.setIndentation(1)
        self.treeWidget_transfer_impedance.setHeaderHidden(False)
        self.treeWidget_transfer_impedance.header().setHighlightSections(False)
        self.treeWidget_transfer_impedance.header().setProperty(u"showSortIndicator", False)
        self.treeWidget_transfer_impedance.header().setStretchLastSection(True)

        self.gridLayout_9.addWidget(self.treeWidget_transfer_impedance, 0, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_list, "")

        self.gridLayout_4.addWidget(self.tabWidget_main, 1, 0, 1, 1)

        self.frame_6 = QFrame(self.frame_2)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setMinimumSize(QSize(400, 110))
        self.frame_6.setMaximumSize(QSize(16777215, 110))
        self.frame_6.setFrameShape(QFrame.NoFrame)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.frame_6.setLineWidth(1)
        self.gridLayout_10 = QGridLayout(self.frame_6)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(6, 6, 6, 6)
        self.label_16 = QLabel(self.frame_6)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setMinimumSize(QSize(100, 28))
        self.label_16.setMaximumSize(QSize(120, 28))
        font5 = QFont()
        font5.setFamilies([u"MS Shell Dlg 2"])
        font5.setPointSize(10)
        font5.setBold(False)
        self.label_16.setFont(font5)
        self.label_16.setTextFormat(Qt.AutoText)
        self.label_16.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_16, 2, 1, 1, 1)

        self.comboBox_selection_type = QComboBox(self.frame_6)
        self.comboBox_selection_type.addItem("")
        self.comboBox_selection_type.addItem("")
        self.comboBox_selection_type.setObjectName(u"comboBox_selection_type")
        self.comboBox_selection_type.setMinimumSize(QSize(160, 28))
        self.comboBox_selection_type.setMaximumSize(QSize(160, 28))
        self.comboBox_selection_type.setFont(font1)

        self.gridLayout_10.addWidget(self.comboBox_selection_type, 2, 2, 1, 2)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_10.addItem(self.horizontalSpacer_6, 0, 4, 1, 1)

        self.lineEdit_selection_id_A = QLineEdit(self.frame_6)
        self.lineEdit_selection_id_A.setObjectName(u"lineEdit_selection_id_A")
        self.lineEdit_selection_id_A.setEnabled(True)
        self.lineEdit_selection_id_A.setMinimumSize(QSize(160, 28))
        self.lineEdit_selection_id_A.setMaximumSize(QSize(160, 28))
        self.lineEdit_selection_id_A.setFont(font1)
        self.lineEdit_selection_id_A.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_selection_id_A.setStyleSheet(u"")
        self.lineEdit_selection_id_A.setAlignment(Qt.AlignCenter)

        self.gridLayout_10.addWidget(self.lineEdit_selection_id_A, 0, 2, 1, 2)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_10.addItem(self.horizontalSpacer_7, 0, 0, 1, 1)

        self.label_selection_A = QLabel(self.frame_6)
        self.label_selection_A.setObjectName(u"label_selection_A")
        self.label_selection_A.setMinimumSize(QSize(100, 28))
        self.label_selection_A.setMaximumSize(QSize(120, 28))
        self.label_selection_A.setFont(font5)
        self.label_selection_A.setTextFormat(Qt.AutoText)
        self.label_selection_A.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_selection_A, 0, 1, 1, 1)

        self.label_selection_B = QLabel(self.frame_6)
        self.label_selection_B.setObjectName(u"label_selection_B")
        self.label_selection_B.setMinimumSize(QSize(100, 28))
        self.label_selection_B.setMaximumSize(QSize(120, 28))
        self.label_selection_B.setFont(font5)
        self.label_selection_B.setTextFormat(Qt.AutoText)
        self.label_selection_B.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_selection_B, 1, 1, 1, 1)

        self.lineEdit_selection_id_B = QLineEdit(self.frame_6)
        self.lineEdit_selection_id_B.setObjectName(u"lineEdit_selection_id_B")
        self.lineEdit_selection_id_B.setEnabled(True)
        self.lineEdit_selection_id_B.setMinimumSize(QSize(160, 28))
        self.lineEdit_selection_id_B.setMaximumSize(QSize(160, 28))
        self.lineEdit_selection_id_B.setFont(font1)
        self.lineEdit_selection_id_B.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_selection_id_B.setStyleSheet(u"")
        self.lineEdit_selection_id_B.setAlignment(Qt.AlignCenter)

        self.gridLayout_10.addWidget(self.lineEdit_selection_id_B, 1, 2, 1, 1)


        self.gridLayout_4.addWidget(self.frame_6, 0, 0, 1, 1)


        self.gridLayout_7.addWidget(self.frame_2, 1, 0, 1, 1)

        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(380, 48))
        self.frame.setMaximumSize(QSize(420, 48))
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
        self.pushButton_attribute.setFont(font2)
        self.pushButton_attribute.setStyleSheet(u"")

        self.gridLayout_14.addWidget(self.pushButton_attribute, 0, 1, 1, 1)

        self.pushButton_exit = QPushButton(self.frame_11)
        self.pushButton_exit.setObjectName(u"pushButton_exit")
        self.pushButton_exit.setMinimumSize(QSize(100, 28))
        self.pushButton_exit.setMaximumSize(QSize(100, 28))
        self.pushButton_exit.setFont(font2)
        self.pushButton_exit.setStyleSheet(u"")

        self.gridLayout_14.addWidget(self.pushButton_exit, 0, 0, 1, 1)


        self.gridLayout_7.addWidget(self.frame_11, 2, 0, 1, 1)


        self.retranslateUi(Dialog)

        self.tabWidget_main.setCurrentIndex(1)
        self.comboBox_selection_type.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Set transfer impendance", None))
#if QT_CONFIG(whatsthis)
        Dialog.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.label_21.setText(QCoreApplication.translate("Dialog", u"[Pa/m/s]", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Real", None))
        self.label_18.setText(QCoreApplication.translate("Dialog", u"Transfer impedance:", None))
        self.label_20.setText(QCoreApplication.translate("Dialog", u"Imaginary", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_constant_data), QCoreApplication.translate("Dialog", u"Constant data", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Choose a table file to import the data", None))
        self.pushButton_load_table.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_change_frequency_setup.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Filter the frequency range of interest</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_change_frequency_setup.setText("")
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_tabular_data), QCoreApplication.translate("Dialog", u"Tabular data", None))
        self.pushButton_reset.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.pushButton_remove.setText(QCoreApplication.translate("Dialog", u"Remove", None))
        ___qtreewidgetitem = self.treeWidget_transfer_impedance.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"Values", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Surface ID", None));
#if QT_CONFIG(tooltip)
        self.treeWidget_transfer_impedance.setToolTip(QCoreApplication.translate("Dialog", u"Select a face to remove the previously attributed boundary condition.", None))
#endif // QT_CONFIG(tooltip)
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_list), QCoreApplication.translate("Dialog", u"List", None))
        self.label_16.setText(QCoreApplication.translate("Dialog", u"Selection type:", None))
        self.comboBox_selection_type.setItemText(0, QCoreApplication.translate("Dialog", u"Inside surfaces", None))
        self.comboBox_selection_type.setItemText(1, QCoreApplication.translate("Dialog", u"Outside surfaces", None))

        self.lineEdit_selection_id_A.setText("")
        self.label_selection_A.setText(QCoreApplication.translate("Dialog", u"Selected surfaces A:", None))
        self.label_selection_B.setText(QCoreApplication.translate("Dialog", u"Selected surfaces B:", None))
        self.lineEdit_selection_id_B.setText("")
        self.label.setText(QCoreApplication.translate("Dialog", u"Set the transfer impedance", None))
        self.pushButton_attribute.setText(QCoreApplication.translate("Dialog", u"Attribute", None))
        self.pushButton_exit.setText(QCoreApplication.translate("Dialog", u"Exit", None))
    # retranslateUi



class TransferImpedanceInputs_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame_2: QFrame
                    - (Layout): QGridLayout
                            - tabWidget_main: QTabWidget
                                - tab_constant_data: QWidget
                                    - (Layout): QGridLayout
                                            - frame_8: QFrame
                                                - (Layout): QGridLayout
                                                        - label_21: QLabel
                                                        - label_4: QLabel
                                                        - label_18: QLabel
                                                        - lineEdit_real_value: QLineEdit
                                                        - label_20: QLabel
                                                        - lineEdit_imag_value: QLineEdit
                                - tab_tabular_data: QWidget
                                    - (Layout): QGridLayout
                                            - frame_9: QFrame
                                                - (Layout): QGridLayout
                                                        - label_2: QLabel
                                                        - pushButton_load_table: QPushButton
                                                        - lineEdit_table_path: QLineEdit
                                                        - pushButton_change_frequency_setup: QPushButton
                                - tab_list: QWidget
                                    - (Layout): QGridLayout
                                            - frame_3: QFrame
                                                - (Layout): QGridLayout
                                                        - pushButton_reset: QPushButton
                                                        - pushButton_remove: QPushButton
                                            - treeWidget_transfer_impedance: QTreeWidget
                            - frame_6: QFrame
                                - (Layout): QGridLayout
                                        - label_16: QLabel
                                        - comboBox_selection_type: QComboBox
                                        - lineEdit_selection_id_A: QLineEdit
                                        - label_selection_A: QLabel
                                        - label_selection_B: QLabel
                                        - lineEdit_selection_id_B: QLineEdit
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
