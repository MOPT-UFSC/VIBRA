from pathlib import Path

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
    input_string = input_string[1:-1].split(',')
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
        input_string = input_string.replace(text,"")
    list_of_strings = input_string.strip().split(",")
    list_bool = [True if item=="True" else False for item in list_of_strings]
    return list_bool

def get_new_path(path, name):
    path = Path(path)
    return path / name

def get_color_rgb(color):
    color = color.replace(" ", "")
    if ("[" or "(") in color:
        color = color[1:-1]
    tokens = color.split(',')
    return list(map(int, tokens))

def get_color_rgb(color):
    color = color.replace(" ", "")
    if ("[" or "(") in color:
        color = color[1:-1]
    tokens = color.split(',')
    return list(map(int, tokens))