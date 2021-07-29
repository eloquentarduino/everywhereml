from sklearn.base import clone
from everywhereml.classification.BaseClassifier import BaseClassifier


class SklearnBaseClassifier(BaseClassifier):
    """
    Base class for classifiers from the sklearn package
    """

    def __call__(self, *args, **kwargs):
        """
        Proxy all calls to sklearn classifier
        """
        return self.sklearn_base(self, *args, **kwargs)

    def __getattr__(self, item):
        """
        Proxy all calls to sklearn classifier
        """
        return getattr(self.sklearn_base, item)

    @property
    def sklearn_base(self):
        """
        Get sklearn native class
        :return: type
        """
        return [base for base in self.__class__.__bases__ if base.__module__.startswith('sklearn.')][0]

    def get_params(self, *args, **kwargs):
        """
        Proxy all calls to sklearn classifier
        :param args:
        :param kwargs:
        :return: dict
        """
        try:
            return self.sklearn_base.get_params(self, *args, **kwargs)
        except IndexError:
            return {}

    def clone(self):
        """
        Clone classifier
        :return:
        """
        return clone(self)

    def fit(self, X, y=None):
        """
        Fit data
        :param X: ndarray|Dataset
        :param y: ndarray
        """
        self.set_Xy(X, y)
        self.sklearn_base.fit(self, self.X_train, self.y_train)

        return self
