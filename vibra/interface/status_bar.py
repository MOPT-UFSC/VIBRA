from PyQt5.QtWidgets import QLabel, QStatusBar

class StatusBar(QStatusBar):
    def __init__(self, parent):
        super().__init__(parent)
        self.points_label = QLabel("Selected Point")
        self.lines_label = QLabel("Selected Line")
        self.faces_label = QLabel("Selected Face")
  
        # adding label to status bar
        self.addPermanentWidget(self.points_label)
        self.addPermanentWidget(self.lines_label)
        self.addPermanentWidget(self.faces_label)
    

    def show_points(self, n_points):
        self.points_label.setText(f"Selected Point:{n_points}")

    def show_faces(self, n_faces):
        self.faces_label.setText(f"Selected Face:{n_faces}")

    def show_lines(self, n_lines):
        self.lines_label.setText(f"Selected Face:{n_lines}")
        
        
    