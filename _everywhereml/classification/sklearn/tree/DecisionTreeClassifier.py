from sklearn.tree import DecisionTreeClassifier as SklearnClassifier
from everywhereml.classification.sklearn.SklearnBaseClassifier import SklearnBaseClassifier


class DecisionTreeClassifier(SklearnBaseClassifier, SklearnClassifier):
    """
    sklearn.tree.DecisionTree wrapper
    """
    def get_template_data(self, **kwargs):
        """
        Get additional data for template
        :return: dict
        """
        return {
            'left': self.tree_.children_left,
            'right': self.tree_.children_right,
            'features': self.tree_.feature,
            'thresholds': self.tree_.threshold,
            'classes': self.tree_.value,
            'i': 0
        }
