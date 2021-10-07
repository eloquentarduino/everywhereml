import numpy as np
from everywhereml.data.preprocessing.BaseTransformer import BaseTransformer


class MinMaxScaler(BaseTransformer):
    """Implementation of sklearn.preprocessing.MinMaxScaler

    @todo clip in templates
    """
    def __init__(self, features_range=(0, 1), clip=False, num_features=1, name='MinMaxScaler'):
        """Constructor

        Parameters
        ----------
        features_range: tuple (min, max), default=(0, 1)
            Desired range of transformed data.

        clip: bool, default=False
            Set to True to clip transformed values of held-out data to provided `feature range`.

        num_features: int, default=1
            Set to 0 to compute global min/max.
            Set to 1 to compute min/max for each feature.

        name: str, default="MinMaxScaler"
            Name of the transformer for the `port()` method.
        """

        assert len(features_range) == 2, 'features_range MUST be a tuple of (min, max)'
        assert isinstance(num_features, int), 'num_features MUST be an integer'

        super().__init__(name)
        self.features_range = features_range
        self.clip = clip is True
        self.num_features = num_features
        self.min = None
        self.max = None

    def _fit(self, X, y=None):
        """Fit

        Parameters
        ----------
        X: np.ndarray
            Data to fit.

        y: np.ndarray or None, default=None
            Ignored.
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

        assert np.asarray(self.min - self.max).sum() != 0, 'Bad fitting (min={}, max={})'.format(self.min, self.max)

    def _transform(self, X, y=None):
        """Transform data

        Parameters
        ----------
        X: np.ndarray
            Data to transform.

        y: np.ndarray or None, default=None
            Ignored.

        Returns
        -------
        Xt: np.ndarray
            Transformed X.

        yt: np.ndarray
            Untouched y.
        """

        assert self.min is not None and self.max is not None, 'Unfitted'

        m, M = self.features_range
        Xt = (X - self.min) / np.nan_to_num(self.max - self.min) * (M - m) + m

        if self.clip:
            Xt = np.where(Xt > M, M, np.where(Xt < m, m, Xt))

        return Xt, y

    def get_template_data(self, **kwargs):
        """Get template data

        Returns
        -------
        dict: dict
        """
        m, M = self.features_range

        return {
            'num_features': self.num_features,
            'min': self.min[:self.num_features] if self.num_features > 0 else [self.min],
            'max': self.max[:self.num_features] if self.num_features > 0 else [self.max],
            'ranges': ((self.max - self.min)[:self.num_features] if self.num_features > 0 else (self.max - self.min)) / (M - m),
            'clip': self.clip,
            'features_range': self.features_range
        }

    def get_config(self):
        """
        Get config options
        :return: dict
        """
        return {
            'num_features': self.num_features
        }
