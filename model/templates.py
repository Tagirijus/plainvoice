from model.base import Base
from model.files import Files
from model.settings import Settings
from view import error_printing


class Templates(Base):
    """
    The class for the templates of plainvoice.
    """

    def __init__(self):
        super(Templates, self).__init__()
        self.FOLDER = 'templates/'

    def get_list(self) -> list:
        """
        Returns the list containing all the possible
        templates from the .plainvoice/templates folder.
        Listing is without the file extension.

        Returns:
            list: The list with the template names.
        """
        try:
            return Files().get_files_list(self.get_folder(), 'j2', True)
        except Exception as e:
            error_printing.print_if_verbose(e)
            return []

    def get_absolute_default_template_filename(self) -> str:
        """
        Returns the absolute filename to the default template asset.

        Returns:
            str: \
                The path to the default template asset from
                the python programs asset directory.
        """
        project_path = Settings().PROJECT_PATH
        return f'{project_path}/assets/invoice.j2'

    def generate_template_filename(self, name: str) -> str:
        """
        Generate the absolute template filename in the data dir
        of the program.

        Args:
            name (str): The template name without extension.

        Returns:
            str: Returns True on success.
        """
        return f'{Settings().DATADIR}/{self.get_folder(name)}.j2'

    def init(self, name: str) -> bool:
        """
        Copy the default template to the data dirs templates
        folder to get a starting point for a template.

        Args:
            name (str): The name of the new template.

        Returns:
            bool: Returns True on success.
        """
        return Files().copy(
            self.get_absolute_default_template_filename(),
            self.generate_template_filename(name)
        )
