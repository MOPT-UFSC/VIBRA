from zipfile import ZipFile
from pathlib import Path
from io import BytesIO, StringIO
import json
from PIL import Image
from PIL.PngImagePlugin import PngImageFile

from vibra.project import Project
from vibra.engine.mesher.mesh import Mesh
from vibra.engine.mesher.mesh_setup import MeshSetup
from vibra.errors import UnsuportedFileError
from vibra import __version__
from vibra.engine.mesher.element_type import ElementType
from vibra.file.custom_json_decoder import CustomJsonDecoder
from vibra.file.custom_json_encoder import CustomJsonEncoder

from dataclasses import asdict
import numpy as np


class VibraFile:
    '''
    Reads and writes data to vibra files.
    The methods of this class are separated in three main parts:
        - Getters (Read data directly from the file)
        - Writers (Write data from a project into the file)
        - Readers (Read data from the file and inserts into the project)
    '''
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

    def write(self, project):
        self._write_header(project)
        self._write_thumbnail(project)
        self._write_geometry(project)
        self._write_mesh(project)

    def read(self, project):
        project = Project()
        self._read_header(project)
        self._read_thumbnail(project)
        self._read_geometry(project)
        self._read_mesh(project)

    # GETTERS
    def get_header(self) -> dict:
        return self._read_json("header.json")

    def get_thumbnail(self) -> PngImageFile | None:
        if not self._path_exists("thumbnail.png"):
            return None

        data = BytesIO(self._read_string("thumbnail.png"))
        return Image.open(data)

    def get_mesh(self) -> Mesh | None:            
        if not self.mesh_exists():
            return None
        
        mesh_info = self._read_json("mesh/mesh_info.json")
        mesh_info["nodal_coordinates"] = self._read_array("mesh/nodal_coordinates.dat")
        mesh_info["lines_connectivity"] = self._read_array("mesh/lines_connectivity.dat", dtype=int)
        mesh_info["faces_connectivity"] = self._read_array("mesh/faces_connectivity.dat", dtype=int)
        mesh_info["solids_connectivity"] = self._read_array("mesh/solids_connectivity.dat", dtype=int)
        return mesh_info

    def get_geometry(self) -> str:
        mesh_info = self._read_json("mesh/mesh_info.json")
        return mesh_info["geometry_setup"]
    
    def mesh_exists(self) -> bool:
        needed_paths = [
            "mesh/nodal_coordinates.dat",
            "mesh/lines_connectivity.dat",
            "mesh/faces_connectivity.dat",
            "mesh/solids_connectivity.dat",
        ]
        return all(self._path_exists(path) for path in needed_paths)

    # WRITER
    def _write_header(self, project):
        pass

    def _write_thumbnail(self, project):
        pass

    def _write_geometry(self, project):
        pass

    def _write_mesh(self, project):
        pass

    # READER
    def _read_header(self, project):
        pass

    def _read_thumbnail(self, project):
        pass

    def _read_geometry(self, project):
        pass

    def _read_mesh(self, project):
        pass

    # USEFULL
    def _path_exists(self, path: str) -> bool:
        file_paths = [member.filename for member in self.zip.infolist()]
        return path in file_paths

    def _write_string(self, arcname, data):
        self.zip.writestr(arcname, data)

    def _read_string(self, arcname):
        return self.zip.read(arcname)

    def _write_json(self, arcname, data):
        json_data = json.dumps(data, indent=2)
        self._write_string(arcname, json_data, cls=CustomJsonEncoder)

    def _read_json(self, arcname):
        data = self._read_string(arcname)
        json_data = json.loads(data, cls=CustomJsonDecoder)
        return dict(json_data)

    def _write_array(self, arcname, data, *args, delimiter=";", **kwargs):
        file = BytesIO()
        np.savetxt(file, data, *args, delimiter=delimiter, **kwargs)
        self._write_string(arcname, file.getvalue().decode())

    def _read_array(self, arcname, *args, delimiter=";", **kwargs):
        data = self._read_string(arcname)
        file = BytesIO(data)
        return np.loadtxt(file, *args, delimiter=delimiter, **kwargs)
