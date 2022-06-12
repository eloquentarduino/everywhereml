import seaborn as sns
from sklearn.feature_selection import SelectKBest


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