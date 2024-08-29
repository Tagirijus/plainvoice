'''
DataRepository Class

This class is for loading and saving from files for the DataModel class.
It also contains a rename method.

Itself has the File class as a component for the file operations. Yet also
for absolute filepath generation.
'''

from plainvoice.model.data.data_model import DataModel
from plainvoice.model.file.file import File

from typing import Any


class DataRepository:

    def __init__(
        self,
        folder: str = '',
        filename_pattern: str = ''
    ):
        '''
        The main class for loading / saving certain data objects.
        It contains some very basic functionality, which might
        be needed for more than just one object type.

        Args:
            folder (str): \
                The folder to search the DataModels.
            filename_pattern (str): \
                For generating and fetching info from \
                file names.
        '''
        self.file = File(folder, 'yaml', filename_pattern)

    def exists(self, name: str) -> bool:
        '''
        Check if the given DataModel exists in the repo.

        Args:
            name (str): The name of the DataModel.

        Returns:
            bool: Returns True on success.
        '''
        return self.file.exists(name)

    def get_absolute_filename(self, name: str) -> str:
        '''
        Get the absolute filename according to the set up folder
        and the given name of the DataModel.

        Args:
            name (str): The name of the DataModel.

        Returns:
            str: Returns the absolute filename as a string.
        '''
        return self.file.generate_absolute_filename(name)

    def get_files_of_data_type(self) -> list:
        '''
        Get a list containing all the filepaths to the DataModels
        with the given DataModel type.

        Returns:
            list: Returns a list with filepath strings.
        '''
        return self.file.find_of_type()

    @property
    def get_folder(self):
        return self.file.get_folder

    def get_list(self, show_only_visible: bool = True) -> dict:
        '''
        Get a dict of all available data objects as dicts. The name
        of the DataModel is on the key and the dict with the loaded
        data on the value.

        Args:
            show_only_visible (bool): \
                Show only the DataModels with the attribute set \
                to "self.visivble = True" in the output list. \
                Here it's data['visible'], since they are still \
                dicts, after all.

        Returns:
            dict: Returns a dict with the DataModel objects on their names.
        '''
        data_files = self.get_files_of_data_type()
        data_list = {}
        for data_file in data_files:
            tmp_data = self.file.load_from_yaml_file(data_file)
            name = self.file.extract_name_from_path(data_file)
            add_me = (
                (show_only_visible and tmp_data.get('visible'))
                or not show_only_visible
            )
            if add_me:
                data_list[name] = tmp_data
        return data_list

    def get_next_code(self) -> str:
        '''
        Get the next possible code according to the set folder, the including
        files and the set filename pattern.
        It's a thing I implemented in the first drafts. The idea is that
        an invoice, for example, should have an invoice number. And I want
        the programm ot be able to get the next invoice number ("code") from
        the filenames with the specified pattern.

        Returns:
            str: Returns an code string.
        '''
        return self.file.get_next_code(
            self.file.find_of_type(
                self.file.get_folder(),
                self.file.get_extension()
            )
        )

    def load_string_from_name(self, name: str) -> str:
        '''
        Load the data from just the given data name string.
        It will do the rest automatically by looking into the
        folder, set for this instance.

        Args:
            name (str): The name string of the data object.

        Returns:
            str: Returns the content of the found file as a string.
        '''
        if self.file.exists(name):
            return self.file.load_from_file(name)
        else:
            return ''

    def load_dict_from_name(self, name: str) -> dict[str, Any]:
        '''
        Load the data from just the given data name string.
        It will do the rest automatically by looking into the
        folder, set for this instance.

        Args:
            name (str): The name string of the data object.

        Returns:
            dict: Returns the loaded dict or otherwise an empty one.
        '''
        if self.file.exists(name):
            return self.file.load_from_yaml_file(name)
        else:
            return {}

    def remove(self, name: str) -> bool:
        '''
        Remove the DataModel with the given name.

        Args:
            name (str): The name of the DataModel.

        Returns:
            bool: Returns True on success.
        '''
        if not self.file.exists(name):
            return False
        else:
            return self.file.remove(name)

    def rename(self, old_name: str, new_name: str) -> bool:
        '''
        This method basically just moves the old file to the
        new name file.

        Args:
            old_name (str): The old name.
            new_name (str): The new name to use.

        Returns:
            bool: Returns True on success.
        '''
        if self.file.exists(new_name):
            return False
        else:
            return self.file.rename(old_name, new_name)

    def save(self, data_model: DataModel, name: str = '') -> str:
        '''
        Save the DataModel to the automatically generated file.

        Args:
            data_model (str): \
                The DataModel to be stored.
            name (str): \
                The name of the object, which is used for \
                generating the filename as well.

        Returns:
            str: Returns the absolute filename on success, otherwise ''.
        '''
        final_filename = ''
        if not name:
            name = data_model.get_name()
            if not name:
                return final_filename
        content_to_save = data_model.to_yaml_string()
        if self.file.save_to_file(content_to_save, name):
            final_filename = self.file.generate_absolute_filename(name)
        return final_filename

    @property
    def set_filename_pattern(self):
        return self.file.set_filename_pattern

    @property
    def set_folder(self):
        return self.file.set_folder
