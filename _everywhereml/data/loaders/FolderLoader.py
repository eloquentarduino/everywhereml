import os.path
import re
from os import scandir

import numpy as np

from everywhereml.data.Dataset import Dataset
from everywhereml.data.loaders.BaseLoader import BaseLoader
from everywhereml.data.loaders.FileLoader import FileLoader


class FolderLoader(BaseLoader):
    """
    Load data from each file inside a folder
    """
    def __init__(self, folder, test=r'\.(txt|csv|tsv|TXT|CSV|TSV)$', ignore=None, max_depth=0, classmap=None, target_column=None, **kwargs):
        """
        Constructor
        :param folder: str path to the folder to load files from
        :param test: str|callable only load files that pass the test (regex or callable)
        :param ignore: str|callable ignore files that pass the test (regex or callable)
        :param target_column: None|int|str if None, target is inferred from filename
        :param max_depth: int how many level to traverse the folder tree
        :param classmap: dict a mapping from class indices to class names
        :param target_column: int column index that holds the target variable
        """
        assert os.path.isdir(folder), '%s MUST be a folder' % folder

        self.root = os.path.abspath(folder)
        self.files = sorted(list(self.walk(self.root, max_depth, test=test, ignore=ignore)))

        assert len(self.files) > 0, 'no file to read'

        datasets = [FileLoader(file, target_column=target_column, **kwargs) for file in self.files]
        X = np.vstack([dataset.X for dataset in datasets])

        if target_column is None:
            y = np.concatenate([np.ones(len(dataset.X), dtype=np.uint8) * i
                                for i, dataset in enumerate(datasets)])

            if classmap is None:
                classmap = {i: self.to_class_name(file) for i, file in enumerate(self.files)}
        else:
            y = np.concatenate([dataset.y for dataset in datasets])

        self.dataset = Dataset(X, y, columns=datasets[0].columns, classmap=classmap)

    def walk(self, folder, max_depth=-1, test=None, ignore=None, root=None):
        """
        Recursively walk a directory
        :param folder: str
        :param max_depth: int
        :param test: callable|regex
        :param ignore: callable|regex
        :param root: str
        :return: Iterator
        """
        queue = []

        if root is None:
            root = folder

        # make test a function
        if isinstance(test, str):
            # filter is a regex
            test_regex = re.compile(test)

            def test(filename):
                return test_regex.search(filename) is not None
        elif not callable(test):
            # dummy filter
            def test(filename):
                return True

        # make ignore a function
        if isinstance(ignore, str):
            # ignore is a regex
            ignore_regex = re.compile(ignore)

            def ignore(filename):
                return ignore_regex.search(filename) is not None
        elif not callable(ignore):
            # dummy ignore
            def test(filename):
                return False

        for entry in scandir(folder):
            if entry.is_dir():
                queue.append(entry)
            else:
                if test(entry.path[len(root) + 1:]) and not ignore(entry.path[len(root) + 1:]):
                    yield entry.path

        if max_depth == 0:
            return

        for q in queue:
            for file in self.walk(q, max_depth=max_depth-1, test=test, ignore=ignore, root=root):
                yield file

    def to_class_name(self, filename):
        """
        Convert file path to class name
        :param filename: str
        :return: str
        """
        return os.path.splitext(filename[len(self.root)+1:])[0]


