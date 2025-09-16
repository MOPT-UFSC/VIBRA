# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'acoustic_pressure_inputs.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QGridLayout,
    QHeaderView, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QTabWidget, QTreeWidget,
    QTreeWidgetItem, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setWindowModality(Qt.WindowModal)
        Dialog.resize(420, 400)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(420, 400))
        Dialog.setMaximumSize(QSize(420, 400))
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
        self.frame_2.setMinimumSize(QSize(380, 280))
        self.frame_2.setMaximumSize(QSize(420, 480))
        self.frame_2.setFrameShape(QFrame.Box)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.frame_4 = QFrame(self.frame_2)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(360, 40))
        self.frame_4.setMaximumSize(QSize(380, 40))
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
        font1 = QFont()
        font1.setFamilies([u"MS Shell Dlg 2"])
        font1.setPointSize(10)
        font1.setBold(False)
        font1.setItalic(False)
        self.lineEdit_selection_id.setFont(font1)
        self.lineEdit_selection_id.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_selection_id.setStyleSheet(u"")
        self.lineEdit_selection_id.setAlignment(Qt.AlignCenter)

        self.gridLayout_5.addWidget(self.lineEdit_selection_id, 0, 2, 1, 1)

        self.label_2 = QLabel(self.frame_4)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(100, 28))
        self.label_2.setMaximumSize(QSize(100, 28))
        self.label_2.setFont(font1)
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_2, 0, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_2, 0, 3, 1, 1)


        self.gridLayout_4.addWidget(self.frame_4, 0, 0, 1, 1)

        self.tabWidget_main = QTabWidget(self.frame_2)
        self.tabWidget_main.setObjectName(u"tabWidget_main")
        self.tabWidget_main.setMinimumSize(QSize(360, 0))
        self.tabWidget_main.setMaximumSize(QSize(380, 16777215))
        font2 = QFont()
        font2.setPointSize(10)
        self.tabWidget_main.setFont(font2)
        self.tab_constant_data = QWidget()
        self.tab_constant_data.setObjectName(u"tab_constant_data")
        self.gridLayout_12 = QGridLayout(self.tab_constant_data)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setHorizontalSpacing(4)
        self.gridLayout_12.setVerticalSpacing(2)
        self.gridLayout_12.setContentsMargins(2, 6, 2, 6)
        self.lineEdit_imag_value = QLineEdit(self.tab_constant_data)
        self.lineEdit_imag_value.setObjectName(u"lineEdit_imag_value")
        self.lineEdit_imag_value.setMinimumSize(QSize(80, 28))
        self.lineEdit_imag_value.setMaximumSize(QSize(80, 28))
        self.lineEdit_imag_value.setFont(font1)
        self.lineEdit_imag_value.setStyleSheet(u"")
        self.lineEdit_imag_value.setAlignment(Qt.AlignCenter)

        self.gridLayout_12.addWidget(self.lineEdit_imag_value, 2, 3, 1, 1)

        self.label_4 = QLabel(self.tab_constant_data)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(80, 26))
        self.label_4.setMaximumSize(QSize(80, 26))
        self.label_4.setFont(font1)
        self.label_4.setAlignment(Qt.AlignCenter)

        self.gridLayout_12.addWidget(self.label_4, 1, 2, 1, 1)

        self.label_18 = QLabel(self.tab_constant_data)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setMinimumSize(QSize(120, 28))
        self.label_18.setMaximumSize(QSize(120, 28))
        self.label_18.setFont(font1)
        self.label_18.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_12.addWidget(self.label_18, 2, 1, 1, 1)

        self.lineEdit_real_value = QLineEdit(self.tab_constant_data)
        self.lineEdit_real_value.setObjectName(u"lineEdit_real_value")
        self.lineEdit_real_value.setMinimumSize(QSize(80, 28))
        self.lineEdit_real_value.setMaximumSize(QSize(80, 28))
        self.lineEdit_real_value.setFont(font1)
        self.lineEdit_real_value.setStyleSheet(u"")
        self.lineEdit_real_value.setAlignment(Qt.AlignCenter)

        self.gridLayout_12.addWidget(self.lineEdit_real_value, 2, 2, 1, 1)

        self.label_21 = QLabel(self.tab_constant_data)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setMinimumSize(QSize(0, 28))
        self.label_21.setMaximumSize(QSize(60, 28))
        self.label_21.setFont(font1)
        self.label_21.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_12.addWidget(self.label_21, 2, 4, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_12.addItem(self.verticalSpacer, 0, 2, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_12.addItem(self.horizontalSpacer_4, 2, 5, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_12.addItem(self.horizontalSpacer_3, 2, 0, 1, 1)

        self.label_20 = QLabel(self.tab_constant_data)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setMinimumSize(QSize(80, 26))
        self.label_20.setMaximumSize(QSize(80, 26))
        self.label_20.setFont(font1)
        self.label_20.setAlignment(Qt.AlignCenter)

        self.gridLayout_12.addWidget(self.label_20, 1, 3, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_12.addItem(self.verticalSpacer_2, 3, 2, 1, 1)

        self.tabWidget_main.addTab(self.tab_constant_data, "")
        self.tab_tabular_data = QWidget()
        self.tab_tabular_data.setObjectName(u"tab_tabular_data")
        self.gridLayout_3 = QGridLayout(self.tab_tabular_data)
        self.gridLayout_3.setSpacing(6)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(2, 6, 2, 6)
        self.pushButton_load_table = QPushButton(self.tab_tabular_data)
        self.pushButton_load_table.setObjectName(u"pushButton_load_table")
        self.pushButton_load_table.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton_load_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_table.setSizePolicy(sizePolicy1)
        self.pushButton_load_table.setMinimumSize(QSize(40, 28))
        self.pushButton_load_table.setMaximumSize(QSize(40, 28))
        self.pushButton_load_table.setFont(font1)
        self.pushButton_load_table.setStyleSheet(u"")
        icon = QIcon()
        icon.addFile(u":/icons/document_search_blue.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_load_table.setIcon(icon)
        self.pushButton_load_table.setIconSize(QSize(20, 20))

        self.gridLayout_3.addWidget(self.pushButton_load_table, 2, 2, 1, 1)

        self.lineEdit_table_path = QLineEdit(self.tab_tabular_data)
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

        self.gridLayout_3.addWidget(self.lineEdit_table_path, 2, 1, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_5, 2, 4, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_6, 2, 0, 1, 1)

        self.pushButton_change_frequency_setup = QPushButton(self.tab_tabular_data)
        self.pushButton_change_frequency_setup.setObjectName(u"pushButton_change_frequency_setup")
        self.pushButton_change_frequency_setup.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.pushButton_change_frequency_setup.sizePolicy().hasHeightForWidth())
        self.pushButton_change_frequency_setup.setSizePolicy(sizePolicy1)
        self.pushButton_change_frequency_setup.setMinimumSize(QSize(40, 28))
        self.pushButton_change_frequency_setup.setMaximumSize(QSize(40, 28))
        self.pushButton_change_frequency_setup.setFont(font1)
        self.pushButton_change_frequency_setup.setStyleSheet(u"")
        icon1 = QIcon()
        icon1.addFile(u":/icons/recent.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_change_frequency_setup.setIcon(icon1)
        self.pushButton_change_frequency_setup.setIconSize(QSize(20, 20))

        self.gridLayout_3.addWidget(self.pushButton_change_frequency_setup, 3, 2, 1, 1)

        self.label_3 = QLabel(self.tab_tabular_data)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(0, 28))
        self.label_3.setMaximumSize(QSize(16777215, 28))
        self.label_3.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.label_3, 1, 1, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer_4, 0, 1, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer_3, 4, 1, 1, 1)

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
        self.pushButton_reset.setFont(font1)
        self.pushButton_reset.setStyleSheet(u"")

        self.gridLayout_8.addWidget(self.pushButton_reset, 0, 0, 1, 1)

        self.pushButton_remove = QPushButton(self.frame_3)
        self.pushButton_remove.setObjectName(u"pushButton_remove")
        self.pushButton_remove.setMinimumSize(QSize(100, 28))
        self.pushButton_remove.setMaximumSize(QSize(100, 28))
        self.pushButton_remove.setFont(font1)
        self.pushButton_remove.setStyleSheet(u"")

        self.gridLayout_8.addWidget(self.pushButton_remove, 0, 1, 1, 1)


        self.gridLayout_9.addWidget(self.frame_3, 1, 0, 1, 1)

        self.treeWidget_acoustic_pressure = QTreeWidget(self.tab_list)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter);
        self.treeWidget_acoustic_pressure.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_acoustic_pressure.setObjectName(u"treeWidget_acoustic_pressure")
        self.treeWidget_acoustic_pressure.setMinimumSize(QSize(320, 100))
        self.treeWidget_acoustic_pressure.setMaximumSize(QSize(320, 200))
        font4 = QFont()
        font4.setFamilies([u"MS Shell Dlg 2"])
        font4.setPointSize(10)
        font4.setItalic(False)
        self.treeWidget_acoustic_pressure.setFont(font4)
        self.treeWidget_acoustic_pressure.setIndentation(1)
        self.treeWidget_acoustic_pressure.setHeaderHidden(False)
        self.treeWidget_acoustic_pressure.header().setHighlightSections(False)
        self.treeWidget_acoustic_pressure.header().setProperty(u"showSortIndicator", False)
        self.treeWidget_acoustic_pressure.header().setStretchLastSection(True)

        self.gridLayout_9.addWidget(self.treeWidget_acoustic_pressure, 0, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_list, "")

        self.gridLayout_4.addWidget(self.tabWidget_main, 1, 0, 1, 1)


        self.gridLayout_7.addWidget(self.frame_2, 1, 0, 1, 1)

        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(380, 48))
        self.frame.setMaximumSize(QSize(420, 48))
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setLineWidth(1)
        self.gridLayout_6 = QGridLayout(self.frame)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        font5 = QFont()
        font5.setFamilies([u"MS Shell Dlg 2"])
        font5.setPointSize(11)
        font5.setBold(False)
        font5.setItalic(False)
        self.label.setFont(font5)
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
        self.pushButton_attribute.setFont(font1)
        self.pushButton_attribute.setStyleSheet(u"")

        self.gridLayout_14.addWidget(self.pushButton_attribute, 0, 1, 1, 1)

        self.pushButton_exit = QPushButton(self.frame_11)
        self.pushButton_exit.setObjectName(u"pushButton_exit")
        self.pushButton_exit.setMinimumSize(QSize(100, 28))
        self.pushButton_exit.setMaximumSize(QSize(100, 28))
        self.pushButton_exit.setFont(font1)
        self.pushButton_exit.setStyleSheet(u"")

        self.gridLayout_14.addWidget(self.pushButton_exit, 0, 0, 1, 1)


        self.gridLayout_7.addWidget(self.frame_11, 2, 0, 1, 1)


        self.retranslateUi(Dialog)

        self.tabWidget_main.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Prescribe an acoustic pressure", None))
#if QT_CONFIG(whatsthis)
        Dialog.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Selection ID:", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Real", None))
        self.label_18.setText(QCoreApplication.translate("Dialog", u"Acoustic pressure:", None))
        self.label_21.setText(QCoreApplication.translate("Dialog", u"[Pa]", None))
        self.label_20.setText(QCoreApplication.translate("Dialog", u"Imaginary", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_constant_data), QCoreApplication.translate("Dialog", u"Constant data", None))
        self.pushButton_load_table.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_change_frequency_setup.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Filter the frequency range of interest</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_change_frequency_setup.setText("")
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Choose a table file to import the data", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_tabular_data), QCoreApplication.translate("Dialog", u"Tabular data", None))
        self.pushButton_reset.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.pushButton_remove.setText(QCoreApplication.translate("Dialog", u"Remove", None))
        ___qtreewidgetitem = self.treeWidget_acoustic_pressure.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"Values", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Nodes", None));
