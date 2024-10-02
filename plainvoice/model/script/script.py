'''
Script class

This class will be instantiated with a string, which holds Python code.
It then can execute this Python string and get a DataModel objects as
arguments (data and user) to be passed on to the script. Internally in
the Python script it is possible to access the following variables:

- client: The client which might be linked to the Document.
- config: The config of the plainvoice program.
- data: The DataModel or Document to render.
- doc_repo: The DocumentRepository, in case in the script it is needed
  to fetch more document objects.
- user: The user which is chosen for the session.
'''

from plainvoice.model.config import Config
from plainvoice.model.document.document import Document
from plainvoice.model.data.data_model import DataModel
from plainvoice.utils import doc_utils

# pyright: reportUnusedVariable=false
# pyright: reportUnusedParameter=false


class Script:
    '''
    The class for the script extension of plainvoice.
    '''

    def __init__(self, python_string: str):
        '''
        The script class contains just the Python executable string
        and will be able to execute it.

        Args:
            python_string (str): A string containing Python code.
        '''
        self.python_string = python_string

    def run(self, data: DataModel | Document, user: DataModel) -> bool:
        '''
        Runs the python code in the python_string attribute. Also
        this method gets arguments, which then will be passed to
        the script itself.

        Args:
            data (DataModel | Document): \
                The DataModel or Document object, which will be \
                accessible in the script to run as "data".
            user (DataModel): \
                The user DataModel to be used in the scripts.

        Returns:
            bool: \
                Returns True if the script ran successfully. \
                At least regarding the main program.
        '''
        try:
            config = Config()
            doc_repo = doc_utils.get_doc_repo()
            if isinstance(data, Document):
                client = doc_repo.get_client_of_document(data)
            else:
                client = Document()
            exec(self.python_string)
            return True
        except Exception:
            return False
