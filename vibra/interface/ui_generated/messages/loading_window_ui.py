# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'loading_window.ui'
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
    QProgressBar, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_loading_window(object):
    def setupUi(self, loading_window):
        if not loading_window.objectName():
            loading_window.setObjectName(u"loading_window")
        loading_window.setWindowModality(Qt.ApplicationModal)
        loading_window.resize(377, 157)
        self.verticalLayout = QVBoxLayout(loading_window)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.progress_label = QLabel(loading_window)
        self.progress_label.setObjectName(u"progress_label")
        self.progress_label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.progress_label)

        self.progress_bar = QProgressBar(loading_window)
        self.progress_bar.setObjectName(u"progress_bar")
        self.progress_bar.setValue(10)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setTextDirection(QProgressBar.TopToBottom)

        self.verticalLayout.addWidget(self.progress_bar)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_3)

        self.frame = QFrame(loading_window)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.push_button_stop_processing = QPushButton(self.frame)
        self.push_button_stop_processing.setObjectName(u"push_button_stop_processing")
        self.push_button_stop_processing.setMinimumSize(QSize(0, 28))
        self.push_button_stop_processing.setMaximumSize(QSize(120, 28))

        self.gridLayout.addWidget(self.push_button_stop_processing, 0, 0, 1, 1)


        self.verticalLayout.addWidget(self.frame)


        self.retranslateUi(loading_window)

        QMetaObject.connectSlotsByName(loading_window)
    # setupUi

    def retranslateUi(self, loading_window):
        loading_window.setWindowTitle(QCoreApplication.translate("loading_window", u"Loading Window", None))
        self.progress_label.setText(QCoreApplication.translate("loading_window", u"Loading ...", None))
        self.push_button_stop_processing.setText(QCoreApplication.translate("loading_window", u"Stop processing", None))
    # retranslateUi



class LoadingWindow_UI(QWidget, Ui_loading_window):
    """
    Component Hierarchy:
    - loading_window: QWidget
        - (Layout): QVBoxLayout
                - progress_label: QLabel
                - progress_bar: QProgressBar
                - frame: QFrame
                    - (Layout): QGridLayout
                            - push_button_stop_processing: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
