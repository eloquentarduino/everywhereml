import numpy as np
from everywhereml.data.preprocessing.BaseTransformer import BaseTransformer


class StandardScaler(BaseTransformer):
    """
    sklearn.ml.StandardScaler implementation
    """
    def __init__(self, num_features=1, name='StandardScaler'):
        """
        :param num_features: int (default=-1) if num_features==0, then a global mean / std is computed;
                            if num_features==1, then each feature gets its own mean / std;
                            if num_features==M, then the input is assumed to be a flattened version of a N * M matrix;
                            if num_features<1, then it is assumed to be a fraction of the input features
        :param name: str default="StandardScaler"
        """
        assert (isinstance(num_features, int) or isinstance(num_features, float)) and num_features >= 0, 'num_features MUST be an non-negative integer'

        if isinstance(num_features, float):
            assert num_features <= 1, 'when num_features is a float, is MUST be between 0 and 1'

        super().__init__(name)

        self.num_features = num_features
        self.mean = None
        self.std = None
        self.repeat = 1

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
        if self.num_features == 1:
            self.num_features = self.input_dim
        elif self.num_features < 1:
            self.num_features = int(self.input_dim * self.num_features)

        if self.num_features == 0:
            self.mean = X.mean()
            self.std = X.std()
        else:
            assert self.input_dim % self.num_features == 0, 'num_features MUST be a divisor of X.shape[1]'

            mean = [X[:, i::self.num_features].mean() for i in range(self.num_features)]
            std = [X[:, i::self.num_features].std() for i in range(self.num_features)]

            self.repeat = self.input_dim // self.num_features
            self.mean = np.asarray(mean * self.repeat)
            self.std = np.asarray(std * self.repeat)

    def _transform(self, X, y=None):
        """
        Transform
        """
        assert self.mean is not None and self.std is not None, 'Unfitted'

        return (X - self.mean) / self.std, y

    def get_template_data(self):
        """
        Get template data
        """
        return {
            'mean': self.mean[:self.num_features],
            'inv_std': 1 / self.std[:self.num_features],
            'num_features': self.num_features,
        }
