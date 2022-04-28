import numpy as np
from everywhereml.data.preprocessing.BaseTransformer import BaseTransformer


class Diff(BaseTransformer):
    """
    Compute np.diff(X)
    """
    def __init__(self, name='Diff'):
        super().__init__(name)

    def _fit(self, X, y=None):
        """
        Fit
        :param X: np.ndarray
        :param y: np.ndarray
        """
        # nothing to fit
        pass

    def _transform(self, X, y=None):
        """
        Compute np.diff(X)
        :return: tuple
        """
        return np.vstack((X[0].reshape((1, -1)), X[1:, :] - X[0:-1])), y
