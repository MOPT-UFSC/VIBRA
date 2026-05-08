
from dataclasses import dataclass

@dataclass
class HEX8_structural:
    extra_shape_functions: bool = False
    option_2: bool = False
    option_3: bool = False

    def get_data(self) -> dict:
        data = dict()

        for attr, value in self.__dict__.items():
            if value is None:
                continue

            if "option_" in attr:
                continue

            data[attr] = value

        return data

@dataclass
class TET10_structural:
    option_1: bool = False
    option_2: bool = False
    option_3: bool = False