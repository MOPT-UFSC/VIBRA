# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'material_widget.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHeaderView,
    QPushButton, QSizePolicy, QSpacerItem, QTableWidget,
    QTableWidgetItem, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(720, 370)
        self.gridLayout_4 = QGridLayout(Form)
        self.gridLayout_4.setSpacing(4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(4, 4, 4, 4)
        self.frame_2 = QFrame(Form)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setHorizontalSpacing(4)
        self.gridLayout_2.setVerticalSpacing(6)
        self.gridLayout_2.setContentsMargins(4, 4, 4, 4)
        self.tableWidget_material_data = QTableWidget(self.frame_2)
        if (self.tableWidget_material_data.rowCount() < 7):
            self.tableWidget_material_data.setRowCount(7)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_material_data.setVerticalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_material_data.setVerticalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        __qtablewidgetitem2.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_material_data.setVerticalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        __qtablewidgetitem3.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_material_data.setVerticalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        __qtablewidgetitem4.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_material_data.setVerticalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        __qtablewidgetitem5.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_material_data.setVerticalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        __qtablewidgetitem6.setTextAlignment(Qt.AlignCenter);
        self.tableWidget_material_data.setVerticalHeaderItem(6, __qtablewidgetitem6)
        self.tableWidget_material_data.setObjectName(u"tableWidget_material_data")
        self.tableWidget_material_data.horizontalHeader().setVisible(False)
        self.tableWidget_material_data.verticalHeader().setVisible(True)
        self.tableWidget_material_data.verticalHeader().setCascadingSectionResizes(True)

        self.gridLayout_2.addWidget(self.tableWidget_material_data, 1, 0, 1, 1)

        self.frame_6 = QFrame(self.frame_2)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setMinimumSize(QSize(0, 0))
        self.frame_6.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_6.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_6)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setHorizontalSpacing(8)
        self.gridLayout_5.setVerticalSpacing(0)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.pushButton_add_column = QPushButton(self.frame_6)
        self.pushButton_add_column.setObjectName(u"pushButton_add_column")
        self.pushButton_add_column.setMinimumSize(QSize(26, 26))
        self.pushButton_add_column.setMaximumSize(QSize(26, 26))
        font = QFont()
        font.setFamilies([u"MS Shell Dlg 2"])
        font.setPointSize(9)
        font.setBold(True)
        font.setItalic(False)
        self.pushButton_add_column.setFont(font)
        self.pushButton_add_column.setStyleSheet(u"")

        self.gridLayout_5.addWidget(self.pushButton_add_column, 0, 2, 1, 1)

        self.frame_7 = QFrame(self.frame_6)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_7.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.frame_7)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.pushButton_reset_library = QPushButton(self.frame_7)
        self.pushButton_reset_library.setObjectName(u"pushButton_reset_library")
        self.pushButton_reset_library.setMinimumSize(QSize(60, 26))
        self.pushButton_reset_library.setMaximumSize(QSize(60, 26))
        font1 = QFont()
        font1.setFamilies([u"MS Shell Dlg 2"])
        font1.setPointSize(10)
        font1.setBold(False)
        font1.setItalic(False)
        self.pushButton_reset_library.setFont(font1)
        self.pushButton_reset_library.setStyleSheet(u"")

        self.gridLayout.addWidget(self.pushButton_reset_library, 0, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 1, 1, 1)


        self.gridLayout_5.addWidget(self.frame_7, 0, 0, 1, 1)

        self.pushButton_duplicate = QPushButton(self.frame_6)
        self.pushButton_duplicate.setObjectName(u"pushButton_duplicate")
        self.pushButton_duplicate.setMinimumSize(QSize(28, 28))
        self.pushButton_duplicate.setMaximumSize(QSize(28, 28))
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        font2.setPointSize(9)
        font2.setBold(False)
        font2.setItalic(False)
        self.pushButton_duplicate.setFont(font2)
        self.pushButton_duplicate.setStyleSheet(u"")
        icon = QIcon()
        icon.addFile(u":/icons/copy_icon.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_duplicate.setIcon(icon)
        self.pushButton_duplicate.setIconSize(QSize(18, 18))

        self.gridLayout_5.addWidget(self.pushButton_duplicate, 0, 4, 1, 1)

        self.pushButton_remove_column = QPushButton(self.frame_6)
        self.pushButton_remove_column.setObjectName(u"pushButton_remove_column")
        self.pushButton_remove_column.setMinimumSize(QSize(26, 26))
        self.pushButton_remove_column.setMaximumSize(QSize(26, 26))
        self.pushButton_remove_column.setFont(font2)
        self.pushButton_remove_column.setStyleSheet(u"")

        self.gridLayout_5.addWidget(self.pushButton_remove_column, 0, 3, 1, 1)


        self.gridLayout_2.addWidget(self.frame_6, 0, 0, 1, 1)


        self.gridLayout_4.addWidget(self.frame_2, 0, 0, 1, 1)

        self.frame_buttons = QFrame(Form)
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
        font3 = QFont()
        font3.setPointSize(10)
        font3.setBold(False)
        font3.setItalic(False)
        self.pushButton_apply_and_close.setFont(font3)
        self.pushButton_apply_and_close.setStyleSheet(u"")
        self.pushButton_apply_and_close.setAutoDefault(False)
        self.pushButton_apply_and_close.setFlat(False)

        self.gridLayout_11.addWidget(self.pushButton_apply_and_close, 0, 3, 1, 1)

        self.pushButton_apply = QPushButton(self.frame_buttons)
        self.pushButton_apply.setObjectName(u"pushButton_apply")
        self.pushButton_apply.setMinimumSize(QSize(72, 30))
        self.pushButton_apply.setMaximumSize(QSize(72, 30))
        self.pushButton_apply.setFont(font3)
        self.pushButton_apply.setStyleSheet(u"")
        self.pushButton_apply.setAutoDefault(False)
        self.pushButton_apply.setFlat(False)

        self.gridLayout_11.addWidget(self.pushButton_apply, 0, 2, 1, 1)

        self.pushButton_cancel = QPushButton(self.frame_buttons)
        self.pushButton_cancel.setObjectName(u"pushButton_cancel")
        self.pushButton_cancel.setMinimumSize(QSize(72, 30))
        self.pushButton_cancel.setMaximumSize(QSize(72, 30))
        self.pushButton_cancel.setFont(font3)
        self.pushButton_cancel.setStyleSheet(u"")
        self.pushButton_cancel.setAutoDefault(False)
        self.pushButton_cancel.setFlat(False)

        self.gridLayout_11.addWidget(self.pushButton_cancel, 0, 0, 1, 1)

        self.horizontalSpacer_17 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_11.addItem(self.horizontalSpacer_17, 0, 1, 1, 1)


        self.gridLayout_4.addWidget(self.frame_buttons, 1, 0, 1, 1)


        self.retranslateUi(Form)

        self.pushButton_apply_and_close.setDefault(False)
        self.pushButton_apply.setDefault(False)
        self.pushButton_cancel.setDefault(False)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        ___qtablewidgetitem = self.tableWidget_material_data.verticalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"Name", None));
        ___qtablewidgetitem1 = self.tableWidget_material_data.verticalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"ID", None));
        ___qtablewidgetitem2 = self.tableWidget_material_data.verticalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Form", u"Density [kg/m\u00b3]", None));
        ___qtablewidgetitem3 = self.tableWidget_material_data.verticalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Form", u"Elasticity modulus [Pa]", None));
        ___qtablewidgetitem4 = self.tableWidget_material_data.verticalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Form", u"Poisson ratio", None));
        ___qtablewidgetitem5 = self.tableWidget_material_data.verticalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Form", u"Thermal expansion coefficient [1/K]", None));
        ___qtablewidgetitem6 = self.tableWidget_material_data.verticalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("Form", u"Color", None));
