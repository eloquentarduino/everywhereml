from everywhereml.classification.sklearn.linear_model import LogisticRegression
from everywhereml.tests.classification.BaseClassifierTest import BaseClassifierTest


class LogisticRegressionTest(BaseClassifierTest):
    def get_instances(self, dataset):
        return [
            LogisticRegression(max_iter=10000)
        ]