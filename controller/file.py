from model.settings import Settings
from view import printing as p

import os
import yaml


class File(object):
    """
    Controller which manages to load and save files from the
    programms home / config folder. It works primary with
    YAML format at the point of writing this.
    """

    def __init__(self):
        self.DATADIR = Settings().DATADIR

    def auto_append_yaml(self, filename):
        if not '.yaml' in filename or not '.YAML' in filename:
            return filename + '.yaml'
        else:
            return filename

    def load(self, filename):
        """
        Uses filename as a relative filename relative to
        the programms home folder.

        Also it is not neccessary to use .yaml as an ending for the filename.
        """
        filename = self.auto_append_yaml(filename)
        absolute_filename = os.path.join(self.DATADIR, filename)
        if not os.path.exists(absolute_filename):
            p.print_error(f'Cannot open file "{absolute_filename}"!')
            exit(1)

        with open(absolute_filename, 'r') as yaml_file:
            data = yaml.load(yaml_file, Loader=yaml.SafeLoader)

        return data

    def save(self, filename, data):
        """
        Uses the filename as a relative filename relative to
        the programms home folder.

        Also it is not neccessary to use .yaml as an ending for the filename.
        """
        filename = self.auto_append_yaml(filename)
        try:
            absolute_filename = os.path.join(self.DATADIR, filename)
            directory = os.path.dirname(absolute_filename)
            if not os.path.exists(directory):
                os.makedirs(directory)
            with open(absolute_filename, 'w') as yaml_file:
                yaml.dump(data, yaml_file, default_flow_style=False)
            return True
        except Exception as e:
            p.print_error(f'Could not save to file "{absolute_filename}"!')
            exit(1)
