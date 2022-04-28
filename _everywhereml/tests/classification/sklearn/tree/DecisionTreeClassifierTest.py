from everywhereml.classification.sklearn.tree import DecisionTreeClassifier
from everywhereml.tests.classification.BaseClassifierTest import BaseClassifierTest


class DecisionTreeClassifierTest(BaseClassifierTest):

    def get_instances(self, dataset):
        return [
            DecisionTreeClassifier(),
        ]