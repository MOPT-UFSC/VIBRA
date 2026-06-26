# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'export_mesh.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QFrame,
    QGridLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QWidget)

from vibra.interface.formatters.icons import themed_icon

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(357, 280)
        Dialog.setMinimumSize(QSize(0, 280))
        Dialog.setMaximumSize(QSize(16777215, 280))
        font = QFont()
        font.setPointSize(10)
        Dialog.setFont(font)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame)
        self.gridLayout_4.setSpacing(4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(4, 4, 4, 4)
        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(4, 4, 4, 4)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.checkBox_nodal_coordinates = QCheckBox(self.frame_2)
        self.checkBox_nodal_coordinates.setObjectName(u"checkBox_nodal_coordinates")
        self.checkBox_nodal_coordinates.setMaximumSize(QSize(260, 16777215))
        self.checkBox_nodal_coordinates.setFont(font)

        self.gridLayout_2.addWidget(self.checkBox_nodal_coordinates, 0, 1, 1, 1)

        self.checkBox_face_elements_connectivity = QCheckBox(self.frame_2)
        self.checkBox_face_elements_connectivity.setObjectName(u"checkBox_face_elements_connectivity")
        self.checkBox_face_elements_connectivity.setMaximumSize(QSize(260, 16777215))
        self.checkBox_face_elements_connectivity.setFont(font)

        self.gridLayout_2.addWidget(self.checkBox_face_elements_connectivity, 1, 1, 1, 1)

        self.checkBox_export_vtu_file = QCheckBox(self.frame_2)
        self.checkBox_export_vtu_file.setObjectName(u"checkBox_export_vtu_file")
        self.checkBox_export_vtu_file.setMaximumSize(QSize(260, 16777215))
        self.checkBox_export_vtu_file.setFont(font)

        self.gridLayout_2.addWidget(self.checkBox_export_vtu_file, 4, 1, 1, 1)

        self.checkBox_solid_elements_connectivity = QCheckBox(self.frame_2)
        self.checkBox_solid_elements_connectivity.setObjectName(u"checkBox_solid_elements_connectivity")
        self.checkBox_solid_elements_connectivity.setMaximumSize(QSize(260, 16777215))
        self.checkBox_solid_elements_connectivity.setFont(font)

        self.gridLayout_2.addWidget(self.checkBox_solid_elements_connectivity, 2, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_2, 0, 2, 1, 1)


        self.gridLayout_4.addWidget(self.frame_2, 2, 0, 1, 1)

        self.frame_4 = QFrame(self.frame)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(0, 40))
        self.frame_4.setMaximumSize(QSize(16777215, 48))
        self.frame_4.setFrameShape(QFrame.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_4)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(4, 4, 4, 4)
        self.pushButton_export_mesh = QPushButton(self.frame_4)
        self.pushButton_export_mesh.setObjectName(u"pushButton_export_mesh")
        self.pushButton_export_mesh.setMinimumSize(QSize(120, 30))
        self.pushButton_export_mesh.setMaximumSize(QSize(120, 30))
        self.pushButton_export_mesh.setFont(font)
        icon = themed_icon(u":/icons/import.png")
        self.pushButton_export_mesh.setIcon(icon)
        self.pushButton_export_mesh.setAutoDefault(False)

        self.gridLayout_5.addWidget(self.pushButton_export_mesh, 0, 1, 1, 1)

        self.pushButton_exit = QPushButton(self.frame_4)
        self.pushButton_exit.setObjectName(u"pushButton_exit")
        self.pushButton_exit.setMinimumSize(QSize(120, 30))
        self.pushButton_exit.setMaximumSize(QSize(120, 30))
        self.pushButton_exit.setFont(font)
        icon1 = themed_icon(u":/icons/exit.png")
        self.pushButton_exit.setIcon(icon1)
        self.pushButton_exit.setAutoDefault(False)

        self.gridLayout_5.addWidget(self.pushButton_exit, 0, 0, 1, 1)


        self.gridLayout_4.addWidget(self.frame_4, 3, 0, 1, 1)

        self.frame_5 = QFrame(self.frame)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setMinimumSize(QSize(0, 40))
        self.frame_5.setFrameShape(QFrame.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.gridLayout_6 = QGridLayout(self.frame_5)
        self.gridLayout_6.setSpacing(4)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(4, 4, 4, 4)
        self.lineEdit_folder_path = QLineEdit(self.frame_5)
        self.lineEdit_folder_path.setObjectName(u"lineEdit_folder_path")
        self.lineEdit_folder_path.setMinimumSize(QSize(0, 30))
        self.lineEdit_folder_path.setMaximumSize(QSize(16777215, 30))
        self.lineEdit_folder_path.setAlignment(Qt.AlignCenter)

        self.gridLayout_6.addWidget(self.lineEdit_folder_path, 0, 0, 1, 1)

        self.pushButton_search_folder = QPushButton(self.frame_5)
        self.pushButton_search_folder.setObjectName(u"pushButton_search_folder")
        self.pushButton_search_folder.setMinimumSize(QSize(40, 30))
        self.pushButton_search_folder.setMaximumSize(QSize(40, 30))
        self.pushButton_search_folder.setFont(font)
        icon2 = themed_icon(u":/icons/views/zoom_icon.png")
        self.pushButton_search_folder.setIcon(icon2)
        self.pushButton_search_folder.setIconSize(QSize(20, 20))
        self.pushButton_search_folder.setAutoDefault(False)

        self.gridLayout_6.addWidget(self.pushButton_search_folder, 0, 1, 1, 1)


        self.gridLayout_4.addWidget(self.frame_5, 1, 0, 1, 1)


        self.gridLayout.addWidget(self.frame, 1, 0, 1, 1)

        self.frame_3 = QFrame(Dialog)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(0, 40))
        self.frame_3.setMaximumSize(QSize(16777215, 48))
        self.frame_3.setFrameShape(QFrame.Box)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_3)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(4, 4, 4, 4)
        self.label = QLabel(self.frame_3)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(0, 26))
        self.label.setMaximumSize(QSize(16777215, 32))
        font1 = QFont()
        font1.setPointSize(11)
        self.label.setFont(font1)
        self.label.setFrameShape(QFrame.NoFrame)
        self.label.setFrameShadow(QFrame.Raised)
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_3, 0, 0, 1, 1)

        QWidget.setTabOrder(self.lineEdit_folder_path, self.pushButton_search_folder)
        QWidget.setTabOrder(self.pushButton_search_folder, self.checkBox_nodal_coordinates)
        QWidget.setTabOrder(self.checkBox_nodal_coordinates, self.checkBox_face_elements_connectivity)
        QWidget.setTabOrder(self.checkBox_face_elements_connectivity, self.checkBox_solid_elements_connectivity)
        QWidget.setTabOrder(self.checkBox_solid_elements_connectivity, self.checkBox_export_vtu_file)
        QWidget.setTabOrder(self.checkBox_export_vtu_file, self.pushButton_export_mesh)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Export mesh data", None))
