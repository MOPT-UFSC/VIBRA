from dataclasses import dataclass
from configparser import ConfigParser
from pathlib import Path


user_config_path = Path(".config.ini")


@dataclass
class UserConfig:
    version: tuple = "0.0.0"
    theme: str = "dark"

    def __post_init__(self):
        self.config = ConfigParser()
        self.config.add_section("info")
        self.config.add_section("appearance")

        if user_config_path.exists():
            self.load()
        else:
            self.save()

    def load(self):
        self.config.read(user_config_path)
        self.version = self.config.get("info", "version", fallback=self.version)
        self.theme = self.config.get("appearance", "theme", fallback=self.theme)

    def save(self):
        self.config.set("info", "version", self.version)
        self.config.set("appearance", "theme", self.theme)

        with open(user_config_path, "w") as file:
            self.config.write(file)