from model.base import Base
from model.files import Files
from view import error_printing


class Scripts(Base):
    """
    The class for the script extension of plainvoice.
    """

    python_string: str
    """
    The final python string to execute.
    """

    def __init__(self):
        super(Scripts, self).__init__()
        self.FOLDER = 'scripts/'
        self.EXTENSION = 'py'
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
            self.python_string = Files().load_string_from_python_file(
                self.get_folder(name),
                True
            )
            return True
        except Exception as e:
            error_printing.print_if_verbose(e)
            return False

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
