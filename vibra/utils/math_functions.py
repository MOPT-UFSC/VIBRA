import numpy as np


def lerp(a, b, t):
    return a + (b - a) * t


def remap(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def bounds_distance(bounds):
    x0, x1, y0, y1, z0, z1 = bounds
    return np.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2 + (z1 - z0) ** 2)


def inside_plane(
    test_points: np.ndarray[float],
    origin: np.ndarray[float],
    normal: np.ndarray[float],
) -> np.ndarray[bool]:
    return (
        np.dot(
            np.array(test_points) - np.array(origin),
            np.array(normal),
        )
        >= 0
    )


def points_in_between(
    test_points: np.ndarray[float],
    origin_a: np.ndarray[float],
    origin_b: np.ndarray[float],
) -> bool | np.ndarray[bool]:
    """
    Tests if test_points are in between the parallel planes
    defined by the two planes orthogonal to the (A - B) line.
    """

    ab = origin_b - origin_a
    ac = test_points - origin_a
    cb = origin_b - test_points

    x = np.dot(ac, ab)
    y = np.dot(cb, ab)

    return (x > 0) & (y > 0)


def rotation_matrices(ax, ay, az):
    sin = np.sin([ax, ay, az])
    cos = np.cos([ax, ay, az])

    rx = np.array(
        [
            [1, 0, 0, 0],
            [0, cos[0], -sin[0], 0],
            [0, sin[0], cos[0], 0],
            [0, 0, 0, 1],
        ]
    )

    ry = np.array(
        [
            [cos[1], 0, sin[1], 0],
            [0, 1, 0, 0],
            [-sin[1], 0, cos[1], 0],
            [0, 0, 0, 1],
        ]
    )

    rz = np.array(
        [
            [cos[2], -sin[2], 0, 0],
            [sin[2], cos[2], 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
    )

    return rx, ry, rz
