from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QScrollArea, QVBoxLayout, QWidget


class HelpWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Help")

        title_label = QLabel("Welcome to the Vibra Help")
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont("Arial", 18, QFont.Bold)
        title_label.setFont(title_font)

        info_label = QLabel()
        info_label.setWordWrap(True)
        info_label.setText(
            "Here are some information about our software and how to contact us on GitHub:"
        )

        contact_label = QLabel()
        contact_label.setText("GitHub: github.com/blabla")

        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addSpacing(20)
        layout.addWidget(info_label)
        layout.addSpacing(10)
        layout.addWidget(contact_label)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_widget.setLayout(layout)
        scroll_area.setWidget(scroll_widget)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)
