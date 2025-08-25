import json
from configparser import ConfigParser
from pathlib import Path

from PIL import Image


def read_json(path: Path) -> dict | None:
    if path.exists():
        with open(path) as f:
            return json.load(f)


def write_json(path: Path, data: dict):
    with open(path, "w") as json_file:
        json.dump(data, json_file, indent=4)


def read_config(path: Path) -> ConfigParser | None:
    if path.exists():
        with open(path) as f:
            config_string = f.read()
            config = ConfigParser()
            config.read_string(config_string)
            return config


def write_config(path: Path, config: ConfigParser):
    with open(path, 'w') as config_file:
        config.write(config_file)


def read_image(path: Path) -> Image.Image | None:
    if path.exists():
        return Image.open(path)


def write_image(path: Path, image: Image.Image):
    image.save(path)
