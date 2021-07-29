import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE


class Scatter:
    """
    Scatter plot
    """
    def __init__(self, X, y=None, title='', hue=None, size=None):
        """

        :param X: numpy.ndarray X data
        :param y: numpy.ndarray (None) y data
        :param title: str ('') title of the plot
        :param hue: str|numpy.ndarray (None) matplotlib's `c` param
        :param size: int|numpy.ndarray (None) matplotlib's `s` param
        """
        if len(X.shape) == 1 or X.shape[1] == 1:
            assert len(y) == len(X), 'when X is 1D, y MUST be a 1D array'
            X = np.hstack((X.reshape((-1, 1), np.asarray(y).reshape((-1, 1)))))

        self.X = X
        self.title = title
        self.hue = hue
        self.size = size

    def tsne(self, n_components=2, random_state=0, **kwargs):
        """
        Apply t-SNE
        :param n_components: int (default=2)
        :param random_state: int (default=0)
        :return: self
        """
        assert isinstance(n_components, int) and n_components >= 1, 'n_components MUST be positive'

        self.X = TSNE(n_components=n_components, random_state=random_state, **kwargs).fit_transform(self.X)

        return self

    def show(self, **kwargs):
        """
        Show
        :param kwargs:
        :return:
        """
        ax = plt.figure().add_subplot()
        scatter = ax.scatter(self.X[:, 0].tolist(), self.X[:, 1].tolist(), c=self.hue, s=self.size, **kwargs)
        ax.legend(*scatter.legend_elements(), title="Classes")
        ax.set_xlabel('Component #1')
        ax.set_ylabel('Component #2')

        if self.title:
            ax.set_title(self.title)

        plt.show()


def scatter(X, y=None, title='', hue=None, size=None, tsne=0):
    """
    Create scatter plot
    :param X: numpy.ndarray X data
    :param y: numpy.ndarray (None) y data
    :param title: str ('') title of the plot
    :param hue: str|numpy.ndarray (None) matplotlib's `c` param
    :param size: int|numpy.ndarray (None) matplotlib's `s` param
    :param tsne: int (0) t-SNE components
    :return:
    """
    scatter = Scatter(X, y, title=title, hue=hue, size=size)

    if tsne > 0:
        scatter.tsne(tsne)

    scatter.show()