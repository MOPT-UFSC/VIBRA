# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dof_prescription_inputs.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFrame,
    QGridLayout, QHeaderView, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QTabWidget,
    QTreeWidget, QTreeWidgetItem, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setWindowModality(Qt.WindowModality.WindowModal)
        Dialog.resize(500, 560)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(500, 540))
        Dialog.setMaximumSize(QSize(500, 560))
        font = QFont()
        font.setPointSize(11)
        font.setBold(False)
        Dialog.setFont(font)
        Dialog.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        self.gridLayout_7 = QGridLayout(Dialog)
        self.gridLayout_7.setSpacing(4)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(4, 4, 4, 4)
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(380, 48))
        self.frame.setMaximumSize(QSize(16777215, 48))
        self.frame.setFrameShape(QFrame.Shape.Box)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.frame.setLineWidth(1)
        self.gridLayout_6 = QGridLayout(self.frame)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        font1 = QFont()
        font1.setFamilies([u"MS Shell Dlg 2"])
        font1.setPointSize(11)
        font1.setBold(False)
        font1.setItalic(False)
        self.label.setFont(font1)
        self.label.setTextFormat(Qt.TextFormat.AutoText)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_6.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout_7.addWidget(self.frame, 0, 0, 1, 1)

        self.frame_2 = QFrame(Dialog)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(380, 395))
        self.frame_2.setMaximumSize(QSize(16777215, 480))
        self.frame_2.setFrameShape(QFrame.Shape.Box)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_2)
        self.gridLayout_4.setSpacing(2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(2, 4, 2, 2)
        self.frame_4 = QFrame(self.frame_2)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(360, 72))
        self.frame_4.setMaximumSize(QSize(16777215, 120))
        self.frame_4.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_4)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setHorizontalSpacing(6)
        self.gridLayout_5.setVerticalSpacing(5)
        self.gridLayout_5.setContentsMargins(2, 4, 2, 2)
        self.label_linear = QLabel(self.frame_4)
        self.label_linear.setObjectName(u"label_linear")
        self.label_linear.setMinimumSize(QSize(72, 0))
        font2 = QFont()
        font2.setPointSize(10)
        font2.setBold(False)
        self.label_linear.setFont(font2)
        self.label_linear.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_linear, 2, 1, 1, 1)

        self.lineEdit_selection_id = QLineEdit(self.frame_4)
        self.lineEdit_selection_id.setObjectName(u"lineEdit_selection_id")
        self.lineEdit_selection_id.setMinimumSize(QSize(120, 28))
        self.lineEdit_selection_id.setMaximumSize(QSize(140, 28))
        font3 = QFont()
        font3.setFamilies([u"MS Shell Dlg 2"])
        font3.setPointSize(10)
        font3.setBold(False)
        font3.setItalic(False)
        self.lineEdit_selection_id.setFont(font3)
        self.lineEdit_selection_id.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.lineEdit_selection_id.setStyleSheet(u"")
        self.lineEdit_selection_id.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.lineEdit_selection_id, 0, 2, 1, 1)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_9, 0, 4, 1, 1)

        self.label_2 = QLabel(self.frame_4)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(100, 28))
        self.label_2.setMaximumSize(QSize(100, 28))
        font4 = QFont()
        font4.setPointSize(10)
        font4.setBold(False)
        font4.setItalic(False)
        self.label_2.setFont(font4)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_2, 0, 1, 1, 1)

        self.comboBox_element_type = QComboBox(self.frame_4)
        self.comboBox_element_type.addItem("")
        self.comboBox_element_type.addItem("")
        self.comboBox_element_type.setObjectName(u"comboBox_element_type")
        self.comboBox_element_type.setMinimumSize(QSize(120, 28))
        self.comboBox_element_type.setMaximumSize(QSize(140, 28))
        self.comboBox_element_type.setFont(font2)

        self.gridLayout_5.addWidget(self.comboBox_element_type, 1, 2, 1, 1)

        self.label_3 = QLabel(self.frame_4)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(100, 28))
        self.label_3.setMaximumSize(QSize(100, 28))
        self.label_3.setFont(font4)
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_3, 1, 1, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_6, 0, 0, 1, 1)

        self.comboBox_attribution_type = QComboBox(self.frame_4)
        self.comboBox_attribution_type.addItem("")
        self.comboBox_attribution_type.addItem("")
        self.comboBox_attribution_type.addItem("")
        self.comboBox_attribution_type.addItem("")
        self.comboBox_attribution_type.setObjectName(u"comboBox_attribution_type")
        self.comboBox_attribution_type.setMinimumSize(QSize(0, 28))
        self.comboBox_attribution_type.setMaximumSize(QSize(16777215, 28))
        self.comboBox_attribution_type.setFont(font2)

        self.gridLayout_5.addWidget(self.comboBox_attribution_type, 0, 3, 1, 1)

        self.comboBox_data_type = QComboBox(self.frame_4)
        self.comboBox_data_type.addItem("")
        self.comboBox_data_type.addItem("")
        self.comboBox_data_type.addItem("")
        self.comboBox_data_type.setObjectName(u"comboBox_data_type")
        self.comboBox_data_type.setMinimumSize(QSize(0, 28))
        self.comboBox_data_type.setMaximumSize(QSize(16777215, 28))
        self.comboBox_data_type.setFont(font2)

        self.gridLayout_5.addWidget(self.comboBox_data_type, 2, 2, 1, 1)


        self.gridLayout_4.addWidget(self.frame_4, 0, 0, 1, 1)

        self.frame_6 = QFrame(self.frame_2)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_6.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_13 = QGridLayout(self.frame_6)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_13.setContentsMargins(4, 4, 4, 8)
        self.tabWidget_main = QTabWidget(self.frame_6)
        self.tabWidget_main.setObjectName(u"tabWidget_main")
        self.tabWidget_main.setMinimumSize(QSize(360, 0))
        self.tabWidget_main.setMaximumSize(QSize(480, 16777215))
        self.tabWidget_main.setFont(font2)
        self.tab_constant_data = QWidget()
        self.tab_constant_data.setObjectName(u"tab_constant_data")
        self.gridLayout_12 = QGridLayout(self.tab_constant_data)
        self.gridLayout_12.setSpacing(2)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setContentsMargins(2, 2, 2, 2)
        self.frame_8 = QFrame(self.tab_constant_data)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setMinimumSize(QSize(340, 0))
        self.frame_8.setMaximumSize(QSize(16777215, 320))
        self.frame_8.setFont(font2)
        self.frame_8.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_8.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.frame_8)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.lineEdit_real_rx = QLineEdit(self.frame_8)
        self.lineEdit_real_rx.setObjectName(u"lineEdit_real_rx")
        self.lineEdit_real_rx.setMinimumSize(QSize(80, 26))
        self.lineEdit_real_rx.setMaximumSize(QSize(100, 26))
        self.lineEdit_real_rx.setFont(font2)
        self.lineEdit_real_rx.setStyleSheet(u"")
        self.lineEdit_real_rx.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_real_rx, 6, 4, 1, 1)

        self.label_Rx_constant = QLabel(self.frame_8)
        self.label_Rx_constant.setObjectName(u"label_Rx_constant")
        self.label_Rx_constant.setMinimumSize(QSize(40, 26))
        self.label_Rx_constant.setMaximumSize(QSize(80, 26))
        self.label_Rx_constant.setFont(font2)
        self.label_Rx_constant.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_Rx_constant, 6, 2, 1, 1)

        self.comboBox_displacement_ux = QComboBox(self.frame_8)
        self.comboBox_displacement_ux.addItem("")
        self.comboBox_displacement_ux.addItem("")
        self.comboBox_displacement_ux.addItem("")
        self.comboBox_displacement_ux.setObjectName(u"comboBox_displacement_ux")
        self.comboBox_displacement_ux.setMinimumSize(QSize(100, 26))
        self.comboBox_displacement_ux.setMaximumSize(QSize(120, 16777215))
        font5 = QFont()
        font5.setPointSize(9)
        font5.setBold(False)
        self.comboBox_displacement_ux.setFont(font5)

        self.gridLayout.addWidget(self.comboBox_displacement_ux, 3, 6, 1, 1)

        self.lineEdit_imag_uy = QLineEdit(self.frame_8)
        self.lineEdit_imag_uy.setObjectName(u"lineEdit_imag_uy")
        self.lineEdit_imag_uy.setMinimumSize(QSize(80, 26))
        self.lineEdit_imag_uy.setMaximumSize(QSize(100, 26))
        self.lineEdit_imag_uy.setFont(font3)
        self.lineEdit_imag_uy.setStyleSheet(u"")
        self.lineEdit_imag_uy.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_imag_uy, 4, 5, 1, 1)

        self.comboBox_displacement_uz = QComboBox(self.frame_8)
        self.comboBox_displacement_uz.addItem("")
        self.comboBox_displacement_uz.addItem("")
        self.comboBox_displacement_uz.addItem("")
        self.comboBox_displacement_uz.setObjectName(u"comboBox_displacement_uz")
        self.comboBox_displacement_uz.setMinimumSize(QSize(100, 26))
        self.comboBox_displacement_uz.setMaximumSize(QSize(120, 16777215))
        self.comboBox_displacement_uz.setFont(font5)

        self.gridLayout.addWidget(self.comboBox_displacement_uz, 5, 6, 1, 1)

        self.comboBox_displacement_uy = QComboBox(self.frame_8)
        self.comboBox_displacement_uy.addItem("")
        self.comboBox_displacement_uy.addItem("")
        self.comboBox_displacement_uy.addItem("")
        self.comboBox_displacement_uy.setObjectName(u"comboBox_displacement_uy")
        self.comboBox_displacement_uy.setMinimumSize(QSize(100, 26))
        self.comboBox_displacement_uy.setMaximumSize(QSize(120, 16777215))
        self.comboBox_displacement_uy.setFont(font5)

        self.gridLayout.addWidget(self.comboBox_displacement_uy, 4, 6, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 3, 8, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 3, 0, 1, 1)

        self.label_4 = QLabel(self.frame_8)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(80, 24))
        self.label_4.setMaximumSize(QSize(80, 24))
        self.label_4.setFont(font3)
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_4, 2, 4, 1, 1)

        self.label_20 = QLabel(self.frame_8)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setMinimumSize(QSize(80, 24))
        self.label_20.setMaximumSize(QSize(80, 24))
        self.label_20.setFont(font3)
        self.label_20.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_20, 2, 5, 1, 1)

        self.lineEdit_real_ux = QLineEdit(self.frame_8)
        self.lineEdit_real_ux.setObjectName(u"lineEdit_real_ux")
        self.lineEdit_real_ux.setMinimumSize(QSize(80, 26))
        self.lineEdit_real_ux.setMaximumSize(QSize(100, 26))
        self.lineEdit_real_ux.setFont(font3)
        self.lineEdit_real_ux.setStyleSheet(u"")
        self.lineEdit_real_ux.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_real_ux, 3, 4, 1, 1)

        self.label_Ry_constant = QLabel(self.frame_8)
        self.label_Ry_constant.setObjectName(u"label_Ry_constant")
        self.label_Ry_constant.setMinimumSize(QSize(40, 26))
        self.label_Ry_constant.setMaximumSize(QSize(80, 26))
        self.label_Ry_constant.setFont(font2)
        self.label_Ry_constant.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_Ry_constant, 7, 2, 1, 1)

        self.lineEdit_imag_uz = QLineEdit(self.frame_8)
        self.lineEdit_imag_uz.setObjectName(u"lineEdit_imag_uz")
        self.lineEdit_imag_uz.setMinimumSize(QSize(80, 26))
        self.lineEdit_imag_uz.setMaximumSize(QSize(100, 26))
        self.lineEdit_imag_uz.setFont(font3)
        self.lineEdit_imag_uz.setStyleSheet(u"")
        self.lineEdit_imag_uz.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_imag_uz, 5, 5, 1, 1)

        self.lineEdit_real_uz = QLineEdit(self.frame_8)
        self.lineEdit_real_uz.setObjectName(u"lineEdit_real_uz")
        self.lineEdit_real_uz.setMinimumSize(QSize(80, 26))
        self.lineEdit_real_uz.setMaximumSize(QSize(100, 26))
        self.lineEdit_real_uz.setFont(font3)
        self.lineEdit_real_uz.setStyleSheet(u"")
        self.lineEdit_real_uz.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_real_uz, 5, 4, 1, 1)

        self.lineEdit_real_uy = QLineEdit(self.frame_8)
        self.lineEdit_real_uy.setObjectName(u"lineEdit_real_uy")
        self.lineEdit_real_uy.setMinimumSize(QSize(80, 26))
        self.lineEdit_real_uy.setMaximumSize(QSize(100, 26))
        self.lineEdit_real_uy.setFont(font3)
        self.lineEdit_real_uy.setStyleSheet(u"")
        self.lineEdit_real_uy.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_real_uy, 4, 4, 1, 1)

        self.label_Uz_constant = QLabel(self.frame_8)
        self.label_Uz_constant.setObjectName(u"label_Uz_constant")
        self.label_Uz_constant.setMinimumSize(QSize(40, 26))
        self.label_Uz_constant.setMaximumSize(QSize(80, 26))
        self.label_Uz_constant.setFont(font4)
        self.label_Uz_constant.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_Uz_constant, 5, 2, 1, 1)

        self.lineEdit_imag_ux = QLineEdit(self.frame_8)
        self.lineEdit_imag_ux.setObjectName(u"lineEdit_imag_ux")
        self.lineEdit_imag_ux.setMinimumSize(QSize(80, 26))
        self.lineEdit_imag_ux.setMaximumSize(QSize(100, 26))
        self.lineEdit_imag_ux.setFont(font3)
        self.lineEdit_imag_ux.setStyleSheet(u"")
        self.lineEdit_imag_ux.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_imag_ux, 3, 5, 1, 1)

        self.label_Uy_constant = QLabel(self.frame_8)
        self.label_Uy_constant.setObjectName(u"label_Uy_constant")
        self.label_Uy_constant.setMinimumSize(QSize(40, 26))
        self.label_Uy_constant.setMaximumSize(QSize(80, 26))
        self.label_Uy_constant.setFont(font4)
        self.label_Uy_constant.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_Uy_constant, 4, 2, 1, 1)

        self.lineEdit_imag_rz = QLineEdit(self.frame_8)
        self.lineEdit_imag_rz.setObjectName(u"lineEdit_imag_rz")
        self.lineEdit_imag_rz.setMinimumSize(QSize(80, 26))
        self.lineEdit_imag_rz.setMaximumSize(QSize(100, 26))
        self.lineEdit_imag_rz.setFont(font2)
        self.lineEdit_imag_rz.setStyleSheet(u"")
        self.lineEdit_imag_rz.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_imag_rz, 8, 5, 1, 1)

        self.lineEdit_imag_ry = QLineEdit(self.frame_8)
        self.lineEdit_imag_ry.setObjectName(u"lineEdit_imag_ry")
        self.lineEdit_imag_ry.setMinimumSize(QSize(80, 26))
        self.lineEdit_imag_ry.setMaximumSize(QSize(100, 26))
        self.lineEdit_imag_ry.setFont(font2)
        self.lineEdit_imag_ry.setStyleSheet(u"")
        self.lineEdit_imag_ry.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_imag_ry, 7, 5, 1, 1)

        self.lineEdit_real_ry = QLineEdit(self.frame_8)
        self.lineEdit_real_ry.setObjectName(u"lineEdit_real_ry")
        self.lineEdit_real_ry.setMinimumSize(QSize(80, 26))
        self.lineEdit_real_ry.setMaximumSize(QSize(100, 26))
        self.lineEdit_real_ry.setFont(font2)
        self.lineEdit_real_ry.setStyleSheet(u"")
        self.lineEdit_real_ry.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_real_ry, 7, 4, 1, 1)

        self.lineEdit_real_rz = QLineEdit(self.frame_8)
        self.lineEdit_real_rz.setObjectName(u"lineEdit_real_rz")
        self.lineEdit_real_rz.setMinimumSize(QSize(80, 26))
        self.lineEdit_real_rz.setMaximumSize(QSize(100, 26))
        self.lineEdit_real_rz.setFont(font2)
        self.lineEdit_real_rz.setStyleSheet(u"")
        self.lineEdit_real_rz.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_real_rz, 8, 4, 1, 1)

        self.lineEdit_imag_rx = QLineEdit(self.frame_8)
        self.lineEdit_imag_rx.setObjectName(u"lineEdit_imag_rx")
        self.lineEdit_imag_rx.setMinimumSize(QSize(80, 26))
        self.lineEdit_imag_rx.setMaximumSize(QSize(100, 26))
        self.lineEdit_imag_rx.setFont(font2)
        self.lineEdit_imag_rx.setStyleSheet(u"")
        self.lineEdit_imag_rx.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_imag_rx, 6, 5, 1, 1)

        self.label_Ux_constant = QLabel(self.frame_8)
        self.label_Ux_constant.setObjectName(u"label_Ux_constant")
        self.label_Ux_constant.setMinimumSize(QSize(40, 26))
        self.label_Ux_constant.setMaximumSize(QSize(80, 26))
        self.label_Ux_constant.setFont(font4)
        self.label_Ux_constant.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_Ux_constant, 3, 2, 1, 1)

        self.label_Rz_constant = QLabel(self.frame_8)
        self.label_Rz_constant.setObjectName(u"label_Rz_constant")
        self.label_Rz_constant.setMinimumSize(QSize(40, 26))
        self.label_Rz_constant.setMaximumSize(QSize(80, 26))
        self.label_Rz_constant.setFont(font2)
        self.label_Rz_constant.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_Rz_constant, 8, 2, 1, 1)

        self.comboBox_rotation_rz = QComboBox(self.frame_8)
        self.comboBox_rotation_rz.addItem("")
        self.comboBox_rotation_rz.addItem("")
        self.comboBox_rotation_rz.addItem("")
        self.comboBox_rotation_rz.setObjectName(u"comboBox_rotation_rz")
        self.comboBox_rotation_rz.setMinimumSize(QSize(100, 26))
        self.comboBox_rotation_rz.setMaximumSize(QSize(120, 16777215))
        self.comboBox_rotation_rz.setFont(font5)

        self.gridLayout.addWidget(self.comboBox_rotation_rz, 8, 6, 1, 1)

        self.comboBox_rotation_ry = QComboBox(self.frame_8)
        self.comboBox_rotation_ry.addItem("")
        self.comboBox_rotation_ry.addItem("")
        self.comboBox_rotation_ry.addItem("")
        self.comboBox_rotation_ry.setObjectName(u"comboBox_rotation_ry")
        self.comboBox_rotation_ry.setMinimumSize(QSize(100, 26))
        self.comboBox_rotation_ry.setMaximumSize(QSize(120, 16777215))
        self.comboBox_rotation_ry.setFont(font5)

        self.gridLayout.addWidget(self.comboBox_rotation_ry, 7, 6, 1, 1)

        self.comboBox_rotation_rx = QComboBox(self.frame_8)
        self.comboBox_rotation_rx.addItem("")
        self.comboBox_rotation_rx.addItem("")
        self.comboBox_rotation_rx.addItem("")
        self.comboBox_rotation_rx.setObjectName(u"comboBox_rotation_rx")
        self.comboBox_rotation_rx.setMinimumSize(QSize(100, 26))
        self.comboBox_rotation_rx.setMaximumSize(QSize(120, 16777215))
        self.comboBox_rotation_rx.setFont(font5)

        self.gridLayout.addWidget(self.comboBox_rotation_rx, 6, 6, 1, 1)

        self.frame_10 = QFrame(self.frame_8)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setMinimumSize(QSize(0, 0))
        self.frame_10.setMaximumSize(QSize(16777215, 40))
        self.frame_10.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_10.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_14 = QGridLayout(self.frame_10)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.gridLayout_14.setContentsMargins(2, 2, 2, 2)
        self.pushButton_all_dof_fixed = QPushButton(self.frame_10)
        self.pushButton_all_dof_fixed.setObjectName(u"pushButton_all_dof_fixed")
        self.pushButton_all_dof_fixed.setMinimumSize(QSize(100, 28))
        self.pushButton_all_dof_fixed.setMaximumSize(QSize(100, 28))
        self.pushButton_all_dof_fixed.setFont(font2)
        self.pushButton_all_dof_fixed.setStyleSheet(u"")
        self.pushButton_all_dof_fixed.setAutoDefault(False)

        self.gridLayout_14.addWidget(self.pushButton_all_dof_fixed, 0, 1, 1, 1)

        self.pushButton_all_dof_free = QPushButton(self.frame_10)
        self.pushButton_all_dof_free.setObjectName(u"pushButton_all_dof_free")
        self.pushButton_all_dof_free.setMinimumSize(QSize(40, 28))
        self.pushButton_all_dof_free.setMaximumSize(QSize(100, 28))
        self.pushButton_all_dof_free.setFont(font2)
        self.pushButton_all_dof_free.setStyleSheet(u"")
        self.pushButton_all_dof_free.setIconSize(QSize(22, 22))
        self.pushButton_all_dof_free.setAutoDefault(False)

        self.gridLayout_14.addWidget(self.pushButton_all_dof_free, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_10, 9, 2, 1, 6)


        self.gridLayout_12.addWidget(self.frame_8, 0, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_constant_data, "")
        self.tab_tabular_data = QWidget()
        self.tab_tabular_data.setObjectName(u"tab_tabular_data")
        self.gridLayout_10 = QGridLayout(self.tab_tabular_data)
        self.gridLayout_10.setSpacing(2)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(2, 2, 2, 2)
        self.frame_9 = QFrame(self.tab_tabular_data)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_9.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_9)
        self.gridLayout_3.setSpacing(6)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(4, 4, 6, 2)
        self.lineEdit_path_table_uz = QLineEdit(self.frame_9)
        self.lineEdit_path_table_uz.setObjectName(u"lineEdit_path_table_uz")
        self.lineEdit_path_table_uz.setEnabled(True)
        self.lineEdit_path_table_uz.setMinimumSize(QSize(260, 26))
        self.lineEdit_path_table_uz.setMaximumSize(QSize(360, 26))
        self.lineEdit_path_table_uz.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_path_table_uz.setClearButtonEnabled(True)

        self.gridLayout_3.addWidget(self.lineEdit_path_table_uz, 2, 1, 1, 1)

        self.pushButton_load_uy_table = QPushButton(self.frame_9)
        self.pushButton_load_uy_table.setObjectName(u"pushButton_load_uy_table")
        self.pushButton_load_uy_table.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton_load_uy_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_uy_table.setSizePolicy(sizePolicy1)
        self.pushButton_load_uy_table.setMinimumSize(QSize(40, 26))
        self.pushButton_load_uy_table.setMaximumSize(QSize(40, 26))
        self.pushButton_load_uy_table.setFont(font2)
        self.pushButton_load_uy_table.setStyleSheet(u"")
        icon = QIcon()
        icon.addFile(u":/icons/document_search_blue.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_load_uy_table.setIcon(icon)
        self.pushButton_load_uy_table.setIconSize(QSize(20, 20))
        self.pushButton_load_uy_table.setAutoDefault(False)

        self.gridLayout_3.addWidget(self.pushButton_load_uy_table, 1, 2, 1, 1)

        self.label_Ry_table = QLabel(self.frame_9)
        self.label_Ry_table.setObjectName(u"label_Ry_table")
        self.label_Ry_table.setEnabled(True)
        self.label_Ry_table.setMinimumSize(QSize(40, 26))
        self.label_Ry_table.setMaximumSize(QSize(80, 26))
        self.label_Ry_table.setFont(font2)
        self.label_Ry_table.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_Ry_table, 4, 0, 1, 1)

        self.pushButton_load_ux_table = QPushButton(self.frame_9)
        self.pushButton_load_ux_table.setObjectName(u"pushButton_load_ux_table")
        self.pushButton_load_ux_table.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.pushButton_load_ux_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_ux_table.setSizePolicy(sizePolicy1)
        self.pushButton_load_ux_table.setMinimumSize(QSize(40, 26))
        self.pushButton_load_ux_table.setMaximumSize(QSize(40, 26))
        self.pushButton_load_ux_table.setFont(font2)
        self.pushButton_load_ux_table.setStyleSheet(u"")
        self.pushButton_load_ux_table.setIcon(icon)
        self.pushButton_load_ux_table.setIconSize(QSize(20, 20))
        self.pushButton_load_ux_table.setAutoDefault(False)

        self.gridLayout_3.addWidget(self.pushButton_load_ux_table, 0, 2, 1, 1)

        self.lineEdit_path_table_ry = QLineEdit(self.frame_9)
        self.lineEdit_path_table_ry.setObjectName(u"lineEdit_path_table_ry")
        self.lineEdit_path_table_ry.setEnabled(True)
        self.lineEdit_path_table_ry.setMinimumSize(QSize(260, 26))
        self.lineEdit_path_table_ry.setMaximumSize(QSize(360, 26))
        self.lineEdit_path_table_ry.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_path_table_ry.setClearButtonEnabled(True)

        self.gridLayout_3.addWidget(self.lineEdit_path_table_ry, 4, 1, 1, 1)

        self.pushButton_load_ry_table = QPushButton(self.frame_9)
        self.pushButton_load_ry_table.setObjectName(u"pushButton_load_ry_table")
        self.pushButton_load_ry_table.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.pushButton_load_ry_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_ry_table.setSizePolicy(sizePolicy1)
        self.pushButton_load_ry_table.setMinimumSize(QSize(40, 26))
        self.pushButton_load_ry_table.setMaximumSize(QSize(40, 26))
        self.pushButton_load_ry_table.setFont(font2)
        self.pushButton_load_ry_table.setStyleSheet(u"")
        self.pushButton_load_ry_table.setIcon(icon)
        self.pushButton_load_ry_table.setIconSize(QSize(20, 20))
        self.pushButton_load_ry_table.setAutoDefault(False)

        self.gridLayout_3.addWidget(self.pushButton_load_ry_table, 4, 2, 1, 1)

        self.label_Ux_table = QLabel(self.frame_9)
        self.label_Ux_table.setObjectName(u"label_Ux_table")
        self.label_Ux_table.setEnabled(True)
        self.label_Ux_table.setMinimumSize(QSize(40, 26))
        self.label_Ux_table.setMaximumSize(QSize(80, 26))
        self.label_Ux_table.setFont(font2)
        self.label_Ux_table.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_Ux_table, 0, 0, 1, 1)

        self.lineEdit_path_table_ux = QLineEdit(self.frame_9)
        self.lineEdit_path_table_ux.setObjectName(u"lineEdit_path_table_ux")
        self.lineEdit_path_table_ux.setEnabled(True)
        self.lineEdit_path_table_ux.setMinimumSize(QSize(260, 26))
        self.lineEdit_path_table_ux.setMaximumSize(QSize(360, 26))
        self.lineEdit_path_table_ux.setStyleSheet(u"")
        self.lineEdit_path_table_ux.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_path_table_ux.setClearButtonEnabled(True)

        self.gridLayout_3.addWidget(self.lineEdit_path_table_ux, 0, 1, 1, 1)

        self.pushButton_load_rz_table = QPushButton(self.frame_9)
        self.pushButton_load_rz_table.setObjectName(u"pushButton_load_rz_table")
        self.pushButton_load_rz_table.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.pushButton_load_rz_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_rz_table.setSizePolicy(sizePolicy1)
        self.pushButton_load_rz_table.setMinimumSize(QSize(40, 26))
        self.pushButton_load_rz_table.setMaximumSize(QSize(40, 26))
        self.pushButton_load_rz_table.setFont(font2)
        self.pushButton_load_rz_table.setStyleSheet(u"")
        self.pushButton_load_rz_table.setIcon(icon)
        self.pushButton_load_rz_table.setIconSize(QSize(20, 20))
        self.pushButton_load_rz_table.setAutoDefault(False)

        self.gridLayout_3.addWidget(self.pushButton_load_rz_table, 5, 2, 1, 1)

        self.lineEdit_path_table_rx = QLineEdit(self.frame_9)
        self.lineEdit_path_table_rx.setObjectName(u"lineEdit_path_table_rx")
        self.lineEdit_path_table_rx.setEnabled(True)
        self.lineEdit_path_table_rx.setMinimumSize(QSize(260, 26))
        self.lineEdit_path_table_rx.setMaximumSize(QSize(360, 26))
        self.lineEdit_path_table_rx.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_path_table_rx.setClearButtonEnabled(True)

        self.gridLayout_3.addWidget(self.lineEdit_path_table_rx, 3, 1, 1, 1)

        self.label_Uz_table = QLabel(self.frame_9)
        self.label_Uz_table.setObjectName(u"label_Uz_table")
        self.label_Uz_table.setEnabled(True)
        self.label_Uz_table.setMinimumSize(QSize(40, 26))
        self.label_Uz_table.setMaximumSize(QSize(80, 26))
        self.label_Uz_table.setFont(font2)
        self.label_Uz_table.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_Uz_table, 2, 0, 1, 1)

        self.label_Uy_table = QLabel(self.frame_9)
        self.label_Uy_table.setObjectName(u"label_Uy_table")
        self.label_Uy_table.setEnabled(True)
        self.label_Uy_table.setMinimumSize(QSize(40, 26))
        self.label_Uy_table.setMaximumSize(QSize(80, 26))
        self.label_Uy_table.setFont(font2)
        self.label_Uy_table.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_Uy_table, 1, 0, 1, 1)

        self.pushButton_load_uz_table = QPushButton(self.frame_9)
        self.pushButton_load_uz_table.setObjectName(u"pushButton_load_uz_table")
        self.pushButton_load_uz_table.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.pushButton_load_uz_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_uz_table.setSizePolicy(sizePolicy1)
        self.pushButton_load_uz_table.setMinimumSize(QSize(40, 26))
        self.pushButton_load_uz_table.setMaximumSize(QSize(40, 26))
        self.pushButton_load_uz_table.setFont(font2)
        self.pushButton_load_uz_table.setStyleSheet(u"")
        self.pushButton_load_uz_table.setIcon(icon)
        self.pushButton_load_uz_table.setIconSize(QSize(20, 20))
        self.pushButton_load_uz_table.setAutoDefault(False)

        self.gridLayout_3.addWidget(self.pushButton_load_uz_table, 2, 2, 1, 1)

        self.pushButton_load_rx_table = QPushButton(self.frame_9)
        self.pushButton_load_rx_table.setObjectName(u"pushButton_load_rx_table")
        self.pushButton_load_rx_table.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.pushButton_load_rx_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_rx_table.setSizePolicy(sizePolicy1)
        self.pushButton_load_rx_table.setMinimumSize(QSize(40, 26))
        self.pushButton_load_rx_table.setMaximumSize(QSize(40, 26))
        self.pushButton_load_rx_table.setFont(font2)
        self.pushButton_load_rx_table.setStyleSheet(u"")
        self.pushButton_load_rx_table.setIcon(icon)
        self.pushButton_load_rx_table.setIconSize(QSize(20, 20))
        self.pushButton_load_rx_table.setAutoDefault(False)

        self.gridLayout_3.addWidget(self.pushButton_load_rx_table, 3, 2, 1, 1)

        self.label_Rz_table = QLabel(self.frame_9)
        self.label_Rz_table.setObjectName(u"label_Rz_table")
        self.label_Rz_table.setEnabled(True)
        self.label_Rz_table.setMinimumSize(QSize(40, 26))
        self.label_Rz_table.setMaximumSize(QSize(80, 26))
        self.label_Rz_table.setFont(font2)
        self.label_Rz_table.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_Rz_table, 5, 0, 1, 1)

        self.lineEdit_path_table_uy = QLineEdit(self.frame_9)
        self.lineEdit_path_table_uy.setObjectName(u"lineEdit_path_table_uy")
        self.lineEdit_path_table_uy.setEnabled(True)
        self.lineEdit_path_table_uy.setMinimumSize(QSize(260, 26))
        self.lineEdit_path_table_uy.setMaximumSize(QSize(360, 26))
        self.lineEdit_path_table_uy.setStyleSheet(u"")
        self.lineEdit_path_table_uy.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_path_table_uy.setClearButtonEnabled(True)

        self.gridLayout_3.addWidget(self.lineEdit_path_table_uy, 1, 1, 1, 1)

        self.lineEdit_path_table_rz = QLineEdit(self.frame_9)
        self.lineEdit_path_table_rz.setObjectName(u"lineEdit_path_table_rz")
        self.lineEdit_path_table_rz.setEnabled(True)
        self.lineEdit_path_table_rz.setMinimumSize(QSize(260, 26))
        self.lineEdit_path_table_rz.setMaximumSize(QSize(360, 26))
        self.lineEdit_path_table_rz.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_path_table_rz.setClearButtonEnabled(True)

        self.gridLayout_3.addWidget(self.lineEdit_path_table_rz, 5, 1, 1, 1)

        self.label_Rx_table = QLabel(self.frame_9)
        self.label_Rx_table.setObjectName(u"label_Rx_table")
        self.label_Rx_table.setEnabled(True)
        self.label_Rx_table.setMinimumSize(QSize(40, 26))
        self.label_Rx_table.setMaximumSize(QSize(80, 26))
        self.label_Rx_table.setFont(font2)
        self.label_Rx_table.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_Rx_table, 3, 0, 1, 1)


        self.gridLayout_10.addWidget(self.frame_9, 0, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_tabular_data, "")
        self.tab_list = QWidget()
        self.tab_list.setObjectName(u"tab_list")
        self.gridLayout_9 = QGridLayout(self.tab_list)
        self.gridLayout_9.setSpacing(2)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(2, 2, 2, 2)
        self.frame_5 = QFrame(self.tab_list)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_5)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.treeWidget_prescribed_dof = QTreeWidget(self.frame_5)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(2, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter);
        self.treeWidget_prescribed_dof.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_prescribed_dof.setObjectName(u"treeWidget_prescribed_dof")
        self.treeWidget_prescribed_dof.setMinimumSize(QSize(320, 170))
        self.treeWidget_prescribed_dof.setMaximumSize(QSize(380, 200))
        self.treeWidget_prescribed_dof.setFont(font3)
        self.treeWidget_prescribed_dof.setIndentation(1)
        self.treeWidget_prescribed_dof.setHeaderHidden(False)
        self.treeWidget_prescribed_dof.header().setHighlightSections(False)
        self.treeWidget_prescribed_dof.header().setProperty(u"showSortIndicator", False)
        self.treeWidget_prescribed_dof.header().setStretchLastSection(True)

        self.gridLayout_2.addWidget(self.treeWidget_prescribed_dof, 0, 0, 1, 1)


        self.gridLayout_9.addWidget(self.frame_5, 0, 0, 1, 1)

        self.frame_3 = QFrame(self.tab_list)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(320, 48))
        self.frame_3.setMaximumSize(QSize(16777215, 48))
        self.frame_3.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_8 = QGridLayout(self.frame_3)
        self.gridLayout_8.setSpacing(4)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(4, 4, 4, 4)
        self.pushButton_reset = QPushButton(self.frame_3)
        self.pushButton_reset.setObjectName(u"pushButton_reset")
        self.pushButton_reset.setMinimumSize(QSize(100, 28))
        self.pushButton_reset.setMaximumSize(QSize(100, 28))
        self.pushButton_reset.setFont(font3)
        self.pushButton_reset.setStyleSheet(u"")
        self.pushButton_reset.setAutoDefault(False)

        self.gridLayout_8.addWidget(self.pushButton_reset, 0, 0, 1, 1)

        self.pushButton_remove = QPushButton(self.frame_3)
        self.pushButton_remove.setObjectName(u"pushButton_remove")
        self.pushButton_remove.setMinimumSize(QSize(100, 28))
        self.pushButton_remove.setMaximumSize(QSize(100, 28))
        self.pushButton_remove.setFont(font3)
        self.pushButton_remove.setStyleSheet(u"")
        self.pushButton_remove.setAutoDefault(False)

        self.gridLayout_8.addWidget(self.pushButton_remove, 0, 1, 1, 1)


        self.gridLayout_9.addWidget(self.frame_3, 1, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_list, "")

        self.gridLayout_13.addWidget(self.tabWidget_main, 0, 0, 1, 1)


        self.gridLayout_4.addWidget(self.frame_6, 1, 0, 1, 1)


        self.gridLayout_7.addWidget(self.frame_2, 1, 0, 1, 1)

        self.frame_buttons = QFrame(Dialog)
        self.frame_buttons.setObjectName(u"frame_buttons")
        self.frame_buttons.setMinimumSize(QSize(0, 48))
        self.frame_buttons.setMaximumSize(QSize(16777215, 48))
        self.frame_buttons.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_buttons.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_11 = QGridLayout(self.frame_buttons)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setVerticalSpacing(0)
        self.gridLayout_11.setContentsMargins(6, 0, 6, 0)
        self.pushButton_apply_and_close = QPushButton(self.frame_buttons)
        self.pushButton_apply_and_close.setObjectName(u"pushButton_apply_and_close")
        self.pushButton_apply_and_close.setMinimumSize(QSize(72, 30))
        self.pushButton_apply_and_close.setMaximumSize(QSize(72, 30))
        self.pushButton_apply_and_close.setFont(font4)
        self.pushButton_apply_and_close.setStyleSheet(u"")
        self.pushButton_apply_and_close.setAutoDefault(False)
        self.pushButton_apply_and_close.setFlat(False)

        self.gridLayout_11.addWidget(self.pushButton_apply_and_close, 0, 3, 1, 1)

        self.pushButton_apply = QPushButton(self.frame_buttons)
        self.pushButton_apply.setObjectName(u"pushButton_apply")
        self.pushButton_apply.setMinimumSize(QSize(72, 30))
        self.pushButton_apply.setMaximumSize(QSize(72, 30))
        self.pushButton_apply.setFont(font4)
        self.pushButton_apply.setStyleSheet(u"")
        self.pushButton_apply.setAutoDefault(False)
        self.pushButton_apply.setFlat(False)

        self.gridLayout_11.addWidget(self.pushButton_apply, 0, 2, 1, 1)

        self.pushButton_cancel = QPushButton(self.frame_buttons)
        self.pushButton_cancel.setObjectName(u"pushButton_cancel")
        self.pushButton_cancel.setMinimumSize(QSize(72, 30))
        self.pushButton_cancel.setMaximumSize(QSize(72, 30))
        self.pushButton_cancel.setFont(font4)
        self.pushButton_cancel.setStyleSheet(u"")
        self.pushButton_cancel.setAutoDefault(False)
        self.pushButton_cancel.setFlat(False)

        self.gridLayout_11.addWidget(self.pushButton_cancel, 0, 0, 1, 1)

        self.horizontalSpacer_17 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_11.addItem(self.horizontalSpacer_17, 0, 1, 1, 1)


        self.gridLayout_7.addWidget(self.frame_buttons, 2, 0, 1, 1)


        self.retranslateUi(Dialog)

        self.tabWidget_main.setCurrentIndex(0)
        self.pushButton_apply_and_close.setDefault(False)
        self.pushButton_apply.setDefault(False)
        self.pushButton_cancel.setDefault(False)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Set a boundary condition", None))
