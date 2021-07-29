from sklearn.svm import SVC as SklearnClassifier
from everywhereml.classification.sklearn.SklearnBaseClassifier import SklearnBaseClassifier


class SVC(SklearnBaseClassifier, SklearnClassifier):
    """
    sklearn.svm.SVC wrapper
    """
    def get_template_data(self):
        """
        Get additional data for template
        :return: dict
        """
        gamma = self.gamma

        if self.gamma == 'scale':
            gamma = 1 / (self.num_inputs * self.X_train.var())
        elif self.gamma == 'auto':
            gamma = 1 / self.num_inputs

        return {
            'n_support': self.n_support_,
            'kernel': {
                'type': self.kernel,
                'gamma': gamma,
                'coef0': self.coef0,
                'degree': self.degree
            },
            'support_vectors': self.support_vectors_,
            'intercepts': self.intercept_,
            'coefs': self.dual_coef_
        }
