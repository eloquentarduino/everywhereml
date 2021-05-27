import numpy as np
from scipy.stats import mode
from everywhereml.data.preprocessing.BaseTransformer import BaseTransformer


class Window(BaseTransformer):
    """
    Sliding window
    """
    def __init__(self, length, overlap=0, flatten=True, name='Window'):
        """
        :param length: int size of window
        :param overlap: int|float (default=1) how many samples to overlap between windows.
                        If float, it is considered as a ratio of length
        :param flatten: bool (default=True) if True, reshapes the samples as a 1D array
        :param name: str (default="Window")
        """
        assert isinstance(length, int) and length > 1, 'length MUST be <= 1'
        assert isinstance(overlap, int) and overlap < length or isinstance(overlap, float) and 0 <= overlap < 1, 'shift MUST be an integer < length or a float in the range [0, 1['

        super().__init__(name)

        self.length = length
        self.overlap = overlap
        self.shift = self.length - overlap if isinstance(overlap, int) else int(length * (1 - overlap))
        self.flatten = flatten

    def get_config(self):
        """
        Get config options
        """
        return {
            'length': self.length,
            'overlap': self.overlap,
            'flatten': self.flatten
        }

    def _fit(self, X, y=None):
        """
        Fit
        """
        pass

    def _transform(self, X, y=None):
        """
        Transform
        """
        idx = self._idx(len(X))
        X = X[idx]

        if self.flatten:
            X = X.reshape((-1, self.input_dim * self.length))

        y = np.asarray([mode(window)[0][0] for window in y[idx]])

        return X, y

    def get_template_data(self):
        """
        Get template data
        """
        return {
            'length': self.length,
            'shift': self.shift,
            'flatten': self.flatten
        }

    def _idx(self, num_samples):
        """
        Get dense indices of array num_samples * N array
        :param num_samples: int
        :return: np.ndarray
        """
        w = np.arange(self.length)
        t = np.arange(num_samples - self.length + 1)
        idx = (w + t.reshape((-1, 1)))

        return idx[::self.shift]