# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mesher_setup.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
    QDoubleSpinBox, QFrame, QGridLayout, QHeaderView,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QTableWidget, QTableWidgetItem, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(560, 500)
        Dialog.setMinimumSize(QSize(520, 480))
        Dialog.setMaximumSize(QSize(560, 500))
        self.gridLayout_7 = QGridLayout(Dialog)
        self.gridLayout_7.setSpacing(4)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(4, 4, 4, 4)
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 0))
        self.frame.setMaximumSize(QSize(16777215, 480))
        font = QFont()
        font.setPointSize(8)
        self.frame.setFont(font)
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_6 = QGridLayout(self.frame)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(4, 4, 4, 4)
        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(0, 62))
        self.frame_2.setFrameShape(QFrame.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame_2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(6)
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.doubleSpinBox_maximum_element_size = QDoubleSpinBox(self.frame_2)
        self.doubleSpinBox_maximum_element_size.setObjectName(u"doubleSpinBox_maximum_element_size")
        self.doubleSpinBox_maximum_element_size.setMinimumSize(QSize(0, 28))
        self.doubleSpinBox_maximum_element_size.setMaximumSize(QSize(16777215, 16777215))
        font1 = QFont()
        font1.setPointSize(10)
        self.doubleSpinBox_maximum_element_size.setFont(font1)
        self.doubleSpinBox_maximum_element_size.setAlignment(Qt.AlignCenter)
        self.doubleSpinBox_maximum_element_size.setDecimals(2)
        self.doubleSpinBox_maximum_element_size.setMinimum(0.010000000000000)
        self.doubleSpinBox_maximum_element_size.setMaximum(2000.000000000000000)
        self.doubleSpinBox_maximum_element_size.setSingleStep(2.000000000000000)
        self.doubleSpinBox_maximum_element_size.setValue(50.000000000000000)

        self.gridLayout.addWidget(self.doubleSpinBox_maximum_element_size, 1, 0, 1, 1)

        self.label = QLabel(self.frame_2)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(150, 20))
        self.label.setMaximumSize(QSize(160, 16777215))
        self.label.setFont(font1)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.lineEdit_geometry_tolerance = QLineEdit(self.frame_2)
        self.lineEdit_geometry_tolerance.setObjectName(u"lineEdit_geometry_tolerance")
        self.lineEdit_geometry_tolerance.setMinimumSize(QSize(0, 28))
        self.lineEdit_geometry_tolerance.setMaximumSize(QSize(160, 16777215))
        self.lineEdit_geometry_tolerance.setFont(font1)
        self.lineEdit_geometry_tolerance.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_geometry_tolerance, 1, 2, 1, 1)

        self.label_2 = QLabel(self.frame_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(0, 20))
        self.label_2.setMaximumSize(QSize(160, 16777215))
        self.label_2.setFont(font1)

        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)

        self.doubleSpinBox_minimum_element_size_factor = QDoubleSpinBox(self.frame_2)
        self.doubleSpinBox_minimum_element_size_factor.setObjectName(u"doubleSpinBox_minimum_element_size_factor")
        self.doubleSpinBox_minimum_element_size_factor.setMinimumSize(QSize(0, 28))
        self.doubleSpinBox_minimum_element_size_factor.setMaximumSize(QSize(16777215, 16777215))
        self.doubleSpinBox_minimum_element_size_factor.setFont(font1)
        self.doubleSpinBox_minimum_element_size_factor.setAlignment(Qt.AlignCenter)
        self.doubleSpinBox_minimum_element_size_factor.setDecimals(1)
        self.doubleSpinBox_minimum_element_size_factor.setMinimum(0.100000000000000)
        self.doubleSpinBox_minimum_element_size_factor.setMaximum(1.000000000000000)
        self.doubleSpinBox_minimum_element_size_factor.setSingleStep(0.100000000000000)
        self.doubleSpinBox_minimum_element_size_factor.setValue(0.900000000000000)

        self.gridLayout.addWidget(self.doubleSpinBox_minimum_element_size_factor, 1, 1, 1, 1)

        self.label_7 = QLabel(self.frame_2)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(150, 20))
        self.label_7.setMaximumSize(QSize(160, 16777215))
        self.label_7.setFont(font1)

        self.gridLayout.addWidget(self.label_7, 0, 1, 1, 1)


        self.gridLayout_6.addWidget(self.frame_2, 0, 0, 1, 1)

        self.frame_3 = QFrame(self.frame)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(0, 62))
        self.frame_3.setFrameShape(QFrame.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_3)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setHorizontalSpacing(6)
        self.gridLayout_3.setContentsMargins(4, 4, 4, 4)
        self.lineEdit_selected_ids = QLineEdit(self.frame_3)
        self.lineEdit_selected_ids.setObjectName(u"lineEdit_selected_ids")
        self.lineEdit_selected_ids.setMinimumSize(QSize(0, 28))
        self.lineEdit_selected_ids.setFont(font1)
        self.lineEdit_selected_ids.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.lineEdit_selected_ids, 1, 1, 1, 1)

        self.label_selected_ids = QLabel(self.frame_3)
        self.label_selected_ids.setObjectName(u"label_selected_ids")
        self.label_selected_ids.setMinimumSize(QSize(0, 20))
        self.label_selected_ids.setFont(font1)

        self.gridLayout_3.addWidget(self.label_selected_ids, 0, 1, 1, 1)

        self.label_6 = QLabel(self.frame_3)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(0, 20))
        self.label_6.setFont(font1)

        self.gridLayout_3.addWidget(self.label_6, 0, 0, 1, 1)

        self.pushButton_delete = QPushButton(self.frame_3)
        self.pushButton_delete.setObjectName(u"pushButton_delete")
        self.pushButton_delete.setMinimumSize(QSize(68, 28))
        self.pushButton_delete.setFont(font1)
        self.pushButton_delete.setAutoDefault(False)

        self.gridLayout_3.addWidget(self.pushButton_delete, 1, 3, 1, 1)

        self.pushButton_add = QPushButton(self.frame_3)
        self.pushButton_add.setObjectName(u"pushButton_add")
        self.pushButton_add.setMinimumSize(QSize(68, 28))
        self.pushButton_add.setFont(font1)
        self.pushButton_add.setAutoDefault(False)

        self.gridLayout_3.addWidget(self.pushButton_add, 1, 2, 1, 1)

        self.doubleSpinBox_refined_element_size = QDoubleSpinBox(self.frame_3)
        self.doubleSpinBox_refined_element_size.setObjectName(u"doubleSpinBox_refined_element_size")
        self.doubleSpinBox_refined_element_size.setMinimumSize(QSize(0, 28))
        self.doubleSpinBox_refined_element_size.setMaximumSize(QSize(16777215, 16777215))
        self.doubleSpinBox_refined_element_size.setFont(font1)
        self.doubleSpinBox_refined_element_size.setAlignment(Qt.AlignCenter)
        self.doubleSpinBox_refined_element_size.setDecimals(2)
        self.doubleSpinBox_refined_element_size.setMinimum(0.010000000000000)
        self.doubleSpinBox_refined_element_size.setMaximum(2000.000000000000000)
        self.doubleSpinBox_refined_element_size.setSingleStep(1.000000000000000)
        self.doubleSpinBox_refined_element_size.setValue(10.000000000000000)

        self.gridLayout_3.addWidget(self.doubleSpinBox_refined_element_size, 1, 0, 1, 1)


        self.gridLayout_6.addWidget(self.frame_3, 2, 0, 1, 1)

        self.frame_5 = QFrame(self.frame)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_5)
        self.gridLayout_5.setSpacing(4)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(4, 4, 4, 4)
        self.tableWidget_refining_mesh_data = QTableWidget(self.frame_5)
        if (self.tableWidget_refining_mesh_data.columnCount() < 3):
            self.tableWidget_refining_mesh_data.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_refining_mesh_data.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_refining_mesh_data.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        __qtablewidgetitem2.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_refining_mesh_data.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.tableWidget_refining_mesh_data.setObjectName(u"tableWidget_refining_mesh_data")
        self.tableWidget_refining_mesh_data.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_refining_mesh_data.verticalHeader().setVisible(False)
        self.tableWidget_refining_mesh_data.verticalHeader().setStretchLastSection(False)

        self.gridLayout_5.addWidget(self.tableWidget_refining_mesh_data, 0, 0, 1, 1)


        self.gridLayout_6.addWidget(self.frame_5, 3, 0, 1, 1)

        self.frame_8 = QFrame(self.frame)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setMinimumSize(QSize(0, 62))
        self.frame_8.setFrameShape(QFrame.NoFrame)
        self.frame_8.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_8)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setHorizontalSpacing(6)
        self.gridLayout_2.setContentsMargins(4, 4, 4, 4)
        self.label_3 = QLabel(self.frame_8)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(0, 20))
        self.label_3.setMaximumSize(QSize(120, 16777215))
        self.label_3.setFont(font1)

        self.gridLayout_2.addWidget(self.label_3, 0, 0, 1, 1)

        self.label_4 = QLabel(self.frame_8)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(0, 20))
        self.label_4.setMaximumSize(QSize(120, 16777215))
        self.label_4.setFont(font1)

        self.gridLayout_2.addWidget(self.label_4, 0, 1, 1, 1)

        self.comboBox_element_type = QComboBox(self.frame_8)
        self.comboBox_element_type.addItem("")
        self.comboBox_element_type.addItem("")
        self.comboBox_element_type.addItem("")
        self.comboBox_element_type.addItem("")
        self.comboBox_element_type.setObjectName(u"comboBox_element_type")
        self.comboBox_element_type.setMinimumSize(QSize(0, 28))
        self.comboBox_element_type.setMaximumSize(QSize(120, 16777215))
        self.comboBox_element_type.setFont(font1)

        self.gridLayout_2.addWidget(self.comboBox_element_type, 1, 0, 1, 1)

        self.comboBox_shape_function = QComboBox(self.frame_8)
        self.comboBox_shape_function.addItem("")
        self.comboBox_shape_function.addItem("")
        self.comboBox_shape_function.setObjectName(u"comboBox_shape_function")
        self.comboBox_shape_function.setMinimumSize(QSize(0, 28))
        self.comboBox_shape_function.setMaximumSize(QSize(120, 16777215))
        self.comboBox_shape_function.setFont(font1)

        self.gridLayout_2.addWidget(self.comboBox_shape_function, 1, 1, 1, 1)

        self.checkBox_mesh_connection = QCheckBox(self.frame_8)
        self.checkBox_mesh_connection.setObjectName(u"checkBox_mesh_connection")
        self.checkBox_mesh_connection.setMinimumSize(QSize(0, 28))
        self.checkBox_mesh_connection.setFont(font1)
        self.checkBox_mesh_connection.setChecked(True)

        self.gridLayout_2.addWidget(self.checkBox_mesh_connection, 1, 2, 1, 1)


        self.gridLayout_6.addWidget(self.frame_8, 1, 0, 1, 1)

        self.frame_4 = QFrame(self.frame)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(4, 4, 4, 4)
        self.pushButton_generate_mesh = QPushButton(self.frame_4)
        self.pushButton_generate_mesh.setObjectName(u"pushButton_generate_mesh")
        self.pushButton_generate_mesh.setMinimumSize(QSize(140, 30))
        self.pushButton_generate_mesh.setMaximumSize(QSize(140, 30))
        self.pushButton_generate_mesh.setFont(font1)

        self.gridLayout_4.addWidget(self.pushButton_generate_mesh, 0, 1, 1, 1)

        self.pushButton_exit = QPushButton(self.frame_4)
        self.pushButton_exit.setObjectName(u"pushButton_exit")
        self.pushButton_exit.setMinimumSize(QSize(140, 30))
        self.pushButton_exit.setMaximumSize(QSize(140, 30))
        self.pushButton_exit.setFont(font1)

        self.gridLayout_4.addWidget(self.pushButton_exit, 0, 0, 1, 1)


        self.gridLayout_6.addWidget(self.frame_4, 4, 0, 1, 1)


        self.gridLayout_7.addWidget(self.frame, 1, 0, 1, 1)

        self.frame_6 = QFrame(Dialog)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setMinimumSize(QSize(400, 48))
        self.frame_6.setMaximumSize(QSize(16777215, 48))
        self.frame_6.setFrameShape(QFrame.Box)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.frame_6.setLineWidth(1)
        self.gridLayout_8 = QGridLayout(self.frame_6)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(6, 6, 6, 6)
        self.label_8 = QLabel(self.frame_6)
        self.label_8.setObjectName(u"label_8")
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        font2.setPointSize(11)
        font2.setBold(False)
        self.label_8.setFont(font2)
        self.label_8.setTextFormat(Qt.AutoText)
        self.label_8.setAlignment(Qt.AlignCenter)

        self.gridLayout_8.addWidget(self.label_8, 0, 0, 1, 1)


        self.gridLayout_7.addWidget(self.frame_6, 0, 0, 1, 1)

        QWidget.setTabOrder(self.lineEdit_geometry_tolerance, self.comboBox_element_type)
        QWidget.setTabOrder(self.comboBox_element_type, self.comboBox_shape_function)
        QWidget.setTabOrder(self.comboBox_shape_function, self.checkBox_mesh_connection)
        QWidget.setTabOrder(self.checkBox_mesh_connection, self.lineEdit_selected_ids)
        QWidget.setTabOrder(self.lineEdit_selected_ids, self.pushButton_add)
        QWidget.setTabOrder(self.pushButton_add, self.pushButton_delete)
        QWidget.setTabOrder(self.pushButton_delete, self.tableWidget_refining_mesh_data)
        QWidget.setTabOrder(self.tableWidget_refining_mesh_data, self.pushButton_generate_mesh)

        self.retranslateUi(Dialog)

        self.pushButton_generate_mesh.setDefault(True)
        self.pushButton_exit.setDefault(True)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Max. element size [mm]:", None))
        self.lineEdit_geometry_tolerance.setText(QCoreApplication.translate("Dialog", u"1e-6", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Geometry tolerance [mm]:", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"Min. element size factor:", None))
        self.lineEdit_selected_ids.setText("")
        self.label_selected_ids.setText(QCoreApplication.translate("Dialog", u"Selected surface IDs:", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"Refined element size [mm]: ", None))
        self.pushButton_delete.setText(QCoreApplication.translate("Dialog", u"Delete", None))
        self.pushButton_add.setText(QCoreApplication.translate("Dialog", u"Add", None))
        ___qtablewidgetitem = self.tableWidget_refining_mesh_data.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Dialog", u"Refining mesh size [mm]", None));
        ___qtablewidgetitem1 = self.tableWidget_refining_mesh_data.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Dialog", u"Selection type", None));
        ___qtablewidgetitem2 = self.tableWidget_refining_mesh_data.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Dialog", u"Surface IDs", None));
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Element type:", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Shape function:", None))
        self.comboBox_element_type.setItemText(0, QCoreApplication.translate("Dialog", u" Tetrahedral", None))
        self.comboBox_element_type.setItemText(1, QCoreApplication.translate("Dialog", u" Hexahedral", None))
        self.comboBox_element_type.setItemText(2, QCoreApplication.translate("Dialog", u" Triangular", None))
        self.comboBox_element_type.setItemText(3, QCoreApplication.translate("Dialog", u" Quadrangular", None))

        self.comboBox_shape_function.setItemText(0, QCoreApplication.translate("Dialog", u" Linear", None))
        self.comboBox_shape_function.setItemText(1, QCoreApplication.translate("Dialog", u" Quadratic", None))

        self.checkBox_mesh_connection.setText(QCoreApplication.translate("Dialog", u"Merge nodes from connected volumes", None))
        self.pushButton_generate_mesh.setText(QCoreApplication.translate("Dialog", u"Generate mesh", None))
        self.pushButton_exit.setText(QCoreApplication.translate("Dialog", u"Exit", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"Mesh configuration", None))
    # retranslateUi



