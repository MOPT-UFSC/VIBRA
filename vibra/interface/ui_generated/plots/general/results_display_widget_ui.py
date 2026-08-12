# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'results_display_widget.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QGridLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSlider, QSpacerItem, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(400, 242)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.frame_4 = QFrame(Form)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(0, 40))
        self.frame_4.setMaximumSize(QSize(16777215, 40))
        self.frame_4.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_15 = QGridLayout(self.frame_4)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.gridLayout_15.setContentsMargins(0, 0, 0, 0)
        self.frame_8 = QFrame(self.frame_4)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setMinimumSize(QSize(176, 0))
        self.frame_8.setMaximumSize(QSize(176, 16777215))
        self.frame_8.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_8.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_16 = QGridLayout(self.frame_8)
        self.gridLayout_16.setSpacing(0)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.gridLayout_16.setContentsMargins(0, 0, 0, 0)
        self.comboBox_colormaps = QComboBox(self.frame_8)
        self.comboBox_colormaps.addItem("")
        self.comboBox_colormaps.addItem("")
        self.comboBox_colormaps.addItem("")
        self.comboBox_colormaps.addItem("")
        self.comboBox_colormaps.addItem("")
        self.comboBox_colormaps.addItem("")
        self.comboBox_colormaps.addItem("")
        self.comboBox_colormaps.addItem("")
        self.comboBox_colormaps.addItem("")
        self.comboBox_colormaps.addItem("")
        self.comboBox_colormaps.addItem("")
        self.comboBox_colormaps.setObjectName(u"comboBox_colormaps")
        self.comboBox_colormaps.setMinimumSize(QSize(120, 26))
        self.comboBox_colormaps.setMaximumSize(QSize(200, 26))
        font = QFont()
        font.setPointSize(10)
        self.comboBox_colormaps.setFont(font)

        self.gridLayout_16.addWidget(self.comboBox_colormaps, 0, 0, 1, 1)


        self.gridLayout_15.addWidget(self.frame_8, 0, 2, 1, 1)

        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_15.addItem(self.horizontalSpacer_14, 0, 3, 1, 1)

        self.label_3 = QLabel(self.frame_4)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(90, 26))
        self.label_3.setMaximumSize(QSize(90, 26))
        self.label_3.setFont(font)
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_15.addWidget(self.label_3, 0, 1, 1, 1)

        self.horizontalSpacer_15 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_15.addItem(self.horizontalSpacer_15, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_4, 0, 0, 1, 1)

        self.frame_2 = QFrame(Form)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(0, 40))
        self.frame_2.setMaximumSize(QSize(16777215, 40))
        self.frame_2.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_5, 0, 0, 1, 1)

        self.lineEdit_min_pressure = QLineEdit(self.frame_2)
        self.lineEdit_min_pressure.setObjectName(u"lineEdit_min_pressure")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_min_pressure.sizePolicy().hasHeightForWidth())
        self.lineEdit_min_pressure.setSizePolicy(sizePolicy)
        self.lineEdit_min_pressure.setMinimumSize(QSize(145, 0))
        self.lineEdit_min_pressure.setMaximumSize(QSize(200, 16777215))
        self.lineEdit_min_pressure.setFont(font)

        self.gridLayout_3.addWidget(self.lineEdit_min_pressure, 0, 2, 1, 1)

        self.min_pressure_check_box = QCheckBox(self.frame_2)
        self.min_pressure_check_box.setObjectName(u"min_pressure_check_box")

        self.gridLayout_3.addWidget(self.min_pressure_check_box, 0, 3, 1, 1)

        self.label_2 = QLabel(self.frame_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(90, 26))
        self.label_2.setMaximumSize(QSize(90, 26))
        self.label_2.setFont(font)
        self.label_2.setLineWidth(0)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_2, 0, 1, 1, 1)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_10, 0, 4, 1, 1)


        self.gridLayout.addWidget(self.frame_2, 3, 0, 1, 1)

        self.frame_transparency = QFrame(Form)
        self.frame_transparency.setObjectName(u"frame_transparency")
        self.frame_transparency.setMinimumSize(QSize(0, 40))
        self.frame_transparency.setMaximumSize(QSize(16777215, 40))
        self.frame_transparency.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_transparency.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_10 = QGridLayout(self.frame_transparency)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(0, 0, 0, 0)
        self.label_4 = QLabel(self.frame_transparency)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(90, 26))
        self.label_4.setMaximumSize(QSize(90, 26))
        self.label_4.setFont(font)
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_4, 0, 1, 1, 1)

        self.slider_transparency = QSlider(self.frame_transparency)
        self.slider_transparency.setObjectName(u"slider_transparency")
        self.slider_transparency.setMinimumSize(QSize(176, 0))
        self.slider_transparency.setMaximumSize(QSize(200, 16777215))
        self.slider_transparency.setOrientation(Qt.Orientation.Horizontal)

        self.gridLayout_10.addWidget(self.slider_transparency, 0, 2, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_10.addItem(self.horizontalSpacer_8, 0, 3, 1, 1)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_10.addItem(self.horizontalSpacer_9, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_transparency, 1, 0, 1, 1)

        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 40))
        self.frame.setMaximumSize(QSize(16777215, 40))
        self.frame.setFrameShape(QFrame.Shape.NoFrame)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_4, 0, 4, 1, 1)

        self.max_pressure_check_box = QCheckBox(self.frame)
        self.max_pressure_check_box.setObjectName(u"max_pressure_check_box")

        self.gridLayout_2.addWidget(self.max_pressure_check_box, 0, 3, 1, 1)

        self.lineEdit_max_pressure = QLineEdit(self.frame)
        self.lineEdit_max_pressure.setObjectName(u"lineEdit_max_pressure")
        sizePolicy.setHeightForWidth(self.lineEdit_max_pressure.sizePolicy().hasHeightForWidth())
        self.lineEdit_max_pressure.setSizePolicy(sizePolicy)
        self.lineEdit_max_pressure.setMinimumSize(QSize(145, 0))
        self.lineEdit_max_pressure.setMaximumSize(QSize(200, 16777215))
        self.lineEdit_max_pressure.setFont(font)

        self.gridLayout_2.addWidget(self.lineEdit_max_pressure, 0, 2, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_3, 0, 0, 1, 1)

        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(90, 26))
        self.label.setMaximumSize(QSize(90, 26))
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label, 0, 1, 1, 1)


        self.gridLayout.addWidget(self.frame, 2, 0, 1, 1)

        self.frame_3 = QFrame(Form)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(0, 40))
        self.frame_3.setMaximumSize(QSize(16777215, 40))
        self.frame_3.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_3)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.pushButton_reset_pressures = QPushButton(self.frame_3)
        self.pushButton_reset_pressures.setObjectName(u"pushButton_reset_pressures")
        self.pushButton_reset_pressures.setMinimumSize(QSize(110, 26))
        self.pushButton_reset_pressures.setMaximumSize(QSize(140, 16777215))
        self.pushButton_reset_pressures.setFont(font)

        self.gridLayout_4.addWidget(self.pushButton_reset_pressures, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_3, 4, 0, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.comboBox_colormaps.setItemText(0, QCoreApplication.translate("Form", u" Jet scale", None))
        self.comboBox_colormaps.setItemText(1, QCoreApplication.translate("Form", u" Viridis scale", None))
        self.comboBox_colormaps.setItemText(2, QCoreApplication.translate("Form", u" Inferno scale", None))
        self.comboBox_colormaps.setItemText(3, QCoreApplication.translate("Form", u" Magma scale", None))
        self.comboBox_colormaps.setItemText(4, QCoreApplication.translate("Form", u" Plasma scale", None))
        self.comboBox_colormaps.setItemText(5, QCoreApplication.translate("Form", u"BWR diverging scale", None))
        self.comboBox_colormaps.setItemText(6, QCoreApplication.translate("Form", u"PiYG diverging scale", None))
        self.comboBox_colormaps.setItemText(7, QCoreApplication.translate("Form", u"PRGn diverging scale", None))
        self.comboBox_colormaps.setItemText(8, QCoreApplication.translate("Form", u"BrBG diverging scale", None))
        self.comboBox_colormaps.setItemText(9, QCoreApplication.translate("Form", u"PuOr diverging scale", None))
        self.comboBox_colormaps.setItemText(10, QCoreApplication.translate("Form", u" Grayscale", None))

        self.label_3.setText(QCoreApplication.translate("Form", u"Colormaps:", None))
        self.min_pressure_check_box.setText(QCoreApplication.translate("Form", u"[Pa]", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Min pressure:", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Transparency:", None))
        self.max_pressure_check_box.setText(QCoreApplication.translate("Form", u"[Pa]", None))
        self.label.setText(QCoreApplication.translate("Form", u"Max pressure:", None))
        self.pushButton_reset_pressures.setText(QCoreApplication.translate("Form", u"Reset pressures", None))
    # retranslateUi



class ResultsDisplayWidget_UI(QWidget, Ui_Form):
    """
    Component Hierarchy:
    - Form: QWidget
        - (Layout): QGridLayout
                - frame_4: QFrame
                    - (Layout): QGridLayout
                            - frame_8: QFrame
                                - (Layout): QGridLayout
                                        - comboBox_colormaps: QComboBox
                            - label_3: QLabel
                - frame_2: QFrame
                    - (Layout): QGridLayout
                            - lineEdit_min_pressure: QLineEdit
                            - min_pressure_check_box: QCheckBox
                            - label_2: QLabel
                - frame_transparency: QFrame
                    - (Layout): QGridLayout
                            - label_4: QLabel
                            - slider_transparency: QSlider
                - frame: QFrame
                    - (Layout): QGridLayout
                            - max_pressure_check_box: QCheckBox
                            - lineEdit_max_pressure: QLineEdit
                            - label: QLabel
                - frame_3: QFrame
                    - (Layout): QGridLayout
                            - pushButton_reset_pressures: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
