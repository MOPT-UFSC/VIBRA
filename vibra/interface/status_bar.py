from PyQt5.QtWidgets import QLabel, QStatusBar


class StatusBar(QStatusBar):
    def __init__(self, parent):
        super().__init__(parent)
        self.points_label = QLabel("Selected Point:\t")
        self.lines_label = QLabel("Selected Line:\t")
        self.faces_label = QLabel("Selected Face:\t")

        # adding label to status bar
        self.addWidget(self.lines_label)
        self.addWidget(self.points_label)
        self.addWidget(self.faces_label)
        self.faces_label.setFixedWidth(120)
        self.points_label.setFixedWidth(120)
        self.lines_label.setFixedWidth(120)

    def show_points(self, n_points):
        self.points_label.setText(f"Selected Point:{n_points}\t")

    def show_lines(self, n_lines):
        self.lines_label.setText(f"Selected Line:{n_lines}\t")

    def show_faces(self, n_faces):
        self.faces_label.setText(f"Selected Face:{n_faces}\t")

    def clear_selections(self):
        self.points_label.setText(f"Selected Point:\t")
        self.lines_label.setText(f"Selected Line:\t")
        self.faces_label.setText(f"Selected Face:\t")
