from plainvoice.model.config import Config
from plainvoice.view import error_printing

import os
import yaml


class FileManager:
    def __init__(
        self,
        folder: str = '.',
        extension: str = 'yaml'
    ):
        """
        Manager which loads and saves files. E.g. from the
        programms home / config folder.

        Args:
            folder (str|None): \
                Tells, if the dotfolder of the program in the home folder \
                should be used automatically for storing relatively to it \
                or use a given string. If the string contains '{pv}', this \
                will be replaced by the data dir in the home folder of the \
                program. That way you can still use the data dir in the \
                home folder, by entering a string, yet relatively to the \
                data dir of the program. Default is set with None, which \
                means to use the programs data dir root. (default: `None`)
            extension (str): \
                The extension with which the FileManager should work. \
                (default: `'yaml'`)
        """
        self.datadir = Config().datadir
        """
        The path to the data dir of plainvoice. Probably it will be
        ~/.plainvoice by default.
        """

        self.extension = extension.replace('.', '')
        """
        The extension with which the FileManager should work. By
        default it is 'yaml'.
        """

        self.folder = folder
        """
        Tells, if the dotfolder of the program in the home folder
        should be used automatically for storing relatively to it
        or use a given string. If the string contains '{pv}', this
        will be replaced by the data dir in the home folder of the
        program. That way you can still use the data dir in the
        home folder, by entering a string, yet relatively to the
        data dir of the program.
        """

        # add the represent function to the dumper options
        yaml.add_representer(str, self.represent_multiline_str)

    def auto_append_extension(self, filename: str) -> str:
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

        Returns:
            str: The filename including the extension.
        """
        full_extension_lower = '.' + self.extension.lower()
        full_extension_upper = '.' + self.extension.upper()
        if (
            full_extension_lower not in filename
            and full_extension_upper not in filename
        ):
            return filename + full_extension_lower
        else:
            return filename

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

    def file_exists(self, filename: str) -> bool:
        """
        Check if the given filename exists.

        Args:
            filename (str): Argument description

        Returns:
            bool: Returns True if file does exist.
        """
        return os.path.exists(self.generate_correct_filename(filename))

    def find_files_of_type(
        self,
        directory: str = '',
        file_extension: str = ''
    ):
        """
        Find all files in the given directory and its subdirectories with
        the specified file extension.

        Args:
            directory (str): The directory to search in.
            file_extension (str): The file extension to look for (e.g. 'txt').

        Returns:
            list[str]: A list of file paths that match the file extension.
        """
        if directory == '':
            directory = self.get_folder()
        if file_extension == '':
            file_extension = self.extension

        matching_files = []

        # Walk through the directory and all its subdirectories
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(file_extension):
                    matching_files.append(os.path.join(root, file))

        return matching_files

    def generate_correct_filename(self, filename: str) -> str:
        """
        Generates the correct filename string by appending the
        file extension and also generating the absolute filename,
        e.g. if the file is supposed to be in the programs data dir.

        Args:
            filename (str): \
                The filename. Either relative to the programs data dir \
                or with the given self.folder variable as the user set \
                data folder.

        Returns:
            str: Returns the new filename.
        """
        filename = self.auto_append_extension(filename)
        # only generate the path automatically if the given
        # filename probably is not absolute
        if filename[0] not in ['.', '/']:
            filename = os.path.join(self.get_folder(), filename)
        return filename

    def get_files_list(self, path: str) -> list:
        """
        Get the files in the given path as a list , yet without the file
        extension. Also if in_data_dir==True, use the path argument
        relatively to the ~/.plainvoice folder.

        Args:
            path (str): The path to scan.

        Returns:
            list: \
                The list containing the files in the path with only the \
                extension.
        """
        path = os.path.dirname(path)
        path = os.path.join(self.get_folder(), path)

        files_with_extension = []

        for filename in os.listdir(path):
            if filename.endswith(self.extension):
                files_with_extension.append(
                    filename.replace(f'.{self.extension}', '')
                )

        return files_with_extension

    def get_folder(self) -> str:
        """
        Returns the user set folder as the data dir, or the
        programs default data dir if None is set for self.folder.

        Returns:
            str: The folder to work in with saving / loading files.
        """
        if self.folder is None:
            return self.datadir
        else:
            """
            The self.folder string can contain '{pv}' or '{pv}',
            which then will be converted to the programs data dir
            like "/home/user/.plainvoice". This way a user given
            folder like '{pv}/clients' can be converted to
            "/home/user/.plainvoice/clients"
            """
            if '{pv}' in self.folder or '{PV}' in self.folder:
                return os.path.join(
                    self.datadir,
                    self.folder.replace('{pv}/', '').replace('{PV}/', '')
                )
            else:
                return self.folder

    def load_from_file(self, filename: str) -> str:
        """
        Loads the given filename and returns a dict from it.

        Args:
            filename (str): \
                Uses filename as a relative filename relative to \
                the programs data dir. Also it is not neccessary \
                to use .yaml as an extension for the filename.

        Returns:
            str: The dict with the data loaded from the file.
        """
        filename = self.generate_correct_filename(filename)
        self.file_exist_check(filename)

        with open(filename, 'r') as any_file:
            data = any_file.read()

        return data

    def load_from_yaml_file(self, filename: str) -> dict:
        """
        Loads the given filename and returns a dict from it.

        Args:
            filename (str): \
                Uses filename as a relative filename relative to \
                the programs data dir. Also it is not neccessary \
                to use .yaml as an extension for the filename.

        Returns:
            dict: The dict with the data loaded from the file.
        """
        filename = self.generate_correct_filename(filename)
        self.file_exist_check(filename)

        with open(filename, 'r') as yaml_file:
            data = yaml.load(yaml_file, Loader=yaml.SafeLoader)

        return data

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

    def remove(self, filename: str) -> bool:
        """
        Remove the given filename.

        Args:
            filename (str): The filename to remove / delete.

        Returns:
            bool: Returns True on success.
        """
        try:
            os.remove(self.generate_correct_filename(filename))
            return True
        except Exception as e:
            error_printing.print_if_verbose(e)
            return False

    def save_to_file(
        self,
        data,
        filename: str,
        follow_extension: bool = True
    ) -> bool:
        """
        Save the given data to the file with the given filename
        and returns a bool if succeeded.

        Args:
            data (dict | str): \
                The data as dict to be saved into the file.

            filename (str): \
                Uses filename as a relative filename relative to \
                the programs data dir. Also it is not neccessary \
                to use .yaml as an extension for the filename.

            follow_extension (bool): \
                If True, the save method will save as a YAML file, \
                if the extension of the FileManager is set to it.

        Returns:
            bool: True if saving was successful.
        """
        try:
            filename = self.generate_correct_filename(filename)
            directory = os.path.dirname(filename)
            if (
                not os.path.exists(directory)
                and directory is not None
                and directory != ''
            ):
                os.makedirs(directory)

            if self.extension in ['yaml', 'YAML'] and follow_extension:
                with open(filename, 'w') as yaml_file:
                    yaml.dump(
                        data,
                        yaml_file,
                        default_flow_style=False,
                        allow_unicode=True,
                        sort_keys=False
                    )
            else:
                with open(filename, 'w') as any_file:
                    any_file.write(data)
            return True
        except Exception as e:
            error_printing.print_if_verbose(e)
            return False

    def to_yaml_string(self, data: dict) -> str:
        """
        Convert a dict to a YAML string as it would be saved.

        Args:
            data (dict): The dict, which should be converted to a YAML string.

        Returns:
            str: Returns the YAML string.
        """
        return yaml.dump(
            data,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False
        )