#if QT_CONFIG(tooltip)
        self.pushButton_add_column.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-weight:400;\">Add an empty material</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_add_column.setText(QCoreApplication.translate("Form", u"+", None))
#if QT_CONFIG(tooltip)
        self.pushButton_reset_library.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-weight:400;\">Reset to default material library</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_reset_library.setText(QCoreApplication.translate("Form", u"Reset", None))
#if QT_CONFIG(tooltip)
        self.pushButton_duplicate.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Duplicate the selected material</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_duplicate.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_remove_column.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Remove the selected material</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_remove_column.setText(QCoreApplication.translate("Form", u"-", None))
        self.pushButton_apply_and_close.setText(QCoreApplication.translate("Form", u"Ok", None))
        self.pushButton_apply.setText(QCoreApplication.translate("Form", u"Apply", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("Form", u"Cancel", None))
    # retranslateUi



class MaterialWidget_UI(QWidget, Ui_Form):
    """
    Component Hierarchy:
    - Form: QWidget
        - (Layout): QGridLayout
                - frame_2: QFrame
                    - (Layout): QGridLayout
                            - tableWidget_material_data: QTableWidget
                            - frame_6: QFrame
                                - (Layout): QGridLayout
                                        - pushButton_add_column: QPushButton
                                        - frame_7: QFrame
                                            - (Layout): QGridLayout
                                                    - pushButton_reset_library: QPushButton
                                        - pushButton_duplicate: QPushButton
                                        - pushButton_remove_column: QPushButton
                - frame_buttons: QFrame
                    - (Layout): QGridLayout
                            - pushButton_apply_and_close: QPushButton
                            - pushButton_apply: QPushButton
                            - pushButton_cancel: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
