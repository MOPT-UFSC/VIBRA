# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'structural_stress_3d_plot_time_inputs.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QLabel, QLineEdit, QPushButton, QScrollArea,
    QSizePolicy, QSpacerItem, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(384, 781)
        Form.setMaximumSize(QSize(16777215, 16777215))
        self.gridLayout_2 = QGridLayout(Form)
        self.gridLayout_2.setSpacing(2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(2, 2, 2, 2)
        self.scrollArea = QScrollArea(Form)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 380, 777))
        self.gridLayout_6 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setHorizontalSpacing(2)
        self.gridLayout_6.setVerticalSpacing(4)
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.frame_color = QFrame(self.scrollAreaWidgetContents)
        self.frame_color.setObjectName(u"frame_color")
        self.frame_color.setMinimumSize(QSize(0, 168))
        self.frame_color.setMaximumSize(QSize(16777215, 168))
        self.frame_color.setFrameShape(QFrame.Shape.Box)
        self.frame_color.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_6.addWidget(self.frame_color, 3, 0, 1, 1)

        self.frame_title = QFrame(self.scrollAreaWidgetContents)
        self.frame_title.setObjectName(u"frame_title")
        self.frame_title.setMinimumSize(QSize(0, 40))
        self.frame_title.setMaximumSize(QSize(16777215, 40))
        self.frame_title.setFrameShape(QFrame.Shape.Box)
        self.frame_title.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_title.setLineWidth(1)
        self.gridLayout = QGridLayout(self.frame_title)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(10, 0, -1, 0)
        self.label_title = QLabel(self.frame_title)
        self.label_title.setObjectName(u"label_title")
        self.label_title.setMinimumSize(QSize(0, 0))
        self.label_title.setMaximumSize(QSize(16777215, 32))
        font = QFont()
        font.setFamilies([u"MS Shell Dlg 2"])
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        self.label_title.setFont(font)
        self.label_title.setFrameShape(QFrame.Shape.NoFrame)
        self.label_title.setFrameShadow(QFrame.Shadow.Raised)
        self.label_title.setTextFormat(Qt.TextFormat.AutoText)
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_title, 0, 0, 1, 1)


        self.gridLayout_6.addWidget(self.frame_title, 0, 0, 1, 1)

        self.frame_main = QFrame(self.scrollAreaWidgetContents)
        self.frame_main.setObjectName(u"frame_main")
        self.frame_main.setMinimumSize(QSize(0, 260))
        self.frame_main.setMaximumSize(QSize(16777215, 260))
        self.frame_main.setSizeIncrement(QSize(0, 0))
        self.frame_main.setBaseSize(QSize(0, 0))
        self.frame_main.setFrameShape(QFrame.Shape.Box)
        self.frame_main.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_main)
        self.gridLayout_5.setSpacing(4)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(4, 4, 4, 4)
        self.frame_plot_controls = QFrame(self.frame_main)
        self.frame_plot_controls.setObjectName(u"frame_plot_controls")
        self.frame_plot_controls.setMinimumSize(QSize(0, 0))
        self.frame_plot_controls.setMaximumSize(QSize(16777215, 16777215))
        self.frame_plot_controls.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_plot_controls.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_plot_controls)
        self.gridLayout_4.setSpacing(6)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 6, 0, 6)
        self.comboBox_reduced_time = QComboBox(self.frame_plot_controls)
        self.comboBox_reduced_time.addItem("")
        self.comboBox_reduced_time.addItem("")
        self.comboBox_reduced_time.addItem("")
        self.comboBox_reduced_time.setObjectName(u"comboBox_reduced_time")
        self.comboBox_reduced_time.setMinimumSize(QSize(176, 28))
        self.comboBox_reduced_time.setMaximumSize(QSize(200, 28))
        font1 = QFont()
        font1.setPointSize(10)
        self.comboBox_reduced_time.setFont(font1)

        self.gridLayout_4.addWidget(self.comboBox_reduced_time, 2, 2, 1, 1)

        self.comboBox_stress_units = QComboBox(self.frame_plot_controls)
        self.comboBox_stress_units.addItem("")
        self.comboBox_stress_units.addItem("")
        self.comboBox_stress_units.addItem("")
        self.comboBox_stress_units.addItem("")
        self.comboBox_stress_units.addItem("")
        self.comboBox_stress_units.addItem("")
        self.comboBox_stress_units.setObjectName(u"comboBox_stress_units")
        self.comboBox_stress_units.setMinimumSize(QSize(180, 28))
        self.comboBox_stress_units.setMaximumSize(QSize(180, 28))
        self.comboBox_stress_units.setFont(font1)
        self.comboBox_stress_units.setStyleSheet(u"")

        self.gridLayout_4.addWidget(self.comboBox_stress_units, 1, 2, 1, 1)

        self.label_reduced_time = QLabel(self.frame_plot_controls)
        self.label_reduced_time.setObjectName(u"label_reduced_time")
        self.label_reduced_time.setMinimumSize(QSize(100, 26))
        self.label_reduced_time.setMaximumSize(QSize(110, 26))
        self.label_reduced_time.setFont(font1)
        self.label_reduced_time.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_reduced_time, 2, 1, 1, 1)

        self.label_animation_time = QLabel(self.frame_plot_controls)
        self.label_animation_time.setObjectName(u"label_animation_time")
        self.label_animation_time.setMinimumSize(QSize(100, 26))
        self.label_animation_time.setMaximumSize(QSize(110, 26))
        self.label_animation_time.setFont(font1)
        self.label_animation_time.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_animation_time, 3, 1, 1, 1)

        self.lineEdit_animation_time = QLineEdit(self.frame_plot_controls)
        self.lineEdit_animation_time.setObjectName(u"lineEdit_animation_time")
        self.lineEdit_animation_time.setMinimumSize(QSize(0, 28))
        self.lineEdit_animation_time.setMaximumSize(QSize(16777215, 28))
        self.lineEdit_animation_time.setFont(font1)

        self.gridLayout_4.addWidget(self.lineEdit_animation_time, 3, 2, 1, 1)

        self.comboBox_plot_type = QComboBox(self.frame_plot_controls)
        self.comboBox_plot_type.addItem("")
        self.comboBox_plot_type.addItem("")
        self.comboBox_plot_type.setObjectName(u"comboBox_plot_type")
        self.comboBox_plot_type.setMinimumSize(QSize(176, 28))
        self.comboBox_plot_type.setMaximumSize(QSize(200, 28))
        self.comboBox_plot_type.setFont(font1)

        self.gridLayout_4.addWidget(self.comboBox_plot_type, 4, 2, 1, 1)

        self.label_linear_2 = QLabel(self.frame_plot_controls)
        self.label_linear_2.setObjectName(u"label_linear_2")
        self.label_linear_2.setMinimumSize(QSize(100, 28))
        self.label_linear_2.setMaximumSize(QSize(110, 28))
        font2 = QFont()
        font2.setPointSize(10)
        font2.setBold(False)
        self.label_linear_2.setFont(font2)
        self.label_linear_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_linear_2, 1, 1, 1, 1)

        self.label_animation_time_unit = QLabel(self.frame_plot_controls)
        self.label_animation_time_unit.setObjectName(u"label_animation_time_unit")
        self.label_animation_time_unit.setMinimumSize(QSize(0, 0))
        self.label_animation_time_unit.setMaximumSize(QSize(28, 16777215))
        self.label_animation_time_unit.setFont(font1)

        self.gridLayout_4.addWidget(self.label_animation_time_unit, 3, 3, 1, 1)

        self.label_7 = QLabel(self.frame_plot_controls)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(100, 28))
        self.label_7.setMaximumSize(QSize(110, 28))
        font3 = QFont()
        font3.setFamilies([u"MS Shell Dlg 2"])
        font3.setPointSize(10)
        font3.setBold(False)
        self.label_7.setFont(font3)
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_7, 0, 1, 1, 1)

        self.comboBox_plotting_results = QComboBox(self.frame_plot_controls)
        self.comboBox_plotting_results.addItem("")
        self.comboBox_plotting_results.addItem("")
        self.comboBox_plotting_results.addItem("")
        self.comboBox_plotting_results.addItem("")
        self.comboBox_plotting_results.addItem("")
        self.comboBox_plotting_results.addItem("")
        self.comboBox_plotting_results.addItem("")
        self.comboBox_plotting_results.addItem("")
        self.comboBox_plotting_results.addItem("")
        self.comboBox_plotting_results.addItem("")
        self.comboBox_plotting_results.addItem("")
        self.comboBox_plotting_results.setObjectName(u"comboBox_plotting_results")
        self.comboBox_plotting_results.setMinimumSize(QSize(180, 28))
        self.comboBox_plotting_results.setMaximumSize(QSize(180, 28))
        self.comboBox_plotting_results.setSizeIncrement(QSize(0, 0))
        self.comboBox_plotting_results.setFont(font1)

        self.gridLayout_4.addWidget(self.comboBox_plotting_results, 0, 2, 1, 1)

        self.label = QLabel(self.frame_plot_controls)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(100, 28))
        self.label.setMaximumSize(QSize(110, 28))
        self.label.setFont(font1)
        self.label.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_4.addWidget(self.label, 4, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer, 3, 4, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_2, 3, 0, 1, 1)


        self.gridLayout_5.addWidget(self.frame_plot_controls, 1, 0, 1, 1)

        self.frame_3 = QFrame(self.frame_main)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(0, 52))
        self.frame_3.setMaximumSize(QSize(16777215, 52))
        self.frame_3.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_47 = QGridLayout(self.frame_3)
        self.gridLayout_47.setSpacing(2)
        self.gridLayout_47.setObjectName(u"gridLayout_47")
        self.gridLayout_47.setContentsMargins(2, 2, 2, 2)
        self.pushButton_process_nodal_stresses = QPushButton(self.frame_3)
        self.pushButton_process_nodal_stresses.setObjectName(u"pushButton_process_nodal_stresses")
        self.pushButton_process_nodal_stresses.setMinimumSize(QSize(160, 32))
        self.pushButton_process_nodal_stresses.setMaximumSize(QSize(180, 32))
        self.pushButton_process_nodal_stresses.setFont(font1)
        self.pushButton_process_nodal_stresses.setStyleSheet(u"")
        self.pushButton_process_nodal_stresses.setFlat(False)

        self.gridLayout_47.addWidget(self.pushButton_process_nodal_stresses, 0, 0, 1, 1)


        self.gridLayout_5.addWidget(self.frame_3, 0, 0, 1, 1)


        self.gridLayout_6.addWidget(self.frame_main, 1, 0, 1, 1)

        self.frame_animation = QFrame(self.scrollAreaWidgetContents)
        self.frame_animation.setObjectName(u"frame_animation")
        self.frame_animation.setMinimumSize(QSize(0, 228))
        self.frame_animation.setFrameShape(QFrame.Shape.Box)
        self.frame_animation.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_6.addWidget(self.frame_animation, 2, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_2.addWidget(self.scrollArea, 0, 0, 1, 1)


        self.retranslateUi(Form)

        self.comboBox_stress_units.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Plot stress field", None))
        self.label_title.setText(QCoreApplication.translate("Form", u"Stress field plot (frequency domain)", None))
        self.comboBox_reduced_time.setItemText(0, QCoreApplication.translate("Form", u"Disabled", None))
        self.comboBox_reduced_time.setItemText(1, QCoreApplication.translate("Form", u"User-defined", None))
        self.comboBox_reduced_time.setItemText(2, QCoreApplication.translate("Form", u"Rotational speed", None))

        self.comboBox_stress_units.setItemText(0, QCoreApplication.translate("Form", u"MPa", None))
        self.comboBox_stress_units.setItemText(1, QCoreApplication.translate("Form", u"kPa", None))
        self.comboBox_stress_units.setItemText(2, QCoreApplication.translate("Form", u"Pa", None))
        self.comboBox_stress_units.setItemText(3, QCoreApplication.translate("Form", u"ksi", None))
        self.comboBox_stress_units.setItemText(4, QCoreApplication.translate("Form", u"psi", None))
        self.comboBox_stress_units.setItemText(5, QCoreApplication.translate("Form", u"N/m\u00b2", None))

        self.label_reduced_time.setText(QCoreApplication.translate("Form", u"Reduced time:", None))
        self.label_animation_time.setText(QCoreApplication.translate("Form", u"Animation time:", None))
        self.comboBox_plot_type.setItemText(0, QCoreApplication.translate("Form", u"Non-absolute (animation)", None))
        self.comboBox_plot_type.setItemText(1, QCoreApplication.translate("Form", u"Absolute (animation)", None))

        self.label_linear_2.setText(QCoreApplication.translate("Form", u"Stress units:", None))
        self.label_animation_time_unit.setText(QCoreApplication.translate("Form", u"[s]", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"Plotting results:", None))
        self.comboBox_plotting_results.setItemText(0, QCoreApplication.translate("Form", u"Normal stress x", None))
        self.comboBox_plotting_results.setItemText(1, QCoreApplication.translate("Form", u"Normal stress y", None))
        self.comboBox_plotting_results.setItemText(2, QCoreApplication.translate("Form", u"Normal stress z", None))
        self.comboBox_plotting_results.setItemText(3, QCoreApplication.translate("Form", u"Shear stress xy", None))
        self.comboBox_plotting_results.setItemText(4, QCoreApplication.translate("Form", u"Shear stress xz", None))
        self.comboBox_plotting_results.setItemText(5, QCoreApplication.translate("Form", u"Shear stress yz", None))
        self.comboBox_plotting_results.setItemText(6, QCoreApplication.translate("Form", u"von Mises stress", None))
        self.comboBox_plotting_results.setItemText(7, QCoreApplication.translate("Form", u"Tresca stress", None))
        self.comboBox_plotting_results.setItemText(8, QCoreApplication.translate("Form", u"Max. principal stress 1", None))
        self.comboBox_plotting_results.setItemText(9, QCoreApplication.translate("Form", u"Max. principal stress 2", None))
        self.comboBox_plotting_results.setItemText(10, QCoreApplication.translate("Form", u"Max. principal stress 3", None))

        self.label.setText(QCoreApplication.translate("Form", u"Plot type:", None))
        self.pushButton_process_nodal_stresses.setText(QCoreApplication.translate("Form", u"Process nodal stresses", None))
    # retranslateUi



class StructuralStress3dPlotTimeInputs_UI(QWidget, Ui_Form):
    """
    Component Hierarchy:
    - Form: QWidget
        - (Layout): QGridLayout
                - scrollArea: QScrollArea
                    - scrollAreaWidgetContents: QWidget
                        - (Layout): QGridLayout
                                - frame_color: QFrame
                                - frame_title: QFrame
                                    - (Layout): QGridLayout
                                            - label_title: QLabel
                                - frame_main: QFrame
                                    - (Layout): QGridLayout
                                            - frame_plot_controls: QFrame
                                                - (Layout): QGridLayout
                                                        - comboBox_reduced_time: QComboBox
                                                        - comboBox_stress_units: QComboBox
                                                        - label_reduced_time: QLabel
                                                        - label_animation_time: QLabel
                                                        - lineEdit_animation_time: QLineEdit
                                                        - comboBox_plot_type: QComboBox
                                                        - label_linear_2: QLabel
                                                        - label_animation_time_unit: QLabel
                                                        - label_7: QLabel
                                                        - comboBox_plotting_results: QComboBox
                                                        - label: QLabel
                                            - frame_3: QFrame
                                                - (Layout): QGridLayout
                                                        - pushButton_process_nodal_stresses: QPushButton
                                - frame_animation: QFrame
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
