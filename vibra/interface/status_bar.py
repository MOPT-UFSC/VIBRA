from PyQt5.QtWidgets import QLabel, QStatusBar

class StatusBar(QStatusBar):
    def __init__(self, parent):
        super().__init__(parent)
        self.label_1 = QLabel("Label 1")
        self.label_1.move(100, 100)
        self.setStyleSheet("background-image : url(data/icons/png.png);")
        self.label_2 = QLabel("Label 2")
        self.label_1.setStyleSheet("""
                border :2px solid;
                border-width: 1px;
                border-color: #888888;
                border-radius: 3px""")
        
  
        # adding label to status bar
        self.addPermanentWidget(self.label_1)
        self.addPermanentWidget(self.label_2)
    

    def show_points(self, n_points):
        self.label_1.setText(f"numero de pontos:{n_points}")
        
    