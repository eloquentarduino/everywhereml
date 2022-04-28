import numpy as np
from math import pi, cos
from collections import Counter
from everywhereml.data.preprocessing.BaseTransformer import BaseTransformer


class kBestFourier(BaseTransformer):
    """Only pick k best components of Fourier transform

    """
    def __init__(self, k, num_features=1, name='kFourierTransform'):
        """Constructor

        Parameters
        ----------
        k: int
           Number of components to keep

        num_features: int
                      How many features are there in the input vector. Used in conjuction with the Window transformer

        name: str
              Name of the transformer
        """
        assert num_features > 0, 'num_features MUST be positive'

        super().__init__(name)
        self.k = k
        self.num_features = num_features
        self.fft_length = 0

    def get_config(self):
        """Get config options

        Returns
        -------
        dict
        """
        return {
            'k': self.k,
            'num_features': self.num_features
        }

    def _fit(self, X, y=None):
        """Fit

        Parameters
        ----------
        X: np.ndarray
            Input samples

        y: np.ndarray or None
            Input labels
        """
        if self.num_features < 1:
            self.num_features = int(self.input_dim * self.num_features)

        self.fft_length = X.shape[1] // self.num_features
        weights = {i: 0 for i in range(self.fft_length)}

        for feature_idx in range(self.num_features):
            Xi = X[:, feature_idx::self.num_features]
            ffti = np.abs(np.fft.rfft(Xi))
            # sort by descending magnitude
            idx = (-ffti).argsort()

            for i, idx in enumerate(idx):
                weights[idx] += (i / self.fft_length) ** 2


        self.idx = np.asarray([idx for idx, count in Counter(candidates).most_common(self.k)])

        assert (self.fft_length & (self.fft_length - 1) == 0), 'input dimension MUST be a power of 2'

    def _transform(self, X, y=None):
        """
        Transform
        """
        fft = None

        if self.num_features > 1:
            for feature_idx in range(self.num_features):
                feature_fft = np.abs(np.fft.rfft(X[:, feature_idx::self.num_features])[:, :-1])
                fft = feature_fft if fft is None else np.hstack((fft, feature_fft))
        else:
            fft = np.abs(np.fft.rfft(X)) ** 2

        return fft, y

    def get_template_data(self):
        """
        Get template data
        """
        return {
            'num_features': self.num_features,
            'num_samples': int(self.input_dim / self.num_features),
            'fft_length': (self.input_dim / self.num_features) // 2,
        }

    def get_template_data_cpp(self):
        """
        Get template data for C++ template
        :return: dict
        """
        return {
            'buffer_size': (self.fft_length // 2) * self.num_features,
            'PI': pi,
            'lookup': [1.0] + [cos(angle / 360 * 2 * pi) for angle in range(0, 360, self.lookup_sparsity)] + [1.0]
            if self.lookup_sparsity > 0 else None
        }
