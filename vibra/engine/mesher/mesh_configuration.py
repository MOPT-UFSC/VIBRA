from dataclasses import dataclass

# please set all the hidden gmsh constants here
DELAUNAY_2D = 0
ALGORITHM_2D = 1
WHATEVER_2D = 2 

DELAUNAY_3D = 0
ALGORITHM_3D = 1
WHATEVER_3D = 2 

@dataclass
class MeshConfiguration:
    name: str
    
    element_size: float
    size_factor: float
    tolerance: float

    algorithm_2d: int
    algorithm_3d: int