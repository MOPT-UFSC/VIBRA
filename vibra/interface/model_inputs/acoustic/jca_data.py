from dataclasses import dataclass, fields


@dataclass
class JCAData:
    porosity: float
    tortuosity: float
    viscous_characteristic_length: float    
    thermal_characteristic_length: float
    flow_resistivity: float
    model: str

    def get_data(self) -> dict:
        data = dict()
        for attr, value in self.__dict__.items():
            data[attr] = value
        
        return data

    def get_parameters_position(self) -> dict:
        parameters = dict()

        for index, field in enumerate(fields(JCAData)):
            parameters[index] = field.name

        return parameters

    def __str__(self) -> str:
        string = ""
        for attr, value in self.__dict__.items():
           string += attr + ": " + str(value) + " "
        
        return string

    @classmethod
    def set_data(cls, data: dict) -> "JCAData":
        if "values" in data.keys():
            data.pop("values")

        return JCAData(**data)