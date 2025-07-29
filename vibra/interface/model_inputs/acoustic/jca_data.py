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
        return {"porosity": self.porosity, "tortuosity": self.tortuosity, 
                "viscous_characteristic_length": self.viscous_characteristic_length, 
                "thermal_characteristic_length": self.thermal_characteristic_length, 
                "flow_resistivity": self.flow_resistivity, "model": self.model}

    @classmethod
    def set_data(cls, data: dict) -> "JCAData":
        if "values" in data.keys():
            data.pop("values")

        return JCAData(**data)