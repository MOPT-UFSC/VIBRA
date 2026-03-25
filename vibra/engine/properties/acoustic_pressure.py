from dataclasses import dataclass, field

from vibra.engine.properties.property import GroupLabel, Property


@dataclass
class AcousticPressure(Property):
    real_values: list[float]
    imag_values: list[float]
    values: list[None | float | complex] = field(init=False)

    def __post_init__(self):
        """build the values list"""
        self.values = self._build_values()

    def get_group_label(self) -> GroupLabel:
        return GroupLabel.ACOUSTIC

    def _build_values(self) -> list[None | float | complex]:
        values: list[None | float | complex] = list()

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

    def to_dict(self) -> dict[str, list[float] | list[None | float | complex]]:
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
        real = data["real_values"]
        imaginary = data["imag_values"]

        return AcousticPressure(real_values=real, imag_values=imaginary)


@dataclass
class AcousticPressureTable(Property):
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
    def from_dict(cls, data: dict[str, list[str] | list[None | float | complex]]) -> "AcousticPressureTable":
        """
        Creates an AcousticPressureTable from a dict

        :param data_dict: A dictionary containing "table_names: list[str]", "table_paths: list[str]" and "values: list[None | float | complex]" keys.
        :type data_dict: dict[str, list[str] | list[None | float | complex]]
        """
        names = data["table_names"]
        paths = data["table_paths"]
        values = data["values"]

        return AcousticPressureTable(table_names=names, table_paths=paths, values=values)
