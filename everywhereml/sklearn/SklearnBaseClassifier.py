from sklearn.base import clone
from sklearn.model_selection import cross_val_score
from everywhereml.data import Dataset
from everywhereml.code_generators import GeneratesCode


class SklearnBaseClassifier(GeneratesCode):
    """
    Base class for classifiers from the sklearn package
    """
    def __init__(self, **kwargs):
        """
        Proxy all calls to sklearn classifier
        :param kwargs:
        """
        self.sklearn.__init__(self, **kwargs)
        self.dataset = None
        self.y_pred = None

    def __call__(self, *args, **kwargs):
        """
        Proxy all calls to sklearn classifier
        """
        return self.sklearn(self, *args, **kwargs)

    def __getattr__(self, item):
        """
        Proxy all calls to sklearn classifier
        """
        return getattr(self.sklearn, item)

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
        attributes = [attr for attr in dir(self)
                      if not attr.startswith('_')
                      and not attr.endswith('_')
                      and not attr in ['dataset', 'y_pred']
                      and not callable(getattr(self, attr))]
        args = ', '.join(['%s=%s' % (attr, getattr(self, attr)) for attr in attributes])

        return f'{self.class_name}({args})'

    @property
    def sklearn(self):
        """
        Get sklearn native class
        :return: type
        """
        return [base for base in self.__class__.__bases__ if base.__module__.startswith('sklearn.')][0]

    @property
    def num_outputs(self):
        """
        Get number of classes
        :return:
        """
        return self.dataset.num_outputs if self.dataset is not None else 0

    def get_params(self, *args, **kwargs):
        """
        Proxy all calls to sklearn classifier
        :param args:
        :param kwargs:
        :return: dict
        """
        try:
            return self.sklearn.get_params(self, *args, **kwargs)
        except IndexError:
            return {}

    def clone(self):
        """
        Clone classifier
        :return:
        """
        return clone(self)

    def fit(self, X, y=None, **kwargs):
        """
        Fit data
        :param X:
        :param y:
        :param kwargs:
        """
        self.dataset = Dataset.from_XY(X, y)
        self.sklearn.fit(self, self.dataset.X, self.dataset.y, **kwargs)

        return self

    def predict(self, X, y=None, **kwargs):
        """
        Predict target
        :param X:
        :param y:
        :param kwargs:
        """
        dataset = Dataset.from_XY(X, y)
        self.y_pred = self.sklearn.predict(self, dataset.X, **kwargs)

        return self.y_pred

    def fit_predict(self, X, y=None, **kwargs):
        """
        Fit data and return predictions on that data
        :param X:
        :param y:
        :param kwargs:
        """
        self.fit(self, X, y)

        return self.predict(X)

    def score(self, X, y=None, **kwargs):
        """
        Get score of classifier on test data
        :param X:
        :param y:
        :param kwargs:
        :return:
        """
        dataset = Dataset.from_XY(X, y)

        return self.sklearn.score(self, dataset.X, dataset.y, **kwargs)

    def cross_val_score(self, X, y=None, **kwargs):
        """
        Get cross validate scores
        :param X:
        :param y:
        :param cv:
        :param kwargs:
        :return:
        """
        dataset = Dataset.from_XY(X, y)

        return cross_val_score(self, dataset.X, dataset.y, **kwargs)

    def get_template_data_cpp(self, dialect=None):
        """

        :param dialect:
        :return:
        """
        return {
            'input_dtype': 'float'
        }
