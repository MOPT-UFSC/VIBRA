from pathlib import Path
import json

from vibra.interface.user_preferences import UserPreferences

from molde.colors import Color


class Config:

    def __init__(self):
        self.config_path = Path().home() / "vibra_config.json"
        self.user_preferences = UserPreferences()

        self.load_config_file()

    def load_config_file(self):
        try:
            with open(self.config_path, "r") as file:
                user_preferences = json.load(file)

                self.user_preferences.interface_theme = user_preferences["interface_theme"]
                self.user_preferences.renderer_background_color_1 = Color(*user_preferences["renderer_background_color_1"])
                self.user_preferences.renderer_background_color_2 = Color(*user_preferences["renderer_background_color_2"])
                self.user_preferences.nodes_points_color = Color(*user_preferences["nodes_points_color"])
                self.user_preferences.lines_color = Color(*user_preferences["lines_color"])
                self.user_preferences.edges_color = Color(*user_preferences["edges_color"])
                self.user_preferences.tubes_color = Color(*user_preferences["tubes_color"])
                self.user_preferences.renderer_font_color = Color(*user_preferences["renderer_font_color"])
                self.user_preferences.renderer_font_size = user_preferences["renderer_font_size"]
                self.user_preferences.show_reference_scale_bar = user_preferences["show_reference_scale_bar"]
                self.user_preferences.color_map = user_preferences["color_map"]
        except:
            self._write_config_file()
    
    def _write_config_file(self):
        data = { 
        "interface_theme" : self.user_preferences.interface_theme,
        "renderer_background_color_1" : self.user_preferences.renderer_background_color_1.to_rgb(),
        "renderer_background_color_2" : self.user_preferences.renderer_background_color_2.to_rgb(),
        "nodes_points_color" : self.user_preferences.nodes_points_color.to_rgb(),
        "lines_color" : self.user_preferences.lines_color.to_rgb(),
        "edges_color" : self.user_preferences.edges_color.to_rgb(),
        "tubes_color" : self.user_preferences.tubes_color.to_rgb(),
        "renderer_font_color" : self.user_preferences.renderer_font_color.to_rgb(),
        "renderer_font_size" : self.user_preferences.renderer_font_size,
        "show_reference_scale_bar" : self.user_preferences.show_reference_scale_bar,
        "color_map" : self.user_preferences.color_map
        }
        
        self.write_data_in_file(data)

    def update_config_file(self):
        data = self.get_config_data()

        data["interface_theme"] = self.user_preferences.interface_theme
        data["renderer_background_color_1"] = self.user_preferences.renderer_background_color_1.to_rgb()
        data["renderer_background_color_2"] = self.user_preferences.renderer_background_color_2.to_rgb()
        data["nodes_points_color"] = self.user_preferences.nodes_points_color.to_rgb()
        data["lines_color"] = self.user_preferences.lines_color.to_rgb()
        data["tubes_color"] = self.user_preferences.tubes_color.to_rgb()
        data["renderer_font_color"] = self.user_preferences.renderer_font_color.to_rgb()
        data["renderer_font_size"] = self.user_preferences.renderer_font_size
        data["show_open_pulse_logo"] = self.user_preferences.show_open_pulse_logo
        data["show_reference_scale_bar"] = self.user_preferences.show_reference_scale_bar
        data["color_map"] = self.user_preferences.color_map

        self.write_data_in_file(data)