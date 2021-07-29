from everywhereml.data.preprocessing import MinMaxScaler
from everywhereml.tests.data.preprocessing.BaseTransformerTest import BaseTransformerTest


class MinMaxScalerTest(BaseTransformerTest):
    def get_instances(self, dataset):
        return [
            MinMaxScaler(num_features=-1),
            MinMaxScaler(num_features=dataset.num_columns),
        ]