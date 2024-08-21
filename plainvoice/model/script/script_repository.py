'''
ScriptRepository Class

This class is for loading scripts from the scripts folder by name
and returns Script objects.
'''

from plainvoice.model.data.data_repository import DataRepository
from plainvoice.model.file.file import File
from plainvoice.model.script.script import Script


class ScriptRepository(DataRepository):
    '''
    This class can load Script objects by name from the scripts folder.
    '''

    DEFAULT_SCRIPTS_FOLDER: str = '{app_dir}/scripts'
    '''
    The folder, in which the scripts are stored by default.
    '''

    def __init__(
        self,
        scripts_folder: str = DEFAULT_SCRIPTS_FOLDER
    ):
        '''
        The main class for loading / saving certain data objects.
        It contains some very basic functionality, which might
        be needed for more than just one object type.

        Args:
            scripts_folder (str): \
                The folder of the scripts.
        '''
        self.file = File(scripts_folder, 'py')

    def load(self, name: str) -> Script:
        '''
        Load a Script object by name.

        Args:
            name (str): The name of the script.

        Returns:
            Script: Returns the Script object.
        '''
        return Script(
            self.load_string_from_name(name)
        )
