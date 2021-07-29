from everywhereml.data.preprocessing import YeoJohnson
from everywhereml.tests.data.preprocessing.BaseTransformerTest import BaseTransformerTest


class YeoJohnsonTest(BaseTransformerTest):
    def get_instances(self, dataset):
        return [
            YeoJohnson()
        ]