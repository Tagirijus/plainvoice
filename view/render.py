from model.template import Template
from view import error_printing

import jinja2
from weasyprint import HTML as wpHTML


class Render:
    """PDF renderer for the invoice or quote"""

    def __init__(self):
        self.template = Template()

    def set_template(self, name):
        return self.template.set_by_name(name)

    def render(self, data, filename):
        """
        Render the given data with the set Template (class attribute).
        The data can be anythin, which will be accessible in the
        Jinja template HTML later. E.g. it can be an Invoice object
        so that the class methods for calculations are available
        as well.
        """
        try:
            with open(self.template.file, 'r') as template_file:
                template_content = template_file.read()
            template = jinja2.Template(template_content)

            # render the template
            html_out = template.render(data=data)

            # convert HTML to PDF
            wpHTML(string=html_out).write_pdf(filename)

            return True
        except Exception as e:
            error_printing.print_if_verbose(e)
            return False
