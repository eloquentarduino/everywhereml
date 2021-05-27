from everywhereml.data.preprocessing.BaseTransformer import BaseTransformer


class RateLimit(BaseTransformer):
    """
    Skip inputs to artificially create a given input frequency
    """
    def __init__(self, once_every, name='RateLimit'):
        """
        :param once_every: int output frequency will be 1/once_every
        :param name: str default="RateLimit"
        """
        assert isinstance(once_every, int) and once_every > 0, 'once_every MUST be a positive integer'

        super().__init__(name)
        self.once_every = once_every

    def _fit(self, X, y=None):
        """
        Fit
        """
        pass

    def _transform(self, X, y=None):
        """
        Transform
        """
        return X[::self.once_every], y[::self.once_every]

    def get_template_data(self):
        """
        Get template data
        """
        return {
            'once_every': self.once_every
        }