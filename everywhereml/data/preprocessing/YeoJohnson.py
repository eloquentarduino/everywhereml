from sklearn.preprocessing import PowerTransformer
from everywhereml.data.preprocessing.BaseTransformer import BaseTransformer


class YeoJohnson(BaseTransformer):
    """
    sklearn.PowerTransform(method='yeo-johnson') implementation
    """
    def __init__(self, name='YeoJohnson'):
        super().__init__(name)

        self.power = PowerTransformer(method='yeo-johnson', standardize=False)

    def _fit(self, X, y=None):
        """
        Fit
        """
        self.power.fit(X)

    def _transform(self, X, y=None):
        """
        Transform
        """
        return self.power.transform(X), y

    def get_template_data(self):
        """
        Get template data
        """
        return {
            'lambdas': self.power.lambdas_,
            'has_zeros': len([l for l in self.power.lambdas_ if l == 0])
        }