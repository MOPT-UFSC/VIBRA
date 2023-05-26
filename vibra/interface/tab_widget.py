from PyQt5.QtCore import QCoreApplication, pyqtSignal
from PyQt5.QtWidgets import QWidget, QTabWidget, QPushButton, QVBoxLayout

from vibra.interface.viewer_3d.viewer_3d import Viewer3D


class ProjectTabs(QTabWidget):
    def __init__(self, parent, project):
        super(QWidget, self).__init__(parent)
        
        self.project = project

        self.tabCloseRequested.connect(self.removeTab)

    def configure_window(self):
        self.setStyleSheet(
        '''
        QTabBar::tab {
            margin-left: 10px;
            margin-right: 10px;
        }
        '''
        )
        self.setTabsClosable(True)
        self.setMovable(True)
        self.setDocumentMode(True)
    
    def add_model_viewer(self):
        viewer = Viewer3D(self, self.project)
        self.addTab(viewer, self.project.name)