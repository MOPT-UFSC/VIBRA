from .common_symbols_actor import CommonSymbolsActor


class CommonSymbolsActorFixedSize(CommonSymbolsActor):
    def build(self):
        self.common_build()

        self.mapper.SetInputData(self.data)
        self.mapper.SetSourceIndexArray("sources")
        self.mapper.SetOrientationArray("rotations")
        self.mapper.SetScaleArray("scales")
        self.mapper.SourceIndexingOn()
        self.mapper.ScalarVisibilityOn()
        self.mapper.SetScaleModeToScaleByMagnitude()
        self.mapper.SetScalarModeToUsePointData()
        self.mapper.SetOrientationModeToDirection()
        self.mapper.Update()
