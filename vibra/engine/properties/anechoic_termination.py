from dataclasses import dataclass

from vibra.engine.properties.property import Property


@dataclass
class AnechoicTermination(Property):
    volume_id: int

    def to_dict(self) -> dict[str, int]:
        return dict(
            anechoic_termination=True,
            volume_id=self.volume_id
        )

    @classmethod
    def from_dict(cls, data: dict[str, int]) -> "AnechoicTermination":
        """
        Creates an AnechoicTermination from a dict

        :param data_dict: A dictionary containing "volume_id" key.
        :type data_dict: dict[str, int]
        """
        volume_id = data["volume_id"]

        return AnechoicTermination(volume_id=volume_id)
