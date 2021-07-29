import numpy as np


def to_Xy(X, y=None):
    """
    Convert X, y from different formats to X, y ndarrays
    :param X:
    :param y:
    :return: tuple first element is X array, second element is y array
    """
    if y is None:
        assert hasattr(X, 'X') and hasattr(X, 'y'), 'when y is None, first argument MUST have X and y attributes'
        y = X.y
        X = X.X

    assert X is not None, 'X CANNOT be None'
    assert y is not None, 'y CANNOT be None'
    assert len(X) == len(y), 'X and y MUST have the same length'

    return np.asarray(X), np.asarray(y, dtype=np.uint8)
