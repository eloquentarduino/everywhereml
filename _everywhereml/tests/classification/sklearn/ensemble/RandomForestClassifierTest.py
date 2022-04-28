from everywhereml.classification.sklearn.ensemble import RandomForestClassifier
from everywhereml.tests.classification.BaseClassifierTest import BaseClassifierTest


class RandomForestClassifierTest(BaseClassifierTest):
    def get_instances(self, dataset):
        return [
            RandomForestClassifier(n_estimators=10),
            RandomForestClassifier(n_estimators=100, max_depth=20),
            RandomForestClassifier(n_estimators=200),
        ]