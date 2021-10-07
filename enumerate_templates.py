import json
from glob import glob


if __name__ == '__main__':
    templates = [filename.replace('everywhereml/', '')
     for filename in glob('everywhereml/templates/**/*.jinja', recursive=True)]

    print(json.dumps(templates).replace('/', '\\/').replace('"', '\\"'))