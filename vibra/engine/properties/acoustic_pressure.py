import numpy as np
from dataclasses import dataclass, field

from pathlib import Path


@dataclass
class AcousticPressure:
    real: list[float]
    imaginary: list[float]
    # postpones the creation of this attribute
    values: list = field(default_factory=list)

    # def __add__(self, other):
    #     ...

    # __radd__ = __add__

    def to_dict(self) -> dict[str, list[float] | list[complex]]:
        return dict(
            real_values=self.real,
            imag_values=self.imaginary,
            values=list(map(complex, self.real, self.imaginary))
        )
 
    @classmethod
    def from_dict(cls, data_dict) -> "AcousticPressure":
        """
        Creates an AcousticPressure from a dict

        :param data_dict: A dictionary containing "real_values" and "imag_values" keys.
        :type data_dict: dict[str, list[float] | list[complex]]
        """

        real = data_dict["real_values"]
        imaginary = data_dict["imag_values"]

        return AcousticPressure(real=real, imaginary=imaginary)

@dataclass
class AcousticPressureTable:
    names: list[str]
    paths: list[str]
    values: list[np.ndarray]

    def to_dict(self) -> dict[str, list[str] | list[str] | list[np.ndarray]]:
        return dict(
            name=self.names,
            path=self.paths,
            data=self.values,
        )
 
    @classmethod
    def from_dict(cls, data_dict) -> "AcousticPressureTable":
        """
        Creates an AcousticPressureTable from a dict

        :param data_dict: A dictionary containing "table_names", "table_paths" and "values" keys.
        :type data_dict: dict[str, list[str] | list[str] | list[np.ndarray]]
        """

        names = data_dict["table_names"]
        paths = data_dict["table_paths"]
        values = data_dict["values"]

        return AcousticPressureTable(names=names, paths=paths, values=values)
