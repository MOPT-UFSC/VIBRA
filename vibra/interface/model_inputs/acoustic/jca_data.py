from dataclasses import dataclass


@dataclass
class JCAData:
    model: str
    porosity: float
    tortuosity: float
    viscous_characteristic_length: float
    thermal_characteristic_length: float
    flow_resistivity: float

    def get_data(self):
        return [self.porosity, self.tortuosity, self.viscous_characteristic_length,
                self.thermal_characteristic_length, self.flow_resistivity]