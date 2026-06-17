# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'porous_material_model_inputs.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
    QDoubleSpinBox, QFrame, QGridLayout, QHeaderView,
    QLabel, QLineEdit, QPushButton, QScrollArea,
    QSizePolicy, QSpacerItem, QTabWidget, QTableWidget,
    QTableWidgetItem, QTreeWidget, QTreeWidgetItem, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(531, 559)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.frame_top = QFrame(Dialog)
        self.frame_top.setObjectName(u"frame_top")
        self.frame_top.setMinimumSize(QSize(0, 48))
        self.frame_top.setMaximumSize(QSize(16777215, 48))
        self.frame_top.setFrameShape(QFrame.Shape.Box)
        self.frame_top.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_top)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label = QLabel(self.frame_top)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_top, 0, 0, 1, 1)

        self.frame_main = QFrame(Dialog)
        self.frame_main.setObjectName(u"frame_main")
        self.frame_main.setFrameShape(QFrame.Shape.Box)
        self.frame_main.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_main)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(4, 6, 4, 4)
        self.scrollArea = QScrollArea(self.frame_main)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 494, 540))
        self.gridLayout_20 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_20.setObjectName(u"gridLayout_20")
        self.frame_plot_setup = QFrame(self.scrollAreaWidgetContents)
        self.frame_plot_setup.setObjectName(u"frame_plot_setup")
        self.frame_plot_setup.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_plot_setup.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_18 = QGridLayout(self.frame_plot_setup)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.label_17 = QLabel(self.frame_plot_setup)
        self.label_17.setObjectName(u"label_17")
        font1 = QFont()
        font1.setPointSize(10)
        self.label_17.setFont(font1)
        self.label_17.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_18.addWidget(self.label_17, 4, 3, 1, 1)

        self.lineEdit_speed_of_sound = QLineEdit(self.frame_plot_setup)
        self.lineEdit_speed_of_sound.setObjectName(u"lineEdit_speed_of_sound")
        self.lineEdit_speed_of_sound.setEnabled(False)
        self.lineEdit_speed_of_sound.setMinimumSize(QSize(100, 28))
        self.lineEdit_speed_of_sound.setMaximumSize(QSize(100, 28))
        self.lineEdit_speed_of_sound.setFont(font1)
        self.lineEdit_speed_of_sound.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.lineEdit_speed_of_sound.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_18.addWidget(self.lineEdit_speed_of_sound, 3, 2, 1, 1)

        self.label_47 = QLabel(self.frame_plot_setup)
        self.label_47.setObjectName(u"label_47")
        self.label_47.setFont(font1)
        self.label_47.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_18.addWidget(self.label_47, 3, 1, 1, 1)

        self.doubleSpinBox_porous_material_depth = QDoubleSpinBox(self.frame_plot_setup)
        self.doubleSpinBox_porous_material_depth.setObjectName(u"doubleSpinBox_porous_material_depth")
        self.doubleSpinBox_porous_material_depth.setMinimumSize(QSize(100, 28))
        self.doubleSpinBox_porous_material_depth.setMaximumSize(QSize(100, 28))
        self.doubleSpinBox_porous_material_depth.setFont(font1)
        self.doubleSpinBox_porous_material_depth.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.doubleSpinBox_porous_material_depth.setDecimals(4)
        self.doubleSpinBox_porous_material_depth.setMinimum(0.001000000000000)
        self.doubleSpinBox_porous_material_depth.setMaximum(100.000000000000000)
        self.doubleSpinBox_porous_material_depth.setSingleStep(0.050000000000000)
        self.doubleSpinBox_porous_material_depth.setValue(0.100000000000000)

        self.gridLayout_18.addWidget(self.doubleSpinBox_porous_material_depth, 4, 2, 1, 1)

        self.label_16 = QLabel(self.frame_plot_setup)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setFont(font1)
        self.label_16.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_18.addWidget(self.label_16, 4, 1, 1, 1)

        self.label_49 = QLabel(self.frame_plot_setup)
        self.label_49.setObjectName(u"label_49")
        self.label_49.setFont(font1)
        self.label_49.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_18.addWidget(self.label_49, 3, 3, 1, 1)

        self.pushButton_get_fluid = QPushButton(self.frame_plot_setup)
        self.pushButton_get_fluid.setObjectName(u"pushButton_get_fluid")
        self.pushButton_get_fluid.setMinimumSize(QSize(72, 0))
        self.pushButton_get_fluid.setMaximumSize(QSize(72, 28))
        self.pushButton_get_fluid.setFont(font1)

        self.gridLayout_18.addWidget(self.pushButton_get_fluid, 1, 3, 1, 1)

        self.lineEdit_fluid_density = QLineEdit(self.frame_plot_setup)
        self.lineEdit_fluid_density.setObjectName(u"lineEdit_fluid_density")
        self.lineEdit_fluid_density.setEnabled(False)
        self.lineEdit_fluid_density.setMinimumSize(QSize(100, 28))
        self.lineEdit_fluid_density.setMaximumSize(QSize(100, 28))
        self.lineEdit_fluid_density.setFont(font1)
        self.lineEdit_fluid_density.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.lineEdit_fluid_density.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_18.addWidget(self.lineEdit_fluid_density, 2, 2, 1, 1)

        self.label_31 = QLabel(self.frame_plot_setup)
        self.label_31.setObjectName(u"label_31")
        self.label_31.setFont(font1)
        self.label_31.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_18.addWidget(self.label_31, 1, 1, 1, 1)

        self.horizontalSpacer_18 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_18.addItem(self.horizontalSpacer_18, 4, 4, 1, 1)

        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_18.addItem(self.horizontalSpacer_14, 4, 0, 1, 1)

        self.label_36 = QLabel(self.frame_plot_setup)
        self.label_36.setObjectName(u"label_36")
        self.label_36.setFont(font1)
        self.label_36.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_18.addWidget(self.label_36, 2, 1, 1, 1)

        self.lineEdit_selected_fluid = QLineEdit(self.frame_plot_setup)
        self.lineEdit_selected_fluid.setObjectName(u"lineEdit_selected_fluid")
        self.lineEdit_selected_fluid.setEnabled(False)
        self.lineEdit_selected_fluid.setMinimumSize(QSize(100, 28))
        self.lineEdit_selected_fluid.setMaximumSize(QSize(100, 28))
        self.lineEdit_selected_fluid.setFont(font1)
        self.lineEdit_selected_fluid.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.lineEdit_selected_fluid.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_18.addWidget(self.lineEdit_selected_fluid, 1, 2, 1, 1)

        self.label_48 = QLabel(self.frame_plot_setup)
        self.label_48.setObjectName(u"label_48")
        self.label_48.setFont(font1)
        self.label_48.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_18.addWidget(self.label_48, 2, 3, 1, 1)

        self.frame_2 = QFrame(self.frame_plot_setup)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_18.addWidget(self.frame_2, 0, 2, 1, 1)


        self.gridLayout_20.addWidget(self.frame_plot_setup, 2, 0, 1, 1)

        self.tabWidget_main = QTabWidget(self.scrollAreaWidgetContents)
        self.tabWidget_main.setObjectName(u"tabWidget_main")
        self.tabWidget_main.setMinimumSize(QSize(0, 300))
        self.tabWidget_main.setMaximumSize(QSize(16777215, 16777215))
        self.tabWidget_main.setSizeIncrement(QSize(0, 0))
        self.tabWidget_main.setFont(font1)
        self.tabWidget_main.setTabBarAutoHide(False)
        self.tab_DBM = QWidget()
        self.tab_DBM.setObjectName(u"tab_DBM")
        self.gridLayout_5 = QGridLayout(self.tab_DBM)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setHorizontalSpacing(4)
        self.gridLayout_5.setVerticalSpacing(2)
        self.gridLayout_5.setContentsMargins(4, 8, 4, 8)
        self.frame_4 = QFrame(self.tab_DBM)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_6 = QGridLayout(self.frame_4)
        self.gridLayout_6.setSpacing(6)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(6, 6, 6, 6)
        self.label_8 = QLabel(self.frame_4)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setFont(font1)
        self.label_8.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_8, 2, 4, 1, 1)

        self.label_7 = QLabel(self.frame_4)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font1)
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_7, 1, 4, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_3, 0, 0, 1, 1)

        self.label_3 = QLabel(self.frame_4)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font1)
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_3, 1, 1, 1, 1)

        self.doubleSpinBox_C4_DBM = QDoubleSpinBox(self.frame_4)
        self.doubleSpinBox_C4_DBM.setObjectName(u"doubleSpinBox_C4_DBM")
        self.doubleSpinBox_C4_DBM.setEnabled(False)
        self.doubleSpinBox_C4_DBM.setMinimumSize(QSize(100, 28))
        self.doubleSpinBox_C4_DBM.setMaximumSize(QSize(100, 28))
        self.doubleSpinBox_C4_DBM.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.doubleSpinBox_C4_DBM.setDecimals(4)
        self.doubleSpinBox_C4_DBM.setMinimum(-100.000000000000000)
        self.doubleSpinBox_C4_DBM.setMaximum(100.000000000000000)
        self.doubleSpinBox_C4_DBM.setValue(0.595000000000000)

        self.gridLayout_6.addWidget(self.doubleSpinBox_C4_DBM, 3, 2, 1, 1)

        self.label_6 = QLabel(self.frame_4)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font1)
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_6, 0, 4, 1, 1)

        self.doubleSpinBox_C5_DBM = QDoubleSpinBox(self.frame_4)
        self.doubleSpinBox_C5_DBM.setObjectName(u"doubleSpinBox_C5_DBM")
        self.doubleSpinBox_C5_DBM.setEnabled(False)
        self.doubleSpinBox_C5_DBM.setMinimumSize(QSize(100, 28))
        self.doubleSpinBox_C5_DBM.setMaximumSize(QSize(100, 28))
        self.doubleSpinBox_C5_DBM.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.doubleSpinBox_C5_DBM.setDecimals(4)
        self.doubleSpinBox_C5_DBM.setMinimum(-100.000000000000000)
        self.doubleSpinBox_C5_DBM.setMaximum(100.000000000000000)
        self.doubleSpinBox_C5_DBM.setValue(0.049700000000000)

        self.gridLayout_6.addWidget(self.doubleSpinBox_C5_DBM, 0, 5, 1, 1)

        self.doubleSpinBox_C6_DBM = QDoubleSpinBox(self.frame_4)
        self.doubleSpinBox_C6_DBM.setObjectName(u"doubleSpinBox_C6_DBM")
        self.doubleSpinBox_C6_DBM.setEnabled(False)
        self.doubleSpinBox_C6_DBM.setMinimumSize(QSize(100, 28))
        self.doubleSpinBox_C6_DBM.setMaximumSize(QSize(100, 28))
        self.doubleSpinBox_C6_DBM.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.doubleSpinBox_C6_DBM.setDecimals(4)
        self.doubleSpinBox_C6_DBM.setMinimum(-100.000000000000000)
        self.doubleSpinBox_C6_DBM.setMaximum(100.000000000000000)
        self.doubleSpinBox_C6_DBM.setValue(0.754000000000000)

        self.gridLayout_6.addWidget(self.doubleSpinBox_C6_DBM, 1, 5, 1, 1)

        self.doubleSpinBox_C7_DBM = QDoubleSpinBox(self.frame_4)
        self.doubleSpinBox_C7_DBM.setObjectName(u"doubleSpinBox_C7_DBM")
        self.doubleSpinBox_C7_DBM.setEnabled(False)
        self.doubleSpinBox_C7_DBM.setMinimumSize(QSize(100, 28))
        self.doubleSpinBox_C7_DBM.setMaximumSize(QSize(100, 28))
        self.doubleSpinBox_C7_DBM.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.doubleSpinBox_C7_DBM.setDecimals(4)
        self.doubleSpinBox_C7_DBM.setMinimum(-100.000000000000000)
        self.doubleSpinBox_C7_DBM.setMaximum(100.000000000000000)
        self.doubleSpinBox_C7_DBM.setValue(0.075800000000000)

        self.gridLayout_6.addWidget(self.doubleSpinBox_C7_DBM, 2, 5, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer, 0, 6, 1, 1)

        self.label_9 = QLabel(self.frame_4)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setFont(font1)
        self.label_9.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_9, 3, 4, 1, 1)

        self.doubleSpinBox_C8_DBM = QDoubleSpinBox(self.frame_4)
        self.doubleSpinBox_C8_DBM.setObjectName(u"doubleSpinBox_C8_DBM")
        self.doubleSpinBox_C8_DBM.setEnabled(False)
        self.doubleSpinBox_C8_DBM.setMinimumSize(QSize(100, 28))
        self.doubleSpinBox_C8_DBM.setMaximumSize(QSize(100, 28))
        self.doubleSpinBox_C8_DBM.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.doubleSpinBox_C8_DBM.setDecimals(4)
        self.doubleSpinBox_C8_DBM.setMinimum(-100.000000000000000)
        self.doubleSpinBox_C8_DBM.setMaximum(100.000000000000000)
        self.doubleSpinBox_C8_DBM.setValue(0.732000000000000)

        self.gridLayout_6.addWidget(self.doubleSpinBox_C8_DBM, 3, 5, 1, 1)

        self.label_5 = QLabel(self.frame_4)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font1)
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_5, 3, 1, 1, 1)

        self.label_4 = QLabel(self.frame_4)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font1)
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_4, 2, 1, 1, 1)

        self.doubleSpinBox_C3_DBM = QDoubleSpinBox(self.frame_4)
        self.doubleSpinBox_C3_DBM.setObjectName(u"doubleSpinBox_C3_DBM")
        self.doubleSpinBox_C3_DBM.setEnabled(False)
        self.doubleSpinBox_C3_DBM.setMinimumSize(QSize(100, 28))
        self.doubleSpinBox_C3_DBM.setMaximumSize(QSize(100, 28))
        self.doubleSpinBox_C3_DBM.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.doubleSpinBox_C3_DBM.setDecimals(4)
        self.doubleSpinBox_C3_DBM.setMinimum(-100.000000000000000)
        self.doubleSpinBox_C3_DBM.setMaximum(100.000000000000000)
        self.doubleSpinBox_C3_DBM.setValue(0.169000000000000)

        self.gridLayout_6.addWidget(self.doubleSpinBox_C3_DBM, 2, 2, 1, 1)

        self.label_2 = QLabel(self.frame_4)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font1)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_2, 0, 1, 1, 1)

        self.doubleSpinBox_C1_DBM = QDoubleSpinBox(self.frame_4)
        self.doubleSpinBox_C1_DBM.setObjectName(u"doubleSpinBox_C1_DBM")
        self.doubleSpinBox_C1_DBM.setEnabled(False)
        self.doubleSpinBox_C1_DBM.setMinimumSize(QSize(100, 28))
        self.doubleSpinBox_C1_DBM.setMaximumSize(QSize(100, 28))
        self.doubleSpinBox_C1_DBM.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.doubleSpinBox_C1_DBM.setDecimals(4)
        self.doubleSpinBox_C1_DBM.setMinimum(-100.000000000000000)
        self.doubleSpinBox_C1_DBM.setMaximum(100.000000000000000)
        self.doubleSpinBox_C1_DBM.setValue(0.085800000000000)

        self.gridLayout_6.addWidget(self.doubleSpinBox_C1_DBM, 0, 2, 1, 1)

        self.doubleSpinBox_C2_DBM = QDoubleSpinBox(self.frame_4)
        self.doubleSpinBox_C2_DBM.setObjectName(u"doubleSpinBox_C2_DBM")
        self.doubleSpinBox_C2_DBM.setEnabled(False)
        self.doubleSpinBox_C2_DBM.setMinimumSize(QSize(100, 28))
        self.doubleSpinBox_C2_DBM.setMaximumSize(QSize(100, 28))
        self.doubleSpinBox_C2_DBM.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.doubleSpinBox_C2_DBM.setDecimals(4)
        self.doubleSpinBox_C2_DBM.setMinimum(-100.000000000000000)
        self.doubleSpinBox_C2_DBM.setMaximum(100.000000000000000)
        self.doubleSpinBox_C2_DBM.setValue(0.700000000000000)

        self.gridLayout_6.addWidget(self.doubleSpinBox_C2_DBM, 1, 2, 1, 1)

        self.pushButton_DB_equations = QPushButton(self.frame_4)
        self.pushButton_DB_equations.setObjectName(u"pushButton_DB_equations")
        self.pushButton_DB_equations.setMinimumSize(QSize(40, 28))
        self.pushButton_DB_equations.setMaximumSize(QSize(100, 28))
        self.pushButton_DB_equations.setFont(font1)
        icon = QIcon()
        icon.addFile(u":/icons/help.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_DB_equations.setIcon(icon)
        self.pushButton_DB_equations.setIconSize(QSize(18, 18))

        self.gridLayout_6.addWidget(self.pushButton_DB_equations, 0, 3, 1, 1)


        self.gridLayout_5.addWidget(self.frame_4, 1, 0, 1, 1)

        self.frame_5 = QFrame(self.tab_DBM)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setMinimumSize(QSize(0, 48))
        self.frame_5.setMaximumSize(QSize(16777215, 48))
        self.frame_5.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_7 = QGridLayout(self.frame_5)
        self.gridLayout_7.setSpacing(6)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(6, 6, 6, 6)
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_5, 0, 4, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_4, 0, 0, 1, 1)

        self.label_10 = QLabel(self.frame_5)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setFont(font1)

        self.gridLayout_7.addWidget(self.label_10, 0, 1, 1, 1)

        self.doubleSpinBox_flow_resistivity_DBM = QDoubleSpinBox(self.frame_5)
        self.doubleSpinBox_flow_resistivity_DBM.setObjectName(u"doubleSpinBox_flow_resistivity_DBM")
        self.doubleSpinBox_flow_resistivity_DBM.setMinimumSize(QSize(100, 28))
        self.doubleSpinBox_flow_resistivity_DBM.setMaximumSize(QSize(120, 28))
        self.doubleSpinBox_flow_resistivity_DBM.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.doubleSpinBox_flow_resistivity_DBM.setDecimals(6)
        self.doubleSpinBox_flow_resistivity_DBM.setMaximum(100000.000000000000000)
        self.doubleSpinBox_flow_resistivity_DBM.setValue(1518.506599999999935)

        self.gridLayout_7.addWidget(self.doubleSpinBox_flow_resistivity_DBM, 0, 2, 1, 1)

        self.label_11 = QLabel(self.frame_5)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setFont(font1)

        self.gridLayout_7.addWidget(self.label_11, 0, 3, 1, 1)


        self.gridLayout_5.addWidget(self.frame_5, 2, 0, 1, 1)

        self.frame = QFrame(self.tab_DBM)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 48))
        self.frame.setMaximumSize(QSize(16777215, 48))
        self.frame.setFrameShape(QFrame.Shape.NoFrame)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_24 = QGridLayout(self.frame)
        self.gridLayout_24.setObjectName(u"gridLayout_24")
        self.gridLayout_24.setContentsMargins(2, 2, 2, 2)
        self.label_51 = QLabel(self.frame)
        self.label_51.setObjectName(u"label_51")
        self.label_51.setFont(font1)
        self.label_51.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_24.addWidget(self.label_51, 0, 1, 1, 1)

        self.comboBox_DBM_constants = QComboBox(self.frame)
        self.comboBox_DBM_constants.addItem("")
        self.comboBox_DBM_constants.addItem("")
        self.comboBox_DBM_constants.addItem("")
        self.comboBox_DBM_constants.setObjectName(u"comboBox_DBM_constants")
        self.comboBox_DBM_constants.setMinimumSize(QSize(160, 0))
        self.comboBox_DBM_constants.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout_24.addWidget(self.comboBox_DBM_constants, 0, 2, 1, 1)

        self.horizontalSpacer_21 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_24.addItem(self.horizontalSpacer_21, 0, 3, 1, 1)

        self.horizontalSpacer_22 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_24.addItem(self.horizontalSpacer_22, 0, 0, 1, 1)


        self.gridLayout_5.addWidget(self.frame, 0, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_DBM, "")
        self.tab_JCAL = QWidget()
        self.tab_JCAL.setObjectName(u"tab_JCAL")
        self.gridLayout_14 = QGridLayout(self.tab_JCAL)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.gridLayout_14.setHorizontalSpacing(2)
        self.gridLayout_14.setVerticalSpacing(4)
        self.gridLayout_14.setContentsMargins(2, 8, 2, 8)
        self.frame_10 = QFrame(self.tab_JCAL)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_10.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_13 = QGridLayout(self.frame_10)
        self.gridLayout_13.setSpacing(6)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_13.setContentsMargins(6, 6, 6, 6)
        self.horizontalSpacer_17 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_13.addItem(self.horizontalSpacer_17, 1, 5, 1, 1)

        self.label_27 = QLabel(self.frame_10)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setMaximumSize(QSize(16777215, 28))
        self.label_27.setFont(font1)
        self.label_27.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_13.addWidget(self.label_27, 4, 1, 1, 1)

        self.label_37 = QLabel(self.frame_10)
        self.label_37.setObjectName(u"label_37")

        self.gridLayout_13.addWidget(self.label_37, 2, 3, 1, 1)

        self.doubleSpinBox_flow_resistivity_JCAL = QDoubleSpinBox(self.frame_10)
        self.doubleSpinBox_flow_resistivity_JCAL.setObjectName(u"doubleSpinBox_flow_resistivity_JCAL")
        self.doubleSpinBox_flow_resistivity_JCAL.setMinimumSize(QSize(100, 28))
        self.doubleSpinBox_flow_resistivity_JCAL.setMaximumSize(QSize(100, 28))
        self.doubleSpinBox_flow_resistivity_JCAL.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.doubleSpinBox_flow_resistivity_JCAL.setDecimals(4)
        self.doubleSpinBox_flow_resistivity_JCAL.setMaximum(100000.000000000000000)
        self.doubleSpinBox_flow_resistivity_JCAL.setValue(1518.506599999999935)

        self.gridLayout_13.addWidget(self.doubleSpinBox_flow_resistivity_JCAL, 6, 2, 1, 1)

        self.label_38 = QLabel(self.frame_10)
        self.label_38.setObjectName(u"label_38")

        self.gridLayout_13.addWidget(self.label_38, 1, 3, 1, 1)

        self.horizontalSpacer_15 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_13.addItem(self.horizontalSpacer_15, 1, 4, 1, 1)

        self.horizontalSpacer_16 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_13.addItem(self.horizontalSpacer_16, 1, 0, 1, 1)

        self.doubleSpinBox_porosity_JCAL = QDoubleSpinBox(self.frame_10)
        self.doubleSpinBox_porosity_JCAL.setObjectName(u"doubleSpinBox_porosity_JCAL")
        self.doubleSpinBox_porosity_JCAL.setMinimumSize(QSize(100, 28))
        self.doubleSpinBox_porosity_JCAL.setMaximumSize(QSize(100, 28))
        self.doubleSpinBox_porosity_JCAL.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.doubleSpinBox_porosity_JCAL.setDecimals(4)
        self.doubleSpinBox_porosity_JCAL.setMinimum(0.000000000000000)
        self.doubleSpinBox_porosity_JCAL.setMaximum(1.000000000000000)
        self.doubleSpinBox_porosity_JCAL.setSingleStep(0.100000000000000)
        self.doubleSpinBox_porosity_JCAL.setValue(0.900000000000000)

        self.gridLayout_13.addWidget(self.doubleSpinBox_porosity_JCAL, 1, 2, 1, 1)

        self.label_32 = QLabel(self.frame_10)
        self.label_32.setObjectName(u"label_32")

        self.gridLayout_13.addWidget(self.label_32, 3, 3, 1, 1)

        self.label_26 = QLabel(self.frame_10)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setFont(font1)

        self.gridLayout_13.addWidget(self.label_26, 6, 3, 1, 1)

        self.lineEdit_thermal_characteristic_length_JCAL = QLineEdit(self.frame_10)
        self.lineEdit_thermal_characteristic_length_JCAL.setObjectName(u"lineEdit_thermal_characteristic_length_JCAL")
        self.lineEdit_thermal_characteristic_length_JCAL.setMinimumSize(QSize(100, 28))
        self.lineEdit_thermal_characteristic_length_JCAL.setMaximumSize(QSize(100, 28))
        self.lineEdit_thermal_characteristic_length_JCAL.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_13.addWidget(self.lineEdit_thermal_characteristic_length_JCAL, 4, 2, 1, 1)

        self.label_15 = QLabel(self.frame_10)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setMaximumSize(QSize(16777215, 28))
        self.label_15.setFont(font1)
        self.label_15.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_13.addWidget(self.label_15, 1, 1, 1, 1)

        self.label_25 = QLabel(self.frame_10)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setFont(font1)
        self.label_25.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_13.addWidget(self.label_25, 6, 1, 1, 1)

        self.lineEdit_viscous_characteristic_length_JCAL = QLineEdit(self.frame_10)
        self.lineEdit_viscous_characteristic_length_JCAL.setObjectName(u"lineEdit_viscous_characteristic_length_JCAL")
        self.lineEdit_viscous_characteristic_length_JCAL.setMinimumSize(QSize(100, 28))
        self.lineEdit_viscous_characteristic_length_JCAL.setMaximumSize(QSize(100, 28))
        self.lineEdit_viscous_characteristic_length_JCAL.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_13.addWidget(self.lineEdit_viscous_characteristic_length_JCAL, 3, 2, 1, 1)

        self.label_18 = QLabel(self.frame_10)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setMaximumSize(QSize(16777215, 28))
        self.label_18.setFont(font1)
        self.label_18.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_13.addWidget(self.label_18, 2, 1, 1, 1)

        self.doubleSpinBox_tortuosity_JCAL = QDoubleSpinBox(self.frame_10)
        self.doubleSpinBox_tortuosity_JCAL.setObjectName(u"doubleSpinBox_tortuosity_JCAL")
        self.doubleSpinBox_tortuosity_JCAL.setMinimumSize(QSize(100, 28))
        self.doubleSpinBox_tortuosity_JCAL.setMaximumSize(QSize(100, 28))
        self.doubleSpinBox_tortuosity_JCAL.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.doubleSpinBox_tortuosity_JCAL.setDecimals(4)
        self.doubleSpinBox_tortuosity_JCAL.setMinimum(0.000000000000000)
        self.doubleSpinBox_tortuosity_JCAL.setMaximum(100.000000000000000)
        self.doubleSpinBox_tortuosity_JCAL.setValue(1.000000000000000)

        self.gridLayout_13.addWidget(self.doubleSpinBox_tortuosity_JCAL, 2, 2, 1, 1)

        self.label_28 = QLabel(self.frame_10)
        self.label_28.setObjectName(u"label_28")
        self.label_28.setMaximumSize(QSize(16777215, 28))
        self.label_28.setFont(font1)
        self.label_28.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_13.addWidget(self.label_28, 3, 1, 1, 1)

        self.label_35 = QLabel(self.frame_10)
        self.label_35.setObjectName(u"label_35")

        self.gridLayout_13.addWidget(self.label_35, 4, 3, 1, 1)


        self.gridLayout_14.addWidget(self.frame_10, 1, 0, 1, 1)

        self.frame_8 = QFrame(self.tab_JCAL)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setMinimumSize(QSize(0, 48))
        self.frame_8.setMaximumSize(QSize(16777215, 48))
        self.frame_8.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_8.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_25 = QGridLayout(self.frame_8)
        self.gridLayout_25.setObjectName(u"gridLayout_25")
        self.gridLayout_25.setContentsMargins(2, 2, 2, 2)
        self.label_52 = QLabel(self.frame_8)
        self.label_52.setObjectName(u"label_52")
        self.label_52.setFont(font1)
        self.label_52.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_25.addWidget(self.label_52, 0, 1, 1, 1)

        self.comboBox_JCAL_pm_model = QComboBox(self.frame_8)
        self.comboBox_JCAL_pm_model.addItem("")
        self.comboBox_JCAL_pm_model.addItem("")
        self.comboBox_JCAL_pm_model.setObjectName(u"comboBox_JCAL_pm_model")
        self.comboBox_JCAL_pm_model.setMinimumSize(QSize(252, 0))
        self.comboBox_JCAL_pm_model.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout_25.addWidget(self.comboBox_JCAL_pm_model, 0, 2, 1, 1)

        self.horizontalSpacer_23 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_25.addItem(self.horizontalSpacer_23, 0, 3, 1, 1)

        self.horizontalSpacer_24 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_25.addItem(self.horizontalSpacer_24, 0, 0, 1, 1)


        self.gridLayout_14.addWidget(self.frame_8, 0, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_JCAL, "")
        self.tab_edit = QWidget()
        self.tab_edit.setObjectName(u"tab_edit")
        self.gridLayout_21 = QGridLayout(self.tab_edit)
        self.gridLayout_21.setObjectName(u"gridLayout_21")
        self.tabWidget_models = QTabWidget(self.tab_edit)
        self.tabWidget_models.setObjectName(u"tabWidget_models")
        self.tabWidget_models.setEnabled(True)
        self.tabWidget_models.setTabsClosable(False)
        self.tabWidget_models.setTabBarAutoHide(False)
        self.tab_DB_and_DBM_parameters = QWidget()
        self.tab_DB_and_DBM_parameters.setObjectName(u"tab_DB_and_DBM_parameters")
        self.gridLayout_22 = QGridLayout(self.tab_DB_and_DBM_parameters)
        self.gridLayout_22.setObjectName(u"gridLayout_22")
        self.tableWidget_DBM = QTableWidget(self.tab_DB_and_DBM_parameters)
        if (self.tableWidget_DBM.rowCount() < 11):
            self.tableWidget_DBM.setRowCount(11)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_DBM.setVerticalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_DBM.setVerticalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        __qtablewidgetitem2.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_DBM.setVerticalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        __qtablewidgetitem3.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_DBM.setVerticalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        __qtablewidgetitem4.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_DBM.setVerticalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        __qtablewidgetitem5.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_DBM.setVerticalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        __qtablewidgetitem6.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_DBM.setVerticalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        __qtablewidgetitem7.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_DBM.setVerticalHeaderItem(7, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        __qtablewidgetitem8.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_DBM.setVerticalHeaderItem(8, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        __qtablewidgetitem9.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_DBM.setVerticalHeaderItem(9, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        __qtablewidgetitem10.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_DBM.setVerticalHeaderItem(10, __qtablewidgetitem10)
        self.tableWidget_DBM.setObjectName(u"tableWidget_DBM")
        self.tableWidget_DBM.horizontalHeader().setVisible(False)

        self.gridLayout_22.addWidget(self.tableWidget_DBM, 0, 0, 1, 1)

        self.tabWidget_models.addTab(self.tab_DB_and_DBM_parameters, "")
        self.tab_JCA_and_JCAL_parameters = QWidget()
        self.tab_JCA_and_JCAL_parameters.setObjectName(u"tab_JCA_and_JCAL_parameters")
        self.gridLayout_23 = QGridLayout(self.tab_JCA_and_JCAL_parameters)
        self.gridLayout_23.setObjectName(u"gridLayout_23")
        self.tableWidget_JCAL = QTableWidget(self.tab_JCA_and_JCAL_parameters)
        if (self.tableWidget_JCAL.rowCount() < 7):
            self.tableWidget_JCAL.setRowCount(7)
        __qtablewidgetitem11 = QTableWidgetItem()
        __qtablewidgetitem11.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_JCAL.setVerticalHeaderItem(0, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        __qtablewidgetitem12.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_JCAL.setVerticalHeaderItem(1, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        __qtablewidgetitem13.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_JCAL.setVerticalHeaderItem(2, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        __qtablewidgetitem14.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_JCAL.setVerticalHeaderItem(3, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        __qtablewidgetitem15.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_JCAL.setVerticalHeaderItem(4, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        __qtablewidgetitem16.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_JCAL.setVerticalHeaderItem(5, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        __qtablewidgetitem17.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_JCAL.setVerticalHeaderItem(6, __qtablewidgetitem17)
        self.tableWidget_JCAL.setObjectName(u"tableWidget_JCAL")
        self.tableWidget_JCAL.horizontalHeader().setVisible(False)
        self.tableWidget_JCAL.verticalHeader().setVisible(False)

        self.gridLayout_23.addWidget(self.tableWidget_JCAL, 0, 0, 1, 1)

        self.tabWidget_models.addTab(self.tab_JCA_and_JCAL_parameters, "")

        self.gridLayout_21.addWidget(self.tabWidget_models, 0, 0, 2, 1)

        self.tabWidget_main.addTab(self.tab_edit, "")
        self.tab_list = QWidget()
        self.tab_list.setObjectName(u"tab_list")
        self.gridLayout_16 = QGridLayout(self.tab_list)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.gridLayout_16.setContentsMargins(9, -1, -1, -1)
        self.frame_3 = QFrame(self.tab_list)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(320, 40))
        self.frame_3.setMaximumSize(QSize(16777215, 40))
        self.frame_3.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_15 = QGridLayout(self.frame_3)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.gridLayout_15.setHorizontalSpacing(12)
        self.gridLayout_15.setContentsMargins(4, 4, 4, 4)
        self.pushButton_reset = QPushButton(self.frame_3)
        self.pushButton_reset.setObjectName(u"pushButton_reset")
        self.pushButton_reset.setMinimumSize(QSize(100, 28))
        self.pushButton_reset.setMaximumSize(QSize(100, 28))
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        self.pushButton_reset.setFont(font2)
        self.pushButton_reset.setStyleSheet(u"")

        self.gridLayout_15.addWidget(self.pushButton_reset, 0, 0, 1, 1)

        self.pushButton_remove = QPushButton(self.frame_3)
        self.pushButton_remove.setObjectName(u"pushButton_remove")
        self.pushButton_remove.setMinimumSize(QSize(100, 28))
        self.pushButton_remove.setMaximumSize(QSize(100, 28))
        self.pushButton_remove.setFont(font2)
        self.pushButton_remove.setStyleSheet(u"")

        self.gridLayout_15.addWidget(self.pushButton_remove, 0, 1, 1, 1)


        self.gridLayout_16.addWidget(self.frame_3, 1, 0, 1, 1)

        self.treeWidget_porous_material_model = QTreeWidget(self.tab_list)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(2, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter);
        self.treeWidget_porous_material_model.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_porous_material_model.setObjectName(u"treeWidget_porous_material_model")
        self.treeWidget_porous_material_model.setMinimumSize(QSize(320, 100))
        self.treeWidget_porous_material_model.setMaximumSize(QSize(16777215, 200))
        font3 = QFont()
        font3.setFamilies([u"MS Shell Dlg 2"])
        font3.setPointSize(10)
        font3.setItalic(False)
        self.treeWidget_porous_material_model.setFont(font3)
        self.treeWidget_porous_material_model.setIndentation(1)
        self.treeWidget_porous_material_model.setHeaderHidden(False)
        self.treeWidget_porous_material_model.header().setHighlightSections(False)
        self.treeWidget_porous_material_model.header().setProperty(u"showSortIndicator", False)
        self.treeWidget_porous_material_model.header().setStretchLastSection(True)

        self.gridLayout_16.addWidget(self.treeWidget_porous_material_model, 0, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_list, "")

        self.gridLayout_20.addWidget(self.tabWidget_main, 0, 0, 1, 1)

        self.frame_plot_buttons = QFrame(self.scrollAreaWidgetContents)
        self.frame_plot_buttons.setObjectName(u"frame_plot_buttons")
        self.frame_plot_buttons.setMaximumSize(QSize(16777215, 48))
        self.frame_plot_buttons.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_plot_buttons.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_19 = QGridLayout(self.frame_plot_buttons)
        self.gridLayout_19.setObjectName(u"gridLayout_19")
        self.label_50 = QLabel(self.frame_plot_buttons)
        self.label_50.setObjectName(u"label_50")
        self.label_50.setMinimumSize(QSize(0, 28))
        self.label_50.setMaximumSize(QSize(16777215, 28))
        self.label_50.setFont(font1)
        self.label_50.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_19.addWidget(self.label_50, 0, 1, 1, 1)

        self.comboBox_plot_type = QComboBox(self.frame_plot_buttons)
        self.comboBox_plot_type.addItem("")
        self.comboBox_plot_type.addItem("")
        self.comboBox_plot_type.addItem("")
        self.comboBox_plot_type.addItem("")
        self.comboBox_plot_type.setObjectName(u"comboBox_plot_type")
        self.comboBox_plot_type.setMinimumSize(QSize(160, 28))
        self.comboBox_plot_type.setMaximumSize(QSize(200, 28))
        self.comboBox_plot_type.setFont(font1)

        self.gridLayout_19.addWidget(self.comboBox_plot_type, 0, 2, 1, 1)

        self.horizontalSpacer_19 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_19.addItem(self.horizontalSpacer_19, 0, 4, 1, 1)

        self.pushButton_plot_data = QPushButton(self.frame_plot_buttons)
        self.pushButton_plot_data.setObjectName(u"pushButton_plot_data")
        self.pushButton_plot_data.setMinimumSize(QSize(80, 28))
        self.pushButton_plot_data.setMaximumSize(QSize(220, 28))
        self.pushButton_plot_data.setFont(font1)

        self.gridLayout_19.addWidget(self.pushButton_plot_data, 0, 3, 1, 1)

        self.horizontalSpacer_20 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_19.addItem(self.horizontalSpacer_20, 0, 0, 1, 1)


        self.gridLayout_20.addWidget(self.frame_plot_buttons, 3, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_3.addWidget(self.scrollArea, 3, 0, 1, 1)

        self.frame_6 = QFrame(self.frame_main)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setMinimumSize(QSize(400, 40))
        self.frame_6.setMaximumSize(QSize(16777215, 80))
        self.frame_6.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_6.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_6.setLineWidth(1)
        self.gridLayout_8 = QGridLayout(self.frame_6)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(6, 6, 6, 6)
        self.comboBox_attribution_type = QComboBox(self.frame_6)
        self.comboBox_attribution_type.addItem("")
        self.comboBox_attribution_type.addItem("")
        self.comboBox_attribution_type.setObjectName(u"comboBox_attribution_type")
        self.comboBox_attribution_type.setMinimumSize(QSize(0, 28))
        self.comboBox_attribution_type.setMaximumSize(QSize(16777215, 28))
        self.comboBox_attribution_type.setFont(font1)

        self.gridLayout_8.addWidget(self.comboBox_attribution_type, 0, 3, 1, 1)

        self.lineEdit_selection_id = QLineEdit(self.frame_6)
        self.lineEdit_selection_id.setObjectName(u"lineEdit_selection_id")
        self.lineEdit_selection_id.setEnabled(True)
        self.lineEdit_selection_id.setMinimumSize(QSize(100, 28))
        self.lineEdit_selection_id.setMaximumSize(QSize(100, 28))
        self.lineEdit_selection_id.setFont(font1)
        self.lineEdit_selection_id.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.lineEdit_selection_id.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_8.addWidget(self.lineEdit_selection_id, 0, 2, 1, 1)

        self.label_12 = QLabel(self.frame_6)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setMinimumSize(QSize(0, 28))
        self.label_12.setMaximumSize(QSize(120, 28))
        font4 = QFont()
        font4.setFamilies([u"MS Shell Dlg 2"])
        font4.setPointSize(10)
        font4.setBold(False)
        self.label_12.setFont(font4)
        self.label_12.setTextFormat(Qt.TextFormat.AutoText)
        self.label_12.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_12, 0, 1, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_6, 0, 4, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_7, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_6, 0, 0, 1, 1)

        self.frame_7 = QFrame(self.frame_main)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_7.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_9 = QGridLayout(self.frame_7)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setHorizontalSpacing(2)
        self.gridLayout_9.setVerticalSpacing(4)
        self.gridLayout_9.setContentsMargins(2, 2, 2, 2)
        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer_8, 0, 2, 1, 1)

        self.checkBox_load_material_data_from_selection = QCheckBox(self.frame_7)
        self.checkBox_load_material_data_from_selection.setObjectName(u"checkBox_load_material_data_from_selection")
        self.checkBox_load_material_data_from_selection.setFont(font1)

        self.gridLayout_9.addWidget(self.checkBox_load_material_data_from_selection, 0, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer_2, 0, 0, 1, 1)

        self.checkBox_advanced_porous_material_plots = QCheckBox(self.frame_7)
        self.checkBox_advanced_porous_material_plots.setObjectName(u"checkBox_advanced_porous_material_plots")
        self.checkBox_advanced_porous_material_plots.setFont(font1)

        self.gridLayout_9.addWidget(self.checkBox_advanced_porous_material_plots, 1, 1, 1, 1)


        self.gridLayout_3.addWidget(self.frame_7, 2, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_main, 1, 0, 1, 1)

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
        font5 = QFont()
        font5.setPointSize(10)
        font5.setBold(False)
        font5.setItalic(False)
        self.pushButton_apply_and_close.setFont(font5)
        self.pushButton_apply_and_close.setStyleSheet(u"")
        self.pushButton_apply_and_close.setAutoDefault(False)
        self.pushButton_apply_and_close.setFlat(False)

        self.gridLayout_11.addWidget(self.pushButton_apply_and_close, 0, 3, 1, 1)

        self.pushButton_apply = QPushButton(self.frame_buttons)
        self.pushButton_apply.setObjectName(u"pushButton_apply")
        self.pushButton_apply.setMinimumSize(QSize(72, 30))
        self.pushButton_apply.setMaximumSize(QSize(72, 30))
        self.pushButton_apply.setFont(font5)
        self.pushButton_apply.setStyleSheet(u"")
        self.pushButton_apply.setAutoDefault(False)
        self.pushButton_apply.setFlat(False)

        self.gridLayout_11.addWidget(self.pushButton_apply, 0, 2, 1, 1)

        self.pushButton_cancel = QPushButton(self.frame_buttons)
        self.pushButton_cancel.setObjectName(u"pushButton_cancel")
        self.pushButton_cancel.setMinimumSize(QSize(72, 30))
        self.pushButton_cancel.setMaximumSize(QSize(72, 30))
        self.pushButton_cancel.setFont(font5)
        self.pushButton_cancel.setStyleSheet(u"")
        self.pushButton_cancel.setAutoDefault(False)
        self.pushButton_cancel.setFlat(False)

        self.gridLayout_11.addWidget(self.pushButton_cancel, 0, 0, 1, 1)

        self.horizontalSpacer_25 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_11.addItem(self.horizontalSpacer_25, 0, 1, 1, 1)


        self.gridLayout.addWidget(self.frame_buttons, 2, 0, 1, 1)

        QWidget.setTabOrder(self.doubleSpinBox_C1_DBM, self.doubleSpinBox_C2_DBM)
        QWidget.setTabOrder(self.doubleSpinBox_C2_DBM, self.doubleSpinBox_C3_DBM)
        QWidget.setTabOrder(self.doubleSpinBox_C3_DBM, self.doubleSpinBox_C4_DBM)
        QWidget.setTabOrder(self.doubleSpinBox_C4_DBM, self.doubleSpinBox_C5_DBM)
        QWidget.setTabOrder(self.doubleSpinBox_C5_DBM, self.doubleSpinBox_C6_DBM)
        QWidget.setTabOrder(self.doubleSpinBox_C6_DBM, self.doubleSpinBox_C7_DBM)
        QWidget.setTabOrder(self.doubleSpinBox_C7_DBM, self.doubleSpinBox_C8_DBM)
        QWidget.setTabOrder(self.doubleSpinBox_C8_DBM, self.doubleSpinBox_flow_resistivity_DBM)
        QWidget.setTabOrder(self.doubleSpinBox_flow_resistivity_DBM, self.pushButton_get_fluid)
        QWidget.setTabOrder(self.pushButton_get_fluid, self.doubleSpinBox_porous_material_depth)
        QWidget.setTabOrder(self.doubleSpinBox_porous_material_depth, self.comboBox_plot_type)
        QWidget.setTabOrder(self.comboBox_plot_type, self.pushButton_plot_data)
        QWidget.setTabOrder(self.pushButton_plot_data, self.doubleSpinBox_porosity_JCAL)
        QWidget.setTabOrder(self.doubleSpinBox_porosity_JCAL, self.doubleSpinBox_tortuosity_JCAL)
        QWidget.setTabOrder(self.doubleSpinBox_tortuosity_JCAL, self.lineEdit_viscous_characteristic_length_JCAL)
        QWidget.setTabOrder(self.lineEdit_viscous_characteristic_length_JCAL, self.lineEdit_thermal_characteristic_length_JCAL)
        QWidget.setTabOrder(self.lineEdit_thermal_characteristic_length_JCAL, self.doubleSpinBox_flow_resistivity_JCAL)
        QWidget.setTabOrder(self.doubleSpinBox_flow_resistivity_JCAL, self.comboBox_attribution_type)
        QWidget.setTabOrder(self.comboBox_attribution_type, self.pushButton_DB_equations)
        QWidget.setTabOrder(self.pushButton_DB_equations, self.treeWidget_porous_material_model)
        QWidget.setTabOrder(self.treeWidget_porous_material_model, self.pushButton_reset)
        QWidget.setTabOrder(self.pushButton_reset, self.pushButton_remove)

        self.retranslateUi(Dialog)

        self.tabWidget_main.setCurrentIndex(0)
        self.tabWidget_models.setCurrentIndex(0)
        self.pushButton_apply_and_close.setDefault(False)
        self.pushButton_apply.setDefault(False)
        self.pushButton_cancel.setDefault(False)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Vibra", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Configure the porous material model", None))
        self.label_17.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.lineEdit_speed_of_sound.setText("")
        self.label_47.setText(QCoreApplication.translate("Dialog", u"Speed of sound:", None))
        self.label_16.setText(QCoreApplication.translate("Dialog", u"Porous material depth:", None))
        self.label_49.setText(QCoreApplication.translate("Dialog", u"[m/s]", None))
        self.pushButton_get_fluid.setText(QCoreApplication.translate("Dialog", u"Get fluid", None))
        self.lineEdit_fluid_density.setText("")
        self.label_31.setText(QCoreApplication.translate("Dialog", u"Selected the fluid:", None))
        self.label_36.setText(QCoreApplication.translate("Dialog", u"Fluid density", None))
        self.lineEdit_selected_fluid.setText("")
        self.label_48.setText(QCoreApplication.translate("Dialog", u"[kg/m\u00b3]", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"C7:", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"C6:", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"C2:", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"C5:", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", u"C8:", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"C4:", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"C3:", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"C1:", None))
#if QT_CONFIG(tooltip)
        self.pushButton_DB_equations.setToolTip(QCoreApplication.translate("Dialog", u"See the equations for Delany-Bazley porous material model.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_DB_equations.setText("")
        self.label_10.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Flow resistivity <span style=\" font-size:11pt;\">\u03c3</span>:</p></body></html>", None))
        self.label_11.setText(QCoreApplication.translate("Dialog", u"[kg/m\u00b3.s]", None))
        self.label_51.setText(QCoreApplication.translate("Dialog", u"Constants from:", None))
        self.comboBox_DBM_constants.setItemText(0, QCoreApplication.translate("Dialog", u"Delany-Bazley", None))
        self.comboBox_DBM_constants.setItemText(1, QCoreApplication.translate("Dialog", u"Delany-Bazley-Miki", None))
        self.comboBox_DBM_constants.setItemText(2, QCoreApplication.translate("Dialog", u"User-defined (DBM)", None))

        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_DBM), QCoreApplication.translate("Dialog", u"DB/DBM models", None))
        self.label_27.setText(QCoreApplication.translate("Dialog", u"Thermal characteristic length:", None))
        self.label_37.setText(QCoreApplication.translate("Dialog", u"[--]", None))
        self.label_38.setText(QCoreApplication.translate("Dialog", u"[--]", None))
        self.label_32.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.label_26.setText(QCoreApplication.translate("Dialog", u"[kg/m\u00b3.s]", None))
        self.lineEdit_thermal_characteristic_length_JCAL.setText(QCoreApplication.translate("Dialog", u"159e-6", None))
        self.label_15.setText(QCoreApplication.translate("Dialog", u"Porosity:", None))
        self.label_25.setText(QCoreApplication.translate("Dialog", u"Flow resistivity:", None))
        self.lineEdit_viscous_characteristic_length_JCAL.setText(QCoreApplication.translate("Dialog", u"77e-6", None))
        self.label_18.setText(QCoreApplication.translate("Dialog", u"Tortuosity:", None))
        self.label_28.setText(QCoreApplication.translate("Dialog", u"Viscous characteristic length:", None))
        self.label_35.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.label_52.setText(QCoreApplication.translate("Dialog", u"Material model:", None))
        self.comboBox_JCAL_pm_model.setItemText(0, QCoreApplication.translate("Dialog", u"Jhonson-Champoux-Allard", None))
        self.comboBox_JCAL_pm_model.setItemText(1, QCoreApplication.translate("Dialog", u"Jhonson-Champoux-Allard-Lafarge", None))

        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_JCAL), QCoreApplication.translate("Dialog", u"JCA/JCAL models", None))
        ___qtablewidgetitem = self.tableWidget_DBM.verticalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Dialog", u"Identifier", None));
        ___qtablewidgetitem1 = self.tableWidget_DBM.verticalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Dialog", u"Model", None));
        ___qtablewidgetitem2 = self.tableWidget_DBM.verticalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Dialog", u"C1", None));
        ___qtablewidgetitem3 = self.tableWidget_DBM.verticalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Dialog", u"C2", None));
        ___qtablewidgetitem4 = self.tableWidget_DBM.verticalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Dialog", u"C3", None));
        ___qtablewidgetitem5 = self.tableWidget_DBM.verticalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Dialog", u"C4", None));
        ___qtablewidgetitem6 = self.tableWidget_DBM.verticalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("Dialog", u"C5", None));
        ___qtablewidgetitem7 = self.tableWidget_DBM.verticalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("Dialog", u"C6", None));
        ___qtablewidgetitem8 = self.tableWidget_DBM.verticalHeaderItem(8)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("Dialog", u"C7", None));
        ___qtablewidgetitem9 = self.tableWidget_DBM.verticalHeaderItem(9)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("Dialog", u"C8", None));
        ___qtablewidgetitem10 = self.tableWidget_DBM.verticalHeaderItem(10)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("Dialog", u"Flow Resistivity", None));
        self.tabWidget_models.setTabText(self.tabWidget_models.indexOf(self.tab_DB_and_DBM_parameters), QCoreApplication.translate("Dialog", u"DB / DBM", None))
        ___qtablewidgetitem11 = self.tableWidget_JCAL.verticalHeaderItem(0)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("Dialog", u"Identifier", None));
        ___qtablewidgetitem12 = self.tableWidget_JCAL.verticalHeaderItem(1)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("Dialog", u"Model", None));
        ___qtablewidgetitem13 = self.tableWidget_JCAL.verticalHeaderItem(2)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("Dialog", u"Porosity", None));
        ___qtablewidgetitem14 = self.tableWidget_JCAL.verticalHeaderItem(3)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("Dialog", u"Tortuosity", None));
        ___qtablewidgetitem15 = self.tableWidget_JCAL.verticalHeaderItem(4)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("Dialog", u"Viscous Char. Length", None));
        ___qtablewidgetitem16 = self.tableWidget_JCAL.verticalHeaderItem(5)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("Dialog", u"Thermal Char. Length", None));
        ___qtablewidgetitem17 = self.tableWidget_JCAL.verticalHeaderItem(6)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("Dialog", u"Flow Resistivity", None));
        self.tabWidget_models.setTabText(self.tabWidget_models.indexOf(self.tab_JCA_and_JCAL_parameters), QCoreApplication.translate("Dialog", u"JCA / JCAL", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_edit), QCoreApplication.translate("Dialog", u"Edit", None))
        self.pushButton_reset.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.pushButton_remove.setText(QCoreApplication.translate("Dialog", u"Remove", None))
        ___qtreewidgetitem = self.treeWidget_porous_material_model.headerItem()
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("Dialog", u"Identifier", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"Model", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Volumes", None));
#if QT_CONFIG(tooltip)
        self.treeWidget_porous_material_model.setToolTip(QCoreApplication.translate("Dialog", u"Select a face to remove the previously attributed boundary condition.", None))
#endif // QT_CONFIG(tooltip)
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_list), QCoreApplication.translate("Dialog", u"List", None))
        self.label_50.setText(QCoreApplication.translate("Dialog", u"Plot selector:", None))
        self.comboBox_plot_type.setItemText(0, QCoreApplication.translate("Dialog", u" Fluid density", None))
        self.comboBox_plot_type.setItemText(1, QCoreApplication.translate("Dialog", u" Speed of sound", None))
        self.comboBox_plot_type.setItemText(2, QCoreApplication.translate("Dialog", u" Surface impedance", None))
        self.comboBox_plot_type.setItemText(3, QCoreApplication.translate("Dialog", u" Absorption coefficient", None))

        self.pushButton_plot_data.setText(QCoreApplication.translate("Dialog", u"Plot data", None))
        self.comboBox_attribution_type.setItemText(0, QCoreApplication.translate("Dialog", u" All bodies", None))
        self.comboBox_attribution_type.setItemText(1, QCoreApplication.translate("Dialog", u" Selected bodies", None))

        self.lineEdit_selection_id.setText("")
        self.label_12.setText(QCoreApplication.translate("Dialog", u"Selected bodies:", None))
        self.checkBox_load_material_data_from_selection.setText(QCoreApplication.translate("Dialog", u"Load porous material data from selection", None))
        self.checkBox_advanced_porous_material_plots.setText(QCoreApplication.translate("Dialog", u"Enable the advanced porous material plots", None))
        self.pushButton_apply_and_close.setText(QCoreApplication.translate("Dialog", u"Ok", None))
        self.pushButton_apply.setText(QCoreApplication.translate("Dialog", u"Apply", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
    # retranslateUi



class PorousMaterialModelInputs_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame_top: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
                - frame_main: QFrame
                    - (Layout): QGridLayout
                            - scrollArea: QScrollArea
                                - scrollAreaWidgetContents: QWidget
                                    - (Layout): QGridLayout
                                            - frame_plot_setup: QFrame
                                                - (Layout): QGridLayout
                                                        - label_17: QLabel
                                                        - lineEdit_speed_of_sound: QLineEdit
                                                        - label_47: QLabel
                                                        - doubleSpinBox_porous_material_depth: QDoubleSpinBox
                                                        - label_16: QLabel
                                                        - label_49: QLabel
                                                        - pushButton_get_fluid: QPushButton
                                                        - lineEdit_fluid_density: QLineEdit
                                                        - label_31: QLabel
                                                        - label_36: QLabel
                                                        - lineEdit_selected_fluid: QLineEdit
                                                        - label_48: QLabel
                                                        - frame_2: QFrame
                                            - tabWidget_main: QTabWidget
                                                - tab_DBM: QWidget
                                                    - (Layout): QGridLayout
                                                            - frame_4: QFrame
                                                                - (Layout): QGridLayout
                                                                        - label_8: QLabel
                                                                        - label_7: QLabel
                                                                        - label_3: QLabel
                                                                        - doubleSpinBox_C4_DBM: QDoubleSpinBox
                                                                        - label_6: QLabel
                                                                        - doubleSpinBox_C5_DBM: QDoubleSpinBox
                                                                        - doubleSpinBox_C6_DBM: QDoubleSpinBox
                                                                        - doubleSpinBox_C7_DBM: QDoubleSpinBox
                                                                        - label_9: QLabel
                                                                        - doubleSpinBox_C8_DBM: QDoubleSpinBox
                                                                        - label_5: QLabel
                                                                        - label_4: QLabel
                                                                        - doubleSpinBox_C3_DBM: QDoubleSpinBox
                                                                        - label_2: QLabel
                                                                        - doubleSpinBox_C1_DBM: QDoubleSpinBox
                                                                        - doubleSpinBox_C2_DBM: QDoubleSpinBox
                                                                        - pushButton_DB_equations: QPushButton
                                                            - frame_5: QFrame
                                                                - (Layout): QGridLayout
                                                                        - label_10: QLabel
                                                                        - doubleSpinBox_flow_resistivity_DBM: QDoubleSpinBox
                                                                        - label_11: QLabel
                                                            - frame: QFrame
                                                                - (Layout): QGridLayout
                                                                        - label_51: QLabel
                                                                        - comboBox_DBM_constants: QComboBox
                                                - tab_JCAL: QWidget
                                                    - (Layout): QGridLayout
                                                            - frame_10: QFrame
                                                                - (Layout): QGridLayout
                                                                        - label_27: QLabel
                                                                        - label_37: QLabel
                                                                        - doubleSpinBox_flow_resistivity_JCAL: QDoubleSpinBox
                                                                        - label_38: QLabel
                                                                        - doubleSpinBox_porosity_JCAL: QDoubleSpinBox
                                                                        - label_32: QLabel
                                                                        - label_26: QLabel
                                                                        - lineEdit_thermal_characteristic_length_JCAL: QLineEdit
                                                                        - label_15: QLabel
                                                                        - label_25: QLabel
                                                                        - lineEdit_viscous_characteristic_length_JCAL: QLineEdit
                                                                        - label_18: QLabel
                                                                        - doubleSpinBox_tortuosity_JCAL: QDoubleSpinBox
                                                                        - label_28: QLabel
                                                                        - label_35: QLabel
                                                            - frame_8: QFrame
                                                                - (Layout): QGridLayout
                                                                        - label_52: QLabel
                                                                        - comboBox_JCAL_pm_model: QComboBox
                                                - tab_edit: QWidget
                                                    - (Layout): QGridLayout
                                                            - tabWidget_models: QTabWidget
                                                                - tab_DB_and_DBM_parameters: QWidget
                                                                    - (Layout): QGridLayout
                                                                            - tableWidget_DBM: QTableWidget
                                                                - tab_JCA_and_JCAL_parameters: QWidget
                                                                    - (Layout): QGridLayout
                                                                            - tableWidget_JCAL: QTableWidget
                                                - tab_list: QWidget
                                                    - (Layout): QGridLayout
                                                            - frame_3: QFrame
                                                                - (Layout): QGridLayout
                                                                        - pushButton_reset: QPushButton
                                                                        - pushButton_remove: QPushButton
                                                            - treeWidget_porous_material_model: QTreeWidget
                                            - frame_plot_buttons: QFrame
                                                - (Layout): QGridLayout
                                                        - label_50: QLabel
                                                        - comboBox_plot_type: QComboBox
                                                        - pushButton_plot_data: QPushButton
                            - frame_6: QFrame
                                - (Layout): QGridLayout
                                        - comboBox_attribution_type: QComboBox
                                        - lineEdit_selection_id: QLineEdit
                                        - label_12: QLabel
                            - frame_7: QFrame
                                - (Layout): QGridLayout
                                        - checkBox_load_material_data_from_selection: QCheckBox
                                        - checkBox_advanced_porous_material_plots: QCheckBox
                - frame_buttons: QFrame
                    - (Layout): QGridLayout
                            - pushButton_apply_and_close: QPushButton
                            - pushButton_apply: QPushButton
                            - pushButton_cancel: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
