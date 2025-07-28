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

    def get_data(self):
        return [self.c1, self.c2, self.c3, self.c4, self.c5,
                self.c6, self.c7, self.c8, self.flow_resistivity]
