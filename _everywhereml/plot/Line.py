import numpy as np
import matplotlib.pyplot as plt


class Line:
    """
    Line plot
    """
    def __init__(self, *args, title='', hue=None):
        """
        :param args: list list of lines
        :param title: str ('') title of the plot
        :param hue: str|numpy.ndarray (None) matplotlib's `c` param
        """
        self.lines = args
        self.title = title
        self.hue = hue

    def show(self, **kwargs):
        """
        Show
        :param kwargs:
        :return:
        """
        ax = plt.figure().add_subplot()

        for i, line in enumerate(self.lines):
            c = self.hue[i] if isinstance(self.hue, list) else self.hue
            ax.plot(line, c=c, **kwargs)

        if self.title:
            ax.set_title(self.title)

        plt.show()


def line(*args, title='', hue=None):
    """
    Create line plot
    :param args: list of lines
    :param title: str ('') title of the plot
    :param hue: str|numpy.ndarray (None) matplotlib's `c` param
    :return:
    """
    scatter = Line(*args, title=title, hue=hue)

    scatter.show()