class MesherSetup_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame: QFrame
                    - (Layout): QGridLayout
                            - frame_2: QFrame
                                - (Layout): QGridLayout
                                        - doubleSpinBox_maximum_element_size: QDoubleSpinBox
                                        - label: QLabel
                                        - lineEdit_geometry_tolerance: QLineEdit
                                        - label_2: QLabel
                                        - doubleSpinBox_minimum_element_size_factor: QDoubleSpinBox
                                        - label_7: QLabel
                            - frame_3: QFrame
                                - (Layout): QGridLayout
                                        - lineEdit_selected_ids: QLineEdit
                                        - label_selected_ids: QLabel
                                        - label_6: QLabel
                                        - pushButton_delete: QPushButton
                                        - pushButton_add: QPushButton
                                        - doubleSpinBox_refined_element_size: QDoubleSpinBox
                            - frame_5: QFrame
                                - (Layout): QGridLayout
                                        - tableWidget_refining_mesh_data: QTableWidget
                            - frame_8: QFrame
                                - (Layout): QGridLayout
                                        - label_3: QLabel
                                        - label_4: QLabel
                                        - comboBox_element_type: QComboBox
                                        - comboBox_shape_function: QComboBox
                                        - checkBox_mesh_connection: QCheckBox
                            - frame_4: QFrame
                                - (Layout): QGridLayout
                                        - pushButton_generate_mesh: QPushButton
                                        - pushButton_exit: QPushButton
                - frame_6: QFrame
                    - (Layout): QGridLayout
                            - label_8: QLabel
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
