import numpy as np
import matplotlib.pyplot as plt
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
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
        self.y = y
        self.title = title
        self.hue = hue
        self.size = size
        self.ax = None
        self.scatter = None

    def tsne(self, n_components=2, random_state=0, learning_rate="auto", init="pca", **kwargs):
        """
        Apply t-SNE
        :param n_components: int (default=2)
        :param random_state: int (default=0)
        :param learning_rate: float|"auto" (default="auto")
        :param init: {"random", "pca"}|ndarray
        :return: self
        """
        assert isinstance(n_components, int) and n_components >= 1, 'n_components MUST be positive'

        self.X = TSNE(n_components=n_components, random_state=random_state, learning_rate=learning_rate, init=init, **kwargs).fit_transform(self.X)

        return self

    def lda(self):
        """Applies LDA dimensionality reduction to data

        Returns
        -------
        self: Scatter
        """
        y = None

        if self.y is not None and len(self.y) == len(self.X):
            y = self.y
        elif self.hue is not None and not isinstance(self.hue, str) and len(self.hue) == len(self.X):
            y = self.hue
        else:
            raise AssertionError('either y or hue MUST be set to apply LDA')

        self.X = LinearDiscriminantAnalysis().fit_transform(self.X, y)

        return self

    def show(self, **kwargs):
        """
        Show
        :param kwargs:
        :return:
        """
        self.ax = plt.figure().add_subplot()
        self.scatter = self.ax.scatter(self.X[:, 0].tolist(), self.X[:, 1].tolist(), c=self.hue, s=self.size, **kwargs)
        self.ax.legend(*self.scatter.legend_elements(), title="Classes")
        self.ax.set_xlabel('Component #1')
        self.ax.set_ylabel('Component #2')

        if self.title:
            self.ax.set_title(self.title)

        plt.show()

        return self


def scatter(X, y=None, title='', hue=None, size=None, tsne=0, lda=False):
    """Create scatter plot

    Parameters
    ----------
    X: np.ndarray of shape (n_samples,) or (n_samples, n_features)
        The data to plot, either a 1D array or a NxM matrix

    y: np.ndarray of shape (n_samples,) or None, default=None
        If X is a 1D array, this is the data along the y axis

    title: str, default=''
        The title of the plot

    hue: str or np.ndarray of shape (n_samples,), default=None
        matplotlib.scatter `c` param

    size: str or np.ndarray of shape (n_samples,), default=None
        matplotlib.scatter `s` param

    tsne: int, default=0
        If greater than 0, applies t-SNE manifold dimensionality reduction to data

    lda: bool, default=False
        If True, applies LDA dimensionality reduction to data

    Returns
    -------
    scatter: Scatter

    """
    scatter = Scatter(X, y, title=title, hue=hue, size=size)

    if tsne > 0:
        scatter.tsne(tsne)

    if lda:
        scatter.lda()

    return scatter.show()