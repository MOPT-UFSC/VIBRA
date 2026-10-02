from copy import deepcopy
from pathlib import Path

from vibra.engine.mesher.element_setup import GMSH_VISUAL_MESH
from vibra.engine.mesher.mesh import Mesh
from vibra.engine.mesher.mesh_setup import MeshSetup
from vibra.errors import IncompleteSetupError, InvalidGeometryError


class GmshMesher:
    def __init__(self, path: str | Path | None = None):
        self.setup = MeshSetup()
        self.path: Path | None = None

        if path is not None:
            self.set_path(path)

    def set_path(self, path: str | Path):
        self.path = Path(path).expanduser()

    def set_mesh_setup(self, setup: MeshSetup):
        self.setup = setup

    def generate(self, threads: int = 0) -> Mesh:
        if self.path is None:
            message = "Geometry not defined"
            context = (
                "The geometry file has not been defined yet."
                "Import a supported CAD file format to proceed."
                "\n\n"
                "Suported file formats: *.iges and *.step"
            )
            raise IncompleteSetupError(message, context=context)

        return Mesh().load_cad(
            self.path,
            deepcopy(self.setup),
            threads,
        )

    def generate_visual_mesh(self) -> tuple[Mesh, MeshSetup]:
        if self.path is None:
            context = (
                "Geometry not defined\n\n"
                "The geometry file has not been defined yet.\n"
                "Import a supported CAD file format to proceed.\n\n"
                "Suported file formats: *.iges and *.step"
            )
            raise InvalidGeometryError(context)

        mesh = Mesh()
        element_size = mesh.compute_initial_mesh_size(str(self.path))
        exception = None

        for _min, _max in [(element_size * 0.4, element_size), (5, 10)]:
            try:
                mesh_setup = MeshSetup(
                    minimum_element_size=_min,
                    maximum_element_size=_max,
                    custom_element_setup=GMSH_VISUAL_MESH,
                )
                mesh.load_cad(self.path, mesh_setup)
            except Exception as error:
                exception = error
            else:
                return mesh, mesh_setup

        raise exception
