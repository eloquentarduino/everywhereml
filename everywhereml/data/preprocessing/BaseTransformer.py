from everywhereml.IsPortableMixin import IsPortableMixin
from everywhereml.data import Dataset


class BaseTransformer(IsPortableMixin):
    """
    Base class for data pre-processing transformers
    A Transformer implements fit(X, y) / transform(X, y)
    """
    def __init__(self, name):
        """
        Constructor
        :param name: str transformer's name
        """
        self.name = name
        self.input_samples = 0
        self.input_dim = 0
        self.output_samples = 0
        self.output_dim = 0

    def fit(self, X, y=None):
        """
        Fit
        :param X: np.ndarray|Dataset
        :param y: np.ndarray
        :return: BaseTransformer
        """
        if isinstance(X, Dataset):
            y = X.y
            X = X.X

        self.input_samples, self.input_dim = X.shape
        self._fit(X, y)

        return self

    def transform(self, X, y=None):
        """
        Transform
        :param X: np.ndarray
        :param y: np.ndarray
        :return: tuple (X, y)
        """
        if isinstance(X, Dataset):
            y = X.y
            X = X.X

        X, y = self._transform(X, y)

        self.output_samples, self.output_dim = X.shape

        return X, y

    def fit_transform(self, X, y=None):
        """
        Fit and transform
        :param X: np.ndarray
        :param y: np.ndarray
        :return: tuple (X, y)
        """
        self.fit(X, y)

        return self.transform(X, y)

    def _fit(self, X, y=None):
        """
        Actual fit
        :param X: np.ndarray
        :param y: np.ndarray
        :return: tuple (X, y)
        """
        raise NotImplemented('_fit not implemented')

    def _transform(self, X, y=None):
        """
        Transform input
        :param X: np.ndarray
        :param y: np.ndarray
        :return: tuple (X, y)
        """
        raise NotImplemented('_transform not implemented')

    def get_template_data_defaults(self):
        """
        Get more template data
        :return: dict
        """
        return {
            **super().get_template_data_defaults(),
            **{
                'classname': self.name,
                'input_dim': self.input_dim,
                'output_dim': self.output_dim
            }
        }
