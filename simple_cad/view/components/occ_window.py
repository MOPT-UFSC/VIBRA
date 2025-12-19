from OCC.Core.AIS import AIS_Trihedron, AIS_Shape
from OCC.Core.Geom import Geom_Axis2Placement
from OCC.Core.Graphic3d import Graphic3d_TMF_ZoomPers, Graphic3d_TransformPers
from OCC.Core.Quantity import Quantity_NOC_RED, Quantity_NOC_GREEN, Quantity_NOC_BLUE, Quantity_Color
from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Ax2
from OCC.Display.backend import load_backend
from PySide6.QtGui import QResizeEvent, QAction, QIcon

from simple_cad.geometry.geometry_models import BaseGeometry
from simple_cad.service.geometry_service import GeometryCollection
from simple_cad.service.view_service import ViewService, ViewAction
from simple_cad.view.components.volume_selection_handler import VolumeSelectionHandler

load_backend('pyside6')
from OCC.Display.qtDisplay import qtViewer3d
from PySide6.QtWidgets import QWidget, QVBoxLayout, QToolBar, QHBoxLayout
from PySide6.QtCore import Signal, QTimer


class ClickableViewer3d(qtViewer3d):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mouse_clicked_callback = None

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if self.mouse_clicked_callback:
            QTimer.singleShot(110, lambda: self.mouse_clicked_callback())


class OCCWindow(QWidget):
    geometrySelected = Signal(BaseGeometry)

    def __init__(self, parent, geometry_collection: GeometryCollection, view_service: ViewService):
        super().__init__(parent=parent)
        self._geometry_collection = geometry_collection
        self._geometry_collection.on_geometries_change.connect(self.updateView)
        self._view_service = view_service
        self._view_service.on_view_change.connect(self.updateView)
        self._view_service.on_view_action.connect(self.applyViewAction)

        self.canvas = ClickableViewer3d(self)
        self.display = self.canvas._display
        self.view = self.canvas._display.View
        self.canvas.mouse_clicked_callback = self.onMousePress
        self.ais_map = {}

        # Solid selection handler (set externally)
        self.volume_selection_handler = None

        self.addCoordinateAxis()

    def onMousePress(self):
        if self.volume_selection_handler and self.volume_selection_handler.is_active():
            # Handle volume selection mode
            ctx = self.display.Context
            selected_ais = ctx.SelectedInteractive()
            self.volume_selection_handler.handle_mouse_click(selected_ais)

    def applyViewAction(self, value: str):
        if value == ViewAction.VIEW_FIT.name:
            self.display.FitAll()
        elif value == ViewAction.VIEW_FRONT.name:
            self.view.SetProj(0, 0, 1)
            self.view.SetUp(0, 1, 0)
            self.view.Update()
        elif value == ViewAction.VIEW_BACK.name:
            self.view.SetProj(0, 0, -1)
            self.view.SetUp(0, 1, 0)
            self.view.Update()
        elif value == ViewAction.VIEW_TOP.name:
            self.view.SetProj(0, 1, 0)
            self.view.SetUp(0, 0, 1)
            self.view.Update()
        elif value == ViewAction.VIEW_BOTTOM.name:
            self.view.SetProj(0, -1, 0)
            self.view.SetUp(0, 0, 1)
            self.view.Update()
        elif value == ViewAction.VIEW_LEFT.name:
            self.view.SetProj(-1, 0, 0)
            self.view.SetUp(0, 1, 0)
            self.view.Update()
        elif value == ViewAction.VIEW_RIGHT.name:
            self.view.SetProj(1, 0, 0)
            self.view.SetUp(0, 1, 0)
            self.view.Update()
        elif value == ViewAction.VIEW_ISO.name:
            self.view.SetProj(1, 1, 1)
            self.view.SetUp(0, 0, 1)
            self.view.Update()


    def AddItem(self, source: BaseGeometry):
        transparency = 0
        if self._view_service.transparency:
            transparency = 0.3

        ais = AIS_Shape(source.GetShape())
        ais.SetTransparency(transparency)
        self.display.Context.Display(ais, True)
        self.ais_map[ais] = source

    def updateView(self):
        self.display.EraseAll()
        self.ais_map = {}
        for geo in self._geometry_collection:
            self.AddItem(geo)

        self.addCoordinateAxis()

    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.canvas.resize(self.width(), self.height())

    def addCoordinateAxis(self):
        ax2 = gp_Ax2(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1))
        axis_placement = Geom_Axis2Placement(ax2)

        trihedron = AIS_Trihedron(axis_placement)
        trihedron.SetAxisColor(Quantity_Color(Quantity_NOC_BLUE))
        trihedron.SetXAxisColor(Quantity_Color(Quantity_NOC_RED))
        trihedron.SetYAxisColor(Quantity_Color(Quantity_NOC_GREEN))

        zoom_pers = Graphic3d_TransformPers(Graphic3d_TMF_ZoomPers, gp_Pnt(0, 0, 0))
        trihedron.SetTransformPersistence(zoom_pers)

        self.display.Context.Display(trihedron, True)


