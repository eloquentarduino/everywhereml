import numpy as np
from itertools import product
from scipy.stats import mode
from everywhereml.code_generators import GeneratesCode


class Window(GeneratesCode):
    """
    Sliding window
    """
    def __init__(self, length, shift=1):
        """
        :param length: int
        :param shift: int|float complement to overlap
        """
        assert isinstance(length, int) and length > 1, 'length MUST be > 1'
        assert isinstance(shift, int) and shift <= length or isinstance(shift, float) and 0 < shift <= 1, 'shift MUST be an integer <= length or a float in the range ]0, 1]'

        self.length = length
        self.shift = shift if isinstance(shift, int) else int(length * shift)
        self.num_inputs = None

    def __repr__(self):
        """
        Convert to string
        :return:
        """
        return str(self)

    def __str__(self):
        """
        Convert to string
        :return:
        """
        return f"Window(length={self.length}, shift={self.shift})"

    def fit(self, dataset):
        """
        Fit dataset
        :param dataset:
        :return:
        """
        # nothing to fit
        self.num_inputs = dataset.num_inputs

        return dataset

    def transform(self, dataset):
        """
        Transform
        """
        assert self.num_inputs is not None, 'Unfitted'

        idx = self.idx(dataset.X)
        X = dataset.X[idx]
        X = X.reshape((-1, self.num_inputs * self.length))
        y = np.asarray([mode(window)[0][0] for window in dataset.y[idx]])
        feature_names = [f'{feature_name}_{i}' for i, feature_name in product(range(self.length), dataset.feature_names)]

        return dataset.replace(X=X, y=y, feature_names=feature_names).annotate(window_length=self.length)

    def idx(self, X):
        """
        Get dense indices of X array
        :param X:
        :return: ndarray
        """
        w = np.arange(self.length)
        t = np.arange(len(X) - self.length + 1)
        idx = (w + t.reshape((-1, 1)))

        return idx[::self.shift]

    def get_template_data(self):
        """
        Get template data
        """
        return {
            'length': self.length,
            'shift': self.shift,
            'num_inputs': self.num_inputs
        }