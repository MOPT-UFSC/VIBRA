from pathlib import Path

import h5py

from vibra.engine.mesher.mesh import Mesh
import numpy as np


class ExternalSimulator:
    def __init__(self, vibra_data_path: str | Path):
        self.vibra_data_path = Path(vibra_data_path)

        self.simulate()

    def simulate(self):
        mesh = self._load_mesh(self.vibra_data_path / "mesh_data.hdf5")
        print(mesh.solids_connectivity)
    
    def _load_mesh(self, mesh_filepath: str | Path) -> Mesh:
        mesh_filepath = Path(mesh_filepath)

        if not mesh_filepath.exists():
            raise FileExistsError("The mesh file is missing.")
        
        mesh = Mesh()

        with h5py.File(mesh_filepath, "r") as file:
            mesh.nodal_coordinates = np.array(file["nodal_data"]["nodal_coordinates"])
            mesh.lines_connectivity = np.array(file["connectivity"]["lines_connectivity"])
            mesh.faces_connectivity = np.array(file["connectivity"]["faces_connectivity"])
            mesh.solids_connectivity = np.array(file["connectivity"]["solids_connectivity"])

        mesh.process_upwards_adjacencies_from_entities()
        mesh.process_mesh_related_mappings()

        return mesh

if __name__ == "__main__":
    ExternalSimulator("/home/vini/temp_vibra/")