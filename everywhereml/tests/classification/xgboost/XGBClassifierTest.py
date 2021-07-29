from xgboost import XGBClassifier as NativeImplementation
from everywhereml.classification.xgboost import XGBClassifier as CustomImplementation
from everywhereml.tests.classification.BaseClassifierTest import BaseClassifierTest


class XGBClassifierTest(BaseClassifierTest):
    def get_custom_implementation(self):
        return CustomImplementation(n_estimators=10)

    def get_native_implementation(self):
        return NativeImplementation(n_estimators=10)