from dataclasses import dataclass, fields


@dataclass
class DelanyBazleyMikiData:
    model: str # "Delany-Bazley" |  "Delany-Bazley-Miki" | "User-defined (DBM)"
    C1: float
    C2: float
    C3: float
    C4: float
    C5: float
    C6: float
    C7: float
    C8: float
    flow_resistivity: float
    normalize_flow_resistivity: bool = False

    def get_data(self) -> dict:
        data = {}
        for attr, value in self.__dict__.items():
            data[attr] = value

        return data

    def get_parameters_position(self) -> dict:
        parameters = {}

        for index, field in enumerate(fields(DelanyBazleyMikiData)):
            parameters[index] = field.name

        return parameters
    
    def __str__(self) -> str:
        string = ""
        for attr, value in self.__dict__.items():
           string += attr + ": " + str(value) + " "
        
        return string
    
    @classmethod
    def set_data(cls, data: dict) -> "DelanyBazleyMikiData":
        if "values" in data:
            data.pop("values")

        return DelanyBazleyMikiData(**data)