import numpy as np
from everywhereml.data.ImageDataset import ImageDataset
from everywhereml.preprocessing.image import HOG
from everywhereml.tests.preprocessing.BasePreprocessingTestCase import BasePreprocessingTestCase


class HOGTest(BasePreprocessingTestCase):
    """

    """
    def get_pipelines(self):
        return [
            HOG()
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
        return
        # todo fix HOG
        self._test_cpp()

