import logging
import numpy as np
from unittest import TestCase
from numpy.testing import assert_allclose
from everywhereml.data import Dataset
from everywhereml.sklearn.ensemble import RandomForestClassifier
from everywhereml.code_generators.jinja.Jinja import Jinja
from everywhereml.tests.runtime.CppRuntime import CppRuntime


class RandomForestClassifierTest(TestCase):
    """

    """
    def setUp(self) -> None:
        """

        :return:
        """
        self.logger = logging.getLogger("default")
        self.datasets = [
            Dataset.from_XY(X=np.random.random((100, 100)), y=np.random.randint(0, 2, 100)),
            Dataset.from_XY(X=np.random.random((1000, 100)), y=np.random.randint(0, 5, 1000))
        ]
        self.instances = [
            RandomForestClassifier(n_estimators=20, max_depth=20)
        ]

    def test_cpp(self):
        runtime = CppRuntime()

        for dataset in self.datasets:
            for clf in self.instances:
                self.logger.info(f"Classifier: {clf}")

                clf.fit(dataset)
                y_true = clf.predict(dataset)
                main = Jinja('tests', language='cpp', dialect=None).render('classifier', {
                    'X': dataset.X,
                    'classifier': clf.to_cpp(instance_name='classifier')
                })
                runtime.add_file('main.cpp', main)
                output = runtime.output(tmp_folder='/Users/simone/Desktop/tmp')
                self.assertIsNotNone(output, "Output is None")

                assert_allclose(y_true, output, rtol=1e-2)
