from model.settings import Settings
from view import printing as p

import os
import yaml


class File:
    """
    Controller which manages to load and save files from the
    programms home / config folder. It works primary with
    YAML format at the point of writing this.
    """

    def __init__(self):
        self.DATADIR = Settings().DATADIR

        # add the represent function to the dumper options
        yaml.add_representer(str, self.represent_multiline_str)

    @staticmethod
    def represent_multiline_str(dumper, data):
        """
        Define a custom represent function for multiline strings.
        This way multiline strings will get dumped by YAML with
        the pipe newline style.
        """
        if '\n' in data:
            return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
        return dumper.represent_scalar('tag:yaml.org,2002:str', data)


    def auto_append_yaml(self, filename):
        if not '.yaml' in filename or not '.YAML' in filename:
            return filename + '.yaml'
        else:
            return filename

    def load(self, filename, in_data_dir=True):
        """
        Uses filename as a relative filename relative to
        the programms home folder.

        Also it is not neccessary to use .yaml as an ending for the filename.
        """
        filename = self.auto_append_yaml(filename)
        if in_data_dir:
            filename = os.path.join(self.DATADIR, filename)
        if not os.path.exists(filename):
            raise Exception(f'Cannot open file "{filename}"!')

        with open(filename, 'r') as yaml_file:
            data = yaml.load(yaml_file, Loader=yaml.SafeLoader)

        return data

    def save(self, data, filename):
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
                yaml.dump(
                    data, yaml_file,
                    default_flow_style=False,
                    allow_unicode=True,
                    sort_keys=False
                )
            return True
        except Exception as e:
            p.print_error(f'Could not save to file "{absolute_filename}"!')
            exit(1)
