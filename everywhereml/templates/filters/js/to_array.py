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
        fmt = '%%.%df' % precision
        return fmt % arr

    contents = (', '.join([to_array(x, precision) for x in arr]))

    return '[%s]' % contents if with_parentheses else contents