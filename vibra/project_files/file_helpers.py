import json
from configparser import ConfigParser
from contextlib import contextmanager
from pathlib import Path

import numpy as np
from cffi.pkgconfig import call
from PIL import Image


def read_json(path: Path) -> dict | None:
    path = Path(path)
    if path.exists():
        with open(path) as f:
            return json.load(f)


def write_json(path: Path, data: dict):
    with open(path, "w") as json_file:
        json.dump(data, json_file, indent=4, cls=NumpyCompatibleEncoder)


def read_config(path: Path) -> ConfigParser | None:
    path = Path(path)
    if path.exists():
        with open(path) as f:
            config_string = f.read()
            config = ConfigParser()
            config.read_string(config_string)
            return config


def write_config(path: Path, config: ConfigParser):
    with open(path, "w") as config_file:
        config.write(config_file)


def read_image(path: Path) -> Image.Image | None:
    path = Path(path)
    if path.exists():
        return Image.open(path).copy()


def write_image(path: Path, image: Image.Image):
    image.save(path)


@contextmanager
def update_json(path: Path, default_type: list | dict | None = None):
    """
    Utility function to read and write a file using "with" syntax.
    If the function fails to read the data a configurable default type
    will be returned instead.

    It is supposed to be used as follows:

    ```
    with update_json(path) as file:
        file["y"] = file["x"] + 2
    ```
    """

    data = read_json(path)
    if (data is None) and callable(default_type):
        data = default_type()

    try:
        yield data
    finally:
        if data is not None:
            write_json(path, data)


class NumpyCompatibleEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        return json.JSONEncoder.default(self, obj)
