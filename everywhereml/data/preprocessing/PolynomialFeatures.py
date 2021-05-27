from sklearn.preprocessing import PolynomialFeatures as Poly
from everywhereml.data.preprocessing.BaseTransformer import BaseTransformer


class PolynomialFeatures(BaseTransformer):
    """
    sklearn.preprocessing.PolynomialFeatures implementation
    """
    def __init__(self, interaction_only=False, name='PolynomialFeatures'):
        """
        :param interaction_only: bool default=False
        :param name: str default="PolynomialFeatures"
        """
        super().__init__(name)
        self.interaction_only = interaction_only

    def _fit(self, X, y=None):
        """
        Fit
        """
        pass

    def _transform(self, X, y=None):
        """
        Transform
        """
        # skip initial 1
        return Poly(2, interaction_only=self.interaction_only).fit_transform(X)[:, 1:], y

    def get_template_data(self):
        """
        Get template data
        """
        return {
            'offset': 1 if self.interaction_only else 0
        }