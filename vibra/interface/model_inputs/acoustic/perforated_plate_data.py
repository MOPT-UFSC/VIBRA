from vibra.engine.properties.fluid import Fluid

from dataclasses import dataclass, fields
import numpy as np


@dataclass
class PerforatedPlateData:
    fluid : Fluid = None
    formulation : str = None
    plate_thickness : float = None
    hole_diameter : float = None
    porosity : float = None
    linear_discharge_coefficient : float = None
    include_effects : str = None
    non_linear_discharge_coefficient : float | None = None
    non_linear_correction_factor : float | None = None
    user_defined_transfer_impedance : np.ndarray | None = None
        
    def set_general_data(self, data: dict):
        for field in fields(PerforatedPlateData):
            if field.name in data:
                setattr(self, field.name, data[field.name])
    
    def set_non_linear_data(self, non_linear_discharge_coefficient: float, non_linear_correction_factor: float):
        self.non_linear_discharge_coefficient = non_linear_discharge_coefficient
        self.non_linear_correction_factor = non_linear_correction_factor
    
    def set_user_defined_transfer_impedance(self, user_defined_transfer_impedance: np.ndarray):
        self.user_defined_transfer_impedance = user_defined_transfer_impedance
    
    def get_data(self) -> dict:
        data = dict()

        for attr, value in self.fluid.__dict__.items():
            data[attr] = value

        for attr, value in self.__dict__.items():
            if value is not None and attr != "fluid":
                data[attr] = value
        
        return data
            
    def __str__(self) -> str:
        string = ""
        for attr, value in self.__dict__.items():
           string += attr + ": " + str(value) + " "
        
        return string
    
    @classmethod
    def set_data(cls, data: dict):
        for key in data.copy():
            if key not in cls.__dict__:
                data.pop(key)

        return PerforatedPlateData(**data)
