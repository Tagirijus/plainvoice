from plainvoice.model.config import Config
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

    def create_template(self, name: str) -> bool:
        '''
        Copy the default template to the templates folder
        to get a starting point for a template.

        This method is not that best placed inside this class,
        yet I did not want to create a new class just for
        this single method.

        Args:
            name (str): The name of the new template.

        Returns:
            bool: Returns True on success.
        '''
        project_path = Config().project_path
        default_template_filename = f'{project_path}/assets/invoice.jinja'

        return self.file.copy(
            default_template_filename,
            self.file.generate_absolute_filename(name)
        )

    def get_template_names(self) -> list[str]:
        '''
        Return a list with only the template names. These are the
        files in the set templates folder, but without its extension.

        Returns:
            list: Returns list of strings, which are template names.
        '''
        return self.file.get_names_list(self.templates_folder)

    def render(
        self,
        template_name: str,
        document: Document,
        filename: str = ''
    ) -> bool:
        '''
        Render the given data with the set template name.
        The data can be anything, which will be accessible in the
        Jinja template J2 file later. E.g. it can be an Invoice object
        so that the class methods for calculations are available
        as well.

        Args:
            template_name (str): \
                The name of the template file without absolute path \
                or file extension.
            document (Document): \
                The Document, which can be accessed in the \
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
                    self.templates_folder
                ),
                autoescape=select_autoescape(['html', 'xml'])
            )

            template = env.get_template(f'{template_name}.jinja')

            # with open(self.template.file, 'r') as template_file:
            #     template_content = template_file.read()
            # template = jinja2.Template(template_content)

            # render the template
            html_out = template.render(document=document)

            # convert HTML to PDF
            if not filename:
                filename = self.file.replace_extension_with_pdf(
                    document.get_filename()
                )
            wpHTML(string=html_out).write_pdf(filename)

            return True
        except Exception:
            return False
