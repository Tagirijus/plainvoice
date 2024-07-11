from model.settings import Settings
from view import error_printing

import os
import yaml


class Files:
    """
    Controller which manages to load and save files from the
    programms home / config folder. It works primary with
    YAML format at the point of writing this.
    """

    DATADIR: str
    """
    The path to the data dir of plainvoice. Probably it will be
    ~/.plainvoice by default.
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

    def auto_append_extension(
        self,
        filename: str,
        extension: str = 'yaml'
    ) -> str:
        """
        With this method you can append a file extension to
        the given filename string. It can contain a dot
        or not, this does not matter. Also if the filename
        already has the extension (lower or upper case), it
        won't be changed.

        The appended file extension, if it does not exist,
        is lower case always.

        Args:
            filename (str): The filename to append the extension to.
            extension (str): The extension to append. (default: `'yaml'`)
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

    def file_exists(self, filename: str) -> bool:
        """
        Check if the given filename exists.

        Args:
            filename (str): Argument description

        Returns:
            bool: Returns True if file does exist.
        """
        return os.path.exists(filename)

    def file_exist_check(self, filename: str) -> None:
        """
        Raise an error if the given file with the
        filename does not exist.

        Args:
            filename (str): The filename to check.

        Raises:
            Exception: Error if the file does not exist.
        """
        if not self.file_exists(filename):
            raise Exception(f'File "{filename}" does not exist!')

    def generate_correct_filename(
        self,
        filename: str,
        extension: str = 'yaml',
        in_data_dir: bool = True
    ) -> str:
        """
        Generates the correct filename string by appending the
        file extension and also generating the absolute filename
        if the file is supposed to be in the programs data dir.

        Args:
            filename (str): The filename
            extension (str): The extension. (default: `'yaml'`)
            in_data_dir (bool): Is this file in the data dir? (default: `True`)

        Returns:
            str: Returns the new filename.
        """
        filename = self.auto_append_extension(filename, extension)
        if in_data_dir:
            filename = os.path.join(self.DATADIR, filename)
        return filename

    def load_dict_from_yaml_file(
        self,
        filename: str,
        in_data_dir: bool = True
    ) -> dict:
        """
        Loads the given filename and returns a dict from it.

        Args:
            filename (str): \
                Uses filename as a relative filename relative to \
                the programs data dir. Also it is not neccessary \
                to use .yaml as an extension for the filename.

            in_data_dir (bool): \
                True, if file is in data dir. (default: `True`)

        Returns:
            dict: The dict with the data loaded from the file.
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

    def save_dict_to_yaml_file(
        self,
        data: dict,
        filename: str,
        in_data_dir: bool = True
    ) -> bool:
        """
        Save the given data to the file with the given filename
        and returns a bool if succeeded.

        Args:
            data (dict): \
                The data as dict to be saved into the file.

            filename (str): \
                Uses filename as a relative filename relative to \
                the programs data dir. Also it is not neccessary \
                to use .yaml as an extension for the filename.

            in_data_dir (bool): \
                True, if file is in data dir. (default: `True`)

        Returns:
            bool: True if saving was successful.
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

    def load_string_from_python_file(
        self,
        filename: str,
        in_data_dir: bool = True
    ) -> str:
        """
        Loads the given filename and returns a string from it.

        Args:
            filename (str): \
                Uses filename as a relative filename relative to \
                the programs data dir. Also it is not neccessary \
                to use .py as an extension for the filename.

            in_data_dir (bool): \
                True, if file is in data dir. (default: `True`)

        Returns:
            str: The python code string.
        """
        filename = self.generate_correct_filename(filename, 'py', in_data_dir)
        self.file_exist_check(filename)

        with open(filename, 'r') as shell_file:
            data = shell_file.read()

        return data

    def get_files_list(
        self,
        path: str,
        extension: str = 'yaml',
        in_data_dir: bool = True
    ) -> list:
        """
        Get the files in the given path as a list , yet without the file
        extension. Also if in_data_dir==True, use the path argument
        relatively to the ~/.plainvoice folder.

        Args:
            path (str): The path to scan.
            extension (str): The extension to scan for. (default: `'yaml'`)
            in_data_dir (bool): Is it a folder in data dir? (default: `True`)

        Returns:
            list: \
                The list containing the files in the path with only the \
                extension.
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

    def copy(self, source: str, target: str) -> bool:
        """
        Copy one file to another location.

        Args:
            source (str): The filename of the source file.
            target (str): The target filename for the copy.

        Returns:
            bool: Returns True on success.
        """
        try:
            with open(source, 'rb') as src_file:
                content = src_file.read()
            with open(target, 'wb') as target_file:
                target_file.write(content)
            return True
        except Exception as e:
            error_printing.print_if_verbose(e)
            return False

    def remove(self, filename: str) -> bool:
        """
        Remove the given filename.

        Args:
            filename (str): The filename to remove / delete.

        Returns:
            bool: Returns True on success.
        """
        try:
            os.remove(filename)
            return True
        except Exception as e:
            error_printing.print_if_verbose(e)
            return False
