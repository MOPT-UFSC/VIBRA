import logging
from pathlib import Path

import gmsh

from vibra.engine.mesher.gmsh_common import GmshCommon
from vibra.engine.mesher.mesh import Mesh

logger = logging.getLogger(__name__)


class MeshReader(GmshCommon):
    def __init__(self, path: str | Path | None = None):
        self.path: Path | None = None
        if path is not None:
            self.set_path(path)

    def set_path(self, path: str | Path):
        self.path = Path(path).expanduser()

    def read_mesh(self) -> Mesh:
        gmsh.initialize("", False, interruptible=False)
        gmsh.option.setNumber("General.Terminal", 0)
        gmsh.option.setNumber("General.Verbosity", 0)
        gmsh.option.setNumber("General.NumThreads", 0)
        gmsh.option.setNumber("Geometry.Tolerance", 1e-8)

        logger.info("Loading mesh data... [25/100]")
        gmsh.open(str(self.path))

        logger.info("Loading mesh data... [90/100]")
        gmsh.model.occ.synchronize()

        mesh = self._create_mesh_from_gmsh_state()
        mesh.geometry_imported = False

        logger.info("Post-processing mesh... [80/100]")
        self._process_geometry_information(mesh)
        mesh.process_downwards_adjacencies_from_mesh_data()

        logger.info("Post-processing mesh... [90/100]")
        mesh.process_upwards_adjacencies()

        gmsh.finalize()

        logger.info(
            f"The mesh file contains {len(mesh.nodal_coordinates)} nodes"
            f", {len(mesh.lines_connectivity)} dim 1"
            f", {len(mesh.faces_connectivity)} dim 2"
            f"and {len(mesh.solids_connectivity)} dim 3 elements"
        )

        return mesh
