# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'set_material.ui'
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
        Dialog.resize(878, 500)
        Dialog.setMinimumSize(QSize(600, 500))
        Dialog.setMaximumSize(QSize(900, 600))
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.frame_main_widget = QFrame(Dialog)
        self.frame_main_widget.setObjectName(u"frame_main_widget")
        self.frame_main_widget.setFrameShape(QFrame.Shape.Box)
        self.frame_main_widget.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_main_widget)
        self.gridLayout_4.setSpacing(2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(2, 2, 2, 2)
        self.frame = QFrame(self.frame_main_widget)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(400, 0))
        self.frame.setMaximumSize(QSize(800, 80))
        font = QFont()
        font.setPointSize(10)
        self.frame.setFont(font)
        self.frame.setFrameShape(QFrame.Shape.NoFrame)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.frame.setLineWidth(1)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(6, 6, 6, 6)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 0, 4, 1, 1)

        self.comboBox_attribution_type = QComboBox(self.frame)
        self.comboBox_attribution_type.addItem("")
        self.comboBox_attribution_type.addItem("")
        self.comboBox_attribution_type.addItem("")
        self.comboBox_attribution_type.addItem("")
        self.comboBox_attribution_type.addItem("")
        self.comboBox_attribution_type.addItem("")
        self.comboBox_attribution_type.setObjectName(u"comboBox_attribution_type")
        self.comboBox_attribution_type.setMinimumSize(QSize(140, 26))
        self.comboBox_attribution_type.setMaximumSize(QSize(16777215, 26))
        self.comboBox_attribution_type.setFont(font)

        self.gridLayout_2.addWidget(self.comboBox_attribution_type, 0, 3, 1, 1)

        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        font1 = QFont()
        font1.setFamilies([u"MS Shell Dlg 2"])
        font1.setPointSize(10)
        font1.setBold(False)
        self.label.setFont(font1)
        self.label.setTextFormat(Qt.TextFormat.AutoText)
        self.label.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label, 0, 1, 1, 1)

        self.lineEdit_selection_id = QLineEdit(self.frame)
        self.lineEdit_selection_id.setObjectName(u"lineEdit_selection_id")
        self.lineEdit_selection_id.setEnabled(True)
        self.lineEdit_selection_id.setMinimumSize(QSize(180, 26))
        self.lineEdit_selection_id.setMaximumSize(QSize(180, 26))
        self.lineEdit_selection_id.setFont(font)
        self.lineEdit_selection_id.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.lineEdit_selection_id.setStyleSheet(u"")
        self.lineEdit_selection_id.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_selection_id, 0, 2, 1, 1)

        self.label_selected_material = QLabel(self.frame)
        self.label_selected_material.setObjectName(u"label_selected_material")
        self.label_selected_material.setFont(font1)
        self.label_selected_material.setTextFormat(Qt.TextFormat.AutoText)
        self.label_selected_material.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_selected_material, 1, 1, 1, 1)

        self.lineEdit_selected_material_name = QLineEdit(self.frame)
        self.lineEdit_selected_material_name.setObjectName(u"lineEdit_selected_material_name")
        self.lineEdit_selected_material_name.setEnabled(False)
        self.lineEdit_selected_material_name.setMinimumSize(QSize(180, 26))
        self.lineEdit_selected_material_name.setMaximumSize(QSize(180, 26))
        self.lineEdit_selected_material_name.setFont(font)
        self.lineEdit_selected_material_name.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.lineEdit_selected_material_name.setStyleSheet(u"")
        self.lineEdit_selected_material_name.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_selected_material_name, 1, 2, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_2, 0, 0, 1, 1)


        self.gridLayout_4.addWidget(self.frame, 0, 0, 1, 1)

        self.tabWidget_main = QTabWidget(self.frame_main_widget)
        self.tabWidget_main.setObjectName(u"tabWidget_main")
        self.tabWidget_main.setFont(font)
        self.tab_setup = QWidget()
        self.tab_setup.setObjectName(u"tab_setup")
        self.gridLayout_5 = QGridLayout(self.tab_setup)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(4, 4, 4, 4)
        self.scrollArea_table_of_materials = QScrollArea(self.tab_setup)
        self.scrollArea_table_of_materials.setObjectName(u"scrollArea_table_of_materials")
        self.scrollArea_table_of_materials.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollArea_table_of_materials.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 848, 322))
        self.scrollArea_table_of_materials.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_5.addWidget(self.scrollArea_table_of_materials, 0, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_setup, "")
        self.tab_list = QWidget()
        self.tab_list.setObjectName(u"tab_list")
        self.gridLayout_6 = QGridLayout(self.tab_list)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
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

        self.tableWidget_model_materials = QTableWidget(self.tab_list)
        if (self.tableWidget_model_materials.columnCount() < 6):
            self.tableWidget_model_materials.setColumnCount(6)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget_model_materials.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget_model_materials.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget_model_materials.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget_model_materials.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget_model_materials.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget_model_materials.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        self.tableWidget_model_materials.setObjectName(u"tableWidget_model_materials")
        self.tableWidget_model_materials.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.tableWidget_model_materials.verticalHeader().setVisible(False)

        self.gridLayout_6.addWidget(self.tableWidget_model_materials, 0, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_list, "")

        self.gridLayout_4.addWidget(self.tabWidget_main, 1, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_main_widget, 1, 0, 1, 1)

        self.frame_title = QFrame(Dialog)
        self.frame_title.setObjectName(u"frame_title")
        self.frame_title.setMinimumSize(QSize(0, 48))
        self.frame_title.setMaximumSize(QSize(16777215, 48))
        self.frame_title.setFrameShape(QFrame.Shape.Box)
        self.frame_title.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_title)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(4, 4, 4, 4)
        self.label_2 = QLabel(self.frame_title)
        self.label_2.setObjectName(u"label_2")
        font3 = QFont()
        font3.setFamilies([u"MS Shell Dlg 2"])
        font3.setPointSize(11)
        font3.setBold(False)
        self.label_2.setFont(font3)
        self.label_2.setTextFormat(Qt.TextFormat.AutoText)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.label_2, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_title, 0, 0, 1, 1)


        self.retranslateUi(Dialog)

        self.tabWidget_main.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.comboBox_attribution_type.setItemText(0, QCoreApplication.translate("Dialog", u"All bodies/faces", None))
        self.comboBox_attribution_type.setItemText(1, QCoreApplication.translate("Dialog", u"All bodies", None))
        self.comboBox_attribution_type.setItemText(2, QCoreApplication.translate("Dialog", u"All faces", None))
        self.comboBox_attribution_type.setItemText(3, QCoreApplication.translate("Dialog", u"Selected bodies", None))
        self.comboBox_attribution_type.setItemText(4, QCoreApplication.translate("Dialog", u"Selected faces", None))
        self.comboBox_attribution_type.setItemText(5, QCoreApplication.translate("Dialog", u"Selected bodies/faces", None))

        self.label.setText(QCoreApplication.translate("Dialog", u"Selection:", None))
        self.lineEdit_selection_id.setText("")
        self.label_selected_material.setText(QCoreApplication.translate("Dialog", u"Selected material:", None))
        self.lineEdit_selected_material_name.setText("")
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_setup), QCoreApplication.translate("Dialog", u"Setup", None))
        self.pushButton_reset.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.pushButton_remove.setText(QCoreApplication.translate("Dialog", u"Remove", None))
        ___qtablewidgetitem = self.tableWidget_model_materials.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Dialog", u"Selection-ID", None));
        ___qtablewidgetitem1 = self.tableWidget_model_materials.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Dialog", u"Name", None));
        ___qtablewidgetitem2 = self.tableWidget_model_materials.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Dialog", u"Identifier", None));
        ___qtablewidgetitem3 = self.tableWidget_model_materials.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Dialog", u"Density [kg/m\u00b3]", None));
        ___qtablewidgetitem4 = self.tableWidget_model_materials.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Dialog", u"Elasticity modulus [Pa]", None));
        ___qtablewidgetitem5 = self.tableWidget_model_materials.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Dialog", u"Poisson ratio [--]", None));
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_list), QCoreApplication.translate("Dialog", u"List", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Set material configuration", None))
    # retranslateUi



class SetMaterial_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame_main_widget: QFrame
                    - (Layout): QGridLayout
                            - frame: QFrame
                                - (Layout): QGridLayout
                                        - comboBox_attribution_type: QComboBox
                                        - label: QLabel
                                        - lineEdit_selection_id: QLineEdit
                                        - label_selected_material: QLabel
                                        - lineEdit_selected_material_name: QLineEdit
                            - tabWidget_main: QTabWidget
                                - tab_setup: QWidget
                                    - (Layout): QGridLayout
                                            - scrollArea_table_of_materials: QScrollArea
                                                - scrollAreaWidgetContents: QWidget
                                - tab_list: QWidget
                                    - (Layout): QGridLayout
                                            - frame_reset_remove_buttons: QFrame
                                                - (Layout): QGridLayout
                                                        - pushButton_reset: QPushButton
                                                        - pushButton_remove: QPushButton
                                            - tableWidget_model_materials: QTableWidget
                - frame_title: QFrame
                    - (Layout): QGridLayout
                            - label_2: QLabel
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
