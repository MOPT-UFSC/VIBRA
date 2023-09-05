from dataclasses import dataclass, field, asdict
from pathlib import Path
import json
import logging

user_config_path = Path(".config.ini")


@dataclass
class UserConfig:
    version: tuple = "0.0.0"
    theme: str = "dark"
    menu_items_visible: bool = True
    recent_files: list = field(default_factory=list)

    @classmethod
    def load(cls):
        path = Path(".config.json")

        if not path.exists():
            return cls()

        try:
            with open(".config.json", "r") as file:
                data = json.load(file)
            return cls(**data)
        except json.decoder.JSONDecodeError as e:
            logging.error(e)
            return cls()

    def save(self):
        with open(".config.json", "w") as file:
            json.dump(asdict(self), file, indent=2)

    def add_recent_file(self, path):
        '''
        Puts the path in the top of the stack.
        If it already exists remove previous instance.

        Here we need to store the path as a string to make
        it is easier to serialize.
        It is not a problem because it is a local configuration 
        file that will not be transfered to anywhere.
        '''

        self.remove_recent_file(str(path))
        self.recent_files.append(str(path))
        while len(self.recent_files) > 5:
            self.recent_files.pop(0)

    def remove_recent_file(self, path):
        if path in self.recent_files:
            self.recent_files.remove(str(path))