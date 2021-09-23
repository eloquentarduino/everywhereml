import numpy as np


class Dataset:
    """
    Dataset abstraction
    """
    def __init__(self, X, y, columns=None, classmap=None, name=''):
        """
        Constructor
        :param X: numpy.ndarray
        :param y: numpy.ndarray
        :param columns: list|None column names
        :param name: str descriptive name of dataset
        """
        assert X is not None and y is not None, 'X and y CANNOT be None'
        assert len(X) == len(y), 'X and y MUST have the same length (%d vs %d found)' % (len(X), len(y))
        assert columns is None or len(columns) == X.shape[1], 'len(columns) and X.shape[1] MUST match'

        if columns is None:
            columns = ['f%d' for i in range(len(X[0]))]

        self.X = np.asarray(X, dtype=np.float32)
        self.y = np.asarray(y, dtype=np.uint8)
        self.columns = columns
        self.classmap = classmap
        self.name = name

    @property
    def num_samples(self):
        """
        Get number of samples in the dataset
        :return: int
        """
        return self.X.shape[0]

    @property
    def num_columns(self):
        """
        Get number of columns in the dataset
        :return: int
        """
        return self.X.shape[1]

    @property
    def num_classes(self):
        """
        Get number of distinct classes
        :return: int
        """
        return len(set(self.y))
