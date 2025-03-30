import numpy as np
from collections import defaultdict

from pathlib import Path

labels = [
          "input_face",
          "output_face"
          ]

class LoadExternalData:
    def __init__(self, path: str, fluid_density: float):
        self.folder_path = Path(path)
        self.fluid_density = fluid_density

    def get_frequencies(self):
        path = self.folder_path / "analysis_frequencies.dat"
        return np.loadtxt(path)

    def load_nodal_pressures(self):

        output_data = dict()

        paths = [
                self.folder_path / "nodal_pressure_input_face.dat",
                self.folder_path / "nodal_pressure_output_face.dat"
                ]

        frequencies = self.get_frequencies()

        for i, path in enumerate(paths):

            data = np.loadtxt(path)
            rows, cols = data.shape
            # print(labels[i], data.shape)
            
            node_ids = data[:, 0]
            array_pressures = np.zeros((rows, len(frequencies) + 1), dtype=complex)

            array_pressures[:, 0] = node_ids
            array_pressures[:, 1:] = data[:, 1::2] + 1j * data[:, 2::2]
            
            dict_pressures = dict(zip(node_ids, array_pressures[:, 1:]))
            output_data[labels[i]] = [frequencies, array_pressures, dict_pressures]

        return output_data

    def load_particle_velocities(self):

        output_data = dict()

        paths = [
                self.folder_path / "particle_velocity_input_face.dat",
                self.folder_path / "particle_velocity_output_face.dat"
                ]

        frequencies = self.get_frequencies()

        den = (-1j * 2 * np.pi * frequencies * self.fluid_density)
        den = 1

        for i, path in enumerate(paths):

            data = np.loadtxt(path)
            rows, cols = data.shape
            # print(labels[i], data.shape)
            node_ids = data[:, 0]

            array_Vx = np.zeros((rows, len(frequencies) + 1), dtype=complex)
            array_Vy = np.zeros((rows, len(frequencies) + 1), dtype=complex)
            array_Vz = np.zeros((rows, len(frequencies) + 1), dtype=complex)

            array_Vx[:, 0] = node_ids
            array_Vx[:, 1:] = (data[:, 1::6] + 1j * data[:, 2::6]) / den
            dict_Vx = dict(zip(node_ids, array_Vx[:, 1:]))

            array_Vy[:, 0] = node_ids
            array_Vy[:, 1:] = (data[:, 3::6] + 1j * data[:, 4::6]) / den
            dict_Vy = dict(zip(node_ids, array_Vy[:, 1:]))

            array_Vz[:, 0] = node_ids
            array_Vz[:, 1:] = (data[:, 5::6] + 1j * data[:, 6::6]) / den
            dict_Vz = dict(zip(node_ids, array_Vz[:, 1:]))

            output_data["Vx", labels[i]] = [frequencies, array_Vx, dict_Vx]
            output_data["Vy", labels[i]] = [frequencies, array_Vy, dict_Vy]
            output_data["Vz", labels[i]] = [frequencies, array_Vz, dict_Vz]

        return output_data

    def load_nodal_area(self):

        output_data = dict()

        paths = [
                self.folder_path / "nodal_area_input_face.dat",
                self.folder_path / "nodal_area_output_face.dat",
                # self.folder_path / "cmsel_neigh/nodal_area_input_face.dat",
                # self.folder_path / "cmsel_neigh/nodal_area_output_face.dat"
                ]

        for i, path in enumerate(paths):

            data = np.loadtxt(path)
            rows, cols = data.shape
            # print(labels[i], data.shape)
            node_ids = data[:, 0]

            array_nodal_area = np.zeros((rows, 2), dtype=float)
            array_nodal_area[:, 0] = data[:, 0]
            array_nodal_area[:, 1] = data[:, 1]

            dict_nodal_area = dict(zip(node_ids, array_nodal_area[:, 1:]))

            output_data[labels[i]] = [array_nodal_area, dict_nodal_area]

        return output_data


if __name__ == "__main__":

    path = Path("data/validation/transmission_loss/results/Zo_real")
    # path = Path("data/validation/transmission_loss/results/Zo_complex")

    ext_data = LoadExternalData(path)

    ext_data.load_nodal_area()
    ext_data.load_nodal_pressures()
    ext_data.load_particle_velocities()