class OCCWindowWithViewToolBar(QWidget):

    def __init__(self, parent, geometry_collection: GeometryCollection):
        super().__init__(parent=parent)
        self.view_service = ViewService()

        self.occ_window = OCCWindow(self, geometry_collection, self.view_service)
        
        # Setup volume selection handler (will be set up after toolbar creation)
        self.volume_selection_handler = None

        # Create view toolbar
        self.view_toolbar = QToolBar("View Toolbar")

        self.top_action = QAction(QIcon(":/icons/views/top.png"), "Top", self.view_toolbar)
        self.top_action.setToolTip('Top view')
        self.top_action.triggered.connect(lambda: self.applyViewAction(ViewAction.VIEW_TOP.name))
        self.view_toolbar.addAction(self.top_action)

        self.bottom_action = QAction(QIcon(":/icons/views/bottom.png"), "Bottom", self.view_toolbar)
        self.bottom_action.setToolTip('Bottom view')
        self.bottom_action.triggered.connect(lambda: self.applyViewAction(ViewAction.VIEW_BOTTOM.name))
        self.view_toolbar.addAction(self.bottom_action)

        self.right_action = QAction(QIcon(":/icons/views/right.png"), "Right", self.view_toolbar)
        self.right_action.setToolTip('Right view')
        self.right_action.triggered.connect(lambda: self.applyViewAction(ViewAction.VIEW_RIGHT.name))
        self.view_toolbar.addAction(self.right_action)

        self.left_action = QAction(QIcon(":/icons/views/left.png"), "Left", self.view_toolbar)
        self.left_action.setToolTip('Left view')
        self.left_action.triggered.connect(lambda: self.applyViewAction(ViewAction.VIEW_LEFT.name))
        self.view_toolbar.addAction(self.left_action)

        self.front_action = QAction(QIcon(":/icons/views/front.png"), "Front", self.view_toolbar)
        self.front_action.setToolTip('Front view')
        self.front_action.triggered.connect(lambda: self.applyViewAction(ViewAction.VIEW_FRONT.name))
        self.view_toolbar.addAction(self.front_action)

        self.back_action = QAction(QIcon(":/icons/views/back.png"), "Back", self.view_toolbar)
        self.back_action.setToolTip('Back view')
        self.back_action.triggered.connect(lambda: self.applyViewAction(ViewAction.VIEW_BACK.name))
        self.view_toolbar.addAction(self.back_action)

        self.iso_action = QAction(QIcon(":/icons/views/orthogonal.png"), "ISO", self.view_toolbar)
        self.iso_action.setToolTip('ISO-view')
        self.iso_action.triggered.connect(lambda: self.applyViewAction(ViewAction.VIEW_ISO.name))
        self.view_toolbar.addAction(self.iso_action)

        self.fit_action = QAction(QIcon(":/icons/views/zoom_icon.png"), "FIT", self.view_toolbar)
        self.fit_action.setToolTip('Fit view')
        self.fit_action.triggered.connect(lambda: self.applyViewAction(ViewAction.VIEW_FIT.name))
        self.view_toolbar.addAction(self.fit_action)

        # Create layout
        layout = QVBoxLayout()
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.view_toolbar)
        hlayout.addStretch()
        layout.addLayout(hlayout)
        layout.addWidget(self.occ_window)
        self.setLayout(layout)
        
        # Setup volume selection handler after everything is created
        self.volume_selection_handler = VolumeSelectionHandler(self.occ_window)
        self.occ_window.volume_selection_handler = self.volume_selection_handler

    def startVolumeSelectionMode(self, geometry):
        """Start volume selection mode for a geometry."""
        self.volume_selection_handler.activate(geometry)

    def applyViewAction(self, value: str):
        self.view_service.setViewAction(value)
