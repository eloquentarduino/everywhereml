import numpy as np
import pandas as pd

from everywhereml.data.Dataset import Dataset
from everywhereml.data.loaders.BaseLoader import BaseLoader


class FileLoader(BaseLoader):
    """
    Load data from file
    (uses pandas.read_csv internally)
    """
    def __init__(self, filename, target_column=-1, **kwargs):
        """

        :param filename: str path to the file to load
        :param columns: str|list a list of column names, or 'auto' to infer the names from the file
        :param target_column: int|str the name of the column that holds the labels
        """
        assert target_column is None or isinstance(target_column, int) or isinstance(target_column, str), 'target_column MUST be None, an integer or a string'

        # add target column to usecols
        usecols = kwargs.get('usecols', None)

        if usecols is not None and isinstance(target_column, str) and target_column not in usecols:
            kwargs['usecols'] = usecols + [target_column]

        df = pd.read_csv(filename, **kwargs)

        # if no header is present, assign dummy column names
        try:
            header = [float(column) for column in df.columns]
            columns = ['c%02d' % i for i in range(len(header))]
            row = pd.DataFrame([header], columns=columns)
            df.columns = columns
            df = pd.concat((row, df))

            # since we added a row at the beginning, drop a row at the end
            if kwargs.get('nrows', 0) > 0 and len(df) > kwargs.get('nrows'):
                df = df.iloc[:-1]
        except ValueError:
            pass

        # only keep numeric columns
        data_columns = [column for column, dtype in zip(df.columns, df.dtypes)
                        if (str(dtype).startswith('int') or str(dtype).startswith('float'))]

        if target_column is None:
            y = np.zeros(len(df), dtype=np.uint8)
        else:
            if isinstance(target_column, int):
                target_column = df.columns[target_column]

            data_columns = [column for column in data_columns if column != target_column]
            y = df[target_column].to_numpy()

        X = df[data_columns].to_numpy()

        self.dataset = Dataset(X, y, data_columns)
