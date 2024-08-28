'''
ScriptRepository Class

This class is for loading scripts from the scripts folder by name
and returns Script objects.
'''

from plainvoice.model.config import Config
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

    def create_script(self, name: str) -> bool:
        '''
        Copy the default script to the scripts folder
        to get a starting point for a new script.

        Args:
            name (str): The name of the new script.

        Returns:
            bool: Returns True on success.
        '''
        project_path = Config().project_path
        default_script_filename = \
            f'{project_path}/assets/script_template.py'

        return self.file.copy(
            default_script_filename,
            self.file.generate_absolute_filename(name)
        )

    def get_script_names(self) -> list[str]:
        '''
        Return a list with only the script names. These are the
        files in the set scripts folder, but without its extension.

        Returns:
            list: Returns list of strings, which are script names.
        '''
        return self.file.get_names_list()

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
