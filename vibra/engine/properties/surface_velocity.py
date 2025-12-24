from dataclasses import dataclass, field

from vibra.engine.properties.property import Property


@dataclass
class SurfaceVelocity(Property):
    real_values: list[float]
    imag_values: list[float]
    values: list[None | float | complex] = field(init=False)
    nodal_attribution: bool = False
    averaged: bool = False

    def __post_init__(self):
        """build the values list"""
        self.values = self._build_values()

    def _build_values(self) -> list[None | float | complex]:
        values = list()
        for i, a in enumerate(self.real_values):
            if a is None:
                values.append(None)

            else:
                b = self.imag_values[i]
                if b is None:
                    values.append(a)
                else:
                    values.append(a + 1j*b)

        return values

    def to_dict(self) -> dict[str, list[float] | list[None | float | complex] | bool]:
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

        :param data_dict: A dictionary containing "real_values", "imag_values", "averaged" and "nodal_attribution" keys.
        :type data_dict: dict[str, list[float] | bool]
        """
        real = data["real_values"]
        imaginary = data["imag_values"]
        averaged = data["averaged"]
        nodal_attribution = data["nodal_attribution"]

        return SurfaceVelocity(real_values=real, imag_values=imaginary, nodal_attribution=nodal_attribution, averaged=averaged)


@dataclass
class SurfaceVelocityTable(Property):
    table_names: list[str]
    table_paths: list[str]
    values: list[None | float | complex]
    nodal_attribution: bool = False
    averaged: bool = False

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

        return SurfaceVelocityTable(table_names=names, table_paths=paths, values=values, nodal_attribution=nodal_attribution, averaged=averaged)
