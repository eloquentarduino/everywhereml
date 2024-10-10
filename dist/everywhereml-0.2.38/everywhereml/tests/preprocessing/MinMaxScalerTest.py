import numpy as np
from everywhereml.data import Dataset
from everywhereml.preprocessing import MinMaxScaler
from everywhereml.tests.preprocessing.BasePreprocessingTestCase import BasePreprocessingTestCase


class MinMaxScalerTest(BasePreprocessingTestCase):
    """

    """
    def get_pipelines(self):
        return [
            MinMaxScaler(),
            MinMaxScaler(low=-1, high=1)
        ]

    def get_datasets(self):
        X = np.random.random((100, 100))
        y = np.random.randint(0, 2, 100)

        return [
            Dataset.from_XY(X, y=y),
            Dataset.from_XY(100 * X, y=y),
            Dataset.from_XY(100 * X - 50, y=y),
        ]

    def test_cpp(self):
        self._test_cpp()

