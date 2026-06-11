from vibra.utils.struct_enum import StructEnum, auto


class Structure(StructEnum):
    Empty = auto()

    class Point:
        x: int
        y: int

    class Line:
        x0: int
        y0: int
        x1: int
        y1: int


def test_instances():
    e1 = Structure.Empty()
    e2 = Structure.Empty()

    assert e1 == e2
    assert isinstance(e1, Structure)
    assert isinstance(e2, Structure)
    assert isinstance(e1, Structure.Empty)
    assert isinstance(e2, Structure.Empty)
    assert not isinstance(e1, Structure.Point)
    assert not isinstance(e2, Structure.Point)
    assert not isinstance(e1, Structure.Line)
    assert not isinstance(e2, Structure.Line)

    p1 = Structure.Point(2, 3)
    p2 = Structure.Point(2, 3)
    p3 = Structure.Point(3, 4)

    assert p1 == p2
    assert p1 != p3
    assert p2 != p3

    assert isinstance(p1, Structure)
    assert isinstance(p2, Structure)
    assert isinstance(p3, Structure)
    assert isinstance(p1, Structure.Point)
    assert isinstance(p2, Structure.Point)
    assert isinstance(p3, Structure.Point)
    assert not isinstance(p1, Structure.Empty)
    assert not isinstance(p2, Structure.Empty)
    assert not isinstance(p3, Structure.Empty)
    assert not isinstance(p1, Structure.Line)
    assert not isinstance(p2, Structure.Line)
    assert not isinstance(p3, Structure.Line)


def test_matches():
    e = Structure.Empty()

    p1 = Structure.Point(1, 2)
    p2 = Structure.Point(2, 3)
    p3 = Structure.Point(3, 3)

    l1 = Structure.Line(1, 2, 5, 4)
    l2 = Structure.Line(1, 2, 3, 5)
    l3 = Structure.Line(5, 1, 5, 2)

    structs = [e, p1, p2, p3, l1, l2, l3]

    for i in structs:
        match i:
            case Structure.Empty():
                assert i == e
            case _:
                assert i != e

        match i:
            case Structure.Point():
                assert i in [p1, p2, p3]
            case _:
                assert i not in [p1, p2, p3]

        match i:
            case Structure.Line():
                assert i in [l1, l2, l3]
            case _:
                assert i not in [l1, l2, l3]

        match i:
            case Structure.Point(_, 3):
                assert i in [p2, p3]
            case _:
                assert i not in [p2, p3]

        match i:
            case Structure.Line(_, _, 5, _):
                assert i in [l1, l3]
            case _:
                assert i not in [l1, l3]
