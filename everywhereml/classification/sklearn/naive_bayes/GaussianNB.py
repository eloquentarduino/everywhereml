import numpy as np
from sklearn.naive_bayes import GaussianNB as SklearnClassifier
from everywhereml.classification.sklearn.SklearnBaseClassifier import SklearnBaseClassifier


class GaussianNB(SklearnBaseClassifier, SklearnClassifier):
    """
    sklearn.naive_bayes.GaussianNB wrapper
    """
    def get_template_data(self):
        """
        Get additional data for template
        :return: dict
        """
        return {
            'sigma_inv': 1 / self.sigma_,
            'theta': self.theta_,
            'prior': self.class_prior_ - 0.5 * np.sum(np.log(2 * np.pi * self.sigma_), axis=1),
            'chunk_size': 16
        }
