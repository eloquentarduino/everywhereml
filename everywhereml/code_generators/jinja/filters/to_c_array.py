import numpy as np
from everywhereml.code_generators.jinja.helpers import is_list


def to_c_array(arr, precision=11, with_parentheses=True):
    """
    Convert array to C format
    :param arr: list|numpy.ndarray
    :param precision: int
    :param with_parentheses: bool
    :return:
    """
    arr = np.nan_to_num(arr)

    if not is_list(arr):
        fmt = '%%.%dff' % precision
        return fmt % arr

    contents = (', '.join([to_c_array(x, precision) for x in arr]))

    return '{%s}' % contents if with_parentheses else contents
