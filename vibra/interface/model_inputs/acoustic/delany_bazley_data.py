from dataclasses import dataclass, fields


@dataclass
class DelanyBazleyData:
    C1: float
    C2: float
    C3: float
    C4: float
    C5: float
    C6: float
    C7: float
    C8: float
    flow_resistivity: float
    model: str 

    def get_data(self) -> dict:
        data = dict()
        for attr, value in self.__dict__.items():
            data[attr] = value
        
        return data

    def get_parameters_position(self) -> dict:
        parameters = dict()

        for index, field in enumerate(fields(DelanyBazleyData)):
            parameters[index] = field.name

        return parameters
    
    def __str__(self) -> str:
        string = ""
        for attr, value in self.__dict__.items():
           string += attr + ": " + str(value) + " "
        
        return string
    
    @classmethod
    def set_data(cls, data: dict) -> "DelanyBazleyData":
        if "values" in data.keys():
            data.pop("values")
        
        return DelanyBazleyData(**data)

        
