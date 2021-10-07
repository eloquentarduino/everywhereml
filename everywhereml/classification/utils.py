import numpy as np


def to_Xy(X, y=None, allow_y_none=False):
    """
    Convert X, y from different formats to X, y arrays
    :param X: np.array
    :param y: np.array
    :param allow_y_none: bool if True, don't raise exception if y is None
    :return: tuple first element is X array, second element is y array
    """
    # X is a Dataset object
    if hasattr(X, "X"):
        y = y or getattr(X, "y", None)
        X = X.X

    if y is None and not allow_y_none:
        raise AssertionError("y CANNOT be None")

    assert X is not None, "X CANNOT be None"
    assert y is None or len(X) == len(y), "X and y MUST have the same length"

    return np.asarray(X), np.asarray(y, dtype=np.uint8)
