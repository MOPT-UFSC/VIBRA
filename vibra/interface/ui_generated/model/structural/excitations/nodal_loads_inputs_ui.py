# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'nodal_loads_inputs.ui'
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

from vibra.interface.formatters.icons import Icon

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setWindowModality(Qt.WindowModality.WindowModal)
        Dialog.resize(460, 541)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(460, 540))
        Dialog.setMaximumSize(QSize(460, 580))
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
        self.frame_4.setMinimumSize(QSize(360, 140))
        self.frame_4.setMaximumSize(QSize(16777215, 140))
        self.frame_4.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_4)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setHorizontalSpacing(6)
        self.gridLayout_5.setVerticalSpacing(2)
        self.gridLayout_5.setContentsMargins(2, 2, 2, 2)
        self.comboBox_assignment_type = QComboBox(self.frame_4)
        self.comboBox_assignment_type.addItem("")
        self.comboBox_assignment_type.addItem("")
        self.comboBox_assignment_type.addItem("")
        self.comboBox_assignment_type.addItem("")
        self.comboBox_assignment_type.setObjectName(u"comboBox_assignment_type")
        self.comboBox_assignment_type.setMinimumSize(QSize(0, 28))
        self.comboBox_assignment_type.setMaximumSize(QSize(16777215, 28))
        font2 = QFont()
        font2.setPointSize(10)
        font2.setBold(False)
        self.comboBox_assignment_type.setFont(font2)

        self.gridLayout_5.addWidget(self.comboBox_assignment_type, 0, 3, 1, 1)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_9, 0, 4, 1, 1)

        self.comboBox_element_type = QComboBox(self.frame_4)
        self.comboBox_element_type.addItem("")
        self.comboBox_element_type.addItem("")
        self.comboBox_element_type.setObjectName(u"comboBox_element_type")
        self.comboBox_element_type.setMinimumSize(QSize(150, 28))
        self.comboBox_element_type.setMaximumSize(QSize(150, 28))
        self.comboBox_element_type.setFont(font2)

        self.gridLayout_5.addWidget(self.comboBox_element_type, 1, 2, 1, 1)

        self.lineEdit_selection_id = QLineEdit(self.frame_4)
        self.lineEdit_selection_id.setObjectName(u"lineEdit_selection_id")
        self.lineEdit_selection_id.setMinimumSize(QSize(150, 28))
        self.lineEdit_selection_id.setMaximumSize(QSize(150, 28))
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

        self.comboBox_distribution_type = QComboBox(self.frame_4)
        self.comboBox_distribution_type.addItem("")
        self.comboBox_distribution_type.addItem("")
        self.comboBox_distribution_type.setObjectName(u"comboBox_distribution_type")
        self.comboBox_distribution_type.setMinimumSize(QSize(150, 28))
        self.comboBox_distribution_type.setMaximumSize(QSize(150, 28))
        self.comboBox_distribution_type.setFont(font2)

        self.gridLayout_5.addWidget(self.comboBox_distribution_type, 2, 2, 1, 1)

        self.label_2 = QLabel(self.frame_4)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(120, 28))
        self.label_2.setMaximumSize(QSize(120, 28))
        self.label_2.setFont(font3)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_2, 0, 1, 1, 1)

        self.label_5 = QLabel(self.frame_4)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(120, 28))
        self.label_5.setMaximumSize(QSize(120, 28))
        self.label_5.setFont(font3)
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_5, 2, 1, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_6, 0, 0, 1, 1)

        self.label_3 = QLabel(self.frame_4)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(120, 28))
        self.label_3.setMaximumSize(QSize(120, 28))
        self.label_3.setFont(font3)
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_3, 1, 1, 1, 1)

        self.label_6 = QLabel(self.frame_4)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(120, 28))
        self.label_6.setMaximumSize(QSize(120, 28))
        self.label_6.setFont(font3)
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_6, 3, 1, 1, 1)

        self.comboBox_average_values = QComboBox(self.frame_4)
        self.comboBox_average_values.addItem("")
        self.comboBox_average_values.addItem("")
        self.comboBox_average_values.setObjectName(u"comboBox_average_values")
        self.comboBox_average_values.setMinimumSize(QSize(150, 28))
        self.comboBox_average_values.setMaximumSize(QSize(150, 28))
        self.comboBox_average_values.setFont(font2)
        self.comboBox_average_values.setMaxVisibleItems(2)

        self.gridLayout_5.addWidget(self.comboBox_average_values, 3, 2, 1, 1)


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
        self.tabWidget_main.setMaximumSize(QSize(420, 16777215))
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
        self.frame_8.setMaximumSize(QSize(16777215, 16777215))
        self.frame_8.setFont(font)
        self.frame_8.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_8.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.frame_8)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(8)
        self.gridLayout.setVerticalSpacing(6)
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.lineEdit_imag_Mx = QLineEdit(self.frame_8)
        self.lineEdit_imag_Mx.setObjectName(u"lineEdit_imag_Mx")
        self.lineEdit_imag_Mx.setMinimumSize(QSize(80, 26))
        self.lineEdit_imag_Mx.setMaximumSize(QSize(80, 26))
        self.lineEdit_imag_Mx.setFont(font2)
        self.lineEdit_imag_Mx.setStyleSheet(u"")
        self.lineEdit_imag_Mx.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_imag_Mx, 6, 3, 1, 1)

        self.lineEdit_real_My = QLineEdit(self.frame_8)
        self.lineEdit_real_My.setObjectName(u"lineEdit_real_My")
        self.lineEdit_real_My.setMinimumSize(QSize(80, 26))
        self.lineEdit_real_My.setMaximumSize(QSize(80, 26))
        self.lineEdit_real_My.setFont(font2)
        self.lineEdit_real_My.setStyleSheet(u"")
        self.lineEdit_real_My.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_real_My, 7, 2, 1, 1)

        self.label_Mz_unit = QLabel(self.frame_8)
        self.label_Mz_unit.setObjectName(u"label_Mz_unit")
        self.label_Mz_unit.setMinimumSize(QSize(50, 26))
        self.label_Mz_unit.setMaximumSize(QSize(50, 26))
        font4 = QFont()
        font4.setPointSize(10)
        font4.setBold(False)
        font4.setItalic(False)
        self.label_Mz_unit.setFont(font4)
        self.label_Mz_unit.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_Mz_unit, 8, 4, 1, 1)

        self.lineEdit_imag_Mz = QLineEdit(self.frame_8)
        self.lineEdit_imag_Mz.setObjectName(u"lineEdit_imag_Mz")
        self.lineEdit_imag_Mz.setMinimumSize(QSize(80, 26))
        self.lineEdit_imag_Mz.setMaximumSize(QSize(80, 26))
        self.lineEdit_imag_Mz.setFont(font2)
        self.lineEdit_imag_Mz.setStyleSheet(u"")
        self.lineEdit_imag_Mz.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_imag_Mz, 8, 3, 1, 1)

        self.label_My_unit = QLabel(self.frame_8)
        self.label_My_unit.setObjectName(u"label_My_unit")
        self.label_My_unit.setMinimumSize(QSize(50, 26))
        self.label_My_unit.setMaximumSize(QSize(50, 26))
        self.label_My_unit.setFont(font4)
        self.label_My_unit.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_My_unit, 7, 4, 1, 1)

        self.label_Fy_constant = QLabel(self.frame_8)
        self.label_Fy_constant.setObjectName(u"label_Fy_constant")
        self.label_Fy_constant.setMinimumSize(QSize(70, 26))
        self.label_Fy_constant.setMaximumSize(QSize(70, 26))
        self.label_Fy_constant.setFont(font3)
        self.label_Fy_constant.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_Fy_constant, 4, 1, 1, 1)

        self.label_Mx_constant = QLabel(self.frame_8)
        self.label_Mx_constant.setObjectName(u"label_Mx_constant")
        self.label_Mx_constant.setMinimumSize(QSize(70, 26))
        self.label_Mx_constant.setMaximumSize(QSize(70, 26))
        self.label_Mx_constant.setFont(font2)
        self.label_Mx_constant.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_Mx_constant, 6, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 3, 5, 1, 1)

        self.label_Fz_constant = QLabel(self.frame_8)
        self.label_Fz_constant.setObjectName(u"label_Fz_constant")
        self.label_Fz_constant.setMinimumSize(QSize(70, 26))
        self.label_Fz_constant.setMaximumSize(QSize(70, 26))
        self.label_Fz_constant.setFont(font3)
        self.label_Fz_constant.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_Fz_constant, 5, 1, 1, 1)

        self.label_Fz_unit = QLabel(self.frame_8)
        self.label_Fz_unit.setObjectName(u"label_Fz_unit")
        self.label_Fz_unit.setMinimumSize(QSize(50, 26))
        self.label_Fz_unit.setMaximumSize(QSize(50, 26))
        self.label_Fz_unit.setFont(font3)
        self.label_Fz_unit.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_Fz_unit, 5, 4, 1, 1)

        self.label_Mz_constant = QLabel(self.frame_8)
        self.label_Mz_constant.setObjectName(u"label_Mz_constant")
        self.label_Mz_constant.setMinimumSize(QSize(70, 26))
        self.label_Mz_constant.setMaximumSize(QSize(70, 26))
        self.label_Mz_constant.setFont(font2)
        self.label_Mz_constant.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_Mz_constant, 8, 1, 1, 1)

        self.label_4 = QLabel(self.frame_8)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(80, 26))
        self.label_4.setMaximumSize(QSize(80, 26))
        self.label_4.setFont(font3)
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_4, 2, 2, 1, 1)

        self.lineEdit_imag_Fy = QLineEdit(self.frame_8)
        self.lineEdit_imag_Fy.setObjectName(u"lineEdit_imag_Fy")
        self.lineEdit_imag_Fy.setMinimumSize(QSize(80, 26))
        self.lineEdit_imag_Fy.setMaximumSize(QSize(80, 26))
        self.lineEdit_imag_Fy.setFont(font3)
        self.lineEdit_imag_Fy.setStyleSheet(u"")
        self.lineEdit_imag_Fy.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_imag_Fy, 4, 3, 1, 1)

        self.lineEdit_imag_Fz = QLineEdit(self.frame_8)
        self.lineEdit_imag_Fz.setObjectName(u"lineEdit_imag_Fz")
        self.lineEdit_imag_Fz.setMinimumSize(QSize(80, 26))
        self.lineEdit_imag_Fz.setMaximumSize(QSize(80, 26))
        self.lineEdit_imag_Fz.setFont(font3)
        self.lineEdit_imag_Fz.setStyleSheet(u"")
        self.lineEdit_imag_Fz.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_imag_Fz, 5, 3, 1, 1)

        self.lineEdit_real_Mz = QLineEdit(self.frame_8)
        self.lineEdit_real_Mz.setObjectName(u"lineEdit_real_Mz")
        self.lineEdit_real_Mz.setMinimumSize(QSize(80, 26))
        self.lineEdit_real_Mz.setMaximumSize(QSize(80, 26))
        self.lineEdit_real_Mz.setFont(font2)
        self.lineEdit_real_Mz.setStyleSheet(u"")
        self.lineEdit_real_Mz.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_real_Mz, 8, 2, 1, 1)

        self.lineEdit_imag_My = QLineEdit(self.frame_8)
        self.lineEdit_imag_My.setObjectName(u"lineEdit_imag_My")
        self.lineEdit_imag_My.setMinimumSize(QSize(80, 26))
        self.lineEdit_imag_My.setMaximumSize(QSize(80, 26))
        self.lineEdit_imag_My.setFont(font2)
        self.lineEdit_imag_My.setStyleSheet(u"")
        self.lineEdit_imag_My.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_imag_My, 7, 3, 1, 1)

        self.lineEdit_real_Fx = QLineEdit(self.frame_8)
        self.lineEdit_real_Fx.setObjectName(u"lineEdit_real_Fx")
        self.lineEdit_real_Fx.setMinimumSize(QSize(80, 26))
        self.lineEdit_real_Fx.setMaximumSize(QSize(80, 26))
        self.lineEdit_real_Fx.setFont(font3)
        self.lineEdit_real_Fx.setStyleSheet(u"")
        self.lineEdit_real_Fx.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_real_Fx, 3, 2, 1, 1)

        self.lineEdit_imag_Fx = QLineEdit(self.frame_8)
        self.lineEdit_imag_Fx.setObjectName(u"lineEdit_imag_Fx")
        self.lineEdit_imag_Fx.setMinimumSize(QSize(80, 26))
        self.lineEdit_imag_Fx.setMaximumSize(QSize(80, 26))
        self.lineEdit_imag_Fx.setFont(font3)
        self.lineEdit_imag_Fx.setStyleSheet(u"")
        self.lineEdit_imag_Fx.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_imag_Fx, 3, 3, 1, 1)

        self.lineEdit_real_Fy = QLineEdit(self.frame_8)
        self.lineEdit_real_Fy.setObjectName(u"lineEdit_real_Fy")
        self.lineEdit_real_Fy.setMinimumSize(QSize(80, 26))
        self.lineEdit_real_Fy.setMaximumSize(QSize(80, 26))
        self.lineEdit_real_Fy.setFont(font3)
        self.lineEdit_real_Fy.setStyleSheet(u"")
        self.lineEdit_real_Fy.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_real_Fy, 4, 2, 1, 1)

        self.label_Fx_constant = QLabel(self.frame_8)
        self.label_Fx_constant.setObjectName(u"label_Fx_constant")
        self.label_Fx_constant.setMinimumSize(QSize(70, 26))
        self.label_Fx_constant.setMaximumSize(QSize(70, 26))
        self.label_Fx_constant.setFont(font3)
        self.label_Fx_constant.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_Fx_constant, 3, 1, 1, 1)

        self.label_Fy_unit = QLabel(self.frame_8)
        self.label_Fy_unit.setObjectName(u"label_Fy_unit")
        self.label_Fy_unit.setMinimumSize(QSize(50, 26))
        self.label_Fy_unit.setMaximumSize(QSize(50, 26))
        self.label_Fy_unit.setFont(font3)
        self.label_Fy_unit.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_Fy_unit, 4, 4, 1, 1)

        self.label_Mx_unit = QLabel(self.frame_8)
        self.label_Mx_unit.setObjectName(u"label_Mx_unit")
        self.label_Mx_unit.setMinimumSize(QSize(50, 26))
        self.label_Mx_unit.setMaximumSize(QSize(50, 26))
        self.label_Mx_unit.setFont(font4)
        self.label_Mx_unit.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_Mx_unit, 6, 4, 1, 1)

        self.lineEdit_real_Mx = QLineEdit(self.frame_8)
        self.lineEdit_real_Mx.setObjectName(u"lineEdit_real_Mx")
        self.lineEdit_real_Mx.setMinimumSize(QSize(80, 26))
        self.lineEdit_real_Mx.setMaximumSize(QSize(80, 26))
        self.lineEdit_real_Mx.setFont(font2)
        self.lineEdit_real_Mx.setStyleSheet(u"")
        self.lineEdit_real_Mx.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_real_Mx, 6, 2, 1, 1)

        self.lineEdit_real_Fz = QLineEdit(self.frame_8)
        self.lineEdit_real_Fz.setObjectName(u"lineEdit_real_Fz")
        self.lineEdit_real_Fz.setMinimumSize(QSize(80, 26))
        self.lineEdit_real_Fz.setMaximumSize(QSize(80, 26))
        self.lineEdit_real_Fz.setFont(font3)
        self.lineEdit_real_Fz.setStyleSheet(u"")
        self.lineEdit_real_Fz.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_real_Fz, 5, 2, 1, 1)

        self.label_Fx_unit = QLabel(self.frame_8)
        self.label_Fx_unit.setObjectName(u"label_Fx_unit")
        self.label_Fx_unit.setMinimumSize(QSize(50, 26))
        self.label_Fx_unit.setMaximumSize(QSize(50, 26))
        self.label_Fx_unit.setFont(font3)
        self.label_Fx_unit.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_Fx_unit, 3, 4, 1, 1)

        self.label_My_constant = QLabel(self.frame_8)
        self.label_My_constant.setObjectName(u"label_My_constant")
        self.label_My_constant.setMinimumSize(QSize(70, 26))
        self.label_My_constant.setMaximumSize(QSize(70, 26))
        self.label_My_constant.setFont(font2)
        self.label_My_constant.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_My_constant, 7, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 3, 0, 1, 1)

        self.label_20 = QLabel(self.frame_8)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setMinimumSize(QSize(80, 26))
        self.label_20.setMaximumSize(QSize(80, 26))
        self.label_20.setFont(font3)
        self.label_20.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_20, 2, 3, 1, 1)


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
        self.gridLayout_3.setContentsMargins(4, 4, 4, 2)
        self.label_Fy_table = QLabel(self.frame_9)
        self.label_Fy_table.setObjectName(u"label_Fy_table")
        self.label_Fy_table.setEnabled(True)
        self.label_Fy_table.setMinimumSize(QSize(0, 26))
        self.label_Fy_table.setMaximumSize(QSize(38, 26))
        self.label_Fy_table.setFont(font2)
        self.label_Fy_table.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_Fy_table, 1, 1, 1, 1)

        self.label_Mx_table = QLabel(self.frame_9)
        self.label_Mx_table.setObjectName(u"label_Mx_table")
        self.label_Mx_table.setEnabled(True)
        self.label_Mx_table.setMinimumSize(QSize(0, 26))
        self.label_Mx_table.setMaximumSize(QSize(38, 26))
        self.label_Mx_table.setFont(font2)
        self.label_Mx_table.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_Mx_table, 3, 1, 1, 1)

        self.pushButton_load_Fz_table = QPushButton(self.frame_9)
        self.pushButton_load_Fz_table.setObjectName(u"pushButton_load_Fz_table")
        self.pushButton_load_Fz_table.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton_load_Fz_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_Fz_table.setSizePolicy(sizePolicy1)
        self.pushButton_load_Fz_table.setMinimumSize(QSize(40, 26))
        self.pushButton_load_Fz_table.setMaximumSize(QSize(40, 26))
        self.pushButton_load_Fz_table.setFont(font2)
        self.pushButton_load_Fz_table.setStyleSheet(u"")
        icon = Icon(u":/icons/document_search_blue.png")
        self.pushButton_load_Fz_table.setIcon(icon)
        self.pushButton_load_Fz_table.setIconSize(QSize(20, 20))
        self.pushButton_load_Fz_table.setAutoDefault(False)

        self.gridLayout_3.addWidget(self.pushButton_load_Fz_table, 2, 3, 1, 1)

        self.label_Mz_table = QLabel(self.frame_9)
        self.label_Mz_table.setObjectName(u"label_Mz_table")
        self.label_Mz_table.setEnabled(True)
        self.label_Mz_table.setMinimumSize(QSize(0, 26))
        self.label_Mz_table.setMaximumSize(QSize(38, 26))
        self.label_Mz_table.setFont(font2)
        self.label_Mz_table.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_Mz_table, 5, 1, 1, 1)

        self.lineEdit_path_table_Fy = QLineEdit(self.frame_9)
        self.lineEdit_path_table_Fy.setObjectName(u"lineEdit_path_table_Fy")
        self.lineEdit_path_table_Fy.setEnabled(True)
        self.lineEdit_path_table_Fy.setMinimumSize(QSize(300, 26))
        self.lineEdit_path_table_Fy.setMaximumSize(QSize(300, 26))
        self.lineEdit_path_table_Fy.setStyleSheet(u"")
        self.lineEdit_path_table_Fy.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_path_table_Fy.setClearButtonEnabled(True)

        self.gridLayout_3.addWidget(self.lineEdit_path_table_Fy, 1, 2, 1, 1)

        self.lineEdit_path_table_My = QLineEdit(self.frame_9)
        self.lineEdit_path_table_My.setObjectName(u"lineEdit_path_table_My")
        self.lineEdit_path_table_My.setEnabled(True)
        self.lineEdit_path_table_My.setMinimumSize(QSize(300, 26))
        self.lineEdit_path_table_My.setMaximumSize(QSize(300, 26))
        self.lineEdit_path_table_My.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_path_table_My.setClearButtonEnabled(True)

        self.gridLayout_3.addWidget(self.lineEdit_path_table_My, 4, 2, 1, 1)

        self.pushButton_load_Fy_table = QPushButton(self.frame_9)
        self.pushButton_load_Fy_table.setObjectName(u"pushButton_load_Fy_table")
        self.pushButton_load_Fy_table.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.pushButton_load_Fy_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_Fy_table.setSizePolicy(sizePolicy1)
        self.pushButton_load_Fy_table.setMinimumSize(QSize(40, 26))
        self.pushButton_load_Fy_table.setMaximumSize(QSize(40, 26))
        self.pushButton_load_Fy_table.setFont(font2)
        self.pushButton_load_Fy_table.setStyleSheet(u"")
        self.pushButton_load_Fy_table.setIcon(icon)
        self.pushButton_load_Fy_table.setIconSize(QSize(20, 20))
        self.pushButton_load_Fy_table.setAutoDefault(False)

        self.gridLayout_3.addWidget(self.pushButton_load_Fy_table, 1, 3, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_3, 0, 0, 1, 1)

        self.lineEdit_path_table_Fx = QLineEdit(self.frame_9)
        self.lineEdit_path_table_Fx.setObjectName(u"lineEdit_path_table_Fx")
        self.lineEdit_path_table_Fx.setEnabled(True)
        self.lineEdit_path_table_Fx.setMinimumSize(QSize(300, 26))
        self.lineEdit_path_table_Fx.setMaximumSize(QSize(300, 26))
        self.lineEdit_path_table_Fx.setStyleSheet(u"")
        self.lineEdit_path_table_Fx.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_path_table_Fx.setClearButtonEnabled(True)

        self.gridLayout_3.addWidget(self.lineEdit_path_table_Fx, 0, 2, 1, 1)

        self.pushButton_load_Mz_table = QPushButton(self.frame_9)
        self.pushButton_load_Mz_table.setObjectName(u"pushButton_load_Mz_table")
        self.pushButton_load_Mz_table.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.pushButton_load_Mz_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_Mz_table.setSizePolicy(sizePolicy1)
        self.pushButton_load_Mz_table.setMinimumSize(QSize(40, 26))
        self.pushButton_load_Mz_table.setMaximumSize(QSize(40, 26))
        self.pushButton_load_Mz_table.setFont(font2)
        self.pushButton_load_Mz_table.setStyleSheet(u"")
        self.pushButton_load_Mz_table.setIcon(icon)
        self.pushButton_load_Mz_table.setIconSize(QSize(20, 20))
        self.pushButton_load_Mz_table.setAutoDefault(False)

        self.gridLayout_3.addWidget(self.pushButton_load_Mz_table, 5, 3, 1, 1)

        self.pushButton_load_My_table = QPushButton(self.frame_9)
        self.pushButton_load_My_table.setObjectName(u"pushButton_load_My_table")
        self.pushButton_load_My_table.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.pushButton_load_My_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_My_table.setSizePolicy(sizePolicy1)
        self.pushButton_load_My_table.setMinimumSize(QSize(40, 26))
        self.pushButton_load_My_table.setMaximumSize(QSize(40, 26))
        self.pushButton_load_My_table.setFont(font2)
        self.pushButton_load_My_table.setStyleSheet(u"")
        self.pushButton_load_My_table.setIcon(icon)
        self.pushButton_load_My_table.setIconSize(QSize(20, 20))
        self.pushButton_load_My_table.setAutoDefault(False)

        self.gridLayout_3.addWidget(self.pushButton_load_My_table, 4, 3, 1, 1)

        self.lineEdit_path_table_Fz = QLineEdit(self.frame_9)
        self.lineEdit_path_table_Fz.setObjectName(u"lineEdit_path_table_Fz")
        self.lineEdit_path_table_Fz.setEnabled(True)
        self.lineEdit_path_table_Fz.setMinimumSize(QSize(300, 26))
        self.lineEdit_path_table_Fz.setMaximumSize(QSize(300, 26))
        self.lineEdit_path_table_Fz.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_path_table_Fz.setClearButtonEnabled(True)

        self.gridLayout_3.addWidget(self.lineEdit_path_table_Fz, 2, 2, 1, 1)

        self.pushButton_load_Fx_table = QPushButton(self.frame_9)
        self.pushButton_load_Fx_table.setObjectName(u"pushButton_load_Fx_table")
        self.pushButton_load_Fx_table.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.pushButton_load_Fx_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_Fx_table.setSizePolicy(sizePolicy1)
        self.pushButton_load_Fx_table.setMinimumSize(QSize(40, 26))
        self.pushButton_load_Fx_table.setMaximumSize(QSize(40, 26))
        self.pushButton_load_Fx_table.setFont(font2)
        self.pushButton_load_Fx_table.setStyleSheet(u"")
        self.pushButton_load_Fx_table.setIcon(icon)
        self.pushButton_load_Fx_table.setIconSize(QSize(20, 20))
        self.pushButton_load_Fx_table.setAutoDefault(False)

        self.gridLayout_3.addWidget(self.pushButton_load_Fx_table, 0, 3, 1, 1)

        self.lineEdit_path_table_Mz = QLineEdit(self.frame_9)
        self.lineEdit_path_table_Mz.setObjectName(u"lineEdit_path_table_Mz")
        self.lineEdit_path_table_Mz.setEnabled(True)
        self.lineEdit_path_table_Mz.setMinimumSize(QSize(300, 26))
        self.lineEdit_path_table_Mz.setMaximumSize(QSize(300, 26))
        self.lineEdit_path_table_Mz.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_path_table_Mz.setClearButtonEnabled(True)

        self.gridLayout_3.addWidget(self.lineEdit_path_table_Mz, 5, 2, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_4, 0, 4, 1, 1)

        self.lineEdit_path_table_Mx = QLineEdit(self.frame_9)
        self.lineEdit_path_table_Mx.setObjectName(u"lineEdit_path_table_Mx")
        self.lineEdit_path_table_Mx.setEnabled(True)
        self.lineEdit_path_table_Mx.setMinimumSize(QSize(300, 26))
        self.lineEdit_path_table_Mx.setMaximumSize(QSize(300, 26))
        self.lineEdit_path_table_Mx.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_path_table_Mx.setClearButtonEnabled(True)

        self.gridLayout_3.addWidget(self.lineEdit_path_table_Mx, 3, 2, 1, 1)

        self.label_Fz_table = QLabel(self.frame_9)
        self.label_Fz_table.setObjectName(u"label_Fz_table")
        self.label_Fz_table.setEnabled(True)
        self.label_Fz_table.setMinimumSize(QSize(0, 26))
        self.label_Fz_table.setMaximumSize(QSize(38, 26))
        self.label_Fz_table.setFont(font2)
        self.label_Fz_table.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_Fz_table, 2, 1, 1, 1)

        self.label_My_table = QLabel(self.frame_9)
        self.label_My_table.setObjectName(u"label_My_table")
        self.label_My_table.setEnabled(True)
        self.label_My_table.setMinimumSize(QSize(0, 26))
        self.label_My_table.setMaximumSize(QSize(38, 26))
        self.label_My_table.setFont(font2)
        self.label_My_table.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_My_table, 4, 1, 1, 1)

        self.pushButton_load_Mx_table = QPushButton(self.frame_9)
        self.pushButton_load_Mx_table.setObjectName(u"pushButton_load_Mx_table")
        self.pushButton_load_Mx_table.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.pushButton_load_Mx_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_Mx_table.setSizePolicy(sizePolicy1)
        self.pushButton_load_Mx_table.setMinimumSize(QSize(40, 26))
        self.pushButton_load_Mx_table.setMaximumSize(QSize(40, 26))
        self.pushButton_load_Mx_table.setFont(font2)
        self.pushButton_load_Mx_table.setStyleSheet(u"")
        self.pushButton_load_Mx_table.setIcon(icon)
        self.pushButton_load_Mx_table.setIconSize(QSize(20, 20))
        self.pushButton_load_Mx_table.setAutoDefault(False)

        self.gridLayout_3.addWidget(self.pushButton_load_Mx_table, 3, 3, 1, 1)

        self.label_Fx_table = QLabel(self.frame_9)
        self.label_Fx_table.setObjectName(u"label_Fx_table")
        self.label_Fx_table.setEnabled(True)
        self.label_Fx_table.setMinimumSize(QSize(0, 26))
        self.label_Fx_table.setMaximumSize(QSize(38, 26))
        self.label_Fx_table.setFont(font2)
        self.label_Fx_table.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_Fx_table, 0, 1, 1, 1)


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
        self.treeWidget_nodal_loads = QTreeWidget(self.frame_5)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(2, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter);
        self.treeWidget_nodal_loads.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_nodal_loads.setObjectName(u"treeWidget_nodal_loads")
        self.treeWidget_nodal_loads.setMinimumSize(QSize(320, 170))
        self.treeWidget_nodal_loads.setMaximumSize(QSize(380, 200))
        self.treeWidget_nodal_loads.setFont(font3)
        self.treeWidget_nodal_loads.setIndentation(1)
        self.treeWidget_nodal_loads.setHeaderHidden(False)
        self.treeWidget_nodal_loads.header().setHighlightSections(False)
        self.treeWidget_nodal_loads.header().setProperty(u"showSortIndicator", False)
        self.treeWidget_nodal_loads.header().setStretchLastSection(True)

        self.gridLayout_2.addWidget(self.treeWidget_nodal_loads, 0, 0, 1, 1)


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


        self.gridLayout_4.addWidget(self.frame_6, 2, 0, 1, 1)


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

        self.comboBox_average_values.setCurrentIndex(1)
        self.tabWidget_main.setCurrentIndex(0)
        self.pushButton_apply_and_close.setDefault(False)
        self.pushButton_apply.setDefault(False)
        self.pushButton_cancel.setDefault(False)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Set structural nodal loads", None))
