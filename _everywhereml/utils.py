import numpy as np


def repr(value, limit=10):
    """
    Return readable version of value
    :param value:
    :param limit: int
    :return: str
    """
    if isinstance(value, np.ndarray):
        if np.prod(value.shape) > limit * limit:
            return "[...]"
        return str(value[:limit])
    elif isinstance(value, list):
        return "[%s ...]" % " ".join([x for x in value[:limit]])
    else:
        return str(value)