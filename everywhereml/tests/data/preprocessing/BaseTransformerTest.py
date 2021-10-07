from unittest import TestCase
import logging

import numpy as np
from numpy.testing import assert_allclose
from sklearn.datasets import *

from everywhereml.data import Dataset
from everywhereml.templates import Jinja
from everywhereml.tests.runtime.CppRuntime import CppRuntime
from everywhereml.tests.runtime.JsRuntime import JsRuntime
from everywhereml.tests.runtime.PHPRuntime import PHPRuntime


class BaseTransformerTest(TestCase):
    def setUp(self):
        self.logger = logging.getLogger("default")

        self.datasets = [
            Dataset(*load_iris(return_X_y=True), name='Iris'),
            Dataset(*load_wine(return_X_y=True), name='Wine'),
            Dataset(*load_breast_cancer(return_X_y=True), name='Cancer'),
            Dataset(*load_digits(return_X_y=True), name='Digits'),
        ]

    def test_languages(self):
        for dataset in self.datasets:
            for transformer in self.get_instances(dataset):
                self.logger.info("Dataset: %s, Transformer: %s" % (dataset.name, transformer))

                transformer.name = "Transformer"
                X = dataset.X

                try:
                    Xt, yt = transformer.fit_transform(dataset)
                    Xt = np.nan_to_num(Xt)
                except ValueError as ex:
                    self.logger.error("Value error: %s" % str(ex))
                    continue

                for runtime_function in [self.cpp, self.js, self.js_es6, self.php]:
                    runtime = runtime_function(transformer, X, Xt)
                    self.logger.info("Runtime %s" % str(runtime))
                    output = runtime.output(tmp_folder="/Users/simone/Desktop/tmp")

                    self.assertIsNotNone(output, "Output is None")
                    assert_allclose(Xt, output, rtol=1e-2)
                    self.logger.info("OK")

    def get_instances(self, dataset):
        return []

    def cpp(self, transformer, X, Xt):
        """
        Test C++ port
        :param transformer:
        :param X:
        :param Xt:
        :return:
        """
        cpp = CppRuntime()
        main = Jinja('tests', language='cpp').render('data/preprocessing/preprocessing.jinja', {
            'X': X,
            'Xt': Xt
        })
        cpp.add_file('main.cpp', main)
        cpp.add_file('transformer.h', transformer.port(language='cpp'))

        return cpp

    def js(self, transformer, X, Xt):
        """
        Test Js port
        :param transformer:
        :param X:
        :param Xt:
        :return:
        """
        js = JsRuntime()
        main = Jinja('tests', language='js').render('data/preprocessing/TransformerTest.jinja', {
            'X': X,
            'Xt': Xt,
            'transformer': transformer.port(language='js')
        })
        js.add_file('main.js', main)

        return js

    def js_es6(self, transformer, X, Xt):
        """
        Test Js port (es6 dialect)
        :param transformer:
        :param X:
        :param Xt:
        :return:
        """
        js = JsRuntime()
        main = Jinja('tests', language='js', dialect='es6').render('data/preprocessing/TransformerTest.jinja', {
            'X': X,
            'Xt': Xt
        })
        js.add_file('main.js', main)
        js.add_file('transformer.js', transformer.port(language='js', dialect='es6'))

        return js

    def php(self, transformer, X, Xt):
        """
        Test PHP port
        :param transformer:
        :param X:
        :param Xt:
        :return:
        """
        php = PHPRuntime()
        main = Jinja('tests', language='php').render('data/preprocessing/preprocessing.jinja', {
            'X': X,
            'Xt': Xt
        })
        php.add_file('main.php', main)
        php.add_file('transformer.php', transformer.port(language='php'))

        return php
