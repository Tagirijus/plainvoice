'''
DocumentRepository class

This class is a wrappeer for the DataRepository class, yet it
get only the document type name and knows how to set the
folder for a specific document type accordingly automatically
then.
'''

from plainvoice.model.data.data_repository import DataRepository
from plainvoice.model.document.document import Document
from plainvoice.model.document.document_cache import DocumentCache
from plainvoice.model.document.document_type import DocumentType
from plainvoice.model.document.document_type_repository import \
    DocumentTypeRepository
from plainvoice.model.document.document_link_manager import DocumentLinkManager


class DocumentRepository:
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
        doc_types_folder: str = DEFAULT_DOC_TYPES_FOLDER
    ):
        '''
        The DocumentRepository is for loading and saving Document objects.
        '''
        self.cache: DocumentCache = DocumentCache()
        '''
        The cache, which holds already loaded Documents. You can
        fetch a document from it by its absolute filename or
        its document type + name combination.
        '''

        self.doc_types: dict[str, DocumentType] = {}
        '''
        The document type objects instantiated as a value on the
        dict with their name as the key.
        '''

        self.doc_type_repo = DocumentTypeRepository(doc_types_folder)
        '''
        The repository for loading document type objects.
        '''

        self.repositories: dict[str, DataRepository] = {}
        '''
        All available data repositories with the document type name
        as the key in the dict.
        '''

        self.links: DocumentLinkManager = DocumentLinkManager()
        '''
        The manager for handling document links.
        '''

        self._init_repositories_and_doc_types()

    def _init_repositories_and_doc_types(self) -> None:
        '''
        Initialize all the available document types and create
        a data repository for each and store it in the
        self.repositories dict with the document type name as
        the key and the DataRepository as the value.
        '''
        doc_type_dicts = self.doc_type_repo.get_list(False)
        self.doc_types = {}
        self.repositories = {}
        for doc_typename in doc_type_dicts:
            doc_type_dict = doc_type_dicts[doc_typename]
            self.repositories[doc_typename] = DataRepository(
                doc_type_dict.get('folder'),
                doc_type_dict.get('filename_pattern')
            )
            self.doc_types[doc_typename] = self.doc_type_repo.load_by_name(
                doc_typename
            )

    @property
    def add_link(self):
        return self.links.add_link

    def get_descriptor(self, doc_typename: str) -> dict:
        '''
        Get the fixed fields descriptor by the given document type
        name. It should exist in the internal dicts.

        Args:
            doc_typename (str): Document type name.

        Returns:
            dict: Returns the descriptor dict.
        '''
        if doc_typename in self.doc_types:
            return self.doc_types[doc_typename].get_descriptor()
        else:
            return {}

    def get_links_of_document(self, document: Document) -> list[Document]:
        '''
        Get the documents linked to the given document.

        Args:
            document (Document): The document to get the links from.

        Returns:
            list: Returns the list containing the loaded documents.
        '''
        # basically load the linked documents into the cache first,
        # if they aren't loaded yet
        if not self.links.document_links_loaded(document):
            for abs_filename in document.get_links():
                self.links.add_link(
                    document,
                    self.load(abs_filename)
                )
        # no get the links
        return self.links.get_links_of_document(document)

    def load(self, name: str, doc_typename: str = '') -> Document:
        '''
        Load a Document instance by just its name and document type
        name. Or maybe by its absolute filename.

        Args:
            name (str): \
                The name of the document or even its absolute \
                filepath.
            doc_typename (str): \
                The document type name. Leave blank, when using \
                an absolute filename. (default: `''`)

        Returns:
            Document: \
                Returns the loaded Document instance, if possible, \
                other an empty Document, which also has no temp \
                filename set. So it's good to check this with \
                docuemnt.get_filename() to see, if there is \
                a value, which means: loaded correctly.
        '''
        # it's probably an absolute filename without
        # a given document type name
        if doc_typename == '':
            cache_loading = self.cache.get_by_filename(name)
            if cache_loading is not None:
                return cache_loading
            else:
                return self._load_by_absolute_filename(name)
        else:
            cache_loading = self.cache.get_by_doc_type_and_name(
                doc_typename,
                name
            )
            if cache_loading is not None:
                return cache_loading
            else:
                return self._load_by_doc_typename_name_combi(
                    name,
                    doc_typename
                )

    def _load_by_absolute_filename(self, abs_filename: str) -> Document:
        '''
        Load a document instance by an absolute filename.

        Args:
            abs_filename (str): The absolute filename.

        Returns:
            Document: \
                Returns the loaded Document instance, if possible, \
                other an empty Document, which also has no temp \
                filename set. So it's good to check this with \
                docuemnt.get_filename() to see, if there is \
                a value, which means: loaded correctly.
        '''
        # generate a temp DataRepository
        tmp_data_repo = DataRepository()
        # with it load basically the plain dict first
        loaded_dict = tmp_data_repo.load_dict_from_name(abs_filename)
        # and get the doc_typename
        doc_typename = str(loaded_dict.get('doc_typename'))
        # now if the doc_typename is a document type, which exists,
        # use its folder to set for the temp DataRepository
        if doc_typename in self.doc_types:
            folder = self.doc_types[doc_typename].get_fixed('folder', False)
            tmp_data_repo.set_folder(folder)
        # the name will only be set correctly, if the given docuemnt type
        # did exist in the first place. otherwise the extract_name_from_path()
        # method won't be able to extract the name correctly
        name = tmp_data_repo.file.extract_name_from_path(abs_filename)
        return self.load(name, doc_typename)

    def _load_by_doc_typename_name_combi(
        self,
        name: str,
        doc_typename: str = ''
    ) -> Document:
        '''
        Load a document from a document typename and name
        combination.

        Args:
            name (str): \
                The name of the document or even its absolute \
                filepath.
            doc_typename (str): \
                The document type name. Leave blank, when using \
                an absolute filename. (default: `''`)

        Returns:
            Document: \
                Returns the loaded Document instance, if possible, \
                other an empty Document, which also has no temp \
                filename set. So it's good to check this with \
                docuemnt.get_filename() to see, if there is \
                a value, which means: loaded correctly.
        '''
        # create a fresh document frist
        document = Document()

        # the document type name should exist in the
        # respecting dicts to be able to set the
        # descriptor correctly
        if (
            doc_typename in self.repositories
            and doc_typename in self.doc_types
        ):
            # this set document type name does exist;
            # get the respecting DataRepository and DocumentType
            data_repo = self.repositories[doc_typename]
            document.set_document_typename(doc_typename)
            document.set_fixed_fields_descriptor(
                self.get_descriptor(doc_typename)
            )
            document.set_filename(
                data_repo.file.generate_absolute_filename(name)
            )
        else:
            # this DataRepository without an existing
            # DocumentType will hopefully just be used
            # to load an absolute filename
            data_repo = DataRepository()

        document.from_dict(
            data_repo.load_dict_from_name(name)
        )

        # also add to the cache
        self.cache.add_document(
            document,
            doc_typename,
            name,
            data_repo.file.generate_absolute_filename(name)
        )
        return document

    def new_document_by_type(self, doc_typename: str) -> Document:
        '''
        Create a new document with the given document type and
        return it.

        Args:
            doc_typename (str): The document type name.

        Returns:
            Document: Returns a new document instance.
        '''
        document = Document(doc_typename)
        if doc_typename in self.doc_types:
            document.set_fixed_fields_descriptor(
                self.get_descriptor(doc_typename)
            )
        return document

    @property
    def remove_link(self):
        return self.links.remove_link

    def save(self, document: Document, name: str = '') -> str:
        '''
        Save the Docuemnt to the automatically generated file. If
        no name is given, it might use the filename stored on the
        Dcouemnts abs_filename attribut, if it exists.

        Args:
            document (Document): The document to save.
            name (str): The name for generating the filename.

        Returns:
            str: Returns the absolute filename on success, otherwise ''.
        '''
        if not name:
            name = document.get_filename()
        doc_typename = document.get_document_typename()
        if doc_typename in self.repositories:
            data_repo = self.repositories[doc_typename]
        else:
            return ''
        output = data_repo.save(document, name)
        if output:
            document.set_filename(output)
            # only add it to the cache, if saving
            # was successful
            self.cache.add_document(
                document,
                doc_typename,
                name,
                output
            )
        return output
