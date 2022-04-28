from everywhereml.data.preprocessing import StandardScaler
from everywhereml.tests.data.preprocessing.BaseTransformerTest import BaseTransformerTest


class StandardScalerTest(BaseTransformerTest):
    def get_instances(self, dataset):
        return [
            StandardScaler(num_features=0),
            StandardScaler(num_features=-1),
            StandardScaler(num_features=dataset.num_columns),
        ]