try:
    from collections import Iterable
except ImportError:
    from collections.abc import Iterable


def is_list(x):
    """
    Check if argument is a list-like object
    :param x:
    :return: bool
    """
    return isinstance(x, Iterable) and not isinstance(x, str)
