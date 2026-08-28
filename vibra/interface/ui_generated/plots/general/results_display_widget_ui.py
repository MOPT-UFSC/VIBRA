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
    QGridLayout, QLabel, QLineEdit, QSizePolicy,
    QSlider, QSpacerItem, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(368, 160)
        Form.setMinimumSize(QSize(0, 160))
        Form.setMaximumSize(QSize(16777215, 160))
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.frame_4 = QFrame(Form)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(0, 40))
        self.frame_4.setMaximumSize(QSize(16777215, 16777215))
        self.frame_4.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_15 = QGridLayout(self.frame_4)
        self.gridLayout_15.setSpacing(6)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.gridLayout_15.setContentsMargins(0, 0, 0, 0)
        self.min_color_check_box = QCheckBox(self.frame_4)
        self.min_color_check_box.setObjectName(u"min_color_check_box")

        self.gridLayout_15.addWidget(self.min_color_check_box, 3, 4, 1, 1)

        self.label_2 = QLabel(self.frame_4)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(120, 26))
        self.label_2.setMaximumSize(QSize(120, 26))
        font = QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setLineWidth(0)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_15.addWidget(self.label_2, 3, 1, 1, 1)

        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_15.addItem(self.horizontalSpacer_14, 2, 5, 1, 1)

        self.label_4 = QLabel(self.frame_4)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(120, 26))
        self.label_4.setMaximumSize(QSize(120, 26))
        self.label_4.setFont(font)
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_15.addWidget(self.label_4, 1, 1, 1, 1)

        self.horizontalSpacer_15 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_15.addItem(self.horizontalSpacer_15, 2, 0, 1, 1)

        self.label = QLabel(self.frame_4)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(120, 26))
        self.label.setMaximumSize(QSize(120, 26))
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_15.addWidget(self.label, 2, 1, 1, 1)

        self.label_3 = QLabel(self.frame_4)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(120, 26))
        self.label_3.setMaximumSize(QSize(120, 26))
        self.label_3.setFont(font)
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_15.addWidget(self.label_3, 0, 1, 1, 1)

        self.max_color_check_box = QCheckBox(self.frame_4)
        self.max_color_check_box.setObjectName(u"max_color_check_box")

        self.gridLayout_15.addWidget(self.max_color_check_box, 2, 4, 1, 1)

        self.comboBox_colormaps = QComboBox(self.frame_4)
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
        self.comboBox_colormaps.setMinimumSize(QSize(160, 26))
        self.comboBox_colormaps.setMaximumSize(QSize(160, 26))
        self.comboBox_colormaps.setFont(font)

        self.gridLayout_15.addWidget(self.comboBox_colormaps, 0, 2, 1, 1)

        self.slider_transparency = QSlider(self.frame_4)
        self.slider_transparency.setObjectName(u"slider_transparency")
        self.slider_transparency.setMinimumSize(QSize(160, 26))
        self.slider_transparency.setMaximumSize(QSize(160, 26))
        self.slider_transparency.setOrientation(Qt.Orientation.Horizontal)

        self.gridLayout_15.addWidget(self.slider_transparency, 1, 2, 1, 1)

        self.lineEdit_max_color_value = QLineEdit(self.frame_4)
        self.lineEdit_max_color_value.setObjectName(u"lineEdit_max_color_value")
        self.lineEdit_max_color_value.setEnabled(False)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_max_color_value.sizePolicy().hasHeightForWidth())
        self.lineEdit_max_color_value.setSizePolicy(sizePolicy)
        self.lineEdit_max_color_value.setMinimumSize(QSize(160, 26))
        self.lineEdit_max_color_value.setMaximumSize(QSize(160, 26))
        self.lineEdit_max_color_value.setFont(font)

        self.gridLayout_15.addWidget(self.lineEdit_max_color_value, 2, 2, 1, 1)

        self.lineEdit_min_color_value = QLineEdit(self.frame_4)
        self.lineEdit_min_color_value.setObjectName(u"lineEdit_min_color_value")
        self.lineEdit_min_color_value.setEnabled(False)
        sizePolicy.setHeightForWidth(self.lineEdit_min_color_value.sizePolicy().hasHeightForWidth())
        self.lineEdit_min_color_value.setSizePolicy(sizePolicy)
        self.lineEdit_min_color_value.setMinimumSize(QSize(160, 26))
        self.lineEdit_min_color_value.setMaximumSize(QSize(160, 26))
        self.lineEdit_min_color_value.setFont(font)

        self.gridLayout_15.addWidget(self.lineEdit_min_color_value, 3, 2, 1, 1)


        self.gridLayout.addWidget(self.frame_4, 0, 0, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.min_color_check_box.setText("")
#if QT_CONFIG(tooltip)
        self.label_2.setToolTip(QCoreApplication.translate("Form", u"Minimum colorbar value", None))
#endif // QT_CONFIG(tooltip)
        self.label_2.setText(QCoreApplication.translate("Form", u"Min. scale value:", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Transparency:", None))
#if QT_CONFIG(tooltip)
        self.label.setToolTip(QCoreApplication.translate("Form", u"Maximum colorbar value", None))
#endif // QT_CONFIG(tooltip)
        self.label.setText(QCoreApplication.translate("Form", u"Max. scale value:", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Colormaps:", None))
        self.max_color_check_box.setText("")
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

    # retranslateUi



class ResultsDisplayWidget_UI(QWidget, Ui_Form):
    """
    Component Hierarchy:
    - Form: QWidget
        - (Layout): QGridLayout
                - frame_4: QFrame
                    - (Layout): QGridLayout
                            - min_color_check_box: QCheckBox
                            - label_2: QLabel
                            - label_4: QLabel
                            - label: QLabel
                            - label_3: QLabel
                            - max_color_check_box: QCheckBox
                            - comboBox_colormaps: QComboBox
                            - slider_transparency: QSlider
                            - lineEdit_max_color_value: QLineEdit
                            - lineEdit_min_color_value: QLineEdit
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
