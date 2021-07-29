import os.path
from subprocess import check_call, check_output
from unittest import TestCase

from numpy.testing import assert_array_equal
from sklearn.datasets import load_iris

from everywhereml.data import Dataset
from everywhereml.templates import Jinja


class BaseClassifierTest(TestCase):
    def get_native_implementation(self):
        raise NotImplemented()

    def get_custom_implementation(self):
        raise NotImplemented()

    def test_fit_Xy(self):
        X, y = load_iris(return_X_y=True)
        self.get_custom_implementation().fit(X, y)

    def test_fit_dataset(self):
        X, y = load_iris(return_X_y=True)
        self.get_custom_implementation().fit(Dataset(X, y))

    def test_predict(self):
        X, y = load_iris(return_X_y=True)
        clf_custom = self.get_custom_implementation()
        clf_native = self.get_native_implementation()

        clf_custom.fit(X, y)
        clf_native.fit(X, y)

        assert_array_equal(clf_custom.predict(X), clf_native.predict(X))

    def test_port_cpp(self):
        X, y = load_iris(return_X_y=True)
        cpp = self.get_custom_implementation().fit(X, y).port(language='cpp', classname='Classifier')

        self.assertRegexpMatches(cpp, 'class Classifier')

    def test_port_cpp_classmap(self):
        X, y = load_iris(return_X_y=True)
        cpp = self.get_custom_implementation().fit(X, y).port(language='cpp', classname='Classifier', classmap={0: 'A', 1: 'B', 2: 'C'})

        self.assertRegexpMatches(cpp, 'const char\* predictLabel')
        self.assertRegexpMatches(cpp, 'const char\* idxToLabel')

    def test_ported_cpp_compiles(self):
        X, y = load_iris(return_X_y=True)
        clf = self.get_custom_implementation().fit(X, y)

        
        project = TestProjectCpp()
        project.add('classifier.h', clf.port(language='cpp'))
        project.add('main.cpp', jinja='predict', data={
            'X': X,
            'y': y
        })
        project.exec()



        ported_clf = clf.port(language='cpp', classname='Classifier').replace('#pragma once', '')
        main = Jinja('cpp', language='cpp').render('tests/predict.jinja', {
            'X': X,
            'y': clf.predict(X),
            'package_name': clf.package_name,
            'clf': ported_clf
        })

        #with NamedTemporaryFile('w', suffix='.cpp') as source:
            #with NamedTemporaryFile('w') as exe:
        src = os.path.abspath(os.path.join(os.path.dirname(__file__), 'main.cpp'))
        out = os.path.abspath(os.path.join(os.path.dirname(__file__), 'clf'))

        with open(src, 'w') as source:
            source.write(main)
            check_call(['gcc', '-o', out, source.name])

            self.assertNotIn('ERROR', check_output([out]).decode('utf-8'))

    def test_port_php(self):
        X, y = load_iris(return_X_y=True)
        php = self.get_custom_implementation().fit(X, y).port(language='php', classname='Classifier')

        print(php)
        self.assertEqual(1, 2)
        self.assertRegexpMatches(php, 'class Classifier')
