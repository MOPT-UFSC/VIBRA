import json
import logging
from dataclasses import asdict, dataclass, field
from pathlib import Path
from vibra import app
user_config_path = Path(".config.ini")


@dataclass
class UserConfig:
    version: tuple = "0.0.0"
    theme: str = "dark"
    menu_items_visible: bool = True
    recent_files: list = field(default_factory=list)

    @classmethod
    def load(cls):
        obj = cls()

        try:
            preferences = app().config.get_user_preferences()
        except:
            return obj

        theme = preferences.get("interface theme")
        menu_items_visible = preferences.get("menu_items_visible")

        if theme is not None:
            obj.theme = theme

        if menu_items_visible == "True":
            obj.menu_items_visible = True

        return obj

    def save(self):
        try:
            app().config.write_theme_in_file(self.theme)
            app().config.write_menu_items_visible_in_file(self.menu_items_visible)
        except:
            pass

    def add_recent_file(self, path):
        """
        Puts the path in the top of the stack.
        If it already exists remove previous instance.

        Here we need to store the path as a string to make
        it is easier to serialize.
        It is not a problem because it is a local configuration
        file that will not be transfered to anywhere.
        """

        self.remove_recent_file(str(path))
        self.recent_files.append(str(path))
        while len(self.recent_files) > 5:
            self.recent_files.pop(0)

    def remove_recent_file(self, path):
        if path in self.recent_files:
            self.recent_files.remove(str(path))
