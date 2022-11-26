import numpy as np
from math import pi
from tqdm import tqdm
from scipy.ndimage import convolve1d
from everywhereml.data import Dataset
from everywhereml.code_generators import GeneratesCode


class HOG(GeneratesCode):
    """
    (Approximated) Histogram of Oriented Gradients image feature extractor
    """
    def __init__(self, block_size: int = 8, bins: int = 9, cell_size: int = 3, approximate_atan2: bool = True, name: str = 'HOG'):
        """

        :param block_size: int
        :param bins: int
        :param cell_size: int
        :param approximate_atan2: bool
        :param name: str
        """
        self.name = name
        self.width = None
        self.height = None
        self.block_size = block_size
        self.cell_size = cell_size
        self.bins = bins
        self.approximate_atan2 = approximate_atan2
        self.num_outputs = None

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
        return f"HOG(block_size={self.block_size}, bins={self.bins}, cell_size={self.cell_size})"

    @property
    def working_size(self):
        """

        :return: int
        """
        return self.width * self.height

    @property
    def dtype(self):
        """
        Get dtype of operator
        :return:
        """
        return 'float'

    def fit(self, dataset):
        """
        Fit dataset
        :param dataset:
        :return:
        """
        self.width = dataset.width
        self.height = dataset.height
        hog = self.hog(dataset.images[0])
        self.num_outputs = len(hog)

    def transform(self, dataset):
        """
        Transform dataset
        :param dataset:
        :return:
        """
        features = [self.hog(im) for im in tqdm(dataset.images, desc='HOG')]
        feature_names = ['hog%d' % i for i in range(len(features[0]))]

        return Dataset(
            name=dataset.name,
            X=np.asarray(features, dtype=np.float),
            y=dataset.y,
            feature_names=feature_names,
            target_names=dataset.target_names
        )

    def hog(self, im):
        """
        Extract HOG features
        :param im:
        :return:
        """
        kernel = np.asarray([1, 0, -1], dtype=np.float)
        hog = []

        # compute bins
        for y in range(0, im.shape[0], self.block_size):
            for x in range(0, im.shape[1], self.block_size):
                block = im[y:y + self.block_size, x:x + self.block_size]

                if block.shape[0] != block.shape[1]:
                    continue

                gradient_y = convolve1d(block.T, kernel, mode='constant')[1:-1, 1:-1].T
                gradient_x = convolve1d(block, kernel, mode='constant')[1:-1, 1:-1]
                gradient = np.sqrt(gradient_y ** 2 + gradient_x ** 2)
                angle = np.abs(np.arctan2(gradient_y, gradient_x) * 180 / pi).astype(np.int)
                hist = np.zeros(self.bins)
                d = 180 // self.bins

                for a, g in zip(angle.flatten(), gradient.flatten()):
                    hist[min(self.bins - 1, a // d)] += g

                hog += hist.tolist()

        # normalize
        cell_length = self.bins * self.cell_size

        for i in range(0, len(hog), cell_length):
            cells = hog[i:i + cell_length]
            m = max(cells)
            m = max(m, 0.0001)

            for j, x in enumerate(cells):
                hog[i + j] /= m

        return np.asarray(hog)

    def get_template_data(self, dialect=None):
        """

        :param dialect:
        :return:
        """
        return {
            'width': self.width,
            'height': self.height,
            'block_size': self.block_size,
            'cell_size': self.cell_size,
            'bins': self.bins,
            'pi': pi,
            'num_outputs': self.num_outputs,
            'approximate_atan2': self.approximate_atan2
        }

    def get_template_data_cpp(self, dialect=None):
        """

        :param dialect:
        :return:
        """
        return {
            'dtype': self.dtype
        }