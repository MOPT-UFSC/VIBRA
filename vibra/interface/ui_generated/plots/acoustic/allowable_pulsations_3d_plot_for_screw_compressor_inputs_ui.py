# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'allowable_pulsations_3d_plot_for_screw_compressor_inputs.ui'
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
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(378, 789)
        Form.setMinimumSize(QSize(0, 200))
        self.gridLayout_4 = QGridLayout(Form)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setVerticalSpacing(4)
        self.gridLayout_4.setContentsMargins(4, 4, 4, 4)
        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 40))
        self.frame.setMaximumSize(QSize(520, 40))
        self.frame.setFrameShape(QFrame.Shape.Box)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.frame.setLineWidth(1)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(0, 30))
        self.label.setMaximumSize(QSize(452, 30))
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        self.label.setFont(font)
        self.label.setTextFormat(Qt.TextFormat.AutoText)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout_4.addWidget(self.frame, 0, 0, 1, 1)

        self.frame_main = QFrame(Form)
        self.frame_main.setObjectName(u"frame_main")
        self.frame_main.setMinimumSize(QSize(0, 120))
        self.frame_main.setMaximumSize(QSize(16777215, 240))
        self.frame_main.setSizeIncrement(QSize(0, 0))
        self.frame_main.setBaseSize(QSize(0, 0))
        self.frame_main.setFrameShape(QFrame.Shape.Box)
        self.frame_main.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_8 = QGridLayout(self.frame_main)
        self.gridLayout_8.setSpacing(4)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(4, 4, 4, 4)
        self.frame_5 = QFrame(self.frame_main)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setMinimumSize(QSize(0, 0))
        self.frame_5.setMaximumSize(QSize(16777215, 48))
        self.frame_5.setSizeIncrement(QSize(0, 0))
        self.frame_5.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_7 = QGridLayout(self.frame_5)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(2, 2, 2, 2)
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_4, 0, 0, 1, 1)

        self.label_8 = QLabel(self.frame_5)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMinimumSize(QSize(0, 28))
        self.label_8.setMaximumSize(QSize(16777215, 28))
        font1 = QFont()
        font1.setPointSize(10)
        self.label_8.setFont(font1)
        self.label_8.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_8, 0, 4, 1, 1)

        self.label_penalization_factor = QLabel(self.frame_5)
        self.label_penalization_factor.setObjectName(u"label_penalization_factor")
        self.label_penalization_factor.setMinimumSize(QSize(0, 28))
        self.label_penalization_factor.setMaximumSize(QSize(140, 28))
        self.label_penalization_factor.setFont(font1)
        self.label_penalization_factor.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_penalization_factor, 0, 1, 1, 1)

        self.comboBox_penalization_factor = QComboBox(self.frame_5)
        self.comboBox_penalization_factor.setObjectName(u"comboBox_penalization_factor")
        self.comboBox_penalization_factor.setMinimumSize(QSize(120, 28))
        self.comboBox_penalization_factor.setMaximumSize(QSize(120, 28))

        self.gridLayout_7.addWidget(self.comboBox_penalization_factor, 0, 2, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_5, 0, 5, 1, 1)


        self.gridLayout_8.addWidget(self.frame_5, 0, 1, 1, 1)

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
        self.pushButton_plot_criterion = QPushButton(self.frame_3)
        self.pushButton_plot_criterion.setObjectName(u"pushButton_plot_criterion")
        self.pushButton_plot_criterion.setMinimumSize(QSize(100, 32))
        self.pushButton_plot_criterion.setMaximumSize(QSize(140, 32))
        self.pushButton_plot_criterion.setFont(font1)
        self.pushButton_plot_criterion.setStyleSheet(u"")
        self.pushButton_plot_criterion.setFlat(False)

        self.gridLayout_47.addWidget(self.pushButton_plot_criterion, 1, 0, 1, 1)


        self.gridLayout_8.addWidget(self.frame_3, 2, 1, 1, 1)


        self.gridLayout_4.addWidget(self.frame_main, 2, 0, 1, 1)

        self.frame_color = QFrame(Form)
        self.frame_color.setObjectName(u"frame_color")
        self.frame_color.setMinimumSize(QSize(0, 168))
        self.frame_color.setMaximumSize(QSize(16777215, 168))
        self.frame_color.setFrameShape(QFrame.Shape.Box)
        self.frame_color.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_4.addWidget(self.frame_color, 3, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_4.addItem(self.verticalSpacer, 4, 0, 1, 1)

        self.frame_ifft_controls = QFrame(Form)
        self.frame_ifft_controls.setObjectName(u"frame_ifft_controls")
        self.frame_ifft_controls.setMinimumSize(QSize(0, 120))
        self.frame_ifft_controls.setFrameShape(QFrame.Shape.Box)
        self.frame_ifft_controls.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_4.addWidget(self.frame_ifft_controls, 1, 0, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"Allowable pulsations field plot for screw compressors", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"[%]", None))
        self.label_penalization_factor.setText(QCoreApplication.translate("Form", u"Penalization factor:", None))
        self.pushButton_plot_criterion.setText(QCoreApplication.translate("Form", u"Plot criterion", None))
    # retranslateUi



class AllowablePulsations3dPlotForScrewCompressorInputs_UI(QWidget, Ui_Form):
    """
    Component Hierarchy:
    - Form: QWidget
        - (Layout): QGridLayout
                - frame: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
                - frame_main: QFrame
                    - (Layout): QGridLayout
                            - frame_5: QFrame
                                - (Layout): QGridLayout
                                        - label_8: QLabel
                                        - label_penalization_factor: QLabel
                                        - comboBox_penalization_factor: QComboBox
                            - frame_3: QFrame
                                - (Layout): QGridLayout
                                        - pushButton_plot_criterion: QPushButton
                - frame_color: QFrame
                - frame_ifft_controls: QFrame
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
