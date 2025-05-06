# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'set_perforated_plate_model_inputs.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFrame,
    QGridLayout, QHeaderView, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QTabWidget,
    QTreeWidget, QTreeWidgetItem, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(476, 575)
        self.gridLayout = QGridLayout(Dialog)
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

        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(4, 4, 4, 4)
        self.frame_6 = QFrame(self.frame)
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
        self.lineEdit_selection_id.setStyleSheet(u"")
        self.lineEdit_selection_id.setAlignment(Qt.AlignCenter)

        self.gridLayout_8.addWidget(self.lineEdit_selection_id, 0, 2, 1, 1)


        self.gridLayout_3.addWidget(self.frame_6, 0, 0, 1, 1)

        self.frame_plot_buttons = QFrame(self.frame)
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
        self.comboBox_plot_type.setObjectName(u"comboBox_plot_type")
        self.comboBox_plot_type.setMinimumSize(QSize(160, 28))
        self.comboBox_plot_type.setMaximumSize(QSize(200, 28))
        self.comboBox_plot_type.setFont(font1)

        self.gridLayout_19.addWidget(self.comboBox_plot_type, 0, 2, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_19.addItem(self.horizontalSpacer_5, 0, 4, 1, 1)

        self.pushButton_plot_data = QPushButton(self.frame_plot_buttons)
        self.pushButton_plot_data.setObjectName(u"pushButton_plot_data")
        self.pushButton_plot_data.setMinimumSize(QSize(80, 28))
        self.pushButton_plot_data.setMaximumSize(QSize(220, 28))
        self.pushButton_plot_data.setFont(font1)

        self.gridLayout_19.addWidget(self.pushButton_plot_data, 0, 3, 1, 1)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_19.addItem(self.horizontalSpacer_9, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_plot_buttons, 3, 0, 1, 1)

        self.tabWidget_main = QTabWidget(self.frame)
        self.tabWidget_main.setObjectName(u"tabWidget_main")
        self.tabWidget_main.setMaximumSize(QSize(16777215, 16777215))
        self.tabWidget_main.setFont(font1)
        self.tab_setup = QWidget()
        self.tab_setup.setObjectName(u"tab_setup")
        self.gridLayout_5 = QGridLayout(self.tab_setup)
        self.gridLayout_5.setSpacing(4)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(4, 4, 4, 4)
        self.tabWidget_perforated_plate_models = QTabWidget(self.tab_setup)
        self.tabWidget_perforated_plate_models.setObjectName(u"tabWidget_perforated_plate_models")
        self.tabWidget_perforated_plate_models.setMinimumSize(QSize(0, 80))
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.gridLayout_6 = QGridLayout(self.tab)
        self.gridLayout_6.setSpacing(4)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(4, 4, 4, 4)
        self.frame_7 = QFrame(self.tab)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.NoFrame)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.gridLayout_9 = QGridLayout(self.frame_7)
        self.gridLayout_9.setSpacing(6)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(6, 6, 6, 6)
        self.label_21 = QLabel(self.frame_7)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setMinimumSize(QSize(40, 0))
        self.label_21.setMaximumSize(QSize(40, 16777215))
        self.label_21.setFont(font1)

        self.gridLayout_9.addWidget(self.label_21, 1, 4, 1, 1)

        self.label_19 = QLabel(self.frame_7)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setMinimumSize(QSize(40, 0))
        self.label_19.setMaximumSize(QSize(40, 16777215))
        self.label_19.setFont(font1)

        self.gridLayout_9.addWidget(self.label_19, 5, 4, 1, 1)

        self.label_7 = QLabel(self.frame_7)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(120, 0))
        self.label_7.setMaximumSize(QSize(132, 16777215))
        self.label_7.setFont(font1)
        self.label_7.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_9.addWidget(self.label_7, 5, 1, 1, 1)

        self.label_8 = QLabel(self.frame_7)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMinimumSize(QSize(120, 0))
        self.label_8.setMaximumSize(QSize(132, 16777215))
        self.label_8.setFont(font1)
        self.label_8.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_9.addWidget(self.label_8, 3, 1, 1, 1)

        self.lineEdit_porosity = QLineEdit(self.frame_7)
        self.lineEdit_porosity.setObjectName(u"lineEdit_porosity")
        self.lineEdit_porosity.setEnabled(True)
        self.lineEdit_porosity.setMinimumSize(QSize(120, 28))
        self.lineEdit_porosity.setMaximumSize(QSize(120, 28))
        self.lineEdit_porosity.setFont(font1)
        self.lineEdit_porosity.setAlignment(Qt.AlignCenter)
        self.lineEdit_porosity.setClearButtonEnabled(True)

        self.gridLayout_9.addWidget(self.lineEdit_porosity, 5, 3, 1, 1)

        self.label_20 = QLabel(self.frame_7)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setMinimumSize(QSize(40, 0))
        self.label_20.setMaximumSize(QSize(40, 16777215))
        self.label_20.setFont(font1)

        self.gridLayout_9.addWidget(self.label_20, 6, 4, 1, 1)

        self.lineEdit_discharge_coefficient = QLineEdit(self.frame_7)
        self.lineEdit_discharge_coefficient.setObjectName(u"lineEdit_discharge_coefficient")
        self.lineEdit_discharge_coefficient.setEnabled(True)
        self.lineEdit_discharge_coefficient.setMinimumSize(QSize(120, 28))
        self.lineEdit_discharge_coefficient.setMaximumSize(QSize(120, 28))
        self.lineEdit_discharge_coefficient.setFont(font1)
        self.lineEdit_discharge_coefficient.setAlignment(Qt.AlignCenter)
        self.lineEdit_discharge_coefficient.setClearButtonEnabled(True)

        self.gridLayout_9.addWidget(self.lineEdit_discharge_coefficient, 6, 3, 1, 1)

        self.label_10 = QLabel(self.frame_7)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(120, 0))
        self.label_10.setMaximumSize(QSize(132, 16777215))
        self.label_10.setFont(font1)
        self.label_10.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_9.addWidget(self.label_10, 6, 1, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer_8, 1, 0, 1, 1)

        self.label_22 = QLabel(self.frame_7)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setMinimumSize(QSize(40, 0))
        self.label_22.setMaximumSize(QSize(40, 16777215))
        self.label_22.setFont(font1)

        self.gridLayout_9.addWidget(self.label_22, 3, 4, 1, 1)

        self.label_13 = QLabel(self.frame_7)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setMinimumSize(QSize(120, 0))
        self.label_13.setMaximumSize(QSize(132, 16777215))
        self.label_13.setFont(font1)
        self.label_13.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_9.addWidget(self.label_13, 1, 1, 1, 1)

        self.label_9 = QLabel(self.frame_7)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMinimumSize(QSize(120, 0))
        self.label_9.setMaximumSize(QSize(132, 16777215))
        self.label_9.setFont(font1)
        self.label_9.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_9.addWidget(self.label_9, 0, 1, 1, 1)

        self.pushButton_circular_hole_equations = QPushButton(self.frame_7)
        self.pushButton_circular_hole_equations.setObjectName(u"pushButton_circular_hole_equations")
        self.pushButton_circular_hole_equations.setMinimumSize(QSize(120, 28))
        self.pushButton_circular_hole_equations.setMaximumSize(QSize(120, 28))
        self.pushButton_circular_hole_equations.setFont(font1)
        icon = QIcon()
        icon.addFile(u"../../../../icons/views/zoom_icon.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_circular_hole_equations.setIcon(icon)
        self.pushButton_circular_hole_equations.setIconSize(QSize(18, 18))

        self.gridLayout_9.addWidget(self.pushButton_circular_hole_equations, 0, 3, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer, 1, 5, 1, 1)

        self.lineEdit_plate_thickness = QLineEdit(self.frame_7)
        self.lineEdit_plate_thickness.setObjectName(u"lineEdit_plate_thickness")
        self.lineEdit_plate_thickness.setEnabled(True)
        self.lineEdit_plate_thickness.setMinimumSize(QSize(120, 28))
        self.lineEdit_plate_thickness.setMaximumSize(QSize(120, 28))
        self.lineEdit_plate_thickness.setFont(font1)
        self.lineEdit_plate_thickness.setAlignment(Qt.AlignCenter)
        self.lineEdit_plate_thickness.setClearButtonEnabled(True)

        self.gridLayout_9.addWidget(self.lineEdit_plate_thickness, 1, 3, 1, 1)

        self.lineEdit_hole_diameter = QLineEdit(self.frame_7)
        self.lineEdit_hole_diameter.setObjectName(u"lineEdit_hole_diameter")
        self.lineEdit_hole_diameter.setMinimumSize(QSize(120, 28))
        self.lineEdit_hole_diameter.setMaximumSize(QSize(120, 28))
        self.lineEdit_hole_diameter.setFont(font1)
        self.lineEdit_hole_diameter.setAlignment(Qt.AlignCenter)
        self.lineEdit_hole_diameter.setClearButtonEnabled(True)

        self.gridLayout_9.addWidget(self.lineEdit_hole_diameter, 3, 3, 1, 1)


        self.gridLayout_6.addWidget(self.frame_7, 0, 0, 1, 1)

        self.tabWidget_perforated_plate_models.addTab(self.tab, "")

        self.gridLayout_5.addWidget(self.tabWidget_perforated_plate_models, 0, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_setup, "")
        self.tab_list = QWidget()
        self.tab_list.setObjectName(u"tab_list")
        self.gridLayout_16 = QGridLayout(self.tab_list)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.gridLayout_16.setContentsMargins(9, -1, -1, -1)
        self.treeWidget_perforated_plate_model = QTreeWidget(self.tab_list)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(2, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter);
        self.treeWidget_perforated_plate_model.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_perforated_plate_model.setObjectName(u"treeWidget_perforated_plate_model")
        self.treeWidget_perforated_plate_model.setMinimumSize(QSize(320, 100))
        self.treeWidget_perforated_plate_model.setMaximumSize(QSize(16777215, 200))
        font3 = QFont()
        font3.setFamilies([u"MS Shell Dlg 2"])
        font3.setPointSize(10)
        font3.setItalic(False)
        self.treeWidget_perforated_plate_model.setFont(font3)
        self.treeWidget_perforated_plate_model.setIndentation(1)
        self.treeWidget_perforated_plate_model.setHeaderHidden(False)
        self.treeWidget_perforated_plate_model.header().setHighlightSections(False)
        self.treeWidget_perforated_plate_model.header().setProperty(u"showSortIndicator", False)
        self.treeWidget_perforated_plate_model.header().setStretchLastSection(True)

        self.gridLayout_16.addWidget(self.treeWidget_perforated_plate_model, 0, 0, 1, 1)

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
        font4 = QFont()
        font4.setFamilies([u"MS Shell Dlg 2"])
        font4.setPointSize(10)
        font4.setBold(False)
        font4.setItalic(False)
        self.pushButton_reset.setFont(font4)
        self.pushButton_reset.setStyleSheet(u"")

        self.gridLayout_15.addWidget(self.pushButton_reset, 0, 0, 1, 1)

        self.pushButton_remove = QPushButton(self.frame_3)
        self.pushButton_remove.setObjectName(u"pushButton_remove")
        self.pushButton_remove.setMinimumSize(QSize(100, 28))
        self.pushButton_remove.setMaximumSize(QSize(100, 28))
        self.pushButton_remove.setFont(font4)
        self.pushButton_remove.setStyleSheet(u"")

        self.gridLayout_15.addWidget(self.pushButton_remove, 0, 1, 1, 1)


        self.gridLayout_16.addWidget(self.frame_3, 1, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_list, "")

        self.gridLayout_3.addWidget(self.tabWidget_main, 1, 0, 1, 1)

        self.frame_fluid_info = QFrame(self.frame)
        self.frame_fluid_info.setObjectName(u"frame_fluid_info")
        self.frame_fluid_info.setMaximumSize(QSize(16777215, 160))
        self.frame_fluid_info.setFrameShape(QFrame.NoFrame)
        self.frame_fluid_info.setFrameShadow(QFrame.Raised)
        self.gridLayout_18 = QGridLayout(self.frame_fluid_info)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.gridLayout_18.setContentsMargins(6, 6, 6, 6)
        self.pushButton_get_fluid = QPushButton(self.frame_fluid_info)
        self.pushButton_get_fluid.setObjectName(u"pushButton_get_fluid")
        self.pushButton_get_fluid.setMinimumSize(QSize(72, 28))
        self.pushButton_get_fluid.setMaximumSize(QSize(72, 28))
        self.pushButton_get_fluid.setFont(font1)

        self.gridLayout_18.addWidget(self.pushButton_get_fluid, 0, 3, 1, 1)

        self.label_36 = QLabel(self.frame_fluid_info)
        self.label_36.setObjectName(u"label_36")
        self.label_36.setMinimumSize(QSize(0, 28))
        self.label_36.setMaximumSize(QSize(16777215, 28))
        self.label_36.setFont(font1)
        self.label_36.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_18.addWidget(self.label_36, 1, 1, 1, 1)

        self.lineEdit_fluid_density = QLineEdit(self.frame_fluid_info)
        self.lineEdit_fluid_density.setObjectName(u"lineEdit_fluid_density")
        self.lineEdit_fluid_density.setEnabled(False)
        self.lineEdit_fluid_density.setMinimumSize(QSize(100, 28))
        self.lineEdit_fluid_density.setMaximumSize(QSize(100, 28))
        self.lineEdit_fluid_density.setFont(font1)
        self.lineEdit_fluid_density.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_fluid_density.setStyleSheet(u"")
        self.lineEdit_fluid_density.setAlignment(Qt.AlignCenter)

        self.gridLayout_18.addWidget(self.lineEdit_fluid_density, 1, 2, 1, 1)

        self.label_31 = QLabel(self.frame_fluid_info)
        self.label_31.setObjectName(u"label_31")
        self.label_31.setMinimumSize(QSize(0, 28))
        self.label_31.setMaximumSize(QSize(16777215, 28))
        self.label_31.setFont(font1)
        self.label_31.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_18.addWidget(self.label_31, 0, 1, 1, 1)

        self.lineEdit_selected_fluid = QLineEdit(self.frame_fluid_info)
        self.lineEdit_selected_fluid.setObjectName(u"lineEdit_selected_fluid")
        self.lineEdit_selected_fluid.setEnabled(False)
        self.lineEdit_selected_fluid.setMinimumSize(QSize(100, 28))
        self.lineEdit_selected_fluid.setMaximumSize(QSize(100, 28))
        self.lineEdit_selected_fluid.setFont(font1)
        self.lineEdit_selected_fluid.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_selected_fluid.setStyleSheet(u"")
        self.lineEdit_selected_fluid.setAlignment(Qt.AlignCenter)

        self.gridLayout_18.addWidget(self.lineEdit_selected_fluid, 0, 2, 1, 1)

        self.lineEdit_speed_of_sound = QLineEdit(self.frame_fluid_info)
        self.lineEdit_speed_of_sound.setObjectName(u"lineEdit_speed_of_sound")
        self.lineEdit_speed_of_sound.setEnabled(False)
        self.lineEdit_speed_of_sound.setMinimumSize(QSize(100, 28))
        self.lineEdit_speed_of_sound.setMaximumSize(QSize(100, 28))
        self.lineEdit_speed_of_sound.setFont(font1)
        self.lineEdit_speed_of_sound.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_speed_of_sound.setStyleSheet(u"")
        self.lineEdit_speed_of_sound.setAlignment(Qt.AlignCenter)

        self.gridLayout_18.addWidget(self.lineEdit_speed_of_sound, 2, 2, 1, 1)

        self.label_47 = QLabel(self.frame_fluid_info)
        self.label_47.setObjectName(u"label_47")
        self.label_47.setMinimumSize(QSize(0, 28))
        self.label_47.setMaximumSize(QSize(16777215, 28))
        self.label_47.setFont(font1)
        self.label_47.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_18.addWidget(self.label_47, 2, 1, 1, 1)

        self.label_48 = QLabel(self.frame_fluid_info)
        self.label_48.setObjectName(u"label_48")
        self.label_48.setMinimumSize(QSize(0, 28))
        self.label_48.setMaximumSize(QSize(16777215, 28))
        self.label_48.setFont(font1)
        self.label_48.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_18.addWidget(self.label_48, 1, 3, 1, 1)

        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_18.addItem(self.horizontalSpacer_14, 0, 0, 1, 1)

        self.horizontalSpacer_18 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_18.addItem(self.horizontalSpacer_18, 0, 4, 1, 1)

        self.label_49 = QLabel(self.frame_fluid_info)
        self.label_49.setObjectName(u"label_49")
        self.label_49.setMinimumSize(QSize(0, 28))
        self.label_49.setMaximumSize(QSize(16777215, 28))
        self.label_49.setFont(font1)
        self.label_49.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_18.addWidget(self.label_49, 2, 3, 1, 1)


        self.gridLayout_3.addWidget(self.frame_fluid_info, 2, 0, 1, 1)


        self.gridLayout.addWidget(self.frame, 1, 0, 1, 1)

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


        self.retranslateUi(Dialog)

        self.comboBox_attribution_type.setCurrentIndex(1)
        self.tabWidget_main.setCurrentIndex(0)
        self.tabWidget_perforated_plate_models.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Perforated plate model setup", None))
        self.comboBox_attribution_type.setItemText(0, QCoreApplication.translate("Dialog", u"All faces", None))
        self.comboBox_attribution_type.setItemText(1, QCoreApplication.translate("Dialog", u"Selected faces", None))

        self.label_12.setText(QCoreApplication.translate("Dialog", u"Selected faces:", None))
        self.lineEdit_selection_id.setText("")
        self.label_50.setText(QCoreApplication.translate("Dialog", u"Plot selector:", None))
        self.comboBox_plot_type.setItemText(0, QCoreApplication.translate("Dialog", u"Acoustic impedance", None))

        self.pushButton_plot_data.setText(QCoreApplication.translate("Dialog", u"Plot data", None))
        self.label_21.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.label_19.setText(QCoreApplication.translate("Dialog", u"[--]", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"Porosity:", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"Hole diameter:", None))
        self.lineEdit_porosity.setText(QCoreApplication.translate("Dialog", u"0.23", None))
        self.label_20.setText(QCoreApplication.translate("Dialog", u"[--]", None))
        self.lineEdit_discharge_coefficient.setText(QCoreApplication.translate("Dialog", u"0.76", None))
        self.label_10.setText(QCoreApplication.translate("Dialog", u"Discharge coefficient:", None))
        self.label_22.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.label_13.setText(QCoreApplication.translate("Dialog", u"Plate thickness:", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", u"Formulation:", None))
#if QT_CONFIG(tooltip)
        self.pushButton_circular_hole_equations.setToolTip(QCoreApplication.translate("Dialog", u"See the equations for Delany-Bazley porous material model.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_circular_hole_equations.setText("")
        self.lineEdit_plate_thickness.setText(QCoreApplication.translate("Dialog", u"0.003", None))
        self.lineEdit_hole_diameter.setText(QCoreApplication.translate("Dialog", u"0.005", None))
        self.tabWidget_perforated_plate_models.setTabText(self.tabWidget_perforated_plate_models.indexOf(self.tab), QCoreApplication.translate("Dialog", u"Circular holes", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_setup), QCoreApplication.translate("Dialog", u"Setup", None))
        ___qtreewidgetitem = self.treeWidget_perforated_plate_model.headerItem()
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("Dialog", u"Parameters", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"Model", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Surfaces", None));
#if QT_CONFIG(tooltip)
        self.treeWidget_perforated_plate_model.setToolTip(QCoreApplication.translate("Dialog", u"Select a face to remove the previously attributed boundary condition.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_reset.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.pushButton_remove.setText(QCoreApplication.translate("Dialog", u"Remove", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_list), QCoreApplication.translate("Dialog", u"List", None))
        self.pushButton_get_fluid.setText(QCoreApplication.translate("Dialog", u"Get fluid", None))
        self.label_36.setText(QCoreApplication.translate("Dialog", u"Fluid density", None))
        self.lineEdit_fluid_density.setText("")
        self.label_31.setText(QCoreApplication.translate("Dialog", u"Selected fluid:", None))
        self.lineEdit_selected_fluid.setText("")
        self.lineEdit_speed_of_sound.setText("")
        self.label_47.setText(QCoreApplication.translate("Dialog", u"Speed of sound:", None))
        self.label_48.setText(QCoreApplication.translate("Dialog", u"[kg/m\u00b3]", None))
        self.label_49.setText(QCoreApplication.translate("Dialog", u"[m/s]", None))
        self.pushButton_confirm.setText(QCoreApplication.translate("Dialog", u"Confirm", None))
        self.pushButton_exit.setText(QCoreApplication.translate("Dialog", u"Exit", None))
    # retranslateUi



class SetPerforatedPlateModelInputs_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame_top: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
                - frame: QFrame
                    - (Layout): QGridLayout
                            - frame_6: QFrame
                                - (Layout): QGridLayout
                                        - comboBox_attribution_type: QComboBox
                                        - label_12: QLabel
                                        - lineEdit_selection_id: QLineEdit
                            - frame_plot_buttons: QFrame
                                - (Layout): QGridLayout
                                        - label_50: QLabel
                                        - comboBox_plot_type: QComboBox
                                        - pushButton_plot_data: QPushButton
                            - tabWidget_main: QTabWidget
                                - tab_setup: QWidget
                                    - (Layout): QGridLayout
                                            - tabWidget_perforated_plate_models: QTabWidget
                                                - tab: QWidget
                                                    - (Layout): QGridLayout
                                                            - frame_7: QFrame
                                                                - (Layout): QGridLayout
                                                                        - label_21: QLabel
                                                                        - label_19: QLabel
                                                                        - label_7: QLabel
                                                                        - label_8: QLabel
                                                                        - lineEdit_porosity: QLineEdit
                                                                        - label_20: QLabel
                                                                        - lineEdit_discharge_coefficient: QLineEdit
                                                                        - label_10: QLabel
                                                                        - label_22: QLabel
                                                                        - label_13: QLabel
                                                                        - label_9: QLabel
                                                                        - pushButton_circular_hole_equations: QPushButton
                                                                        - lineEdit_plate_thickness: QLineEdit
                                                                        - lineEdit_hole_diameter: QLineEdit
                                - tab_list: QWidget
                                    - (Layout): QGridLayout
                                            - treeWidget_perforated_plate_model: QTreeWidget
                                            - frame_3: QFrame
                                                - (Layout): QGridLayout
                                                        - pushButton_reset: QPushButton
                                                        - pushButton_remove: QPushButton
                            - frame_fluid_info: QFrame
                                - (Layout): QGridLayout
                                        - pushButton_get_fluid: QPushButton
                                        - label_36: QLabel
                                        - lineEdit_fluid_density: QLineEdit
                                        - label_31: QLabel
                                        - lineEdit_selected_fluid: QLineEdit
                                        - lineEdit_speed_of_sound: QLineEdit
                                        - label_47: QLabel
                                        - label_48: QLabel
                                        - label_49: QLabel
                - frame_bottom: QFrame
                    - (Layout): QGridLayout
                            - pushButton_confirm: QPushButton
                            - pushButton_exit: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
