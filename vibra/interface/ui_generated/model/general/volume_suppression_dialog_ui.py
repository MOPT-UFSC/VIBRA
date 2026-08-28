# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'volume_suppression_dialog.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QDialog, QFrame,
    QGridLayout, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(323, 415)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.Box)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.frame)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

        self.frame_3 = QFrame(Dialog)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_3)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.pushButton_ok = QPushButton(self.frame_3)
        self.pushButton_ok.setObjectName(u"pushButton_ok")
        self.pushButton_ok.setMinimumSize(QSize(68, 28))
        self.pushButton_ok.setMaximumSize(QSize(140, 16777215))
        font1 = QFont()
        font1.setPointSize(10)
        self.pushButton_ok.setFont(font1)
        self.pushButton_ok.setAutoDefault(False)

        self.gridLayout_4.addWidget(self.pushButton_ok, 0, 3, 1, 1)

        self.pushButton_apply = QPushButton(self.frame_3)
        self.pushButton_apply.setObjectName(u"pushButton_apply")
        self.pushButton_apply.setMinimumSize(QSize(68, 28))
        self.pushButton_apply.setMaximumSize(QSize(140, 16777215))
        self.pushButton_apply.setFont(font1)
        self.pushButton_apply.setAutoDefault(False)

        self.gridLayout_4.addWidget(self.pushButton_apply, 0, 2, 1, 1)

        self.pushButton_cancel = QPushButton(self.frame_3)
        self.pushButton_cancel.setObjectName(u"pushButton_cancel")
        self.pushButton_cancel.setMinimumSize(QSize(68, 28))
        self.pushButton_cancel.setMaximumSize(QSize(140, 16777215))
        self.pushButton_cancel.setFont(font1)
        self.pushButton_cancel.setAutoDefault(False)

        self.gridLayout_4.addWidget(self.pushButton_cancel, 0, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer, 0, 1, 1, 1)


        self.gridLayout.addWidget(self.frame_3, 2, 0, 1, 1)

        self.frame_2 = QFrame(Dialog)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.Box)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame_4 = QFrame(self.frame_2)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_4)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.label_selected_ids = QLabel(self.frame_4)
        self.label_selected_ids.setObjectName(u"label_selected_ids")
        self.label_selected_ids.setMinimumSize(QSize(50, 20))
        self.label_selected_ids.setMaximumSize(QSize(16777215, 160))
        self.label_selected_ids.setFont(font1)
        self.label_selected_ids.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_selected_ids, 0, 0, 1, 1)

        self.lineEdit_selected_ids = QLineEdit(self.frame_4)
        self.lineEdit_selected_ids.setObjectName(u"lineEdit_selected_ids")
        self.lineEdit_selected_ids.setMinimumSize(QSize(0, 28))
        self.lineEdit_selected_ids.setMaximumSize(QSize(200, 16777215))
        self.lineEdit_selected_ids.setFont(font1)
        self.lineEdit_selected_ids.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.lineEdit_selected_ids, 0, 1, 1, 1)


        self.verticalLayout.addWidget(self.frame_4)

        self.tableWidget_local_mesh_size_control_data = QTableWidget(self.frame_2)
        if (self.tableWidget_local_mesh_size_control_data.columnCount() < 2):
            self.tableWidget_local_mesh_size_control_data.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget_local_mesh_size_control_data.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget_local_mesh_size_control_data.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.tableWidget_local_mesh_size_control_data.setObjectName(u"tableWidget_local_mesh_size_control_data")
        self.tableWidget_local_mesh_size_control_data.setMaximumSize(QSize(16777215, 16777215))
        self.tableWidget_local_mesh_size_control_data.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableWidget_local_mesh_size_control_data.setShowGrid(False)
        self.tableWidget_local_mesh_size_control_data.horizontalHeader().setDefaultSectionSize(160)
        self.tableWidget_local_mesh_size_control_data.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_local_mesh_size_control_data.verticalHeader().setVisible(False)
        self.tableWidget_local_mesh_size_control_data.verticalHeader().setStretchLastSection(False)

        self.verticalLayout.addWidget(self.tableWidget_local_mesh_size_control_data)

        self.frame_5 = QFrame(self.frame_2)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_5)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton_unsuppress = QPushButton(self.frame_5)
        self.pushButton_unsuppress.setObjectName(u"pushButton_unsuppress")
        self.pushButton_unsuppress.setMinimumSize(QSize(100, 28))
        self.pushButton_unsuppress.setMaximumSize(QSize(70, 16777215))
        self.pushButton_unsuppress.setFont(font1)
        self.pushButton_unsuppress.setAutoDefault(False)

        self.horizontalLayout.addWidget(self.pushButton_unsuppress)

        self.pushButton_suppress = QPushButton(self.frame_5)
        self.pushButton_suppress.setObjectName(u"pushButton_suppress")
        self.pushButton_suppress.setMinimumSize(QSize(100, 28))
        self.pushButton_suppress.setMaximumSize(QSize(70, 16777215))
        self.pushButton_suppress.setFont(font1)
        self.pushButton_suppress.setAutoDefault(False)

        self.horizontalLayout.addWidget(self.pushButton_suppress)


        self.verticalLayout.addWidget(self.frame_5)


        self.gridLayout.addWidget(self.frame_2, 1, 0, 1, 1)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Volume suppression setup", None))
        self.pushButton_ok.setText(QCoreApplication.translate("Dialog", u"Ok", None))
        self.pushButton_apply.setText(QCoreApplication.translate("Dialog", u"Apply", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
        self.label_selected_ids.setText(QCoreApplication.translate("Dialog", u"Selected IDs:", None))
        self.lineEdit_selected_ids.setText("")
        ___qtablewidgetitem = self.tableWidget_local_mesh_size_control_data.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Dialog", u"Volume ID", None));
        ___qtablewidgetitem1 = self.tableWidget_local_mesh_size_control_data.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Dialog", u"Status", None));
        self.pushButton_unsuppress.setText(QCoreApplication.translate("Dialog", u"Unsuppress", None))
        self.pushButton_suppress.setText(QCoreApplication.translate("Dialog", u"Suppress", None))
    # retranslateUi



class VolumeSuppressionDialog_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
                - frame_3: QFrame
                    - (Layout): QGridLayout
                            - pushButton_ok: QPushButton
                            - pushButton_apply: QPushButton
                            - pushButton_cancel: QPushButton
                - frame_2: QFrame
                    - (Layout): QVBoxLayout
                            - frame_4: QFrame
                                - (Layout): QGridLayout
                                        - label_selected_ids: QLabel
                                        - lineEdit_selected_ids: QLineEdit
                            - tableWidget_local_mesh_size_control_data: QTableWidget
                            - frame_5: QFrame
                                - (Layout): QHBoxLayout
                                        - pushButton_unsuppress: QPushButton
                                        - pushButton_suppress: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
