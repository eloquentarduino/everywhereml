import numpy as np
from everywhereml.data.preprocessing.BaseTransformer import BaseTransformer
from sklearn.feature_selection import RFE as SklearnRFE


class RFE(BaseTransformer):
    """
    sklearn.feature_selection.RFE implementation
    """
    def __init__(self, estimator, k, name='RFE'):
        """
        Constructor
        :param estimator: classifier
        :param k: int number of features to keep
        :param name: str default="RFE"
        """
        assert isinstance(k, int) and k > 0, 'k MUST be positive'

        super().__init__(name)
        self.k = k
        self.rfe = SklearnRFE(estimator=estimator, n_features_to_select=k)
        self.idx = None

    def get_config(self):
        """
        Get config options
        """
        return {
            'k': self.k
        }

    def _fit(self, X, y=None):
        """
        Fit
        """
        self.rfe.fit(X, y)
        self.idx = np.sort(self.rfe.ranking_.argsort()[:self.k])

    def _transform(self, X, y=None):
        """
        Transform
        """
        return X[:, self.idx], y

    def get_template_data(self, **kwargs):
        """
        Get template data
        """
        return {
            'k': self.k,
            'idx': self.idx
        }
