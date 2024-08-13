'''
DocumentCache class

With this class I try to implement some cache logic so that
loaded Documents can be fetched from cache by its absolute
filename or their "docuemnt type + name" combi. Also this
cache will be used by DocumentLinkManager to link documents
in a clean way.
'''

from plainvoice.model.document.document import Document


class DocumentCache:
    '''
    The cache, which can hold document instances and return
    one by its absolute filename or its document type + name
    combination.
    '''

    def __init__(self):
        '''
        This object is a cache for Document instances.
        '''
        self.by_filename: dict[str, Document] = {}
        '''
        The cache dict, holding Documents based on their
        absolute filename.
        '''

        self.by_doc_type_and_name: dict[str, Document] = {}
        '''
        The cache dict, holding Documents based on their
        document type and name combination.
        '''

    def generate_doc_name_combi(
        self,
        doc_typename: str,
        name: str
    ) -> str:
        '''
        Generate a string with the combination of docuemnt type
        name and document name. It is used for generating some
        kind of id for a document instance.

        Args:
            doc_typename (str): The document type name.
            name (str): The document name.

        Returns:
            str: Returns the doc type name combination as a string.
        '''
        return f'{doc_typename}::{name}'

    def get_by_doc_type_and_name(
        self,
        doc_typename: str,
        name: str
    ) -> Document | None:
        '''
        Get a document instance by filename from the cache.

        Args:
            doc_typename (str): The document type name.
            name (str): The document name.

        Returns:
            Document: Returns the Document from the cache.
        '''
        doc_type_name_combi = self.generate_doc_name_combi(
            doc_typename,
            name
        )
        if doc_type_name_combi in self.by_filename:
            return self.by_doc_type_and_name[doc_type_name_combi]
        else:
            return None

    def get_by_filename(self, abs_filename: str) -> Document | None:
        '''
        Get a document instance by filename from the cache.

        Args:
            abs_filename (str): The absolute filename of the document.

        Returns:
            Document: Returns the Document from the cache.
        '''
        if abs_filename in self.by_filename:
            return self.by_filename[abs_filename]
        else:
            return None
