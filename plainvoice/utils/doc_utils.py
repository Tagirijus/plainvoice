'''
Some helper functions for e.g. getting user or helping
in the command line interface to get documents or
document repositories and so on.
'''

from plainvoice.model.config import Config
from plainvoice.model.document.document import Document
from plainvoice.model.document.document_repository import DocumentRepository


def get_doc_type_and_name(doc_type: str | None, name: str) -> tuple:
    '''
    Get a document name and a document type by the given
    arguments. While type cna be none, which could mean
    that the given name is a path to a document file.
    Extract it's document type then and return both
    accordingly.

    Args:
        doc_type (str): The document type name.
        name (str): The document name or file path.

    Returns:
        tuple: Returns final document type as string, final document name.
    '''
    doc_repo = get_doc_repo()
    if not doc_type:
        # means that the given name should be a path
        # to a file directly
        doc_type = doc_repo.get_document_type_from_file(name)
        # also if the given name is not absolute nor have
        # "./" in the beginning, at the latter one at least
        if not name.startswith('/') and not name.startswith('./'):
            name = './' + name
    return doc_type, name


def get_doc_repo() -> DocumentRepository:
    '''
    Return the DocumentRepository which has the folder
    set according to the config.

    Returns:
        DocumentRepository: Returns the DocumentRepository instance.
    '''
    return DocumentRepository(str(Config().get('types_folder')))


def get_user(user_name: str = '') -> Document:
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
    doc_repo = get_doc_repo()
    user = doc_repo.load(user_name, str(Config().get('user_type')))
    return user
