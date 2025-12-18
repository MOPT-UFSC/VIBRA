import numpy as np
from dataclasses import dataclass, field


@dataclass
class AcousticPressure:
    real: list[float]
    imaginary: list[float]
    # postpones the creation of this attribute
    values: list = field(init=False)

    def __post_init__(self):
        """build the values list"""
        self.values = self._build_values()

    # def __add__(self, other):
    #     ...

    # __radd__ = __add__

    def _build_values(self) -> list:
        values = list()
        for i, a in enumerate(self.real):
            if a is None:
                values.append(None)

            else:
                b = self.imaginary[i]
                if b is None:
                    values.append(a)
                else:
                    values.append(a + 1j * b)

        return values

    def to_dict(self) -> dict[str, list[float] | list[complex]]:
        return dict(
            real_values=self.real,
            imag_values=self.imaginary,
            values=list(map(complex, self.real, self.imaginary)),
        )

    @classmethod
    def from_dict(cls, data_dict) -> "AcousticPressure":
        """
        Creates an AcousticPressure from a dict

        :param data_dict: A dictionary containing "real_values" and "imag_values" keys.
        :type data_dict: dict[str, list]
        """

        real = data_dict["real_values"]
        imaginary = data_dict["imag_values"]

        return AcousticPressure(real=real, imaginary=imaginary)


@dataclass
class AcousticPressureTable:
    names: list[str]
    paths: list[str]
    values: list

    def to_dict(self) -> dict[str, list[str] | list[str] | list]:
        return dict(
            name=self.names,
            path=self.paths,
            values=self.values,
        )

    @classmethod
    def from_dict(cls, data_dict) -> "AcousticPressureTable":
        """
        Creates an AcousticPressureTable from a dict

        :param data_dict: A dictionary containing "table_names", "table_paths" and "values" keys.
        :type data_dict: dict[str, list[str] | list]
        """

        names = data_dict["table_names"]
        paths = data_dict["table_paths"]
        values = data_dict["values"]

        return AcousticPressureTable(names=names, paths=paths, values=values)
