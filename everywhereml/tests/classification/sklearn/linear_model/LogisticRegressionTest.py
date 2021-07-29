from sklearn.linear_model import LogisticRegression as NativeImplementation
from everywhereml.classification.sklearn.linear_model import LogisticRegression as CustomImplementation
from everywhereml.tests.classification.BaseClassifierTest import BaseClassifierTest


class LogisticRegressionClassifierTest(BaseClassifierTest):
    def get_custom_implementation(self):
        return CustomImplementation()

    def get_native_implementation(self):
        return NativeImplementation()