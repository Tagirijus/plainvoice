from plainvoice.model.document import Document
from plainvoice.model.document_type import DocumentType
from plainvoice.model.filemanager import FileManager


class DocumentList:
    """
    The class, which can get a list of the documents with
    the set document type.
    """

    def __init__(self, document_type_name: str = 'dummy'):
        self.document_type_name = document_type_name
        """
        The DocumentType, which will describe the type of the lists
        objects.
        A user can configure custom types of documents besides the
        basic ones.
        """

        self.document_type = DocumentType(document_type_name)
        """
        The document type which this list class will handle.
        """

        self.documents = []
        """
        The final documents list.
        """

        self.file_manager = FileManager(self.document_type.folder)
        """
        Init the file manager with the correct folder accordingly.
        """

    def get_files_of_document_type(self) -> list:
        """
        Get a list containing all the filepaths to the documents
        with the given document type.

        Returns:
            list: Returns a list with filepath strings.
        """
        return self.file_manager.find_files_of_type()

    def get_list(self, show_only_visible: bool = True) -> list:
        """
        Get a list of all available documents according to the set
        type

        Args:
            show_only_visible (bool): \
                Show only the documents with the attribute set
                to "self.visivble = True" in the output list.

        Returns:
            list: Returns a list with the document objects.
        """
        document_files = self.get_files_of_document_type()
        self.documents = []
        for document_file in document_files:
            tmp_doc = Document()
            tmp_doc.from_dict(
                self.file_manager.load_from_yaml_file(document_file)
            )
            add_me = (
                (show_only_visible and tmp_doc.visible)
                or not show_only_visible
            )
            if add_me:
                self.documents.append(tmp_doc)
        return self.documents
