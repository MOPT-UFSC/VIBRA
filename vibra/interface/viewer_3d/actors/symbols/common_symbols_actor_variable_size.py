from .common_symbols_actor import CommonSymbolsActor
from vtkmodules.vtkRenderingCore import vtkDistanceToCamera, vtkRenderer


class CommonSymbolsActorVariableSize(CommonSymbolsActor):
    def __init__(self, renderer: vtkRenderer):
        super().__init__()
        self.renderer = renderer

    def build(self):
        self.common_build()

        distance_to_camera = vtkDistanceToCamera()
        distance_to_camera.SetInputData(self.data)
        distance_to_camera.SetScreenSize(40)
        distance_to_camera.SetRenderer(self.renderer)

        self.mapper.SetInputConnection(distance_to_camera.GetOutputPort())
        self.mapper.SetSourceIndexArray("sources")
        self.mapper.SetOrientationArray("rotations")
        self.mapper.SetScaleArray("DistanceToCamera")
        self.mapper.SourceIndexingOn()
        self.mapper.ScalarVisibilityOn()
        self.mapper.SetScaleModeToScaleByMagnitude()
        self.mapper.SetScalarModeToUsePointData()
        self.mapper.SetOrientationModeToDirection()

        # shows the actor in front of everything else
        # offset = -66000
        offset = 0
        factor = 1.3
        self.mapper.SetResolveCoincidentTopologyToPolygonOffset()
        self.mapper.SetRelativeCoincidentTopologyLineOffsetParameters(factor, offset)
        self.mapper.SetRelativeCoincidentTopologyPolygonOffsetParameters(factor, offset)
        self.mapper.SetRelativeCoincidentTopologyPointOffsetParameter(offset)

        self.mapper.Update()
