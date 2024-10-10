from everywhereml.preprocessing import Pipeline
from everywhereml.tests.BaseTestCase import BaseTestCase


class BasePreprocessingTestCase(BaseTestCase):
    """

    """

    def _test_cpp(self):
        """

        :return:
        """
        for dataset in self.get_datasets():
            for pipeline in self.get_pipelines():
                if not isinstance(pipeline, Pipeline):
                    steps = pipeline if isinstance(pipeline, list) else [pipeline]
                    pipeline = Pipeline(name='Test', steps=steps)

                self._test_pipeline_cpp(pipeline=pipeline, dataset=dataset)