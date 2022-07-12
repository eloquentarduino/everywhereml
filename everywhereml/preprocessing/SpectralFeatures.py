import re
import numpy as np

from everywhereml.code_generators import GeneratesCode


class SpectralFeatures(GeneratesCode):
    """
    Extract features from time-series
    """

    def __init__(self, order=2, eps=1e-3):
        """
        Constructor
        """
        assert order in (1, 2), 'order MUST be either 1 or 2'

        self.num_inputs = None
        self.window_length = None
        self.eps = eps
        self.order = order

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
        return f"SpectralFeatures(num_inputs={self.num_inputs}, window_length={self.window_length}, order={self.order}, num_features={len(self.feature_names)})"

    @property
    def first_order_feature_names(self):
        """
        Get names of first-order features
        :return:
        """
        return [
            'maximum',
            'minimum',
            'abs_maximum',
            'abs_minimum',
            'mean',
            'abs_energy',
            'mean_abs_change',
            'cid_ce'
        ]

    @property
    def second_order_feature_names(self):
        """
        Get names of second-order features
        :return:
        """
        return [
            'std',
            'var',
            'count_above_mean',
            'count_below_mean',
            'first_position_of_max',
            'first_position_of_min',
            'max_count',
            'min_count',
            'has_large_std',
            'skew',
            'kurtosis',
            'variation_coefficient',
        ]

    @property
    def feature_names(self):
        """
        Get names of used features
        :return: list
        """
        if self.order == 1:
            return self.first_order_feature_names
        return self.first_order_feature_names + self.second_order_feature_names

    def fit(self, dataset):
        """
        Fit dataset
        :param dataset:
        :return:
        """
        # this step is made to be used with a Window
        window_length = list(dataset.get_annotations_by_attribute('window_length'))

        assert len(window_length) > 0, 'SpectralFeatures MUST follow a Window'
        assert dataset.num_inputs % window_length[-1] == 0, 'window length MUST be a divider of dataset.num_inputs'

        self.window_length = window_length[-1]
        self.num_inputs = dataset.num_inputs // self.window_length

        return dataset

    def transform(self, dataset):
        """
        Transform dataset
        :param dataset:
        :return:
        """
        assert dataset.num_inputs % self.num_inputs == 0, 'self.num_inputs MUST be a divisor of dataset.num_inputs'

        spectral_features = None
        feature_names = []
        eps = self.eps

        for k in range(self.num_inputs):
            series = dataset.X[:, k::self.num_inputs]

            # first-order features
            maximum = series.max(axis=1).reshape((-1, 1))
            minimum = series.min(axis=1).reshape((-1, 1))
            abs_maximum = np.abs(maximum)
            abs_minimum = np.abs(minimum)
            mean = series.mean(axis=1).reshape((-1, 1))
            abs_energy = (series ** 2).mean(axis=1)
            mean_abs_change = np.abs(np.diff(series, axis=1)).mean(axis=1)
            cid_ce = (np.diff(series, axis=1) ** 2).mean(axis=1)

            spectral_features_k = [
                maximum,
                minimum,
                abs_maximum,
                abs_minimum,
                mean,
                abs_energy,
                mean_abs_change,
                cid_ce
            ]

            # second-order features
            if self.order == 2:
                ts_zero_mean = series - mean
                std = series.std(axis=1).reshape((-1, 1))
                var = ((series - mean) ** 2).mean(axis=1).reshape((-1, 1))
                count_above_mean = (ts_zero_mean > eps).sum(axis=1)
                count_below_mean = (ts_zero_mean < -eps).sum(axis=1)
                first_position_of_max = np.argmax(series, axis=1)
                first_position_of_min = np.argmin(series, axis=1)
                max_count = (series > (maximum - np.abs(maximum) * 0.02)).sum(axis=1)
                min_count = (series < (minimum + np.abs(minimum) * 0.02)).sum(axis=1)
                has_large_std = (std > 0.25 * (maximum - minimum))
                skew = np.where(var < eps, 0, ((series - mean) ** 3) / (var ** 1.5)).mean(axis=1)
                kurtosis = np.where(np.abs(var) < eps, 0, ((series - mean) ** 4) / (var ** 2)).mean(axis=1)
                variation_coefficient = np.where(mean < eps, 0, std / mean)

                spectral_features_k += [
                    std,
                    var,
                    count_above_mean,
                    count_below_mean,
                    first_position_of_max,
                    first_position_of_min,
                    max_count,
                    min_count,
                    has_large_std,
                    skew,
                    kurtosis,
                    variation_coefficient,
                ]

            spectral_features_k = np.hstack([feature.reshape((-1, 1)) for feature in spectral_features_k])
            spectral_features = spectral_features_k if spectral_features is None else np.hstack((spectral_features, spectral_features_k))
            # Window adds a _0 suffix to all features
            original_feature_name = re.sub(r'_0$', '', dataset.feature_names[k])
            feature_names += [f'{original_feature_name}_{feature_name}' for feature_name in self.feature_names]

        return dataset.replace(X=spectral_features, feature_names=feature_names)

    def get_template_data(self):
        """
        Get data for template
        :return: dict
        """
        return {
            'num_inputs': self.num_inputs,
            'window_length': self.window_length,
            'num_features': len(self.feature_names),
            'order': self.order,
            'eps': getattr(self, 'eps', 1e-3)
        }
