from dataclasses import dataclass, fields

@dataclass
class RectangularDuctData:
    section_type: str
    formulation: str
    height: float
    width: float
    number_of_terms: int

    def get_data(self) -> dict:
        data = dict()
        for attr, value in self.__dict__.items():
            data[attr] = value
        
        return data

    def get_parameters_position(self) -> dict:
        parameters = dict()

        for index, field in enumerate(fields(RectangularDuctData)):
            parameters[index] = field.name

        return parameters

    def __str__(self) -> str:
        string = ""
        for attr, value in self.__dict__.items():
           string += attr + ": " + str(value) + " "
        
        return string


    @classmethod
    def set_data(self, data: dict) -> "RectangularDuctData":
        if "values" in data:
            data.pop("values")
        
        if "model_id" in data:
            data.pop("model_id")

        return RectangularDuctData(**data)