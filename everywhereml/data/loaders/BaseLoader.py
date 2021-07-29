import numpy as np
from csv import Sniffer, reader as Reader


class BaseLoader:
    """
    Base class for loaders
    """
    def __getattr__(self, item):
        """
        Proxy all calls to dataset object
        :param item:
        :return:
        """
        if item == 'dataset':
            raise AttributeError('loader has no dataset')

        return getattr(self.dataset, item)

    def loadtxt(self, filename, columns='auto', **kwargs):
        """
        Load file
        :param filename: str
        :param columns: str|list
        :param kwargs:
        :return: numpy.ndarray
        """
        # sniff delimiter
        if kwargs.get('delimiter', None) is None:
            with open(filename) as file:
                kwargs['delimiter'] = Sniffer().sniff(file.read(1024 * 2)).delimiter

        # sniff header
        if columns == 'auto':
            with open(filename) as file:
                has_header = Sniffer().has_header(file.read(1024))
                file.seek(0)
                reader = Reader(file, delimiter=kwargs.get('delimiter'))
                header = list(next(reader))
                columns = header if has_header else ['f%d' % i for i in range(len(header))]

                if has_header:
                    kwargs['skiprows'] = max(kwargs.get('skiprows', 0), 1)
        elif isinstance(columns, list) and len(columns) > 0:
            kwargs['skiprows'] = max(kwargs.get('skiprows', 0), 1)

        return np.loadtxt(filename, **kwargs), columns

    def select(self, data, columns, target_column):
        pass
