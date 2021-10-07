import os
import json
from os.path import isdir
from glob import glob


def package_name(folder):
    if folder.endswith(os.path.sep):
        folder = folder[:-1]

    return folder.replace(os.path.sep, '.')


if __name__ == '__main__':
    packages = [package_name(folder) for folder in glob('everywhereml/**', recursive=True)
                if isdir(folder) and '__pycache__' not in folder]

    print(json.dumps(packages).replace('/', '\\/').replace('"', '\\"'))