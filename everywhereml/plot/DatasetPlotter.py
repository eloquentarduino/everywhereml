import seaborn as sns


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

    def features_pairplot(self, **kwargs):
        """
        Plot pairplot of features
        :return:
        """
        df = self.dataset.df

        if kwargs.get('palette', None) is None and self.dataset.num_outputs < 10:
            kwargs.update(palette=sns.color_palette("tab10")[:self.dataset.num_outputs])

        sns.pairplot(df.drop(['target'], axis=1), hue='target_name', **kwargs)