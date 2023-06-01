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

    # override it =)
    def show_points(self):
        pass

    def show_lines(self):
        pass

    def show_faces(self):
        pass

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
