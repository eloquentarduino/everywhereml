import numpy as np
from everywhereml.data.preprocessing.BaseTransformer import BaseTransformer


class MinMaxScaler(BaseTransformer):
    """
    sklearn.preprocessing.MinMaxScaler implementation
    """
    def __init__(self, num_features=1, name='MinMaxScaler'):
        """
        :param num_features: int 0 for global, -1 for each feature, n for a specific number
        :param name: str default="MinMaxScaler"
        """
        assert isinstance(num_features, int), 'num_features MUST be an integer'

        super().__init__(name)
        self.num_features = num_features
        self.min = None
        self.max = None

    def _fit(self, X, y=None):
        """
        Fit
        :param X: np.ndarray
        :param y: np.ndarray
        """
        if self.num_features == 1:
            self.num_features = self.input_dim

        if self.num_features == 0:
            # global min/max
            self.min = X.min()
            self.max = X.max()
        else:
            # min/max at slices of num_features
            if self.num_features == -1:
                self.num_features = self.input_dim

            assert self.num_features <= self.input_dim and (self.input_dim % self.num_features) == 0, 'num_features MUST be a divisor of X.shape[1]'
            
            mins = [X[:, i::self.num_features].min() for i in range(self.num_features)]
            maxs = [X[:, i::self.num_features].max() for i in range(self.num_features)]

            repeat = self.input_dim // self.num_features
            self.min = np.asarray(mins * repeat)
            self.max = np.asarray(maxs * repeat)

    def _transform(self, X, y=None):
        """
        Transform
        :param X: np.ndarray
        :param y: np.ndarray
        :return: tuple
        """
        assert self.min is not None and self.max is not None, 'Unfitted'
        assert np.asarray(self.min - self.max).sum() != 0, 'Bad fitting ({} - {})'.format(self.min, self.max)

        return (X - self.min) / (self.max - self.min), y

    def get_template_data(self, **kwargs):
        """
        Get template data
        :return: dict
        """
        return {
            'num_features': self.num_features,
            'min': self.min[:self.num_features] if self.num_features > 0 else self.min,
            'inv_range': 1 / (self.max - self.min)[:self.num_features] if self.num_features > 0 else 1 / (self.max - self.min),
        }

    def get_config(self):
        """
        Get config options
        :return: dict
        """
        return {
            'num_features': self.num_features
        }
