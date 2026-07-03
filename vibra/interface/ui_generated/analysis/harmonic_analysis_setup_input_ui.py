# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'harmonic_analysis_setup_input.ui'
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
    QGridLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QTabWidget, QWidget)

from vibra.interface.formatters.icons import Icon

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setWindowModality(Qt.WindowModality.NonModal)
        Dialog.resize(420, 460)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(360, 460))
        Dialog.setMaximumSize(QSize(420, 16777215))
        Dialog.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        self.gridLayout_2 = QGridLayout(Dialog)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(4, 4, 4, 4)
        self.frame_title = QFrame(Dialog)
        self.frame_title.setObjectName(u"frame_title")
        self.frame_title.setMinimumSize(QSize(0, 48))
        self.frame_title.setMaximumSize(QSize(430, 48))
        self.frame_title.setFrameShape(QFrame.Shape.Box)
        self.frame_title.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_title.setLineWidth(1)
        self.gridLayout = QGridLayout(self.frame_title)
        self.gridLayout.setSpacing(2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(2, 2, 2, 2)
        self.label_title = QLabel(self.frame_title)
        self.label_title.setObjectName(u"label_title")
        font = QFont()
        font.setFamilies([u"MS Shell Dlg 2"])
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        self.label_title.setFont(font)
        self.label_title.setTextFormat(Qt.TextFormat.AutoText)
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_title, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.frame_title, 0, 0, 1, 1)

        self.frame_main = QFrame(Dialog)
        self.frame_main.setObjectName(u"frame_main")
        self.frame_main.setMinimumSize(QSize(0, 320))
        self.frame_main.setFrameShape(QFrame.Shape.Box)
        self.frame_main.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_9 = QGridLayout(self.frame_main)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setHorizontalSpacing(2)
        self.gridLayout_9.setVerticalSpacing(4)
        self.gridLayout_9.setContentsMargins(6, 6, 6, 4)
        self.frame_analysis_type = QFrame(self.frame_main)
        self.frame_analysis_type.setObjectName(u"frame_analysis_type")
        self.frame_analysis_type.setMinimumSize(QSize(0, 120))
        self.frame_analysis_type.setMaximumSize(QSize(1000, 140))
        self.frame_analysis_type.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_analysis_type.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_7 = QGridLayout(self.frame_analysis_type)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.pushButton_show_solution_steps_table = QPushButton(self.frame_analysis_type)
        self.pushButton_show_solution_steps_table.setObjectName(u"pushButton_show_solution_steps_table")
        self.pushButton_show_solution_steps_table.setMinimumSize(QSize(0, 0))
        self.pushButton_show_solution_steps_table.setMaximumSize(QSize(36, 28))
        font1 = QFont()
        font1.setPointSize(10)
        self.pushButton_show_solution_steps_table.setFont(font1)
        icon = Icon(u":/icons/preview_data.png")
        self.pushButton_show_solution_steps_table.setIcon(icon)
        self.pushButton_show_solution_steps_table.setIconSize(QSize(20, 20))
        self.pushButton_show_solution_steps_table.setAutoDefault(False)

        self.gridLayout_7.addWidget(self.pushButton_show_solution_steps_table, 1, 3, 1, 1)

        self.label_3 = QLabel(self.frame_analysis_type)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(120, 28))
        self.label_3.setMaximumSize(QSize(160, 28))
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        font2.setPointSize(10)
        font2.setBold(False)
        self.label_3.setFont(font2)
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_3, 0, 1, 1, 1)

        self.comboBox_method = QComboBox(self.frame_analysis_type)
        self.comboBox_method.addItem("")
        self.comboBox_method.addItem("")
        self.comboBox_method.setObjectName(u"comboBox_method")
        self.comboBox_method.setMinimumSize(QSize(160, 28))
        self.comboBox_method.setMaximumSize(QSize(160, 28))
        font3 = QFont()
        font3.setFamilies([u"MS Shell Dlg 2"])
        font3.setPointSize(10)
        font3.setBold(False)
        font3.setItalic(False)
        self.comboBox_method.setFont(font3)
        self.comboBox_method.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)

        self.gridLayout_7.addWidget(self.comboBox_method, 0, 2, 1, 1)

        self.label_modes_to_expand = QLabel(self.frame_analysis_type)
        self.label_modes_to_expand.setObjectName(u"label_modes_to_expand")
        self.label_modes_to_expand.setMinimumSize(QSize(120, 28))
        self.label_modes_to_expand.setMaximumSize(QSize(160, 28))
        self.label_modes_to_expand.setFont(font3)
        self.label_modes_to_expand.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_modes_to_expand, 2, 1, 1, 1)

        self.label_4 = QLabel(self.frame_analysis_type)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(120, 28))
        self.label_4.setMaximumSize(QSize(160, 28))
        self.label_4.setFont(font2)
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_4, 1, 1, 1, 1)

        self.comboBox_frequency_spacing = QComboBox(self.frame_analysis_type)
        self.comboBox_frequency_spacing.addItem("")
        self.comboBox_frequency_spacing.addItem("")
        self.comboBox_frequency_spacing.setObjectName(u"comboBox_frequency_spacing")
        self.comboBox_frequency_spacing.setMinimumSize(QSize(160, 28))
        self.comboBox_frequency_spacing.setMaximumSize(QSize(160, 28))
        self.comboBox_frequency_spacing.setFont(font3)
        self.comboBox_frequency_spacing.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)

        self.gridLayout_7.addWidget(self.comboBox_frequency_spacing, 1, 2, 1, 1)

        self.lineEdit_modes_to_expand = QLineEdit(self.frame_analysis_type)
        self.lineEdit_modes_to_expand.setObjectName(u"lineEdit_modes_to_expand")
        self.lineEdit_modes_to_expand.setMinimumSize(QSize(160, 28))
        self.lineEdit_modes_to_expand.setMaximumSize(QSize(160, 28))
        self.lineEdit_modes_to_expand.setFont(font3)
        self.lineEdit_modes_to_expand.setStyleSheet(u"")
        self.lineEdit_modes_to_expand.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_7.addWidget(self.lineEdit_modes_to_expand, 2, 2, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_8, 1, 4, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_7, 1, 0, 1, 1)


        self.gridLayout_9.addWidget(self.frame_analysis_type, 0, 0, 1, 1)

        self.tabWidget_main = QTabWidget(self.frame_main)
        self.tabWidget_main.setObjectName(u"tabWidget_main")
        self.tabWidget_main.setMinimumSize(QSize(0, 200))
        self.tabWidget_main.setMaximumSize(QSize(16777215, 400))
        self.tabWidget_main.setFont(font3)
        self.tab_setup = QWidget()
        self.tab_setup.setObjectName(u"tab_setup")
        self.gridLayout_5 = QGridLayout(self.tab_setup)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setHorizontalSpacing(8)
        self.gridLayout_5.setVerticalSpacing(6)
        self.gridLayout_5.setContentsMargins(4, 4, 4, 4)
        self.frame_solution_steps_setup = QFrame(self.tab_setup)
        self.frame_solution_steps_setup.setObjectName(u"frame_solution_steps_setup")
        self.frame_solution_steps_setup.setMaximumSize(QSize(16777215, 60))
        self.frame_solution_steps_setup.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_solution_steps_setup.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_10 = QGridLayout(self.frame_solution_steps_setup)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(4, 4, 4, 4)
        self.pushButton_solution_steps_configurator = QPushButton(self.frame_solution_steps_setup)
        self.pushButton_solution_steps_configurator.setObjectName(u"pushButton_solution_steps_configurator")
        self.pushButton_solution_steps_configurator.setMinimumSize(QSize(0, 32))
        self.pushButton_solution_steps_configurator.setMaximumSize(QSize(220, 32))
        self.pushButton_solution_steps_configurator.setFont(font3)
        self.pushButton_solution_steps_configurator.setStyleSheet(u"")
        icon1 = Icon(u":/icons/user_preferences_icon.png")
        self.pushButton_solution_steps_configurator.setIcon(icon1)
        self.pushButton_solution_steps_configurator.setIconSize(QSize(20, 20))
        self.pushButton_solution_steps_configurator.setAutoDefault(False)

        self.gridLayout_10.addWidget(self.pushButton_solution_steps_configurator, 0, 0, 1, 1)


        self.gridLayout_5.addWidget(self.frame_solution_steps_setup, 1, 0, 1, 2)

        self.frame_equally_distributed = QFrame(self.tab_setup)
        self.frame_equally_distributed.setObjectName(u"frame_equally_distributed")
        self.frame_equally_distributed.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_equally_distributed.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_8 = QGridLayout(self.frame_equally_distributed)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(4, 4, 4, 4)
        self.label_22 = QLabel(self.frame_equally_distributed)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setMinimumSize(QSize(80, 28))
        self.label_22.setMaximumSize(QSize(100, 28))
        font4 = QFont()
        font4.setFamilies([u"MS Shell Dlg 2"])
        font4.setPointSize(10)
        font4.setBold(False)
        font4.setItalic(False)
        font4.setKerning(False)
        self.label_22.setFont(font4)
        self.label_22.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_22, 0, 1, 1, 1)

        self.lineEdit_fstep = QLineEdit(self.frame_equally_distributed)
        self.lineEdit_fstep.setObjectName(u"lineEdit_fstep")
        self.lineEdit_fstep.setMinimumSize(QSize(170, 28))
        self.lineEdit_fstep.setMaximumSize(QSize(180, 28))
        self.lineEdit_fstep.setFont(font3)
        self.lineEdit_fstep.setStyleSheet(u"")
        self.lineEdit_fstep.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_8.addWidget(self.lineEdit_fstep, 2, 2, 1, 1)

        self.label_24 = QLabel(self.frame_equally_distributed)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setMinimumSize(QSize(0, 28))
        self.label_24.setMaximumSize(QSize(32, 28))
        self.label_24.setFont(font3)
        self.label_24.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_24, 0, 3, 1, 1)

        self.lineEdit_fmin = QLineEdit(self.frame_equally_distributed)
        self.lineEdit_fmin.setObjectName(u"lineEdit_fmin")
        self.lineEdit_fmin.setMinimumSize(QSize(170, 28))
        self.lineEdit_fmin.setMaximumSize(QSize(180, 28))
        self.lineEdit_fmin.setFont(font3)
        self.lineEdit_fmin.setStyleSheet(u"")
        self.lineEdit_fmin.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_8.addWidget(self.lineEdit_fmin, 0, 2, 1, 1)

        self.pushButton_reset_frequency_settings = QPushButton(self.frame_equally_distributed)
        self.pushButton_reset_frequency_settings.setObjectName(u"pushButton_reset_frequency_settings")
        self.pushButton_reset_frequency_settings.setMinimumSize(QSize(42, 28))
        icon2 = Icon(u":/icons/reset_settings.png")
        self.pushButton_reset_frequency_settings.setIcon(icon2)
        self.pushButton_reset_frequency_settings.setIconSize(QSize(22, 22))
        self.pushButton_reset_frequency_settings.setAutoDefault(False)

        self.gridLayout_8.addWidget(self.pushButton_reset_frequency_settings, 0, 4, 1, 1)

        self.label_fstep_unit_line_edit = QLabel(self.frame_equally_distributed)
        self.label_fstep_unit_line_edit.setObjectName(u"label_fstep_unit_line_edit")
        self.label_fstep_unit_line_edit.setMinimumSize(QSize(0, 28))
        self.label_fstep_unit_line_edit.setMaximumSize(QSize(32, 28))
        self.label_fstep_unit_line_edit.setFont(font3)
        self.label_fstep_unit_line_edit.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_fstep_unit_line_edit, 2, 3, 1, 1)

        self.label_25 = QLabel(self.frame_equally_distributed)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setMinimumSize(QSize(0, 28))
        self.label_25.setMaximumSize(QSize(32, 28))
        self.label_25.setFont(font3)
        self.label_25.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_25, 1, 3, 1, 1)

        self.lineEdit_fmax = QLineEdit(self.frame_equally_distributed)
        self.lineEdit_fmax.setObjectName(u"lineEdit_fmax")
        self.lineEdit_fmax.setMinimumSize(QSize(170, 28))
        self.lineEdit_fmax.setMaximumSize(QSize(180, 28))
        self.lineEdit_fmax.setFont(font3)
        self.lineEdit_fmax.setStyleSheet(u"")
        self.lineEdit_fmax.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_8.addWidget(self.lineEdit_fmax, 1, 2, 1, 1)

        self.label_23 = QLabel(self.frame_equally_distributed)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setMinimumSize(QSize(80, 28))
        self.label_23.setMaximumSize(QSize(100, 28))
        self.label_23.setFont(font4)
        self.label_23.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_23, 1, 1, 1, 1)

        self.label_fstep_line_edit = QLabel(self.frame_equally_distributed)
        self.label_fstep_line_edit.setObjectName(u"label_fstep_line_edit")
        self.label_fstep_line_edit.setMinimumSize(QSize(80, 28))
        self.label_fstep_line_edit.setMaximumSize(QSize(100, 28))
        self.label_fstep_line_edit.setFont(font4)
        self.label_fstep_line_edit.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_fstep_line_edit, 2, 1, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_3, 0, 0, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_4, 0, 5, 1, 1)

        self.label_fstep_combo_box = QLabel(self.frame_equally_distributed)
        self.label_fstep_combo_box.setObjectName(u"label_fstep_combo_box")
        self.label_fstep_combo_box.setMinimumSize(QSize(80, 28))
        self.label_fstep_combo_box.setMaximumSize(QSize(100, 28))
        self.label_fstep_combo_box.setFont(font4)
        self.label_fstep_combo_box.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_fstep_combo_box, 3, 1, 1, 1)

        self.label_fstep_unit_combo_box = QLabel(self.frame_equally_distributed)
        self.label_fstep_unit_combo_box.setObjectName(u"label_fstep_unit_combo_box")
        self.label_fstep_unit_combo_box.setMinimumSize(QSize(0, 28))
        self.label_fstep_unit_combo_box.setMaximumSize(QSize(32, 28))
        self.label_fstep_unit_combo_box.setFont(font3)
        self.label_fstep_unit_combo_box.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_fstep_unit_combo_box, 3, 3, 1, 1)

        self.comboBox_fstep = QComboBox(self.frame_equally_distributed)
        self.comboBox_fstep.setObjectName(u"comboBox_fstep")
        self.comboBox_fstep.setMinimumSize(QSize(0, 28))
        self.comboBox_fstep.setMaximumSize(QSize(16777215, 28))

        self.gridLayout_8.addWidget(self.comboBox_fstep, 3, 2, 1, 1)


        self.gridLayout_5.addWidget(self.frame_equally_distributed, 0, 0, 1, 2)

        self.tabWidget_main.addTab(self.tab_setup, "")
        self.tab_damping = QWidget()
        self.tab_damping.setObjectName(u"tab_damping")
        self.gridLayout_4 = QGridLayout(self.tab_damping)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(6, 4, 6, 4)
        self.frame_dampings = QFrame(self.tab_damping)
        self.frame_dampings.setObjectName(u"frame_dampings")
        self.frame_dampings.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_dampings.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_6 = QGridLayout(self.frame_dampings)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(4, 4, 4, 4)
        self.label_16 = QLabel(self.frame_dampings)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setMinimumSize(QSize(0, 26))
        self.label_16.setMaximumSize(QSize(16777215, 26))
        self.label_16.setFont(font3)
        self.label_16.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_6.addWidget(self.label_16, 2, 4, 1, 1)

        self.lineEdit_constant_structural_coefficient = QLineEdit(self.frame_dampings)
        self.lineEdit_constant_structural_coefficient.setObjectName(u"lineEdit_constant_structural_coefficient")
        self.lineEdit_constant_structural_coefficient.setMinimumSize(QSize(80, 26))
        self.lineEdit_constant_structural_coefficient.setMaximumSize(QSize(100, 26))
        self.lineEdit_constant_structural_coefficient.setFont(font3)
        self.lineEdit_constant_structural_coefficient.setStyleSheet(u"")
        self.lineEdit_constant_structural_coefficient.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_6.addWidget(self.lineEdit_constant_structural_coefficient, 2, 3, 1, 1)

        self.label_9 = QLabel(self.frame_dampings)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMinimumSize(QSize(132, 0))
        self.label_9.setFont(font3)
        self.label_9.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_9.setWordWrap(True)

        self.gridLayout_6.addWidget(self.label_9, 2, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer, 0, 5, 1, 1)

        self.lineEdit_stiffness_multiplier = QLineEdit(self.frame_dampings)
        self.lineEdit_stiffness_multiplier.setObjectName(u"lineEdit_stiffness_multiplier")
        self.lineEdit_stiffness_multiplier.setMinimumSize(QSize(80, 26))
        self.lineEdit_stiffness_multiplier.setMaximumSize(QSize(100, 26))
        self.lineEdit_stiffness_multiplier.setFont(font3)
        self.lineEdit_stiffness_multiplier.setStyleSheet(u"")
        self.lineEdit_stiffness_multiplier.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_6.addWidget(self.lineEdit_stiffness_multiplier, 1, 3, 1, 1)

        self.label_10 = QLabel(self.frame_dampings)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(132, 0))
        self.label_10.setFont(font3)
        self.label_10.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_10.setWordWrap(True)

        self.gridLayout_6.addWidget(self.label_10, 1, 1, 1, 1)

        self.label_11 = QLabel(self.frame_dampings)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMinimumSize(QSize(20, 26))
        self.label_11.setMaximumSize(QSize(40, 26))
        font5 = QFont()
        font5.setFamilies([u"Arial"])
        font5.setPointSize(11)
        font5.setBold(False)
        font5.setItalic(False)
        self.label_11.setFont(font5)
        self.label_11.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_11, 1, 2, 1, 1)

        self.label_14 = QLabel(self.frame_dampings)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setMinimumSize(QSize(0, 26))
        self.label_14.setMaximumSize(QSize(16777215, 26))
        self.label_14.setFont(font3)
        self.label_14.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_6.addWidget(self.label_14, 1, 4, 1, 1)

        self.lineEdit_mass_multiplier = QLineEdit(self.frame_dampings)
        self.lineEdit_mass_multiplier.setObjectName(u"lineEdit_mass_multiplier")
        self.lineEdit_mass_multiplier.setMinimumSize(QSize(80, 26))
        self.lineEdit_mass_multiplier.setMaximumSize(QSize(100, 26))
        self.lineEdit_mass_multiplier.setFont(font3)
        self.lineEdit_mass_multiplier.setStyleSheet(u"")
        self.lineEdit_mass_multiplier.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_6.addWidget(self.lineEdit_mass_multiplier, 0, 3, 1, 1)

        self.label_12 = QLabel(self.frame_dampings)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setMinimumSize(QSize(20, 26))
        self.label_12.setMaximumSize(QSize(40, 26))
        self.label_12.setFont(font5)
        self.label_12.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_12, 0, 2, 1, 1)

        self.label_17 = QLabel(self.frame_dampings)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setMinimumSize(QSize(132, 0))
        self.label_17.setFont(font3)
        self.label_17.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_17.setWordWrap(True)

        self.gridLayout_6.addWidget(self.label_17, 0, 1, 1, 1)

        self.label_15 = QLabel(self.frame_dampings)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setMinimumSize(QSize(0, 26))
        self.label_15.setMaximumSize(QSize(16777215, 26))
        self.label_15.setFont(font3)
        self.label_15.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_6.addWidget(self.label_15, 0, 4, 1, 1)

        self.label_13 = QLabel(self.frame_dampings)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setMinimumSize(QSize(20, 26))
        self.label_13.setMaximumSize(QSize(40, 26))
        self.label_13.setFont(font5)
        self.label_13.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_13, 2, 2, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_2, 0, 0, 1, 1)

        self.label_12.raise_()
        self.label_16.raise_()
        self.lineEdit_constant_structural_coefficient.raise_()
        self.label_9.raise_()
        self.lineEdit_stiffness_multiplier.raise_()
        self.label_10.raise_()
        self.label_11.raise_()
        self.label_14.raise_()
        self.lineEdit_mass_multiplier.raise_()
        self.label_17.raise_()
        self.label_15.raise_()
        self.label_13.raise_()

        self.gridLayout_4.addWidget(self.frame_dampings, 0, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_damping, "")

        self.gridLayout_9.addWidget(self.tabWidget_main, 1, 0, 1, 1)


        self.gridLayout_2.addWidget(self.frame_main, 1, 0, 1, 1)

        self.frame_buttons = QFrame(Dialog)
        self.frame_buttons.setObjectName(u"frame_buttons")
        self.frame_buttons.setMinimumSize(QSize(0, 48))
        self.frame_buttons.setMaximumSize(QSize(16777215, 48))
        self.frame_buttons.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_buttons.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_buttons)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setHorizontalSpacing(12)
        self.gridLayout_3.setVerticalSpacing(4)
        self.gridLayout_3.setContentsMargins(6, 4, 6, 4)
        self.pushButton_exit = QPushButton(self.frame_buttons)
        self.pushButton_exit.setObjectName(u"pushButton_exit")
        self.pushButton_exit.setMinimumSize(QSize(90, 30))
        self.pushButton_exit.setMaximumSize(QSize(90, 30))
        self.pushButton_exit.setFont(font3)
        self.pushButton_exit.setStyleSheet(u"")
        icon3 = Icon(u":/icons/exit_to_app_icon.png")
        self.pushButton_exit.setIcon(icon3)
        self.pushButton_exit.setIconSize(QSize(18, 18))
        self.pushButton_exit.setAutoDefault(False)

        self.gridLayout_3.addWidget(self.pushButton_exit, 0, 0, 1, 1)

        self.pushButton_enter_setup = QPushButton(self.frame_buttons)
        self.pushButton_enter_setup.setObjectName(u"pushButton_enter_setup")
        self.pushButton_enter_setup.setMinimumSize(QSize(120, 30))
        self.pushButton_enter_setup.setMaximumSize(QSize(120, 30))
        self.pushButton_enter_setup.setFont(font3)
        self.pushButton_enter_setup.setStyleSheet(u"")
        icon4 = Icon(u":/icons/settings_b_roll.png")
        self.pushButton_enter_setup.setIcon(icon4)
        self.pushButton_enter_setup.setIconSize(QSize(18, 18))
        self.pushButton_enter_setup.setAutoDefault(False)

        self.gridLayout_3.addWidget(self.pushButton_enter_setup, 0, 2, 1, 1)

        self.pushButton_run_analysis = QPushButton(self.frame_buttons)
        self.pushButton_run_analysis.setObjectName(u"pushButton_run_analysis")
        self.pushButton_run_analysis.setMinimumSize(QSize(120, 30))
        self.pushButton_run_analysis.setMaximumSize(QSize(120, 30))
        self.pushButton_run_analysis.setFont(font3)
        self.pushButton_run_analysis.setStyleSheet(u"")
        icon5 = Icon(u":/icons/start_solution.png")
        self.pushButton_run_analysis.setIcon(icon5)
        self.pushButton_run_analysis.setIconSize(QSize(18, 18))
        self.pushButton_run_analysis.setAutoDefault(False)

        self.gridLayout_3.addWidget(self.pushButton_run_analysis, 0, 3, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_5, 0, 1, 1, 1)


        self.gridLayout_2.addWidget(self.frame_buttons, 2, 0, 1, 1)

        QWidget.setTabOrder(self.comboBox_method, self.comboBox_frequency_spacing)
        QWidget.setTabOrder(self.comboBox_frequency_spacing, self.pushButton_show_solution_steps_table)
        QWidget.setTabOrder(self.pushButton_show_solution_steps_table, self.lineEdit_modes_to_expand)
        QWidget.setTabOrder(self.lineEdit_modes_to_expand, self.tabWidget_main)
        QWidget.setTabOrder(self.tabWidget_main, self.lineEdit_fmin)
        QWidget.setTabOrder(self.lineEdit_fmin, self.lineEdit_fmax)
        QWidget.setTabOrder(self.lineEdit_fmax, self.lineEdit_fstep)
        QWidget.setTabOrder(self.lineEdit_fstep, self.comboBox_fstep)
        QWidget.setTabOrder(self.comboBox_fstep, self.pushButton_solution_steps_configurator)
        QWidget.setTabOrder(self.pushButton_solution_steps_configurator, self.pushButton_reset_frequency_settings)
        QWidget.setTabOrder(self.pushButton_reset_frequency_settings, self.lineEdit_mass_multiplier)
        QWidget.setTabOrder(self.lineEdit_mass_multiplier, self.lineEdit_stiffness_multiplier)
        QWidget.setTabOrder(self.lineEdit_stiffness_multiplier, self.lineEdit_constant_structural_coefficient)
        QWidget.setTabOrder(self.lineEdit_constant_structural_coefficient, self.pushButton_enter_setup)
        QWidget.setTabOrder(self.pushButton_enter_setup, self.pushButton_run_analysis)
        QWidget.setTabOrder(self.pushButton_run_analysis, self.pushButton_exit)

        self.retranslateUi(Dialog)

        self.tabWidget_main.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Harmonic analysis setup", None))
