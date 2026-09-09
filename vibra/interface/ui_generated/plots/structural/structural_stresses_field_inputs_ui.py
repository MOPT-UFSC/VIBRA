# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'structural_stresses_field_inputs.ui'
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

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(364, 806)
        Form.setMaximumSize(QSize(16777215, 16777215))
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
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 343, 838))
        self.gridLayout_6 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setHorizontalSpacing(2)
        self.gridLayout_6.setVerticalSpacing(4)
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.frame_color = QFrame(self.scrollAreaWidgetContents)
        self.frame_color.setObjectName(u"frame_color")
        self.frame_color.setMinimumSize(QSize(0, 168))
        self.frame_color.setMaximumSize(QSize(16777215, 168))
        self.frame_color.setFrameShape(QFrame.Shape.Box)
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
        self.gridLayout.setContentsMargins(10, 0, -1, 0)
        self.label_title = QLabel(self.frame_title)
        self.label_title.setObjectName(u"label_title")
        self.label_title.setMinimumSize(QSize(0, 0))
        self.label_title.setMaximumSize(QSize(16777215, 32))
        font = QFont()
        font.setFamilies([u"MS Shell Dlg 2"])
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        self.label_title.setFont(font)
        self.label_title.setFrameShape(QFrame.Shape.NoFrame)
        self.label_title.setFrameShadow(QFrame.Shadow.Raised)
        self.label_title.setTextFormat(Qt.TextFormat.AutoText)
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_title, 0, 0, 1, 1)


        self.gridLayout_6.addWidget(self.frame_title, 0, 0, 1, 1)

        self.frame_main = QFrame(self.scrollAreaWidgetContents)
        self.frame_main.setObjectName(u"frame_main")
        self.frame_main.setMaximumSize(QSize(16777215, 460))
        self.frame_main.setSizeIncrement(QSize(0, 0))
        self.frame_main.setBaseSize(QSize(0, 0))
        self.frame_main.setFrameShape(QFrame.Shape.Box)
        self.frame_main.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_main)
        self.gridLayout_5.setSpacing(4)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(4, 4, 4, 4)
        self.frame_plot_type = QFrame(self.frame_main)
        self.frame_plot_type.setObjectName(u"frame_plot_type")
        self.frame_plot_type.setMinimumSize(QSize(0, 40))
        self.frame_plot_type.setMaximumSize(QSize(16777215, 16777215))
        self.frame_plot_type.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_plot_type.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_13 = QGridLayout(self.frame_plot_type)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_13.setContentsMargins(0, 6, 0, 6)
        self.label = QLabel(self.frame_plot_type)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(80, 26))
        self.label.setMaximumSize(QSize(80, 26))
        font1 = QFont()
        font1.setPointSize(10)
        self.label.setFont(font1)
        self.label.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_13.addWidget(self.label, 0, 1, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_13.addItem(self.horizontalSpacer_3, 0, 3, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_13.addItem(self.horizontalSpacer_4, 0, 0, 1, 1)

        self.comboBox_plot_type = QComboBox(self.frame_plot_type)
        self.comboBox_plot_type.addItem("")
        self.comboBox_plot_type.addItem("")
        self.comboBox_plot_type.addItem("")
        self.comboBox_plot_type.addItem("")
        self.comboBox_plot_type.addItem("")
        self.comboBox_plot_type.setObjectName(u"comboBox_plot_type")
        self.comboBox_plot_type.setMinimumSize(QSize(176, 26))
        self.comboBox_plot_type.setMaximumSize(QSize(200, 26))
        self.comboBox_plot_type.setFont(font1)

        self.gridLayout_13.addWidget(self.comboBox_plot_type, 0, 2, 1, 1)


        self.gridLayout_5.addWidget(self.frame_plot_type, 3, 0, 1, 1)

        self.frame_frequency = QFrame(self.frame_main)
        self.frame_frequency.setObjectName(u"frame_frequency")
        self.frame_frequency.setMinimumSize(QSize(0, 0))
        self.frame_frequency.setMaximumSize(QSize(16777215, 16777215))
        self.frame_frequency.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_frequency.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_frequency)
        self.gridLayout_4.setSpacing(6)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 6, 0, 6)
        self.lineEdit_selected_frequency = QLineEdit(self.frame_frequency)
        self.lineEdit_selected_frequency.setObjectName(u"lineEdit_selected_frequency")
        self.lineEdit_selected_frequency.setEnabled(False)
        self.lineEdit_selected_frequency.setMinimumSize(QSize(160, 28))
        self.lineEdit_selected_frequency.setMaximumSize(QSize(180, 28))
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        self.lineEdit_selected_frequency.setFont(font2)
        self.lineEdit_selected_frequency.setStyleSheet(u"")
        self.lineEdit_selected_frequency.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.lineEdit_selected_frequency, 1, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer, 1, 4, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_2, 1, 0, 1, 1)

        self.label_4 = QLabel(self.frame_frequency)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(0, 28))
        self.label_4.setMaximumSize(QSize(16777215, 28))
        font3 = QFont()
        font3.setFamilies([u"MS Shell Dlg 2"])
        font3.setPointSize(10)
        font3.setBold(False)
        self.label_4.setFont(font3)
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_4, 1, 1, 1, 1)

        self.label_5 = QLabel(self.frame_frequency)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(0, 28))
        self.label_5.setMaximumSize(QSize(16777215, 28))
        self.label_5.setFont(font3)
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.label_5, 1, 3, 1, 1)

        self.label_7 = QLabel(self.frame_frequency)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(0, 28))
        self.label_7.setMaximumSize(QSize(16777215, 28))
        self.label_7.setFont(font3)
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.label_7, 0, 1, 1, 1)

        self.comboBox_plotting_results = QComboBox(self.frame_frequency)
        self.comboBox_plotting_results.addItem("")
        self.comboBox_plotting_results.addItem("")
        self.comboBox_plotting_results.addItem("")
        self.comboBox_plotting_results.addItem("")
        self.comboBox_plotting_results.addItem("")
        self.comboBox_plotting_results.addItem("")
        self.comboBox_plotting_results.addItem("")
        self.comboBox_plotting_results.addItem("")
        self.comboBox_plotting_results.addItem("")
        self.comboBox_plotting_results.addItem("")
        self.comboBox_plotting_results.addItem("")
        self.comboBox_plotting_results.setObjectName(u"comboBox_plotting_results")
        self.comboBox_plotting_results.setMinimumSize(QSize(180, 28))
        self.comboBox_plotting_results.setMaximumSize(QSize(180, 28))
        self.comboBox_plotting_results.setSizeIncrement(QSize(0, 0))
        self.comboBox_plotting_results.setFont(font1)

        self.gridLayout_4.addWidget(self.comboBox_plotting_results, 0, 2, 1, 1)


        self.gridLayout_5.addWidget(self.frame_frequency, 1, 0, 1, 1)

        self.frame_tree_widget = QFrame(self.frame_main)
        self.frame_tree_widget.setObjectName(u"frame_tree_widget")
        self.frame_tree_widget.setMinimumSize(QSize(0, 200))
        self.frame_tree_widget.setMaximumSize(QSize(16777215, 250))
        self.frame_tree_widget.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_tree_widget.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_tree_widget)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.treeWidget_frequencies = QTreeWidget(self.frame_tree_widget)
        font4 = QFont()
        font4.setFamilies([u"MS Shell Dlg 2"])
        font4.setPointSize(10)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(1, u"Frequency [Hz]");
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem.setFont(1, font2);
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter);
        __qtreewidgetitem.setFont(0, font4);
        self.treeWidget_frequencies.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_frequencies.setObjectName(u"treeWidget_frequencies")
        self.treeWidget_frequencies.setMinimumSize(QSize(260, 160))
        self.treeWidget_frequencies.setMaximumSize(QSize(260, 240))
        self.treeWidget_frequencies.setFont(font2)
        self.treeWidget_frequencies.setAlternatingRowColors(True)
        self.treeWidget_frequencies.setIndentation(0)

        self.gridLayout_3.addWidget(self.treeWidget_frequencies, 0, 0, 1, 1)


        self.gridLayout_5.addWidget(self.frame_tree_widget, 2, 0, 1, 1)

        self.frame_3 = QFrame(self.frame_main)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(0, 52))
        self.frame_3.setMaximumSize(QSize(16777215, 52))
        self.frame_3.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_47 = QGridLayout(self.frame_3)
        self.gridLayout_47.setSpacing(2)
        self.gridLayout_47.setObjectName(u"gridLayout_47")
        self.gridLayout_47.setContentsMargins(2, 2, 2, 2)
        self.pushButton_plot_data = QPushButton(self.frame_3)
        self.pushButton_plot_data.setObjectName(u"pushButton_plot_data")
        self.pushButton_plot_data.setMinimumSize(QSize(160, 32))
        self.pushButton_plot_data.setMaximumSize(QSize(180, 32))
        self.pushButton_plot_data.setFont(font1)
        self.pushButton_plot_data.setStyleSheet(u"")
        self.pushButton_plot_data.setFlat(False)

        self.gridLayout_47.addWidget(self.pushButton_plot_data, 0, 0, 1, 1)


        self.gridLayout_5.addWidget(self.frame_3, 0, 0, 1, 1)


        self.gridLayout_6.addWidget(self.frame_main, 1, 0, 1, 1)

        self.frame_animation = QFrame(self.scrollAreaWidgetContents)
        self.frame_animation.setObjectName(u"frame_animation")
        self.frame_animation.setMinimumSize(QSize(0, 228))
        self.frame_animation.setFrameShape(QFrame.Shape.Box)
        self.frame_animation.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_6.addWidget(self.frame_animation, 2, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_2.addWidget(self.scrollArea, 0, 0, 1, 1)

        QWidget.setTabOrder(self.lineEdit_selected_frequency, self.treeWidget_frequencies)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Plot stress field", None))
        self.label_title.setText(QCoreApplication.translate("Form", u"Plot the stress field", None))
        self.label.setText(QCoreApplication.translate("Form", u"Plot type:", None))
        self.comboBox_plot_type.setItemText(0, QCoreApplication.translate("Form", u"Non-absolute (animation)", None))
        self.comboBox_plot_type.setItemText(1, QCoreApplication.translate("Form", u"Absolute (animation)", None))
        self.comboBox_plot_type.setItemText(2, QCoreApplication.translate("Form", u"Absolute values", None))
        self.comboBox_plot_type.setItemText(3, QCoreApplication.translate("Form", u"Real values", None))
        self.comboBox_plot_type.setItemText(4, QCoreApplication.translate("Form", u"Imag values", None))

        self.lineEdit_selected_frequency.setText("")
        self.label_4.setText(QCoreApplication.translate("Form", u"Frequency:", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"[Hz]", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"Plotting results:", None))
        self.comboBox_plotting_results.setItemText(0, QCoreApplication.translate("Form", u"Normal stress x", None))
        self.comboBox_plotting_results.setItemText(1, QCoreApplication.translate("Form", u"Normal stress y", None))
        self.comboBox_plotting_results.setItemText(2, QCoreApplication.translate("Form", u"Normal stress z", None))
        self.comboBox_plotting_results.setItemText(3, QCoreApplication.translate("Form", u"Shear stress xy", None))
        self.comboBox_plotting_results.setItemText(4, QCoreApplication.translate("Form", u"Shear stress xz", None))
        self.comboBox_plotting_results.setItemText(5, QCoreApplication.translate("Form", u"Shear stress yz", None))
        self.comboBox_plotting_results.setItemText(6, QCoreApplication.translate("Form", u"von Mises stress", None))
        self.comboBox_plotting_results.setItemText(7, QCoreApplication.translate("Form", u"Tresca stress", None))
        self.comboBox_plotting_results.setItemText(8, QCoreApplication.translate("Form", u"Max. principal stress 1", None))
        self.comboBox_plotting_results.setItemText(9, QCoreApplication.translate("Form", u"Max. principal stress 2", None))
        self.comboBox_plotting_results.setItemText(10, QCoreApplication.translate("Form", u"Max. principal stress 3", None))

        ___qtreewidgetitem = self.treeWidget_frequencies.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Form", u"Index", None));
#if QT_CONFIG(tooltip)
        self.treeWidget_frequencies.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Select a frequency to plot the strutural response field</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_plot_data.setText(QCoreApplication.translate("Form", u"Process nodal stresses", None))
    # retranslateUi



class StructuralStressesFieldInputs_UI(QWidget, Ui_Form):
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
                                - frame_main: QFrame
                                    - (Layout): QGridLayout
                                            - frame_plot_type: QFrame
                                                - (Layout): QGridLayout
                                                        - label: QLabel
                                                        - comboBox_plot_type: QComboBox
                                            - frame_frequency: QFrame
                                                - (Layout): QGridLayout
                                                        - lineEdit_selected_frequency: QLineEdit
                                                        - label_4: QLabel
                                                        - label_5: QLabel
                                                        - label_7: QLabel
                                                        - comboBox_plotting_results: QComboBox
                                            - frame_tree_widget: QFrame
                                                - (Layout): QGridLayout
                                                        - treeWidget_frequencies: QTreeWidget
                                            - frame_3: QFrame
                                                - (Layout): QGridLayout
                                                        - pushButton_plot_data: QPushButton
                                - frame_animation: QFrame
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
