from everywhereml.data.preprocessing import PolynomialFeatures
from everywhereml.tests.data.preprocessing.BaseTransformerTest import BaseTransformerTest


class PolynomialFeaturesTest(BaseTransformerTest):
    def get_instances(self, dataset):
        return [
            PolynomialFeatures(interaction_only=True),
            PolynomialFeatures(interaction_only=False),
        ]