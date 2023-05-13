import vtk


class CommonRenderer(vtk.vtkRenderer):
    def set_view_up(self):
        x, y, z = self.GetActiveCamera().GetFocalPoint()
        position = (x, y + 1, z)
        view_up = (0, 0, -1)
        self.set_custom_view(position, view_up)

    def set_view_down(self):
        x, y, z = self.GetActiveCamera().GetFocalPoint()
        position = (x, y - 1, z)
        view_up = (0, 0, 1)
        self.set_custom_view(position, view_up)

    def set_view_left(self):
        x, y, z = self.GetActiveCamera().GetFocalPoint()
        position = (x - 1, y, z)
        view_up = (0, 1, 0)
        self.set_custom_view(position, view_up)

    def set_view_right(self):
        x, y, z = self.GetActiveCamera().GetFocalPoint()
        position = (x + 1, y, z)
        view_up = (0, 1, 0)
        self.set_custom_view(position, view_up)

    def set_view_front(self):
        x, y, z = self.GetActiveCamera().GetFocalPoint()
        position = (x, y, z + 1)
        view_up = (0, 1, 0)
        self.set_custom_view(position, view_up)

    def set_view_back(self):
        x, y, z = self.GetActiveCamera().GetFocalPoint()
        position = (x, y, z - 1)
        view_up = (0, 1, 0)
        self.set_custom_view(position, view_up)

    def set_view_orthogonal(self):
        x, y, z = self.GetActiveCamera().GetFocalPoint()
        position = (x + 1, y + 1, z + 1)
        view_up = (0, 1, 0)
        self.set_custom_view(position, view_up)

    def set_custom_view(self, position, view_up):
        self.GetActiveCamera().SetPosition(position)
        self.GetActiveCamera().SetViewUp(view_up)
        self.GetActiveCamera().SetParallelProjection(True)
        self.ResetCamera(*self.ComputeVisiblePropBounds())

        if self.GetRenderWindow() is not None:
            self.GetRenderWindow().Render()

    def create_axes(self):
        axes_actor = vtk.vtkAxesActor()

        x_property = axes_actor.GetXAxisCaptionActor2D().GetCaptionTextProperty()
        y_property = axes_actor.GetYAxisCaptionActor2D().GetCaptionTextProperty()
        z_property = axes_actor.GetZAxisCaptionActor2D().GetCaptionTextProperty()

        for i in [x_property, y_property, z_property]:
            i.ItalicOff()
            i.BoldOff()

        self.axes = vtk.vtkOrientationMarkerWidget()
        self.axes.SetOrientationMarker(axes_actor)
        self.axes.SetInteractor(self.GetRenderWindow().GetInteractor())
        self.axes.EnabledOn()
        self.axes.InteractiveOff()

    def create_scale_bar(self):
        self.scale_bar = vtk.vtkLegendScaleActor()
        self.scale_bar.AllAxesOff()

        title_property = self.scale_bar.GetLegendTitleProperty()
        title_property.SetFontSize(14)
        title_property.ShadowOff()
        title_property.ItalicOff()
        title_property.SetLineOffset(-35)
        title_property.SetVerticalJustificationToTop()

        label_property = self.scale_bar.GetLegendLabelProperty()
        label_property.SetFontSize(12)
        label_property.ShadowOff()
        label_property.ItalicOff()
        label_property.BoldOff()
        label_property.SetLineOffset(-25)

        self.AddActor(self.scale_bar)
