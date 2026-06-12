# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'degrees_of_freedom_decoupling_inputs.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QGridLayout,
    QHeaderView, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QTabWidget, QTreeWidget,
    QTreeWidgetItem, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setWindowModality(Qt.WindowModality.WindowModal)
        Dialog.resize(400, 400)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(400, 340))
        Dialog.setMaximumSize(QSize(400, 400))
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
        self.frame.setMaximumSize(QSize(420, 48))
        self.frame.setFrameShape(QFrame.Shape.Box)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.frame.setLineWidth(1)
        self.gridLayout_6 = QGridLayout(self.frame)
        self.gridLayout_6.setSpacing(4)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(4, 4, 4, 4)
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
        self.frame_2.setMinimumSize(QSize(380, 0))
        self.frame_2.setMaximumSize(QSize(420, 480))
        self.frame_2.setFrameShape(QFrame.Shape.Box)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_2)
        self.gridLayout_4.setSpacing(4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(4, 4, 4, 4)
        self.tabWidget_main = QTabWidget(self.frame_2)
        self.tabWidget_main.setObjectName(u"tabWidget_main")
        self.tabWidget_main.setMinimumSize(QSize(360, 0))
        self.tabWidget_main.setMaximumSize(QSize(380, 16777215))
        font2 = QFont()
        font2.setPointSize(10)
        font2.setBold(False)
        self.tabWidget_main.setFont(font2)
        self.tab_setup = QWidget()
        self.tab_setup.setObjectName(u"tab_setup")
        self.gridLayout_12 = QGridLayout(self.tab_setup)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setHorizontalSpacing(2)
        self.gridLayout_12.setVerticalSpacing(8)
        self.gridLayout_12.setContentsMargins(12, 12, 12, 12)
        self.label_2 = QLabel(self.tab_setup)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(0, 32))
        self.label_2.setMaximumSize(QSize(16777215, 32))
        self.label_2.setFrameShape(QFrame.Shape.Box)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_12.addWidget(self.label_2, 0, 0, 1, 1)

        self.treeWidget_selection_info = QTreeWidget(self.tab_setup)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter);
        self.treeWidget_selection_info.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_selection_info.setObjectName(u"treeWidget_selection_info")
        self.treeWidget_selection_info.setMinimumSize(QSize(0, 0))
        self.treeWidget_selection_info.setMaximumSize(QSize(340, 16777215))
        self.treeWidget_selection_info.setIndentation(0)

        self.gridLayout_12.addWidget(self.treeWidget_selection_info, 1, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_setup, "")
        self.tab_list = QWidget()
        self.tab_list.setObjectName(u"tab_list")
        self.gridLayout_9 = QGridLayout(self.tab_list)
        self.gridLayout_9.setSpacing(2)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(2, 8, 2, 2)
        self.frame_3 = QFrame(self.tab_list)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(320, 40))
        self.frame_3.setMaximumSize(QSize(320, 40))
        self.frame_3.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_8 = QGridLayout(self.frame_3)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setHorizontalSpacing(12)
        self.gridLayout_8.setContentsMargins(4, 4, 4, 4)
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

        self.treeWidget_dof_decoupling = QTreeWidget(self.tab_list)
        __qtreewidgetitem1 = QTreeWidgetItem()
        __qtreewidgetitem1.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem1.setTextAlignment(0, Qt.AlignCenter);
        self.treeWidget_dof_decoupling.setHeaderItem(__qtreewidgetitem1)
        self.treeWidget_dof_decoupling.setObjectName(u"treeWidget_dof_decoupling")
        self.treeWidget_dof_decoupling.setMinimumSize(QSize(320, 0))
        self.treeWidget_dof_decoupling.setMaximumSize(QSize(320, 200))
        font4 = QFont()
        font4.setFamilies([u"MS Shell Dlg 2"])
        font4.setPointSize(9)
        font4.setBold(False)
        font4.setItalic(False)
        self.treeWidget_dof_decoupling.setFont(font4)
        self.treeWidget_dof_decoupling.setIndentation(1)
        self.treeWidget_dof_decoupling.setHeaderHidden(False)
        self.treeWidget_dof_decoupling.header().setHighlightSections(False)
        self.treeWidget_dof_decoupling.header().setProperty(u"showSortIndicator", False)
        self.treeWidget_dof_decoupling.header().setStretchLastSection(True)

        self.gridLayout_9.addWidget(self.treeWidget_dof_decoupling, 0, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_list, "")

        self.gridLayout_4.addWidget(self.tabWidget_main, 1, 0, 1, 1)

        self.frame_8 = QFrame(self.frame_2)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setMinimumSize(QSize(0, 52))
        self.frame_8.setMaximumSize(QSize(16777215, 52))
        self.frame_8.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_8.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.frame_8)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(6)
        self.gridLayout.setVerticalSpacing(2)
        self.gridLayout.setContentsMargins(2, 2, 2, 2)
        self.lineEdit_selection_id = QLineEdit(self.frame_8)
        self.lineEdit_selection_id.setObjectName(u"lineEdit_selection_id")
        self.lineEdit_selection_id.setMinimumSize(QSize(200, 28))
        self.lineEdit_selection_id.setMaximumSize(QSize(200, 28))
        font5 = QFont()
        font5.setPointSize(10)
        font5.setBold(False)
        font5.setItalic(False)
        self.lineEdit_selection_id.setFont(font5)
        self.lineEdit_selection_id.setStyleSheet(u"")
        self.lineEdit_selection_id.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_selection_id, 0, 2, 1, 1)

        self.label_10 = QLabel(self.frame_8)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(90, 28))
        self.label_10.setMaximumSize(QSize(90, 28))
        self.label_10.setFont(font3)
        self.label_10.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_10, 0, 1, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_4, 0, 3, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_3, 0, 0, 1, 1)


        self.gridLayout_4.addWidget(self.frame_8, 0, 0, 1, 1)


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

        self.horizontalSpacer_17 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_11.addItem(self.horizontalSpacer_17, 0, 1, 1, 1)


        self.gridLayout_7.addWidget(self.frame_buttons, 2, 0, 1, 1)


        self.retranslateUi(Dialog)

        self.tabWidget_main.setCurrentIndex(0)
        self.pushButton_apply_and_close.setDefault(False)
        self.pushButton_apply.setDefault(False)
        self.pushButton_cancel.setDefault(False)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Set anechoic termination", None))
