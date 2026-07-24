import numpy as np
from dataclasses import dataclass, field


@dataclass
class NodalParticleVelocities:
    Vx: dict[int, np.ndarray[tuple[int], complex]] = field(default_factory=dict)
    Vy: dict[int, np.ndarray[tuple[int], complex]] = field(default_factory=dict)
    Vz: dict[int, np.ndarray[tuple[int], complex]] = field(default_factory=dict)
    Vn: dict[int, np.ndarray[tuple[int], complex]] = field(default_factory=dict)
    nodal_normals: dict[int, np.ndarray[tuple[int], complex]] = field(default_factory=dict)

    def reset_attributes(self):
        self.Vx.clear()
        self.Vy.clear()
        self.Vz.clear()
        self.Vn.clear()
        self.nodal_normals.clear()

    def Vx_array(self) -> np.ndarray:
        order_indexes = np.argsort(list(self.Vx.keys()))
        return np.array(list(self.Vx.values()), dtype=complex)[order_indexes, :]

    def Vy_array(self) -> np.ndarray:
        order_indexes = np.argsort(list(self.Vy.keys()))
        return np.array(list(self.Vy.values()), dtype=complex)[order_indexes, :]

    def Vz_array(self) -> np.ndarray:
        order_indexes = np.argsort(list(self.Vz.keys()))
        return np.array(list(self.Vz.values()), dtype=complex)[order_indexes, :]

    def Vn_array(self) -> np.ndarray:
        order_indexes = np.argsort(list(self.Vn.keys()))
        return np.array(list(self.Vn.values()), dtype=complex)[order_indexes, :]