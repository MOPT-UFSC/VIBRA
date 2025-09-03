# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'porous_material_model_inputs.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
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
    QFrame, QGridLayout, QHeaderView, QLabel,
    QLineEdit, QPushButton, QScrollArea, QSizePolicy,
    QSpacerItem, QTabWidget, QTableWidget, QTableWidgetItem,
    QTreeWidget, QTreeWidgetItem, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(531, 446)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.frame_top = QFrame(Dialog)
        self.frame_top.setObjectName(u"frame_top")
        self.frame_top.setMinimumSize(QSize(0, 48))
        self.frame_top.setMaximumSize(QSize(16777215, 48))
        self.frame_top.setFrameShape(QFrame.Box)
        self.frame_top.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_top)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label = QLabel(self.frame_top)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_top, 0, 0, 1, 1)

        self.frame_main = QFrame(Dialog)
        self.frame_main.setObjectName(u"frame_main")
        self.frame_main.setFrameShape(QFrame.Box)
        self.frame_main.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_main)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(4, 4, 4, 4)
        self.frame_6 = QFrame(self.frame_main)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setMinimumSize(QSize(400, 40))
        self.frame_6.setMaximumSize(QSize(16777215, 80))
        self.frame_6.setFrameShape(QFrame.NoFrame)
        self.frame_6.setFrameShadow(QFrame.Raised)
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
        font1 = QFont()
        font1.setPointSize(10)
        self.comboBox_attribution_type.setFont(font1)

        self.gridLayout_8.addWidget(self.comboBox_attribution_type, 0, 3, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_6, 0, 4, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_7, 0, 0, 1, 1)

        self.label_12 = QLabel(self.frame_6)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setMinimumSize(QSize(0, 28))
        self.label_12.setMaximumSize(QSize(120, 28))
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        font2.setPointSize(10)
        font2.setBold(False)
        self.label_12.setFont(font2)
        self.label_12.setTextFormat(Qt.AutoText)
        self.label_12.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_12, 0, 1, 1, 1)

        self.lineEdit_selection_id = QLineEdit(self.frame_6)
        self.lineEdit_selection_id.setObjectName(u"lineEdit_selection_id")
        self.lineEdit_selection_id.setEnabled(True)
        self.lineEdit_selection_id.setMinimumSize(QSize(100, 28))
        self.lineEdit_selection_id.setMaximumSize(QSize(100, 28))
        self.lineEdit_selection_id.setFont(font1)
        self.lineEdit_selection_id.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_selection_id.setAlignment(Qt.AlignCenter)

        self.gridLayout_8.addWidget(self.lineEdit_selection_id, 0, 2, 1, 1)


        self.gridLayout_3.addWidget(self.frame_6, 0, 0, 1, 1)

        self.scrollArea = QScrollArea(self.frame_main)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setFrameShape(QFrame.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 494, 500))
        self.gridLayout_20 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_20.setObjectName(u"gridLayout_20")
        self.tabWidget_main = QTabWidget(self.scrollAreaWidgetContents)
        self.tabWidget_main.setObjectName(u"tabWidget_main")
        self.tabWidget_main.setMinimumSize(QSize(0, 260))
        self.tabWidget_main.setMaximumSize(QSize(16777215, 16777215))
        self.tabWidget_main.setSizeIncrement(QSize(0, 0))
        self.tabWidget_main.setFont(font1)
        self.tabWidget_main.setTabBarAutoHide(False)
        self.tab_Delany_Bazley = QWidget()
        self.tab_Delany_Bazley.setObjectName(u"tab_Delany_Bazley")
        self.gridLayout_5 = QGridLayout(self.tab_Delany_Bazley)
        self.gridLayout_5.setSpacing(4)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(4, 4, 4, 4)
        self.frame_4 = QFrame(self.tab_Delany_Bazley)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.gridLayout_6 = QGridLayout(self.frame_4)
        self.gridLayout_6.setSpacing(6)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(6, 6, 6, 6)
        self.label_8 = QLabel(self.frame_4)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setFont(font1)
        self.label_8.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_8, 2, 4, 1, 1)

        self.label_7 = QLabel(self.frame_4)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font1)
        self.label_7.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_7, 1, 4, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_3, 0, 0, 1, 1)

        self.label_3 = QLabel(self.frame_4)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font1)
        self.label_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_3, 1, 1, 1, 1)

        self.doubleSpinBox_C4_DB = QDoubleSpinBox(self.frame_4)
        self.doubleSpinBox_C4_DB.setObjectName(u"doubleSpinBox_C4_DB")
        self.doubleSpinBox_C4_DB.setMinimumSize(QSize(100, 28))
        self.doubleSpinBox_C4_DB.setMaximumSize(QSize(100, 28))
        self.doubleSpinBox_C4_DB.setAlignment(Qt.AlignCenter)
        self.doubleSpinBox_C4_DB.setDecimals(4)
        self.doubleSpinBox_C4_DB.setMinimum(-100.000000000000000)
        self.doubleSpinBox_C4_DB.setMaximum(100.000000000000000)
        self.doubleSpinBox_C4_DB.setValue(0.595000000000000)

        self.gridLayout_6.addWidget(self.doubleSpinBox_C4_DB, 3, 2, 1, 1)

        self.label_6 = QLabel(self.frame_4)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font1)
        self.label_6.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_6, 0, 4, 1, 1)

        self.doubleSpinBox_C5_DB = QDoubleSpinBox(self.frame_4)
        self.doubleSpinBox_C5_DB.setObjectName(u"doubleSpinBox_C5_DB")
        self.doubleSpinBox_C5_DB.setMinimumSize(QSize(100, 28))
        self.doubleSpinBox_C5_DB.setMaximumSize(QSize(100, 28))
        self.doubleSpinBox_C5_DB.setAlignment(Qt.AlignCenter)
        self.doubleSpinBox_C5_DB.setDecimals(4)
        self.doubleSpinBox_C5_DB.setMinimum(-100.000000000000000)
        self.doubleSpinBox_C5_DB.setMaximum(100.000000000000000)
        self.doubleSpinBox_C5_DB.setValue(0.049700000000000)

        self.gridLayout_6.addWidget(self.doubleSpinBox_C5_DB, 0, 5, 1, 1)

        self.doubleSpinBox_C6_DB = QDoubleSpinBox(self.frame_4)
        self.doubleSpinBox_C6_DB.setObjectName(u"doubleSpinBox_C6_DB")
        self.doubleSpinBox_C6_DB.setMinimumSize(QSize(100, 28))
        self.doubleSpinBox_C6_DB.setMaximumSize(QSize(100, 28))
        self.doubleSpinBox_C6_DB.setAlignment(Qt.AlignCenter)
        self.doubleSpinBox_C6_DB.setDecimals(4)
        self.doubleSpinBox_C6_DB.setMinimum(-100.000000000000000)
        self.doubleSpinBox_C6_DB.setMaximum(100.000000000000000)
        self.doubleSpinBox_C6_DB.setValue(0.754000000000000)

        self.gridLayout_6.addWidget(self.doubleSpinBox_C6_DB, 1, 5, 1, 1)

        self.doubleSpinBox_C7_DB = QDoubleSpinBox(self.frame_4)
        self.doubleSpinBox_C7_DB.setObjectName(u"doubleSpinBox_C7_DB")
        self.doubleSpinBox_C7_DB.setMinimumSize(QSize(100, 28))
        self.doubleSpinBox_C7_DB.setMaximumSize(QSize(100, 28))
        self.doubleSpinBox_C7_DB.setAlignment(Qt.AlignCenter)
        self.doubleSpinBox_C7_DB.setDecimals(4)
        self.doubleSpinBox_C7_DB.setMinimum(-100.000000000000000)
        self.doubleSpinBox_C7_DB.setMaximum(100.000000000000000)
        self.doubleSpinBox_C7_DB.setValue(0.075800000000000)

        self.gridLayout_6.addWidget(self.doubleSpinBox_C7_DB, 2, 5, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer, 0, 6, 1, 1)

        self.label_9 = QLabel(self.frame_4)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setFont(font1)
        self.label_9.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_9, 3, 4, 1, 1)

        self.doubleSpinBox_C8_DB = QDoubleSpinBox(self.frame_4)
        self.doubleSpinBox_C8_DB.setObjectName(u"doubleSpinBox_C8_DB")
        self.doubleSpinBox_C8_DB.setMinimumSize(QSize(100, 28))
        self.doubleSpinBox_C8_DB.setMaximumSize(QSize(100, 28))
        self.doubleSpinBox_C8_DB.setAlignment(Qt.AlignCenter)
        self.doubleSpinBox_C8_DB.setDecimals(4)
        self.doubleSpinBox_C8_DB.setMinimum(-100.000000000000000)
        self.doubleSpinBox_C8_DB.setMaximum(100.000000000000000)
        self.doubleSpinBox_C8_DB.setValue(0.732000000000000)

        self.gridLayout_6.addWidget(self.doubleSpinBox_C8_DB, 3, 5, 1, 1)

        self.label_5 = QLabel(self.frame_4)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font1)
        self.label_5.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_5, 3, 1, 1, 1)

        self.label_4 = QLabel(self.frame_4)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font1)
        self.label_4.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_4, 2, 1, 1, 1)

        self.doubleSpinBox_C3_DB = QDoubleSpinBox(self.frame_4)
        self.doubleSpinBox_C3_DB.setObjectName(u"doubleSpinBox_C3_DB")
        self.doubleSpinBox_C3_DB.setMinimumSize(QSize(100, 28))
        self.doubleSpinBox_C3_DB.setMaximumSize(QSize(100, 28))
        self.doubleSpinBox_C3_DB.setAlignment(Qt.AlignCenter)
        self.doubleSpinBox_C3_DB.setDecimals(4)
        self.doubleSpinBox_C3_DB.setMinimum(-100.000000000000000)
        self.doubleSpinBox_C3_DB.setMaximum(100.000000000000000)
        self.doubleSpinBox_C3_DB.setValue(0.169000000000000)

        self.gridLayout_6.addWidget(self.doubleSpinBox_C3_DB, 2, 2, 1, 1)

        self.label_2 = QLabel(self.frame_4)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font1)
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_2, 0, 1, 1, 1)

        self.doubleSpinBox_C1_DB = QDoubleSpinBox(self.frame_4)
        self.doubleSpinBox_C1_DB.setObjectName(u"doubleSpinBox_C1_DB")
        self.doubleSpinBox_C1_DB.setMinimumSize(QSize(100, 28))
        self.doubleSpinBox_C1_DB.setMaximumSize(QSize(100, 28))
        self.doubleSpinBox_C1_DB.setAlignment(Qt.AlignCenter)
        self.doubleSpinBox_C1_DB.setDecimals(4)
        self.doubleSpinBox_C1_DB.setMinimum(-100.000000000000000)
        self.doubleSpinBox_C1_DB.setMaximum(100.000000000000000)
        self.doubleSpinBox_C1_DB.setValue(0.085800000000000)

        self.gridLayout_6.addWidget(self.doubleSpinBox_C1_DB, 0, 2, 1, 1)

        self.doubleSpinBox_C2_DB = QDoubleSpinBox(self.frame_4)
        self.doubleSpinBox_C2_DB.setObjectName(u"doubleSpinBox_C2_DB")
        self.doubleSpinBox_C2_DB.setMinimumSize(QSize(100, 28))
        self.doubleSpinBox_C2_DB.setMaximumSize(QSize(100, 28))
        self.doubleSpinBox_C2_DB.setAlignment(Qt.AlignCenter)
        self.doubleSpinBox_C2_DB.setDecimals(4)
        self.doubleSpinBox_C2_DB.setMinimum(-100.000000000000000)
        self.doubleSpinBox_C2_DB.setMaximum(100.000000000000000)
        self.doubleSpinBox_C2_DB.setValue(0.700000000000000)

        self.gridLayout_6.addWidget(self.doubleSpinBox_C2_DB, 1, 2, 1, 1)

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


        self.gridLayout_5.addWidget(self.frame_4, 0, 0, 1, 1)

        self.frame_5 = QFrame(self.tab_Delany_Bazley)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setMinimumSize(QSize(0, 48))
        self.frame_5.setMaximumSize(QSize(16777215, 48))
        self.frame_5.setFrameShape(QFrame.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Raised)
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

        self.doubleSpinBox_flow_resistivity_DB = QDoubleSpinBox(self.frame_5)
        self.doubleSpinBox_flow_resistivity_DB.setObjectName(u"doubleSpinBox_flow_resistivity_DB")
        self.doubleSpinBox_flow_resistivity_DB.setMinimumSize(QSize(100, 28))
        self.doubleSpinBox_flow_resistivity_DB.setMaximumSize(QSize(100, 28))
        self.doubleSpinBox_flow_resistivity_DB.setAlignment(Qt.AlignCenter)
        self.doubleSpinBox_flow_resistivity_DB.setDecimals(4)
        self.doubleSpinBox_flow_resistivity_DB.setMaximum(100000.000000000000000)
        self.doubleSpinBox_flow_resistivity_DB.setValue(1518.506599999999935)

        self.gridLayout_7.addWidget(self.doubleSpinBox_flow_resistivity_DB, 0, 2, 1, 1)

        self.label_11 = QLabel(self.frame_5)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setFont(font1)

        self.gridLayout_7.addWidget(self.label_11, 0, 3, 1, 1)


        self.gridLayout_5.addWidget(self.frame_5, 1, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_Delany_Bazley, "")
        self.tab_Delany_Bazley_Miki = QWidget()
        self.tab_Delany_Bazley_Miki.setObjectName(u"tab_Delany_Bazley_Miki")
        self.gridLayout_17 = QGridLayout(self.tab_Delany_Bazley_Miki)
        self.gridLayout_17.setSpacing(4)
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.gridLayout_17.setContentsMargins(4, 4, 4, 4)
        self.frame_8 = QFrame(self.tab_Delany_Bazley_Miki)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setFrameShape(QFrame.NoFrame)
        self.frame_8.setFrameShadow(QFrame.Raised)
        self.gridLayout_10 = QGridLayout(self.frame_8)
        self.gridLayout_10.setSpacing(6)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(6, 6, 6, 6)
        self.doubleSpinBox_C4_DBM = QDoubleSpinBox(self.frame_8)
        self.doubleSpinBox_C4_DBM.setObjectName(u"doubleSpinBox_C4_DBM")
        self.doubleSpinBox_C4_DBM.setMinimumSize(QSize(100, 28))
        self.doubleSpinBox_C4_DBM.setMaximumSize(QSize(100, 28))
        self.doubleSpinBox_C4_DBM.setAlignment(Qt.AlignCenter)
        self.doubleSpinBox_C4_DBM.setDecimals(4)
        self.doubleSpinBox_C4_DBM.setMinimum(-100.000000000000000)
        self.doubleSpinBox_C4_DBM.setMaximum(100.000000000000000)
        self.doubleSpinBox_C4_DBM.setValue(0.618000000000000)

        self.gridLayout_10.addWidget(self.doubleSpinBox_C4_DBM, 3, 2, 1, 1)

        self.doubleSpinBox_C5_DBM = QDoubleSpinBox(self.frame_8)
        self.doubleSpinBox_C5_DBM.setObjectName(u"doubleSpinBox_C5_DBM")
        self.doubleSpinBox_C5_DBM.setMinimumSize(QSize(100, 28))
        self.doubleSpinBox_C5_DBM.setMaximumSize(QSize(100, 28))
        self.doubleSpinBox_C5_DBM.setAlignment(Qt.AlignCenter)
        self.doubleSpinBox_C5_DBM.setDecimals(4)
        self.doubleSpinBox_C5_DBM.setMinimum(-100.000000000000000)
        self.doubleSpinBox_C5_DBM.setMaximum(100.000000000000000)
        self.doubleSpinBox_C5_DBM.setValue(0.069900000000000)

        self.gridLayout_10.addWidget(self.doubleSpinBox_C5_DBM, 0, 5, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_10.addItem(self.horizontalSpacer_2, 0, 6, 1, 1)

        self.label_39 = QLabel(self.frame_8)
        self.label_39.setObjectName(u"label_39")
        self.label_39.setFont(font1)
        self.label_39.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_39, 0, 4, 1, 1)

        self.doubleSpinBox_C7_DBM = QDoubleSpinBox(self.frame_8)
        self.doubleSpinBox_C7_DBM.setObjectName(u"doubleSpinBox_C7_DBM")
        self.doubleSpinBox_C7_DBM.setMinimumSize(QSize(100, 28))
        self.doubleSpinBox_C7_DBM.setMaximumSize(QSize(100, 28))
        self.doubleSpinBox_C7_DBM.setAlignment(Qt.AlignCenter)
        self.doubleSpinBox_C7_DBM.setDecimals(4)
        self.doubleSpinBox_C7_DBM.setMinimum(-100.000000000000000)
        self.doubleSpinBox_C7_DBM.setMaximum(100.000000000000000)
        self.doubleSpinBox_C7_DBM.setValue(0.107000000000000)

        self.gridLayout_10.addWidget(self.doubleSpinBox_C7_DBM, 2, 5, 1, 1)

        self.label_40 = QLabel(self.frame_8)
        self.label_40.setObjectName(u"label_40")
        self.label_40.setFont(font1)
        self.label_40.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_40, 3, 4, 1, 1)

        self.doubleSpinBox_C8_DBM = QDoubleSpinBox(self.frame_8)
        self.doubleSpinBox_C8_DBM.setObjectName(u"doubleSpinBox_C8_DBM")
        self.doubleSpinBox_C8_DBM.setMinimumSize(QSize(100, 28))
        self.doubleSpinBox_C8_DBM.setMaximumSize(QSize(100, 28))
        self.doubleSpinBox_C8_DBM.setAlignment(Qt.AlignCenter)
        self.doubleSpinBox_C8_DBM.setDecimals(4)
        self.doubleSpinBox_C8_DBM.setMinimum(-100.000000000000000)
        self.doubleSpinBox_C8_DBM.setMaximum(100.000000000000000)
        self.doubleSpinBox_C8_DBM.setValue(0.632000000000000)

        self.gridLayout_10.addWidget(self.doubleSpinBox_C8_DBM, 3, 5, 1, 1)

        self.doubleSpinBox_C3_DBM = QDoubleSpinBox(self.frame_8)
        self.doubleSpinBox_C3_DBM.setObjectName(u"doubleSpinBox_C3_DBM")
        self.doubleSpinBox_C3_DBM.setMinimumSize(QSize(100, 28))
        self.doubleSpinBox_C3_DBM.setMaximumSize(QSize(100, 28))
        self.doubleSpinBox_C3_DBM.setAlignment(Qt.AlignCenter)
        self.doubleSpinBox_C3_DBM.setDecimals(4)
        self.doubleSpinBox_C3_DBM.setMinimum(-100.000000000000000)
        self.doubleSpinBox_C3_DBM.setMaximum(100.000000000000000)
        self.doubleSpinBox_C3_DBM.setValue(0.160000000000000)

        self.gridLayout_10.addWidget(self.doubleSpinBox_C3_DBM, 2, 2, 1, 1)

        self.label_41 = QLabel(self.frame_8)
        self.label_41.setObjectName(u"label_41")
        self.label_41.setFont(font1)
        self.label_41.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_41, 3, 1, 1, 1)

        self.label_42 = QLabel(self.frame_8)
        self.label_42.setObjectName(u"label_42")
        self.label_42.setFont(font1)
        self.label_42.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_42, 0, 1, 1, 1)

        self.label_43 = QLabel(self.frame_8)
        self.label_43.setObjectName(u"label_43")
        self.label_43.setFont(font1)
        self.label_43.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_43, 2, 1, 1, 1)

        self.doubleSpinBox_C1_DBM = QDoubleSpinBox(self.frame_8)
        self.doubleSpinBox_C1_DBM.setObjectName(u"doubleSpinBox_C1_DBM")
        self.doubleSpinBox_C1_DBM.setMinimumSize(QSize(100, 28))
        self.doubleSpinBox_C1_DBM.setMaximumSize(QSize(100, 28))
        self.doubleSpinBox_C1_DBM.setAlignment(Qt.AlignCenter)
        self.doubleSpinBox_C1_DBM.setDecimals(4)
        self.doubleSpinBox_C1_DBM.setMinimum(-100.000000000000000)
        self.doubleSpinBox_C1_DBM.setMaximum(100.000000000000000)
        self.doubleSpinBox_C1_DBM.setValue(0.109000000000000)

        self.gridLayout_10.addWidget(self.doubleSpinBox_C1_DBM, 0, 2, 1, 1)

        self.doubleSpinBox_C2_DBM = QDoubleSpinBox(self.frame_8)
        self.doubleSpinBox_C2_DBM.setObjectName(u"doubleSpinBox_C2_DBM")
        self.doubleSpinBox_C2_DBM.setMinimumSize(QSize(100, 28))
        self.doubleSpinBox_C2_DBM.setMaximumSize(QSize(100, 28))
        self.doubleSpinBox_C2_DBM.setAlignment(Qt.AlignCenter)
        self.doubleSpinBox_C2_DBM.setDecimals(4)
        self.doubleSpinBox_C2_DBM.setMinimum(-100.000000000000000)
        self.doubleSpinBox_C2_DBM.setMaximum(100.000000000000000)
        self.doubleSpinBox_C2_DBM.setValue(0.618000000000000)

        self.gridLayout_10.addWidget(self.doubleSpinBox_C2_DBM, 1, 2, 1, 1)

        self.label_44 = QLabel(self.frame_8)
        self.label_44.setObjectName(u"label_44")
        self.label_44.setFont(font1)
        self.label_44.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_44, 1, 1, 1, 1)

        self.label_19 = QLabel(self.frame_8)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setFont(font1)
        self.label_19.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_19, 2, 4, 1, 1)

        self.label_20 = QLabel(self.frame_8)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setFont(font1)
        self.label_20.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_20, 1, 4, 1, 1)

        self.doubleSpinBox_C6_DBM = QDoubleSpinBox(self.frame_8)
        self.doubleSpinBox_C6_DBM.setObjectName(u"doubleSpinBox_C6_DBM")
        self.doubleSpinBox_C6_DBM.setMinimumSize(QSize(100, 28))
        self.doubleSpinBox_C6_DBM.setMaximumSize(QSize(100, 28))
        self.doubleSpinBox_C6_DBM.setAlignment(Qt.AlignCenter)
        self.doubleSpinBox_C6_DBM.setDecimals(4)
        self.doubleSpinBox_C6_DBM.setMinimum(-100.000000000000000)
        self.doubleSpinBox_C6_DBM.setMaximum(100.000000000000000)
        self.doubleSpinBox_C6_DBM.setValue(0.632000000000000)

        self.gridLayout_10.addWidget(self.doubleSpinBox_C6_DBM, 1, 5, 1, 1)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_10.addItem(self.horizontalSpacer_11, 0, 0, 1, 1)

        self.pushButton_DBM_equations = QPushButton(self.frame_8)
        self.pushButton_DBM_equations.setObjectName(u"pushButton_DBM_equations")
        self.pushButton_DBM_equations.setMinimumSize(QSize(40, 28))
        self.pushButton_DBM_equations.setMaximumSize(QSize(100, 28))
        self.pushButton_DBM_equations.setFont(font1)
        self.pushButton_DBM_equations.setIcon(icon)
        self.pushButton_DBM_equations.setIconSize(QSize(18, 18))

        self.gridLayout_10.addWidget(self.pushButton_DBM_equations, 0, 3, 1, 1)


        self.gridLayout_17.addWidget(self.frame_8, 0, 0, 1, 1)

        self.frame_9 = QFrame(self.tab_Delany_Bazley_Miki)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setMinimumSize(QSize(0, 48))
        self.frame_9.setMaximumSize(QSize(16777215, 48))
        self.frame_9.setFrameShape(QFrame.NoFrame)
        self.frame_9.setFrameShadow(QFrame.Raised)
        self.gridLayout_12 = QGridLayout(self.frame_9)
        self.gridLayout_12.setSpacing(6)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setContentsMargins(6, 6, 6, 6)
        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_12.addItem(self.horizontalSpacer_12, 0, 4, 1, 1)

        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_12.addItem(self.horizontalSpacer_13, 0, 0, 1, 1)

        self.label_45 = QLabel(self.frame_9)
        self.label_45.setObjectName(u"label_45")
        self.label_45.setFont(font1)

        self.gridLayout_12.addWidget(self.label_45, 0, 1, 1, 1)

        self.doubleSpinBox_flow_resistivity_DBM = QDoubleSpinBox(self.frame_9)
        self.doubleSpinBox_flow_resistivity_DBM.setObjectName(u"doubleSpinBox_flow_resistivity_DBM")
        self.doubleSpinBox_flow_resistivity_DBM.setMinimumSize(QSize(100, 28))
        self.doubleSpinBox_flow_resistivity_DBM.setMaximumSize(QSize(100, 28))
        self.doubleSpinBox_flow_resistivity_DBM.setAlignment(Qt.AlignCenter)
        self.doubleSpinBox_flow_resistivity_DBM.setDecimals(4)
        self.doubleSpinBox_flow_resistivity_DBM.setMaximum(100000.000000000000000)
        self.doubleSpinBox_flow_resistivity_DBM.setValue(1518.506599999999935)

        self.gridLayout_12.addWidget(self.doubleSpinBox_flow_resistivity_DBM, 0, 2, 1, 1)

        self.label_46 = QLabel(self.frame_9)
        self.label_46.setObjectName(u"label_46")
        self.label_46.setFont(font1)

        self.gridLayout_12.addWidget(self.label_46, 0, 3, 1, 1)


        self.gridLayout_17.addWidget(self.frame_9, 1, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_Delany_Bazley_Miki, "")
        self.tab_JCA = QWidget()
        self.tab_JCA.setObjectName(u"tab_JCA")
        self.gridLayout_11 = QGridLayout(self.tab_JCA)
        self.gridLayout_11.setSpacing(4)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setContentsMargins(4, 4, 4, 4)
        self.frame_7 = QFrame(self.tab_JCA)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.NoFrame)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.gridLayout_9 = QGridLayout(self.frame_7)
        self.gridLayout_9.setSpacing(6)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(6, 6, 6, 6)
        self.doubleSpinBox_tortuosity_JCA = QDoubleSpinBox(self.frame_7)
        self.doubleSpinBox_tortuosity_JCA.setObjectName(u"doubleSpinBox_tortuosity_JCA")
        self.doubleSpinBox_tortuosity_JCA.setMinimumSize(QSize(100, 28))
        self.doubleSpinBox_tortuosity_JCA.setMaximumSize(QSize(100, 28))
        self.doubleSpinBox_tortuosity_JCA.setAlignment(Qt.AlignCenter)
        self.doubleSpinBox_tortuosity_JCA.setDecimals(4)
        self.doubleSpinBox_tortuosity_JCA.setMinimum(0.000000000000000)
        self.doubleSpinBox_tortuosity_JCA.setMaximum(100.000000000000000)
        self.doubleSpinBox_tortuosity_JCA.setValue(1.000000000000000)

        self.gridLayout_9.addWidget(self.doubleSpinBox_tortuosity_JCA, 1, 2, 1, 1)

        self.label_30 = QLabel(self.frame_7)
        self.label_30.setObjectName(u"label_30")

        self.gridLayout_9.addWidget(self.label_30, 1, 3, 1, 1)

        self.label_34 = QLabel(self.frame_7)
        self.label_34.setObjectName(u"label_34")

        self.gridLayout_9.addWidget(self.label_34, 3, 3, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer_8, 0, 4, 1, 1)

        self.label_29 = QLabel(self.frame_7)
        self.label_29.setObjectName(u"label_29")

        self.gridLayout_9.addWidget(self.label_29, 0, 3, 1, 1)

        self.label_23 = QLabel(self.frame_7)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setMaximumSize(QSize(16777215, 28))
        self.label_23.setFont(font1)
        self.label_23.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_9.addWidget(self.label_23, 3, 1, 1, 1)

        self.label_14 = QLabel(self.frame_7)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setMaximumSize(QSize(16777215, 28))
        self.label_14.setFont(font1)
        self.label_14.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_9.addWidget(self.label_14, 0, 1, 1, 1)

        self.doubleSpinBox_flow_resistivity_JCA = QDoubleSpinBox(self.frame_7)
        self.doubleSpinBox_flow_resistivity_JCA.setObjectName(u"doubleSpinBox_flow_resistivity_JCA")
        self.doubleSpinBox_flow_resistivity_JCA.setMinimumSize(QSize(100, 28))
        self.doubleSpinBox_flow_resistivity_JCA.setMaximumSize(QSize(100, 28))
        self.doubleSpinBox_flow_resistivity_JCA.setAlignment(Qt.AlignCenter)
        self.doubleSpinBox_flow_resistivity_JCA.setDecimals(4)
        self.doubleSpinBox_flow_resistivity_JCA.setMaximum(100000.000000000000000)
        self.doubleSpinBox_flow_resistivity_JCA.setValue(1518.506599999999935)

        self.gridLayout_9.addWidget(self.doubleSpinBox_flow_resistivity_JCA, 5, 2, 1, 1)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer_9, 0, 5, 1, 1)

        self.label_22 = QLabel(self.frame_7)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setFont(font1)

        self.gridLayout_9.addWidget(self.label_22, 5, 3, 1, 1)

        self.label_13 = QLabel(self.frame_7)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setMaximumSize(QSize(16777215, 28))
        self.label_13.setFont(font1)
        self.label_13.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_9.addWidget(self.label_13, 1, 1, 1, 1)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer_10, 0, 0, 1, 1)

        self.doubleSpinBox_porosity_JCA = QDoubleSpinBox(self.frame_7)
        self.doubleSpinBox_porosity_JCA.setObjectName(u"doubleSpinBox_porosity_JCA")
        self.doubleSpinBox_porosity_JCA.setMinimumSize(QSize(100, 28))
        self.doubleSpinBox_porosity_JCA.setMaximumSize(QSize(100, 28))
        self.doubleSpinBox_porosity_JCA.setAlignment(Qt.AlignCenter)
        self.doubleSpinBox_porosity_JCA.setDecimals(4)
        self.doubleSpinBox_porosity_JCA.setMinimum(0.000000000000000)
        self.doubleSpinBox_porosity_JCA.setMaximum(1.000000000000000)
        self.doubleSpinBox_porosity_JCA.setSingleStep(0.100000000000000)
        self.doubleSpinBox_porosity_JCA.setValue(0.900000000000000)

        self.gridLayout_9.addWidget(self.doubleSpinBox_porosity_JCA, 0, 2, 1, 1)

        self.label_21 = QLabel(self.frame_7)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setFont(font1)
        self.label_21.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_9.addWidget(self.label_21, 5, 1, 1, 1)

        self.lineEdit_thermal_characteristic_length_JCA = QLineEdit(self.frame_7)
        self.lineEdit_thermal_characteristic_length_JCA.setObjectName(u"lineEdit_thermal_characteristic_length_JCA")
        self.lineEdit_thermal_characteristic_length_JCA.setMinimumSize(QSize(100, 28))
        self.lineEdit_thermal_characteristic_length_JCA.setMaximumSize(QSize(100, 28))
        self.lineEdit_thermal_characteristic_length_JCA.setAlignment(Qt.AlignCenter)

        self.gridLayout_9.addWidget(self.lineEdit_thermal_characteristic_length_JCA, 3, 2, 1, 1)

        self.label_24 = QLabel(self.frame_7)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setMaximumSize(QSize(16777215, 28))
        self.label_24.setFont(font1)
        self.label_24.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_9.addWidget(self.label_24, 2, 1, 1, 1)

        self.lineEdit_viscous_characteristic_length_JCA = QLineEdit(self.frame_7)
        self.lineEdit_viscous_characteristic_length_JCA.setObjectName(u"lineEdit_viscous_characteristic_length_JCA")
        self.lineEdit_viscous_characteristic_length_JCA.setMinimumSize(QSize(100, 28))
        self.lineEdit_viscous_characteristic_length_JCA.setMaximumSize(QSize(100, 28))
        self.lineEdit_viscous_characteristic_length_JCA.setAlignment(Qt.AlignCenter)

        self.gridLayout_9.addWidget(self.lineEdit_viscous_characteristic_length_JCA, 2, 2, 1, 1)

        self.label_33 = QLabel(self.frame_7)
        self.label_33.setObjectName(u"label_33")

        self.gridLayout_9.addWidget(self.label_33, 2, 3, 1, 1)


        self.gridLayout_11.addWidget(self.frame_7, 0, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_JCA, "")
        self.tab_JCAL = QWidget()
        self.tab_JCAL.setObjectName(u"tab_JCAL")
        self.gridLayout_14 = QGridLayout(self.tab_JCAL)
        self.gridLayout_14.setSpacing(4)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.gridLayout_14.setContentsMargins(4, 4, 4, 4)
        self.frame_10 = QFrame(self.tab_JCAL)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setFrameShape(QFrame.NoFrame)
        self.frame_10.setFrameShadow(QFrame.Raised)
        self.gridLayout_13 = QGridLayout(self.frame_10)
        self.gridLayout_13.setSpacing(6)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_13.setContentsMargins(6, 6, 6, 6)
        self.label_18 = QLabel(self.frame_10)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setMaximumSize(QSize(16777215, 28))
        self.label_18.setFont(font1)
        self.label_18.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_13.addWidget(self.label_18, 1, 1, 1, 1)

        self.label_38 = QLabel(self.frame_10)
        self.label_38.setObjectName(u"label_38")

        self.gridLayout_13.addWidget(self.label_38, 0, 3, 1, 1)

        self.label_37 = QLabel(self.frame_10)
        self.label_37.setObjectName(u"label_37")

        self.gridLayout_13.addWidget(self.label_37, 1, 3, 1, 1)

        self.label_35 = QLabel(self.frame_10)
        self.label_35.setObjectName(u"label_35")

        self.gridLayout_13.addWidget(self.label_35, 3, 3, 1, 1)

        self.doubleSpinBox_porosity_JCAL = QDoubleSpinBox(self.frame_10)
        self.doubleSpinBox_porosity_JCAL.setObjectName(u"doubleSpinBox_porosity_JCAL")
        self.doubleSpinBox_porosity_JCAL.setMinimumSize(QSize(100, 28))
        self.doubleSpinBox_porosity_JCAL.setMaximumSize(QSize(100, 28))
        self.doubleSpinBox_porosity_JCAL.setAlignment(Qt.AlignCenter)
        self.doubleSpinBox_porosity_JCAL.setDecimals(4)
        self.doubleSpinBox_porosity_JCAL.setMinimum(0.000000000000000)
        self.doubleSpinBox_porosity_JCAL.setMaximum(1.000000000000000)
        self.doubleSpinBox_porosity_JCAL.setSingleStep(0.100000000000000)
        self.doubleSpinBox_porosity_JCAL.setValue(0.900000000000000)

        self.gridLayout_13.addWidget(self.doubleSpinBox_porosity_JCAL, 0, 2, 1, 1)

        self.doubleSpinBox_tortuosity_JCAL = QDoubleSpinBox(self.frame_10)
        self.doubleSpinBox_tortuosity_JCAL.setObjectName(u"doubleSpinBox_tortuosity_JCAL")
        self.doubleSpinBox_tortuosity_JCAL.setMinimumSize(QSize(100, 28))
        self.doubleSpinBox_tortuosity_JCAL.setMaximumSize(QSize(100, 28))
        self.doubleSpinBox_tortuosity_JCAL.setAlignment(Qt.AlignCenter)
        self.doubleSpinBox_tortuosity_JCAL.setDecimals(4)
        self.doubleSpinBox_tortuosity_JCAL.setMinimum(0.000000000000000)
        self.doubleSpinBox_tortuosity_JCAL.setMaximum(100.000000000000000)
        self.doubleSpinBox_tortuosity_JCAL.setValue(1.000000000000000)

        self.gridLayout_13.addWidget(self.doubleSpinBox_tortuosity_JCAL, 1, 2, 1, 1)

        self.label_15 = QLabel(self.frame_10)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setMaximumSize(QSize(16777215, 28))
        self.label_15.setFont(font1)
        self.label_15.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_13.addWidget(self.label_15, 0, 1, 1, 1)

        self.label_27 = QLabel(self.frame_10)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setMaximumSize(QSize(16777215, 28))
        self.label_27.setFont(font1)
        self.label_27.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_13.addWidget(self.label_27, 3, 1, 1, 1)

        self.horizontalSpacer_17 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_13.addItem(self.horizontalSpacer_17, 0, 5, 1, 1)

        self.doubleSpinBox_flow_resistivity_JCAL = QDoubleSpinBox(self.frame_10)
        self.doubleSpinBox_flow_resistivity_JCAL.setObjectName(u"doubleSpinBox_flow_resistivity_JCAL")
        self.doubleSpinBox_flow_resistivity_JCAL.setMinimumSize(QSize(100, 28))
        self.doubleSpinBox_flow_resistivity_JCAL.setMaximumSize(QSize(100, 28))
        self.doubleSpinBox_flow_resistivity_JCAL.setAlignment(Qt.AlignCenter)
        self.doubleSpinBox_flow_resistivity_JCAL.setDecimals(4)
        self.doubleSpinBox_flow_resistivity_JCAL.setMaximum(100000.000000000000000)
        self.doubleSpinBox_flow_resistivity_JCAL.setValue(1518.506599999999935)

        self.gridLayout_13.addWidget(self.doubleSpinBox_flow_resistivity_JCAL, 5, 2, 1, 1)

        self.horizontalSpacer_16 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_13.addItem(self.horizontalSpacer_16, 0, 0, 1, 1)

        self.horizontalSpacer_15 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_13.addItem(self.horizontalSpacer_15, 0, 4, 1, 1)

        self.label_26 = QLabel(self.frame_10)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setFont(font1)

        self.gridLayout_13.addWidget(self.label_26, 5, 3, 1, 1)

        self.label_25 = QLabel(self.frame_10)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setFont(font1)
        self.label_25.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_13.addWidget(self.label_25, 5, 1, 1, 1)

        self.lineEdit_thermal_characteristic_length_JCAL = QLineEdit(self.frame_10)
        self.lineEdit_thermal_characteristic_length_JCAL.setObjectName(u"lineEdit_thermal_characteristic_length_JCAL")
        self.lineEdit_thermal_characteristic_length_JCAL.setMinimumSize(QSize(100, 28))
        self.lineEdit_thermal_characteristic_length_JCAL.setMaximumSize(QSize(100, 28))
        self.lineEdit_thermal_characteristic_length_JCAL.setAlignment(Qt.AlignCenter)

        self.gridLayout_13.addWidget(self.lineEdit_thermal_characteristic_length_JCAL, 3, 2, 1, 1)

        self.label_28 = QLabel(self.frame_10)
        self.label_28.setObjectName(u"label_28")
        self.label_28.setMaximumSize(QSize(16777215, 28))
        self.label_28.setFont(font1)
        self.label_28.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_13.addWidget(self.label_28, 2, 1, 1, 1)

        self.lineEdit_viscous_characteristic_length_JCAL = QLineEdit(self.frame_10)
        self.lineEdit_viscous_characteristic_length_JCAL.setObjectName(u"lineEdit_viscous_characteristic_length_JCAL")
        self.lineEdit_viscous_characteristic_length_JCAL.setMinimumSize(QSize(100, 28))
        self.lineEdit_viscous_characteristic_length_JCAL.setMaximumSize(QSize(100, 28))
        self.lineEdit_viscous_characteristic_length_JCAL.setAlignment(Qt.AlignCenter)

        self.gridLayout_13.addWidget(self.lineEdit_viscous_characteristic_length_JCAL, 2, 2, 1, 1)

        self.label_32 = QLabel(self.frame_10)
        self.label_32.setObjectName(u"label_32")

        self.gridLayout_13.addWidget(self.label_32, 2, 3, 1, 1)


        self.gridLayout_14.addWidget(self.frame_10, 0, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_JCAL, "")
        self.frame_11 = QWidget()
        self.frame_11.setObjectName(u"frame_11")
        self.gridLayout_21 = QGridLayout(self.frame_11)
        self.gridLayout_21.setObjectName(u"gridLayout_21")
        self.tabWidget_models = QTabWidget(self.frame_11)
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

        self.tabWidget_main.addTab(self.frame_11, "")
        self.tab_list = QWidget()
        self.tab_list.setObjectName(u"tab_list")
        self.gridLayout_16 = QGridLayout(self.tab_list)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.gridLayout_16.setContentsMargins(9, -1, -1, -1)
        self.frame_3 = QFrame(self.tab_list)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(320, 40))
        self.frame_3.setMaximumSize(QSize(16777215, 40))
        self.frame_3.setFrameShape(QFrame.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.gridLayout_15 = QGridLayout(self.frame_3)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.gridLayout_15.setHorizontalSpacing(12)
        self.gridLayout_15.setContentsMargins(4, 4, 4, 4)
        self.pushButton_reset = QPushButton(self.frame_3)
        self.pushButton_reset.setObjectName(u"pushButton_reset")
        self.pushButton_reset.setMinimumSize(QSize(100, 28))
        self.pushButton_reset.setMaximumSize(QSize(100, 28))
        font3 = QFont()
        font3.setFamilies([u"MS Shell Dlg 2"])
        font3.setPointSize(10)
        font3.setBold(False)
        font3.setItalic(False)
        self.pushButton_reset.setFont(font3)
        self.pushButton_reset.setStyleSheet(u"")

        self.gridLayout_15.addWidget(self.pushButton_reset, 0, 0, 1, 1)

        self.pushButton_remove = QPushButton(self.frame_3)
        self.pushButton_remove.setObjectName(u"pushButton_remove")
        self.pushButton_remove.setMinimumSize(QSize(100, 28))
        self.pushButton_remove.setMaximumSize(QSize(100, 28))
        self.pushButton_remove.setFont(font3)
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
        font4 = QFont()
        font4.setFamilies([u"MS Shell Dlg 2"])
        font4.setPointSize(10)
        font4.setItalic(False)
        self.treeWidget_porous_material_model.setFont(font4)
        self.treeWidget_porous_material_model.setIndentation(1)
        self.treeWidget_porous_material_model.setHeaderHidden(False)
        self.treeWidget_porous_material_model.header().setHighlightSections(False)
        self.treeWidget_porous_material_model.header().setProperty(u"showSortIndicator", False)
        self.treeWidget_porous_material_model.header().setStretchLastSection(True)

        self.gridLayout_16.addWidget(self.treeWidget_porous_material_model, 0, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_list, "")

        self.gridLayout_20.addWidget(self.tabWidget_main, 0, 0, 1, 1)

        self.frame_plot_setup = QFrame(self.scrollAreaWidgetContents)
        self.frame_plot_setup.setObjectName(u"frame_plot_setup")
        self.frame_plot_setup.setFrameShape(QFrame.NoFrame)
        self.frame_plot_setup.setFrameShadow(QFrame.Raised)
        self.gridLayout_18 = QGridLayout(self.frame_plot_setup)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.label_36 = QLabel(self.frame_plot_setup)
        self.label_36.setObjectName(u"label_36")
        self.label_36.setFont(font1)
        self.label_36.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_18.addWidget(self.label_36, 1, 1, 1, 1)

        self.lineEdit_fluid_density = QLineEdit(self.frame_plot_setup)
        self.lineEdit_fluid_density.setObjectName(u"lineEdit_fluid_density")
        self.lineEdit_fluid_density.setEnabled(False)
        self.lineEdit_fluid_density.setMinimumSize(QSize(100, 28))
        self.lineEdit_fluid_density.setMaximumSize(QSize(100, 28))
        self.lineEdit_fluid_density.setFont(font1)
        self.lineEdit_fluid_density.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_fluid_density.setAlignment(Qt.AlignCenter)

        self.gridLayout_18.addWidget(self.lineEdit_fluid_density, 1, 2, 1, 1)

        self.label_17 = QLabel(self.frame_plot_setup)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setFont(font1)
        self.label_17.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_18.addWidget(self.label_17, 3, 3, 1, 1)

        self.pushButton_get_fluid = QPushButton(self.frame_plot_setup)
        self.pushButton_get_fluid.setObjectName(u"pushButton_get_fluid")
        self.pushButton_get_fluid.setMinimumSize(QSize(72, 0))
        self.pushButton_get_fluid.setMaximumSize(QSize(72, 28))
        self.pushButton_get_fluid.setFont(font1)

        self.gridLayout_18.addWidget(self.pushButton_get_fluid, 0, 3, 1, 1)

        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_18.addItem(self.horizontalSpacer_14, 3, 0, 1, 1)

        self.horizontalSpacer_18 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_18.addItem(self.horizontalSpacer_18, 3, 4, 1, 1)

        self.doubleSpinBox_porous_material_depth = QDoubleSpinBox(self.frame_plot_setup)
        self.doubleSpinBox_porous_material_depth.setObjectName(u"doubleSpinBox_porous_material_depth")
        self.doubleSpinBox_porous_material_depth.setMinimumSize(QSize(100, 28))
        self.doubleSpinBox_porous_material_depth.setMaximumSize(QSize(100, 28))
        self.doubleSpinBox_porous_material_depth.setFont(font1)
        self.doubleSpinBox_porous_material_depth.setAlignment(Qt.AlignCenter)
        self.doubleSpinBox_porous_material_depth.setDecimals(4)
        self.doubleSpinBox_porous_material_depth.setMinimum(0.001000000000000)
        self.doubleSpinBox_porous_material_depth.setMaximum(100.000000000000000)
        self.doubleSpinBox_porous_material_depth.setSingleStep(0.050000000000000)
        self.doubleSpinBox_porous_material_depth.setValue(0.100000000000000)

        self.gridLayout_18.addWidget(self.doubleSpinBox_porous_material_depth, 3, 2, 1, 1)

        self.label_16 = QLabel(self.frame_plot_setup)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setFont(font1)
        self.label_16.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_18.addWidget(self.label_16, 3, 1, 1, 1)

        self.lineEdit_selected_fluid = QLineEdit(self.frame_plot_setup)
        self.lineEdit_selected_fluid.setObjectName(u"lineEdit_selected_fluid")
        self.lineEdit_selected_fluid.setEnabled(False)
        self.lineEdit_selected_fluid.setMinimumSize(QSize(100, 28))
        self.lineEdit_selected_fluid.setMaximumSize(QSize(100, 28))
        self.lineEdit_selected_fluid.setFont(font1)
        self.lineEdit_selected_fluid.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_selected_fluid.setAlignment(Qt.AlignCenter)

        self.gridLayout_18.addWidget(self.lineEdit_selected_fluid, 0, 2, 1, 1)

        self.label_31 = QLabel(self.frame_plot_setup)
        self.label_31.setObjectName(u"label_31")
        self.label_31.setFont(font1)
        self.label_31.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_18.addWidget(self.label_31, 0, 1, 1, 1)

        self.label_47 = QLabel(self.frame_plot_setup)
        self.label_47.setObjectName(u"label_47")
        self.label_47.setFont(font1)
        self.label_47.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_18.addWidget(self.label_47, 2, 1, 1, 1)

        self.lineEdit_speed_of_sound = QLineEdit(self.frame_plot_setup)
        self.lineEdit_speed_of_sound.setObjectName(u"lineEdit_speed_of_sound")
        self.lineEdit_speed_of_sound.setEnabled(False)
        self.lineEdit_speed_of_sound.setMinimumSize(QSize(100, 28))
        self.lineEdit_speed_of_sound.setMaximumSize(QSize(100, 28))
        self.lineEdit_speed_of_sound.setFont(font1)
        self.lineEdit_speed_of_sound.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_speed_of_sound.setAlignment(Qt.AlignCenter)

        self.gridLayout_18.addWidget(self.lineEdit_speed_of_sound, 2, 2, 1, 1)

        self.label_48 = QLabel(self.frame_plot_setup)
        self.label_48.setObjectName(u"label_48")
        self.label_48.setFont(font1)
        self.label_48.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_18.addWidget(self.label_48, 1, 3, 1, 1)

        self.label_49 = QLabel(self.frame_plot_setup)
        self.label_49.setObjectName(u"label_49")
        self.label_49.setFont(font1)
        self.label_49.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_18.addWidget(self.label_49, 2, 3, 1, 1)


        self.gridLayout_20.addWidget(self.frame_plot_setup, 2, 0, 1, 1)

        self.frame_plot_buttons = QFrame(self.scrollAreaWidgetContents)
        self.frame_plot_buttons.setObjectName(u"frame_plot_buttons")
        self.frame_plot_buttons.setMaximumSize(QSize(16777215, 48))
        self.frame_plot_buttons.setFrameShape(QFrame.NoFrame)
        self.frame_plot_buttons.setFrameShadow(QFrame.Raised)
        self.gridLayout_19 = QGridLayout(self.frame_plot_buttons)
        self.gridLayout_19.setObjectName(u"gridLayout_19")
        self.label_50 = QLabel(self.frame_plot_buttons)
        self.label_50.setObjectName(u"label_50")
        self.label_50.setMinimumSize(QSize(0, 28))
        self.label_50.setMaximumSize(QSize(16777215, 28))
        self.label_50.setFont(font1)
        self.label_50.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

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

        self.frame_2 = QFrame(self.scrollAreaWidgetContents)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)

        self.gridLayout_20.addWidget(self.frame_2, 1, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_3.addWidget(self.scrollArea, 1, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_main, 1, 0, 1, 1)

        self.frame_bottom = QFrame(Dialog)
        self.frame_bottom.setObjectName(u"frame_bottom")
        self.frame_bottom.setMinimumSize(QSize(0, 48))
        self.frame_bottom.setMaximumSize(QSize(16777215, 48))
        self.frame_bottom.setFrameShape(QFrame.NoFrame)
        self.frame_bottom.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_bottom)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.pushButton_confirm = QPushButton(self.frame_bottom)
        self.pushButton_confirm.setObjectName(u"pushButton_confirm")
        self.pushButton_confirm.setMinimumSize(QSize(100, 28))
        self.pushButton_confirm.setMaximumSize(QSize(100, 28))
        self.pushButton_confirm.setFont(font1)

        self.gridLayout_4.addWidget(self.pushButton_confirm, 0, 1, 1, 1)

        self.pushButton_exit = QPushButton(self.frame_bottom)
        self.pushButton_exit.setObjectName(u"pushButton_exit")
        self.pushButton_exit.setMinimumSize(QSize(100, 28))
        self.pushButton_exit.setMaximumSize(QSize(100, 28))
        self.pushButton_exit.setFont(font1)

        self.gridLayout_4.addWidget(self.pushButton_exit, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_bottom, 2, 0, 1, 1)

        QWidget.setTabOrder(self.doubleSpinBox_C1_DB, self.doubleSpinBox_C2_DB)
        QWidget.setTabOrder(self.doubleSpinBox_C2_DB, self.doubleSpinBox_C3_DB)
        QWidget.setTabOrder(self.doubleSpinBox_C3_DB, self.doubleSpinBox_C4_DB)
        QWidget.setTabOrder(self.doubleSpinBox_C4_DB, self.doubleSpinBox_C5_DB)
        QWidget.setTabOrder(self.doubleSpinBox_C5_DB, self.doubleSpinBox_C6_DB)
        QWidget.setTabOrder(self.doubleSpinBox_C6_DB, self.doubleSpinBox_C7_DB)
        QWidget.setTabOrder(self.doubleSpinBox_C7_DB, self.doubleSpinBox_C8_DB)
        QWidget.setTabOrder(self.doubleSpinBox_C8_DB, self.doubleSpinBox_flow_resistivity_DB)
        QWidget.setTabOrder(self.doubleSpinBox_flow_resistivity_DB, self.pushButton_get_fluid)
        QWidget.setTabOrder(self.pushButton_get_fluid, self.doubleSpinBox_porous_material_depth)
        QWidget.setTabOrder(self.doubleSpinBox_porous_material_depth, self.comboBox_plot_type)
        QWidget.setTabOrder(self.comboBox_plot_type, self.pushButton_plot_data)
        QWidget.setTabOrder(self.pushButton_plot_data, self.doubleSpinBox_C1_DBM)
        QWidget.setTabOrder(self.doubleSpinBox_C1_DBM, self.doubleSpinBox_C2_DBM)
        QWidget.setTabOrder(self.doubleSpinBox_C2_DBM, self.doubleSpinBox_C3_DBM)
        QWidget.setTabOrder(self.doubleSpinBox_C3_DBM, self.doubleSpinBox_C4_DBM)
        QWidget.setTabOrder(self.doubleSpinBox_C4_DBM, self.doubleSpinBox_C5_DBM)
        QWidget.setTabOrder(self.doubleSpinBox_C5_DBM, self.doubleSpinBox_C6_DBM)
        QWidget.setTabOrder(self.doubleSpinBox_C6_DBM, self.doubleSpinBox_C7_DBM)
        QWidget.setTabOrder(self.doubleSpinBox_C7_DBM, self.doubleSpinBox_C8_DBM)
        QWidget.setTabOrder(self.doubleSpinBox_C8_DBM, self.doubleSpinBox_flow_resistivity_DBM)
        QWidget.setTabOrder(self.doubleSpinBox_flow_resistivity_DBM, self.doubleSpinBox_porosity_JCA)
        QWidget.setTabOrder(self.doubleSpinBox_porosity_JCA, self.doubleSpinBox_tortuosity_JCA)
        QWidget.setTabOrder(self.doubleSpinBox_tortuosity_JCA, self.lineEdit_viscous_characteristic_length_JCA)
        QWidget.setTabOrder(self.lineEdit_viscous_characteristic_length_JCA, self.lineEdit_thermal_characteristic_length_JCA)
        QWidget.setTabOrder(self.lineEdit_thermal_characteristic_length_JCA, self.doubleSpinBox_flow_resistivity_JCA)
        QWidget.setTabOrder(self.doubleSpinBox_flow_resistivity_JCA, self.doubleSpinBox_porosity_JCAL)
        QWidget.setTabOrder(self.doubleSpinBox_porosity_JCAL, self.doubleSpinBox_tortuosity_JCAL)
        QWidget.setTabOrder(self.doubleSpinBox_tortuosity_JCAL, self.lineEdit_viscous_characteristic_length_JCAL)
        QWidget.setTabOrder(self.lineEdit_viscous_characteristic_length_JCAL, self.lineEdit_thermal_characteristic_length_JCAL)
        QWidget.setTabOrder(self.lineEdit_thermal_characteristic_length_JCAL, self.doubleSpinBox_flow_resistivity_JCAL)
        QWidget.setTabOrder(self.doubleSpinBox_flow_resistivity_JCAL, self.pushButton_confirm)
        QWidget.setTabOrder(self.pushButton_confirm, self.pushButton_exit)
        QWidget.setTabOrder(self.pushButton_exit, self.comboBox_attribution_type)
        QWidget.setTabOrder(self.comboBox_attribution_type, self.pushButton_DB_equations)
        QWidget.setTabOrder(self.pushButton_DB_equations, self.pushButton_DBM_equations)
        QWidget.setTabOrder(self.pushButton_DBM_equations, self.treeWidget_porous_material_model)
        QWidget.setTabOrder(self.treeWidget_porous_material_model, self.pushButton_reset)
        QWidget.setTabOrder(self.pushButton_reset, self.pushButton_remove)

        self.retranslateUi(Dialog)

        self.tabWidget_main.setCurrentIndex(0)
        self.tabWidget_models.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Vibra", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Set the porous material model", None))
        self.comboBox_attribution_type.setItemText(0, QCoreApplication.translate("Dialog", u" All bodies", None))
        self.comboBox_attribution_type.setItemText(1, QCoreApplication.translate("Dialog", u" Selected bodies", None))

        self.label_12.setText(QCoreApplication.translate("Dialog", u"Selected bodies:", None))
        self.lineEdit_selection_id.setText("")
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
        self.label_10.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Flow resistivity &sigma;:</p></body></html>", None))
        self.label_11.setText(QCoreApplication.translate("Dialog", u"[kg/m\u00b3.s]", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_Delany_Bazley), QCoreApplication.translate("Dialog", u"Delany-Bazley", None))
        self.label_39.setText(QCoreApplication.translate("Dialog", u"C5:", None))
        self.label_40.setText(QCoreApplication.translate("Dialog", u"C8:", None))
        self.label_41.setText(QCoreApplication.translate("Dialog", u"C4:", None))
        self.label_42.setText(QCoreApplication.translate("Dialog", u"C1:", None))
        self.label_43.setText(QCoreApplication.translate("Dialog", u"C3:", None))
        self.label_44.setText(QCoreApplication.translate("Dialog", u"C2:", None))
        self.label_19.setText(QCoreApplication.translate("Dialog", u"C7:", None))
        self.label_20.setText(QCoreApplication.translate("Dialog", u"C6:", None))
