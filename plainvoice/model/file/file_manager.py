from .file_path_generator import FilePathGenerator
from plainvoice.view.printing import Printing

import os
import yaml


class FileManager:
    def __init__(self, file_path_generator: FilePathGenerator):
        '''
        The manager to save and load data from / to files.
        It gives certain file operatrion features.
        '''
        self.file_path_generator = file_path_generator
        '''
        The FilePathGenerator to have access to some helper
        methods for generating file and folder strings.
        '''

        # add the represent function to the dumper options
        yaml.add_representer(str, self.represent_multiline_str)

    def copy(self, source: str, target: str) -> bool:
        '''
        Copy one file to another location.

        Args:
            source (str): The filename of the source file.
            target (str): The target filename for the copy.

        Returns:
            bool: Returns True on success.
        '''
        try:
            with open(source, 'rb') as src_file:
                content = src_file.read()
            with open(target, 'wb') as target_file:
                target_file.write(content)
            return True
        except Exception as e:
            Printing.print_if_verbose(e)
            return False

    def file_exist_check(self, filename: str) -> None:
        '''
        Raise an error if the given file with the
        filename does not exist.

        Args:
            filename (str): The filename to check.

        Raises:
            Exception: Error if the file does not exist.
        '''
        if not self.file_exists(filename):
            raise Exception(f'File "{filename}" does not exist!')

    def file_exists(self, filename: str) -> bool:
        '''
        Check if the given filename exists.

        Args:
            filename (str): Argument description

        Returns:
            bool: Returns True if file does exist.
        '''
        return os.path.exists(
            self.file_path_generator.generate_correct_filename(
                filename
            )
        )

    def find_files_of_type(
        self,
        directory: str = '',
        file_extension: str = ''
    ):
        '''
        Find all files in the given directory and its subdirectories with
        the specified file extension.

        Args:
            directory (str): The directory to search in.
            file_extension (str): The file extension to look for (e.g. 'txt').

        Returns:
            list[str]: A list of file paths that match the file extension.
        '''
        if directory == '':
            directory = self.file_path_generator.get_folder()
        if file_extension == '':
            file_extension = self.file_path_generator.get_extension()

        matching_files = []

        # Walk through the directory and all its subdirectories
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(file_extension):
                    matching_files.append(os.path.join(root, file))

        return matching_files

    def get_files_list(self, path: str) -> list:
        '''
        Get the files in the given path as a list , yet without the file
        extension. Also if in_data_dir==True, use the path argument
        relatively to the ~/.plainvoice folder.

        Args:
            path (str): The path to scan.

        Returns:
            list: \
                The list containing the files in the path with only the \
                extension.
        '''
        path = os.path.dirname(path)
        path = os.path.join(
            self.file_path_generator.get_folder(),
            path
        )

        files_with_extension = []

        for filename in os.listdir(path):
            if filename.endswith(
                self.file_path_generator.get_extension()
            ):
                files_with_extension.append(
                    filename.replace(
                        f'.{self.file_path_generator.get_extension()}',
                        ''
                    )
                )

        return files_with_extension

    def load_from_file(self, filename: str) -> str:
        '''
        Loads the given filename and returns a dict from it.

        Args:
            filename (str): \
                Uses filename as a relative filename relative to \
                the programs data dir. Also it is not neccessary \
                to use .yaml as an extension for the filename.

        Returns:
            str: The dict with the data loaded from the file.
        '''
        filename = self.file_path_generator.generate_correct_filename(
            filename
        )
        self.file_exist_check(filename)

        with open(filename, 'r') as any_file:
            data = any_file.read()

        return data

    def load_from_yaml_file(self, filename: str) -> dict:
        '''
        Loads the given filename and returns a dict from it.

        Args:
            filename (str): \
                Uses filename as a relative filename relative to \
                the programs data dir. Also it is not neccessary \
                to use .yaml as an extension for the filename.

        Returns:
            dict: The dict with the data loaded from the file.
        '''
        filename = self.file_path_generator.generate_correct_filename(
            filename
        )
        self.file_exist_check(filename)

        with open(filename, 'r') as yaml_file:
            data = yaml.load(yaml_file, Loader=yaml.SafeLoader)

        return data

    @staticmethod
    def represent_multiline_str(dumper, data):
        '''
        Define a custom represent function for multiline strings.
        This way multiline strings will get dumped by YAML with
        the pipe newline style.
        '''
        if '\n' in data:
            return dumper.represent_scalar(
                'tag:yaml.org,2002:str', data, style='|'
            )
        return dumper.represent_scalar('tag:yaml.org,2002:str', data)

    def remove(self, filename: str) -> bool:
        '''
        Remove the given filename.

        Args:
            filename (str): The filename to remove / delete.

        Returns:
            bool: Returns True on success.
        '''
        try:
            os.remove(
                self.file_path_generator.generate_correct_filename(
                    filename
                )
            )
            return True
        except Exception as e:
            Printing.print_if_verbose(e)
            return False

    def save_to_file(
        self,
        data,
        filename: str,
        follow_extension: bool = True
    ) -> bool:
        '''
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
        '''
        try:
            filename = (
                self.file_path_generator.generate_correct_filename(
                    filename
                )
            )
            directory = os.path.dirname(filename)
            if (
                not os.path.exists(directory)
                and directory is not None
                and directory != ''
            ):
                os.makedirs(directory)

            if (
                self.file_path_generator.get_extension()
                in ['yaml', 'YAML']
                and follow_extension
            ):
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
            Printing.print_if_verbose(e)
            return False

    @staticmethod
    def to_yaml_string(data: dict) -> str:
        '''
        Convert a dict to a YAML string as it would be saved. This
        method exists in this class, due to the YAML representer
        being changed here.

        Args:
            data (dict): The dict, which should be converted to a YAML string.

        Returns:
            str: Returns the YAML string.
        '''
        return yaml.dump(
            data,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False
        )
