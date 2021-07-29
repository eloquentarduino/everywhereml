import numpy as np
from everywhereml.data.preprocessing.BaseTransformer import BaseTransformer
from sklearn.feature_selection import SelectKBest as KBest, chi2


class SelectKBest(BaseTransformer):
    """
    sklearn.feature_selection.SelectKBest implementation
    """
    def __init__(self, k, score_func=chi2, name='SelectKBest'):
        """
        Constructor
        :param k: int k best features
        :param score_func: callable scoring function
        :param name: str default="SelectKBest"
        """
        assert isinstance(k, int) and k > 0, 'k MUST be positive'

        super().__init__(name)

        self.k = k
        self.kbest = KBest(k=k, score_func=score_func)
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
        self.kbest.fit(X, y)
        self.idx = np.sort((-self.kbest.scores_).argsort()[:self.k])

    def _transform(self, X, y=None):
        """
        Transform
        """
        return X[:, self.idx], y

    def get_template_data(self):
        """
        Get template data
        """
        return {
            'k': self.k,
            'idx': self.idx
        }
