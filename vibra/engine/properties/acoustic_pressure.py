from ctypes import ArgumentError
from dataclasses import dataclass
import numpy as np

from vibra.engine.properties.property import GroupLabel, Property


@dataclass
class AcousticPressure(Property):
    value: complex

    def get_group_label(self) -> GroupLabel:
        return GroupLabel.ACOUSTIC

    @property
    def real_values(self) -> list[float]:
        return [np.real(self.value)]

    @property
    def imag_values(self) -> list[float]:
        return [np.imag(self.value)]

    @property
    def values(self) -> list[complex]:
        return [self.value]

    def to_dict(self) -> dict[str, list[float] | list[complex]]:
        return dict(
            real_values=self.real_values,
            imag_values=self.imag_values,
            values=self.values
        )

    @classmethod
    def from_dict(cls, data: dict[str, list[float]]) -> "AcousticPressure":
        """
        Creates an AcousticPressure from a dict

        :param data_dict: A dictionary containing "real_values: list[float]" and "imag_values: [float]" keys.
        :type data_dict: dict[str, list[float] | list[None | float | complex]]
        """
        try:
            real = data["real_values"]
            imaginary = data["imag_values"]

            acoustic_pressure = cls(value=(real[0] + imaginary[0]*1j))
        except Exception as e:
            raise ArgumentError("Invalid argument") from e

        return acoustic_pressure


@dataclass
class AcousticPressureTable(Property):
    table_names: list[str]
    table_paths: list[str]
    values: list[None | float | complex]

    def get_group_label(self) -> GroupLabel:
        return GroupLabel.ACOUSTIC

    def to_dict(self) -> dict[str, list[str] | list[None | float | complex]]:
        return dict(
            table_names=self.table_names,
            table_paths=self.table_paths,
            values=self.values
        )

    @classmethod
    def from_dict(cls, data: dict[str, list[str] | list[None | float | complex]]) -> "AcousticPressureTable":
        """
        Creates an AcousticPressureTable from a dict

        :param data_dict: A dictionary containing "table_names: list[str]", "table_paths: list[str]" and "values: list[None | float | complex]" keys.
        :type data_dict: dict[str, list[str] | list[None | float | complex]]
        """
        names = data["table_names"]
        paths = data["table_paths"]
        values = data["values"]

        return cls(table_names=names, table_paths=paths, values=values)
