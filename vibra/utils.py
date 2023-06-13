from dataclasses import dataclass
import numpy as np

def lerp(a, b, t):
    return (a +(b-a)*t)

def distance_points(bounds):
    x0,x1,y0,y1,z0,z1 = bounds
    return (np.sqrt((x1-x0)**2 + (y1-y0)**2 + (z1-z0)**2))


@dataclass
class ProgressStatus:
    step: int
    max_steps: int
    message: str = ""

    def __str__(self):
        return f"{self.message} {self.step}/{self.max_steps}"

    def __radd__(self, lhs):
        self.message = str(lhs)
        return self
