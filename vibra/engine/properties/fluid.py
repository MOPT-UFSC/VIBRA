from dataclasses import dataclass


@dataclass
class Fluid:
    name: str
    identifier: int
    color: str
    fluid_density: float
    speed_of_sound: float
    isentropic_exponent: float = 0.0
    thermal_conductivity: float = 0.0
    specific_heat_Cp: float = 0.0
    dynamic_viscosity: float = 0.0
    temperature: float = 0.0
    pressure: float = 0.0

    @property
    def impedance(self):
        return self.fluid_density*self.speed_of_sound