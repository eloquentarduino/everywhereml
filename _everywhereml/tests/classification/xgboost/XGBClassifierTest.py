from everywhereml.classification.xgboost.XGBClassifier import XGBClassifier
from everywhereml.tests.classification.BaseClassifierTest import BaseClassifierTest


class XGBClassifierTest(BaseClassifierTest):
    def get_instances(self, dataset):
        return [
            XGBClassifier()
        ]