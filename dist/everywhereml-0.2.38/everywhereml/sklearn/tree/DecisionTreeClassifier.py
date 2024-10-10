from sklearn.tree import DecisionTreeClassifier as Impl
from everywhereml.sklearn.SklearnBaseClassifier import SklearnBaseClassifier


class DecisionTreeClassifier(SklearnBaseClassifier, Impl):
    """
    sklearn.ensemble.DecisionTreeClassifier wrapper
    """
    def get_template_data(self):
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
