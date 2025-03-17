from dataclasses import dataclass

from molde.colors import Color, color_names

@dataclass
class UserPreferences:
    interface_theme: str = "light"
    renderer_background_color_1: Color =  Color("#8092A6")
    renderer_background_color_2: Color = Color("#EEF2F3")
    nodes_points_color: Color = Color("#FFB432")
    lines_color: Color = color_names.BLACK
    edges_color: Color = color_names.BLACK
    faces_color: Color = color_names.WHITE
    renderer_font_color: Color = color_names.BLACK
    renderer_font_size: int  = 12
    points_size: int = 15
    nodes_size: int = 10
    lines_thickness: int = 5
    edges_thickness: int = 1
    show_reference_scale_bar: bool = True
    color_map: str = "jet"

    def set_light_theme(self):
        self.interface_theme = "light"
        self.renderer_background_color_1 = Color("#8092A6")
        self.renderer_background_color_2 = Color("#EEF2F3")
        self.renderer_font_color = Color("#111111")
        self.nodes_points_color = Color("#FFB432")
        self.lines_color = color_names.BLACK
        self.edges_color = color_names.BLACK
        self.faces_color = color_names.WHITE
        self.renderer_font_color = color_names.BLACK
    
    def set_dark_theme(self):
        self.interface_theme = "dark"
        self.renderer_background_color_1 = Color("#0b0f17")
        self.renderer_background_color_2 = Color("#3e424d")
        self.renderer_font_color = Color("#CCCCCC")
        self.nodes_points_color = Color("#FFB432")
        self.lines_color = color_names.BLACK
        self.edges_color = color_names.BLACK
        self.faces_color = color_names.WHITE
        self.renderer_font_color = color_names.WHITE
    
    def reset_sizes(self):
        self.renderer_font_size = 12
        self.points_size: int = 15
        self.nodes_size: int = 10
        self.lines_thickness: int = 5
        self.edges_thickness: int = 1
    
    def reset_reference_scale_bar(self):
        self.show_reference_scale_bar = True

    def get_attributes(self):
        attributes = dict()
        for attr, value in self.__dict__.items():
            attributes[attr] = value

        return attributes