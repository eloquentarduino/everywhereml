from everywhereml.data.preprocessing import CrossDiff
from everywhereml.tests.data.preprocessing.BaseTransformerTest import BaseTransformerTest


class CrossDiffTest(BaseTransformerTest):
    def get_instances(self, dataset):
        return [
            CrossDiff()
        ]