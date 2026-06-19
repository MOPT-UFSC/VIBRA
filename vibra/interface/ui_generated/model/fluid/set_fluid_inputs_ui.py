# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'set_fluid_inputs.ui'
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
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QComboBox, QDialog,
    QFrame, QGridLayout, QHeaderView, QLabel,
    QLineEdit, QPushButton, QScrollArea, QSizePolicy,
    QSpacerItem, QTabWidget, QTableWidget, QTableWidgetItem,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(752, 720)
        Dialog.setMinimumSize(QSize(740, 600))
        Dialog.setMaximumSize(QSize(1000, 720))
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.frame_main_widget = QFrame(Dialog)
        self.frame_main_widget.setObjectName(u"frame_main_widget")
        self.frame_main_widget.setMinimumSize(QSize(0, 0))
        self.frame_main_widget.setMaximumSize(QSize(16777215, 16777215))
        self.frame_main_widget.setFrameShape(QFrame.Shape.Box)
        self.frame_main_widget.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_main_widget)
        self.gridLayout_3.setSpacing(2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(2, 2, 2, 2)
        self.frame_2 = QFrame(self.frame_main_widget)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(400, 0))
        self.frame_2.setMaximumSize(QSize(16777215, 80))
        self.frame_2.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_2.setLineWidth(1)
        self.gridLayout_4 = QGridLayout(self.frame_2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(6, 6, 6, 6)
        self.label_selected_fluid = QLabel(self.frame_2)
        self.label_selected_fluid.setObjectName(u"label_selected_fluid")
        font = QFont()
        font.setFamilies([u"MS Shell Dlg 2"])
        font.setPointSize(10)
        font.setBold(False)
        self.label_selected_fluid.setFont(font)
        self.label_selected_fluid.setTextFormat(Qt.TextFormat.AutoText)
        self.label_selected_fluid.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_selected_fluid, 1, 1, 1, 1)

        self.lineEdit_selection_id = QLineEdit(self.frame_2)
        self.lineEdit_selection_id.setObjectName(u"lineEdit_selection_id")
        self.lineEdit_selection_id.setEnabled(True)
        self.lineEdit_selection_id.setMinimumSize(QSize(180, 26))
        self.lineEdit_selection_id.setMaximumSize(QSize(180, 26))
        font1 = QFont()
        font1.setPointSize(10)
        self.lineEdit_selection_id.setFont(font1)
        self.lineEdit_selection_id.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.lineEdit_selection_id.setStyleSheet(u"")
        self.lineEdit_selection_id.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.lineEdit_selection_id, 0, 2, 1, 1)

        self.label_selected_id = QLabel(self.frame_2)
        self.label_selected_id.setObjectName(u"label_selected_id")
        self.label_selected_id.setFont(font)
        self.label_selected_id.setTextFormat(Qt.TextFormat.AutoText)
        self.label_selected_id.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_selected_id, 0, 1, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_3, 0, 4, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_4, 0, 0, 1, 1)

        self.lineEdit_selected_fluid_name = QLineEdit(self.frame_2)
        self.lineEdit_selected_fluid_name.setObjectName(u"lineEdit_selected_fluid_name")
        self.lineEdit_selected_fluid_name.setEnabled(False)
        self.lineEdit_selected_fluid_name.setMinimumSize(QSize(180, 26))
        self.lineEdit_selected_fluid_name.setMaximumSize(QSize(180, 26))
        self.lineEdit_selected_fluid_name.setFont(font1)
        self.lineEdit_selected_fluid_name.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.lineEdit_selected_fluid_name.setStyleSheet(u"")
        self.lineEdit_selected_fluid_name.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.lineEdit_selected_fluid_name, 1, 2, 1, 1)

        self.comboBox_attribution_type = QComboBox(self.frame_2)
        self.comboBox_attribution_type.addItem("")
        self.comboBox_attribution_type.addItem("")
        self.comboBox_attribution_type.setObjectName(u"comboBox_attribution_type")
        self.comboBox_attribution_type.setMinimumSize(QSize(140, 26))
        self.comboBox_attribution_type.setMaximumSize(QSize(16777215, 26))
        self.comboBox_attribution_type.setFont(font1)

        self.gridLayout_4.addWidget(self.comboBox_attribution_type, 0, 3, 1, 1)


        self.gridLayout_3.addWidget(self.frame_2, 0, 0, 1, 1)

        self.frame_3 = QFrame(self.frame_main_widget)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_7 = QGridLayout(self.frame_3)
        self.gridLayout_7.setSpacing(4)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(4, 4, 4, 4)
        self.tabWidget_main = QTabWidget(self.frame_3)
        self.tabWidget_main.setObjectName(u"tabWidget_main")
        self.tabWidget_main.setFont(font1)
        self.tab_setup = QWidget()
        self.tab_setup.setObjectName(u"tab_setup")
        self.gridLayout_5 = QGridLayout(self.tab_setup)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(4, 4, 4, 4)
        self.scrollArea_table_of_fluids = QScrollArea(self.tab_setup)
        self.scrollArea_table_of_fluids.setObjectName(u"scrollArea_table_of_fluids")
        self.scrollArea_table_of_fluids.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollArea_table_of_fluids.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 712, 532))
        self.scrollArea_table_of_fluids.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_5.addWidget(self.scrollArea_table_of_fluids, 0, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_setup, "")
        self.tab_list = QWidget()
        self.tab_list.setObjectName(u"tab_list")
        self.gridLayout_6 = QGridLayout(self.tab_list)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.tableWidget_model_fluids = QTableWidget(self.tab_list)
        if (self.tableWidget_model_fluids.columnCount() < 6):
            self.tableWidget_model_fluids.setColumnCount(6)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget_model_fluids.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget_model_fluids.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget_model_fluids.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget_model_fluids.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget_model_fluids.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget_model_fluids.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        self.tableWidget_model_fluids.setObjectName(u"tableWidget_model_fluids")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget_model_fluids.sizePolicy().hasHeightForWidth())
        self.tableWidget_model_fluids.setSizePolicy(sizePolicy)
        self.tableWidget_model_fluids.setMinimumSize(QSize(0, 350))
        self.tableWidget_model_fluids.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.tableWidget_model_fluids.verticalHeader().setVisible(False)

        self.gridLayout_6.addWidget(self.tableWidget_model_fluids, 0, 0, 1, 1)

        self.frame_reset_remove_buttons = QFrame(self.tab_list)
        self.frame_reset_remove_buttons.setObjectName(u"frame_reset_remove_buttons")
        self.frame_reset_remove_buttons.setMinimumSize(QSize(560, 40))
        self.frame_reset_remove_buttons.setMaximumSize(QSize(16777215, 40))
        self.frame_reset_remove_buttons.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_reset_remove_buttons.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_8 = QGridLayout(self.frame_reset_remove_buttons)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setHorizontalSpacing(12)
        self.gridLayout_8.setContentsMargins(4, 4, 4, 4)
        self.pushButton_reset = QPushButton(self.frame_reset_remove_buttons)
        self.pushButton_reset.setObjectName(u"pushButton_reset")
        self.pushButton_reset.setMinimumSize(QSize(100, 28))
        self.pushButton_reset.setMaximumSize(QSize(100, 28))
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        self.pushButton_reset.setFont(font2)
        self.pushButton_reset.setStyleSheet(u"")
        self.pushButton_reset.setAutoDefault(False)

        self.gridLayout_8.addWidget(self.pushButton_reset, 0, 0, 1, 1)

        self.pushButton_remove = QPushButton(self.frame_reset_remove_buttons)
        self.pushButton_remove.setObjectName(u"pushButton_remove")
        self.pushButton_remove.setMinimumSize(QSize(100, 28))
        self.pushButton_remove.setMaximumSize(QSize(100, 28))
        self.pushButton_remove.setFont(font2)
        self.pushButton_remove.setStyleSheet(u"")
        self.pushButton_remove.setAutoDefault(False)

        self.gridLayout_8.addWidget(self.pushButton_remove, 0, 1, 1, 1)


        self.gridLayout_6.addWidget(self.frame_reset_remove_buttons, 1, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_list, "")

        self.gridLayout_7.addWidget(self.tabWidget_main, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_3, 1, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_main_widget, 1, 0, 1, 1)

        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(400, 48))
        self.frame.setMaximumSize(QSize(16777215, 48))
        self.frame.setFrameShape(QFrame.Shape.Box)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.frame.setLineWidth(1)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(6, 6, 6, 6)
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        font3 = QFont()
        font3.setFamilies([u"MS Shell Dlg 2"])
        font3.setPointSize(11)
        font3.setBold(False)
        self.label.setFont(font3)
        self.label.setTextFormat(Qt.TextFormat.AutoText)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)


        self.retranslateUi(Dialog)

        self.tabWidget_main.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_selected_fluid.setText(QCoreApplication.translate("Dialog", u"Selected fluid:", None))
        self.lineEdit_selection_id.setText("")
        self.label_selected_id.setText(QCoreApplication.translate("Dialog", u"Selected id:", None))
        self.lineEdit_selected_fluid_name.setText("")
        self.comboBox_attribution_type.setItemText(0, QCoreApplication.translate("Dialog", u"All bodies", None))
        self.comboBox_attribution_type.setItemText(1, QCoreApplication.translate("Dialog", u"Selected bodies", None))

        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_setup), QCoreApplication.translate("Dialog", u"Setup", None))
        ___qtablewidgetitem = self.tableWidget_model_fluids.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Dialog", u"Selection-ID", None));
        ___qtablewidgetitem1 = self.tableWidget_model_fluids.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Dialog", u"Name", None));
        ___qtablewidgetitem2 = self.tableWidget_model_fluids.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Dialog", u"Identifier", None));
        ___qtablewidgetitem3 = self.tableWidget_model_fluids.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Dialog", u"Density [kg/m\u00b3]", None));
        ___qtablewidgetitem4 = self.tableWidget_model_fluids.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Dialog", u"Speed of sound [m/s]", None));
        ___qtablewidgetitem5 = self.tableWidget_model_fluids.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Dialog", u"Dynamic viscosity [Pa.s]", None));
        self.pushButton_reset.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.pushButton_remove.setText(QCoreApplication.translate("Dialog", u"Remove", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_list), QCoreApplication.translate("Dialog", u"List", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Set fluid configuration", None))
    # retranslateUi



class SetFluidInputs_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame_main_widget: QFrame
                    - (Layout): QGridLayout
                            - frame_2: QFrame
                                - (Layout): QGridLayout
                                        - label_selected_fluid: QLabel
                                        - lineEdit_selection_id: QLineEdit
                                        - label_selected_id: QLabel
                                        - lineEdit_selected_fluid_name: QLineEdit
                                        - comboBox_attribution_type: QComboBox
                            - frame_3: QFrame
                                - (Layout): QGridLayout
                                        - tabWidget_main: QTabWidget
                                            - tab_setup: QWidget
                                                - (Layout): QGridLayout
                                                        - scrollArea_table_of_fluids: QScrollArea
                                                            - scrollAreaWidgetContents: QWidget
                                            - tab_list: QWidget
                                                - (Layout): QGridLayout
                                                        - tableWidget_model_fluids: QTableWidget
                                                        - frame_reset_remove_buttons: QFrame
                                                            - (Layout): QGridLayout
                                                                    - pushButton_reset: QPushButton
                                                                    - pushButton_remove: QPushButton
                - frame: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
