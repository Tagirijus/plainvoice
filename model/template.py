from model.base import Base
from model.files import Files
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
            return Files().get_files_list(self.folder(), 'j2', True)
        except Exception as e:
            error_printing.print_if_verbose(e)
            return []
