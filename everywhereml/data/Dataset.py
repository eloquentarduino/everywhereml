import numpy as np
import pandas as pd
from pandas import DataFrame
from sklearn.model_selection import train_test_split
from everywhereml.plot.DatasetPlotter import DatasetPlotter


class Dataset:
    """
    Dataset data structure
    """
    @staticmethod
    def looks_like(dataset):
        """
        Test if argument looks like a dataset
        :param dataset:
        :return: bool
        """
        return hasattr(dataset, 'X') and hasattr(dataset, 'y') and hasattr(dataset, 'feature_names') and hasattr(dataset, 'target_names')

    @staticmethod
    def from_XY(X, y, feature_names=None, target_names=None, name=None):
        """
        Construct dataset from X and y arrays
        :param X:
        :param y:
        :param feature_names:
        :param target_names:
        :param name:
        :return:
        """
        if Dataset.looks_like(X):
            dataset = X
            y = dataset.y
            X = dataset.X
            feature_names = feature_names or dataset.feature_names
            target_names = target_names or dataset.target_names

        return Dataset(
            name=name or 'Dataset',
            feature_names=feature_names,
            target_names=target_names,
            X=np.asarray(X, dtype=float),
            y=np.asarray(y, dtype=int) if y is not None else np.zeros(len(X))
        )

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

    @staticmethod
    def from_csv(filename, name, target_column='target', target_name_column=None, **kwargs):
        """
        Construct dataset from csv file
        :param filename:
        :param name:
        :param target_column:
        :param target_name_column:
        :param kwargs:
        :return:
        """
        return Dataset.from_pandas(
            pd.read_csv(filename, **kwargs),
            name=name,
            target_column=target_column,
            target_name_column=target_name_column
        )

    @staticmethod
    def from_pandas(df, name, target_column='target', target_name_column=None):
        """
        Construct dataset from pandas dataframe
        :param df:
        :param name:
        :param target_column:
        :param target_name_column:
        :return:
        """
        numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
        numeric_df = df.select_dtypes(include=numerics)
        feature_names = [c for c in numeric_df.columns if c != target_column and c != target_name_column]
        target_names = df[target_name_column].unique() if target_name_column is not None else None

        return Dataset(
            name=name,
            feature_names=feature_names,
            target_names=target_names,
            X=df[feature_names].to_numpy(),
            y=df[target_column].to_numpy()
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
        self.annotations = []

        feature_names = [f for f in feature_names] if feature_names is not None else ['f_%d' % i for i in range(X.shape[1])]
        target_names = [n for n in target_names] if target_names is not None else ['target_%d' % i for i in range(len(set(y)))]

        self.replace(X=X, y=y, feature_names=feature_names, target_names=target_names)

    @property
    def distinct_targets(self):
        """
        Get distinct targets, sorted
        :return:
        """
        return sorted(list(set(self.y)))

    @property
    def num_inputs(self):
        """
        Get number of inputs
        :return: int
        """
        return len(self.feature_names)

    @property
    def num_outputs(self):
        """
        Get number of outputs
        :return:
        """
        return len(self.distinct_targets)

    @property
    def class_map(self):
        """
        Get mapping from target id to target name
        :return: dict
        """
        return {i: target_name for i, target_name in enumerate(self.target_names)}

    @property
    def plot(self):
        """
        Get instance of dataset plotter
        :return:
        """
        return DatasetPlotter(self)

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
        self._update_df()

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
        ).annotate(*self.annotations)

    def annotate(self, *args, **kwargs):
        """
        Add annotation to dataset
        :param args:
        :param kwargs:
        :return: self
        """
        if len(args) > 0:
            for arg in args:
                if isinstance(arg, dict):
                    self.annotate(**arg)

        if len(kwargs) > 0:
            self.annotations.append(kwargs)

        return self

    def get_annotations_by_attribute(self, attribute, **kwargs):
        """
        Get annotation that has the given attribute
        :param attribute: str
        :return: iterator
        """
        search_by_value = 'value' in kwargs
        value = kwargs.get('value')

        for annotation in self.annotations:
            if attribute in annotation:
                if not search_by_value or annotation.get(attribute) == value:
                    yield annotation.get(attribute)

        return None

    def drop_columns(self, columns: list):
        """
        Remove columns by index or name
        :param columns: list
        :return: Dataset
        """
        keep_columns = [(i, c) for i, c in enumerate(self.feature_names)
                        if i not in columns and c not in columns]
        keep_columns_indices = [i for i, c in keep_columns]

        return self.replace(
            X=self.X[:, keep_columns_indices],
            feature_names=[c for i, c in keep_columns]
        )

    def apply(self, pipeline):
        """
        Apply pipeline
        :param pipeline:
        :return:
        """
        dataset = pipeline.fit_transform(self)

        return self.replace(**dataset.__dict__)

    def split(self, train_size=None, test_size=None, **kwargs):
        """
        Split into train/test
        :param train_size:
        :param test_size:
        :return:
        """
        assert (train_size is None or 0 < train_size < 1) or (test_size is None or 0 < test_size < 1), 'train or test size MUST be in the range [0, 1] exclusive'

        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, train_size=train_size, test_size=test_size, **kwargs)

        return (
            self.clone(name='%s Train' % self.name, X=X_train, y=y_train),
            self.clone(name='%s Test' % self.name, X=X_test, y=y_test)
        )

    def _update_df(self):
        """
        Update internal DataFrame
        :return:
        """
        data = np.hstack((self.X, self.y.reshape((-1, 1))))
        columns = self.feature_names + ['target']

        self.df = DataFrame(data, columns=columns)
        self.df['target_name'] = [self.target_names[int(target)] for target in self.y]

    def _assert_consistency(self):
        """
        Assert properties are consistent
        :return:
        """
        assert self.X is not None, 'X CANNOT be NONE'
        assert self.y is not None, 'y CANNOT be NONE'
        assert len(self.X) == len(self.y), 'X and y MUST have the same length. X has shape %s, y has shape %s' % (str(self.X.shape), str(self.y.shape))
        assert len(self.feature_names) == self.X.shape[1], 'feature_names MUST be None or have the same length of X.shape[1] (%d given, %d expected)' % (len(self.feature_names), self.X.shape[1])
        assert len(self.target_names) == len(set(self.y)), 'target_names MUST be None or have the same length as the number of labels'

