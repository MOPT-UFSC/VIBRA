from PyQt5.QtWidgets import QDialog, QPushButton, QLabel, QFrame
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pathlib import Path


class PrintMessageInput(QDialog):
    def __init__(self, text_info, justify=True, opv=None, fontsizes=[13, 12], *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("data/ui_files/general/print_messages.ui", self)

        self.pushButton_close = self.findChild(QPushButton, "pushButton_close")
        self.pushButton_close.clicked.connect(self.message_close)

        self.frame_message = self.findChild(QFrame, "frame_message")

        icons_path = 'data/icons/'
        path = str(Path(icons_path + 'logo_vibra.png'))
        self.icon = QIcon(path)
        self.setWindowIcon(self.icon)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        if opv is not None:
            opv.setInputObject(self)

        self.title_fontsize, self.message_fontsize = fontsizes

        self.label_title = self.findChild(QLabel, 'label_title')
        self.label_message = self.findChild(QLabel, 'label_message')
        
        self.pushButton_close.setVisible(True)
        self.create_font_title()
        self.create_font_message()
        self.label_title.setFont(self.font_title)
        self.label_message.setFont(self.font_message)
        self.label_message.setWordWrap(True)
        self.label_message.setMargin(20)
        self.label_message.setAlignment(Qt.AlignCenter)

        self.text_info = text_info
        message = self.preprocess_big_strings(self.text_info[1])
        self.config_sizes(message)

        self.label_title.setText(text_info[0])
        self.label_message.setText(message)
        
        if len(text_info)>2:
            self.setWindowTitle(text_info[2])

        if justify:
            self.label_message.setAlignment(Qt.AlignJustify | Qt.AlignVCenter)
        
        self.exec_()

        self.exec_()

    def message_close(self):
        self.close()

    def create_font_title(self):
        self.font_title = QFont()
        self.font_title.setFamily("Arial")
        self.font_title.setPointSize(self.title_fontsize)
        self.font_title.setBold(True)
        self.font_title.setItalic(False)
        self.font_title.setWeight(75)

    def create_font_message(self):
        self.font_message = QFont()
        self.font_message.setFamily("Arial")
        self.font_message.setPointSize(self.message_fontsize)
        self.font_message.setBold(True)
        self.font_message.setItalic(False)
        self.font_message.setWeight(75)

    def config_message_font(self):
        font = QFont()
        font.setPointSize(17)
        font.setBold(True)
        # font.setItalic(True)
        font.setFamily("Arial")
        # font.setWeight(60)
        self.label_message.setFont(font)
        self.label_message.setStyleSheet("color:blue")

    def config_title_font(self):
        font = QFont()
        font.setPointSize(19)
        font.setBold(True)
        font.setItalic(True)
        font.setFamily("Arial")
        # font.setWeight(60)
        self.label_title.setFont(font)
        self.label_title.setStyleSheet("color:black")
    

    def preprocess_big_strings(self, text):
        message = ""
        list_words = text.split(" ")
        for word in list_words:
            if len(word) > 60:
                while len(word) > 60:
                    message += word[0:60] + " "
                    word = word[60:]
                message += word + " "
            else:
                message += word + " "
        return message

    def config_sizes(self, message):
        if 0 < len(message) < 200:
            height = 300
            width = 600
        elif 200 <= len(message) < 400:
            height = 360
            width = 600
        elif 400 <= len(message) < 800:
            height = 420
            width = 600
        elif 800 <= len(message) < 1000:
            height = 500
            width = 600
        else:
            height = 600
            width = 600

        self.setMinimumWidth(width)
        self.setMinimumHeight(height)
        self.setMaximumWidth(width)
        self.setMaximumHeight(height)
