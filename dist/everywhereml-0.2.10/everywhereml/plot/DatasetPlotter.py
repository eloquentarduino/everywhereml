import seaborn as sns
from sklearn.feature_selection import SelectKBest
from umap import UMAP
import matplotlib.pyplot as plt


class DatasetPlotter:
    """
    Plot views of dataset
    """
    def __init__(self, dataset):
        """
        Constructor
        :param dataset:
        """
        self.dataset = dataset

    def features_pairplot(self, n=None, frac=None, k=None, **kwargs):
        """
        Plot pairplot of features
        :param n: int subsample
        :param frac: float subsample
        :param k: int feature selection
        :return:
        """
        df = self.dataset.df
        feature_columns = [c for c in df.columns if not c.startswith('target')]
        target_columns = [c for c in df.columns if c.startswith('target')]

        if kwargs.get('palette', None) is None and self.dataset.num_outputs < 10:
            kwargs.update(palette=sns.color_palette("tab10")[:self.dataset.num_outputs])

        if n is not None:
            df = df.sample(n=n)
        elif frac is not None:
            df = df.sample(frac=frac)

        X = df.drop(target_columns, axis=1)
        y = df[target_columns[0]]

        if k is None and len(df.columns) > 10:
            k = 6

        if k is not None:
            k_best = SelectKBest(k=k)
            k_best.fit(X, y)
            cols = k_best.get_support(indices=True)
            feature_columns = [column for i, column in enumerate(feature_columns) if i in cols]

        sns.pairplot(df, hue='target_name', vars=feature_columns, **kwargs)

    def umap(self, **kwargs):
        """
        Plot UMAP (https://umap-learn.readthedocs.io/en/latest/)
        :return:
        """
        kwargs = {
            **{'n_neighbors': 15, 'min_dist': 0.1},
            **kwargs
        }
        X = UMAP(n_components=2, **kwargs).fit_transform(self.dataset.X)

        ax = plt.figure().add_subplot()
        scatter = ax.scatter(X[:, 0], X[:, 1], c=self.dataset.y)
        ax.legend(*scatter.legend_elements(), title="Classes")
        ax.set_xlabel('Component #1')
        ax.set_ylabel('Component #2')
        ax.set_title(f'UMAP of {self.dataset.name}')
        plt.show()