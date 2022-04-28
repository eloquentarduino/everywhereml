from everywhereml.data.preprocessing import Normalizer
from everywhereml.tests.data.preprocessing.BaseTransformerTest import BaseTransformerTest


class NormalizerTest(BaseTransformerTest):
    def get_instances(self, dataset):
        return [
            Normalizer(norm='l1'),
            Normalizer(norm='l2'),
            Normalizer(norm='inf'),
        ]