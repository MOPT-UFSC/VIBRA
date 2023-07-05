from dataclasses import dataclass


@dataclass
class Fluid:
    name: str
    density: float
    speed_of_sound: float
    color: list
