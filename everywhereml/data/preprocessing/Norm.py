import numpy as np
from everywhereml.data.preprocessing.BaseTransformer import BaseTransformer


class Norm(BaseTransformer):
    """
    sklearn.preprocessing.normalize implementation
    """
    def __init__(self, norm='l2', name='Norm'):
        """
        Constructor
        :param norm: str default="l2",  one of {l1, l2, inf}
        :param name: str default="Norm"
        """
        assert norm in ['l1', 'l2', 'inf'], 'norm MUST be one of {l1, l2, inf}'

        super().__init__(name)
        self.norm = norm

    def get_config(self):
        """
        Get config options
        """
        return {
            'norm': self.norm
        }

    def _fit(self, X, y=None):
        """
        Fit
        """
        pass

    def _transform(self, X, y=None):
        """
        Transform
        """
        div = None

        if self.norm == 'l2':
            div = np.linalg.norm(X, axis=1)
        elif self.norm == 'l1':
            div = np.sum(np.abs(X), axis=1)
        elif self.norm == 'inf':
            div = np.max(np.abs(X), axis=1)

        return X / div.reshape((-1, 1)), y

    def get_template_data(self):
        """
        Get template data
        """
        return {
            'norm': self.norm
        }
