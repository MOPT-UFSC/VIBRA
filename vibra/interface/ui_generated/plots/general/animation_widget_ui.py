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

from vibra.interface.formatters.icons import Icon

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(377, 220)
        Form.setMinimumSize(QSize(0, 220))
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setVerticalSpacing(2)
        self.gridLayout.setContentsMargins(2, 8, 2, 4)
        self.frame_bottom = QFrame(Form)
        self.frame_bottom.setObjectName(u"frame_bottom")
        self.frame_bottom.setMinimumSize(QSize(0, 48))
        self.frame_bottom.setMaximumSize(QSize(16777215, 48))
        self.frame_bottom.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_bottom.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_bottom)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(2, 2, 2, 2)
        self.pushButton_animate = QPushButton(self.frame_bottom)
        self.pushButton_animate.setObjectName(u"pushButton_animate")
        self.pushButton_animate.setMinimumSize(QSize(0, 30))
        self.pushButton_animate.setMaximumSize(QSize(140, 16777215))
        font = QFont()
        font.setPointSize(10)
        self.pushButton_animate.setFont(font)
        self.pushButton_animate.setIconSize(QSize(20, 20))

        self.gridLayout_2.addWidget(self.pushButton_animate, 1, 1, 1, 1)

        self.pushButton_export_video = QPushButton(self.frame_bottom)
        self.pushButton_export_video.setObjectName(u"pushButton_export_video")
        self.pushButton_export_video.setMinimumSize(QSize(0, 30))
        self.pushButton_export_video.setMaximumSize(QSize(140, 16777215))
        self.pushButton_export_video.setFont(font)
        self.pushButton_export_video.setIconSize(QSize(20, 20))

        self.gridLayout_2.addWidget(self.pushButton_export_video, 1, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_bottom, 4, 0, 1, 2)

        self.frame_top = QFrame(Form)
        self.frame_top.setObjectName(u"frame_top")
        self.frame_top.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_top.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_top)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(6, 2, 6, 2)
        self.spinBox_frames = QSpinBox(self.frame_top)
        self.spinBox_frames.setObjectName(u"spinBox_frames")
        self.spinBox_frames.setMinimumSize(QSize(80, 28))
        self.spinBox_frames.setMaximumSize(QSize(80, 28))
        self.spinBox_frames.setFont(font)
        self.spinBox_frames.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spinBox_frames.setMinimum(20)
        self.spinBox_frames.setMaximum(60)
        self.spinBox_frames.setSingleStep(10)
        self.spinBox_frames.setValue(40)

        self.gridLayout_4.addWidget(self.spinBox_frames, 0, 2, 1, 1)

        self.label_frames_cycle = QLabel(self.frame_top)
        self.label_frames_cycle.setObjectName(u"label_frames_cycle")
        self.label_frames_cycle.setMinimumSize(QSize(0, 28))
        self.label_frames_cycle.setMaximumSize(QSize(16777215, 28))
        self.label_frames_cycle.setFont(font)
        self.label_frames_cycle.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_frames_cycle, 0, 1, 1, 1)

        self.spinBox_cycles = QSpinBox(self.frame_top)
        self.spinBox_cycles.setObjectName(u"spinBox_cycles")
        self.spinBox_cycles.setMinimumSize(QSize(80, 28))
        self.spinBox_cycles.setMaximumSize(QSize(80, 28))
        self.spinBox_cycles.setFont(font)
        self.spinBox_cycles.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spinBox_cycles.setMaximum(20)
        self.spinBox_cycles.setValue(5)

        self.gridLayout_4.addWidget(self.spinBox_cycles, 1, 2, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(79, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_2, 1, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer, 1, 4, 1, 1)

        self.label_animation_cycles = QLabel(self.frame_top)
        self.label_animation_cycles.setObjectName(u"label_animation_cycles")
        self.label_animation_cycles.setMinimumSize(QSize(0, 28))
        self.label_animation_cycles.setMaximumSize(QSize(16777215, 28))
        self.label_animation_cycles.setFont(font)
        self.label_animation_cycles.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_animation_cycles, 1, 1, 1, 1)

        self.pushButton_animation_loop = QPushButton(self.frame_top)
        self.pushButton_animation_loop.setObjectName(u"pushButton_animation_loop")
        self.pushButton_animation_loop.setMinimumSize(QSize(40, 28))
        self.pushButton_animation_loop.setMaximumSize(QSize(16777215, 28))
        icon = Icon(u":/icons/circular_arrows_icon.png")
        self.pushButton_animation_loop.setIcon(icon)
        self.pushButton_animation_loop.setIconSize(QSize(22, 22))
        self.pushButton_animation_loop.setCheckable(False)

        self.gridLayout_4.addWidget(self.pushButton_animation_loop, 1, 3, 1, 1)


        self.gridLayout.addWidget(self.frame_top, 1, 0, 1, 2)

        self.frame_middle = QFrame(Form)
        self.frame_middle.setObjectName(u"frame_middle")
        self.frame_middle.setMaximumSize(QSize(16777215, 16777215))
        self.frame_middle.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_middle.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_middle)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(6, 2, 6, 2)
        self.label_phase_angle = QLabel(self.frame_middle)
        self.label_phase_angle.setObjectName(u"label_phase_angle")
        self.label_phase_angle.setMinimumSize(QSize(60, 26))
        self.label_phase_angle.setMaximumSize(QSize(16777215, 26))

        self.gridLayout_3.addWidget(self.label_phase_angle, 1, 2, 1, 1)

        self.magnification_factor_slider = QSlider(self.frame_middle)
        self.magnification_factor_slider.setObjectName(u"magnification_factor_slider")
        self.magnification_factor_slider.setMinimumSize(QSize(0, 0))
        self.magnification_factor_slider.setMaximum(2)
        self.magnification_factor_slider.setValue(1)
        self.magnification_factor_slider.setOrientation(Qt.Orientation.Horizontal)

        self.gridLayout_3.addWidget(self.magnification_factor_slider, 2, 1, 1, 1)

        self.label_factor = QLabel(self.frame_middle)
        self.label_factor.setObjectName(u"label_factor")
        self.label_factor.setMinimumSize(QSize(60, 26))
        self.label_factor.setMaximumSize(QSize(16777215, 26))

        self.gridLayout_3.addWidget(self.label_factor, 2, 2, 1, 1)

        self.label_animation_phase = QLabel(self.frame_middle)
        self.label_animation_phase.setObjectName(u"label_animation_phase")
        self.label_animation_phase.setMinimumSize(QSize(0, 26))
        self.label_animation_phase.setMaximumSize(QSize(16777215, 26))
        self.label_animation_phase.setFont(font)
        self.label_animation_phase.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_animation_phase, 1, 0, 1, 1)

        self.phase_slider = QSlider(self.frame_middle)
        self.phase_slider.setObjectName(u"phase_slider")
        self.phase_slider.setMinimumSize(QSize(0, 0))
        self.phase_slider.setOrientation(Qt.Orientation.Horizontal)

        self.gridLayout_3.addWidget(self.phase_slider, 1, 1, 1, 1)

        self.label_magnification_factor = QLabel(self.frame_middle)
        self.label_magnification_factor.setObjectName(u"label_magnification_factor")
        self.label_magnification_factor.setMinimumSize(QSize(0, 26))
        self.label_magnification_factor.setMaximumSize(QSize(16777215, 26))
        self.label_magnification_factor.setFont(font)
        self.label_magnification_factor.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_magnification_factor, 2, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_middle, 2, 0, 1, 2)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.pushButton_animate.setText(QCoreApplication.translate("Form", u"Animate", None))
        self.pushButton_export_video.setText(QCoreApplication.translate("Form", u"Export video", None))
        self.label_frames_cycle.setText(QCoreApplication.translate("Form", u"Frames / cycle:", None))
        self.label_animation_cycles.setText(QCoreApplication.translate("Form", u"Animation cycles:", None))
