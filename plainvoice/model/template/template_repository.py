'''
TemplateRepository class

It is a wrapper for DataRepository, but for templates.
'''

from plainvoice.model.config import Config
from plainvoice.model.data.data_repository import DataRepository
from plainvoice.model.file.file import File


class TemplateRepository(DataRepository):
    '''
    The repository to handle templates.
    '''

    DEFAULT_TEMPLATES_FOLDER: str = '{app_dir}/templates'
    '''
    The folder, in which the templates are stored by default.
    '''

    def __init__(
        self,
        templates_folder: str = DEFAULT_TEMPLATES_FOLDER
    ):
        '''
        This class is for loading and saving templates.

        Args:
            templates_folder (str): \
                The folder where the templates are stored normally.
        '''
        self.file = File(templates_folder, 'jinja')

    def create_template(self, name: str) -> bool:
        '''
        Copy the default template to the templates folder
        to get a starting point for a new template.

        Args:
            name (str): The name of the new template.

        Returns:
            bool: Returns True on success.
        '''
        project_path = Config().project_path
        default_template_filename = \
            f'{project_path}/assets/invoice_template.jinja'

        return self.file.copy(
            default_template_filename,
            self.file.generate_absolute_filename(name)
        )

    def get_template_names(self) -> list[str]:
        '''
        Return a list with only the template names. These are the
        files in the set templates folder, but without its extension.

        Returns:
            list: Returns list of strings, which are template names.
        '''
        return self.file.get_names_list()
