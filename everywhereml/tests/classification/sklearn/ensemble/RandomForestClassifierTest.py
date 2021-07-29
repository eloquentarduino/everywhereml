from sklearn.ensemble import RandomForestClassifier as NativeImplementation
from everywhereml.classification.sklearn.ensemble import RandomForestClassifier as CustomImplementation
from everywhereml.tests.classification.BaseClassifierTest import BaseClassifierTest


class RandomForestClassifierTest(BaseClassifierTest):
    def get_custom_implementation(self):
        return CustomImplementation()

    def get_native_implementation(self):
        return NativeImplementation()