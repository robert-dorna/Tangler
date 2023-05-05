from os import path
import json
import yaml
import sys


class JsonFile:
    def __init__(self, path, on_closed=None):
        self.file = open(path, 'r+')
        self.data = json.load(self.file)
        self.on_closed = on_closed

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def close(self):
        if not self.file.closed:
            self.flush()
            self.file.close()
            if self.on_closed:
                self.on_closed()

    def flush(self):
        if not self.file.closed:
            self.file.truncate(0)
            self.file.seek(0)
            self.file.write(json.dumps(self.data, indent=4, sort_keys=True))


def read_yaml(path):
    with open(path) as f:
        return yaml.safe_load(f)


def write_yaml(path, data):
    with open(path, 'w') as f:
        yaml.safe_dump(data, f)


def read_json(path):
    with open(path, 'r') as f:
        return json.load(f)


project_path = path.dirname(path.realpath(sys.argv[0]))
config_file_path = path.join(project_path, 'tangler.yaml')
config = read_yaml(config_file_path)


DATADIR_PATH = config['directories']['data']
CONFIG_PATH = path.join(DATADIR_PATH, "_config.yaml")