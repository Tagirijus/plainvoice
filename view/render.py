from model.settings import Settings
from view import error_printing
from jinja2 import Environment, FileSystemLoader, select_autoescape
from weasyprint import HTML as wpHTML

import os


class Render:
    """PDF renderer for the invoice or quote"""

    def __init__(self):
        self.template_name = ''

    def set_template(self, name):
        self.template_name = name

    def render(self, data, filename):
        """
        Render the given data with the set template name.
        The data can be anything, which will be accessible in the
        Jinja template J2 file later. E.g. it can be an Invoice object
        so that the class methods for calculations are available
        as well.
        """
        try:

            env = Environment(
                loader=FileSystemLoader(os.path.join(Settings().DATADIR, 'templates')),
                autoescape=select_autoescape(['html', 'xml'])
            )

            template = env.get_template(f'{self.template_name}.j2')

            # with open(self.template.file, 'r') as template_file:
            #     template_content = template_file.read()
            # template = jinja2.Template(template_content)

            # render the template
            html_out = template.render(data=data)

            # convert HTML to PDF
            wpHTML(string=html_out).write_pdf(filename)

            return True
        except Exception as e:
            error_printing.print_if_verbose(e)
            return False
