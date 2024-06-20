from model.invoice import Invoice
from model.template import Template
from model.file import File
from view import error_printing

import jinja2
import os
from weasyprint import HTML as wpHTML
import yaml


class Renderer:
    """PDF renderer for the invoice or quote"""

    def __init__(self):
        self.data = None
        self.data_filename = None
        self.invoice = Invoice()
        self.output_filename = None
        self.template = Template()

    def set_file(self, filename):
        if not os.path.exists(filename):
            return False
        else:
            self.data_filename = filename
            self.output_filename = self.data_filename.replace('.yaml', '.pdf').replace('.YAML', '.pdf')
            return True

    def load_file(self):
        try:
            self.data = File().load(
                self.data_filename,
                False
            )
            self.invoice.set_from_dict(self.data)
            return True
        except Exception as e:
            error_printing.print_if_verbose(e)
            return False

    def set_template(self, name):
        return self.template.set_by_name(name)

    def render(self):
        # get the template from the chosen type and its template name
        with open(self.template.file, 'r') as template_file:
            template_content = template_file.read()
        template = jinja2.Template(template_content)

        # render the template
        html_out = template.render(invoice=self.invoice)

        # convert HTML to PDF
        wpHTML(string=html_out).write_pdf(self.output_filename)

        return True
