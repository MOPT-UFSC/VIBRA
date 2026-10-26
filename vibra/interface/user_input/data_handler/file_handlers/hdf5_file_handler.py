from dataclasses import dataclass
from pathlib import Path

import h5py
import numpy as np

from vibra.interface.user_input.data_handler.file_handlers.io_handler import IOHandler
from vibra.interface.user_input.data_handler.imported_data import SimulationData


@dataclass
class AcousticImpedanceData:
    path: str | Path | None = None
    nodal_coordinates: np.ndarray | None = None
    nodal_pressures: np.ndarray | None = None
    normal_particle_velocities: np.ndarray | None = None


class HDF5FileHandler(IOHandler):

    EXTENSIONS = [".h5", ".hd5", ".hdf5"]

    @staticmethod
    def read(file_path: Path) -> SimulationData:
        simulation_data = SimulationData(file_path)

        with h5py.File(file_path, 'r') as hf:

            # Read key data
            nodal_data = hf.get("nodal_data")
            variables = hf.get("variables")
            metadata = hf.get("metadata")

            # Save the nodal coordinates matrix
            simulation_data.nodal_area = np.array(nodal_data.get("nodal_area"), dtype=float)
            simulation_data.nodal_coordinates = np.array(nodal_data.get("coords"), dtype=float)

            # Save other attributes
            for attr_key in metadata.attrs:
                setattr(simulation_data, attr_key, metadata.attrs[attr_key])

            # Calculate the start point from last revolution
            delta_theta = metadata.attrs["delta_theta"]
            steps_per_rev = int(360 / delta_theta)
            start = steps_per_rev + 1

            # filter the last revolution data for metadata
            for key, values in metadata.items():
                setattr(simulation_data, key, values[-start:])

            # filter the last revolution data for variables
            for key, values in variables.items():
                setattr(simulation_data, key, values[:, -start:])

        return simulation_data


    @staticmethod
    def write_acoustic_impedance_data(acoustic_impedance_data: AcousticImpedanceData):

        with h5py.File(acoustic_impedance_data.path, 'w') as file:

            # write data in HDF file
            for key, values in acoustic_impedance_data.__dict__.items():
                if not isinstance(values, np.ndarray):
                    continue

                file[key] = values


    @staticmethod
    def read_acoustic_impedance_data(file_path: Path) -> SimulationData:
        acoustic_impedance_data = AcousticImpedanceData(file_path)

        with h5py.File(file_path, 'r') as file:

            # read data from HDF file
            for key, values in file.items():
                setattr(acoustic_impedance_data, key, values)

        return acoustic_impedance_data