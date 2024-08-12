'''
DocumentRepository class

This class is a wrappeer for the DataRepository class, yet it
get only the document type name and knows how to set the
folder for a specific document type accordingly automatically
then.
'''

from plainvoice.model.data.data_repository import DataRepository
from plainvoice.model.document.document import Document
from plainvoice.model.document.document_type import DocumentType


class DocumentRepository(DataRepository):
    '''
    The DocumentRepository, which can save and load Documents.
    '''

    DEFAULT_DOC_TYPES_FOLDER: str = '{app_dir}/types'
    '''
    The folder, in which the document types are stored
    by default.
    '''

    def __init__(
        self,
        doc_typename: str = '',
        doc_types_folder: str = DEFAULT_DOC_TYPES_FOLDER
    ):
        '''
        The DocumentRepository is for loading and saving Document objects.
        '''
        self.doc_types_folder = doc_types_folder
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
        data_repository = DataRepository(self.doc_types_folder)
        return DocumentType().instance_from_dict(
            data_repository.load_dict_from_name(doc_typename)
        )

    def get_links_from_document(
        self,
        doc: Document | str,
        names_only: bool = True
    ) -> list:
        '''
        Get the document names or even the loaded documents,
        which are linked to the given document.

        Args:
            doc (Document): \
                The document, which could have links or maybe \
                just its name and it will be loaded from it.

        Returns:
            list: Returns list with doc names or loaded documents.
        '''
        # load the document from its name, if the argument is a string,
        # which probabl is a documents name
        if isinstance(doc, str):
            doc = self.load_document_from_name(doc)
        # get its links
        links = doc.get_links()
        # instantiate them, if names_only is False
        if not names_only:
            output = [
                self.load_document_from_file(filename) for filename in links
            ]
        else:
            output = links
        return output

    def get_links_from_document_as_document(
        self,
        doc: Document | str,
    ) -> list[Document]:
        '''
        Get the document instances, which are linked to the given document.

        Args:
            doc (Document | str): \
                The document, which could have links or maybe \
                just its name and it will be loaded from it.

        Returns:
            list: Returns list with instantiated documents.
        '''
        return self.get_links_from_document(doc, False)

    def get_links_from_document_as_names(
        self,
        doc: Document | str,
    ) -> list[str]:
        '''
        Get the document names, which are linked to the given document.

        Args:
            doc (Document | str): \
                The document, which could have links or maybe \
                just its name and it will be loaded from it.

        Returns:
            list: Returns list with doc names.
        '''
        return self.get_links_from_document(doc, True)

    def load_document_from_file(self, abs_filename: str) -> Document:
        '''
        Load a Document instance by an absolute filename. It will load
        the YAML, find the doc_typename, load the document type into
        this document repo instance and then use the method
        document_instance_from_name() to return the Document.

        Args:
            abs_filename (str): The absolute filename of the document.

        Returns:
            Document: Returns the loaded Document instance.
        '''
        self.set_document_type_from_file(abs_filename)
        name = self.file.extract_name_from_path(abs_filename)
        return self.load_document_from_name(name)

    def load_document_from_name(self, name: str) -> Document:
        '''
        Load a Document instance by just its name and return it.
        The document type has to be set for this method to work.

        Args:
            name (str): The name of the document.

        Returns:
            Document: Returns the loaded Document instance.
        '''
        document = Document()
        document.set_fixed_fields_descriptor(
            self.doc_type.get_descriptor()
        )
        document.from_dict(
            self.load_dict_from_name(name)
        )
        return document

    def set_document_type_from_file(self, abs_filename: str) -> None:
        '''
        Load the given document YAML, get its doc_typename string and load
        this document type into this instance.

        Args:
            abs_filename (str): The absolute filename of the document.
        '''
        document_dict = self.load_dict_from_name(abs_filename)
        self.doc_type = self._get_document_type_by_name(
            str(document_dict.get('doc_typename'))
        )