#if QT_CONFIG(tooltip)
        self.pushButton_DBM_equations.setToolTip(QCoreApplication.translate("Dialog", u"See the equations for Delany-Bazley-Miki porous material model.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_DBM_equations.setText("")
        self.label_45.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Flow resistivity \u03c3:</p></body></html>", None))
        self.label_46.setText(QCoreApplication.translate("Dialog", u"[kg/m\u00b3.s]", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_Delany_Bazley_Miki), QCoreApplication.translate("Dialog", u"Delany-Bazley-Miki", None))
        self.label_30.setText(QCoreApplication.translate("Dialog", u"[--]", None))
        self.label_34.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.label_29.setText(QCoreApplication.translate("Dialog", u"[--]", None))
        self.label_23.setText(QCoreApplication.translate("Dialog", u"Thermal characteristic length:", None))
        self.label_14.setText(QCoreApplication.translate("Dialog", u"Porosity:", None))
        self.label_22.setText(QCoreApplication.translate("Dialog", u"[kg/m\u00b3.s]", None))
        self.label_13.setText(QCoreApplication.translate("Dialog", u"Tortuosity:", None))
        self.label_21.setText(QCoreApplication.translate("Dialog", u"Flow resistivity:", None))
        self.lineEdit_thermal_characteristic_length_JCA.setText(QCoreApplication.translate("Dialog", u"159e-6", None))
        self.label_24.setText(QCoreApplication.translate("Dialog", u"Viscous characteristic length:", None))
        self.lineEdit_viscous_characteristic_length_JCA.setText(QCoreApplication.translate("Dialog", u"77e-6", None))
        self.label_33.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_JCA), QCoreApplication.translate("Dialog", u"JCA", None))
        self.label_18.setText(QCoreApplication.translate("Dialog", u"Tortuosity:", None))
        self.label_38.setText(QCoreApplication.translate("Dialog", u"[--]", None))
        self.label_37.setText(QCoreApplication.translate("Dialog", u"[--]", None))
        self.label_35.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.label_15.setText(QCoreApplication.translate("Dialog", u"Porosity:", None))
        self.label_27.setText(QCoreApplication.translate("Dialog", u"Thermal characteristic length:", None))
        self.label_26.setText(QCoreApplication.translate("Dialog", u"[kg/m\u00b3.s]", None))
        self.label_25.setText(QCoreApplication.translate("Dialog", u"Flow resistivity:", None))
        self.lineEdit_thermal_characteristic_length_JCAL.setText(QCoreApplication.translate("Dialog", u"159e-6", None))
        self.label_28.setText(QCoreApplication.translate("Dialog", u"Viscous characteristic length:", None))
        self.lineEdit_viscous_characteristic_length_JCAL.setText(QCoreApplication.translate("Dialog", u"77e-6", None))
        self.label_32.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_JCAL), QCoreApplication.translate("Dialog", u"JCAL", None))
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
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.frame_11), QCoreApplication.translate("Dialog", u"Edit", None))
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
        self.label_36.setText(QCoreApplication.translate("Dialog", u"Fluid density", None))
        self.lineEdit_fluid_density.setText("")
        self.label_17.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.pushButton_get_fluid.setText(QCoreApplication.translate("Dialog", u"Get fluid", None))
        self.label_16.setText(QCoreApplication.translate("Dialog", u"Porous material depth:", None))
        self.lineEdit_selected_fluid.setText("")
        self.label_31.setText(QCoreApplication.translate("Dialog", u"Selected the fluid:", None))
        self.label_47.setText(QCoreApplication.translate("Dialog", u"Speed of sound:", None))
        self.lineEdit_speed_of_sound.setText("")
        self.label_48.setText(QCoreApplication.translate("Dialog", u"[kg/m\u00b3]", None))
        self.label_49.setText(QCoreApplication.translate("Dialog", u"[m/s]", None))
        self.label_50.setText(QCoreApplication.translate("Dialog", u"Plot selector:", None))
        self.comboBox_plot_type.setItemText(0, QCoreApplication.translate("Dialog", u" Fluid density", None))
        self.comboBox_plot_type.setItemText(1, QCoreApplication.translate("Dialog", u" Speed of sound", None))
        self.comboBox_plot_type.setItemText(2, QCoreApplication.translate("Dialog", u" Surface impedance", None))
        self.comboBox_plot_type.setItemText(3, QCoreApplication.translate("Dialog", u" Absorption coefficient", None))

        self.pushButton_plot_data.setText(QCoreApplication.translate("Dialog", u"Plot data", None))
        self.pushButton_confirm.setText(QCoreApplication.translate("Dialog", u"Confirm", None))
        self.pushButton_exit.setText(QCoreApplication.translate("Dialog", u"Exit", None))
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
                            - frame_6: QFrame
                                - (Layout): QGridLayout
                                        - comboBox_attribution_type: QComboBox
                                        - label_12: QLabel
                                        - lineEdit_selection_id: QLineEdit
                            - scrollArea: QScrollArea
                                - scrollAreaWidgetContents: QWidget
                                    - (Layout): QGridLayout
                                            - tabWidget_main: QTabWidget
                                                - tab_Delany_Bazley: QWidget
                                                    - (Layout): QGridLayout
                                                            - frame_4: QFrame
                                                                - (Layout): QGridLayout
                                                                        - label_8: QLabel
                                                                        - label_7: QLabel
                                                                        - label_3: QLabel
                                                                        - doubleSpinBox_C4_DB: QDoubleSpinBox
                                                                        - label_6: QLabel
                                                                        - doubleSpinBox_C5_DB: QDoubleSpinBox
                                                                        - doubleSpinBox_C6_DB: QDoubleSpinBox
                                                                        - doubleSpinBox_C7_DB: QDoubleSpinBox
                                                                        - label_9: QLabel
                                                                        - doubleSpinBox_C8_DB: QDoubleSpinBox
                                                                        - label_5: QLabel
                                                                        - label_4: QLabel
                                                                        - doubleSpinBox_C3_DB: QDoubleSpinBox
                                                                        - label_2: QLabel
                                                                        - doubleSpinBox_C1_DB: QDoubleSpinBox
                                                                        - doubleSpinBox_C2_DB: QDoubleSpinBox
                                                                        - pushButton_DB_equations: QPushButton
                                                            - frame_5: QFrame
                                                                - (Layout): QGridLayout
                                                                        - label_10: QLabel
                                                                        - doubleSpinBox_flow_resistivity_DB: QDoubleSpinBox
                                                                        - label_11: QLabel
                                                - tab_Delany_Bazley_Miki: QWidget
                                                    - (Layout): QGridLayout
                                                            - frame_8: QFrame
                                                                - (Layout): QGridLayout
                                                                        - doubleSpinBox_C4_DBM: QDoubleSpinBox
                                                                        - doubleSpinBox_C5_DBM: QDoubleSpinBox
                                                                        - label_39: QLabel
                                                                        - doubleSpinBox_C7_DBM: QDoubleSpinBox
                                                                        - label_40: QLabel
                                                                        - doubleSpinBox_C8_DBM: QDoubleSpinBox
                                                                        - doubleSpinBox_C3_DBM: QDoubleSpinBox
                                                                        - label_41: QLabel
                                                                        - label_42: QLabel
                                                                        - label_43: QLabel
                                                                        - doubleSpinBox_C1_DBM: QDoubleSpinBox
                                                                        - doubleSpinBox_C2_DBM: QDoubleSpinBox
                                                                        - label_44: QLabel
                                                                        - label_19: QLabel
                                                                        - label_20: QLabel
                                                                        - doubleSpinBox_C6_DBM: QDoubleSpinBox
                                                                        - pushButton_DBM_equations: QPushButton
                                                            - frame_9: QFrame
                                                                - (Layout): QGridLayout
                                                                        - label_45: QLabel
                                                                        - doubleSpinBox_flow_resistivity_DBM: QDoubleSpinBox
                                                                        - label_46: QLabel
                                                - tab_JCA: QWidget
                                                    - (Layout): QGridLayout
                                                            - frame_7: QFrame
                                                                - (Layout): QGridLayout
                                                                        - doubleSpinBox_tortuosity_JCA: QDoubleSpinBox
                                                                        - label_30: QLabel
                                                                        - label_34: QLabel
                                                                        - label_29: QLabel
                                                                        - label_23: QLabel
                                                                        - label_14: QLabel
                                                                        - doubleSpinBox_flow_resistivity_JCA: QDoubleSpinBox
                                                                        - label_22: QLabel
                                                                        - label_13: QLabel
                                                                        - doubleSpinBox_porosity_JCA: QDoubleSpinBox
                                                                        - label_21: QLabel
                                                                        - lineEdit_thermal_characteristic_length_JCA: QLineEdit
                                                                        - label_24: QLabel
                                                                        - lineEdit_viscous_characteristic_length_JCA: QLineEdit
                                                                        - label_33: QLabel
                                                - tab_JCAL: QWidget
                                                    - (Layout): QGridLayout
                                                            - frame_10: QFrame
                                                                - (Layout): QGridLayout
                                                                        - label_18: QLabel
                                                                        - label_38: QLabel
                                                                        - label_37: QLabel
                                                                        - label_35: QLabel
                                                                        - doubleSpinBox_porosity_JCAL: QDoubleSpinBox
                                                                        - doubleSpinBox_tortuosity_JCAL: QDoubleSpinBox
                                                                        - label_15: QLabel
                                                                        - label_27: QLabel
                                                                        - doubleSpinBox_flow_resistivity_JCAL: QDoubleSpinBox
                                                                        - label_26: QLabel
                                                                        - label_25: QLabel
                                                                        - lineEdit_thermal_characteristic_length_JCAL: QLineEdit
                                                                        - label_28: QLabel
                                                                        - lineEdit_viscous_characteristic_length_JCAL: QLineEdit
                                                                        - label_32: QLabel
                                                - frame_11: QWidget
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
                                            - frame_plot_setup: QFrame
                                                - (Layout): QGridLayout
                                                        - label_36: QLabel
                                                        - lineEdit_fluid_density: QLineEdit
                                                        - label_17: QLabel
                                                        - pushButton_get_fluid: QPushButton
                                                        - doubleSpinBox_porous_material_depth: QDoubleSpinBox
                                                        - label_16: QLabel
                                                        - lineEdit_selected_fluid: QLineEdit
                                                        - label_31: QLabel
                                                        - label_47: QLabel
                                                        - lineEdit_speed_of_sound: QLineEdit
                                                        - label_48: QLabel
                                                        - label_49: QLabel
                                            - frame_plot_buttons: QFrame
                                                - (Layout): QGridLayout
                                                        - label_50: QLabel
                                                        - comboBox_plot_type: QComboBox
                                                        - pushButton_plot_data: QPushButton
                                            - frame_2: QFrame
                - frame_bottom: QFrame
                    - (Layout): QGridLayout
                            - pushButton_confirm: QPushButton
                            - pushButton_exit: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
