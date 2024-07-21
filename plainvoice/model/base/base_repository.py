from plainvoice.model.file.file import File
from plainvoice.view.printing import Printing


class BaseRepository:

    def __init__(
        self,
        folder: str = '.'
    ):
        '''
        The base class for loading / saving certain objects.
        It contains some very basic functionality, which might
        be needed for more than just one object type.
        '''
        self.file = File(folder)

    def load_from_id(self, id: str) -> dict:
        '''
        Load a document or document type from its plain id.

        Args:
            id (str): The id of the document or type.

        Returns:
            dict: Returns the loaded dict or otherwise an empty one.
        '''
        # WEITER HIER
        # TODO
        # Ähnlich wie load_from_name(), aber die Methode
        # lädt sämtliche Objetkte aus dem Ordner und
        # findet das passende mit der ID (das erste)
        return {}

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

    def set_folder(self, folder: str) -> None:
        """
        Set the data folder.

        Args:
            folder (str): The folder for the data.
        """
        self.file.set_folder(folder)
