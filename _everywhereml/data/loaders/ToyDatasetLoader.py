from cached_property import cached_property
from everywhereml.data.Dataset import Dataset
from sklearn.datasets import load_digits, load_wine, load_iris, load_boston, load_diabetes


class ToyDatasetLoader:
    """Load toy datasets
    """
    @cached_property
    def Iris(self):
        """Load Iris dataset

        Returns
        -------
        dataset: Dataset
        """
        return self._from_sklearn('Iris', load_iris())

    def _from_sklearn(self, name, dataset):
        """Convert scikit-learn dataset into everywhereml Dataset

        Parameters
        ----------
        name: str
            Name of the dataset

        dataset:Bunch with properties {data, target, feature_names, target_names}
            Scikit-learn dataset

        Returns
        -------
        dataset: Dataset
        """
        return Dataset(
            name=name,
            X=dataset.data,
            y=dataset.target,
            columns=dataset.feature_names,
            classmap={i: classname for i, classname in enumerate(dataset.target_names)}
        )