#if QT_CONFIG(whatsthis)
        Dialog.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.label_title.setText(QCoreApplication.translate("Dialog", u"Harmonic analysis setup", None))
#if QT_CONFIG(tooltip)
        self.pushButton_show_solution_steps_table.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>See the solution steps table</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_show_solution_steps_table.setText("")
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Method:", None))
        self.comboBox_method.setItemText(0, QCoreApplication.translate("Dialog", u"Direct", None))
        self.comboBox_method.setItemText(1, QCoreApplication.translate("Dialog", u"Mode Superposition", None))

#if QT_CONFIG(tooltip)
        self.comboBox_method.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Select the analysis method</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_modes_to_expand.setText(QCoreApplication.translate("Dialog", u"Modes to expand:", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Frequency spacing:", None))
        self.comboBox_frequency_spacing.setItemText(0, QCoreApplication.translate("Dialog", u"Equally distributed", None))
        self.comboBox_frequency_spacing.setItemText(1, QCoreApplication.translate("Dialog", u"User-defined", None))

#if QT_CONFIG(tooltip)
        self.comboBox_frequency_spacing.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Define the frequency spacing type</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_solution_steps_configurator.setText(QCoreApplication.translate("Dialog", u"Solution steps configurator", None))
        self.label_22.setText(QCoreApplication.translate("Dialog", u"Freq. min:", None))
        self.label_24.setText(QCoreApplication.translate("Dialog", u"[Hz]", None))
#if QT_CONFIG(tooltip)
        self.pushButton_reset_frequency_settings.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Reset the frequency settings</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_reset_frequency_settings.setText("")
        self.label_fstep_unit_line_edit.setText(QCoreApplication.translate("Dialog", u"[Hz]", None))
        self.label_25.setText(QCoreApplication.translate("Dialog", u"[Hz]", None))
        self.label_23.setText(QCoreApplication.translate("Dialog", u"Freq. max:", None))
        self.label_fstep_line_edit.setText(QCoreApplication.translate("Dialog", u"Freq. step:", None))
        self.label_fstep_combo_box.setText(QCoreApplication.translate("Dialog", u"Freq. step:", None))
        self.label_fstep_unit_combo_box.setText(QCoreApplication.translate("Dialog", u"[Hz]", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_setup), QCoreApplication.translate("Dialog", u"Frequency setup", None))
        self.label_16.setText(QCoreApplication.translate("Dialog", u"[--]", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", u"Constant structural damping coefficient", None))
        self.label_10.setText(QCoreApplication.translate("Dialog", u"Stiffness matrix multiplier", None))
        self.label_11.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">\u03b2:</p></body></html>", None))
        self.label_14.setText(QCoreApplication.translate("Dialog", u"[s]", None))
        self.label_12.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">\u03b1:</p></body></html>", None))
        self.label_17.setText(QCoreApplication.translate("Dialog", u"Mass matrix multiplier", None))
        self.label_15.setText(QCoreApplication.translate("Dialog", u"[1/s]", None))
        self.label_13.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">\u03b7:</p></body></html>", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_damping), QCoreApplication.translate("Dialog", u"Damping setup", None))
        self.pushButton_exit.setText(QCoreApplication.translate("Dialog", u"Exit", None))
        self.pushButton_enter_setup.setText(QCoreApplication.translate("Dialog", u"Enter setup", None))
        self.pushButton_run_analysis.setText(QCoreApplication.translate("Dialog", u"Run analysis", None))
    # retranslateUi



