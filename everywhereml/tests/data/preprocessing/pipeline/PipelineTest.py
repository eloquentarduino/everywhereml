from everywhereml.data.preprocessing import *
from everywhereml.data.preprocessing.pipeline import Pipeline
from everywhereml.tests.data.preprocessing.BaseTransformerTest import BaseTransformerTest


class PipelineTest(BaseTransformerTest):
    def get_instances(self, dataset):
        return [
            Pipeline("Test", [MinMaxScaler(), StandardScaler()]),
        ]