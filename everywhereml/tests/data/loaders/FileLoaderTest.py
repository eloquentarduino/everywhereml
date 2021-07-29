import os
import os.path
from unittest import TestCase
from numpy.testing import assert_array_equal
from everywhereml.data.loaders import FileLoader


class FileLoaderTest(TestCase):
    def setUp(self):
        os.chdir(os.path.join(os.path.dirname(__file__), 'example_files'))

    def test_no_columns(self):
        data = FileLoader('no_columns.txt', delimiter=' ')

        self.assertEqual(10, data.num_samples)
        self.assertEqual(3, data.num_columns)
        self.assertEqual(['c00', 'c01', 'c02'], data.columns)

    def test_skiprows(self):
        data = FileLoader('no_columns.csv', skiprows=1, nrows=5)

        self.assertEqual(5, data.num_samples)
        self.assertEqual(3, data.num_columns)
        assert_array_equal([4, 5, 6], data.X[0])

    def test_default_columns(self):
        data = FileLoader('columns.csv')

        self.assertEqual(['a', 'b', 'c'], data.columns)

    def test_custom_columns(self):
        data = FileLoader('columns.csv', usecols=['a', 'c'], target_column='b')

        self.assertEqual(['a', 'c'], data.columns)
        self.assertEqual(1, data.y[0])

    def test_no_target_column(self):
        data = FileLoader('columns.csv', target_column=None)

        self.assertEqual(4, len(data.columns))
