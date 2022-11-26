import numpy as np
from math import log2
from itertools import product
from everywhereml.data import Dataset
from everywhereml.code_generators import GeneratesCode


class LBP(GeneratesCode):
    """
    Local Binary Pattern image feature extractor
    """
    def __init__(self, r=1, p=8, bins=64, spacing=1, eps=0):
        """

        :param r:
        :param p:
        :param bins:
        :param spacing: int compute LBP once every nth pixels (both along x and y axes)
        :param eps: int LBP returns 1 if (pixel - neighbor) > eps
        """
        assert r in (1, 2), 'r MUST be either 1 or 2'
        assert p == 8, 'p MUST be 8'
        assert bins and (not(bins & (bins - 1))), 'bins MUST be a power of 2'

        self.width = None
        self.height = None
        self.r = r
        self.p = p
        self.bins = bins
        self.spacing = spacing
        self.eps = eps
        self._lbp = None

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
        return f"LBP(r={self.r}, p={self.p}, spacing={self.spacing}, eps={self.eps})"

    @property
    def working_size(self):
        """

        :return: int
        """
        return self.width * self.height

    @property
    def bit_shift(self):
        """

        :return: int
        """
        return int(log2(256 // self.bins))

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

    def transform(self, dataset):
        """
        Transform dataset
        :param dataset:
        :return:
        """
        lbps = [self.lbp(im) for im in dataset.images]
        self._lbp = lbps
        hist = [self.hist(lbp) for lbp in lbps]
        feature_names = ['hist%d' % i for i in range(len(hist[0]))]

        return Dataset(
            name=dataset.name,
            X=np.asarray(hist, dtype=np.int),
            y=dataset.y,
            feature_names=feature_names,
            target_names=dataset.target_names
        )

    def lbp(self, im):
        """

        :param im:
        :return:
        """
        if im.max() <= 1:
            im = (im * 255).astype(np.uint8)

        if self.r == 1:
            roi = im[1:-1, 1:-1]
            roi = np.where(roi > 255 - self.eps, 255, roi + self.eps)
            d0 = np.where(im[0:-2, 0:-2] > roi, 1, 0).astype(np.uint8)
            d1 = np.where(im[0:-2, 1:-1] > roi, 1, 0).astype(np.uint8)
            d2 = np.where(im[0:-2, 2:] > roi, 1, 0).astype(np.uint8)
            d3 = np.where(im[1:-1, 2:] > roi, 1, 0).astype(np.uint8)
            d4 = np.where(im[2:, 2:] > roi, 1, 0).astype(np.uint8)
            d5 = np.where(im[2:, 1:-1] > roi, 1, 0).astype(np.uint8)
            d6 = np.where(im[2:, 0:-2] > roi, 1, 0).astype(np.uint8)
            d7 = np.where(im[1:-1, 0:-2] > roi, 1, 0).astype(np.uint8)
        elif self.r == 2:
            roi = im[2:-2, 2:-2] + self.eps
            roi = np.where(roi > 255, 255, roi).astype(np.uint8)
            d0 = np.where(im[1:-3, 1:-3] > roi, 1, 0).astype(np.uint8)
            d1 = np.where(im[0:-4, 2:-2] > roi, 1, 0).astype(np.uint8)
            d2 = np.where(im[1:-3, 3:-1] > roi, 1, 0).astype(np.uint8)
            d3 = np.where(im[2:-2, 4:] > roi, 1, 0).astype(np.uint8)
            d4 = np.where(im[3:-1, 3:-1] > roi, 1, 0).astype(np.uint8)
            d5 = np.where(im[4:, 2:-2] > roi, 1, 0).astype(np.uint8)
            d6 = np.where(im[3:-1, 1:-3] > roi, 1, 0).astype(np.uint8)
            d7 = np.where(im[2:-2, 0:-4] > roi, 1, 0).astype(np.uint8)
        else:
            raise AssertionError('LBP.r MUST be either 1 or 2')

        lbp = (
                d0
               | (d1 << 1)
               | (d2 << 2)
               | (d3 << 3)
               | (d4 << 4)
               | (d5 << 5)
               | (d6 << 6)
               | (d7 << 7)
        ).flatten()

        if self.spacing > 1:
            w = self.width - 2 * self.r
            xs = np.arange(w)[::self.spacing]
            ys = np.arange(self.height - 2 * self.r)[::self.spacing] * w
            idx = np.asarray([x + y for x, y in product(ys, xs)], dtype=np.int)
            lbp = lbp[idx]

        return lbp

    def hist(self, arr):
        """
        Compute histogram
        :param arr:
        :return:
        """
        return np.histogram(arr, bins=self.bins)[0]

    def get_template_data(self, dialect=None):
        """

        :param dialect:
        :return:
        """
        return {
            'width': self.width,
            'height': self.height,
            'r': self.r,
            'p': self.p,
            'bins': self.bins,
            'shift': self.bit_shift,
            'spacing': self.spacing,
            'eps': self.eps
        }

    def get_template_data_cpp(self, dialect=None):
        """

        :param dialect:
        :return:
        """
        return {
            'dtype': self.dtype
        }