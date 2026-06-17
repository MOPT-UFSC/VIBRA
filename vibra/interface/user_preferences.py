from dataclasses import dataclass, fields

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
    selection_color: Color = Color("#146AF5")
    selection_faces_color: Color = Color("#146AF5")
    selection_nodes_points_color: Color = Color("#F52A14")
    selection_lines_color: Color = Color("#F52A14")
    renderer_font_color: Color = color_names.BLACK
    renderer_font_size: int  = 11
    points_size: int = 15
    nodes_size: int = 10
    lines_thickness: int = 3
    edges_thickness: int = 1
    show_reference_scale_bar: bool = True
    compatibility_mode: bool = False
    run_analysis_in_subprocess: bool = True
    generate_mesh_in_subprocess: bool = True
    color_map: str = "jet"

    def set_light_theme(self):
        self.interface_theme = "light"
        self.renderer_background_color_1 = Color("#8092A6")
        self.renderer_background_color_2 = Color("#EEF2F3")
        self.renderer_font_color = color_names.BLACK
        self.nodes_points_color = Color("#FFB432")
        self.lines_color = color_names.BLACK
        self.edges_color = color_names.BLACK
        self.faces_color = color_names.WHITE
        self.selection_faces_color = Color("#146AF5")
        self.selection_nodes_points_color = Color("#F52A14")
        self.selection_lines_color = Color("#F52A14")

    def set_dark_theme(self):
        self.interface_theme = "dark"
        self.renderer_background_color_1 = Color("#0b0f17")
        self.renderer_background_color_2 = Color("#3e424d")
        self.renderer_font_color = color_names.WHITE
        self.nodes_points_color = Color("#FFB432")
        self.lines_color = color_names.BLACK
        self.edges_color = color_names.BLACK
        self.faces_color = color_names.WHITE
        self.selection_faces_color: Color = Color("#146AF5")
        self.selection_nodes_points_color: Color = Color("#F52A14")
        self.selection_lines_color = Color("#F52A14")

    def reset_attributes(self):
        theme = self.interface_theme
        for field in fields(UserPreferences):
            setattr(self, field.name, field.default)
        
        if theme == "dark":
            self.set_dark_theme()
        else:
            self.set_light_theme()

    def get_attributes(self):
        attributes = dict()
        for attr, value in self.__dict__.items():
            attributes[attr] = value

        return attributes
