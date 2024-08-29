'''
Render class

This class can create a default template in the templates
folder and also render templates with a given Document.
'''

from plainvoice.model.config import Config
from plainvoice.model.data.data_model import DataModel
from plainvoice.model.document.document import Document
from plainvoice.model.file.file import File
from jinja2 import Environment, FileSystemLoader, select_autoescape
from weasyprint import HTML as wpHTML


class Render:
    '''
    PDF renderer for the docuemnt class.
    '''

    DEFAULT_TEMPLATES_FOLDER: str = '{app_dir}/templates'
    '''
    The folder, in which the templates are stored by default.
    '''

    def __init__(
        self,
        templates_folder: str = DEFAULT_TEMPLATES_FOLDER
    ):
        '''
        The main class handling renders and also templates.

        Args:
            templates_folder (str): \
                The folder of the templates.
        '''
        self.file = File(templates_folder, 'jinja')
        self.templates_folder = templates_folder

    def render(
        self,
        template_name: str,
        data: DataModel | Document,
        user: DataModel,
        filename: str = ''
    ) -> bool:
        '''
        Render the given data with the set template name.
        The data can be anything, which will be accessible in the
        Jinja template file later. E.g. it can be an Invoice object
        so that the class methods for calculations are available
        as well.

        Args:
            template_name (str): \
                The name of the template file without absolute path \
                or file extension.
            data (DataModel | Document): \
                The Document, which can be accessed in the \
                Jinja template later.
            user (DataModel | Document): \
                The user, which can be accessed in the \
                Jinja template later.
            filename (str): \
                The filename for the output file. If left empty, \
                the Document.get_filename() will be used instead.

        Returns:
            bool: \
                Returns if succeeded or not.
        '''
        try:
            env = Environment(
                loader=FileSystemLoader(
                    self.file.get_folder()
                ),
                autoescape=select_autoescape(['html', 'xml'])
            )

            template = env.get_template(f'{template_name}.jinja')

            # with open(self.template.file, 'r') as template_file:
            #     template_content = template_file.read()
            # template = jinja2.Template(template_content)

            # render the template
            config = Config()
            html_out = template.render(
                data=data,
                config=config,
                user=user
            )

            # convert HTML to PDF
            if not filename:
                if isinstance(data, Document):
                    filename = self.file.replace_extension_with_pdf(
                        data.get_filename()
                    )
                else:
                    return False
            wpHTML(string=html_out).write_pdf(filename)

            return True
        except Exception:
            return False
