from vibra.vibra_file.file_handler import FileHandler
from vibra import __version__


class VibraEncoder(FileHandler):
    def encode(self, project):
        self._write_header(project)
        self._write_thumbnail(project)
        self._write_mesh(project)

    def _write_header(self, project):
        header = dict(name=project.name, version=(__version__))
        self._write_json("header.json", header)

    def _write_thumbnail(self, project):
        if project.thumbnail is None:
            return
        
        self._write_image(project.thumbnail)

    def _write_mesh(self, project):
        mesh = project.model.mesh
        if mesh is None:
            return

        mesh_info = dict()
        mesh_info["dimension"] = mesh.dimension
        mesh_info["entity_ranges"] = mesh.entity_ranges
        mesh_info["element_type"] = mesh.element_type

        mesh_info["geometry_setup"] = mesh.geometry_setup

        if mesh.mesh_setup is not None:
            mesh_info["mesh_setup"] = mesh.mesh_setup

        self._write_json("mesh/mesh_info.json", mesh_info)
        self._write_array(
            "mesh/nodal_coordinates.dat",
            mesh.nodal_coordinates,
            fmt=["%i", "%.16f", "%.16f", "%.16f"],
        )
        self._write_array("mesh/lines_connectivity.dat", mesh.lines_connectivity, fmt="%i")
        self._write_array("mesh/faces_connectivity.dat", mesh.faces_connectivity, fmt="%i")
        self._write_array("mesh/solids_connectivity.dat", mesh.solids_connectivity, fmt="%i")
