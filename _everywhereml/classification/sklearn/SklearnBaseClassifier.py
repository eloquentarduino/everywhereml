from sklearn.base import clone
from everywhereml.classification.utils import to_Xy
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

    @property
    def classification_errors(self):
        """
        Return classification errors, if any

        Returns
        -------
        errors: numpy.ndarray or None
        """
        return (self.y_pred != self.y_true) if self.y_pred is not None and self.y_true is not None else None

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

    def fit(self, X, y=None, **kwargs):
        """Fit data

        Parameters
        ----------
        X: numpy.ndarray or Dataset
            Input data

        y: numpy.ndarray or None
            Target data

        Returns
        -------
        self: SklearnBaseClassifier
        """
        self.set_Xy(X, y)
        self.sklearn_base.fit(self, self.X_train, self.y_train, **kwargs)

        return self

    def predict(self, X, y=None, **kwargs):
        """Predict target

        Parameters
        ----------
        X: numpy.ndarray or Dataset
            Input data

        y: numpy.ndarray or None
            Ignored

        Returns
        -------
        y_pred: numpy.ndarray
        """
        X, y = to_Xy(X, y, allow_y_none=True)
        self.y_true = None
        self.y_pred = self.sklearn_base.predict(self, X, **kwargs)

        return self.y_pred

    def fit_predict(self, X, y=None):
        """Fit data and return predictions on that data

        Parameters
        ----------
        X: numpy.ndarray or Dataset
            Input data

        y: numpy.ndarray or None
            Target data

        Returns
        -------
        y_pred: numpy.ndarray
        """
        self.set_Xy(X, y)
        self.sklearn_base.fit(self, self.X_train, self.y_train)

        self.y_true = y

        return self.predict(self.X_train)

