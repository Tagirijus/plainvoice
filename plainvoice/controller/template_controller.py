'''
TemplateController class

Handles Template managing.
'''

from plainvoice.controller.io_facade.io_facade import IOFacade as io
from plainvoice.model.config import Config
from plainvoice.model.template.template_repository import TemplateRepository
from plainvoice.utils import file_utils

import os


class TemplateController:
    '''
    Handles Template managing.
    '''

    def __init__(self):
        '''
        Handles Template managing.
        '''
        self.template_repo = TemplateRepository(str(Config().get('templates_folder')))

    def edit(self, name: str) -> None:
        '''
        Edit the template with the given name. If it does not
        exist, create a new one from hard-coded asset.

        Args:
            name (str): The name of the template.
        '''
        file_name = self.template_repo.get_absolute_filename(name)
        if not os.path.exists(file_name):
            self.template_repo.create_template(name)
        file_utils.open_in_editor(file_name)

    def list(self) -> None:
        '''
        List templates.
        '''
        io.print_list(sorted(self.template_repo.get_template_names()))

    def remove(self, name: str) -> None:
        '''
        Remove the document type with the given name.

        Args:
            name (str): The name of the document type.
        '''
        if self.template_repo.exists(name):
            if io.ask_yes_no(f'Remove template "{name}"?'):
                self.template_repo.remove(name)
                io.print(f'Template "{name}" removed.', 'success')
            else:
                io.print(f'Template "{name}" not removed.', 'warning')
        else:
            io.print(f'Template "{name}" not found.', 'warning')
