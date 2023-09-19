import json
from io import BytesIO
from pathlib import Path
from typing import Any
from zipfile import ZipFile

import numpy as np
from PIL import Image

from vibra import __version__
from vibra.file.custom_json_decoder import CustomJsonDecoder
from vibra.file.custom_json_encoder import CustomJsonEncoder


class FileHandler:
    def __init__(self, path, open_mode="r") -> None:
        self.path = Path(path)
        self.open_mode = open_mode
        self.zip = None

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, *args, **kwargs):
        self.close()

    def open(self):
        self.zip = ZipFile(self.path, self.open_mode)

    def close(self):
        self.zip.close()
        self.zip = None

    def _path_exists(self, path: str) -> bool:
        file_paths = [member.filename for member in self.zip.infolist()]
        return path in file_paths

    def _write_string(self, arcname: str, data: str):
        self.zip.writestr(arcname, data)

    def _read_string(self, arcname: str) -> str:
        return self.zip.read(arcname)

    def _write_json(self, arcname: str, data: Any):
        json_data = json.dumps(data, indent=2, cls=CustomJsonEncoder)
        self._write_string(arcname, json_data)

    def _read_json(self, arcname: str) -> dict:
        data = self._read_string(arcname)
        json_data = json.loads(data, cls=CustomJsonDecoder)
        return dict(json_data)

    def _write_array(self, arcname: str, data: np.ndarray, *args, delimiter=";", **kwargs):
        file = BytesIO()
        np.savetxt(file, data, *args, delimiter=delimiter, **kwargs)
        self._write_string(arcname, file.getvalue().decode())

    def _read_array(self, arcname: str, *args, delimiter=";", **kwargs) -> np.ndarray:
        data = self._read_string(arcname)
        file = BytesIO(data)
        return np.loadtxt(file, *args, delimiter=delimiter, **kwargs)

    def _write_image(self, arcname: str, image: Image, format="PNG"):
        file = BytesIO()
        image.save(file, format)
        self._write_string(arcname, file.getvalue())

    def _read_image(self, arcname: str) -> Image:
        data = self._read_string(arcname)
        file = BytesIO(data)
        return Image.open(file)
