# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'acoustic_mode_shape_inputs.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QHeaderView, QLabel, QLineEdit, QPushButton,
    QScrollArea, QSizePolicy, QSpacerItem, QTreeWidget,
    QTreeWidgetItem, QWidget)

from vibra.interface.formatters.icons import Icon

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(461, 726)
        self.gridLayout_2 = QGridLayout(Form)
        self.gridLayout_2.setSpacing(2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(2, 2, 2, 2)
        self.scrollArea = QScrollArea(Form)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 443, 820))
        self.gridLayout_6 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setHorizontalSpacing(2)
        self.gridLayout_6.setVerticalSpacing(4)
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.frame_color = QFrame(self.scrollAreaWidgetContents)
        self.frame_color.setObjectName(u"frame_color")
        self.frame_color.setMinimumSize(QSize(0, 228))
        self.frame_color.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_color.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_6.addWidget(self.frame_color, 3, 0, 1, 1)

        self.frame_title = QFrame(self.scrollAreaWidgetContents)
        self.frame_title.setObjectName(u"frame_title")
        self.frame_title.setMinimumSize(QSize(0, 40))
        self.frame_title.setMaximumSize(QSize(16777215, 40))
        self.frame_title.setFrameShape(QFrame.Shape.Box)
        self.frame_title.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_title.setLineWidth(1)
        self.gridLayout = QGridLayout(self.frame_title)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.label_title = QLabel(self.frame_title)
        self.label_title.setObjectName(u"label_title")
        self.label_title.setMinimumSize(QSize(0, 0))
        self.label_title.setMaximumSize(QSize(16777215, 16777215))
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        self.label_title.setFont(font)
        self.label_title.setFrameShape(QFrame.Shape.NoFrame)
        self.label_title.setFrameShadow(QFrame.Shadow.Raised)
        self.label_title.setTextFormat(Qt.TextFormat.AutoText)
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_title, 0, 0, 1, 1)


        self.gridLayout_6.addWidget(self.frame_title, 0, 0, 1, 1)

        self.frame_frequencies = QFrame(self.scrollAreaWidgetContents)
        self.frame_frequencies.setObjectName(u"frame_frequencies")
        self.frame_frequencies.setMaximumSize(QSize(16777215, 460))
        self.frame_frequencies.setSizeIncrement(QSize(0, 0))
        self.frame_frequencies.setBaseSize(QSize(0, 0))
        self.frame_frequencies.setFrameShape(QFrame.Shape.Box)
        self.frame_frequencies.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_frequencies)
        self.gridLayout_5.setSpacing(4)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(4, 4, 4, 4)
        self.frame_3 = QFrame(self.frame_frequencies)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(0, 40))
        self.frame_3.setMaximumSize(QSize(16777215, 40))
        self.frame_3.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_10 = QGridLayout(self.frame_3)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setHorizontalSpacing(6)
        self.gridLayout_10.setVerticalSpacing(0)
        self.gridLayout_10.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_10.addItem(self.horizontalSpacer_5, 0, 0, 1, 1)

        self.label_color_scalling = QLabel(self.frame_3)
        self.label_color_scalling.setObjectName(u"label_color_scalling")
        self.label_color_scalling.setMinimumSize(QSize(90, 26))
        self.label_color_scalling.setMaximumSize(QSize(90, 26))
        font1 = QFont()
        font1.setPointSize(10)
        self.label_color_scalling.setFont(font1)
        self.label_color_scalling.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_color_scalling, 0, 1, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_10.addItem(self.horizontalSpacer_8, 0, 3, 1, 1)

        self.comboBox_plot_type = QComboBox(self.frame_3)
        self.comboBox_plot_type.addItem("")
        self.comboBox_plot_type.addItem("")
        self.comboBox_plot_type.addItem("")
        self.comboBox_plot_type.addItem("")
        self.comboBox_plot_type.addItem("")
        self.comboBox_plot_type.setObjectName(u"comboBox_plot_type")
        self.comboBox_plot_type.setMinimumSize(QSize(176, 26))
        self.comboBox_plot_type.setMaximumSize(QSize(200, 26))
        self.comboBox_plot_type.setFont(font1)

        self.gridLayout_10.addWidget(self.comboBox_plot_type, 0, 2, 1, 1)


        self.gridLayout_5.addWidget(self.frame_3, 3, 0, 1, 1)

        self.frame_selector = QFrame(self.frame_frequencies)
        self.frame_selector.setObjectName(u"frame_selector")
        self.frame_selector.setMinimumSize(QSize(0, 40))
        self.frame_selector.setMaximumSize(QSize(16777215, 40))
        self.frame_selector.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_selector.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_selector)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setHorizontalSpacing(6)
        self.gridLayout_4.setVerticalSpacing(0)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label_4 = QLabel(self.frame_selector)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(0, 28))
        self.label_4.setMaximumSize(QSize(16777215, 28))
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        font2.setPointSize(10)
        font2.setBold(False)
        self.label_4.setFont(font2)
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.label_4, 0, 1, 1, 1)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_9, 0, 4, 1, 1)

        self.pushButton_export_results = QPushButton(self.frame_selector)
        self.pushButton_export_results.setObjectName(u"pushButton_export_results")
        self.pushButton_export_results.setMinimumSize(QSize(32, 28))
        self.pushButton_export_results.setMaximumSize(QSize(32, 16777215))
        icon = Icon(u":/icons/file_export_icon.png")
        self.pushButton_export_results.setIcon(icon)
        self.pushButton_export_results.setIconSize(QSize(18, 18))

        self.gridLayout_4.addWidget(self.pushButton_export_results, 0, 5, 1, 1)

        self.lineEdit_natural_frequency = QLineEdit(self.frame_selector)
        self.lineEdit_natural_frequency.setObjectName(u"lineEdit_natural_frequency")
        self.lineEdit_natural_frequency.setEnabled(False)
        self.lineEdit_natural_frequency.setMinimumSize(QSize(160, 28))
        self.lineEdit_natural_frequency.setMaximumSize(QSize(180, 28))
        font3 = QFont()
        font3.setFamilies([u"MS Shell Dlg 2"])
        font3.setPointSize(10)
        font3.setBold(False)
        font3.setItalic(False)
        self.lineEdit_natural_frequency.setFont(font3)
        self.lineEdit_natural_frequency.setStyleSheet(u"")
        self.lineEdit_natural_frequency.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.lineEdit_natural_frequency, 0, 2, 1, 1)

        self.label_5 = QLabel(self.frame_selector)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(0, 28))
        self.label_5.setMaximumSize(QSize(16777215, 28))
        self.label_5.setFont(font2)
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.label_5, 0, 3, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_3, 0, 0, 1, 1)


        self.gridLayout_5.addWidget(self.frame_selector, 0, 0, 1, 1)

        self.frame_treeWidget = QFrame(self.frame_frequencies)
        self.frame_treeWidget.setObjectName(u"frame_treeWidget")
        self.frame_treeWidget.setMaximumSize(QSize(16777215, 250))
        self.frame_treeWidget.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_treeWidget.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_treeWidget)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(4, 6, 4, 6)
        self.treeWidget_frequencies = QTreeWidget(self.frame_treeWidget)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.treeWidget_frequencies.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_frequencies.setObjectName(u"treeWidget_frequencies")
        self.treeWidget_frequencies.setMinimumSize(QSize(260, 200))
        self.treeWidget_frequencies.setMaximumSize(QSize(16777215, 240))
        self.treeWidget_frequencies.setFont(font3)
        self.treeWidget_frequencies.setAlternatingRowColors(True)
        self.treeWidget_frequencies.setIndentation(0)

        self.gridLayout_3.addWidget(self.treeWidget_frequencies, 0, 0, 1, 1)


        self.gridLayout_5.addWidget(self.frame_treeWidget, 1, 0, 1, 1)


        self.gridLayout_6.addWidget(self.frame_frequencies, 1, 0, 1, 1)

        self.frame_animation = QFrame(self.scrollAreaWidgetContents)
        self.frame_animation.setObjectName(u"frame_animation")
        self.frame_animation.setMinimumSize(QSize(0, 228))
        self.frame_animation.setFrameShape(QFrame.Shape.Box)
        self.frame_animation.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_6.addWidget(self.frame_animation, 2, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_2.addWidget(self.scrollArea, 0, 0, 1, 1)

        QWidget.setTabOrder(self.lineEdit_natural_frequency, self.treeWidget_frequencies)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Plot acoustic mode shape", None))
        self.label_title.setText(QCoreApplication.translate("Form", u"Plot the acoustic mode shape", None))
        self.label_color_scalling.setText(QCoreApplication.translate("Form", u"Plot type:", None))
        self.comboBox_plot_type.setItemText(0, QCoreApplication.translate("Form", u"Non-absolute (animation)", None))
        self.comboBox_plot_type.setItemText(1, QCoreApplication.translate("Form", u"Absolute (animation)", None))
        self.comboBox_plot_type.setItemText(2, QCoreApplication.translate("Form", u"Absolute values", None))
        self.comboBox_plot_type.setItemText(3, QCoreApplication.translate("Form", u"Real values", None))
        self.comboBox_plot_type.setItemText(4, QCoreApplication.translate("Form", u"Imag values", None))

        self.label_4.setText(QCoreApplication.translate("Form", u"Natural frequency:", None))
#if QT_CONFIG(tooltip)
        self.pushButton_export_results.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Export the modal analysis results</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_export_results.setText("")
        self.label_5.setText(QCoreApplication.translate("Form", u"[Hz]", None))
#if QT_CONFIG(tooltip)
        self.treeWidget_frequencies.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Select the mode shape to be plotted</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
    # retranslateUi



class AcousticModeShapeInputs_UI(QWidget, Ui_Form):
    """
    Component Hierarchy:
    - Form: QWidget
        - (Layout): QGridLayout
                - scrollArea: QScrollArea
                    - scrollAreaWidgetContents: QWidget
                        - (Layout): QGridLayout
                                - frame_color: QFrame
                                - frame_title: QFrame
                                    - (Layout): QGridLayout
                                            - label_title: QLabel
                                - frame_frequencies: QFrame
                                    - (Layout): QGridLayout
                                            - frame_3: QFrame
                                                - (Layout): QGridLayout
                                                        - label_color_scalling: QLabel
                                                        - comboBox_plot_type: QComboBox
                                            - frame_selector: QFrame
                                                - (Layout): QGridLayout
                                                        - label_4: QLabel
                                                        - pushButton_export_results: QPushButton
                                                        - lineEdit_natural_frequency: QLineEdit
                                                        - label_5: QLabel
                                            - frame_treeWidget: QFrame
                                                - (Layout): QGridLayout
                                                        - treeWidget_frequencies: QTreeWidget
                                - frame_animation: QFrame
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
