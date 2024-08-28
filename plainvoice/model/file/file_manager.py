from .file_path_generator import FilePathGenerator

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
            target_directory = os.path.dirname(target)
            if (
                not os.path.exists(target_directory)
                and target_directory is not None
                and target_directory != ''
            ):
                os.makedirs(target_directory)
            with open(source, 'rb') as src_file:
                content = src_file.read()
            with open(target, 'wb') as target_file:
                target_file.write(content)
            return True
        except Exception:
            return False

    def exists(self, name: str) -> bool:
        '''
        Check if the given name exists as a file.

        Args:
            name (str): The name to convert to a filename.

        Returns:
            bool: Returns True if file does exist.
        '''
        return os.path.exists(
            self.file_path_generator.generate_absolute_filename(
                name
            )
        )

    def exist_check(self, name: str) -> None:
        '''
        Raise an error if the given file does not exist.
        Filename gets automatically generated from the
        given name.

        Args:
            name (str): The name to convert to a filename.

        Raises:
            Exception: Error if the file does not exist.
        '''
        if not self.exists(name):
            raise Exception(f'File "{name}" does not exist!')

    def find_of_type(
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

    def get_names_list(self, path: str = '') -> list:
        '''
        Get the files in the given path as a list, yet without the file
        extension.

        Args:
            path (str): The path to scan.

        Returns:
            list: \
                The list containing the files in the path with only the \
                extension.
        '''
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

    def load_from_file(self, name: str) -> str:
        '''
        Loads the given name and returns a dict from it.
        The filename will be generated from the given
        name.

        Args:
            name (str): \
                Uses name as a relative filename relative to \
                the programs data dir. Also it is not neccessary \
                to use .yaml as an extension for the filename.

        Returns:
            str: The dict with the data loaded from the file.
        '''
        name = self.file_path_generator.generate_absolute_filename(
            name
        )
        self.exist_check(name)

        with open(name, 'r') as any_file:
            data = any_file.read()

        return data

    def load_from_yaml_file(self, name: str) -> dict:
        '''
        Loads the given name and returns a dict from it.

        Args:
            name (str): \
                Uses name as a relative filename relative to \
                the programs data dir. Also it is not neccessary \
                to use .yaml as an extension for the filename.

        Returns:
            dict: The dict with the data loaded from the file.
        '''
        name = self.file_path_generator.generate_absolute_filename(
            name
        )
        self.exist_check(name)

        with open(name, 'r') as yaml_file:
            data = yaml.load(yaml_file, Loader=yaml.SafeLoader)

        return data

    def remove(self, name: str) -> bool:
        '''
        Remove the given name, which will generate
        the correct filename to use.

        Args:
            name (str): The name to convert to a filename.

        Returns:
            bool: Returns True on success.
        '''
        try:
            os.remove(
                self.file_path_generator.generate_absolute_filename(
                    name
                )
            )
            return True
        except Exception:
            return False

    def rename(self, old_name: str, new_name: str) -> bool:
        '''
        Simply renames a file. It generates the filenames
        by the given names automatically.

        Args:
            old_name (str): The old name.
            new_name (str): The new name.

        Returns:
            bool: Returns True on success.
        '''
        try:
            os.rename(
                self.file_path_generator.generate_absolute_filename(
                    old_name
                ),
                self.file_path_generator.generate_absolute_filename(
                    new_name
                )
            )
            return True
        except Exception:
            return False

    def save_to_file(self, data: str, name: str) -> bool:
        '''
        Save the given data to the file with the given name
        and returns a bool if succeeded. The filename will
        be generated from the given name.

        Args:
            data (str): \
                The data as dict to be saved into the file.
            name (str): \
                Uses name as a relative filename relative to \
                the programs data dir. Also it is not neccessary \
                to use .yaml as an extension for the filename.

        Returns:
            bool: True if saving was successful.
        '''
        try:
            name = (
                self.file_path_generator.generate_absolute_filename(
                    name
                )
            )
            directory = os.path.dirname(name)
            if (
                not os.path.exists(directory)
                and directory is not None
                and directory != ''
            ):
                os.makedirs(directory)

            with open(name, 'w') as any_file:
                any_file.write(data)

            return True
        except Exception:
            return False
