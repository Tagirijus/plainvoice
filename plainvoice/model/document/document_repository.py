'''
DocumentRepository class

This class is a wrappeer for the DataRepository class, yet it
get only the document type name and knows how to set the
folder for a specific document type accordingly automatically
then.
'''

from plainvoice.model.data.data_repository import DataRepository
from plainvoice.model.document.document_type import DocumentType


class DocumentRepository(DataRepository):
    '''
    The DocumentRepository, which can save and load Documents.
    '''

    DOC_TYPES_FOLDER: str = '{app_dir}/types'
    '''
    The folder, in which the document types are stored
    by default.
    '''

    def __init__(self, doc_typename: str):
        '''Initialize the class.'''
        self.doc_type = self._get_document_type_by_name(doc_typename)
        folder = self.doc_type.get_fixed('folder', True)
        filename_pattern = self.doc_type.get_fixed('filename_pattern', True)
        super().__init__(folder, filename_pattern)

    def _get_document_type_by_name(self, doc_typename: str) -> DocumentType:
        '''
        Get an DocumentType instance by its name.

        Args:
            doc_typename (str): The document type name.

        Returns:
            DocumentType: Returns the DocumentType instance.
        '''
        data_repository = DataRepository(self.DOC_TYPES_FOLDER)
        return DocumentType().instance_from_dict(
            data_repository.load_from_name(doc_typename)
        )