class HarmonicAnalysisSetupInput_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame_title: QFrame
                    - (Layout): QGridLayout
                            - label_title: QLabel
                - frame_main: QFrame
                    - (Layout): QGridLayout
                            - frame_analysis_type: QFrame
                                - (Layout): QGridLayout
                                        - pushButton_show_solution_steps_table: QPushButton
                                        - label_3: QLabel
                                        - comboBox_method: QComboBox
                                        - label_modes_to_expand: QLabel
                                        - label_4: QLabel
                                        - comboBox_frequency_spacing: QComboBox
                                        - lineEdit_modes_to_expand: QLineEdit
                            - tabWidget_main: QTabWidget
                                - tab_setup: QWidget
                                    - (Layout): QGridLayout
                                            - frame_solution_steps_setup: QFrame
                                                - (Layout): QGridLayout
                                                        - pushButton_solution_steps_configurator: QPushButton
                                            - frame_equally_distributed: QFrame
                                                - (Layout): QGridLayout
                                                        - label_22: QLabel
                                                        - lineEdit_fstep: QLineEdit
                                                        - label_24: QLabel
                                                        - lineEdit_fmin: QLineEdit
                                                        - pushButton_reset_frequency_settings: QPushButton
                                                        - label_fstep_unit_line_edit: QLabel
                                                        - label_25: QLabel
                                                        - lineEdit_fmax: QLineEdit
                                                        - label_23: QLabel
                                                        - label_fstep_line_edit: QLabel
                                                        - label_fstep_combo_box: QLabel
                                                        - label_fstep_unit_combo_box: QLabel
                                                        - comboBox_fstep: QComboBox
                                - tab_damping: QWidget
                                    - (Layout): QGridLayout
                                            - frame_dampings: QFrame
                                                - (Layout): QGridLayout
                                                        - label_16: QLabel
                                                        - lineEdit_constant_structural_coefficient: QLineEdit
                                                        - label_9: QLabel
                                                        - lineEdit_stiffness_multiplier: QLineEdit
                                                        - label_10: QLabel
                                                        - label_11: QLabel
                                                        - label_14: QLabel
                                                        - lineEdit_mass_multiplier: QLineEdit
                                                        - label_12: QLabel
                                                        - label_17: QLabel
                                                        - label_15: QLabel
                                                        - label_13: QLabel
                - frame_buttons: QFrame
                    - (Layout): QGridLayout
                            - pushButton_exit: QPushButton
                            - pushButton_enter_setup: QPushButton
                            - pushButton_run_analysis: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
