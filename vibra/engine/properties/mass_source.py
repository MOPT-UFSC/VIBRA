from dataclasses import dataclass, field
from vibra.engine.properties.property import GroupLabel, Property


@dataclass
class MassSource(Property):
    real_values: list[float]
    imag_values: list[float]
    volume_id: int | None = None
    values: list[None | float | complex] = field(init=False)

    def __post_init__(self):
        """build the values list"""
        self.values = self._build_values()

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

    def get_group_label(self) -> GroupLabel:
        return GroupLabel.ACOUSTIC

    def to_dict(self) -> dict[str, list[float] | int | None | list[None | float | complex]]:
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
        real = [float(x) for x in data.get("real_values", [])]
        real = data["real_values"]
        imaginary = data["imag_values"]
        volume_id = data["volume_id"] if "volume_id" in data.keys() else None

        return MassSource(real_values=real, imag_values=imaginary, volume_id=volume_id)


@dataclass
class MassSourceTable(Property):
    table_names: list[str]
    table_paths: list[str]
    values: list[None | float | complex]
    volume_id: int | None = None

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

        return MassSourceTable(table_names=names, table_paths=paths, values=values)