#if QT_CONFIG(whatsthis)
        Dialog.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.label.setText(QCoreApplication.translate("Dialog", u"Set structural nodal loads", None))
        self.comboBox_assignment_type.setItemText(0, QCoreApplication.translate("Dialog", u"Selected faces", None))
        self.comboBox_assignment_type.setItemText(1, QCoreApplication.translate("Dialog", u"Selected lines", None))
        self.comboBox_assignment_type.setItemText(2, QCoreApplication.translate("Dialog", u"Selected points", None))
        self.comboBox_assignment_type.setItemText(3, QCoreApplication.translate("Dialog", u"Selected nodes", None))

        self.comboBox_element_type.setItemText(0, QCoreApplication.translate("Dialog", u"Face element", None))
        self.comboBox_element_type.setItemText(1, QCoreApplication.translate("Dialog", u"Solid element", None))

        self.comboBox_distribution_type.setItemText(0, QCoreApplication.translate("Dialog", u"Element integration", None))
        self.comboBox_distribution_type.setItemText(1, QCoreApplication.translate("Dialog", u"Nodal distribution", None))

        self.label_2.setText(QCoreApplication.translate("Dialog", u"Selection ID:", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"Distribution type:", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Element type:", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"Average values:", None))
        self.comboBox_average_values.setItemText(0, QCoreApplication.translate("Dialog", u"Disabled", None))
        self.comboBox_average_values.setItemText(1, QCoreApplication.translate("Dialog", u"Enabled", None))

        self.label_Mz_unit.setText(QCoreApplication.translate("Dialog", u"[N.m]", None))
        self.label_My_unit.setText(QCoreApplication.translate("Dialog", u"[N.m]", None))
        self.label_Fy_constant.setText(QCoreApplication.translate("Dialog", u"Fy:", None))
        self.label_Mx_constant.setText(QCoreApplication.translate("Dialog", u"Mx:", None))
        self.label_Fz_constant.setText(QCoreApplication.translate("Dialog", u"Fz:", None))
        self.label_Fz_unit.setText(QCoreApplication.translate("Dialog", u"[N]", None))
        self.label_Mz_constant.setText(QCoreApplication.translate("Dialog", u"Mz:", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Real", None))
        self.lineEdit_real_Fx.setText("")
        self.label_Fx_constant.setText(QCoreApplication.translate("Dialog", u"Fx:", None))
        self.label_Fy_unit.setText(QCoreApplication.translate("Dialog", u"[N]", None))
        self.label_Mx_unit.setText(QCoreApplication.translate("Dialog", u"[N.m]", None))
        self.label_Fx_unit.setText(QCoreApplication.translate("Dialog", u"[N]", None))
        self.label_My_constant.setText(QCoreApplication.translate("Dialog", u"My:", None))
        self.label_20.setText(QCoreApplication.translate("Dialog", u"Imaginary", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_constant_data), QCoreApplication.translate("Dialog", u"Constant data", None))
        self.label_Fy_table.setText(QCoreApplication.translate("Dialog", u"Fy:", None))
        self.label_Mx_table.setText(QCoreApplication.translate("Dialog", u"Mx:", None))
        self.pushButton_load_Fz_table.setText("")
        self.label_Mz_table.setText(QCoreApplication.translate("Dialog", u"Mz:", None))
        self.pushButton_load_Fy_table.setText("")
        self.pushButton_load_Mz_table.setText("")
        self.pushButton_load_My_table.setText("")
        self.pushButton_load_Fx_table.setText("")
        self.label_Fz_table.setText(QCoreApplication.translate("Dialog", u"Fz:", None))
        self.label_My_table.setText(QCoreApplication.translate("Dialog", u"My:", None))
        self.pushButton_load_Mx_table.setText("")
        self.label_Fx_table.setText(QCoreApplication.translate("Dialog", u"Fx:", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_tabular_data), QCoreApplication.translate("Dialog", u"Tabular data", None))
        ___qtreewidgetitem = self.treeWidget_nodal_loads.headerItem()
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("Dialog", u"Element type", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"Nodal loads", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Selection-ID", None));
#if QT_CONFIG(tooltip)
        self.treeWidget_nodal_loads.setToolTip(QCoreApplication.translate("Dialog", u"Select a node to remove the attributed boundary condition.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_reset.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.pushButton_remove.setText(QCoreApplication.translate("Dialog", u"Remove", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_list), QCoreApplication.translate("Dialog", u"List", None))
        self.pushButton_apply_and_close.setText(QCoreApplication.translate("Dialog", u"Ok", None))
        self.pushButton_apply.setText(QCoreApplication.translate("Dialog", u"Apply", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
    # retranslateUi



class NodalLoadsInputs_UI(QDialog, Ui_Dialog):
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
                                        - comboBox_assignment_type: QComboBox
                                        - comboBox_element_type: QComboBox
                                        - lineEdit_selection_id: QLineEdit
                                        - comboBox_distribution_type: QComboBox
                                        - label_2: QLabel
                                        - label_5: QLabel
                                        - label_3: QLabel
                                        - label_6: QLabel
                                        - comboBox_average_values: QComboBox
                            - frame_6: QFrame
                                - (Layout): QGridLayout
                                        - tabWidget_main: QTabWidget
                                            - tab_constant_data: QWidget
                                                - (Layout): QGridLayout
                                                        - frame_8: QFrame
                                                            - (Layout): QGridLayout
                                                                    - lineEdit_imag_Mx: QLineEdit
                                                                    - lineEdit_real_My: QLineEdit
                                                                    - label_Mz_unit: QLabel
                                                                    - lineEdit_imag_Mz: QLineEdit
                                                                    - label_My_unit: QLabel
                                                                    - label_Fy_constant: QLabel
                                                                    - label_Mx_constant: QLabel
                                                                    - label_Fz_constant: QLabel
                                                                    - label_Fz_unit: QLabel
                                                                    - label_Mz_constant: QLabel
                                                                    - label_4: QLabel
                                                                    - lineEdit_imag_Fy: QLineEdit
                                                                    - lineEdit_imag_Fz: QLineEdit
                                                                    - lineEdit_real_Mz: QLineEdit
                                                                    - lineEdit_imag_My: QLineEdit
                                                                    - lineEdit_real_Fx: QLineEdit
                                                                    - lineEdit_imag_Fx: QLineEdit
                                                                    - lineEdit_real_Fy: QLineEdit
                                                                    - label_Fx_constant: QLabel
                                                                    - label_Fy_unit: QLabel
                                                                    - label_Mx_unit: QLabel
                                                                    - lineEdit_real_Mx: QLineEdit
                                                                    - lineEdit_real_Fz: QLineEdit
                                                                    - label_Fx_unit: QLabel
                                                                    - label_My_constant: QLabel
                                                                    - label_20: QLabel
                                            - tab_tabular_data: QWidget
                                                - (Layout): QGridLayout
                                                        - frame_9: QFrame
                                                            - (Layout): QGridLayout
                                                                    - label_Fy_table: QLabel
                                                                    - label_Mx_table: QLabel
                                                                    - pushButton_load_Fz_table: QPushButton
                                                                    - label_Mz_table: QLabel
                                                                    - lineEdit_path_table_Fy: QLineEdit
                                                                    - lineEdit_path_table_My: QLineEdit
                                                                    - pushButton_load_Fy_table: QPushButton
                                                                    - lineEdit_path_table_Fx: QLineEdit
                                                                    - pushButton_load_Mz_table: QPushButton
                                                                    - pushButton_load_My_table: QPushButton
                                                                    - lineEdit_path_table_Fz: QLineEdit
                                                                    - pushButton_load_Fx_table: QPushButton
                                                                    - lineEdit_path_table_Mz: QLineEdit
                                                                    - lineEdit_path_table_Mx: QLineEdit
                                                                    - label_Fz_table: QLabel
                                                                    - label_My_table: QLabel
                                                                    - pushButton_load_Mx_table: QPushButton
                                                                    - label_Fx_table: QLabel
                                            - tab_list: QWidget
                                                - (Layout): QGridLayout
                                                        - frame_5: QFrame
                                                            - (Layout): QGridLayout
                                                                    - treeWidget_nodal_loads: QTreeWidget
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
