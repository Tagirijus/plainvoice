from model.template import Template

import jinja2
import os
import weasyprint
import yaml


class Renderer(object):
    """PDF renderer for the invoice or quote"""

    def __init__(self):
        self.data = None
        self.data_filename = None
        self.output_filename = None
        self.template = Template()

    def set_data(self, data):
        if not os.path.exists(data):
            return False
        else:
            with open(data, 'r') as data_file:
                self.data = yaml.safe_load(data_file)
            self.data_filename = data
            self.output_filename = self.data_filename.replace('.yaml', '.pdf').replace('.YAML', '.pdf')
            return True

    def get_output_filename(self):
        return self.output_filename

    def set_template(self, name):
        return self.template.set_by_name(name)

    def render(self):
        # get the template from the chosen type and its template name
        with open(self.template.get_file(), 'r') as template_file:
            template_content = template_file.read()
        template = jinja2.Template(template_content)

        # render the template
        html_out = template.render(self.data)

        # convert HTML to PDF
        weasyprint.HTML(string=html_out).write_pdf(self.output_filename)

        return True
