from sklearn.tree import DecisionTreeClassifier as NativeImplementation
from everywhereml.classification.sklearn.tree import DecisionTreeClassifier as CustomImplementation
from everywhereml.tests.classification.BaseClassifierTest import BaseClassifierTest


class DecisionTreeClassifierTest(BaseClassifierTest):
    def get_custom_implementation(self):
        return CustomImplementation()

    def get_native_implementation(self):
        return NativeImplementation()