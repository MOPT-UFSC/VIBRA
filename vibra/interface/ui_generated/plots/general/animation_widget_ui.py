# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'animation_widget.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QLabel,
    QPushButton, QSizePolicy, QSlider, QSpacerItem,
    QSpinBox, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(367, 228)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(2, 2, 2, 2)
        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        self.frame.setMaximumSize(QSize(16777215, 16777215))
        self.frame.setFrameShape(QFrame.Shape.NoFrame)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.pushButton_export_animation = QPushButton(self.frame)
        self.pushButton_export_animation.setObjectName(u"pushButton_export_animation")
        self.pushButton_export_animation.setMinimumSize(QSize(0, 30))
        self.pushButton_export_animation.setMaximumSize(QSize(140, 16777215))
        self.pushButton_export_animation.setIconSize(QSize(20, 20))

        self.gridLayout_2.addWidget(self.pushButton_export_animation, 0, 0, 1, 1)

        self.pushButton_play_animation = QPushButton(self.frame)
        self.pushButton_play_animation.setObjectName(u"pushButton_play_animation")
        self.pushButton_play_animation.setMinimumSize(QSize(0, 30))
        self.pushButton_play_animation.setMaximumSize(QSize(140, 16777215))
        self.pushButton_play_animation.setIconSize(QSize(20, 20))

        self.gridLayout_2.addWidget(self.pushButton_play_animation, 0, 1, 1, 1)


        self.gridLayout.addWidget(self.frame, 2, 0, 1, 2)

        self.frame_2 = QFrame(Form)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMaximumSize(QSize(16777215, 16777215))
        self.frame_2.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(6, 6, 6, 6)
        self.label_animation_phase = QLabel(self.frame_2)
        self.label_animation_phase.setObjectName(u"label_animation_phase")
        self.label_animation_phase.setMinimumSize(QSize(0, 30))
        self.label_animation_phase.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_animation_phase, 0, 0, 1, 1)

        self.phase_slider = QSlider(self.frame_2)
        self.phase_slider.setObjectName(u"phase_slider")
        self.phase_slider.setMinimumSize(QSize(0, 0))
        self.phase_slider.setOrientation(Qt.Orientation.Horizontal)

        self.gridLayout_3.addWidget(self.phase_slider, 0, 1, 1, 1)

        self.label_phase_angle = QLabel(self.frame_2)
        self.label_phase_angle.setObjectName(u"label_phase_angle")
        self.label_phase_angle.setMinimumSize(QSize(0, 30))

        self.gridLayout_3.addWidget(self.label_phase_angle, 0, 2, 1, 1)

        self.label_magnification_factor = QLabel(self.frame_2)
        self.label_magnification_factor.setObjectName(u"label_magnification_factor")
        self.label_magnification_factor.setMinimumSize(QSize(0, 30))
        self.label_magnification_factor.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_magnification_factor, 1, 0, 1, 1)

        self.magnification_factor_slider = QSlider(self.frame_2)
        self.magnification_factor_slider.setObjectName(u"magnification_factor_slider")
        self.magnification_factor_slider.setMinimumSize(QSize(0, 0))
        self.magnification_factor_slider.setMaximum(2)
        self.magnification_factor_slider.setValue(1)
        self.magnification_factor_slider.setOrientation(Qt.Orientation.Horizontal)

        self.gridLayout_3.addWidget(self.magnification_factor_slider, 1, 1, 1, 1)

        self.label_factor = QLabel(self.frame_2)
        self.label_factor.setObjectName(u"label_factor")
        self.label_factor.setMinimumSize(QSize(0, 30))

        self.gridLayout_3.addWidget(self.label_factor, 1, 2, 1, 1)


        self.gridLayout.addWidget(self.frame_2, 1, 0, 1, 2)

        self.frame_3 = QFrame(Form)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_3)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(6, 6, 6, 6)
        self.horizontalSpacer_2 = QSpacerItem(79, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_2, 0, 0, 1, 1)

        self.label = QLabel(self.frame_3)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_4.addWidget(self.label, 0, 1, 1, 1)

        self.spinBox_frames = QSpinBox(self.frame_3)
        self.spinBox_frames.setObjectName(u"spinBox_frames")
        self.spinBox_frames.setMinimumSize(QSize(0, 30))
        self.spinBox_frames.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spinBox_frames.setMinimum(20)
        self.spinBox_frames.setMaximum(60)
        self.spinBox_frames.setSingleStep(10)
        self.spinBox_frames.setValue(40)

        self.gridLayout_4.addWidget(self.spinBox_frames, 0, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer, 0, 3, 1, 1)

        self.label_2 = QLabel(self.frame_3)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_2, 1, 1, 1, 1)

        self.spinBox_cycles = QSpinBox(self.frame_3)
        self.spinBox_cycles.setObjectName(u"spinBox_cycles")
        self.spinBox_cycles.setMinimumSize(QSize(0, 30))
        self.spinBox_cycles.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spinBox_cycles.setMaximum(20)
        self.spinBox_cycles.setValue(5)

        self.gridLayout_4.addWidget(self.spinBox_cycles, 1, 2, 1, 1)


        self.gridLayout.addWidget(self.frame_3, 0, 0, 1, 2)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.pushButton_export_animation.setText(QCoreApplication.translate("Form", u"Export animation", None))
        self.pushButton_play_animation.setText(QCoreApplication.translate("Form", u"Play animation", None))
        self.label_animation_phase.setText(QCoreApplication.translate("Form", u"Animation phase:", None))
        self.label_phase_angle.setText(QCoreApplication.translate("Form", u"(0\u00ba)", None))
        self.label_magnification_factor.setText(QCoreApplication.translate("Form", u"Magnification factor:", None))
        self.label_factor.setText(QCoreApplication.translate("Form", u"(1.0x)", None))
        self.label.setText(QCoreApplication.translate("Form", u"Frames per cycle:", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Animation cycles:", None))
    # retranslateUi



class AnimationWidget_UI(QWidget, Ui_Form):
    """
    Component Hierarchy:
    - Form: QWidget
        - (Layout): QGridLayout
                - frame: QFrame
                    - (Layout): QGridLayout
                            - pushButton_export_animation: QPushButton
                            - pushButton_play_animation: QPushButton
                - frame_2: QFrame
                    - (Layout): QGridLayout
                            - label_animation_phase: QLabel
                            - phase_slider: QSlider
                            - label_phase_angle: QLabel
                            - label_magnification_factor: QLabel
                            - magnification_factor_slider: QSlider
                            - label_factor: QLabel
                - frame_3: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
                            - spinBox_frames: QSpinBox
                            - label_2: QLabel
                            - spinBox_cycles: QSpinBox
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
