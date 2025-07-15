import platform

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QColorDialog

from vibra import app


class PickColorInput(QColorDialog):
    def __init__(self, *args, **kwargs):
        super().__init__()

        self.title = kwargs.get("title", "")

        self._config_window()
        self._initialize()
        self.exec()

    def _config_window(self):
        if platform.system() == "Linux":
            self.setOption(QColorDialog.ColorDialogOption.DontUseNativeDialog)
        self.setFixedSize(QSize(540, 410))
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowIcon(app().main_window.vibra_icon) 
        self.setWindowTitle(self.title)
    
    def _initialize(self):
        self.color = [] 
        self.complete = False  
        self.colorSelected.connect(self.confirm_color)   

    def confirm_color(self):
        color = self.currentColor().getRgb()
        self.complete = True
        self.color = list(color[0:3])
        self.close()
     
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()