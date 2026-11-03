# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'small_areas_detection_tool.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QDoubleSpinBox,
    QFrame, QGridLayout, QHBoxLayout, QHeaderView,
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(592, 601)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.frame)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(9, 9, 9, 9)
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)


        self.verticalLayout.addWidget(self.frame)

        self.frame_2 = QFrame(Dialog)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(6, 6, 6, 6)
        self.label_4 = QLabel(self.frame_2)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_2.addWidget(self.label_4, 2, 0, 1, 1)

        self.comboBox_element_size_factor = QComboBox(self.frame_2)
        self.comboBox_element_size_factor.setObjectName(u"comboBox_element_size_factor")
        self.comboBox_element_size_factor.setMaximumSize(QSize(150, 16777215))

        self.gridLayout_2.addWidget(self.comboBox_element_size_factor, 1, 2, 1, 2)

        self.label_2 = QLabel(self.frame_2)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)

        self.label_3 = QLabel(self.frame_2)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_2.addWidget(self.label_3, 0, 0, 1, 1)

        self.label_5 = QLabel(self.frame_2)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_2.addWidget(self.label_5, 0, 3, 1, 1)

        self.comboBox_size_groups_quantity = QComboBox(self.frame_2)
        self.comboBox_size_groups_quantity.setObjectName(u"comboBox_size_groups_quantity")
        self.comboBox_size_groups_quantity.setMaximumSize(QSize(150, 16777215))

        self.gridLayout_2.addWidget(self.comboBox_size_groups_quantity, 2, 2, 1, 2)

        self.doubleSpinBox_area_detection_threshold = QDoubleSpinBox(self.frame_2)
        self.doubleSpinBox_area_detection_threshold.setObjectName(u"doubleSpinBox_area_detection_threshold")
        self.doubleSpinBox_area_detection_threshold.setMaximumSize(QSize(150, 16777215))

        self.gridLayout_2.addWidget(self.doubleSpinBox_area_detection_threshold, 0, 2, 1, 1)


        self.verticalLayout.addWidget(self.frame_2)

        self.frame_4 = QFrame(Dialog)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_4)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_faces_area = QLabel(self.frame_4)
        self.label_faces_area.setObjectName(u"label_faces_area")

        self.verticalLayout_2.addWidget(self.label_faces_area)

        self.pushButton_detect_small_areas = QPushButton(self.frame_4)
        self.pushButton_detect_small_areas.setObjectName(u"pushButton_detect_small_areas")
        self.pushButton_detect_small_areas.setMinimumSize(QSize(0, 30))
        self.pushButton_detect_small_areas.setMaximumSize(QSize(200, 16777215))
        font = QFont()
        font.setPointSize(10)
        self.pushButton_detect_small_areas.setFont(font)

        self.verticalLayout_2.addWidget(self.pushButton_detect_small_areas)

        self.label_faces_detected = QLabel(self.frame_4)
        self.label_faces_detected.setObjectName(u"label_faces_detected")
        self.label_faces_detected.setMaximumSize(QSize(16777215, 25))
        font1 = QFont()
        font1.setBold(True)
        font1.setKerning(True)
        self.label_faces_detected.setFont(font1)
        self.label_faces_detected.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout_2.addWidget(self.label_faces_detected)

        self.tableWidget = QTableWidget(self.frame_4)
        if (self.tableWidget.columnCount() < 2):
            self.tableWidget.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_2.addWidget(self.tableWidget)


        self.verticalLayout.addWidget(self.frame_4)

        self.frame_3 = QFrame(Dialog)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_3)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton_cancel = QPushButton(self.frame_3)
        self.pushButton_cancel.setObjectName(u"pushButton_cancel")
        self.pushButton_cancel.setMinimumSize(QSize(0, 30))
        self.pushButton_cancel.setFont(font)

        self.horizontalLayout.addWidget(self.pushButton_cancel)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButton_send_to_local_size_control = QPushButton(self.frame_3)
        self.pushButton_send_to_local_size_control.setObjectName(u"pushButton_send_to_local_size_control")
        self.pushButton_send_to_local_size_control.setMinimumSize(QSize(0, 30))
        self.pushButton_send_to_local_size_control.setFont(font)

        self.horizontalLayout.addWidget(self.pushButton_send_to_local_size_control)


        self.verticalLayout.addWidget(self.frame_3)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Small areas detection tool", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Size groups quantity:", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Element size factor:", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Area detection threshold", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"x element area", None))
        self.label_faces_area.setText(QCoreApplication.translate("Dialog", u"Faces with area \u2264 x are selected", None))
        self.pushButton_detect_small_areas.setText(QCoreApplication.translate("Dialog", u"Detect small areas", None))
        self.label_faces_detected.setText(QCoreApplication.translate("Dialog", u"x small faces detected", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Dialog", u"Surface tag", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Dialog", u"Area", None));
        self.pushButton_cancel.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
        self.pushButton_send_to_local_size_control.setText(QCoreApplication.translate("Dialog", u"Send to Local Size Control Tool", None))
    # retranslateUi



class SmallAreasDetectionTool_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QVBoxLayout
                - frame: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
                - frame_2: QFrame
                    - (Layout): QGridLayout
                            - label_4: QLabel
                            - comboBox_element_size_factor: QComboBox
                            - label_2: QLabel
                            - label_3: QLabel
                            - label_5: QLabel
                            - comboBox_size_groups_quantity: QComboBox
                            - doubleSpinBox_area_detection_threshold: QDoubleSpinBox
                - frame_4: QFrame
                    - (Layout): QVBoxLayout
                            - label_faces_area: QLabel
                            - pushButton_detect_small_areas: QPushButton
                            - label_faces_detected: QLabel
                            - tableWidget: QTableWidget
                - frame_3: QFrame
                    - (Layout): QHBoxLayout
                            - pushButton_cancel: QPushButton
                            - pushButton_send_to_local_size_control: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
