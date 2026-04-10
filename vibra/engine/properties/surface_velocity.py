from ctypes import ArgumentError
from dataclasses import dataclass
import numpy as np

from vibra.engine.properties.property import GroupLabel, Property


@dataclass
class SurfaceVelocity(Property):
    value: complex
    nodal_attribution: bool = False
    averaged: bool = False

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

    def to_dict(self) -> dict[str, list[float] | list[complex] | bool]:
        return dict(
            real_values=self.real_values,
            imag_values=self.imag_values,
            values=self.values,
            nodal_attribution=self.nodal_attribution,
            averaged=self.averaged
        )

    @classmethod
    def from_dict(cls, data: dict[str, list[float] | bool]) -> "SurfaceVelocity":
        """
        Creates an SurfaceVelocity from a dict

        :param data_dict: A dictionary containing "real_values" list[float], "imag_values" list[float], "averaged" bool and "nodal_attribution" bool keys.
        :type data_dict: dict[str, list[float] | bool]
        """
        try:
            real: list[float] = data["real_values"]
            imaginary: list[float] = data["imag_values"]
            averaged: bool = data["averaged"]
            nodal_attribution: bool = data["nodal_attribution"]

            surface_velocity = cls(value=(real[0] + imaginary[0]*1j), nodal_attribution=nodal_attribution, averaged=averaged)
        except Exception as e:
            raise ArgumentError(f'Invalid argument {e}') from e

        return surface_velocity


@dataclass
class SurfaceVelocityTable(Property):
    table_names: list[str]
    table_paths: list[str]
    values: list[None | float | complex]
    nodal_attribution: bool = False
    averaged: bool = False

    def get_group_label(self) -> GroupLabel:
        return GroupLabel.ACOUSTIC

    def to_dict(self) -> dict[str, list[str] | list[None | float | complex] | bool]:
        return dict(
            name=self.table_names,
            path=self.table_paths,
            values=self.values,
            nodal_attribution=self.nodal_attribution,
            averaged=self.averaged
        )

    @classmethod
    def from_dict(cls, data: dict[str, list[str] | list[None | float | complex] | bool]) -> "SurfaceVelocityTable":
        """
        Creates an SurfaceVelocityTable from a dict

        :param data: A dictionary containing "table_names", "table_paths", "averaged", "nodal_attribution" and "values" keys.
        :type data: dict[str, list[str] | list[None | float | complex] | bool]'
        """
        names = data["table_names"]
        paths = data["table_paths"]
        values = data["values"]
        averaged = data["averaged"]
        nodal_attribution = data["nodal_attribution"]

        return cls(table_names=names, table_paths=paths, values=values, nodal_attribution=nodal_attribution, averaged=averaged)
