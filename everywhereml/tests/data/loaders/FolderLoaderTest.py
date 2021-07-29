import os
import os.path
from unittest import TestCase
from numpy.testing import assert_array_equal
from everywhereml.data.loaders import FolderLoader


class FolderLoaderTest(TestCase):
    def setUp(self):
        os.chdir(os.path.join(os.path.dirname(__file__), 'example_files'))

    def test_walk(self):
        self.assertEqual(4, len(FolderLoader('folder').files))
        self.assertEqual(3, len(FolderLoader('folder', test='csv$').files))
        self.assertEqual(6, len(FolderLoader('folder', max_depth=-1).files))
        self.assertEqual(1, len(FolderLoader('folder', test=lambda x: x.endswith('e.txt'), max_depth=-1).files))

    def test_direct_children(self):
        data = FolderLoader('folder', target_column=-1)

        self.assertEqual(40, data.num_samples)
        self.assertEqual(3, data.num_columns)
        self.assertEqual(10, data.num_classes)

    def test_direct_children_infer_target(self):
        data = FolderLoader('folder')

        self.assertEqual(40, data.num_samples)
        self.assertEqual(4, data.num_columns)
        self.assertEqual(4, data.num_classes)

    def test_recursive_infer_target(self):
        data = FolderLoader('folder', max_depth=-1)

        self.assertEqual(60, data.num_samples)
        self.assertEqual(4, data.num_columns)
        self.assertEqual(6, data.num_classes)

    def test_classmap(self):
        data = FolderLoader('folder')
        self.assertEqual(4, len(data.classmap))
        self.assertEqual('a', data.classmap[0])

    def test_columns(self):
        data = FolderLoader('folder', usecols=['b', 'a'])
        self.assertEqual(2, data.num_columns)
