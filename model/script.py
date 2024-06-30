from model.file import File
from view import error_printing
from view import printing as p

import click


class Script:
    """docstring for Script"""

    def __init__(self):
        self.python_string = ''

    def load_script_string_from_python_file(self, filename):
        try:
            filename = 'scripts/' + filename.replace('scripts/', '')
            self.python_string = File().load_string_from_python_file(filename, True)
            return True
        except Exception as e:
            error_printing.print_if_verbose(e)
            return False

    def run(self, invoice):
        """Run the shell script."""
        try:
            ctx = click.get_current_context()
            verbose = ctx.obj.get('verbose', 0)
            if verbose >= 1:
                p.print_formatted('Executing the follwing shell string:')
                p.print_formatted(self.python_string)
            exec(self.python_string)
            return True
        except Exception as e:
            error_printing.print_if_verbose(e)
            return False
