from model.base import Base
from model.file import File
from view import error_printing


class Script(Base):
    """
    The class for the script extension of plainvoice.
    """

    python_string: str
    """
    The final python string to execute.
    """

    def __init__(self):
        super(Script, self).__init__()
        self.FOLDER = 'scripts/'
        self.python_string = ''

    def load_script_string_from_python_file(self, name: str) -> bool:
        """
        Fills the python_string attribute with the script with the
        given name. This file should be in the .plainvoice/scripts
        folder.

        Args:
            name (str): \
                The name of the script withotu the file extension.

        Returns:
            bool: Returns True if loading succeeded.
        """
        try:
            self.python_string = File().load_string_from_python_file(
                self.folder(name),
                True
            )
            return True
        except Exception as e:
            error_printing.print_if_verbose(e)
            return False

    def get_list(self) -> list:
        """
        Returns the list containing all the possible
        scripts from the .plainvoice/scripts folder.
        Listing is without the file extension.

        Returns:
            list: The list with the script names.
        """
        try:
            return File().get_files_list(self.folder(), 'py', True)
        except Exception as e:
            error_printing.print_if_verbose(e)
            return []

    def run(self, invoice) -> bool:
        """[summary]

        Runs the python code in the python_string attribute.

        Args:
            invoice (Invoice): \
                The Invoice object, which will be accessible
                in the script to run as "invoice".

        Returns:
            bool: \
                Returns True if the script ran successfully.
                At least regarding the main programm.
        """
        try:
            exec(self.python_string)
            return True
        except Exception as e:
            error_printing.print_if_verbose(e)
            return False
