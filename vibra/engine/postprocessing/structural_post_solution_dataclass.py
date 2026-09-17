import numpy as np
from dataclasses import dataclass, field

@dataclass
class NodalDisplacements:
    displacement_x: dict[int, np.ndarray[tuple[int], complex]] = field(default_factory=dict)
    displacement_y: dict[int, np.ndarray[tuple[int], complex]] = field(default_factory=dict)
    displacement_z: dict[int, np.ndarray[tuple[int], complex]] = field(default_factory=dict)

@dataclass
class NodalStresses:
    sigma_x: np.ndarray
    sigma_y: np.ndarray
    sigma_z: np.ndarray
    tau_xy: np.ndarray
    tau_xz: np.ndarray
    tau_yz: np.ndarray