#if QT_CONFIG(tooltip)
        self.checkBox_nodal_coordinates.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>The nodal coordinates will be exported to the &quot;nodal_coordinates.dat&quot; file.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_nodal_coordinates.setText(QCoreApplication.translate("Dialog", u"Nodal coordinates", None))
#if QT_CONFIG(tooltip)
        self.checkBox_face_elements_connectivity.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>The face elements connectivity data will be exported to the &quot;face_elements_connectivity.dat&quot; file.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_face_elements_connectivity.setText(QCoreApplication.translate("Dialog", u"Face elements connectivity", None))
#if QT_CONFIG(tooltip)
        self.checkBox_export_vtu_file.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>The mesh data will be exported to the &quot;mesh_data.vtu&quot; file.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_export_vtu_file.setText(QCoreApplication.translate("Dialog", u"Paraview compatible format", None))
#if QT_CONFIG(tooltip)
        self.checkBox_solid_elements_connectivity.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>The solid elements connectivity data will be exported to the &quot;solid_elements_connectivity.dat&quot; file.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_solid_elements_connectivity.setText(QCoreApplication.translate("Dialog", u"Solid elements connectivity", None))
        self.pushButton_export_mesh.setText(QCoreApplication.translate("Dialog", u" Export mesh", None))
        self.pushButton_exit.setText(QCoreApplication.translate("Dialog", u"Exit", None))
        self.pushButton_search_folder.setText("")
        self.label.setText(QCoreApplication.translate("Dialog", u"Mesh data export assistant", None))
    # retranslateUi



class ExportMesh_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame: QFrame
                    - (Layout): QGridLayout
                            - frame_2: QFrame
                                - (Layout): QGridLayout
                                        - checkBox_nodal_coordinates: QCheckBox
                                        - checkBox_face_elements_connectivity: QCheckBox
                                        - checkBox_export_vtu_file: QCheckBox
                                        - checkBox_solid_elements_connectivity: QCheckBox
                            - frame_4: QFrame
                                - (Layout): QGridLayout
                                        - pushButton_export_mesh: QPushButton
                                        - pushButton_exit: QPushButton
                            - frame_5: QFrame
                                - (Layout): QGridLayout
                                        - lineEdit_folder_path: QLineEdit
                                        - pushButton_search_folder: QPushButton
                - frame_3: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
