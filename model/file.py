from model.settings import Settings
from view import error_printing

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
            return dumper.represent_scalar(
                'tag:yaml.org,2002:str', data, style='|'
            )
        return dumper.represent_scalar('tag:yaml.org,2002:str', data)

    def auto_append_extension(self, filename, extension='yaml'):
        """
        With this method you can append a file extension to
        the given filename string. It can contain a dot
        or not, this does not matter. Also if the filename
        already has the extension (lower or upper case), it
        won't be changed.

        The appended file extension, if it does not exist,
        is lower case always.
        """
        full_extension_lower = '.' + extension.replace('.', '').lower()
        full_extension_upper = '.' + extension.replace('.', '').upper()
        if (
            full_extension_lower not in filename
            and full_extension_upper not in filename
        ):
            return filename + full_extension_lower
        else:
            return filename

    def file_exist_check(self, filename):
        """
        Raise an error if the given file with the
        filename does not exist.
        """
        if not os.path.exists(filename):
            raise Exception(f'File "{filename}" does not exist!')

    def generate_correct_filename(
        self, filename, extension='yaml', in_data_dir=True
    ):
        """Make something."""
        filename = self.auto_append_extension(filename, extension)
        if in_data_dir:
            filename = os.path.join(self.DATADIR, filename)
        return filename

    def load_dict_from_yaml_file(self, filename, in_data_dir=True):
        """
        Uses filename as a relative filename relative to
        the programms home folder.

        Also it is not neccessary to use .yaml as an extension for the
        filename.
        """
        filename = self.generate_correct_filename(
            filename,
            'yaml',
            in_data_dir
        )
        self.file_exist_check(filename)

        with open(filename, 'r') as yaml_file:
            data = yaml.load(yaml_file, Loader=yaml.SafeLoader)

        return data

    def save_dict_to_yaml_file(self, data, filename, in_data_dir=True):
        """
        Uses the filename as a relative filename relative to
        the programms home folder. Optionally you can set
        with in_data_dir=False to use the given filename like a normal
        filename.

        Also it is not neccessary to use .yaml as an extension for the
        filename.
        """
        try:
            filename = self.generate_correct_filename(
                filename,
                'yaml',
                in_data_dir
            )
            directory = os.path.dirname(filename)
            if (
                not os.path.exists(directory)
                and directory is not None
                and directory != ''
            ):
                os.makedirs(directory)
            with open(filename, 'w') as yaml_file:
                yaml.dump(
                    data, yaml_file,
                    default_flow_style=False,
                    allow_unicode=True,
                    sort_keys=False
                )
            return True
        except Exception as e:
            error_printing.print_if_verbose(e)
            return False

    def load_string_from_python_file(self, filename, in_data_dir=True):
        """
        Uses filename as a relative filename relative to
        the programms home folder.

        Also it is not neccessary to use .py as an extension for the filename.
        """
        filename = self.generate_correct_filename(filename, 'py', in_data_dir)
        self.file_exist_check(filename)

        with open(filename, 'r') as shell_file:
            data = shell_file.read()

        return data

    def get_files_list(self, path, extension='yaml', in_data_dir=True):
        """
        Get the files in the given path as a list , yet without the file
        extension. Also if in_data_dir==True, use the path argument
        relatively to the ~/.plainvoice folder.
        """
        path = os.path.dirname(path)
        if in_data_dir:
            path = os.path.join(self.DATADIR, path)

        files_with_extension = []

        for filename in os.listdir(path):
            if filename.endswith(extension):
                files_with_extension.append(
                    filename.replace(f'.{extension}', '')
                )

        return files_with_extension
