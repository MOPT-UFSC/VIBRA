from dataclasses import dataclass, field

from vibra.engine.properties.property import Property


@dataclass
class AbsorptionSurface(Property):
    real_values: list[float]
    imag_values: list[float | None] | list[None]
    # postpones the creation of this attribute
    values: list[None | float | complex] = field(init=False)

    def __post_init__(self):
        """build the values list"""
        self.values = self._build_values()

    # TODO: check if build_values is necessary
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
                    values.append(a + 1j * b)

        return values

    def to_dict(self) -> dict[str, list[float] | list[float | None] | list[None] | list[None | float | complex]]:
        return dict(
            real_values=self.real_values,
            imag_values=self.imag_values,
            values=self.values
        )

    @classmethod
    def from_dict(cls, data) -> "AbsorptionSurface":
        """
        Creates an AbsorptionSurface from a dict

        :param data: A dictionary containing "real_values" and "imag_values" keys.
        :type data: dict[str, list[float]]
        """
        real = data["real_values"]
        imaginary = data["imag_values"]

        return AbsorptionSurface(real_values=real, imag_values=imaginary)


@dataclass
class AbsorptionSurfaceTable(Property):
    table_names: list[str]
    table_paths: list[str]
    values: list[None | float | complex]

    def to_dict(self) -> dict[str, list[str] | list[None | float | complex]]:
        return dict(
            table_names=self.table_names,
            table_paths=self.table_paths,
            values=self.values
        )

    @classmethod
    def from_dict(cls, data) -> "AbsorptionSurfaceTable":
        """
        Creates an AbsorptionSurfaceTable from a dict

        :param data: A dictionary containing "table_names", "table_paths" and "values" keys.
        :type data: dict[str, list[str] | list[None | float | complex]]
        """
        names = data["table_names"]
        paths = data["table_paths"]
        values = data["values"]

        return AbsorptionSurfaceTable(table_names=names, table_paths=paths, values=values)