#if QT_CONFIG(whatsthis)
        Dialog.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.label.setText(QCoreApplication.translate("Dialog", u"Degrees of freedom prescription setup", None))
        self.label_linear.setText(QCoreApplication.translate("Dialog", u"Data type:", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Selection ID:", None))
        self.comboBox_element_type.setItemText(0, QCoreApplication.translate("Dialog", u" Face element", None))
        self.comboBox_element_type.setItemText(1, QCoreApplication.translate("Dialog", u" Solid element", None))

        self.label_3.setText(QCoreApplication.translate("Dialog", u"Element type:", None))
        self.comboBox_attribution_type.setItemText(0, QCoreApplication.translate("Dialog", u"Selected faces", None))
        self.comboBox_attribution_type.setItemText(1, QCoreApplication.translate("Dialog", u"Selected lines", None))
        self.comboBox_attribution_type.setItemText(2, QCoreApplication.translate("Dialog", u"Selected points", None))
        self.comboBox_attribution_type.setItemText(3, QCoreApplication.translate("Dialog", u"Selected nodes", None))

        self.comboBox_data_type.setItemText(0, QCoreApplication.translate("Dialog", u" Displacement", None))
        self.comboBox_data_type.setItemText(1, QCoreApplication.translate("Dialog", u" Velocity", None))
        self.comboBox_data_type.setItemText(2, QCoreApplication.translate("Dialog", u" Acceleration", None))

        self.label_Rx_constant.setText(QCoreApplication.translate("Dialog", u"Rx:", None))
        self.comboBox_displacement_ux.setItemText(0, QCoreApplication.translate("Dialog", u"Value (m)", None))
        self.comboBox_displacement_ux.setItemText(1, QCoreApplication.translate("Dialog", u"Free", None))
        self.comboBox_displacement_ux.setItemText(2, QCoreApplication.translate("Dialog", u"Fixed", None))

        self.comboBox_displacement_uz.setItemText(0, QCoreApplication.translate("Dialog", u"Value (m)", None))
        self.comboBox_displacement_uz.setItemText(1, QCoreApplication.translate("Dialog", u"Free", None))
        self.comboBox_displacement_uz.setItemText(2, QCoreApplication.translate("Dialog", u"Fixed", None))

        self.comboBox_displacement_uy.setItemText(0, QCoreApplication.translate("Dialog", u"Value (m)", None))
        self.comboBox_displacement_uy.setItemText(1, QCoreApplication.translate("Dialog", u"Free", None))
        self.comboBox_displacement_uy.setItemText(2, QCoreApplication.translate("Dialog", u"Fixed", None))

        self.label_4.setText(QCoreApplication.translate("Dialog", u"Real", None))
        self.label_20.setText(QCoreApplication.translate("Dialog", u"Imaginary", None))
        self.lineEdit_real_ux.setText("")
        self.label_Ry_constant.setText(QCoreApplication.translate("Dialog", u" Ry:", None))
        self.label_Uz_constant.setText(QCoreApplication.translate("Dialog", u"Uz:", None))
        self.label_Uy_constant.setText(QCoreApplication.translate("Dialog", u"Uy:", None))
        self.label_Ux_constant.setText(QCoreApplication.translate("Dialog", u"Ux:", None))
        self.label_Rz_constant.setText(QCoreApplication.translate("Dialog", u"Rz:", None))
        self.comboBox_rotation_rz.setItemText(0, QCoreApplication.translate("Dialog", u"Value (rad)", None))
        self.comboBox_rotation_rz.setItemText(1, QCoreApplication.translate("Dialog", u"Free", None))
        self.comboBox_rotation_rz.setItemText(2, QCoreApplication.translate("Dialog", u"Fixed", None))

        self.comboBox_rotation_ry.setItemText(0, QCoreApplication.translate("Dialog", u"Value (rad)", None))
        self.comboBox_rotation_ry.setItemText(1, QCoreApplication.translate("Dialog", u"Free", None))
        self.comboBox_rotation_ry.setItemText(2, QCoreApplication.translate("Dialog", u"Fixed", None))

        self.comboBox_rotation_rx.setItemText(0, QCoreApplication.translate("Dialog", u"Value (rad)", None))
        self.comboBox_rotation_rx.setItemText(1, QCoreApplication.translate("Dialog", u"Free", None))
        self.comboBox_rotation_rx.setItemText(2, QCoreApplication.translate("Dialog", u"Fixed", None))

        self.pushButton_all_dof_fixed.setText(QCoreApplication.translate("Dialog", u"All DOF fixed", None))
        self.pushButton_all_dof_free.setText(QCoreApplication.translate("Dialog", u"All DOF free", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_constant_data), QCoreApplication.translate("Dialog", u"Constant data", None))
        self.pushButton_load_uy_table.setText("")
        self.label_Ry_table.setText(QCoreApplication.translate("Dialog", u"Ry:", None))
        self.pushButton_load_ux_table.setText("")
        self.pushButton_load_ry_table.setText("")
        self.label_Ux_table.setText(QCoreApplication.translate("Dialog", u"Ux:", None))
        self.pushButton_load_rz_table.setText("")
        self.label_Uz_table.setText(QCoreApplication.translate("Dialog", u"Uz:", None))
        self.label_Uy_table.setText(QCoreApplication.translate("Dialog", u"Uy:", None))
        self.pushButton_load_uz_table.setText("")
        self.pushButton_load_rx_table.setText("")
        self.label_Rz_table.setText(QCoreApplication.translate("Dialog", u"Rz:", None))
        self.label_Rx_table.setText(QCoreApplication.translate("Dialog", u"Rx:", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_tabular_data), QCoreApplication.translate("Dialog", u"Tabular data", None))
        ___qtreewidgetitem = self.treeWidget_prescribed_dof.headerItem()
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("Dialog", u"Element type", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"Prescribed DOF", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Selection-ID", None));
#if QT_CONFIG(tooltip)
        self.treeWidget_prescribed_dof.setToolTip(QCoreApplication.translate("Dialog", u"Select a node to remove the attributed boundary condition.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_reset.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.pushButton_remove.setText(QCoreApplication.translate("Dialog", u"Remove", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_list), QCoreApplication.translate("Dialog", u"List", None))
        self.pushButton_apply_and_close.setText(QCoreApplication.translate("Dialog", u"Ok", None))
        self.pushButton_apply.setText(QCoreApplication.translate("Dialog", u"Apply", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
    # retranslateUi



class DofPrescriptionInputs_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
                - frame_2: QFrame
                    - (Layout): QGridLayout
                            - frame_4: QFrame
                                - (Layout): QGridLayout
                                        - label_linear: QLabel
                                        - lineEdit_selection_id: QLineEdit
                                        - label_2: QLabel
                                        - comboBox_element_type: QComboBox
                                        - label_3: QLabel
                                        - comboBox_attribution_type: QComboBox
                                        - comboBox_data_type: QComboBox
                            - frame_6: QFrame
                                - (Layout): QGridLayout
                                        - tabWidget_main: QTabWidget
                                            - tab_constant_data: QWidget
                                                - (Layout): QGridLayout
                                                        - frame_8: QFrame
                                                            - (Layout): QGridLayout
                                                                    - lineEdit_real_rx: QLineEdit
                                                                    - label_Rx_constant: QLabel
                                                                    - comboBox_displacement_ux: QComboBox
                                                                    - lineEdit_imag_uy: QLineEdit
                                                                    - comboBox_displacement_uz: QComboBox
                                                                    - comboBox_displacement_uy: QComboBox
                                                                    - label_4: QLabel
                                                                    - label_20: QLabel
                                                                    - lineEdit_real_ux: QLineEdit
                                                                    - label_Ry_constant: QLabel
                                                                    - lineEdit_imag_uz: QLineEdit
                                                                    - lineEdit_real_uz: QLineEdit
                                                                    - lineEdit_real_uy: QLineEdit
                                                                    - label_Uz_constant: QLabel
                                                                    - lineEdit_imag_ux: QLineEdit
                                                                    - label_Uy_constant: QLabel
                                                                    - lineEdit_imag_rz: QLineEdit
                                                                    - lineEdit_imag_ry: QLineEdit
                                                                    - lineEdit_real_ry: QLineEdit
                                                                    - lineEdit_real_rz: QLineEdit
                                                                    - lineEdit_imag_rx: QLineEdit
                                                                    - label_Ux_constant: QLabel
                                                                    - label_Rz_constant: QLabel
                                                                    - comboBox_rotation_rz: QComboBox
                                                                    - comboBox_rotation_ry: QComboBox
                                                                    - comboBox_rotation_rx: QComboBox
                                                                    - frame_10: QFrame
                                                                        - (Layout): QGridLayout
                                                                                - pushButton_all_dof_fixed: QPushButton
                                                                                - pushButton_all_dof_free: QPushButton
                                            - tab_tabular_data: QWidget
                                                - (Layout): QGridLayout
                                                        - frame_9: QFrame
                                                            - (Layout): QGridLayout
                                                                    - lineEdit_path_table_uz: QLineEdit
                                                                    - pushButton_load_uy_table: QPushButton
                                                                    - label_Ry_table: QLabel
                                                                    - pushButton_load_ux_table: QPushButton
                                                                    - lineEdit_path_table_ry: QLineEdit
                                                                    - pushButton_load_ry_table: QPushButton
                                                                    - label_Ux_table: QLabel
                                                                    - lineEdit_path_table_ux: QLineEdit
                                                                    - pushButton_load_rz_table: QPushButton
                                                                    - lineEdit_path_table_rx: QLineEdit
                                                                    - label_Uz_table: QLabel
                                                                    - label_Uy_table: QLabel
                                                                    - pushButton_load_uz_table: QPushButton
                                                                    - pushButton_load_rx_table: QPushButton
                                                                    - label_Rz_table: QLabel
                                                                    - lineEdit_path_table_uy: QLineEdit
                                                                    - lineEdit_path_table_rz: QLineEdit
                                                                    - label_Rx_table: QLabel
                                            - tab_list: QWidget
                                                - (Layout): QGridLayout
                                                        - frame_5: QFrame
                                                            - (Layout): QGridLayout
                                                                    - treeWidget_prescribed_dof: QTreeWidget
                                                        - frame_3: QFrame
                                                            - (Layout): QGridLayout
                                                                    - pushButton_reset: QPushButton
                                                                    - pushButton_remove: QPushButton
                - frame_buttons: QFrame
                    - (Layout): QGridLayout
                            - pushButton_apply_and_close: QPushButton
                            - pushButton_apply: QPushButton
                            - pushButton_cancel: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
