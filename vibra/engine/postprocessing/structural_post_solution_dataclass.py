import numpy as np
from dataclasses import dataclass, field

@dataclass
class NodalDisplacements:
    displacement_x: dict[int, np.ndarray[tuple[int], complex]] = field(default_factory=dict)
    displacement_y: dict[int, np.ndarray[tuple[int], complex]] = field(default_factory=dict)
    displacement_z: dict[int, np.ndarray[tuple[int], complex]] = field(default_factory=dict)

@dataclass
class NodalStresses:
    sigma_x: dict[int, np.ndarray[tuple[int], complex]] = field(default_factory=dict)
    sigma_y: dict[int, np.ndarray[tuple[int], complex]] = field(default_factory=dict)
    sigma_z: dict[int, np.ndarray[tuple[int], complex]] = field(default_factory=dict)
    tau_xy: dict[int, np.ndarray[tuple[int], complex]] = field(default_factory=dict)
    tau_xz: dict[int, np.ndarray[tuple[int], complex]] = field(default_factory=dict)
    tau_yz: dict[int, np.ndarray[tuple[int], complex]] = field(default_factory=dict)