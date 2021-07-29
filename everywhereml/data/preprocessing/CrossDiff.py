import numpy as np
from everywhereml.data.preprocessing.BaseTransformer import BaseTransformer


class CrossDiff(BaseTransformer):
    """
    Compute difference across inputs
    """
    def __init__(self, name='CrossDiff'):
        super().__init__(name)

    def _fit(self, X, y=None):
        """
        Fit
        """
        pass

    def _transform(self, X, y=None):
        """
        Transform
        :return: np.ndarray
        """
        for i in range(self.input_dim - 1):
            for j in range(i + 1, self.input_dim):
                X = np.hstack((X, (X[:, i] - X[:, j]).reshape((-1, 1))))

        return X, y
