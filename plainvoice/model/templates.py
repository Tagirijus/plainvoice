from plainvoice.model.base import Base
from plainvoice.model.files import Files
from plainvoice.model.config import Config


class Templates(Base):
    """
    The class for the templates of plainvoice.
    """

    def __init__(self):
        super(Templates, self).__init__()
        self.FOLDER = 'templates/'
        self.EXTENSION = 'j2'

    def create(self, name: str) -> bool:
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
            self.get_absolute_filename(name)
        )

    def get_absolute_default_template_filename(self) -> str:
        """
        Returns the absolute filename to the default template asset.

        Returns:
            str: \
                The path to the default template asset from
                the python programs asset directory.
        """
        project_path = Config().project_path
        return f'{project_path}/assets/invoice.j2'
