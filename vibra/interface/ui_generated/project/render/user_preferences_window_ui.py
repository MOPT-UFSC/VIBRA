from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QGridLayout,
    QHBoxLayout, QLineEdit, QListWidget, QListWidgetItem,
    QPushButton, QSizePolicy, QSpacerItem, QStackedWidget,
    QVBoxLayout, QWidget)

class Ui_Dialog(object):

    def setupUi(self, Dialog):
        if not Dialog.objectName():

            Dialog.setObjectName(u"Dialog")

        Dialog.resize(580, 420)
        Dialog.setMinimumSize(QSize(570, 400))
        self.verticalLayout_main = QVBoxLayout(Dialog)
        self.verticalLayout_main.setSpacing(4)
        self.verticalLayout_main.setObjectName(u"verticalLayout_main")
        self.verticalLayout_main.setContentsMargins(4, 4, 4, 4)
        self.lineEdit_search = QLineEdit(Dialog)
        self.lineEdit_search.setObjectName(u"lineEdit_search")
        self.lineEdit_search.setMinimumSize(QSize(0, 30))

        font = QFont()
        font.setPointSize(10)

        self.lineEdit_search.setFont(font)

        self.verticalLayout_main.addWidget(self.lineEdit_search)

        self.horizontalLayout_content = QHBoxLayout()
        self.horizontalLayout_content.setSpacing(4)
        self.horizontalLayout_content.setObjectName(u"horizontalLayout_content")
        self.listWidget_categories = QListWidget(Dialog)
        self.listWidget_categories.setObjectName(u"listWidget_categories")
        self.listWidget_categories.setMinimumSize(QSize(180, 0))
        self.listWidget_categories.setMaximumSize(QSize(180, 16777215))
        self.listWidget_categories.setFont(font)

        self.horizontalLayout_content.addWidget(self.listWidget_categories)

        self.stackedWidget_categories = QStackedWidget(Dialog)
        self.stackedWidget_categories.setObjectName(u"stackedWidget_categories")
        self.page_placeholder = QWidget()
        self.page_placeholder.setObjectName(u"page_placeholder")
        self.stackedWidget_categories.addWidget(self.page_placeholder)

        self.horizontalLayout_content.addWidget(self.stackedWidget_categories)


        self.verticalLayout_main.addLayout(self.horizontalLayout_content)

        self.frame_buttons = QFrame(Dialog)
        self.frame_buttons.setObjectName(u"frame_buttons")
        self.frame_buttons.setMinimumSize(QSize(0, 48))
        self.frame_buttons.setMaximumSize(QSize(16777215, 48))
        self.frame_buttons.setFrameShape(QFrame.Shape.NoFrame)
        self.gridLayout = QGridLayout(self.frame_buttons)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.pushButton_reset_to_default = QPushButton(self.frame_buttons)
        self.pushButton_reset_to_default.setObjectName(u"pushButton_reset_to_default")
        self.pushButton_reset_to_default.setMinimumSize(QSize(120, 30))
        self.pushButton_reset_to_default.setMaximumSize(QSize(120, 30))
        self.pushButton_reset_to_default.setFont(font)
        self.pushButton_reset_to_default.setAutoDefault(False)

        self.gridLayout.addWidget(self.pushButton_reset_to_default, 0, 0, 1, 1)

        self.horizontalSpacer_buttons = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_buttons, 0, 1, 1, 1)

        self.pushButton_apply_settings = QPushButton(self.frame_buttons)
        self.pushButton_apply_settings.setObjectName(u"pushButton_apply_settings")
        self.pushButton_apply_settings.setMinimumSize(QSize(120, 30))
        self.pushButton_apply_settings.setMaximumSize(QSize(120, 30))
        self.pushButton_apply_settings.setFont(font)
        self.pushButton_apply_settings.setAutoDefault(False)

        self.gridLayout.addWidget(self.pushButton_apply_settings, 0, 2, 1, 1)

        self.pushButton_update_settings = QPushButton(self.frame_buttons)
        self.pushButton_update_settings.setObjectName(u"pushButton_update_settings")
        self.pushButton_update_settings.setMinimumSize(QSize(120, 30))
        self.pushButton_update_settings.setMaximumSize(QSize(120, 30))
        self.pushButton_update_settings.setFont(font)
        self.pushButton_update_settings.setAutoDefault(False)

        self.gridLayout.addWidget(self.pushButton_update_settings, 0, 3, 1, 1)


        self.verticalLayout_main.addWidget(self.frame_buttons)


        self.retranslateUi(Dialog)

        self.pushButton_update_settings.setDefault(False)


        QMetaObject.connectSlotsByName(Dialog)


    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"User Preferences", None))

        self.lineEdit_search.setPlaceholderText(QCoreApplication.translate("Dialog", u"Search settings", None))
        self.pushButton_reset_to_default.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.pushButton_apply_settings.setText(QCoreApplication.translate("Dialog", u"Apply", None))
        self.pushButton_update_settings.setText(QCoreApplication.translate("Dialog", u"Ok", None))



class UserPreferencesWindow_UI(QDialog, Ui_Dialog):

    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QVBoxLayout
                - lineEdit_search: QLineEdit
                - (Layout): QHBoxLayout
                        - listWidget_categories: QListWidget
                        - stackedWidget_categories: QStackedWidget
                            - page_placeholder: QWidget
                - frame_buttons: QFrame
                    - (Layout): QGridLayout
                            - pushButton_reset_to_default: QPushButton
                            - pushButton_apply_settings: QPushButton
                            - pushButton_update_settings: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
