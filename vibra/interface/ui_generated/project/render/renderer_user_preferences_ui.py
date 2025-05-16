# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'renderer_user_preferences.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QFrame,
    QGridLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QSpinBox, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(488, 642)
        self.gridLayout_2 = QGridLayout(Dialog)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(4, 4, 4, 4)
        self.frame_background_color_2 = QFrame(Dialog)
        self.frame_background_color_2.setObjectName(u"frame_background_color_2")
        self.frame_background_color_2.setMinimumSize(QSize(320, 46))
        self.frame_background_color_2.setMaximumSize(QSize(16777215, 16777215))
        self.frame_background_color_2.setFrameShape(QFrame.Box)
        self.frame_background_color_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_20 = QGridLayout(self.frame_background_color_2)
        self.gridLayout_20.setObjectName(u"gridLayout_20")
        self.gridLayout_20.setHorizontalSpacing(8)
        self.gridLayout_20.setVerticalSpacing(5)
        self.gridLayout_20.setContentsMargins(4, 4, 4, 4)
        self.lineEdit_renderer_background_color_1 = QLineEdit(self.frame_background_color_2)
        self.lineEdit_renderer_background_color_1.setObjectName(u"lineEdit_renderer_background_color_1")
        self.lineEdit_renderer_background_color_1.setEnabled(False)
        self.lineEdit_renderer_background_color_1.setMinimumSize(QSize(90, 26))
        self.lineEdit_renderer_background_color_1.setMaximumSize(QSize(90, 26))
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(False)
        self.lineEdit_renderer_background_color_1.setFont(font)
        self.lineEdit_renderer_background_color_1.setFrame(True)
        self.lineEdit_renderer_background_color_1.setEchoMode(QLineEdit.Normal)

        self.gridLayout_20.addWidget(self.lineEdit_renderer_background_color_1, 1, 2, 1, 1)

        self.spinBox_nodes_size = QSpinBox(self.frame_background_color_2)
        self.spinBox_nodes_size.setObjectName(u"spinBox_nodes_size")
        self.spinBox_nodes_size.setMinimumSize(QSize(90, 26))
        font1 = QFont()
        font1.setPointSize(10)
        self.spinBox_nodes_size.setFont(font1)
        self.spinBox_nodes_size.setMinimum(1)
        self.spinBox_nodes_size.setValue(10)

        self.gridLayout_20.addWidget(self.spinBox_nodes_size, 13, 2, 1, 1)

        self.label_12 = QLabel(self.frame_background_color_2)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setMinimumSize(QSize(180, 30))
        self.label_12.setMaximumSize(QSize(180, 32))
        self.label_12.setFont(font1)
        self.label_12.setFrameShape(QFrame.NoFrame)
        self.label_12.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_20.addWidget(self.label_12, 4, 1, 1, 1)

        self.label_8 = QLabel(self.frame_background_color_2)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMinimumSize(QSize(180, 30))
        self.label_8.setMaximumSize(QSize(180, 32))
        self.label_8.setFont(font1)
        self.label_8.setFrameShape(QFrame.NoFrame)
        self.label_8.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_20.addWidget(self.label_8, 8, 1, 1, 1)

        self.label_10 = QLabel(self.frame_background_color_2)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(180, 30))
        self.label_10.setMaximumSize(QSize(180, 32))
        self.label_10.setFont(font1)
        self.label_10.setFrameShape(QFrame.NoFrame)
        self.label_10.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_20.addWidget(self.label_10, 1, 1, 1, 1)

        self.lineEdit_renderer_font_color = QLineEdit(self.frame_background_color_2)
        self.lineEdit_renderer_font_color.setObjectName(u"lineEdit_renderer_font_color")
        self.lineEdit_renderer_font_color.setEnabled(False)
        self.lineEdit_renderer_font_color.setMinimumSize(QSize(90, 26))
        self.lineEdit_renderer_font_color.setMaximumSize(QSize(90, 26))
        self.lineEdit_renderer_font_color.setFont(font)
        self.lineEdit_renderer_font_color.setFrame(True)
        self.lineEdit_renderer_font_color.setEchoMode(QLineEdit.Normal)

        self.gridLayout_20.addWidget(self.lineEdit_renderer_font_color, 4, 2, 1, 1)

        self.pushButton_renderer_background_color_2 = QPushButton(self.frame_background_color_2)
        self.pushButton_renderer_background_color_2.setObjectName(u"pushButton_renderer_background_color_2")
        self.pushButton_renderer_background_color_2.setMinimumSize(QSize(90, 25))
        self.pushButton_renderer_background_color_2.setMaximumSize(QSize(90, 25))
        self.pushButton_renderer_background_color_2.setFont(font1)
        self.pushButton_renderer_background_color_2.setAutoDefault(False)

        self.gridLayout_20.addWidget(self.pushButton_renderer_background_color_2, 2, 3, 1, 1)

        self.pushButton_selection_color = QPushButton(self.frame_background_color_2)
        self.pushButton_selection_color.setObjectName(u"pushButton_selection_color")
        self.pushButton_selection_color.setMinimumSize(QSize(90, 25))
        self.pushButton_selection_color.setMaximumSize(QSize(90, 25))
        font2 = QFont()
        font2.setFamilies([u"Arial"])
        font2.setPointSize(10)
        self.pushButton_selection_color.setFont(font2)
        self.pushButton_selection_color.setStyleSheet(u"")
        self.pushButton_selection_color.setAutoDefault(False)

        self.gridLayout_20.addWidget(self.pushButton_selection_color, 9, 3, 1, 1)

        self.label_6 = QLabel(self.frame_background_color_2)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(180, 30))
        self.label_6.setMaximumSize(QSize(180, 32))
        self.label_6.setFont(font1)
        self.label_6.setFrameShape(QFrame.NoFrame)
        self.label_6.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_20.addWidget(self.label_6, 5, 1, 1, 1)

        self.lineEdit_renderer_background_color_2 = QLineEdit(self.frame_background_color_2)
        self.lineEdit_renderer_background_color_2.setObjectName(u"lineEdit_renderer_background_color_2")
        self.lineEdit_renderer_background_color_2.setEnabled(False)
        self.lineEdit_renderer_background_color_2.setMinimumSize(QSize(90, 26))
        self.lineEdit_renderer_background_color_2.setMaximumSize(QSize(90, 26))
        font3 = QFont()
        font3.setFamilies([u"Arial"])
        font3.setPointSize(11)
        self.lineEdit_renderer_background_color_2.setFont(font3)
        self.lineEdit_renderer_background_color_2.setFrame(True)
        self.lineEdit_renderer_background_color_2.setEchoMode(QLineEdit.Normal)

        self.gridLayout_20.addWidget(self.lineEdit_renderer_background_color_2, 2, 2, 1, 1)

        self.label = QLabel(self.frame_background_color_2)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(180, 30))
        self.label.setMaximumSize(QSize(180, 32))
        self.label.setFont(font1)
        self.label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label.setWordWrap(False)

        self.gridLayout_20.addWidget(self.label, 2, 1, 1, 1)

        self.lineEdit_nodes_points_color = QLineEdit(self.frame_background_color_2)
        self.lineEdit_nodes_points_color.setObjectName(u"lineEdit_nodes_points_color")
        self.lineEdit_nodes_points_color.setEnabled(False)
        self.lineEdit_nodes_points_color.setMinimumSize(QSize(90, 26))
        self.lineEdit_nodes_points_color.setMaximumSize(QSize(90, 26))
        self.lineEdit_nodes_points_color.setFont(font)
        self.lineEdit_nodes_points_color.setFrame(True)
        self.lineEdit_nodes_points_color.setEchoMode(QLineEdit.Normal)

        self.gridLayout_20.addWidget(self.lineEdit_nodes_points_color, 5, 2, 1, 1)

        self.lineEdit_selection_color = QLineEdit(self.frame_background_color_2)
        self.lineEdit_selection_color.setObjectName(u"lineEdit_selection_color")
        self.lineEdit_selection_color.setEnabled(False)
        self.lineEdit_selection_color.setMinimumSize(QSize(90, 26))
        self.lineEdit_selection_color.setMaximumSize(QSize(90, 26))
        self.lineEdit_selection_color.setFont(font3)

        self.gridLayout_20.addWidget(self.lineEdit_selection_color, 9, 2, 1, 1)

        self.lineEdit_faces_color = QLineEdit(self.frame_background_color_2)
        self.lineEdit_faces_color.setObjectName(u"lineEdit_faces_color")
        self.lineEdit_faces_color.setEnabled(False)
        self.lineEdit_faces_color.setMinimumSize(QSize(90, 26))
        self.lineEdit_faces_color.setMaximumSize(QSize(90, 26))
        self.lineEdit_faces_color.setFont(font)
        self.lineEdit_faces_color.setFrame(True)
        self.lineEdit_faces_color.setEchoMode(QLineEdit.Normal)

        self.gridLayout_20.addWidget(self.lineEdit_faces_color, 8, 2, 1, 1)

        self.label_7 = QLabel(self.frame_background_color_2)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(180, 30))
        self.label_7.setMaximumSize(QSize(180, 32))
        self.label_7.setFont(font1)
        self.label_7.setFrameShape(QFrame.NoFrame)
        self.label_7.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_20.addWidget(self.label_7, 6, 1, 1, 1)

        self.label_17 = QLabel(self.frame_background_color_2)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setMinimumSize(QSize(180, 30))
        self.label_17.setMaximumSize(QSize(180, 32))
        self.label_17.setFont(font1)
        self.label_17.setFrameShape(QFrame.NoFrame)
        self.label_17.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_20.addWidget(self.label_17, 10, 1, 1, 1)

        self.label_20 = QLabel(self.frame_background_color_2)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setMinimumSize(QSize(180, 30))
        self.label_20.setMaximumSize(QSize(180, 32))
        self.label_20.setFont(font1)
        self.label_20.setFrameShape(QFrame.NoFrame)
        self.label_20.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_20.addWidget(self.label_20, 14, 1, 1, 1)

        self.pushButton_nodes_points_color = QPushButton(self.frame_background_color_2)
        self.pushButton_nodes_points_color.setObjectName(u"pushButton_nodes_points_color")
        self.pushButton_nodes_points_color.setMinimumSize(QSize(90, 25))
        self.pushButton_nodes_points_color.setMaximumSize(QSize(90, 25))
        self.pushButton_nodes_points_color.setFont(font1)
        self.pushButton_nodes_points_color.setStyleSheet(u"")
        self.pushButton_nodes_points_color.setAutoDefault(False)

        self.gridLayout_20.addWidget(self.pushButton_nodes_points_color, 5, 3, 1, 1)

        self.pushButton_renderer_font_color = QPushButton(self.frame_background_color_2)
        self.pushButton_renderer_font_color.setObjectName(u"pushButton_renderer_font_color")
        self.pushButton_renderer_font_color.setMinimumSize(QSize(90, 25))
        self.pushButton_renderer_font_color.setMaximumSize(QSize(90, 25))
        self.pushButton_renderer_font_color.setFont(font1)
        self.pushButton_renderer_font_color.setStyleSheet(u"")
        self.pushButton_renderer_font_color.setAutoDefault(False)

        self.gridLayout_20.addWidget(self.pushButton_renderer_font_color, 4, 3, 1, 1)

        self.pushButton_renderer_background_color_1 = QPushButton(self.frame_background_color_2)
        self.pushButton_renderer_background_color_1.setObjectName(u"pushButton_renderer_background_color_1")
        self.pushButton_renderer_background_color_1.setMinimumSize(QSize(90, 25))
        self.pushButton_renderer_background_color_1.setMaximumSize(QSize(90, 25))
        self.pushButton_renderer_background_color_1.setFont(font1)
        self.pushButton_renderer_background_color_1.setStyleSheet(u"")
        self.pushButton_renderer_background_color_1.setAutoDefault(False)

        self.gridLayout_20.addWidget(self.pushButton_renderer_background_color_1, 1, 3, 1, 1)

        self.pushButton_faces_color = QPushButton(self.frame_background_color_2)
        self.pushButton_faces_color.setObjectName(u"pushButton_faces_color")
        self.pushButton_faces_color.setMinimumSize(QSize(90, 25))
        self.pushButton_faces_color.setMaximumSize(QSize(90, 25))
        self.pushButton_faces_color.setFont(font2)
        self.pushButton_faces_color.setStyleSheet(u"")
        self.pushButton_faces_color.setAutoDefault(False)

        self.gridLayout_20.addWidget(self.pushButton_faces_color, 8, 3, 1, 1)

        self.label_19 = QLabel(self.frame_background_color_2)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setMinimumSize(QSize(180, 30))
        self.label_19.setMaximumSize(QSize(180, 32))
        self.label_19.setFont(font1)
        self.label_19.setFrameShape(QFrame.NoFrame)
        self.label_19.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_20.addWidget(self.label_19, 13, 1, 1, 1)

        self.spinBox_edges_thickness = QSpinBox(self.frame_background_color_2)
        self.spinBox_edges_thickness.setObjectName(u"spinBox_edges_thickness")
        self.spinBox_edges_thickness.setMinimumSize(QSize(90, 26))
        self.spinBox_edges_thickness.setFont(font1)
        self.spinBox_edges_thickness.setMinimum(1)
        self.spinBox_edges_thickness.setValue(1)

        self.gridLayout_20.addWidget(self.spinBox_edges_thickness, 15, 2, 1, 1)

        self.label_21 = QLabel(self.frame_background_color_2)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setMinimumSize(QSize(180, 30))
        self.label_21.setMaximumSize(QSize(180, 30))
        self.label_21.setFont(font1)
        self.label_21.setFrameShape(QFrame.NoFrame)
        self.label_21.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_20.addWidget(self.label_21, 15, 1, 1, 1)

        self.pushButton_lines_color = QPushButton(self.frame_background_color_2)
        self.pushButton_lines_color.setObjectName(u"pushButton_lines_color")
        self.pushButton_lines_color.setMinimumSize(QSize(90, 25))
        self.pushButton_lines_color.setMaximumSize(QSize(90, 25))
        self.pushButton_lines_color.setFont(font1)
        self.pushButton_lines_color.setStyleSheet(u"")
        self.pushButton_lines_color.setAutoDefault(False)

        self.gridLayout_20.addWidget(self.pushButton_lines_color, 6, 3, 1, 1)

        self.label_3 = QLabel(self.frame_background_color_2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font1)

        self.gridLayout_20.addWidget(self.label_3, 10, 3, 1, 1)

        self.lineEdit_edges_color = QLineEdit(self.frame_background_color_2)
        self.lineEdit_edges_color.setObjectName(u"lineEdit_edges_color")
        self.lineEdit_edges_color.setEnabled(False)
        self.lineEdit_edges_color.setMinimumSize(QSize(90, 26))
        self.lineEdit_edges_color.setMaximumSize(QSize(90, 26))
        self.lineEdit_edges_color.setFont(font)
        self.lineEdit_edges_color.setFrame(True)
        self.lineEdit_edges_color.setEchoMode(QLineEdit.Normal)

        self.gridLayout_20.addWidget(self.lineEdit_edges_color, 7, 2, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_20.addItem(self.horizontalSpacer_5, 1, 4, 1, 1)

        self.spinBox_points_size = QSpinBox(self.frame_background_color_2)
        self.spinBox_points_size.setObjectName(u"spinBox_points_size")
        self.spinBox_points_size.setMinimumSize(QSize(90, 26))
        self.spinBox_points_size.setFont(font1)
        self.spinBox_points_size.setMinimum(1)
        self.spinBox_points_size.setValue(15)

        self.gridLayout_20.addWidget(self.spinBox_points_size, 12, 2, 1, 1)

        self.label_2 = QLabel(self.frame_background_color_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(180, 30))
        self.label_2.setMaximumSize(QSize(180, 32))
        self.label_2.setFont(font1)
        self.label_2.setLayoutDirection(Qt.LeftToRight)
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_20.addWidget(self.label_2, 9, 1, 1, 1)

        self.spinBox_renderer_font_size = QSpinBox(self.frame_background_color_2)
        self.spinBox_renderer_font_size.setObjectName(u"spinBox_renderer_font_size")
        self.spinBox_renderer_font_size.setMinimumSize(QSize(90, 26))
        self.spinBox_renderer_font_size.setFont(font1)
        self.spinBox_renderer_font_size.setMinimum(1)
        self.spinBox_renderer_font_size.setMaximum(99)
        self.spinBox_renderer_font_size.setValue(12)

        self.gridLayout_20.addWidget(self.spinBox_renderer_font_size, 10, 2, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_20.addItem(self.verticalSpacer, 18, 2, 1, 1)

        self.pushButton_edges_color = QPushButton(self.frame_background_color_2)
        self.pushButton_edges_color.setObjectName(u"pushButton_edges_color")
        self.pushButton_edges_color.setMinimumSize(QSize(90, 25))
        self.pushButton_edges_color.setMaximumSize(QSize(90, 25))
        self.pushButton_edges_color.setFont(font1)
        self.pushButton_edges_color.setStyleSheet(u"")
        self.pushButton_edges_color.setAutoDefault(False)

        self.gridLayout_20.addWidget(self.pushButton_edges_color, 7, 3, 1, 1)

        self.spinBox_lines_thickness = QSpinBox(self.frame_background_color_2)
        self.spinBox_lines_thickness.setObjectName(u"spinBox_lines_thickness")
        self.spinBox_lines_thickness.setMinimumSize(QSize(90, 26))
        self.spinBox_lines_thickness.setFont(font1)
        self.spinBox_lines_thickness.setMinimum(1)
        self.spinBox_lines_thickness.setValue(5)

        self.gridLayout_20.addWidget(self.spinBox_lines_thickness, 14, 2, 1, 1)

        self.lineEdit_lines_color = QLineEdit(self.frame_background_color_2)
        self.lineEdit_lines_color.setObjectName(u"lineEdit_lines_color")
        self.lineEdit_lines_color.setEnabled(False)
        self.lineEdit_lines_color.setMinimumSize(QSize(90, 26))
        self.lineEdit_lines_color.setMaximumSize(QSize(90, 26))
        self.lineEdit_lines_color.setFont(font)
        self.lineEdit_lines_color.setFrame(True)
        self.lineEdit_lines_color.setEchoMode(QLineEdit.Normal)

        self.gridLayout_20.addWidget(self.lineEdit_lines_color, 6, 2, 1, 1)

        self.label_5 = QLabel(self.frame_background_color_2)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font1)

        self.gridLayout_20.addWidget(self.label_5, 12, 3, 1, 1)

        self.label_9 = QLabel(self.frame_background_color_2)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMinimumSize(QSize(180, 30))
        self.label_9.setMaximumSize(QSize(180, 32))
        self.label_9.setFont(font1)
        self.label_9.setFrameShape(QFrame.NoFrame)
        self.label_9.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_20.addWidget(self.label_9, 7, 1, 1, 1)

        self.label_22 = QLabel(self.frame_background_color_2)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setFont(font1)

        self.gridLayout_20.addWidget(self.label_22, 13, 3, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_20.addItem(self.horizontalSpacer_3, 1, 0, 1, 1)

        self.label_18 = QLabel(self.frame_background_color_2)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setMinimumSize(QSize(180, 30))
        self.label_18.setMaximumSize(QSize(180, 32))
        self.label_18.setFont(font1)
        self.label_18.setFrameShape(QFrame.NoFrame)
        self.label_18.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_20.addWidget(self.label_18, 12, 1, 1, 1)

        self.checkBox_reference_scale = QCheckBox(self.frame_background_color_2)
        self.checkBox_reference_scale.setObjectName(u"checkBox_reference_scale")
        font4 = QFont()
        font4.setFamilies([u"Segoe UI"])
        font4.setPointSize(8)
        font4.setBold(False)
        font4.setItalic(False)
        self.checkBox_reference_scale.setFont(font4)
        self.checkBox_reference_scale.setLayoutDirection(Qt.LeftToRight)
        self.checkBox_reference_scale.setChecked(True)

        self.gridLayout_20.addWidget(self.checkBox_reference_scale, 16, 2, 1, 1, Qt.AlignHCenter)

        self.checkBox_compatibility_mode = QCheckBox(self.frame_background_color_2)
        self.checkBox_compatibility_mode.setObjectName(u"checkBox_compatibility_mode")

        self.gridLayout_20.addWidget(self.checkBox_compatibility_mode, 17, 2, 1, 1, Qt.AlignHCenter|Qt.AlignVCenter)

        self.label_11 = QLabel(self.frame_background_color_2)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMinimumSize(QSize(180, 30))
        self.label_11.setMaximumSize(QSize(180, 32))
        self.label_11.setFont(font1)
        self.label_11.setFrameShape(QFrame.NoFrame)
        self.label_11.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_20.addWidget(self.label_11, 16, 1, 1, 1)

        self.label_23 = QLabel(self.frame_background_color_2)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setMinimumSize(QSize(180, 30))
        self.label_23.setMaximumSize(QSize(180, 32))
        self.label_23.setFont(font1)
        self.label_23.setFrameShape(QFrame.NoFrame)
        self.label_23.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_20.addWidget(self.label_23, 17, 1, 1, 1)


        self.gridLayout_2.addWidget(self.frame_background_color_2, 1, 0, 1, 1)

        self.frame_title = QFrame(Dialog)
        self.frame_title.setObjectName(u"frame_title")
        self.frame_title.setMinimumSize(QSize(0, 42))
        self.frame_title.setMaximumSize(QSize(600, 42))
        self.frame_title.setFrameShape(QFrame.NoFrame)
        self.frame_title.setLineWidth(1)
        self.gridLayout_10 = QGridLayout(self.frame_title)
        self.gridLayout_10.setSpacing(0)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(0, 0, 0, 0)
        self.label_title = QLabel(self.frame_title)
        self.label_title.setObjectName(u"label_title")
        self.label_title.setMinimumSize(QSize(0, 28))
        self.label_title.setMaximumSize(QSize(16777215, 16777215))
        font5 = QFont()
        font5.setPointSize(11)
        self.label_title.setFont(font5)
        self.label_title.setFrameShape(QFrame.Box)
        self.label_title.setFrameShadow(QFrame.Raised)
        self.label_title.setTextFormat(Qt.PlainText)
        self.label_title.setAlignment(Qt.AlignCenter)

        self.gridLayout_10.addWidget(self.label_title, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.frame_title, 0, 0, 1, 1)

        self.frame_buttons = QFrame(Dialog)
        self.frame_buttons.setObjectName(u"frame_buttons")
        self.frame_buttons.setMinimumSize(QSize(0, 48))
        self.frame_buttons.setMaximumSize(QSize(16777215, 48))
        self.frame_buttons.setFrameShape(QFrame.NoFrame)
        self.gridLayout = QGridLayout(self.frame_buttons)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.pushButton_apply_settings = QPushButton(self.frame_buttons)
        self.pushButton_apply_settings.setObjectName(u"pushButton_apply_settings")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_apply_settings.sizePolicy().hasHeightForWidth())
        self.pushButton_apply_settings.setSizePolicy(sizePolicy)
        self.pushButton_apply_settings.setMinimumSize(QSize(120, 30))
        self.pushButton_apply_settings.setMaximumSize(QSize(120, 30))
        self.pushButton_apply_settings.setFont(font1)
        self.pushButton_apply_settings.setAutoDefault(False)

        self.gridLayout.addWidget(self.pushButton_apply_settings, 0, 2, 1, 1)

        self.pushButton_update_settings = QPushButton(self.frame_buttons)
        self.pushButton_update_settings.setObjectName(u"pushButton_update_settings")
        self.pushButton_update_settings.setMinimumSize(QSize(120, 30))
        self.pushButton_update_settings.setMaximumSize(QSize(120, 30))
        self.pushButton_update_settings.setFont(font1)
        self.pushButton_update_settings.setStyleSheet(u"")
        self.pushButton_update_settings.setAutoDefault(False)

        self.gridLayout.addWidget(self.pushButton_update_settings, 0, 3, 1, 1)

        self.pushButton_reset_to_default = QPushButton(self.frame_buttons)
        self.pushButton_reset_to_default.setObjectName(u"pushButton_reset_to_default")
        self.pushButton_reset_to_default.setMinimumSize(QSize(120, 30))
        self.pushButton_reset_to_default.setMaximumSize(QSize(120, 30))
        self.pushButton_reset_to_default.setFont(font1)
        self.pushButton_reset_to_default.setStyleSheet(u"")
        self.pushButton_reset_to_default.setAutoDefault(False)

        self.gridLayout.addWidget(self.pushButton_reset_to_default, 0, 0, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.horizontalSpacer_4, 0, 1, 1, 1)


        self.gridLayout_2.addWidget(self.frame_buttons, 5, 0, 1, 1)

        QWidget.setTabOrder(self.lineEdit_renderer_background_color_1, self.pushButton_renderer_background_color_1)
        QWidget.setTabOrder(self.pushButton_renderer_background_color_1, self.lineEdit_renderer_font_color)
        QWidget.setTabOrder(self.lineEdit_renderer_font_color, self.pushButton_renderer_font_color)
        QWidget.setTabOrder(self.pushButton_renderer_font_color, self.lineEdit_nodes_points_color)
        QWidget.setTabOrder(self.lineEdit_nodes_points_color, self.pushButton_nodes_points_color)
        QWidget.setTabOrder(self.pushButton_nodes_points_color, self.lineEdit_lines_color)
        QWidget.setTabOrder(self.lineEdit_lines_color, self.pushButton_lines_color)
        QWidget.setTabOrder(self.pushButton_lines_color, self.lineEdit_faces_color)
        QWidget.setTabOrder(self.lineEdit_faces_color, self.pushButton_faces_color)
        QWidget.setTabOrder(self.pushButton_faces_color, self.pushButton_reset_to_default)
        QWidget.setTabOrder(self.pushButton_reset_to_default, self.pushButton_update_settings)

        self.retranslateUi(Dialog)

        self.pushButton_update_settings.setDefault(False)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Interface visibility settings", None))
        self.label_12.setText(QCoreApplication.translate("Dialog", u"Renderer font color:", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"Faces color:", None))
        self.label_10.setText(QCoreApplication.translate("Dialog", u"Renderer background color 1:", None))
        self.pushButton_renderer_background_color_2.setText(QCoreApplication.translate("Dialog", u"Pick color", None))
        self.pushButton_selection_color.setText(QCoreApplication.translate("Dialog", u"Pick color", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"Nodes / Points color:", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Renderer background color 2:", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"Lines color:", None))
        self.label_17.setText(QCoreApplication.translate("Dialog", u"Renderer font size:", None))
        self.label_20.setText(QCoreApplication.translate("Dialog", u"Lines thickness:", None))
        self.pushButton_nodes_points_color.setText(QCoreApplication.translate("Dialog", u"Pick color", None))
        self.pushButton_renderer_font_color.setText(QCoreApplication.translate("Dialog", u"Pick color", None))
        self.pushButton_renderer_background_color_1.setText(QCoreApplication.translate("Dialog", u"Pick color", None))
        self.pushButton_faces_color.setText(QCoreApplication.translate("Dialog", u"Pick color", None))
        self.label_19.setText(QCoreApplication.translate("Dialog", u"Nodes size:", None))
        self.label_21.setText(QCoreApplication.translate("Dialog", u"Edges thickness:", None))
        self.pushButton_lines_color.setText(QCoreApplication.translate("Dialog", u"Pick color", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"pt", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Selection color:", None))
        self.pushButton_edges_color.setText(QCoreApplication.translate("Dialog", u"Pick color", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"pt", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", u"Edges color:", None))
        self.label_22.setText(QCoreApplication.translate("Dialog", u"pt", None))
        self.label_18.setText(QCoreApplication.translate("Dialog", u"Points size:", None))
        self.checkBox_reference_scale.setText("")
        self.checkBox_compatibility_mode.setText("")
        self.label_11.setText(QCoreApplication.translate("Dialog", u"Show reference scale:", None))
#if QT_CONFIG(tooltip)
        self.label_23.setToolTip(QCoreApplication.translate("Dialog", u"If points are not showing in your renderers, try this option.", None))
#endif // QT_CONFIG(tooltip)
        self.label_23.setText(QCoreApplication.translate("Dialog", u"Compatibility mode:", None))
        self.label_title.setText(QCoreApplication.translate("Dialog", u"Interface visibility settings", None))
        self.pushButton_apply_settings.setText(QCoreApplication.translate("Dialog", u"Apply", None))
        self.pushButton_update_settings.setText(QCoreApplication.translate("Dialog", u"Ok", None))
        self.pushButton_reset_to_default.setText(QCoreApplication.translate("Dialog", u"Reset", None))
    # retranslateUi



class RendererUserPreferences_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame_background_color_2: QFrame
                    - (Layout): QGridLayout
                            - lineEdit_renderer_background_color_1: QLineEdit
                            - spinBox_nodes_size: QSpinBox
                            - label_12: QLabel
                            - label_8: QLabel
                            - label_10: QLabel
                            - lineEdit_renderer_font_color: QLineEdit
                            - pushButton_renderer_background_color_2: QPushButton
                            - pushButton_selection_color: QPushButton
                            - label_6: QLabel
                            - lineEdit_renderer_background_color_2: QLineEdit
                            - label: QLabel
                            - lineEdit_nodes_points_color: QLineEdit
                            - lineEdit_selection_color: QLineEdit
                            - lineEdit_faces_color: QLineEdit
                            - label_7: QLabel
                            - label_17: QLabel
                            - label_20: QLabel
                            - pushButton_nodes_points_color: QPushButton
                            - pushButton_renderer_font_color: QPushButton
                            - pushButton_renderer_background_color_1: QPushButton
                            - pushButton_faces_color: QPushButton
                            - label_19: QLabel
                            - spinBox_edges_thickness: QSpinBox
                            - label_21: QLabel
                            - pushButton_lines_color: QPushButton
                            - label_3: QLabel
                            - lineEdit_edges_color: QLineEdit
                            - spinBox_points_size: QSpinBox
                            - label_2: QLabel
                            - spinBox_renderer_font_size: QSpinBox
                            - pushButton_edges_color: QPushButton
                            - spinBox_lines_thickness: QSpinBox
                            - lineEdit_lines_color: QLineEdit
                            - label_5: QLabel
                            - label_9: QLabel
                            - label_22: QLabel
                            - label_18: QLabel
                            - checkBox_reference_scale: QCheckBox
                            - checkBox_compatibility_mode: QCheckBox
                            - label_11: QLabel
                            - label_23: QLabel
                - frame_title: QFrame
                    - (Layout): QGridLayout
                            - label_title: QLabel
                - frame_buttons: QFrame
                    - (Layout): QGridLayout
                            - pushButton_apply_settings: QPushButton
                            - pushButton_update_settings: QPushButton
                            - pushButton_reset_to_default: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
