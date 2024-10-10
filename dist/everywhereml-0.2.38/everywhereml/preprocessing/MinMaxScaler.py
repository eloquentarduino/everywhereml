import numpy as np
from everywhereml.code_generators import GeneratesCode


class MinMaxScaler(GeneratesCode):
    """
    See sklearn.preprocessing.MinMaxScaler
    """
    def __init__(self, low=0, high=1):
        """
        Constructor
        :param low:
        :param high:
        """
        self.dataset = None
        self.num_inputs = None
        self.min = None
        self.max = None
        self.low = low
        self.high = high

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
        return f"MinMaxScaler(low={self.low}, high={self.high})"

    def fit(self, dataset):
        """
        Fit dataset
        :param dataset:
        :return:
        """
        self.dataset = dataset
        self.num_inputs = dataset.num_inputs
        self.min = np.min(dataset.X, axis=0)
        self.max = np.max(dataset.X, axis=0)

    def transform(self, dataset):
        """
        Transform dataset
        :param dataset:
        :return:
        """
        X = (dataset.X - self.min) / (self.max - self.min) * (self.high - self.low) + self.low
        X[X < self.low] = self.low
        X[X > self.high] = self.high

        return dataset.replace(X=X)

    def get_template_data(self, dialect=None):
        """
        Get data for code generation
        :param dialect: str
        :return: dict
        """
        return {
            'num_inputs': self.num_inputs,
            'offset': self.min,
            'scale': np.nan_to_num(1 / (self.max - self.min)) * (self.high - self.low),
            'offset2': self.low,
            'low': self.low,
            'high': self.high
        }
