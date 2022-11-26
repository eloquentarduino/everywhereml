import numpy as np
from everywhereml.data import ImageDataset
from everywhereml.preprocessing.image import LBP
from everywhereml.tests.preprocessing.BasePreprocessingTestCase import BasePreprocessingTestCase


class LBPTest(BasePreprocessingTestCase):
    """

    """
    def get_pipelines(self):
        return [
            LBP(r=1, spacing=1, eps=0),
            # LBP(r=1, spacing=2, eps=0),
            # LBP(r=1, spacing=1, eps=5),
        ]

    def get_datasets(self):
        return [
            ImageDataset(
                name='Test',
                images=np.random.randint(0, 255, size=(10, 100, 100)),
                labels=['test'] * 10
            )
        ]

    def test_cpp(self):
        self._test_cpp()

