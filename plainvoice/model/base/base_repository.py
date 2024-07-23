'''
BaseRepository Class

This class is for loading and saving from files for the Base class. It also
contains a rename method. In generall it is used in the Base class as a
component.

Itself has the File class as a component for the file operations. Yet also
for absolute filepath generation.
'''


from plainvoice.model.file.file import File


class BaseRepository:

    def __init__(
        self,
        folder: str = '.',
        filename_pattern: str = '{id}'
    ):
        '''
        The base class for loading / saving certain objects.
        It contains some very basic functionality, which might
        be needed for more than just one object type.
        '''
        self.file = File(folder, 'yaml', filename_pattern)

    def get_files_of_data_type(self) -> list:
        '''
        Get a list containing all the filepaths to the documents
        with the given document type.

        Returns:
            list: Returns a list with filepath strings.
        '''
        return self.file.find_of_type()

    def get_list(self, show_only_visible: bool = True) -> list:
        '''
        Get a list of all available data objects as dicts.

        Args:
            show_only_visible (bool): \
                Show only the documents with the attribute set \
                to "self.visivble = True" in the output list. \
                Here it's data['visible'], since they are still \
                dicts, of course.

        Returns:
            list: Returns a list with the document objects.
        '''
        data_files = self.get_files_of_data_type()
        data_list = []
        for data_file in data_files:
            tmp_data = self.file.load_from_yaml_file(data_file)
            tmp_data['name'] = self.file.extract_name_from_path(data_file)
            add_me = (
                (show_only_visible and tmp_data['visible'])
                or not show_only_visible
            )
            if add_me:
                data_list.append(tmp_data)
        return data_list

    def get_next_id(self) -> str:
        """
        Get the next possible id according to the set folder, the including
        files and the set filename pattern.

        Returns:
            str: Returns an id string.
        """
        return self.file.get_next_id(
            self.file.find_of_type(
                self.file.get_folder(),
                self.file.get_extension()
            )
        )

    def load_from_name(self, name: str) -> dict:
        '''
        Load the data from just the given data name string
        It will do the rest automatically by looking into the
        programs data dir folder for the correct file.

        Args:
            name (str): The name string of the data object.

        Returns:
            dict: Returns the loaded dict or otherwise an empty one.
        '''
        if self.file.exists(name):
            return self.file.load_from_yaml_file(name)
        else:
            return {}

    def rename(self, old_name: str, new_name: str) -> bool:
        """
        This method basically just moves the old file to the
        new name file.

        Args:
            old_name (str): The old name.
            new_name (str): The new name to use.

        Returns:
            bool: Returns True on success.
        """
        if self.file.exists(new_name):
            return False
        else:
            return self.file.rename(old_name, new_name)

    def save(self, content: str, name: str) -> bool:
        """
        Save the content to the automatically generated file.

        Args:
            content (str): \
                The content to be stored. It should be a YAML string, \
                probably generated through the base's to_yaml_string() \
                method.
            name (str): \
                The name of the object, which is used for \
                generating the filename as well.

        Returns:
            bool: Returns True on success.
        """
        return self.file.save_to_file(content, name, False)

    def set_filename_pattern(self, filename_pattern: str) -> None:
        """
        Set the data filename pattern.

        Args:
            filename_pattern (str): The filename pattern for the data.
        """
        self.file.set_filename_pattern(filename_pattern)

    def set_folder(self, folder: str) -> None:
        """
        Set the data folder.

        Args:
            folder (str): The folder for the data.
        """
        self.file.set_folder(folder)
