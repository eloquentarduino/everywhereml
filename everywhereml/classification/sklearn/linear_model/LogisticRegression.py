from sklearn.linear_model import LogisticRegression as SklearnClassifier
from everywhereml.classification.sklearn.SklearnBaseClassifier import SklearnBaseClassifier


class LogisticRegression(SklearnBaseClassifier, SklearnClassifier):
    """
    sklearn.linear_model.LogisticRegression wrapper
    """
    def get_template_data(self):
        """
        Get additional data for template
        :return: dict
        """
        return {
            'weights': self.coef_,
            'intercepts': self.intercept_,
            'classes': self.classes_,
            'inverted': len(self.classes_) == 2
        }
