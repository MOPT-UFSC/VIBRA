# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'prescribed_dofs_input.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
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
        Dialog.setWindowModality(Qt.WindowModal)
        Dialog.resize(460, 500)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(460, 500))
        Dialog.setMaximumSize(QSize(460, 540))
        font = QFont()
        font.setPointSize(11)
        font.setBold(False)
        Dialog.setFont(font)
        Dialog.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.gridLayout_7 = QGridLayout(Dialog)
        self.gridLayout_7.setSpacing(4)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(4, 4, 4, 4)
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(380, 48))
        self.frame.setMaximumSize(QSize(16777215, 48))
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setFrameShadow(QFrame.Raised)
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
        self.label.setTextFormat(Qt.AutoText)
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout_6.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout_7.addWidget(self.frame, 0, 0, 1, 1)

        self.frame_2 = QFrame(Dialog)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(380, 395))
        self.frame_2.setMaximumSize(QSize(16777215, 480))
        self.frame_2.setFrameShape(QFrame.Box)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_2)
        self.gridLayout_4.setSpacing(2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(2, 4, 2, 2)
        self.frame_4 = QFrame(self.frame_2)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(360, 72))
        self.frame_4.setMaximumSize(QSize(16777215, 72))
        self.frame_4.setFrameShape(QFrame.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_4)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setHorizontalSpacing(6)
        self.gridLayout_5.setVerticalSpacing(2)
        self.gridLayout_5.setContentsMargins(2, 2, 2, 2)
        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_6, 0, 0, 1, 1)

        self.lineEdit_selection_id = QLineEdit(self.frame_4)
        self.lineEdit_selection_id.setObjectName(u"lineEdit_selection_id")
        self.lineEdit_selection_id.setMinimumSize(QSize(120, 28))
        self.lineEdit_selection_id.setMaximumSize(QSize(140, 28))
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        self.lineEdit_selection_id.setFont(font2)
        self.lineEdit_selection_id.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_selection_id.setStyleSheet(u"")
        self.lineEdit_selection_id.setAlignment(Qt.AlignCenter)

        self.gridLayout_5.addWidget(self.lineEdit_selection_id, 0, 2, 1, 1)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_9, 0, 4, 1, 1)

        self.label_2 = QLabel(self.frame_4)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(100, 28))
        self.label_2.setMaximumSize(QSize(100, 28))
        self.label_2.setFont(font2)
        self.label_2.setAlignment(Qt.AlignCenter)

        self.gridLayout_5.addWidget(self.label_2, 0, 1, 1, 1)

        self.label_3 = QLabel(self.frame_4)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(100, 28))
        self.label_3.setMaximumSize(QSize(100, 28))
        self.label_3.setFont(font2)
        self.label_3.setAlignment(Qt.AlignCenter)

        self.gridLayout_5.addWidget(self.label_3, 1, 1, 1, 1)

        self.comboBox_element_type = QComboBox(self.frame_4)
        self.comboBox_element_type.addItem("")
        self.comboBox_element_type.addItem("")
        self.comboBox_element_type.setObjectName(u"comboBox_element_type")
        self.comboBox_element_type.setMinimumSize(QSize(120, 28))
        self.comboBox_element_type.setMaximumSize(QSize(140, 28))
        font3 = QFont()
        font3.setPointSize(10)
        self.comboBox_element_type.setFont(font3)

        self.gridLayout_5.addWidget(self.comboBox_element_type, 1, 2, 1, 1)

        self.comboBox_attribution_type = QComboBox(self.frame_4)
        self.comboBox_attribution_type.addItem("")
        self.comboBox_attribution_type.addItem("")
        self.comboBox_attribution_type.addItem("")
        self.comboBox_attribution_type.addItem("")
        self.comboBox_attribution_type.setObjectName(u"comboBox_attribution_type")
        self.comboBox_attribution_type.setMinimumSize(QSize(0, 28))
        self.comboBox_attribution_type.setMaximumSize(QSize(16777215, 28))
        self.comboBox_attribution_type.setFont(font3)

        self.gridLayout_5.addWidget(self.comboBox_attribution_type, 0, 3, 1, 1)


        self.gridLayout_4.addWidget(self.frame_4, 0, 0, 1, 1)

        self.frame_6 = QFrame(self.frame_2)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.NoFrame)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.gridLayout_13 = QGridLayout(self.frame_6)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_13.setContentsMargins(4, 4, 4, 8)
        self.tabWidget_main = QTabWidget(self.frame_6)
        self.tabWidget_main.setObjectName(u"tabWidget_main")
        self.tabWidget_main.setMinimumSize(QSize(360, 0))
        self.tabWidget_main.setMaximumSize(QSize(420, 16777215))
        self.tabWidget_main.setFont(font3)
        self.tab_constant_values = QWidget()
        self.tab_constant_values.setObjectName(u"tab_constant_values")
        self.gridLayout_12 = QGridLayout(self.tab_constant_values)
        self.gridLayout_12.setSpacing(2)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setContentsMargins(2, 2, 2, 2)
        self.frame_8 = QFrame(self.tab_constant_values)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setMinimumSize(QSize(340, 250))
        self.frame_8.setMaximumSize(QSize(16777215, 320))
        font4 = QFont()
        font4.setPointSize(11)
        self.frame_8.setFont(font4)
        self.frame_8.setFrameShape(QFrame.NoFrame)
        self.frame_8.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame_8)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(8)
        self.gridLayout.setVerticalSpacing(6)
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.label_Ux_constant = QLabel(self.frame_8)
        self.label_Ux_constant.setObjectName(u"label_Ux_constant")
        self.label_Ux_constant.setMinimumSize(QSize(70, 26))
        self.label_Ux_constant.setMaximumSize(QSize(70, 26))
        self.label_Ux_constant.setFont(font2)
        self.label_Ux_constant.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_Ux_constant, 3, 1, 1, 1)

        self.label_Ry_constant = QLabel(self.frame_8)
        self.label_Ry_constant.setObjectName(u"label_Ry_constant")
        self.label_Ry_constant.setMinimumSize(QSize(70, 26))
        self.label_Ry_constant.setMaximumSize(QSize(70, 26))
        self.label_Ry_constant.setFont(font3)
        self.label_Ry_constant.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_Ry_constant, 7, 1, 1, 1)

        self.lineEdit_real_rx = QLineEdit(self.frame_8)
        self.lineEdit_real_rx.setObjectName(u"lineEdit_real_rx")
        self.lineEdit_real_rx.setMinimumSize(QSize(80, 26))
        self.lineEdit_real_rx.setMaximumSize(QSize(80, 26))
        font5 = QFont()
        font5.setPointSize(10)
        font5.setBold(False)
        self.lineEdit_real_rx.setFont(font5)
        self.lineEdit_real_rx.setStyleSheet(u"")
        self.lineEdit_real_rx.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_real_rx, 6, 2, 1, 1)

        self.label_Rz_constant = QLabel(self.frame_8)
        self.label_Rz_constant.setObjectName(u"label_Rz_constant")
        self.label_Rz_constant.setMinimumSize(QSize(70, 26))
        self.label_Rz_constant.setMaximumSize(QSize(70, 26))
        self.label_Rz_constant.setFont(font3)
        self.label_Rz_constant.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_Rz_constant, 8, 1, 1, 1)

        self.lineEdit_real_ry = QLineEdit(self.frame_8)
        self.lineEdit_real_ry.setObjectName(u"lineEdit_real_ry")
        self.lineEdit_real_ry.setMinimumSize(QSize(80, 26))
        self.lineEdit_real_ry.setMaximumSize(QSize(80, 26))
        self.lineEdit_real_ry.setFont(font5)
        self.lineEdit_real_ry.setStyleSheet(u"")
        self.lineEdit_real_ry.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_real_ry, 7, 2, 1, 1)

        self.label_Rx_constant = QLabel(self.frame_8)
        self.label_Rx_constant.setObjectName(u"label_Rx_constant")
        self.label_Rx_constant.setMinimumSize(QSize(70, 26))
        self.label_Rx_constant.setMaximumSize(QSize(70, 26))
        self.label_Rx_constant.setFont(font3)
        self.label_Rx_constant.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_Rx_constant, 6, 1, 1, 1)

        self.lineEdit_imag_ry = QLineEdit(self.frame_8)
        self.lineEdit_imag_ry.setObjectName(u"lineEdit_imag_ry")
        self.lineEdit_imag_ry.setMinimumSize(QSize(80, 26))
        self.lineEdit_imag_ry.setMaximumSize(QSize(80, 26))
        self.lineEdit_imag_ry.setFont(font5)
        self.lineEdit_imag_ry.setStyleSheet(u"")
        self.lineEdit_imag_ry.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_imag_ry, 7, 3, 1, 1)

        self.lineEdit_imag_rz = QLineEdit(self.frame_8)
        self.lineEdit_imag_rz.setObjectName(u"lineEdit_imag_rz")
        self.lineEdit_imag_rz.setMinimumSize(QSize(80, 26))
        self.lineEdit_imag_rz.setMaximumSize(QSize(80, 26))
        self.lineEdit_imag_rz.setFont(font5)
        self.lineEdit_imag_rz.setStyleSheet(u"")
        self.lineEdit_imag_rz.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_imag_rz, 8, 3, 1, 1)

        self.lineEdit_imag_rx = QLineEdit(self.frame_8)
        self.lineEdit_imag_rx.setObjectName(u"lineEdit_imag_rx")
        self.lineEdit_imag_rx.setMinimumSize(QSize(80, 26))
        self.lineEdit_imag_rx.setMaximumSize(QSize(80, 26))
        self.lineEdit_imag_rx.setFont(font5)
        self.lineEdit_imag_rx.setStyleSheet(u"")
        self.lineEdit_imag_rx.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_imag_rx, 6, 3, 1, 1)

        self.lineEdit_real_rz = QLineEdit(self.frame_8)
        self.lineEdit_real_rz.setObjectName(u"lineEdit_real_rz")
        self.lineEdit_real_rz.setMinimumSize(QSize(80, 26))
        self.lineEdit_real_rz.setMaximumSize(QSize(80, 26))
        self.lineEdit_real_rz.setFont(font5)
        self.lineEdit_real_rz.setStyleSheet(u"")
        self.lineEdit_real_rz.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_real_rz, 8, 2, 1, 1)

        self.label_Rx_unit = QLabel(self.frame_8)
        self.label_Rx_unit.setObjectName(u"label_Rx_unit")
        self.label_Rx_unit.setMinimumSize(QSize(50, 26))
        self.label_Rx_unit.setMaximumSize(QSize(50, 26))
        font6 = QFont()
        font6.setPointSize(10)
        font6.setBold(False)
        font6.setItalic(False)
        self.label_Rx_unit.setFont(font6)
        self.label_Rx_unit.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_Rx_unit, 6, 4, 1, 1)

        self.label_Ry_unit = QLabel(self.frame_8)
        self.label_Ry_unit.setObjectName(u"label_Ry_unit")
        self.label_Ry_unit.setMinimumSize(QSize(50, 26))
        self.label_Ry_unit.setMaximumSize(QSize(50, 26))
        self.label_Ry_unit.setFont(font6)
        self.label_Ry_unit.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_Ry_unit, 7, 4, 1, 1)

        self.label_Rz_unit = QLabel(self.frame_8)
        self.label_Rz_unit.setObjectName(u"label_Rz_unit")
        self.label_Rz_unit.setMinimumSize(QSize(50, 26))
        self.label_Rz_unit.setMaximumSize(QSize(50, 26))
        self.label_Rz_unit.setFont(font6)
        self.label_Rz_unit.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_Rz_unit, 8, 4, 1, 1)

        self.label_18 = QLabel(self.frame_8)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setMinimumSize(QSize(70, 26))
        self.label_18.setMaximumSize(QSize(70, 26))
        self.label_18.setFont(font2)
        self.label_18.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_18, 9, 1, 1, 1)

        self.lineEdit_imag_uz = QLineEdit(self.frame_8)
        self.lineEdit_imag_uz.setObjectName(u"lineEdit_imag_uz")
        self.lineEdit_imag_uz.setMinimumSize(QSize(80, 26))
        self.lineEdit_imag_uz.setMaximumSize(QSize(80, 26))
        self.lineEdit_imag_uz.setFont(font2)
        self.lineEdit_imag_uz.setStyleSheet(u"")
        self.lineEdit_imag_uz.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_imag_uz, 5, 3, 1, 1)

        self.lineEdit_real_alldofs = QLineEdit(self.frame_8)
        self.lineEdit_real_alldofs.setObjectName(u"lineEdit_real_alldofs")
        self.lineEdit_real_alldofs.setMinimumSize(QSize(80, 26))
        self.lineEdit_real_alldofs.setMaximumSize(QSize(80, 26))
        self.lineEdit_real_alldofs.setFont(font2)
        self.lineEdit_real_alldofs.setStyleSheet(u"")
        self.lineEdit_real_alldofs.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_real_alldofs, 9, 2, 1, 1)

        self.label_Uz_unit = QLabel(self.frame_8)
        self.label_Uz_unit.setObjectName(u"label_Uz_unit")
        self.label_Uz_unit.setMinimumSize(QSize(50, 26))
        self.label_Uz_unit.setMaximumSize(QSize(50, 26))
        self.label_Uz_unit.setFont(font2)
        self.label_Uz_unit.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_Uz_unit, 5, 4, 1, 1)

        self.lineEdit_imag_alldofs = QLineEdit(self.frame_8)
        self.lineEdit_imag_alldofs.setObjectName(u"lineEdit_imag_alldofs")
        self.lineEdit_imag_alldofs.setMinimumSize(QSize(80, 26))
        self.lineEdit_imag_alldofs.setMaximumSize(QSize(80, 26))
        self.lineEdit_imag_alldofs.setFont(font2)
        self.lineEdit_imag_alldofs.setStyleSheet(u"")
        self.lineEdit_imag_alldofs.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_imag_alldofs, 9, 3, 1, 1)

        self.label_21 = QLabel(self.frame_8)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setMinimumSize(QSize(50, 26))
        self.label_21.setMaximumSize(QSize(50, 26))
        self.label_21.setFont(font2)
        self.label_21.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_21, 9, 4, 1, 1)

        self.label_Uy_constant = QLabel(self.frame_8)
        self.label_Uy_constant.setObjectName(u"label_Uy_constant")
        self.label_Uy_constant.setMinimumSize(QSize(70, 26))
        self.label_Uy_constant.setMaximumSize(QSize(70, 26))
        self.label_Uy_constant.setFont(font2)
        self.label_Uy_constant.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_Uy_constant, 4, 1, 1, 1)

        self.lineEdit_imag_ux = QLineEdit(self.frame_8)
        self.lineEdit_imag_ux.setObjectName(u"lineEdit_imag_ux")
        self.lineEdit_imag_ux.setMinimumSize(QSize(80, 26))
        self.lineEdit_imag_ux.setMaximumSize(QSize(80, 26))
        self.lineEdit_imag_ux.setFont(font2)
        self.lineEdit_imag_ux.setStyleSheet(u"")
        self.lineEdit_imag_ux.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_imag_ux, 3, 3, 1, 1)

        self.lineEdit_real_ux = QLineEdit(self.frame_8)
        self.lineEdit_real_ux.setObjectName(u"lineEdit_real_ux")
        self.lineEdit_real_ux.setMinimumSize(QSize(80, 26))
        self.lineEdit_real_ux.setMaximumSize(QSize(80, 26))
        self.lineEdit_real_ux.setFont(font2)
        self.lineEdit_real_ux.setStyleSheet(u"")
        self.lineEdit_real_ux.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_real_ux, 3, 2, 1, 1)

        self.lineEdit_imag_uy = QLineEdit(self.frame_8)
        self.lineEdit_imag_uy.setObjectName(u"lineEdit_imag_uy")
        self.lineEdit_imag_uy.setMinimumSize(QSize(80, 26))
        self.lineEdit_imag_uy.setMaximumSize(QSize(80, 26))
        self.lineEdit_imag_uy.setFont(font2)
        self.lineEdit_imag_uy.setStyleSheet(u"")
        self.lineEdit_imag_uy.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_imag_uy, 4, 3, 1, 1)

        self.label_Uz_constant = QLabel(self.frame_8)
        self.label_Uz_constant.setObjectName(u"label_Uz_constant")
        self.label_Uz_constant.setMinimumSize(QSize(70, 26))
        self.label_Uz_constant.setMaximumSize(QSize(70, 26))
        self.label_Uz_constant.setFont(font2)
        self.label_Uz_constant.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_Uz_constant, 5, 1, 1, 1)

        self.label_Uy_unit = QLabel(self.frame_8)
        self.label_Uy_unit.setObjectName(u"label_Uy_unit")
        self.label_Uy_unit.setMinimumSize(QSize(50, 26))
        self.label_Uy_unit.setMaximumSize(QSize(50, 26))
        self.label_Uy_unit.setFont(font2)
        self.label_Uy_unit.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_Uy_unit, 4, 4, 1, 1)

        self.label_Ux_unit = QLabel(self.frame_8)
        self.label_Ux_unit.setObjectName(u"label_Ux_unit")
        self.label_Ux_unit.setMinimumSize(QSize(50, 26))
        self.label_Ux_unit.setMaximumSize(QSize(50, 26))
        self.label_Ux_unit.setFont(font2)
        self.label_Ux_unit.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_Ux_unit, 3, 4, 1, 1)

        self.lineEdit_real_uz = QLineEdit(self.frame_8)
        self.lineEdit_real_uz.setObjectName(u"lineEdit_real_uz")
        self.lineEdit_real_uz.setMinimumSize(QSize(80, 26))
        self.lineEdit_real_uz.setMaximumSize(QSize(80, 26))
        self.lineEdit_real_uz.setFont(font2)
        self.lineEdit_real_uz.setStyleSheet(u"")
        self.lineEdit_real_uz.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_real_uz, 5, 2, 1, 1)

        self.lineEdit_real_uy = QLineEdit(self.frame_8)
        self.lineEdit_real_uy.setObjectName(u"lineEdit_real_uy")
        self.lineEdit_real_uy.setMinimumSize(QSize(80, 26))
        self.lineEdit_real_uy.setMaximumSize(QSize(80, 26))
        self.lineEdit_real_uy.setFont(font2)
        self.lineEdit_real_uy.setStyleSheet(u"")
        self.lineEdit_real_uy.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_real_uy, 4, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 3, 5, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 3, 0, 1, 1)

        self.label_4 = QLabel(self.frame_8)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(80, 26))
        self.label_4.setMaximumSize(QSize(80, 26))
        self.label_4.setFont(font2)
        self.label_4.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_4, 2, 2, 1, 1)

        self.label_20 = QLabel(self.frame_8)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setMinimumSize(QSize(80, 26))
        self.label_20.setMaximumSize(QSize(80, 26))
        self.label_20.setFont(font2)
        self.label_20.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_20, 2, 3, 1, 1)


        self.gridLayout_12.addWidget(self.frame_8, 1, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_12.addItem(self.verticalSpacer, 0, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_12.addItem(self.verticalSpacer_2, 2, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_constant_values, "")
        self.tab_load_tables = QWidget()
        self.tab_load_tables.setObjectName(u"tab_load_tables")
        self.gridLayout_10 = QGridLayout(self.tab_load_tables)
        self.gridLayout_10.setSpacing(2)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(2, 2, 2, 2)
        self.frame_9 = QFrame(self.tab_load_tables)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setFrameShape(QFrame.NoFrame)
        self.frame_9.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_9)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setHorizontalSpacing(4)
        self.gridLayout_3.setVerticalSpacing(7)
        self.gridLayout_3.setContentsMargins(4, 4, 4, 2)
        self.lineEdit_path_table_ry = QLineEdit(self.frame_9)
        self.lineEdit_path_table_ry.setObjectName(u"lineEdit_path_table_ry")
        self.lineEdit_path_table_ry.setEnabled(False)
        self.lineEdit_path_table_ry.setMinimumSize(QSize(210, 26))
        self.lineEdit_path_table_ry.setMaximumSize(QSize(240, 26))
        self.lineEdit_path_table_ry.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.lineEdit_path_table_ry, 4, 1, 1, 1)

        self.pushButton_load_ry_table = QPushButton(self.frame_9)
        self.pushButton_load_ry_table.setObjectName(u"pushButton_load_ry_table")
        self.pushButton_load_ry_table.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton_load_ry_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_ry_table.setSizePolicy(sizePolicy1)
        self.pushButton_load_ry_table.setMinimumSize(QSize(62, 26))
        self.pushButton_load_ry_table.setMaximumSize(QSize(62, 26))
        self.pushButton_load_ry_table.setFont(font3)
        self.pushButton_load_ry_table.setStyleSheet(u"")

        self.gridLayout_3.addWidget(self.pushButton_load_ry_table, 4, 2, 1, 1)

        self.label_Ry_table = QLabel(self.frame_9)
        self.label_Ry_table.setObjectName(u"label_Ry_table")
        self.label_Ry_table.setEnabled(True)
        self.label_Ry_table.setMinimumSize(QSize(0, 26))
        self.label_Ry_table.setMaximumSize(QSize(38, 26))
        self.label_Ry_table.setFont(font3)
        self.label_Ry_table.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_Ry_table, 4, 0, 1, 1)

        self.label_Rz_table = QLabel(self.frame_9)
        self.label_Rz_table.setObjectName(u"label_Rz_table")
        self.label_Rz_table.setEnabled(True)
        self.label_Rz_table.setMinimumSize(QSize(0, 26))
        self.label_Rz_table.setMaximumSize(QSize(38, 26))
        self.label_Rz_table.setFont(font3)
        self.label_Rz_table.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_Rz_table, 5, 0, 1, 1)

        self.lineEdit_path_table_rz = QLineEdit(self.frame_9)
        self.lineEdit_path_table_rz.setObjectName(u"lineEdit_path_table_rz")
        self.lineEdit_path_table_rz.setEnabled(False)
        self.lineEdit_path_table_rz.setMinimumSize(QSize(210, 26))
        self.lineEdit_path_table_rz.setMaximumSize(QSize(240, 26))
        self.lineEdit_path_table_rz.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.lineEdit_path_table_rz, 5, 1, 1, 1)

        self.lineEdit_path_table_uy = QLineEdit(self.frame_9)
        self.lineEdit_path_table_uy.setObjectName(u"lineEdit_path_table_uy")
        self.lineEdit_path_table_uy.setEnabled(False)
        self.lineEdit_path_table_uy.setMinimumSize(QSize(210, 26))
        self.lineEdit_path_table_uy.setMaximumSize(QSize(240, 26))
        self.lineEdit_path_table_uy.setStyleSheet(u"")
        self.lineEdit_path_table_uy.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.lineEdit_path_table_uy, 1, 1, 1, 1)

        self.pushButton_load_uz_table = QPushButton(self.frame_9)
        self.pushButton_load_uz_table.setObjectName(u"pushButton_load_uz_table")
        self.pushButton_load_uz_table.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.pushButton_load_uz_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_uz_table.setSizePolicy(sizePolicy1)
        self.pushButton_load_uz_table.setMinimumSize(QSize(62, 26))
        self.pushButton_load_uz_table.setMaximumSize(QSize(62, 26))
        self.pushButton_load_uz_table.setFont(font3)
        self.pushButton_load_uz_table.setStyleSheet(u"")

        self.gridLayout_3.addWidget(self.pushButton_load_uz_table, 2, 2, 1, 1)

        self.pushButton_load_uy_table = QPushButton(self.frame_9)
        self.pushButton_load_uy_table.setObjectName(u"pushButton_load_uy_table")
        self.pushButton_load_uy_table.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.pushButton_load_uy_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_uy_table.setSizePolicy(sizePolicy1)
        self.pushButton_load_uy_table.setMinimumSize(QSize(62, 26))
        self.pushButton_load_uy_table.setMaximumSize(QSize(62, 26))
        self.pushButton_load_uy_table.setFont(font3)
        self.pushButton_load_uy_table.setStyleSheet(u"")

        self.gridLayout_3.addWidget(self.pushButton_load_uy_table, 1, 2, 1, 1)

        self.pushButton_load_rx_table = QPushButton(self.frame_9)
        self.pushButton_load_rx_table.setObjectName(u"pushButton_load_rx_table")
        self.pushButton_load_rx_table.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.pushButton_load_rx_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_rx_table.setSizePolicy(sizePolicy1)
        self.pushButton_load_rx_table.setMinimumSize(QSize(62, 26))
        self.pushButton_load_rx_table.setMaximumSize(QSize(62, 26))
        self.pushButton_load_rx_table.setFont(font3)
        self.pushButton_load_rx_table.setStyleSheet(u"")

        self.gridLayout_3.addWidget(self.pushButton_load_rx_table, 3, 2, 1, 1)

        self.label_Ux_table = QLabel(self.frame_9)
        self.label_Ux_table.setObjectName(u"label_Ux_table")
        self.label_Ux_table.setEnabled(True)
        self.label_Ux_table.setMinimumSize(QSize(0, 26))
        self.label_Ux_table.setMaximumSize(QSize(38, 26))
        self.label_Ux_table.setFont(font3)
        self.label_Ux_table.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_Ux_table, 0, 0, 1, 1)

        self.lineEdit_path_table_rx = QLineEdit(self.frame_9)
        self.lineEdit_path_table_rx.setObjectName(u"lineEdit_path_table_rx")
        self.lineEdit_path_table_rx.setEnabled(False)
        self.lineEdit_path_table_rx.setMinimumSize(QSize(210, 26))
        self.lineEdit_path_table_rx.setMaximumSize(QSize(240, 26))
        self.lineEdit_path_table_rx.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.lineEdit_path_table_rx, 3, 1, 1, 1)

        self.label_Rx_table = QLabel(self.frame_9)
        self.label_Rx_table.setObjectName(u"label_Rx_table")
        self.label_Rx_table.setEnabled(True)
        self.label_Rx_table.setMinimumSize(QSize(0, 26))
        self.label_Rx_table.setMaximumSize(QSize(38, 26))
        self.label_Rx_table.setFont(font3)
        self.label_Rx_table.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_Rx_table, 3, 0, 1, 1)

        self.lineEdit_path_table_uz = QLineEdit(self.frame_9)
        self.lineEdit_path_table_uz.setObjectName(u"lineEdit_path_table_uz")
        self.lineEdit_path_table_uz.setEnabled(False)
        self.lineEdit_path_table_uz.setMinimumSize(QSize(210, 26))
        self.lineEdit_path_table_uz.setMaximumSize(QSize(240, 26))
        self.lineEdit_path_table_uz.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.lineEdit_path_table_uz, 2, 1, 1, 1)

        self.label_Uy_table = QLabel(self.frame_9)
        self.label_Uy_table.setObjectName(u"label_Uy_table")
        self.label_Uy_table.setEnabled(True)
        self.label_Uy_table.setMinimumSize(QSize(0, 26))
        self.label_Uy_table.setMaximumSize(QSize(38, 26))
        self.label_Uy_table.setFont(font3)
        self.label_Uy_table.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_Uy_table, 1, 0, 1, 1)

        self.pushButton_load_rz_table = QPushButton(self.frame_9)
        self.pushButton_load_rz_table.setObjectName(u"pushButton_load_rz_table")
        self.pushButton_load_rz_table.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.pushButton_load_rz_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_rz_table.setSizePolicy(sizePolicy1)
        self.pushButton_load_rz_table.setMinimumSize(QSize(62, 26))
        self.pushButton_load_rz_table.setMaximumSize(QSize(62, 26))
        self.pushButton_load_rz_table.setFont(font3)
        self.pushButton_load_rz_table.setStyleSheet(u"")

        self.gridLayout_3.addWidget(self.pushButton_load_rz_table, 5, 2, 1, 1)

        self.lineEdit_path_table_ux = QLineEdit(self.frame_9)
        self.lineEdit_path_table_ux.setObjectName(u"lineEdit_path_table_ux")
        self.lineEdit_path_table_ux.setEnabled(False)
        self.lineEdit_path_table_ux.setMinimumSize(QSize(210, 26))
        self.lineEdit_path_table_ux.setMaximumSize(QSize(240, 26))
        self.lineEdit_path_table_ux.setStyleSheet(u"")
        self.lineEdit_path_table_ux.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.lineEdit_path_table_ux, 0, 1, 1, 1)

        self.label_Uz_table = QLabel(self.frame_9)
        self.label_Uz_table.setObjectName(u"label_Uz_table")
        self.label_Uz_table.setEnabled(True)
        self.label_Uz_table.setMinimumSize(QSize(0, 26))
        self.label_Uz_table.setMaximumSize(QSize(38, 26))
        self.label_Uz_table.setFont(font3)
        self.label_Uz_table.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_Uz_table, 2, 0, 1, 1)

        self.pushButton_load_ux_table = QPushButton(self.frame_9)
        self.pushButton_load_ux_table.setObjectName(u"pushButton_load_ux_table")
        self.pushButton_load_ux_table.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.pushButton_load_ux_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_ux_table.setSizePolicy(sizePolicy1)
        self.pushButton_load_ux_table.setMinimumSize(QSize(62, 26))
        self.pushButton_load_ux_table.setMaximumSize(QSize(62, 26))
        self.pushButton_load_ux_table.setFont(font3)
        self.pushButton_load_ux_table.setStyleSheet(u"")

        self.gridLayout_3.addWidget(self.pushButton_load_ux_table, 0, 2, 1, 1)


        self.gridLayout_10.addWidget(self.frame_9, 3, 0, 1, 1)

        self.frame_16 = QFrame(self.tab_load_tables)
        self.frame_16.setObjectName(u"frame_16")
        self.frame_16.setMinimumSize(QSize(0, 48))
        self.frame_16.setMaximumSize(QSize(16777215, 48))
        self.frame_16.setFont(font3)
        self.frame_16.setFrameShape(QFrame.NoFrame)
        self.frame_16.setFrameShadow(QFrame.Raised)
        self.gridLayout_19 = QGridLayout(self.frame_16)
        self.gridLayout_19.setObjectName(u"gridLayout_19")
        self.gridLayout_19.setHorizontalSpacing(6)
        self.gridLayout_19.setContentsMargins(6, 0, 6, 0)
        self.label_angular = QLabel(self.frame_16)
        self.label_angular.setObjectName(u"label_angular")
        self.label_angular.setFont(font3)
        self.label_angular.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_19.addWidget(self.label_angular, 0, 4, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_19.addItem(self.horizontalSpacer_8, 0, 0, 1, 1)

        self.comboBox_linear_data_type = QComboBox(self.frame_16)
        self.comboBox_linear_data_type.addItem("")
        self.comboBox_linear_data_type.addItem("")
        self.comboBox_linear_data_type.addItem("")
        self.comboBox_linear_data_type.setObjectName(u"comboBox_linear_data_type")
        self.comboBox_linear_data_type.setFont(font3)

        self.gridLayout_19.addWidget(self.comboBox_linear_data_type, 0, 2, 1, 1)

        self.label_linear = QLabel(self.frame_16)
        self.label_linear.setObjectName(u"label_linear")
        self.label_linear.setFont(font3)
        self.label_linear.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_19.addWidget(self.label_linear, 0, 1, 1, 1)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_19.addItem(self.horizontalSpacer_12, 0, 6, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_19.addItem(self.horizontalSpacer_3, 0, 3, 1, 1)

        self.comboBox_angular_data_type = QComboBox(self.frame_16)
        self.comboBox_angular_data_type.addItem("")
        self.comboBox_angular_data_type.addItem("")
        self.comboBox_angular_data_type.addItem("")
        self.comboBox_angular_data_type.setObjectName(u"comboBox_angular_data_type")
        self.comboBox_angular_data_type.setFont(font3)

        self.gridLayout_19.addWidget(self.comboBox_angular_data_type, 0, 5, 1, 1)


        self.gridLayout_10.addWidget(self.frame_16, 1, 0, 1, 1)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_10.addItem(self.verticalSpacer_6, 4, 0, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_10.addItem(self.verticalSpacer_4, 0, 0, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_10.addItem(self.verticalSpacer_3, 2, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_load_tables, "")
        self.tab_list = QWidget()
        self.tab_list.setObjectName(u"tab_list")
        self.gridLayout_9 = QGridLayout(self.tab_list)
        self.gridLayout_9.setSpacing(2)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(2, 2, 2, 2)
        self.frame_5 = QFrame(self.tab_list)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_5)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.treeWidget_prescribed_dofs = QTreeWidget(self.frame_5)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(2, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter);
        self.treeWidget_prescribed_dofs.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_prescribed_dofs.setObjectName(u"treeWidget_prescribed_dofs")
        self.treeWidget_prescribed_dofs.setMinimumSize(QSize(320, 170))
        self.treeWidget_prescribed_dofs.setMaximumSize(QSize(380, 200))
        font7 = QFont()
        font7.setFamilies([u"MS Shell Dlg 2"])
        font7.setPointSize(10)
        font7.setItalic(False)
        self.treeWidget_prescribed_dofs.setFont(font7)
        self.treeWidget_prescribed_dofs.setIndentation(1)
        self.treeWidget_prescribed_dofs.setHeaderHidden(False)
        self.treeWidget_prescribed_dofs.header().setHighlightSections(False)
        self.treeWidget_prescribed_dofs.header().setProperty(u"showSortIndicator", False)
        self.treeWidget_prescribed_dofs.header().setStretchLastSection(True)

        self.gridLayout_2.addWidget(self.treeWidget_prescribed_dofs, 0, 0, 1, 1)


        self.gridLayout_9.addWidget(self.frame_5, 0, 0, 1, 1)

        self.frame_3 = QFrame(self.tab_list)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(320, 48))
        self.frame_3.setMaximumSize(QSize(16777215, 48))
        self.frame_3.setFrameShape(QFrame.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.gridLayout_8 = QGridLayout(self.frame_3)
        self.gridLayout_8.setSpacing(4)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(4, 4, 4, 4)
        self.pushButton_reset = QPushButton(self.frame_3)
        self.pushButton_reset.setObjectName(u"pushButton_reset")
        self.pushButton_reset.setMinimumSize(QSize(100, 28))
        self.pushButton_reset.setMaximumSize(QSize(100, 28))
        self.pushButton_reset.setFont(font2)
        self.pushButton_reset.setStyleSheet(u"")

        self.gridLayout_8.addWidget(self.pushButton_reset, 0, 0, 1, 1)

        self.pushButton_remove = QPushButton(self.frame_3)
        self.pushButton_remove.setObjectName(u"pushButton_remove")
        self.pushButton_remove.setMinimumSize(QSize(100, 28))
        self.pushButton_remove.setMaximumSize(QSize(100, 28))
        self.pushButton_remove.setFont(font2)
        self.pushButton_remove.setStyleSheet(u"")

        self.gridLayout_8.addWidget(self.pushButton_remove, 0, 1, 1, 1)


        self.gridLayout_9.addWidget(self.frame_3, 1, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_list, "")

        self.gridLayout_13.addWidget(self.tabWidget_main, 0, 0, 1, 1)


        self.gridLayout_4.addWidget(self.frame_6, 1, 0, 1, 1)


        self.gridLayout_7.addWidget(self.frame_2, 1, 0, 1, 1)

        self.frame_7 = QFrame(Dialog)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setMinimumSize(QSize(340, 48))
        self.frame_7.setMaximumSize(QSize(16777215, 48))
        self.frame_7.setFrameShape(QFrame.NoFrame)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.gridLayout_11 = QGridLayout(self.frame_7)
        self.gridLayout_11.setSpacing(0)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setContentsMargins(0, 0, 0, 0)
        self.pushButton_exit = QPushButton(self.frame_7)
        self.pushButton_exit.setObjectName(u"pushButton_exit")
        self.pushButton_exit.setMinimumSize(QSize(100, 28))
        self.pushButton_exit.setMaximumSize(QSize(100, 28))
        self.pushButton_exit.setFont(font3)
        self.pushButton_exit.setStyleSheet(u"")
        self.pushButton_exit.setAutoDefault(False)

        self.gridLayout_11.addWidget(self.pushButton_exit, 0, 0, 1, 1)

        self.pushButton_attribute = QPushButton(self.frame_7)
        self.pushButton_attribute.setObjectName(u"pushButton_attribute")
        self.pushButton_attribute.setMinimumSize(QSize(100, 28))
        self.pushButton_attribute.setMaximumSize(QSize(100, 28))
        self.pushButton_attribute.setFont(font3)
        self.pushButton_attribute.setStyleSheet(u"")
        self.pushButton_attribute.setAutoDefault(False)

        self.gridLayout_11.addWidget(self.pushButton_attribute, 0, 1, 1, 1)


        self.gridLayout_7.addWidget(self.frame_7, 2, 0, 1, 1)


        self.retranslateUi(Dialog)

        self.tabWidget_main.setCurrentIndex(0)
        self.pushButton_attribute.setDefault(True)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Set a boundary condition", None))
#if QT_CONFIG(whatsthis)
        Dialog.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.label.setText(QCoreApplication.translate("Dialog", u"Degrees of freedom prescription setup", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Selection ID:", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Element type:", None))
        self.comboBox_element_type.setItemText(0, QCoreApplication.translate("Dialog", u" Face element", None))
        self.comboBox_element_type.setItemText(1, QCoreApplication.translate("Dialog", u" Solid element", None))

        self.comboBox_attribution_type.setItemText(0, QCoreApplication.translate("Dialog", u"Selected faces", None))
        self.comboBox_attribution_type.setItemText(1, QCoreApplication.translate("Dialog", u"Selected lines", None))
        self.comboBox_attribution_type.setItemText(2, QCoreApplication.translate("Dialog", u"Selected points", None))
        self.comboBox_attribution_type.setItemText(3, QCoreApplication.translate("Dialog", u"Selected nodes", None))

        self.label_Ux_constant.setText(QCoreApplication.translate("Dialog", u"Ux:", None))
        self.label_Ry_constant.setText(QCoreApplication.translate("Dialog", u"Ry:", None))
        self.label_Rz_constant.setText(QCoreApplication.translate("Dialog", u"Rz:", None))
        self.label_Rx_constant.setText(QCoreApplication.translate("Dialog", u"Rx:", None))
        self.label_Rx_unit.setText(QCoreApplication.translate("Dialog", u"[rad]", None))
        self.label_Ry_unit.setText(QCoreApplication.translate("Dialog", u"[rad]", None))
        self.label_Rz_unit.setText(QCoreApplication.translate("Dialog", u"[rad]", None))
        self.label_18.setText(QCoreApplication.translate("Dialog", u"All dofs:", None))
        self.label_Uz_unit.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.label_21.setText(QCoreApplication.translate("Dialog", u"[--]", None))
        self.label_Uy_constant.setText(QCoreApplication.translate("Dialog", u"Uy:", None))
        self.lineEdit_real_ux.setText("")
        self.label_Uz_constant.setText(QCoreApplication.translate("Dialog", u"Uz:", None))
        self.label_Uy_unit.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.label_Ux_unit.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Real", None))
        self.label_20.setText(QCoreApplication.translate("Dialog", u"Imaginary", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_constant_values), QCoreApplication.translate("Dialog", u"Constant values", None))
        self.pushButton_load_ry_table.setText(QCoreApplication.translate("Dialog", u"Search", None))
        self.label_Ry_table.setText(QCoreApplication.translate("Dialog", u"Ry:", None))
        self.label_Rz_table.setText(QCoreApplication.translate("Dialog", u"Rz:", None))
        self.pushButton_load_uz_table.setText(QCoreApplication.translate("Dialog", u"Search", None))
        self.pushButton_load_uy_table.setText(QCoreApplication.translate("Dialog", u"Search", None))
        self.pushButton_load_rx_table.setText(QCoreApplication.translate("Dialog", u"Search", None))
        self.label_Ux_table.setText(QCoreApplication.translate("Dialog", u"Ux:", None))
        self.label_Rx_table.setText(QCoreApplication.translate("Dialog", u"Rx:", None))
        self.label_Uy_table.setText(QCoreApplication.translate("Dialog", u"Uy:", None))
        self.pushButton_load_rz_table.setText(QCoreApplication.translate("Dialog", u"Search", None))
        self.label_Uz_table.setText(QCoreApplication.translate("Dialog", u"Uz:", None))
        self.pushButton_load_ux_table.setText(QCoreApplication.translate("Dialog", u"Search", None))
        self.label_angular.setText(QCoreApplication.translate("Dialog", u"Angular:", None))
        self.comboBox_linear_data_type.setItemText(0, QCoreApplication.translate("Dialog", u" Displacement", None))
        self.comboBox_linear_data_type.setItemText(1, QCoreApplication.translate("Dialog", u" Velocity", None))
        self.comboBox_linear_data_type.setItemText(2, QCoreApplication.translate("Dialog", u" Acceleration", None))

        self.label_linear.setText(QCoreApplication.translate("Dialog", u"Linear:", None))
        self.comboBox_angular_data_type.setItemText(0, QCoreApplication.translate("Dialog", u" Displacement", None))
        self.comboBox_angular_data_type.setItemText(1, QCoreApplication.translate("Dialog", u" Velocity", None))
        self.comboBox_angular_data_type.setItemText(2, QCoreApplication.translate("Dialog", u" Acceleration", None))

        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_load_tables), QCoreApplication.translate("Dialog", u"Load tables", None))
        ___qtreewidgetitem = self.treeWidget_prescribed_dofs.headerItem()
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("Dialog", u"Element type", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"Prescribed DOFs", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Selection-ID", None));
#if QT_CONFIG(tooltip)
        self.treeWidget_prescribed_dofs.setToolTip(QCoreApplication.translate("Dialog", u"Select a node to remove the attributed boundary condition.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_reset.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.pushButton_remove.setText(QCoreApplication.translate("Dialog", u"Remove", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_list), QCoreApplication.translate("Dialog", u"List", None))
        self.pushButton_exit.setText(QCoreApplication.translate("Dialog", u"Exit", None))
        self.pushButton_attribute.setText(QCoreApplication.translate("Dialog", u"Attribute", None))
    # retranslateUi



class PrescribedDofsInput_UI(QDialog, Ui_Dialog):
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
                                        - lineEdit_selection_id: QLineEdit
                                        - label_2: QLabel
                                        - label_3: QLabel
                                        - comboBox_element_type: QComboBox
                                        - comboBox_attribution_type: QComboBox
                            - frame_6: QFrame
                                - (Layout): QGridLayout
                                        - tabWidget_main: QTabWidget
                                            - tab_constant_values: QWidget
                                                - (Layout): QGridLayout
                                                        - frame_8: QFrame
                                                            - (Layout): QGridLayout
                                                                    - label_Ux_constant: QLabel
                                                                    - label_Ry_constant: QLabel
                                                                    - lineEdit_real_rx: QLineEdit
                                                                    - label_Rz_constant: QLabel
                                                                    - lineEdit_real_ry: QLineEdit
                                                                    - label_Rx_constant: QLabel
                                                                    - lineEdit_imag_ry: QLineEdit
                                                                    - lineEdit_imag_rz: QLineEdit
                                                                    - lineEdit_imag_rx: QLineEdit
                                                                    - lineEdit_real_rz: QLineEdit
                                                                    - label_Rx_unit: QLabel
                                                                    - label_Ry_unit: QLabel
                                                                    - label_Rz_unit: QLabel
                                                                    - label_18: QLabel
                                                                    - lineEdit_imag_uz: QLineEdit
                                                                    - lineEdit_real_alldofs: QLineEdit
                                                                    - label_Uz_unit: QLabel
                                                                    - lineEdit_imag_alldofs: QLineEdit
                                                                    - label_21: QLabel
                                                                    - label_Uy_constant: QLabel
                                                                    - lineEdit_imag_ux: QLineEdit
                                                                    - lineEdit_real_ux: QLineEdit
                                                                    - lineEdit_imag_uy: QLineEdit
                                                                    - label_Uz_constant: QLabel
                                                                    - label_Uy_unit: QLabel
                                                                    - label_Ux_unit: QLabel
                                                                    - lineEdit_real_uz: QLineEdit
                                                                    - lineEdit_real_uy: QLineEdit
                                                                    - label_4: QLabel
                                                                    - label_20: QLabel
                                            - tab_load_tables: QWidget
                                                - (Layout): QGridLayout
                                                        - frame_9: QFrame
                                                            - (Layout): QGridLayout
                                                                    - lineEdit_path_table_ry: QLineEdit
                                                                    - pushButton_load_ry_table: QPushButton
                                                                    - label_Ry_table: QLabel
                                                                    - label_Rz_table: QLabel
                                                                    - lineEdit_path_table_rz: QLineEdit
                                                                    - lineEdit_path_table_uy: QLineEdit
                                                                    - pushButton_load_uz_table: QPushButton
                                                                    - pushButton_load_uy_table: QPushButton
                                                                    - pushButton_load_rx_table: QPushButton
                                                                    - label_Ux_table: QLabel
                                                                    - lineEdit_path_table_rx: QLineEdit
                                                                    - label_Rx_table: QLabel
                                                                    - lineEdit_path_table_uz: QLineEdit
                                                                    - label_Uy_table: QLabel
                                                                    - pushButton_load_rz_table: QPushButton
                                                                    - lineEdit_path_table_ux: QLineEdit
                                                                    - label_Uz_table: QLabel
                                                                    - pushButton_load_ux_table: QPushButton
                                                        - frame_16: QFrame
                                                            - (Layout): QGridLayout
                                                                    - label_angular: QLabel
                                                                    - comboBox_linear_data_type: QComboBox
                                                                    - label_linear: QLabel
                                                                    - comboBox_angular_data_type: QComboBox
                                            - tab_list: QWidget
                                                - (Layout): QGridLayout
                                                        - frame_5: QFrame
                                                            - (Layout): QGridLayout
                                                                    - treeWidget_prescribed_dofs: QTreeWidget
                                                        - frame_3: QFrame
                                                            - (Layout): QGridLayout
                                                                    - pushButton_reset: QPushButton
                                                                    - pushButton_remove: QPushButton
                - frame_7: QFrame
                    - (Layout): QGridLayout
                            - pushButton_exit: QPushButton
                            - pushButton_attribute: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
