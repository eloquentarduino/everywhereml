from everywhereml.data.preprocessing.feature_selection import RFE
from everywhereml.tests.data.preprocessing.BaseTransformerTest import BaseTransformerTest
from sklearn.tree import DecisionTreeClassifier


class RFETest(BaseTransformerTest):
    def get_instances(self, dataset):
        return [
            RFE(estimator=DecisionTreeClassifier(), k=2)
        ]