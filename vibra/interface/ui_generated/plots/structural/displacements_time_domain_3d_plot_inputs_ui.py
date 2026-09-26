# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'displacements_time_domain_3d_plot_inputs.ui'
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
        Form.resize(401, 756)
        Form.setMaximumSize(QSize(16777215, 1000))
        self.gridLayout_2 = QGridLayout(Form)
        self.gridLayout_2.setSpacing(2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(2, 2, 2, 2)
        self.scrollArea = QScrollArea(Form)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 397, 752))
        self.gridLayout_6 = QGridLayout(self.scrollAreaWidgetContents_2)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setHorizontalSpacing(2)
        self.gridLayout_6.setVerticalSpacing(4)
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.frame_color = QFrame(self.scrollAreaWidgetContents_2)
        self.frame_color.setObjectName(u"frame_color")
        self.frame_color.setMinimumSize(QSize(0, 168))
        self.frame_color.setMaximumSize(QSize(16777215, 168))
        self.frame_color.setFrameShape(QFrame.Shape.Box)
        self.frame_color.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_6.addWidget(self.frame_color, 3, 0, 1, 1)

        self.frame_main = QFrame(self.scrollAreaWidgetContents_2)
        self.frame_main.setObjectName(u"frame_main")
        self.frame_main.setMinimumSize(QSize(0, 180))
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
        self.frame_plot_controls.setMinimumSize(QSize(0, 120))
        self.frame_plot_controls.setMaximumSize(QSize(16777215, 300))
        self.frame_plot_controls.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_plot_controls.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_13 = QGridLayout(self.frame_plot_controls)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_13.setContentsMargins(0, 6, 0, 0)
        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_13.addItem(self.horizontalSpacer_14, 3, 0, 1, 1)

        self.label_7 = QLabel(self.frame_plot_controls)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(0, 28))
        self.label_7.setMaximumSize(QSize(16777215, 28))
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(10)
        font.setBold(False)
        self.label_7.setFont(font)
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_13.addWidget(self.label_7, 0, 1, 1, 1)

        self.label_color_scalling = QLabel(self.frame_plot_controls)
        self.label_color_scalling.setObjectName(u"label_color_scalling")
        self.label_color_scalling.setMinimumSize(QSize(110, 26))
        self.label_color_scalling.setMaximumSize(QSize(110, 26))
        font1 = QFont()
        font1.setPointSize(10)
        self.label_color_scalling.setFont(font1)
        self.label_color_scalling.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_13.addWidget(self.label_color_scalling, 1, 1, 1, 1)

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
        self.comboBox_plotting_results.setObjectName(u"comboBox_plotting_results")
        self.comboBox_plotting_results.setMinimumSize(QSize(160, 28))
        self.comboBox_plotting_results.setMaximumSize(QSize(180, 28))
        self.comboBox_plotting_results.setSizeIncrement(QSize(0, 0))
        self.comboBox_plotting_results.setFont(font1)

        self.gridLayout_13.addWidget(self.comboBox_plotting_results, 0, 3, 1, 1)

        self.label_animation_time_unit = QLabel(self.frame_plot_controls)
        self.label_animation_time_unit.setObjectName(u"label_animation_time_unit")
        self.label_animation_time_unit.setMinimumSize(QSize(40, 0))
        self.label_animation_time_unit.setMaximumSize(QSize(40, 16777215))
        self.label_animation_time_unit.setFont(font1)

        self.gridLayout_13.addWidget(self.label_animation_time_unit, 3, 4, 1, 1)

        self.comboBox_reduced_time = QComboBox(self.frame_plot_controls)
        self.comboBox_reduced_time.addItem("")
        self.comboBox_reduced_time.addItem("")
        self.comboBox_reduced_time.addItem("")
        self.comboBox_reduced_time.setObjectName(u"comboBox_reduced_time")
        self.comboBox_reduced_time.setMinimumSize(QSize(176, 26))
        self.comboBox_reduced_time.setMaximumSize(QSize(200, 26))
        self.comboBox_reduced_time.setFont(font1)

        self.gridLayout_13.addWidget(self.comboBox_reduced_time, 2, 3, 1, 1)

        self.label_animation_time = QLabel(self.frame_plot_controls)
        self.label_animation_time.setObjectName(u"label_animation_time")
        self.label_animation_time.setMinimumSize(QSize(110, 26))
        self.label_animation_time.setMaximumSize(QSize(110, 26))
        self.label_animation_time.setFont(font1)
        self.label_animation_time.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_13.addWidget(self.label_animation_time, 3, 1, 1, 1)

        self.label_reduced_time = QLabel(self.frame_plot_controls)
        self.label_reduced_time.setObjectName(u"label_reduced_time")
        self.label_reduced_time.setMinimumSize(QSize(110, 26))
        self.label_reduced_time.setMaximumSize(QSize(110, 26))
        self.label_reduced_time.setFont(font1)
        self.label_reduced_time.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_13.addWidget(self.label_reduced_time, 2, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_13.addItem(self.horizontalSpacer, 3, 5, 1, 1)

        self.lineEdit_animation_time = QLineEdit(self.frame_plot_controls)
        self.lineEdit_animation_time.setObjectName(u"lineEdit_animation_time")
        self.lineEdit_animation_time.setMinimumSize(QSize(0, 26))
        self.lineEdit_animation_time.setMaximumSize(QSize(16777215, 26))
        self.lineEdit_animation_time.setFont(font1)

        self.gridLayout_13.addWidget(self.lineEdit_animation_time, 3, 3, 1, 1)

        self.comboBox_plot_type = QComboBox(self.frame_plot_controls)
        self.comboBox_plot_type.addItem("")
        self.comboBox_plot_type.addItem("")
        self.comboBox_plot_type.addItem("")
        self.comboBox_plot_type.addItem("")
        self.comboBox_plot_type.setObjectName(u"comboBox_plot_type")
        self.comboBox_plot_type.setMinimumSize(QSize(176, 26))
        self.comboBox_plot_type.setMaximumSize(QSize(200, 26))
        self.comboBox_plot_type.setFont(font1)

        self.gridLayout_13.addWidget(self.comboBox_plot_type, 1, 3, 1, 1)


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
        self.pushButton_process_nodal_solution_iffts = QPushButton(self.frame_3)
        self.pushButton_process_nodal_solution_iffts.setObjectName(u"pushButton_process_nodal_solution_iffts")
        self.pushButton_process_nodal_solution_iffts.setMinimumSize(QSize(200, 32))
        self.pushButton_process_nodal_solution_iffts.setMaximumSize(QSize(220, 32))
        self.pushButton_process_nodal_solution_iffts.setFont(font1)
        self.pushButton_process_nodal_solution_iffts.setStyleSheet(u"")
        self.pushButton_process_nodal_solution_iffts.setFlat(False)

        self.gridLayout_47.addWidget(self.pushButton_process_nodal_solution_iffts, 0, 0, 1, 1)


        self.gridLayout_5.addWidget(self.frame_3, 0, 0, 1, 1)


        self.gridLayout_6.addWidget(self.frame_main, 1, 0, 1, 1)

        self.frame = QFrame(self.scrollAreaWidgetContents_2)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 40))
        self.frame.setMaximumSize(QSize(16777215, 40))
        self.frame.setFrameShape(QFrame.Shape.Box)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.frame.setLineWidth(1)
        self.gridLayout = QGridLayout(self.frame)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(2, 0, -1, 0)
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(0, 0))
        self.label.setMaximumSize(QSize(16777215, 16777215))
        font2 = QFont()
        font2.setFamilies([u"Segoe UI"])
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        self.label.setFont(font2)
        self.label.setFrameShape(QFrame.Shape.NoFrame)
        self.label.setFrameShadow(QFrame.Shadow.Raised)
        self.label.setTextFormat(Qt.TextFormat.AutoText)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout_6.addWidget(self.frame, 0, 0, 1, 1)

        self.frame_animation = QFrame(self.scrollAreaWidgetContents_2)
        self.frame_animation.setObjectName(u"frame_animation")
        self.frame_animation.setMinimumSize(QSize(0, 228))
        self.frame_animation.setFrameShape(QFrame.Shape.Box)
        self.frame_animation.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_6.addWidget(self.frame_animation, 2, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)

        self.gridLayout_2.addWidget(self.scrollArea, 0, 0, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Plot pressure field", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"Plotting results:", None))
        self.label_color_scalling.setText(QCoreApplication.translate("Form", u"Plot type:", None))
        self.comboBox_plotting_results.setItemText(0, QCoreApplication.translate("Form", u"Displacement (m)", None))
        self.comboBox_plotting_results.setItemText(1, QCoreApplication.translate("Form", u"Velocity (m/s)", None))
        self.comboBox_plotting_results.setItemText(2, QCoreApplication.translate("Form", u"Acceleration (m/s\u00b2)", None))
        self.comboBox_plotting_results.setItemText(3, QCoreApplication.translate("Form", u"Displacement (mm)", None))
        self.comboBox_plotting_results.setItemText(4, QCoreApplication.translate("Form", u"Velocity (mm/s)", None))
        self.comboBox_plotting_results.setItemText(5, QCoreApplication.translate("Form", u"Acceleration (mm/s\u00b2)", None))
        self.comboBox_plotting_results.setItemText(6, QCoreApplication.translate("Form", u"Displacement (um)", None))
        self.comboBox_plotting_results.setItemText(7, QCoreApplication.translate("Form", u"Velocity (um/s)", None))
        self.comboBox_plotting_results.setItemText(8, QCoreApplication.translate("Form", u"Acceleration (um/s\u00b2)", None))

        self.label_animation_time_unit.setText(QCoreApplication.translate("Form", u"[s]", None))
        self.comboBox_reduced_time.setItemText(0, QCoreApplication.translate("Form", u"Disabled", None))
        self.comboBox_reduced_time.setItemText(1, QCoreApplication.translate("Form", u"User-defined", None))
        self.comboBox_reduced_time.setItemText(2, QCoreApplication.translate("Form", u"Rotational speed", None))

        self.label_animation_time.setText(QCoreApplication.translate("Form", u"Animation time:", None))
        self.label_reduced_time.setText(QCoreApplication.translate("Form", u"Reduced time:", None))
        self.comboBox_plot_type.setItemText(0, QCoreApplication.translate("Form", u"Sum", None))
        self.comboBox_plot_type.setItemText(1, QCoreApplication.translate("Form", u"Real Ux", None))
        self.comboBox_plot_type.setItemText(2, QCoreApplication.translate("Form", u"Real Uy", None))
        self.comboBox_plot_type.setItemText(3, QCoreApplication.translate("Form", u"Real Uz", None))

        self.pushButton_process_nodal_solution_iffts.setText(QCoreApplication.translate("Form", u"Process nodal solution (IFFTs)", None))
        self.label.setText(QCoreApplication.translate("Form", u"Displacements Field Plot (time domain)", None))
    # retranslateUi



class DisplacementsTimeDomain3dPlotInputs_UI(QWidget, Ui_Form):
    """
    Component Hierarchy:
    - Form: QWidget
        - (Layout): QGridLayout
                - scrollArea: QScrollArea
                    - scrollAreaWidgetContents_2: QWidget
                        - (Layout): QGridLayout
                                - frame_color: QFrame
                                - frame_main: QFrame
                                    - (Layout): QGridLayout
                                            - frame_plot_controls: QFrame
                                                - (Layout): QGridLayout
                                                        - label_7: QLabel
                                                        - label_color_scalling: QLabel
                                                        - comboBox_plotting_results: QComboBox
                                                        - label_animation_time_unit: QLabel
                                                        - comboBox_reduced_time: QComboBox
                                                        - label_animation_time: QLabel
                                                        - label_reduced_time: QLabel
                                                        - lineEdit_animation_time: QLineEdit
                                                        - comboBox_plot_type: QComboBox
                                            - frame_3: QFrame
                                                - (Layout): QGridLayout
                                                        - pushButton_process_nodal_solution_iffts: QPushButton
                                - frame: QFrame
                                    - (Layout): QGridLayout
                                            - label: QLabel
                                - frame_animation: QFrame
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
