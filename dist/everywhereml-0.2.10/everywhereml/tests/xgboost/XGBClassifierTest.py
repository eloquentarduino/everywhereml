import logging
import numpy as np
from unittest import TestCase
from numpy.testing import assert_allclose
from sklearn.datasets import load_iris
from everywhereml.data import Dataset
from everywhereml.xgboost import XGBClassifier
from everywhereml.code_generators.jinja.Jinja import Jinja
from everywhereml.tests.runtime.CppRuntime import CppRuntime


class XGBClassifierTest(TestCase):
    """

    """
    def setUp(self) -> None:
        """

        :return:
        """
        self.logger = logging.getLogger("default")
        bin_dataset = Dataset.from_XY(X=np.random.random((100, 25)), y=np.random.randint(0, 2, 100))
        bin_dataset.replace(
            X=np.vstack((bin_dataset.X, [[0] * bin_dataset.num_inputs])),
            y=np.concatenate((bin_dataset.y, [2])),
            target_names=['0', '1', '2']
        )

        self.datasets = [
            Dataset.from_sklearn(load_iris(), 'iris'),
            #bin_dataset
            #Dataset.from_XY(X=np.random.random((1000, 30)), y=np.random.randint(0, 5, 1000))
        ]
        self.instances = [
            XGBClassifier(n_estimators=3, max_depth=3)
        ]

    def test_cpp(self):
        runtime = CppRuntime()

        for dataset in self.datasets:
            for clf in self.instances:
                self.logger.info(f"Classifier: {clf}")

                clf.fit(dataset)
                y_true = clf.predict(dataset)
                main = Jinja('tests/templates', language='cpp', dialect=None).render('classifier', {
                    'X': dataset.X,
                    'classifier': clf.to_cpp(instance_name='classifier')
                })
                runtime.add_file('main.cpp', main)
                output = runtime.output(tmp_folder='/Users/simone/Desktop/tmp')
                self.assertIsNotNone(output, "Output is None")

                assert_allclose(y_true, output, rtol=1e-2)
