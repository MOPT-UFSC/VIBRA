import logging
from pathlib import Path

import gmsh
import numpy as np

from vibra.engine.mesher.mesh import Mesh
from vibra.utils.time_utils import context_timer, function_timer

logger = logging.getLogger(__name__)


class MeshReader:
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

        logging.info("Loading mesh data... [25/100]")
        gmsh.open(str(self.path))

        logging.info("Loading mesh data... [90/100]")
        gmsh.model.occ.synchronize()

        mesh = Mesh()
        mesh.geometry_imported = False

        self.bla()

        logging.info("Post-processing mesh... [50/100]")
        with context_timer("foo"):
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

    @function_timer
    def bla(self):
        indices, coords, _parametric_coords = gmsh.model.mesh.get_nodes(includeBoundary=True)
        indices = np.array(indices) - 1
        coords = np.array(coords)

        nodal_coordinates = np.zeros((np.max(indices) + 1, 4))
        nodal_coordinates[indices, 1:] = coords.reshape(-1, 3)
        nodal_coordinates[indices, :1] = indices.reshape(-1, 1)

        for el_type, el_indices, el_nodes in zip(*gmsh.model.mesh.get_elements()):
            _name, dim, _order, nodes_per_element, _, _ = gmsh.model.mesh.get_element_properties(el_type)

            el_indices = np.array(el_indices).reshape(-1, 1)
            el_nodes = np.array(el_nodes).reshape(-1, nodes_per_element)
            el_types = np.full(el_indices.size, el_type)
            el_sizes = np.full(el_indices.size, nodes_per_element)

            print(dim)
