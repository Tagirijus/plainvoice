from plainvoice.model.filemanager import FileManager
from plainvoice.view import error_printing


class DataLoader:
    """
    The base class for certain objects. It contains some
    very basic functionality, which might be needed
    for more than just one object type.
    """

    def from_dict(self, values: dict) -> None:
        """
        This is basically an abstract method, which
        should be overwritten by the child.

        Args:
            values (dict): The dict to load the attributes from.
        """
        pass

    def load_from_name(self, name: str, folder: str) -> bool:
        """
        Wrapper for the _load_from_name() method to let the
        child objects handle the default arguments.

        Args:
            name (str): The name of the object to load.
            folder (str): The folder where such objects are stored.

        Returns:
            bool: Returns True on success.
        """
        return self._load_from_name(name, folder)

    def _load_from_name(self, name: str, folder: str = '{pv}/types') -> bool:
        """
        Load the document type from just the given document
        type name string. It will do the rest automatically
        by looking into the programs data dir folder 'types/'
        for the correct file.

        Args:
            name (str): \
                The name string of the document type. The method \
                will look in the programs data dir 'types/' folder \
                to find the fitting document type automatically.
            folder (str): \
                The folder where such objects are stored.

        Returns:
            bool: Returns True on success.
        """
        try:
            # Using the FileManager here feels like having a bit high
            # dependency for this object. Yet I am not sure how to
            # code this in a more elegant way, yet.
            fm = FileManager(folder)
            document_type_dict = fm.load_from_yaml_file(name)
            self.from_dict(document_type_dict)
            return True
        except Exception as e:
            error_printing.print_if_verbose(e)
            return False
