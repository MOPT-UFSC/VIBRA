import numpy as np
from dataclasses import dataclass, field


@dataclass
class SurfaceVelocity:
    real: list[float]
    imaginary: list[float]
    nodal_attribution: bool = False
    averaged: bool = False
    # postpones the creation of this attribute
    values: list = field(init=False)

    def __post_init__(self):
        """build the values list"""
        self.values = self._build_values()

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
                    values.append(a + 1j*b)

        return values

    def to_dict(self) -> dict[str, list[float] | list[complex] | bool]:
        return dict(
            real_values=self.real,
            imag_values=self.imaginary,
            nodal_attribution=self.nodal_attribution,
            averaged=self.averaged,
            values=list(map(complex, self.real, self.imaginary)),
        )

    @classmethod
    def from_dict(cls, data_dict) -> "SurfaceVelocity":
        """
        Creates an SurfaceVelocity from a dict

        :param data_dict: A dictionary containing "real_values", "imag_values", "averaged" and "nodal_attribution" keys.
        :type data_dict: dict[str, list[float] | bool]
        """

        real = data_dict["real_values"]
        imaginary = data_dict["imag_values"]
        averaged = data_dict["averaged"]
        nodal_attribution = data_dict["nodal_attribution"]

        return SurfaceVelocity(real=real, imaginary=imaginary, nodal_attribution=nodal_attribution, averaged=averaged)


@dataclass
class SurfaceVelocityTable:
    names: list[str]
    paths: list[str]
    values: list
    nodal_attribution: bool = False
    averaged: bool = False

    def to_dict(self) -> dict[str, list[str] | list[str] | list]:
        return dict(
            name=self.names,
            path=self.paths,
            values=self.values,
            nodal_attribution=self.nodal_attribution,
            averaged=self.averaged
        )

    @classmethod
    def from_dict(cls, data_dict) -> "SurfaceVelocityTable":
        """
        Creates an SurfaceVelocityTable from a dict

        :param data_dict: A dictionary containing "table_names", "table_paths", "averaged", "nodal_attribution" and "values" keys.
        :type data_dict: dict[str, list[str] | list[np.ndarray]]
        """

        names = data_dict["table_names"]
        paths = data_dict["table_paths"]
        averaged = data_dict["averaged"]
        nodal_attribution = data_dict["nodal_attribution"]
        values = data_dict["values"]

        return SurfaceVelocityTable(names=names, paths=paths, values=values, nodal_attribution=nodal_attribution, averaged=averaged)
