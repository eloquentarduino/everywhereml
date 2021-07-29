from everywhereml.data.preprocessing import BoxCox
from everywhereml.tests.data.preprocessing.BaseTransformerTest import BaseTransformerTest


class BoxCoxTest(BaseTransformerTest):
    def get_instances(self, dataset):
        return [
            BoxCox()
        ]