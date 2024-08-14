'''
DocumentTypeRepository class

It is a wrapper for DataRepository, but for document types
specifically.
'''

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

    def __init__(
        self,
        doc_types_folder: str = DEFAULT_DOC_TYPES_FOLDER
    ):
        '''
        This class is for loading and saving document types.
        '''
        super().__init__(doc_types_folder, '')

    def load_by_name(self, name: str) -> DocumentType:
        '''
        Instantiate a DocumentType by name, which is the name
        in the folder or even an absolute filename.

        Args:
            name (str): The name or absolute file name for the document type.

        Returns:
            DocumentType: Returns a loaded DocumentType.
        '''
        return DocumentType.instance_from_dict(
            self.load_dict_from_name(name)
        )
