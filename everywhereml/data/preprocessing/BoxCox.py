from sklearn.preprocessing import PowerTransformer
from everywhereml.data.preprocessing.BaseTransformer import BaseTransformer


class BoxCox(BaseTransformer):
    """
    sklearn.preprocessing.PowerTransform(method='box-cox') wrapper
    """
    def __init__(self, name='BoxCox'):
        super().__init__(name)
        self.power = PowerTransformer(method='box-cox', standardize=False)

    def _fit(self, X, y=None):
        """
        Fit
        :param X:
        :param y:
        :return: tuple
        """
        self.power.fit(X)

    def _transform(self, X, y=None):
        """
        Transform
        :param X:
        :param y:
        :return: tuple
        """
        return self.power.transform(X), y

    def get_template_data(self):
        """
        Get template data
        :return: dict
        """
        return {
            'lambdas': self.power.lambdas_,
            'has_zeros': len([l for l in self.power.lambdas_ if l == 0])
        }
