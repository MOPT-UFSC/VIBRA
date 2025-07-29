from dataclasses import dataclass


@dataclass
class DelanyBazleyData:
    model: str 
    c1: float
    c2: float
    c3: float
    c4: float
    c5: float
    c6: float
    c7: float
    c8: float
    flow_resistivity: float

    def get_data(self) -> dict:
        return {"c1": self.c1, "c2": self.c2, 
                "c3": self.c3, "c4": self.c4, "c5": self.c5,
                "c6": self.c6, "c7": self.c7, 
                "c8": self.c8, "flow_resistivity": self.flow_resistivity,
                "model": self.model}
    
    @classmethod
    def set_data(cls, data: dict) -> "DelanyBazleyData":
        if "values" in data.keys():
            data.pop("values")
        
        return DelanyBazleyData(**data)
