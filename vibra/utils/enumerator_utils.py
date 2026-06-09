from dataclasses import dataclass, is_dataclass
from enum import auto
from typing import Any

__all__ = ["StructEnum", "auto"]


@dataclass
class StructEnumItem:
    pass


class StructEnumMeta(type):
    def __new__(mcs, name: str, bases: tuple[type], dct: dict[str, Any]):
        cls = super().__new__(mcs, name, bases, dct)
        enum_members = list()

        for k, v in dct.items():
            if k.startswith("_"):
                continue

            if is_dataclass(v):
                enum_members.append(v)

            elif isinstance(v, auto):
                inner_cls = type(
                    f"{cls.__name__}.{k}",
                    (cls, StructEnumItem),
                    dict(v.__dict__),
                )
                setattr(cls, k, inner_cls)
                enum_members.append(inner_cls)

            elif isinstance(v, type):
                inner_cls = dataclass(
                    type(
                        f"{cls.__name__}.{k}",
                        (cls, StructEnumItem),
                        dict(v.__dict__),
                    )
                )
                setattr(cls, k, inner_cls)
                enum_members.append(inner_cls)

            else:
                raise ValueError("The types are expected to be dataclasses")

        cls._enum_members = tuple(enum_members)
        return cls

    def __iter__(cls):
        yield from cls._enum_members

    def __instancecheck__(cls, instance):
        return isinstance(instance, cls._enum_members)


class StructEnum(metaclass=StructEnumMeta):
    """
    Custom enumerator for structs.
    All items in this enumerator are expected to be dataclasses.
    If "auto()" is used, the type will be an empty class.

    Otherwise, if a class or a dataclass is defined, it will be part of the enumerator.
    It is expected to work similar to the enumerators of Rust.
    """
