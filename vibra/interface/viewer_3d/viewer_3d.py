import vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor






class Viewer3D(QVTKRenderWindowInteractor):
    def __init__(self, parent=None):
        super().__init__()
