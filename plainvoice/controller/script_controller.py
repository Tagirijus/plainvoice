'''
ScriptController class

Handles Script managing.
'''

from plainvoice.controller.io_facade.io_facade import IOFacade as io
from plainvoice.model.config import Config
from plainvoice.model.script.script_repository import ScriptRepository
from plainvoice.utils import file_utils


class ScriptController:
    '''
    Handles Script managing.
    '''

    def __init__(self):
        '''
        Handles Script managing.
        '''
        self.script_repo = ScriptRepository(str(Config().get('scripts_folder')))

    def edit(self, name: str) -> None:
        '''
        Edit the script with the given name. If it does not
        exist, create a new one from hard-coded asset.

        Args:
            name (str): The name of the script.
        '''
        if not self.script_repo.exists(name):
            self.script_repo.create_script(name)
        file_utils.open_in_editor(self.script_repo.get_absolute_filename(name))

    def list(self) -> None:
        '''
        List templates.
        '''
        io.print_list(sorted(self.script_repo.get_script_names()))

    def remove(self, name: str) -> None:
        '''
        Remove the document type with the given name.

        Args:
            name (str): The name of the document type.
        '''
        if self.script_repo.exists(name):
            if io.ask_yes_no(f'Remove script "{name}"?'):
                self.script_repo.remove(name)
                io.print(f'Script "{name}" removed.', 'success')
            else:
                io.print(f'Script "{name}" not removed.', 'warning')
        else:
            io.print(f'Script "{name}" not found.', 'warning')
