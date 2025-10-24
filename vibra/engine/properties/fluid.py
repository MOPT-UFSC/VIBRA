from dataclasses import dataclass, asdict

@dataclass
class Fluid:
    name: str = None
    fluid_density: float = 0.0
    speed_of_sound: float = 0.0
    color: tuple = (0, 0, 0)
    identifier: int = 0
    isentropic_exponent: float = 0.0
    thermal_conductivity: float = 0.0
    specific_heat_Cp: float = 0.0
    dynamic_viscosity: float = 0.0
    temperature: float = 0.0
    pressure: float = 0.0
    molar_mass: float = 0.0
    key_mixture: str | None = None
    molar_fractions: list | None = None

    @property
    def impedance(self):
        return self.fluid_density * self.speed_of_sound
    
    @property
    def prandtl_number(self):
        if self.thermal_conductivity != 0:
            return (self.specific_heat_Cp*self.dynamic_viscosity)/self.thermal_conductivity
        else:
            print("Define the fluid thermal conductivity to proceed with the Prandtl number calculation.")
            return None
        
    @property
    def pressure_state(self):
        return self.fluid_density*(self.speed_of_sound**2)/self.isentropic_exponent

    def get_data(self) -> dict:
        return asdict(self)
    
    def get_lrf_properties(self):
        c_0 = self.speed_of_sound
        rho_0 = self.fluid_density
        mu = self.dynamic_viscosity
        gamma = self.isentropic_exponent
        Pr = self.prandtl_number
        P_0 = self.pressure_state
        return c_0, rho_0, mu, gamma, Pr, P_0