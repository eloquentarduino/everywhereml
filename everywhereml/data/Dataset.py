import numpy as np
from pandas import DataFrame
from sklearn.model_selection import train_test_split


class Dataset:
    """
    Dataset data structure
    """

    @staticmethod
    def from_sklearn(dataset, name=None):
        """
        Construct dataset from sklearn.datasets functions
        :param dataset:
        :param name:
        :return:
        """
        return Dataset(
            name=name or dataset.filename,
            feature_names=dataset.feature_names,
            target_names=dataset.target_names,
            X=dataset.data,
            y=dataset.target
        )

    def __init__(self, name, X, y, feature_names=None, target_names=None):
        """
        Constructor
        :param name:
        :param X:
        :param y:
        :param feature_names:
        :param target_names:
        """
        self.name = name
        self.df = None
        self.X = None
        self.y = None
        self.feature_names = None
        self.target_names = None

        feature_names = [f for f in feature_names] if feature_names is not None else ['f_%d' % i for i in range(X.shape[1])]
        target_names = [n for n in target_names] if target_names is not None else ['target_%d' % i for i in range(len(set(y)))]

        self.replace(X=X, y=y, feature_names=feature_names, target_names=target_names)

    # @property
    # def plot(self):
    #     """
    #     Get instance of dataset plotter
    #     :return:
    #     """
    #     return DatasetPlotter(self)

    def describe(self):
        """
        Describe dataset
        :return:
        """
        return self.df.describe()

    def replace(self, X=None, y=None, feature_names=None, target_names=None, **kwargs):
        """
        Replace dataset properties
        :param X:
        :param y:
        :param feature_names:
        :param target_names:
        :return:
        """
        if X is not None:
            self.X = X

        if y is not None:
            self.y = y

        if feature_names is not None:
            self.feature_names = feature_names

        if target_names is not None:
            self.target_names = target_names

        self._assert_consistency()
        self.update_df()

        return self

    def clone(self, X=None, y=None, name=None):
        """
        Clone dataset
        :param X:
        :param y:
        :param name:
        :return:
        """
        if X is None:
            X = self.X

        if y is None:
            y = self.y

        return Dataset(
            name=name,
            X=X.copy(),
            y=y.copy(),
            target_names=self.target_names,
            feature_names=self.feature_names
        )

    def apply(self, pipeline):
        """
        Apply pipeline
        :param pipeline:
        :return:
        """
        dataset = pipeline.fit_transform(self)

        return self.replace(**dataset.__dict__)

    def split(self, train_size=None, test_size=None):
        """
        Split into train/test
        :param train_size:
        :param test_size:
        :return:
        """
        assert (train_size is None or 0 < train_size < 1) or (test_size is None or 0 < test_size < 1), 'train or test size MUST be in the range [0, 1] exclusive'

        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, train_size=train_size, test_size=test_size)

        return (
            self.clone(name='%s Train' % self.name, X=X_train, y=y_train),
            self.clone(name='%s Test' % self.name, X=X_test, y=y_test)
        )

    def update_df(self):
        """
        Update internal DataFrame
        :return:
        """
        data = np.hstack((self.X, self.y.reshape((-1, 1))))
        columns = self.feature_names + ['target']
        target_names = [self.target_names[int(target)] for target in self.y]

        self.df = DataFrame(data, columns=columns)
        self.df['target_name'] = target_names

    def _assert_consistency(self):
        """
        Assert properties are consistent
        :return:
        """
        assert self.X is not None, 'X CANNOT be NONE'
        assert self.y is not None, 'y CANNOT be NONE'
        assert len(self.X) == len(self.y), 'X and y MUST have the same length. X has shape %s, y has shape %s' % (str(self.X.shape), str(self.y.shape))
        assert len(self.feature_names) == self.X.shape[1], 'feature_names MUST be None or have the same length of X.shape[1]'
        assert len(self.target_names) == len(set(self.y)), 'target_names MUST be None or have the same length as the number of labels'

