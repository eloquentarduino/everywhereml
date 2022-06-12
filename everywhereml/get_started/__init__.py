from sklearn.datasets import load_iris
from everywhereml.data import Dataset
from everywhereml.sklearn.ensemble import RandomForestClassifier


iris_dataset = Dataset.from_sklearn(load_iris(), name='Iris')
iris_classifier = RandomForestClassifier(n_estimators=10, max_depth=10)