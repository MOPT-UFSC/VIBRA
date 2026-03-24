from ast import Call
from types import UnionType
from typing import Generator, Iterable, Sequence, Type, Callable

from numpy import true_divide
from vibra.engine.properties.acoustic_pressure import AcousticPressure
from vibra.engine.properties.mass_source import MassSource
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


PropertiesKey = tuple[VibraID, type[Property]]


class ModelProperties:
    EQUIVALENT_PROPERTIES: list[set[type[Property]]] = [
        {SurfaceVelocity, AcousticPressure},
        {MassSource},
    ]

    def __init__(self) -> None:
        self._properties: dict[PropertiesKey, Property] = dict()

    def add_property(self, vibra_id: VibraID, property: Property):
        self.remove_equivalent_properties(vibra_id, type(property))
        self._properties[vibra_id, type(property)] = property

    def remove_property(self, vibra_id: VibraID, property_type: type[Property]) -> Property | None:
        return self._properties.pop((vibra_id, property_type), None)

    def remove_all_properties_on_id(self, vibra_id: VibraID):
        ...

    def remove_equivalent_properties(
        self, vibra_id: VibraID, property_type: type[Property]
    ):
        self.remove_property(vibra_id, property_type)

        for property_set in self.EQUIVALENT_PROPERTIES:
            if property_type not in property_set:
                continue

            for property in property_set:
                self.remove_property(vibra_id, property)

    def get_properties_by_id(self, vibra_id: VibraID) -> Generator[Property]:
        func = lambda key, _: key == vibra_id

        for _, value in self.filter(func):
            yield value

    def get_ids_by_property(
        self, property_type: type[Property]
    ) -> Generator[VibraID]:
        func = lambda _, property: isinstance(property, property_type)

        for id, _ in self.filter(func):
            yield id

    def get_property(
        self, vibra_id: VibraID, property_type: type[Property]
    ) -> Property:
        return self._properties[vibra_id, property_type]

    def reset_property(self, property_type: type[Property]): ...

    def keys(self) -> Generator[VibraID]:
        for vibra_id, _ in self._properties.keys():
            yield vibra_id

    def values(self) -> Generator[Property]:
        for value in self._properties.values()
            yield value

    def items(self) -> Generator[tuple[VibraID, Property]]:
        for (vibra_id, _), value in self._properties.items():
            yield (vibra_id, value)

    def filter(
        self, func: Callable[[VibraID, Property], bool]
    ) -> Generator[tuple[VibraID, Property]]:
        for vibra_id, value in self.items():
            if func(vibra_id, value):
                yield (vibra_id, value)


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
