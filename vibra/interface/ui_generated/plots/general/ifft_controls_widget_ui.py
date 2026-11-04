# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ifft_controls_widget.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QLabel,
    QLineEdit, QSizePolicy, QSpacerItem, QSpinBox,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(340, 120)
        Form.setMinimumSize(QSize(0, 120))
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(2, 6, 2, 6)
        self.lineEdit_frequency_resolution = QLineEdit(Form)
        self.lineEdit_frequency_resolution.setObjectName(u"lineEdit_frequency_resolution")
        self.lineEdit_frequency_resolution.setEnabled(True)
        self.lineEdit_frequency_resolution.setMinimumSize(QSize(100, 28))
        self.lineEdit_frequency_resolution.setMaximumSize(QSize(160, 28))
        font = QFont()
        font.setPointSize(10)
        self.lineEdit_frequency_resolution.setFont(font)
        self.lineEdit_frequency_resolution.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_frequency_resolution, 2, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 3, 0, 1, 1)

        self.lineEdit_maximum_frequency = QLineEdit(Form)
        self.lineEdit_maximum_frequency.setObjectName(u"lineEdit_maximum_frequency")
        self.lineEdit_maximum_frequency.setEnabled(True)
        self.lineEdit_maximum_frequency.setMinimumSize(QSize(100, 28))
        self.lineEdit_maximum_frequency.setMaximumSize(QSize(160, 28))
        self.lineEdit_maximum_frequency.setFont(font)
        self.lineEdit_maximum_frequency.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_maximum_frequency, 3, 2, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_5, 3, 4, 1, 1)

        self.label_reduced_time_6 = QLabel(Form)
        self.label_reduced_time_6.setObjectName(u"label_reduced_time_6")
        self.label_reduced_time_6.setMinimumSize(QSize(0, 28))
        self.label_reduced_time_6.setMaximumSize(QSize(16777215, 28))
        self.label_reduced_time_6.setFont(font)
        self.label_reduced_time_6.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_reduced_time_6, 3, 1, 1, 1)

        self.label_animation_time_unit_4 = QLabel(Form)
        self.label_animation_time_unit_4.setObjectName(u"label_animation_time_unit_4")
        self.label_animation_time_unit_4.setMinimumSize(QSize(40, 0))
        self.label_animation_time_unit_4.setMaximumSize(QSize(40, 16777215))
        self.label_animation_time_unit_4.setFont(font)

        self.gridLayout.addWidget(self.label_animation_time_unit_4, 3, 3, 1, 1)

        self.label_reduced_time_5 = QLabel(Form)
        self.label_reduced_time_5.setObjectName(u"label_reduced_time_5")
        self.label_reduced_time_5.setMinimumSize(QSize(0, 28))
        self.label_reduced_time_5.setMaximumSize(QSize(130, 28))
        self.label_reduced_time_5.setFont(font)
        self.label_reduced_time_5.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_reduced_time_5, 2, 1, 1, 1)

        self.checkBox_control_frequency_resolution = QCheckBox(Form)
        self.checkBox_control_frequency_resolution.setObjectName(u"checkBox_control_frequency_resolution")
        self.checkBox_control_frequency_resolution.setFont(font)
        self.checkBox_control_frequency_resolution.setIconSize(QSize(22, 22))
        self.checkBox_control_frequency_resolution.setChecked(True)

        self.gridLayout.addWidget(self.checkBox_control_frequency_resolution, 1, 3, 1, 1)

        self.label_reduced_time_4 = QLabel(Form)
        self.label_reduced_time_4.setObjectName(u"label_reduced_time_4")
        self.label_reduced_time_4.setMinimumSize(QSize(0, 28))
        self.label_reduced_time_4.setMaximumSize(QSize(130, 28))
        self.label_reduced_time_4.setFont(font)
        self.label_reduced_time_4.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_reduced_time_4, 1, 1, 1, 1)

        self.label_animation_time_unit_3 = QLabel(Form)
        self.label_animation_time_unit_3.setObjectName(u"label_animation_time_unit_3")
        self.label_animation_time_unit_3.setMinimumSize(QSize(40, 0))
        self.label_animation_time_unit_3.setMaximumSize(QSize(40, 16777215))
        self.label_animation_time_unit_3.setFont(font)

        self.gridLayout.addWidget(self.label_animation_time_unit_3, 2, 3, 1, 1)

        self.spinBox_intervals_number = QSpinBox(Form)
        self.spinBox_intervals_number.setObjectName(u"spinBox_intervals_number")
        self.spinBox_intervals_number.setMinimumSize(QSize(100, 28))
        self.spinBox_intervals_number.setMaximumSize(QSize(160, 28))
        self.spinBox_intervals_number.setFont(font)
        self.spinBox_intervals_number.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spinBox_intervals_number.setMinimum(1)
        self.spinBox_intervals_number.setMaximum(200)
        self.spinBox_intervals_number.setSingleStep(1)
        self.spinBox_intervals_number.setValue(30)

        self.gridLayout.addWidget(self.spinBox_intervals_number, 1, 2, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_frequency_resolution.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>The frequency resolution considered in IFFT processing. It is equivalent to f<span style=\" font-size:12pt; vertical-align:sub;\">step</span> / N<span style=\" font-size:12pt; vertical-align:sub;\">div</span>.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.lineEdit_maximum_frequency.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>The maximum frequency value of the spectrum, where f<span style=\" font-size:12pt; vertical-align:sub;\">s</span> = 2 * f<span style=\" font-size:12pt; vertical-align:sub;\">max</span>.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_reduced_time_6.setText(QCoreApplication.translate("Form", u"<html><head/><body><p>F<span style=\" font-size:12pt; vertical-align:sub;\">max</span> (ifft):</p></body></html>", None))
        self.label_animation_time_unit_4.setText(QCoreApplication.translate("Form", u"[Hz]", None))
        self.label_reduced_time_5.setText(QCoreApplication.translate("Form", u"<html><head/><body><p>&Delta;f (ifft):</p></body></html>", None))
        self.checkBox_control_frequency_resolution.setText("")
        self.label_reduced_time_4.setText(QCoreApplication.translate("Form", u"<html><head/><body><p>N<span style=\" font-size:12pt; vertical-align:sub;\">div</span> (ifft):</p></body></html>", None))
        self.label_animation_time_unit_3.setText(QCoreApplication.translate("Form", u"[Hz]", None))
#if QT_CONFIG(tooltip)
        self.spinBox_intervals_number.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>The number of zero-amplitude subdivision spectral lines between two consecutive solution steps, used to virtually regenerate a complete spectrum for IFFT processing.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(whatsthis)
        self.spinBox_intervals_number.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
    # retranslateUi



class IfftControlsWidget_UI(QWidget, Ui_Form):
    """
    Component Hierarchy:
    - Form: QWidget
        - (Layout): QGridLayout
                - lineEdit_frequency_resolution: QLineEdit
                - lineEdit_maximum_frequency: QLineEdit
                - label_reduced_time_6: QLabel
                - label_animation_time_unit_4: QLabel
                - label_reduced_time_5: QLabel
                - checkBox_control_frequency_resolution: QCheckBox
                - label_reduced_time_4: QLabel
                - label_animation_time_unit_3: QLabel
                - spinBox_intervals_number: QSpinBox
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
