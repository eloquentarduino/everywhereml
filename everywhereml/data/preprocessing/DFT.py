import numpy as np
from math import pi, cos
from everywhereml.data.preprocessing.BaseTransformer import BaseTransformer


class DFT(BaseTransformer):
    """
    np.fft.rfft "naive" implementation
    """
    def __init__(self, num_features, lookup_sparsity=0, name='DFT'):
        """
        :param num_features: int how many features are there in the input vector (expected to be flattened)
        :param lookup_sparsity: int default=0 how many values to use to approximate sin/cos
        :param name: str default="DFT"
        """
        assert num_features > 0, 'num_features MUST be positive'
        assert lookup_sparsity >= 0, 'lookup_sparsity MUST be non-negative'

        super().__init__(name)
        self.num_features = num_features
        self.lookup_sparsity = lookup_sparsity
        self.fft_length = 0

    def get_config(self):
        """
        Get config options
        :return: dict
        """
        return {
            'num_features': self.num_features
        }

    def _fit(self, X, y=None):
        """
        Fit
        """
        if self.num_features < 1:
            self.num_features = int(self.input_dim * self.num_features)

        self.fft_samples = X.shape[1] // self.num_features

        assert (self.fft_samples & (self.fft_samples - 1) == 0), 'input dimension MUST be a power of 2'

    def _transform(self, X, y=None):
        """
        Transform
        """
        fft = None

        if self.num_features > 1:
            for feature_idx in range(self.num_features):
                # skip sqrt() on MCU
                feature_fft = np.abs(np.fft.rfft(X[:, feature_idx::self.num_features])[:, :-1]) ** 2
                fft = feature_fft if fft is None else np.hstack((fft, feature_fft))
        else:
            fft = np.abs(np.fft.rfft(X)) ** 2

        return fft, y

    def get_template_data(self):
        """
        Get template data
        """
        return {
            'fft_length': self.fft_length,
        }

    def get_cpp_template_data(self):
        """
        Get template data for C++ template
        :return: dict
        """
        return {
            'buffer_size': self.fft_samples // 2 * self.num_features,
            'PI': pi,
            'lookup': [1.0] + [cos(angle / 360 * 2 * pi) for angle in range(0, 360, self.lookup_sparsity)] + [1.0]
            if self.lookup_sparsity > 0 else None
        }
