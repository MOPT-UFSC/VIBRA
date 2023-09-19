from vibra.vibra_file.file_handler import FileHandler

from vibra import __version__
from vibra.engine.mesher.element_type import ElementType
from vibra.engine.mesher.geometry_setup import GeometrySetup
from vibra.engine.mesher.mesh import Mesh
from vibra.engine.mesher.mesh_setup import MeshSetup
from vibra.errors import UnsuportedFileError
from vibra.project import Project
from PIL.PngImagePlugin import PngImageFile


class VibraDecoder(FileHandler):
    def decode(self) -> Project:
        project = Project()
        self._read_header(project)
        self._read_thumbnail(project)
        self._read_mesh(project)
        return project
    
    def get_header(self) -> dict:
        return self._read_json("header.json")

    def get_thumbnail(self) -> PngImageFile | None:
        if not self._path_exists("thumbnail.png"):
            return None

        return self._read_image("thumbnail.png")

    def get_mesh(self) -> Mesh | None:
        if not self.mesh_exists():
            return None

        mesh = Mesh()
        mesh.generated_mesh = True
        mesh_info = self._read_json("mesh/mesh_info.json")
        mesh.dimension = mesh_info["dimension"]
        mesh.entity_ranges = mesh_info["entity_ranges"]
        mesh.element_type = ElementType(**mesh_info["element_type"])

        if "geometry_setup" in mesh_info:
            mesh.geometry_setup = GeometrySetup(**mesh_info["geometry_setup"])

        if "mesh_setup" in mesh_info:
            mesh.mesh_setup = mesh_info["mesh_setup"]
            mesh.mesh_setup["element_type"] = mesh.element_type

        mesh.nodal_coordinates = self._read_array("mesh/nodal_coordinates.dat")
        mesh.lines_connectivity = self._read_array("mesh/lines_connectivity.dat", dtype=int)
        mesh.faces_connectivity = self._read_array("mesh/faces_connectivity.dat", dtype=int)
        mesh.solids_connectivity = self._read_array("mesh/solids_connectivity.dat", dtype=int)

        return mesh

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

    def _read_header(self, project):
        header = self.get_header()
        project.name = header["name"]

    def _read_thumbnail(self, project):
        project.thumbnail = self.get_thumbnail()

    def _read_mesh(self, project):
        project.model.mesh = self.get_mesh()
        project.model.mesh_setup = project.model.mesh.mesh_setup

    def _read_properties(self, project):
        data = self._read_json("model/properties.json")
        project.model.properties.global_properties = data["global_properties"]
        project.model.properties.volume_properties = data["volume_properties"]
        project.model.properties.surface_properties = data["surface_properties"]
        project.model.properties.line_properties = data["line_properties"]
        project.model.properties.element_properties = data["element_properties"]
        project.model.properties.nodal_properties = data["nodal_properties"]
