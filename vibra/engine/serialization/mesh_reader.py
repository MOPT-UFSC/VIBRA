import logging
from pathlib import Path

import gmsh
import numpy as np

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
        self._process_adjacencies(mesh)

        gmsh.finalize()

        logger.info(
            f"The mesh file contains {len(mesh.nodal_coordinates)} nodes"
            f", {len(mesh.lines_connectivity)} dim 1"
            f", {len(mesh.faces_connectivity)} dim 2"
            f"and {len(mesh.solids_connectivity)} dim 3 elements"
        )

        return mesh

    def _process_adjacencies(self, mesh: Mesh):
        """
        This method processes the downwards adjacencies from entities
        from the solids, faces and lines connectivities matrices.
        """

        e_nodes_2d = mesh.faces_connectivity[0, 4:].size
        for vol_id in mesh.geometry_information.get("volumes"):
            nodes_from_volume = mesh.get_nodes_from_volume(vol_id)
            if nodes_from_volume is None:
                continue

            mask = np.sum(np.isin(mesh.faces_connectivity[:, 4:], nodes_from_volume), axis=1) == e_nodes_2d
            mesh.surfaces_from_volume[vol_id] = [int(tag) for tag in set(mesh.faces_connectivity[mask, 1])]

        if mesh.lines_connectivity.size:
            e_nodes_1d = mesh.lines_connectivity[0, 4:].size
            for surf_id in mesh.geometry_information.get("surfaces"):
                nodes_from_surface = mesh.get_nodes_from_surface(surf_id)
                if nodes_from_surface is None:
                    continue

                mask = (
                    np.sum(
                        np.isin(mesh.lines_connectivity[:, 4:], nodes_from_surface),
                        axis=1,
                    )
                    == e_nodes_1d
                )
                mesh.lines_from_surface[surf_id] = [int(tag) for tag in set(mesh.lines_connectivity[mask, 1])]

        mesh.process_lines_from_mesh_data()
        mesh.process_lines_connectivitiy_from_mesh_data()
        mesh.process_points_from_mesh_data()
        mesh.process_upwards_adjacencies()
