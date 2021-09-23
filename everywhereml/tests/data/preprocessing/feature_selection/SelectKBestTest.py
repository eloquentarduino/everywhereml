from everywhereml.data.preprocessing.feature_selection import SelectKBest
from everywhereml.tests.data.preprocessing.BaseTransformerTest import BaseTransformerTest


class SelectKBestTest(BaseTransformerTest):
    def get_instances(self, dataset):
        return [
            SelectKBest(k=2)
        ]