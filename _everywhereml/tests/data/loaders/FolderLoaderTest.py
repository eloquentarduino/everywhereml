import os
import os.path
from unittest import TestCase

from everywhereml.data.loaders import FolderLoader


class FolderLoaderTest(TestCase):
    def setUp(self):
        os.chdir(os.path.join(os.path.dirname(__file__), 'example_files'))

    def test_walk(self):
        self.assertEqual(4, len(self.loader().files))
        self.assertEqual(3, len(self.loader(test='csv$').files))
        self.assertEqual(6, len(self.loader(max_depth=-1).files))
        self.assertEqual(1, len(self.loader(test=lambda x: x.endswith('e.txt'), max_depth=-1).files))

    def test_direct_children(self):
        data = self.loader(target_column=-1)

        self.assertEqual(40, data.num_samples)
        self.assertEqual(3, data.num_columns)
        self.assertEqual(10, data.num_classes)

    def test_direct_children_infer_target(self):
        data = self.loader()

        self.assertEqual(40, data.num_samples)
        self.assertEqual(4, data.num_columns)
        self.assertEqual(4, data.num_classes)

    def test_recursive_infer_target(self):
        data = self.loader(max_depth=-1)

        self.assertEqual(60, data.num_samples)
        self.assertEqual(4, data.num_columns)
        self.assertEqual(6, data.num_classes)

    def test_classmap(self):
        data = self.loader()
        self.assertEqual(4, len(data.classmap))
        self.assertEqual('a', data.classmap[0])

    def test_columns(self):
        data = self.loader(usecols=['b', 'a'])
        self.assertEqual(2, data.num_columns)

    def loader(self, **kwargs):
        """
        Create loader with smart defaults
        :param kwargs:
        :return:
        """
        return FolderLoader('folder', ignore=r'\.py$', **kwargs)
