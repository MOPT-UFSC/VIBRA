from ast import Call
from typing import Iterable, Sequence, Type, Callable
from vibra.engine.properties.property import GroupLabel, Property
from vibra.engine.properties.surface_velocity import SurfaceVelocity


class VibraID(int):
    def __ne__(self, other: object, /) -> bool:
        return not self == other

    def __eq__(self, other: object, /) -> bool:
        if not isinstance(other, self.__class__):
            return False

        return super().__eq__(other)

    def __str__(self):
        return f"{type(self).__name__}({super().__str__()})"

    def __hash__(self) -> int:
        return hash((type(self), int(self)))


class GlobalID(VibraID):
    def __init__(self):
        super().__int__()

    def __str__(self):
        return f"{type(self).__name__}"


class PointID(VibraID): ...


class LineID(VibraID): ...


class ModelProperties:
    def __init__(self) -> None:
        self.equivalent_properties: dict[GroupLabel, set[Property]] = list()
        self._config_property_list()

    def _config_property_list(self):
        for label in GroupLabel:
            print(label)

    def add_property(self, vibra_ids: VibraID, property: Property):
        ...

    def remove_property(
        self, vibra_id: VibraID, property: type[Property] | None = None
    ):
        ...

    def get_properties_by_id(self, vibra_id: VibraID) -> Sequence[Property]:
        ...

    def get_ids_by_property(self, property: type[Property]) -> Sequence[VibraID]:
        ...

    def get_property(self, vibra_id: VibraID, property: type[Property]) -> Property:
        ...

    def reset_property(self, property: type[Property]):
        ...

    def keys(self) -> Sequence[VibraID]:
        ...

    def values(self) -> Sequence[Property]:
        ...

    def items(self) -> Sequence[tuple[VibraID, Property]]:
        ...

    def filter(self, func: Callable[[VibraID, Property], bool]) -> Sequence[tuple[VibraID, Property]]:
        ...


a = PointID(2)
b = LineID(2)
c = PointID(2)

g = GlobalID()
h = GlobalID()

sv = SurfaceVelocity([1], [2])
print(sv.name())

mp = ModelProperties()
mp.add_property(sv, PointID(2))


assert a != b
assert a == c
assert g != a
assert g == h
assert hash(a) == hash(c)
assert hash(a) != hash(b)
