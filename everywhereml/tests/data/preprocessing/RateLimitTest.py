from everywhereml.data.preprocessing import RateLimit
from everywhereml.tests.data.preprocessing.BaseTransformerTest import BaseTransformerTest


class RateLimitTest(BaseTransformerTest):
    def get_instances(self, dataset):
        return [
            RateLimit(once_every=2)
        ]