#if QT_CONFIG(whatsthis)
        Dialog.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.label.setText(QCoreApplication.translate("Dialog", u"Degrees of Freedom Decoupling Assistant", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Entity selection information", None))
        ___qtreewidgetitem = self.treeWidget_selection_info.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"Volumes from surface", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Surface", None));
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_setup), QCoreApplication.translate("Dialog", u"Setup", None))
        self.pushButton_reset.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.pushButton_remove.setText(QCoreApplication.translate("Dialog", u"Remove", None))
        ___qtreewidgetitem1 = self.treeWidget_dof_decoupling.headerItem()
        ___qtreewidgetitem1.setText(1, QCoreApplication.translate("Dialog", u"Volume to decouple", None));
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("Dialog", u"Surface", None));
#if QT_CONFIG(tooltip)
        self.treeWidget_dof_decoupling.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_list), QCoreApplication.translate("Dialog", u"List", None))
        self.lineEdit_selection_id.setText("")
        self.label_10.setText(QCoreApplication.translate("Dialog", u"Selected ID:", None))
        self.pushButton_apply_and_close.setText(QCoreApplication.translate("Dialog", u"Ok", None))
        self.pushButton_apply.setText(QCoreApplication.translate("Dialog", u"Apply", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
    # retranslateUi



class DegreesOfFreedomDecouplingInputs_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
                - frame_2: QFrame
                    - (Layout): QGridLayout
                            - tabWidget_main: QTabWidget
                                - tab_setup: QWidget
                                    - (Layout): QGridLayout
                                            - label_2: QLabel
                                            - treeWidget_selection_info: QTreeWidget
                                - tab_list: QWidget
                                    - (Layout): QGridLayout
                                            - frame_3: QFrame
                                                - (Layout): QGridLayout
                                                        - pushButton_reset: QPushButton
                                                        - pushButton_remove: QPushButton
                                            - treeWidget_dof_decoupling: QTreeWidget
                            - frame_8: QFrame
                                - (Layout): QGridLayout
                                        - lineEdit_selection_id: QLineEdit
                                        - label_10: QLabel
                - frame_buttons: QFrame
                    - (Layout): QGridLayout
                            - pushButton_apply_and_close: QPushButton
                            - pushButton_apply: QPushButton
                            - pushButton_cancel: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
