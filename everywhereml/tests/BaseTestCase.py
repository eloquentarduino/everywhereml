import logging
import numpy as np
from unittest import TestCase
from numpy.testing import assert_allclose
from everywhereml.code_generators.jinja.Jinja import Jinja
from everywhereml.tests.runtime.CppRuntime import CppRuntime


class BaseTestCase(TestCase):
    def setUp(self):
        """

        :return:
        """
        self.logger = logging.getLogger("default")

    def _test_pipeline(self, runtime, pipeline, dataset, **kwargs):
        """

        :param runtime:
        :param pipeline:
        :param dataset:
        :param language:
        :param kwargs:
        :return:
        """
        self.logger.debug(f"Testing runtime={runtime}, pipeline={pipeline}, dataset={dataset}")

        dataset_t = pipeline.fit_transform(dataset.clone())
        main = Jinja('tests', language=runtime.language, dialect=runtime.dialect).render('pipeline', {
            'X': dataset.X,
            'pipeline': pipeline.to_cpp(instance_name='pipeline')
        })
        runtime.add_main(main)
        output = runtime.output(tmp_folder='/Users/simone/Desktop/tmp')
        self.assertIsNotNone(output, "Output is None")

        for x_true, x_pred in zip(dataset_t.X, output):
            #self.assertLess(abs((sum(x_true) - sum(x_pred)) / len(x_true)), 0.1, 'sum of values does not match')
            is_not_close = np.abs(x_true - x_pred) > 0.1
            self.assertLess(sum(is_not_close), len(is_not_close) * 0.01, f'{self.summarize_array(x_pred)} vs {self.summarize_array(x_true)}')

    def _test_pipeline_cpp(self, pipeline, dataset):
        """

        :return:
        """
        self._test_pipeline(
            runtime=CppRuntime(),
            pipeline=pipeline,
            dataset=dataset
        )

    def summarize_array(self, arr):
        """

        :param arr:
        :return:
        """
        start = ', '.join(['%.3f' % x for x in arr[:10]])
        end = ', '.join(['%.3f' % x for x in arr[-min(len(arr) - 10, 10):]])
        ellipsis = ' ... ' if len(arr) > 20 else ''

        return f'[{start}{ellipsis}{end}]'