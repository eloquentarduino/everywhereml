from sklearn.naive_bayes import GaussianNB as NativeImplementation
from everywhereml.classification.sklearn.naive_bayes import GaussianNB as CustomImplementation
from everywhereml.tests.classification.BaseClassifierTest import BaseClassifierTest


class GaussianNBTest(BaseClassifierTest):
    def get_custom_implementation(self):
        return CustomImplementation()

    def get_native_implementation(self):
        return NativeImplementation()