from dataclasses import dataclass
from vibra.engine.properties.property import GroupLabel, Property
import numpy as np


@dataclass
class MassSource(Property):
    value: complex
    volume_id: int | None = None

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

    def to_dict(self) -> dict[str, list[float] | int | None | list[complex]]:
        return dict(
            real_values=self.real_values,
            imag_values=self.imag_values,
            volume_id=self.volume_id,
            values=self.values
        )

    @classmethod
    def from_dict(cls, data: dict) -> "MassSource":
        """
        Creates an MassSource from a dict

        :param data_dict: A dictionary containing "real_values: list[float]", "imag_values: [float]" and "volume_id: int | None" keys.
        :type data_dict: dict[str, list[float] | list[None | float | complex] | int | None]
        """
        try:
            real = data["real_values"]
            imaginary = data["imag_values"]
            volume_id = data["volume_id"] if "volume_id" in data.keys() else None

            mass_source = cls(value=(real[0] + imaginary[0]*1j), volume_id=volume_id)
        except Exception as e:
            raise ArgumentError("Invalid argument") from e

        return mass_source

@dataclass
class MassSourceTable(Property):
    table_names: list[str]
    table_paths: list[str]
    values: list[None | float | complex]
    volume_id: int | None = None

    def get_group_label(self) -> GroupLabel:
        return GroupLabel.ACOUSTIC

    def to_dict(self) -> dict[str, list[str] | list[None | float | complex] | int | None]:
        return dict(
            table_names=self.table_names,
            table_paths=self.table_paths,
            values=self.values,
            volume_id=self.volume_id
        )

    @classmethod
    def from_dict(cls, data: dict[str, list[str] | list[None | float | complex]]) -> "MassSourceTable":
        """
        Creates an MassSourceTable from a dict

        :param data_dict: A dictionary containing "table_names: list[str]", "table_paths: list[str]" and "values: list[None | float | complex]" keys.
        :type data_dict: dict[str, list[str] | list[None | float | complex]]
        """
        names = data["table_names"]
        paths = data["table_paths"]
        values = data["values"]

        return cls(table_names=names, table_paths=paths, values=values)
