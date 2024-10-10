from sklearn.ensemble import RandomForestClassifier as Impl
from everywhereml.sklearn.SklearnBaseClassifier import SklearnBaseClassifier


class RandomForestClassifier(SklearnBaseClassifier, Impl):
    """
    sklearn.ensemble.RandomForestClassifier wrapper
    """
    def get_template_data(self):
        """
        Get additional data for template
        :return: dict
        """
        return {
            'trees': [{
                'left': tree.tree_.children_left,
                'right': tree.tree_.children_right,
                'features': tree.tree_.feature,
                'thresholds': tree.tree_.threshold,
                'classes': tree.tree_.value,
            } for tree in self.estimators_]
        }
