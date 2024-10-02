'''
DocumentTypeRepository class

It is a wrapper for DataRepository, but for document types
specifically.
'''

from plainvoice.model.config import Config
from plainvoice.model.data.data_repository import DataRepository
from plainvoice.model.document.document_type import DocumentType


class DocumentTypeRepository(DataRepository):
    '''
    The repository to handle DocumentType objects.
    '''

    DEFAULT_DOC_TYPES_FOLDER: str = '{app_dir}/types'
    '''
    The folder, in which the document types are stored
    by default.
    '''

    def __init__(self, doc_types_folder: str = DEFAULT_DOC_TYPES_FOLDER):
        '''
        This class is for loading and saving document types.

        Args:
            doc_types_folder (str): \
                The folder where the document types are stored normally.
        '''
        super().__init__(doc_types_folder, '')

    def create_type(self, name: str) -> bool:
        '''
        Copy the default docuemtn type to the document types
        folder to get a starting point for a document type.

        Args:
            name (str): The name of the new document type.

        Returns:
            bool: Returns True on success.
        '''
        project_path = Config().project_path
        default_template_filename = f'{project_path}/assets/invoice_type.yaml'

        return self.file.copy(
            default_template_filename, self.file.generate_absolute_filename(name)
        )

    def load_by_name(self, name: str) -> DocumentType:
        '''
        Instantiate a DocumentType by name, which is the name
        in the folder or even an absolute filename.

        Args:
            name (str): The name or absolute file name for the document type.

        Returns:
            DocumentType: Returns a loaded DocumentType.
        '''
        output_doc_type = DocumentType.instance_from_dict(
            self.load_dict_from_name(name)
        )
        output_doc_type.set_name(name)
        return output_doc_type
