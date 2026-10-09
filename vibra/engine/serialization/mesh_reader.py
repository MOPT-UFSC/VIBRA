import logging
from pathlib import Path

import gmsh

from vibra.engine.mesher.mesh import Mesh

logger = logging.getLogger(__name__)


class MeshReader:
    def __init__(self, path: str | Path | None = None):
        self.path: Path | None = None
        if path is not None:
            self.set_path(path)

    def set_path(self, path: str | Path):
        self.path = Path(path).expanduser()

    def read_mesh(self, path: Path | str) -> Mesh:
        gmsh.initialize("", False, interruptible=False)
        gmsh.option.setNumber("General.Terminal", 0)
        gmsh.option.setNumber("General.Verbosity", 0)
        gmsh.option.setNumber("General.NumThreads", 0)
        gmsh.option.setNumber("Geometry.Tolerance", 1e-8)

        logging.info("Loading mesh data... [25/100]")
        gmsh.open(str(path))

        logging.info("Loading mesh data... [90/100]")
        gmsh.model.occ.synchronize()

        mesh = Mesh()
        mesh.geometry_imported = False

        logging.info("Post-processing mesh... [50/100]")
        mesh.post_process_mesh_data()
        mesh.update_element_topology_based_on_connectivity()

        logging.info("Post-processing mesh... [80/100]")
        mesh.process_downwards_adjacencies_from_mesh_data()

        logging.info("Post-processing mesh... [90/100]")
        mesh.process_upwards_adjacencies_from_entities()

        gmsh.finalize()

        logging.info(
            f"The mesh file contains {len(mesh.nodal_coordinates)} nodes"
            f", {len(mesh.lines_connectivity)} dim 1"
            f", {len(mesh.faces_connectivity)} dim 2"
            f"and {len(mesh.solids_connectivity)} dim 3 elements"
        )

        return mesh
