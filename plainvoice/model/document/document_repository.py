'''
DocumentRepository class

This class is a wrappeer for the DataRepository class, yet it
get only the document type name and knows how to set the
folder for a specific document type accordingly automatically
then.
'''

from plainvoice.model.config import Config
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
                '' if not doc_type_dict.get('folder') else
                str(doc_type_dict.get('folder')),
                '' if not doc_type_dict.get('filename_pattern') else
                str(doc_type_dict.get('filename_pattern'))
            )
            self.doc_types[doc_typename] = self.doc_type_repo.load_by_name(
                doc_typename
            )

    @property
    def add_link(self):
        return self.links.add_link

    def create_document(self, doc_typename: str, name: str = '') -> Document:
        '''
        Create a new document for the given document type, save it and
        return the object immediately as well. It will load the given
        document instance, if it might exist already so that a doc
        creation won't be able to overwrite anything.

        Args:
            doc_typename (str): The document type name.
            name (str): The name of the document.

        Returns:
            bool: \
                Returns the new Document. If something went wrong, though, \
                the Document is unsaved and "empty".
        '''
        # return a document, which might already exist
        if self.exists(doc_typename, name):
            return self.load(name, doc_typename)

        # if the document type does not exist, simply return
        # an empty Document instance as a fallback
        if doc_typename not in self.repositories:
            return Document()

        document = self.new_document_by_type(doc_typename)
        document.set_name(name)
        self.fill_new_documents_data(document)

        self.save(document)

        # also add to the cache
        data_repo = self.repositories[doc_typename]
        self.cache.add_document(
            document,
            doc_typename,
            name,
            data_repo.file.generate_absolute_filename(name)
        )
        return document

    def exists(self, doc_typename: str, name: str) -> bool:
        '''
        Checkif the given document of the given document type
        does exist.

        Args:
            doc_typename (str): The document type name.
            name (str): The document name.

        Returns:
            bool: Returns True on success.
        '''
        # first check, if the given name might be the code maybe.
        # if it's not, this method will return the name as it
        # came in otherwise
        doc_typename, name = self.get_doc_typename_name_combi_from_code(
            doc_typename,
            name
        )
        if doc_typename in self.repositories:
            doc_repo = self.repositories[doc_typename]
            return doc_repo.exists(name)
        else:
            tmp_repo = DataRepository()
            return tmp_repo.exists(name)

    def fill_new_documents_data(self, doc: Document) -> None:
        '''
        Fill the given documents fields with certain values. The document
        should be one, which probably is new and might not even be saved.

        Args:
            doc (Document): The new document instance.
        '''
        name = doc.get_name()
        doc_typename = doc.get_document_typename()

        if name == '':
            name = self.generate_next_name(doc_typename)
            next_code = self.get_next_code(doc_typename)
        else:
            next_code = None

        # set some internal data for the document
        doc.set_name(name)
        data_repo = self.repositories[doc_typename]
        doc.set_filename(
            data_repo.file.generate_absolute_filename(name)
        )

        # fill some fixed fields
        if next_code:
            doc.set_code(next_code)

    def generate_next_name(self, doc_typename: str) -> str:
        '''
        Generate the next new filename according to the filename pattern
        for the docuemnt type with the given name.

        Args:
            doc_typename (str): Document type name.

        Returns:
            str: Returns the new next filename as a string.
        '''
        if doc_typename in self.repositories:
            doc_repo = self.repositories[doc_typename]
        next_code = doc_repo.get_next_code()
        return doc_repo.file.generate_name({'code': next_code})

    def get_client_of_document(self, document: Document) -> Document:
        '''
        Get the linked client of the given document. It will see
        which document type is set for being a "client" and then
        browse through the documents linked documents. The FIRST
        document, which has this "client document type" will be
        used as the result to return as an instantiated document.

        Args:
            document (Document): The document to get the client for.

        Returns:
            Document: \
                Returns a client as a document or a blank one as a fallback.
        '''
        client_type = Config().get('client_type')
        links_of_doc = self.get_links_of_document(document)
        for link in links_of_doc:
            if link.get_document_typename() == client_type:
                return link
        return Document()

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

    def get_document_by_code(
        self,
        doc_typename: str,
        code: str
    ) -> Document | None:
        '''
        Get a document by its code.

        Args:
            doc_typename (str): Document type name.
            code (str): The code to search for.

        Returns:
            Document: Returns the found document object or None.
        '''
        if not (
            doc_typename in self.repositories
            and doc_typename in self.doc_types
        ):
            return None

        doc_type = self.doc_types[doc_typename]
        code_fieldname = doc_type.get_fixed('code_fieldname')

        # iter through all documents of the type; also the
        # hidden ones
        for doc in self.get_list_of_docs(doc_typename, False):
            if code == doc.get_fixed(code_fieldname):
                return doc

        # return None if nothing found
        return None

    def get_document_by_name_type_combi(
        self,
        name: str,
        doc_typename: str | None
    ) -> Document | None:
        '''
        Get a document by its document typename and name or code,
        or by only its absolute file name.

        Args:
            name (str): \
                This can be the document name, its absolute \
                file name or just its code.
            doc_typename (str): \
                If left blank, "name" should be an absolute \
                file name. Otherwise this is supposed to be \
                the document type name.

        Returns:
            Document | None: \
                Returns None, if nothing found, otherwise the found \
                Document.
        '''
        doc_typename, name = self.get_doc_typename_and_name(
            doc_typename,
            name
        )
        if self.exists(doc_typename, name):
            return self.load(name, doc_typename)
        else:
            return None

    def get_document_type_from_file(self, abs_filename: str) -> str:
        '''
        Get the docuemnt type from the given file, which should
        be a document, for example.

        Args:
            abs_filename (str): \
                The absolute filename. Can maybe also be \
                relative, though.

        Returns:
            str: Returns the document type as a string.
        '''
        # generate a temp DataRepository
        tmp_data_repo = DataRepository()
        # with it load basically the plain dict first
        loaded_dict = tmp_data_repo.load_dict_from_name(abs_filename)
        # and get the doc_typename
        doc_typename = loaded_dict.get('doc_typename')
        return doc_typename if doc_typename else ''

    def get_doc_typename_and_name(
        self,
        doc_typename: str | None,
        name: str
    ) -> tuple[str, str]:
        '''
        Get a document name and a document type by the given
        arguments. While type can be none, which could mean
        that the given name is a path to a document file.
        Extract it's document type then and return both
        accordingly.

        Args:
            doc_typename (str): The document type name.
            name (str): The document name or file path.

        Returns:
            tuple: Returns final document type as string, final document name.
        '''
        if not isinstance(doc_typename, str):
            # means that the given name should be a path
            # to a file directly
            doc_typename = self.get_document_type_from_file(name)
            # also if the given name is not absolute nor have
            # "./" in the beginning, at the latter one at least
            if not name.startswith('/') and not name.startswith('./'):
                name = './' + name
        return doc_typename, name

    def get_doc_typename_name_combi_from_code(
        self,
        doc_typename: str,
        code: str
    ) -> tuple:
        '''
        Make something.

        Args:
            doc_typename (str): The document type name.
            code (str): The possible document code.

        Returns:
            tuple: Returns final document type as string, final document name.
        '''
        doc = self.get_document_by_code(doc_typename, code)
        if doc:
            return doc.get_document_typename(), doc.get_name()
        else:
            # otherwise it might be no code, but its name;
            # return it as this then
            return doc_typename, code

    def get_due_docs(
        self,
        doc_typename: str,
        include_due: bool = True,
        include_overdue: bool = True,
        show_only_visible: bool = True
    ) -> list[Document]:
        '''
        Get a list of documents, which have a due date set, but
        no done date NOW. Get for the specified document type or
        all types, if not specified.

        Args:
            doc_typename (str): The document type name.
            include_due (bool): include the docuemnts which are due.
            include_overdue (bool): include the docuemnts which are overdue.
            show_only_visible (bool): \
                Show only the DataModels with the attribute set \
                to "self.visivble = True" in the output list. \
                Here it's data['visible'], since they are still \
                dicts, after all.

        Returns:
            list: Returns a list with document objects.
        '''
        all_doc_dicts: list[Document] = []

        # a doc type is given and exists
        if doc_typename != '' and doc_typename in self.repositories:
            all_doc_dicts.extend(
                self.get_list_of_docs(doc_typename, show_only_visible)
            )

        # no doc type given, use all doc types
        elif doc_typename == '':
            for doc_type in self.doc_types.keys():
                all_doc_dicts.extend(
                    self.get_list_of_docs(doc_type, show_only_visible)
                )

        # only use docs for output, if they are not done, thus
        # due or even overdue - but also only according to the
        # set parameters include_due and include_overdue
        output = []
        for doc in all_doc_dicts:
            is_due = doc.is_due()
            is_overdue = doc.is_overdue()

            only_due = (
                include_due and not include_overdue and
                (is_due and not is_overdue)
            )

            only_overdue = (
                not include_due and include_overdue and
                (is_due and is_overdue)
            )

            due_and_overdue = (
                include_due and include_overdue and
                (is_due or is_overdue)
            )
            if only_due or only_overdue or due_and_overdue:
                if not show_only_visible or doc.is_visible():
                    output.append(doc)

        return output

    def get_filename(self, doc_typename: str, name: str) -> str:
        '''
        Get filename of given document with the given
        document type.

        Args:
            doc_typename (str): The document type name.
            name (str): The document name.

        Returns:
            str: Returns filename of document as string.
        '''
        document = self.load(name, doc_typename)
        return document.get_filename()

    def get_filename_pattern(self, doc_typename: str) -> str:
        '''
        Get the filename pattern of the document type.

        Args:
            doc_typename (str): The name of the document type.

        Returns:
            str: Returns the filename pattern as a string.
        '''
        if doc_typename in self.doc_types:
            return self.doc_types[doc_typename].get_filename_pattern()
        else:
            return ''

    def get_folder(self, doc_typename: str) -> str:
        '''
        Get the absolute path of the document type.

        Args:
            doc_typename (str): The name of the document type.

        Returns:
            str: Returns the path as a string.
        '''
        if doc_typename in self.repositories:
            return self.repositories[doc_typename].get_folder()
        else:
            return ''

    def get_list(
        self,
        doc_typename: str,
        show_only_visible: bool = True
    ) -> dict[str, dict]:
        '''
        Get a list of document as dicts according to the document type.

        Args:
            doc_typename (str): \
                The document type name.
            show_only_visible (bool): \
                Show only the DataModels with the attribute set \
                to "self.visivble = True" in the output list. \
                Here it's data['visible'], since they are still \
                dicts, after all.

        Returns:
            dict: Returns a dict with the Document-dicts on their names.
        '''
        if doc_typename in self.repositories:
            return self.repositories[doc_typename].get_list(show_only_visible)
        else:
            return {}

    def get_list_of_docs(
        self,
        doc_typename: str,
        show_only_visible: bool = True
    ) -> list[Document]:
        '''
        Get a list of document objects as a sorted list This
        is some kind of wrapper for the get_list() method, which
        only gets the documents as dicts on the values.

        Also this method sorts the found documents by (prioritizing):
          - date issued
          - code
          - name

        Args:
            doc_typename (str): \
                The document type name.
            show_only_visible (bool): \
                Show only the DataModels with the attribute set \
                to "self.visivble = True" in the output list. \
                Here it's data['visible'], since they are still \
                dicts, after all.

        Returns:
            list: Returns a sorted list with Document objects.
        '''
        docs_dict = self.get_list(doc_typename, show_only_visible)
        docs_list = []
        for doc_name, doc_dict in docs_dict.items():
            doc = Document(doc_typename, doc_name)
            doc.init_internals_with_doctype(
                self.doc_types[doc_typename]
            )
            doc.from_dict(doc_dict)
            docs_list.append(doc)

        # sort documents by:
        # - date issued
        # - code
        # - name
        docs_list = sorted(
            docs_list,
            key=lambda doc: (
                doc.get_issued_date() or '9999-12-31',
                doc.get_code() or 'ZZZZ',
                doc.get_name() or ''
            )
        )

        return docs_list

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
                if abs_filename != '':
                    self.links.add_link(
                        document,
                        self.load(abs_filename)
                    )
        # now get the links
        return self.links.get_links_of_document(document)

    def get_next_code(self, doc_typename: str = '') -> str:
        '''
        Get the next code for the document type with the given name.

        Args:
            doc_typename (str): Document type name.

        Returns:
            str: Returns next code as a string.
        '''
        if doc_typename in self.repositories:
            doc_repo = self.repositories[doc_typename]
        return doc_repo.get_next_code()

    def get_user_by_username(self, user_name: str = '') -> Document:
        '''
        Return the user according to the given user name. If none
        is given, use the name from the config. This method will
        be used in the command line interface, for example.

        Args:
            user_name (str): The name of the user to get.

        Returns:
            Document: Returns the user Document.
        '''
        if not user_name:
            user_name = str(Config().get('user_default_name'))
        user = self.load(user_name, str(Config().get('user_type')))
        return user

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
            # first check, if the given name might be the code maybe.
            # if it's not, this method will return the name as it
            # came in otherwise
            doc_typename, name = self.get_doc_typename_name_combi_from_code(
                doc_typename,
                name
            )
            # now use the doc_typename and name to maybe load the doc
            # from cache or load it with the respective method
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
        # get the doc_typename
        doc_typename = self.get_document_type_from_file(abs_filename)
        # generate a temp DataRepository
        tmp_data_repo = DataRepository()
        # now if the doc_typename is a document type, which exists,
        # use its folder to set for the temp DataRepository
        if doc_typename in self.doc_types:
            folder = self.doc_types[doc_typename].get_fixed('folder', False)
            tmp_data_repo.set_folder(folder)
        # the name will only be set correctly, if the given docuemnt type
        # did exist in the first place. otherwise the extract_name_from_path()
        # method won't be able to extract the name correctly
        name = tmp_data_repo.file.extract_name_from_path(abs_filename)
        return self.load(name, str(doc_typename))

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
        document.set_name(name)

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
            document.init_internals_with_doctype(
                self.doc_types[doc_typename]
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
            document.set_document_typename(doc_typename)
            document.init_internals_with_doctype(
                self.doc_types[doc_typename]
            )
        return document

    def remove(self, doc_typename: str, name: str) -> bool:
        '''
        Checkif the given document of the given document type
        does exist.

        Args:
            doc_typename (str): The document type name.
            name (str): The document name.

        Returns:
            bool: Returns True on success.
        '''
        if doc_typename in self.repositories:
            doc_repo = self.repositories[doc_typename]
        else:
            doc_repo = DataRepository()

        # go through the linked documents and remove the documents, which
        # has to be deleted here, from the linked documents list
        doc_to_remove = self.load(name, doc_typename)
        for linked_doc_path in doc_to_remove.get_links():
            unlink_doc = self.load(linked_doc_path)
            self.remove_link(doc_to_remove, unlink_doc)
            self.save(unlink_doc)

        # finally remove the document, which has to be deleted
        return doc_repo.remove(name)

    def remove_link(self, document_a: Document, document_b: Document) -> bool:
        '''
        Remove a link between the documents.

        Args:
            document_a (Document): The one document.
            document_b (Document): The other document.

        Returns:
            bool: Returns True on success and False, if there was no link.
        '''
        # basically load the linked documents into the cache first,
        # if they aren't loaded yet; otherwise the unlinking method
        # will return False, since it does not know the link yet
        if not self.links.document_links_loaded(document_a):
            for abs_filename in document_a.get_links():
                self.links.add_link(
                    document_a,
                    self.load(abs_filename)
                )
        if not self.links.document_links_loaded(document_b):
            for abs_filename in document_b.get_links():
                self.links.add_link(
                    document_b,
                    self.load(abs_filename)
                )
        # now remove the link
        return self.links.remove_link(document_a, document_b)

    def rename_document(self, document: Document, new_name: str) -> bool:
        '''
        Rename a document and adjust its links accordingly.

        Args:
            document (Document): The document object to rename.
            new_name (str): The new name to set for the document.

        Returns:
            bool: Returns True on success.
        '''
        doc_typename = document.get_document_typename()
        if doc_typename in self.repositories:
            data_repo = self.repositories[doc_typename]
        else:
            return False
        old_path = document.get_filename()
        old_name = data_repo.file.extract_name_from_path(
            old_path,
            False
        )

        doc_rename_success = data_repo.rename(
            old_name,
            new_name
        )
        new_path = data_repo.file.generate_absolute_filename(new_name)

        self.cache.rename_document(
            document,
            doc_typename,
            old_name,
            new_name,
            old_path,
            new_path
        )

        links_update_success = self._update_new_doc_name_in_its_links(
            document,
            old_name,
            new_name
        )

        return doc_rename_success and links_update_success

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

    def _update_new_doc_name_in_its_links(
        self,
        document: Document,
        old_name: str,
        new_name: str
    ) -> bool:
        '''
        Update the new document name in its links. This will get the
        given documents links and just replace the old name with the
        new name in the plain absolute filename string.

        ATTENTION:
        This method will immediately save the linked documents! This
        might not be wanted on runtime, yet at the moment I am not
        sure and not motivated enough to make it work better.

        Args:
            document (Document): \
                The document, which got renamed.
            old_name (str): \
                The old plain name of the doc without the base path \
                or the file extension.
            new_name (str): \
                The new plain name of the doc. Also without the base \
                path or the file extension.

        Returns:
            bool: Returns True on success.
        '''
        # get document variables for this task
        doc_typename = document.get_document_typename()
        if doc_typename not in self.repositories:
            return False
        doc_data_repo = self.repositories[doc_typename]
        old_path = doc_data_repo.file.generate_absolute_filename(old_name)
        new_path = doc_data_repo.file.generate_absolute_filename(new_name)

        # modify the documents links
        links = self.links.get_links_of_document(document)
        for linked_doc in links:
            # update the old documents path in the linked documents link list
            linked_doc.links = [
                new_path if item == old_path else item
                for item in linked_doc.get_links()
            ]

            # save the linked document directly
            linked_doc_typename = linked_doc.get_document_typename()
            if linked_doc_typename not in self.repositories:
                return False
            linked_doc_data_repo = self.repositories[linked_doc_typename]
            linked_doc_name = linked_doc_data_repo.file.extract_name_from_path(
                linked_doc.get_filename()
            )
            linked_doc_data_repo.save(linked_doc, linked_doc_name)

        return True
