from everywhereml.classification.sklearn.svm import SVC
from everywhereml.tests.classification.BaseClassifierTest import BaseClassifierTest


class SVCTest(BaseClassifierTest):
    def get_instances(self, dataset):
        return [
            SVC(kernel='linear'),
            SVC(kernel='poly', degree=2),
            SVC(kernel='rbf', gamma=0.001),
            #SVC(kernel='sigmoid'),
        ]