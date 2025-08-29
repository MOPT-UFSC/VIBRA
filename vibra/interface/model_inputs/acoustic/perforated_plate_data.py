from vibra.engine.properties.fluid import Fluid

from dataclasses import dataclass, fields, asdict
import numpy as np


@dataclass
class PerforatedPlateData:
    coupling_type: str = None
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

        for attr, value in self.__dict__.items():
            if value is not None:
                data[attr] = value
        
        return data
    
    def get_data_to_fill_edit_table_widget(self) -> list:
        data = list()

        for attr, value in self.__dict__.items():
            if attr in ["fluid", "formulation", "coupling_type"]:
                continue
            
            if value is None:
                value = "---"

            data.append(value)
    
        return data

    def get_fluid_data_to_fill_edit_table_widget(self) -> list:
        return [self.fluid.name, self.fluid.fluid_density, 
                self.fluid.speed_of_sound]

    def get_indexed_attributes(self) -> dict:
        indexed_attr = dict()

        for index, attr in enumerate(self.__dict__):
            indexed_attr[index] = attr

        return indexed_attr

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
