import numpy as np
from everywhereml.templates.filters.helpers import is_list


def to_array(arr, precision=9, with_parentheses=True):
    """
    Convert array to C
    :param arr: list|numpy.ndarray
    :param precision: int
    :param with_parentheses: bool
    :return:
    """
    if not is_list(arr):
        if np.isinf(arr):
            arr = np.finfo(np.float32).max

        fmt = '%%.%df' % precision
        return fmt % arr

    contents = (', '.join([to_array(x, precision) for x in arr]))

    return '{%s}' % contents if with_parentheses else contents


def to_json_array(arr, precision=9, with_parentheses=True):
    """
    Convert array to JSON format
    :param arr: list|ndarray
    :param precision: int
    :param with_parentes: bool
    :return:
    """
    if not is_list(arr):
        fmt = '%%.%df' % precision
        return fmt % arr

    contents = (', '.join([to_array(x, precision) for x in arr]))

    return '[%s]' % contents if with_parentheses else contents