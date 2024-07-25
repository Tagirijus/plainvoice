from .file_manager import FileManager
from .file_path_generator import FilePathGenerator


class File:
    '''
    The abstract layer for the FileController. With this
    class you can controll file operations and also get
    helper methods for generating filepaths or so.
    '''

    def __init__(
        self,
        folder: str = '.',
        extension: str = 'yaml',
        filename_pattern: str = '{id}'
    ):
        '''
        Manager which loads and saves files. E.g. from the
        programs home / config folder.

        Args:
            folder (str|None): \
                Tells, if the dotfolder of the program in the home folder \
                should be used automatically for storing relatively to it \
                or use a given string. If the string contains '{app_dir}', \
                this will be replaced by the data dir in the home folder of \
                the program. That way you can still use the data dir in the \
                home folder, by entering a string, yet relatively to the \
                data dir of the program. Default is set with None, which \
                means to use the programs data dir root. (default: `None`)
            extension (str): \
                The extension with which the FileManager should work. \
                (default: `'yaml'`)
        '''
        self.file_path_generator = FilePathGenerator(
            folder,
            extension,
            filename_pattern
        )
        self.file_manager = FileManager(self.file_path_generator)

    @property
    def copy(self):
        return self.file_manager.copy

    @property
    def exists(self):
        return self.file_manager.exists

    @property
    def exist_check(self):
        return self.file_manager.exist_check

    @property
    def extract_name_from_path(self):
        return self.file_path_generator.extract_name_from_path

    @property
    def find_of_type(self):
        return self.file_manager.find_of_type

    @property
    def generate_absolute_filename(self):
        return self.file_path_generator.generate_absolute_filename

    @property
    def generate_name(self):
        return self.file_path_generator.generate_name

    @property
    def get_extension(self):
        return self.file_path_generator.get_extension

    @property
    def get_names_list(self):
        return self.file_manager.get_names_list

    @property
    def get_folder(self):
        return self.file_path_generator.get_folder

    @property
    def get_next_id(self):
        return self.file_path_generator.get_next_id

    @property
    def load_from_file(self):
        return self.file_manager.load_from_file

    @property
    def load_from_yaml_file(self):
        return self.file_manager.load_from_yaml_file

    @property
    def remove(self):
        return self.file_manager.remove

    @property
    def rename(self):
        return self.file_manager.rename

    @property
    def replace_extension_with_pdf(self):
        return self.file_path_generator.replace_extension_with_pdf

    @property
    def save_to_file(self):
        return self.file_manager.save_to_file

    @property
    def set_extension(self):
        return self.file_path_generator.set_extension

    @property
    def set_filename_pattern(self):
        return self.file_path_generator.set_filename_pattern

    @property
    def set_folder(self):
        return self.file_path_generator.set_folder

    @property
    def to_yaml_string(self):
        return self.file_manager.to_yaml_string
