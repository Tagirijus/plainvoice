from plainvoice.model.filemanager import FileManager
from plainvoice import Printing


class BaseRepository:
    '''
    The base class for loading / saving certain objects.
    It contains some very basic functionality, which might
    be needed for more than just one object type.
    '''

    def from_dict(self, values: dict) -> None:
        '''
        This is basically an abstract method, which
        should be overwritten by the child. It is for
        filling the class attributes from a dict.

        Args:
            values (dict): The dict to load the attributes from.
        '''
        raise NotImplementedError('Subclasses should implement from_dict()!')

    def load_from_id(self, id: str) -> bool:
        '''
        Load a document or document type from its plain id.

        Args:
            id (str): The id of the document or type.

        Returns:
            bool: Returns True on success.
        '''
        return False

    def load_from_name(self, name: str, folder: str) -> bool:
        '''
        Wrapper for the _load_from_name() method to let the
        child objects handle the default arguments.

        Args:
            name (str): The name of the object to load.
            folder (str): The folder where such objects are stored.

        Returns:
            bool: Returns True on success.
        '''
        return self._load_from_name(name, folder)

    def _load_from_name(self, name: str, folder: str = '{pv}/types') -> bool:
        '''
        Load the document type from just the given document
        type name string. It will do the rest automatically
        by looking into the programs data dir folder 'types/'
        for the correct file.

        Args:
            name (str): \
                The name string of the document or type. The method \
                will look in the specified folder to find the fitting \
                document or type automatically. You can also use a \
                relative path like './filename' or an absolute filepath \
                like '/home/user/path/to/filename' to be used on loading.
            folder (str): \
                The folder where such objects are stored. Use '{pv}' \
                inside the folder string to use the programs data dir.

        Returns:
            bool: Returns True on success.
        '''
        try:
            # Using the FileManager here feels like having a bit high
            # dependency for this object. Yet I am not sure how to
            # code this in a more elegant way, yet.
            fm = FileManager(folder)
            document_type_dict = fm.load_from_yaml_file(name)
            self.from_dict(document_type_dict)
            return True
        except Exception as e:
            Printing.print_if_verbose(e)
            return False
