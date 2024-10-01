'''
Some helper functions for e.g. getting user or helping
in the command line interface to get documents or
document repositories and so on.
'''

from plainvoice.model.config import Config
from plainvoice.model.document.document_repository import DocumentRepository


def get_doc_repo() -> DocumentRepository:
    '''
    Return the DocumentRepository which has the folder
    set according to the config.

    Returns:
        DocumentRepository: Returns the DocumentRepository instance.
    '''
    return DocumentRepository(str(Config().get('types_folder')))