#if QT_CONFIG(tooltip)
        self.treeWidget_acoustic_pressure.setToolTip(QCoreApplication.translate("Dialog", u"Select a face to remove the previously attributed boundary condition.", None))
#endif // QT_CONFIG(tooltip)
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_list), QCoreApplication.translate("Dialog", u"List", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Acoustic pressure prescription setup", None))
        self.pushButton_attribute.setText(QCoreApplication.translate("Dialog", u"Attribute", None))
        self.pushButton_exit.setText(QCoreApplication.translate("Dialog", u"Exit", None))
    # retranslateUi



class AcousticPressureInputs_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame_2: QFrame
                    - (Layout): QGridLayout
                            - frame_4: QFrame
                                - (Layout): QGridLayout
                                        - lineEdit_selection_id: QLineEdit
                                        - label_2: QLabel
                            - tabWidget_main: QTabWidget
                                - tab_constant_data: QWidget
                                    - (Layout): QGridLayout
                                            - lineEdit_imag_value: QLineEdit
                                            - label_4: QLabel
                                            - label_18: QLabel
                                            - lineEdit_real_value: QLineEdit
                                            - label_21: QLabel
                                            - label_20: QLabel
                                - tab_tabular_data: QWidget
                                    - (Layout): QGridLayout
                                            - pushButton_load_table: QPushButton
                                            - lineEdit_table_path: QLineEdit
                                            - pushButton_change_frequency_setup: QPushButton
                                            - label_3: QLabel
                                - tab_list: QWidget
                                    - (Layout): QGridLayout
                                            - frame_3: QFrame
                                                - (Layout): QGridLayout
                                                        - pushButton_reset: QPushButton
                                                        - pushButton_remove: QPushButton
                                            - treeWidget_acoustic_pressure: QTreeWidget
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
