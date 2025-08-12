from dataclasses import dataclass, fields

@dataclass
class CircularDuctData:
    section_type: str
    formulation: str
    diameter: float

    def get_data(self) -> dict:
        data = dict()
        for attr, value in self.__dict__.items():
            data[attr] = value
        
        return data

    def get_parameters_position(self) -> dict:
        parameters = dict()

        for index, field in enumerate(fields(CircularDuctData)):
            parameters[index] = field.name

        return parameters

    def __str__(self) -> str:
        string = ""
        for attr, value in self.__dict__.items():
           string += attr + ": " + str(value) + " "
        
        return string
    
    @classmethod
    def set_data(self, data: dict) -> "CircularDuctData":
        if "values" in data:
            data.pop("values")

        if "model_id" in data:
            data.pop("model_id")

        return CircularDuctData(**data)

