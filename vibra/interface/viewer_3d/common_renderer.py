import vtk


class CommonRenderer(vtk.vtkRenderer):
    def set_view_up(self):
        x, y, z = self.GetActiveCamera().GetFocalPoint()
        position = (x, y + 1, z)
        view_up = (0, 1, 0)
        self.set_custom_view(position, view_up)

    def set_view_down(self):
        x, y, z = self.GetActiveCamera().GetFocalPoint()
        position = (x, y - 1, z)
        view_up = (0, 1, 0)
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
        position = (x, y + 1, z)
        view_up = (0, 1, 0)
        self.set_custom_view(position, view_up)

    def set_custom_view(self, position, view_up):
        self.GetActiveCamera().SetPosition(position)
        self.GetActiveCamera().SetViewUp(view_up)
        self.GetActiveCamera().SetParallelProjection(True)
        self.ResetCamera(*self.ComputeVisiblePropBounds())

        if self.GetRenderWindow() is not None:
            self.GetRenderWindow().Render()
