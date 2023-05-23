import vtk


class CommonRenderer(vtk.vtkRenderer):
    '''
    Base class for all renderers.

    All the common structures that obviously need to be the 
    same in every interactor should be implemented here.
    '''
    
    def set_theme(self, theme):
        if theme == "dark":
            self.GradientBackgroundOn()
            self.SetBackground(0.06, 0.08, 0.12)
            self.SetBackground2(0, 0, 0)
        elif theme == "light":
            self.GradientBackgroundOn()
            self.SetBackground(0.5, 0.5, 0.65)
            self.SetBackground2(1, 1, 1)
        else:
            NotImplemented

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

    # override it =)
    def show_points(self):
        pass

    def show_edges(self):
        pass

    def show_faces(self):
        pass

    def set_custom_view(self, position, view_up):
        self.GetActiveCamera().SetPosition(position)
        self.GetActiveCamera().SetViewUp(view_up)
        self.GetActiveCamera().SetParallelProjection(True)
        self.ResetCamera(*self.ComputeVisiblePropBounds())

        if self.GetRenderWindow() is not None:
            self.GetRenderWindow().Render()

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

    def update(self):
        ren_win = self.GetRenderWindow()
        if ren_win is not None:
            ren_win.Render()
