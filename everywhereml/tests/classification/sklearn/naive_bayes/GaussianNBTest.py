from everywhereml.classification.sklearn.naive_bayes import GaussianNB
from everywhereml.tests.classification.BaseClassifierTest import BaseClassifierTest


class GaussianNBTest(BaseClassifierTest):
    def get_instances(self, dataset):
        return [
            GaussianNB()
        ]