import numpy as np
from everywhereml.data.preprocessing.BaseTransformer import BaseTransformer


class StandardScaler(BaseTransformer):
    """
    sklearn.ml.StandardScaler implementation
    """
    def __init__(self, num_features=1, name='StandardScaler'):
        """
        :param num_features: int (default=-1)
                            if num_features==0, then a global mean / std is computed;
                            if num_features==-1, then each feature gets its own mean / std;
                            if num_features==M, then the input is assumed to be a flattened version of a N * M matrix;
                            if num_features<1, then it is assumed to be a fraction of the input features
        :param name: str default="StandardScaler"
        """
        assert (isinstance(num_features, int) or isinstance(num_features, float)) and num_features >= -1, 'num_features MUST be an non-negative integer, -1 or a float in the range ]0, 1]'

        if isinstance(num_features, float):
            assert 0 <= num_features <= 1, 'when num_features is a float, is MUST be between 0 and 1'

        super().__init__(name)

        self.num_features = num_features
        self.mean = None
        self.inv_std = None

    def get_config(self):
        """
        Get config options
        """
        return {
            'num_features': self.num_features
        }

    def _fit(self, X, y=None):
        """
        Fit
        """
        if self.num_features == -1:
            self.num_features = self.input_dim

        if self.num_features < 1:
            self.num_features = int(self.input_dim * self.num_features)

        if self.num_features == 0:
            self.mean = X.mean()
            self.inv_std = 1 / X.std()
        else:
            assert self.input_dim % self.num_features == 0, 'num_features MUST be a divisor of X.shape[1]'

            mean = [X[:, i::self.num_features].mean() for i in range(self.num_features)]
            std = [X[:, i::self.num_features].std() for i in range(self.num_features)]

            repeat = self.input_dim // self.num_features
            self.mean = np.asarray(mean * repeat)
            std = np.asarray(std * repeat)

            self.inv_std = np.where(np.abs(std) < 1e-6, 1, 1 / std)

    def _transform(self, X, y=None):
        """
        Transform
        """
        assert self.mean is not None and self.inv_std is not None, 'Unfitted'

        return (X - self.mean) * self.inv_std, y

    def get_template_data(self, **kwargs):
        """
        Get template data
        """
        return {
            'mean': self.mean[:self.num_features] if self.num_features > 0 else self.mean,
            'inv_std': self.inv_std[:self.num_features] if self.num_features > 0 else self.inv_std,
            'num_features': self.num_features,
        }
