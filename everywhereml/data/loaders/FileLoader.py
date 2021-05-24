import os.path
import numpy as np
import pandas as pd
from csv import Sniffer
from everywhereml.data.loaders.BaseLoader import BaseLoader
from everywhereml.data.Dataset import Dataset


class FileLoader(BaseLoader):
    """
    Load data from file
    """
    def __init__(self, filename, target_column=-1, **kwargs):
        """

        :param filename: str path to the file to load
        :param columns: str|list a list of column names, or 'auto' to infer the names from the file
        :param target_column: int|str the name of the column that holds the labels
        """
        assert isinstance(target_column, int) or isinstance(target_column, str), 'target_column MUST be an integer or a string'

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

        if isinstance(target_column, int):
            target_column = df.columns[target_column]

        data_columns = [column for column, dtype in zip(df.columns, df.dtypes)
                        if column != target_column and
                        (str(dtype).startswith('int') or str(dtype).startswith('float'))]

        X = df[data_columns].to_numpy()
        y = df[target_column].to_numpy()

        self.dataset = Dataset(X, y, data_columns)
