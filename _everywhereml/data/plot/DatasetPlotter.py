from everywhereml.plot import scatter


class DatasetPlotter:
    """Plot utilities entry-point for Dataset
    """
    def __init__(self, dataset):
        """Constructor

        Parameters
        ----------
        dataset: Dataset
        """
        self.dataset = dataset

    def scatter(self, **kwargs):
        """Draw scatter plot of dataset

        Returns
        -------
        scatter: Scatter
        """
        if 'title' not in kwargs:
            kwargs.update(title=self.dataset.name)

        return scatter(X=self.dataset.X, hue=self.dataset.y, **kwargs)