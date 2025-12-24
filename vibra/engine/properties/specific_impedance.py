from dataclasses import dataclass, field
from numpy import ndarray

from vibra.engine.properties.property import Property


@dataclass
class SpecifcImpedance(Property):
    real_values: list[float]
    imag_values: list[float]
    values: list[None | float | complex | ndarray] = field(init=False)

    def __post_init__(self):
        """build the values list"""
        self.values = self._build_values()

    # Create a list of numbers while preserving the indices.
    def _build_values(self) -> list[None | float | complex | ndarray]:
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

    def to_dict(self) -> dict[str, list[float] | list[None | float | complex | ndarray]]:
        return dict(
            real_values=self.real_values,
            imag_values=self.imag_values,
            values=self.values
        )

    @classmethod
    def from_dict(cls, data: dict[str, list[float]]) -> "SpecifcImpedance":
        """
        Creates an SpecifcImpedance from a dict

        :param data_dict: A dictionary containing "real_values" and "imag_values" keys.
        :type data_dict: dict[str, list[float]]
        """
        real = data["real_values"]
        imaginary = data["imag_values"]

        return SpecifcImpedance(real_values=real, imag_values=imaginary)


@dataclass
class SpecifcImpedanceTable(Property):
    table_names: list[str]
    table_paths: list[str]
    values: list[None | float | complex | ndarray]

    def to_dict(self) -> dict[str, list[str] | list[None | float | complex | ndarray]]:
        return dict(
            table_names=self.table_names,
            table_paths=self.table_paths,
            values=self.values
        )

    @classmethod
    def from_dict(cls, data: dict[str, list[str] | list[None | float | complex | ndarray]]) -> "SpecifcImpedanceTable":
        """
        Creates an SpecifcImpedanceTable from a dict

        :param data_dict: A dictionary containing "table_names: list[str]", "table_paths: list[str]" and "values: list[None | float | complex | ndarray]" keys.
        :type data_dict: dict[str, str | list[None | float | complex]]
        """
        names = data["table_names"]
        paths = data["table_paths"]
        values = data["values"]

        return SpecifcImpedanceTable(table_names=names, table_paths=paths, values=values)
