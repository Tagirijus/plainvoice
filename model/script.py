from model.base import Base
from model.file import File
from view import error_printing


class Script(Base):

    def __init__(self):
        super(Script, self).__init__()
        self.python_string = ''

    def folder(self, filename=''):
        return 'scripts/' + filename

    def load_script_string_from_python_file(self, name):
        try:
            self.python_string = File().load_string_from_python_file(self.folder(name), True)
            return True
        except Exception as e:
            error_printing.print_if_verbose(e)
            return False

    def get_list(self):
        try:
            return File().get_files_list(self.folder(), 'py', True)
        except Exception as e:
            error_printing.print_if_verbose(e)
            return False

    def run(self, invoice):
        """Run the shell script."""
        try:
            exec(self.python_string)
            return True
        except Exception as e:
            error_printing.print_if_verbose(e)
            return False
