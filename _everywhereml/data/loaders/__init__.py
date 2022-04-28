from everywhereml.data.loaders.FileLoader import FileLoader
from everywhereml.data.loaders.FolderLoader import FolderLoader
from everywhereml.data.loaders.ToyDatasetLoader import ToyDatasetLoader as ToyDatasetLoaderClass

# singleton
ToyDatasetLoader = ToyDatasetLoaderClass()
