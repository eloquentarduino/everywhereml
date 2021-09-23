import os.path
import numpy as np
from subprocess import check_call, check_output
from unittest import TestCase

from numpy.testing import assert_array_equal
from sklearn.datasets import *

from everywhereml.data import Dataset
from everywhereml.templates import Jinja
from everywhereml.tests.runtime.CppRuntime import CppRuntime


class BaseClassifierTest(TestCase):
    def setUp(self):
        self.datasets = [
            Dataset(*load_iris(return_X_y=True), name='Iris'),
            Dataset(*load_wine(return_X_y=True), name='Wine'),
            Dataset(*load_breast_cancer(return_X_y=True), name='Cancer'),
            Dataset(*load_digits(return_X_y=True), name='Digits'),
        ]

    def get_instances(self, dataset):
        raise NotImplementedError('%s.get_instances()' % type(self))

    def test_languages(self):
        for dataset in self.datasets:
            for clf in self.get_instances(dataset):
                print(dataset.name, clf)
                clf.fit(dataset.X, dataset.y)
                y_pred = clf.predict(dataset.X).astype(int)

                for runtime in [self.cpp]:
                    output = runtime(clf, dataset.X).output(tmp_folder='/Users/simone/Desktop/tmp').astype(int)
                    self.assert_array_equal(y_pred, output)

    def cpp(self, clf, X):
        """
        Test C++ port
        :param clf:
        :param X:
        :return:
        """
        cpp = CppRuntime()
        main = Jinja('tests', language='cpp').render('classification/sklearn.jinja', {
            'X': X,
        })
        cpp.add_file('main.cpp', main)
        cpp.add_file('classifier.h', clf.port(classname='Classifier', language='cpp'))

        return cpp

    def assert_array_equal(self, y_pred, output, allowed_mismatches=1):
        """
        Assert that two array matches allowing a certain degree of tolerance
        :param y_pred:
        :param output:
        :param allowed_mismatches:
        :return:
        """
        mismatches = (y_pred.astype(int) != output.astype(int))
        mismatches_count = np.sum(mismatches)

        self.assertLessEqual(mismatches_count, allowed_mismatches, "%d mismatches (%d allowed)" % (mismatches_count, allowed_mismatches))

        if mismatches_count <= allowed_mismatches:
            return

        mismatch_idx = np.argmax(mismatches)
        self.assertEqual(y_pred[mismatch_idx], output[mismatch_idx], "Mismatch at position %d" % mismatch_idx)
