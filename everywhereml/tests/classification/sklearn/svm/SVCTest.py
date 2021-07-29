from sklearn.svm import SVC as NativeImplementation
from everywhereml.classification.sklearn.svm import SVC as CustomImplementation
from everywhereml.tests.classification.BaseClassifierTest import BaseClassifierTest
from sklearn.datasets import load_iris


class SVCTest(BaseClassifierTest):
    def get_custom_implementation(self):
        return CustomImplementation()

    def get_native_implementation(self):
        return NativeImplementation()

    def test_port_cpp_binary(self):
        X, y = load_iris(return_X_y=True)
        X = X[y < 2]
        y = y[y < 2]
        cpp = self.get_custom_implementation().fit(X, y).port(language='cpp', classname='Classifier')

        self.assertRegexpMatches(cpp, 'class Classifier')
