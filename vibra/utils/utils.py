from pathlib import Path

import numpy as np
from numpy import ndarray


def group_by(keys: np.ndarray, values: np.ndarray):
    keys = keys.ravel()
    order = keys.argsort()
    values = values.ravel()

    keys = keys[order]
    values = values[order]

    unique, unique_indices = np.unique(keys, return_index=True)
    groups = np.split(values, unique_indices[1:])

    return dict(zip(unique, groups))


def get_list_of_values_from_string(input_string, int_values=True):
    """
    This function returns a list of values for a given string of a list.

    Parameters
    ----------
    input_string: string of a list
    int_values: bool

    Returns
    ----------
    list of int values if int_values is True or a list of float numbers if int_values is False
    """
    input_string = input_string[1:-1].split(",")
    list_values = []
    if int_values:
        for value in input_string:
            list_values.append(int(value))
    else:
        for value in input_string:
            list_values.append(float(value))
    return list_values


def get_list_bool_from_string(input_string):
    """
    This function returns a list of boolean variables for a given string of a boolean list.

    Parameters
    ----------
    input_string: string of a list of boolean variables

    Returns
    ----------
    list of boolean variables

    """
    for text in ["[", "]", " "]:
        input_string = input_string.replace(text, "")
    list_of_strings = input_string.strip().split(",")
    list_bool = [True if item == "True" else False for item in list_of_strings]
    return list_bool


def get_new_path(path, name):
    path = Path(path)
    return path / name


def get_color_rgb(color):
    color = color.replace(" ", "")
    if ("[" or "(") in color:
        color = color[1:-1]
    tokens = color.split(",")
    return list(map(int, tokens))


def get_color_rgb(color):
    color = color.replace(" ", "")
    if ("[" or "(") in color:
        color = color[1:-1]
    tokens = color.split(",")
    return list(map(int, tokens))


def are_there_values_different_from_zero(values: list[complex | ndarray]):
    """ """
    for value in values:
        if value is None:
            continue

        if isinstance(value, complex):
            if value != complex(0):
                return True

        if isinstance(value, ndarray):
            if value.any():
                return True

    return False