#if QT_CONFIG(tooltip)
        self.pushButton_animation_loop.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Loop the animation</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_animation_loop.setText("")
        self.label_phase_angle.setText(QCoreApplication.translate("Form", u"0\u00ba", None))
        self.label_factor.setText(QCoreApplication.translate("Form", u"1.0x", None))
        self.label_animation_phase.setText(QCoreApplication.translate("Form", u"Phase:", None))
        self.label_magnification_factor.setText(QCoreApplication.translate("Form", u"Magnification:", None))
    # retranslateUi



class AnimationWidget_UI(QWidget, Ui_Form):
    """
    Component Hierarchy:
    - Form: QWidget
        - (Layout): QGridLayout
                - frame_bottom: QFrame
                    - (Layout): QGridLayout
                            - pushButton_animate: QPushButton
                            - pushButton_export_video: QPushButton
                - frame_top: QFrame
                    - (Layout): QGridLayout
                            - spinBox_frames: QSpinBox
                            - label_frames_cycle: QLabel
                            - spinBox_cycles: QSpinBox
                            - label_animation_cycles: QLabel
                            - pushButton_animation_loop: QPushButton
                - frame_middle: QFrame
                    - (Layout): QGridLayout
                            - label_phase_angle: QLabel
                            - magnification_factor_slider: QSlider
                            - label_factor: QLabel
                            - label_animation_phase: QLabel
                            - phase_slider: QSlider
                            - label_magnification_factor: QLabel
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
