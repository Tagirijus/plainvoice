from plainvoice.model.invoice import Invoice
from plainvoice.model.config import Config
from plainvoice.view import error_printing
from jinja2 import Environment, FileSystemLoader, select_autoescape
from weasyprint import HTML as wpHTML

import os


class Render:
    """
    PDF renderer for the invoice or quote, or maybe further formats
    in the future (or present already?). You basically set a template
    for this class with set_template(NAME) and then render(DATA, OUTFILE)
    to render the DATA into the OUTFILE.
    """

    template_name: str
    """
    The template name withou any path or file extension.
    """

    def __init__(self):
        self.template_name = ''

    def render(self, data: dict | Invoice, filename: str) -> bool:
        """
        Render the given data with the set template name.
        The data can be anything, which will be accessible in the
        Jinja template J2 file later. E.g. it can be an Invoice object
        so that the class methods for calculations are available
        as well.

        Args:
            data (dict | Invoice): \
                The dict or any object, which can be accessed in the \
                jinja template later.
            filename (str): \
                The filename for the output file.

        Returns:
            bool: \
                Returns if succeede or not.
        """
        try:

            env = Environment(
                loader=FileSystemLoader(
                    os.path.join(Config().datadir, 'templates')
                ),
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

    def set_template(self, name: str) -> None:
        """
        Sets a template name for the renderer.

        Args:
            name (str): \
                The template name without path or file extension.
        """
        self.template_name = name
