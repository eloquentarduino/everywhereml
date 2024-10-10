import numpy as np
from everywhereml.code_generators.jinja.helpers import is_list


def to_py_list(arr, precision=11, with_parentheses=True):
    """
    Convert array to Python format
    :param arr: list|numpy.ndarray
    :param precision: int
    :param with_parentheses: bool
    :return:
    """
    arr = np.nan_to_num(arr)

    if not is_list(arr):
        fmt = '%%.%df' % precision
        return fmt % arr

    contents = (', '.join([to_py_list(x, precision) for x in arr]))

    return '[%s]' % contents if with_parentheses else contents
