import re
from operator import eq
from typing import (
    Any,
    Callable,
    Generic,
    Optional,
    Protocol,
    Sequence,
    TypeVar,
    runtime_checkable,
)


@runtime_checkable
class HasIdentifier(Protocol):
    """
    Protocol for objects that can be used inside PropertyLibrary.

    Even if the objects are not instances of HasIdentifier they
    can be validated with isinstance(object, HasIdentifier).
    """

    name: str
    identifier: int


T = TypeVar("T", bound=HasIdentifier)


class PropertyLibrary(Generic[T]):
    def __init__(self):
        self._data: dict[int, T] = dict()
        self._max_id: int = -1

    def add(self, obj: T) -> int:
        if not isinstance(obj, HasIdentifier):
            raise TypeError("Object must have name and identifier attributes")

        self._max_id = max(obj.identifier, self._max_id + 1)
        obj.identifier = self._max_id
        self._data[self._max_id] = obj
        return self._max_id

    def pop(self, obj: T) -> Optional[T]:
        return self.pop_by_id(obj.identifier)

    def pop_by_id(self, identifier: int) -> Optional[T]:
        return self._data.pop(identifier, None)

    def get(self, identifier: int, fallback: Optional[T] = None) -> Optional[T]:
        return self._data.get(identifier, fallback)

    def get_from_ordered_index(self, index: int) -> Optional[T]:
        """
        Gets the object by the order it was added to the library,
        even though the identifier might be different.
        """
        for i, obj in enumerate(self._data.values()):
            if i == index:
                return obj
        return None

    def extend(self, objs: Sequence[T]):
        for obj in objs:
            self.add(obj)

    def keys(self):
        return self._data.keys()

    def values(self):
        return self._data.values()

    def items(self):
        return self._data.items()

    def find_by_name(self, name: str) -> Optional[T]:
        return self._find_by_attribute("name", name)

    def contains_id(self, identifier: int) -> bool:
        return identifier in self._data.keys()

    def contains(self, obj: T) -> bool:
        return obj in self._data.values()

    def get_dupplicated_name(self, name: str) -> str:
        ENDS_WITH_COPY_PATTERN = re.compile(r"\(copy \d+\)")
        DIGITS_PATTERN = re.compile(r"\d+")

        def decouple_copy(text: str) -> tuple[str, str]:
            match = ENDS_WITH_COPY_PATTERN.search(text)
            if match is None:
                return text, ""

            suffix = match.group().strip()
            preffix = text[: -len(suffix)].strip()
            return preffix, suffix

        def get_copy_number(copy_text: str) -> int:
            match = DIGITS_PATTERN.search(copy_text)
            if match is None:
                return -1
            return int(match.group())

        preffix, suffix = decouple_copy(name)
        max_copy = get_copy_number(suffix)

        for item in self.values():
            item_preffix, item_suffix = decouple_copy(item.name)
            if item_preffix == preffix:
                copy_number = get_copy_number(item_suffix)
                max_copy = max(max_copy, copy_number)

        return f"{preffix} (copy {max_copy + 1})"

    @classmethod
    def default(cls):
        raise NotImplementedError(f'Class "{cls.__name__}" does not implement the "default" method.')

    def _find_by_attribute(
        self,
        attribute_name: str,
        attribute_value: str,
        comparator: Optional[Callable[[Any, Any], bool]] = None,
    ) -> Optional[T]:
        """
        Helpper function to find the first instance of an object
        that has an attribute with the given name and value.
        """

        if comparator is None:
            comparator = eq

        for obj in self._data.values():
            if not hasattr(obj, attribute_name):
                continue

            attribute = getattr(obj, attribute_name)

            if comparator(attribute, attribute_value):
                return obj

        return None

    def _recalculate_max_id(self):
        self._max_id = max(self._data.keys()) if self._data else -1

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __setitem__(self, key: int, obj: T):
        obj.identifier = key
        self._data[key] = obj
        self._max_id = max(obj.identifier, self._max_id)

    def __getitem__(self, key: int) -> T:
        return self._data[key]

    def __str__(self) -> str:
        class_name = self.__class__.__name__
        names = ", ".join([f'"{fluid.name}"' for fluid in self._data.values()])
        return f"{class_name}({names})"
