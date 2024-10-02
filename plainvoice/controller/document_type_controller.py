'''
DocumentTypeController class

Handles DocumentType managing.
'''

from plainvoice.controller.io_facade.io_facade import IOFacade as io
from plainvoice.model.config import Config
from plainvoice.model.document.document_type_repository import DocumentTypeRepository
from plainvoice.utils import file_utils


class DocumentTypeController:
    '''
    Handles DocumentType managing.
    '''

    def __init__(self):
        '''
        Handles DocumentType managing.
        '''
        self.doc_type_repo = DocumentTypeRepository(str(Config().get('types_folder')))

    def edit(self, name: str) -> None:
        '''
        Edit the document type with the given name.

        Args:
            name (str): The name of the document type.
        '''
        if name not in self.doc_type_repo.get_list(True).keys():
            self.doc_type_repo.create_type(name)
        file_utils.open_in_editor(self.doc_type_repo.get_absolute_filename(name))

    def hide(self, name: str) -> None:
        '''
        Hide the document type with the given name.

        Args:
            name (str): The name of the document type.
        '''
        if name in self.doc_type_repo.get_list(True).keys():
            doc_type = self.doc_type_repo.load_by_name(name)
            doc_type.hide()
            self.doc_type_repo.save(doc_type)
            io.print(f'Document type "{name}" now hidden.', 'success')
        else:
            io.print(f'Document type "{name}" not found.', 'warning')

    def list(self, show_all: bool) -> None:
        '''
        List document types.

        Args:
            show_all (bool): If True, shows also hidden types.
        '''
        # show_all is on the show_only_visible argument; thus
        # it has to be inverted to act correct
        io.print_list(sorted(self.doc_type_repo.get_list(not show_all).keys()))

    def remove(self, name: str) -> None:
        '''
        Remove the document type with the given name.

        Args:
            name (str): The name of the document type.
        '''
        if self.doc_type_repo.exists(name):
            if io.ask_yes_no(f'Remove type "{name}"?'):
                self.doc_type_repo.remove(name)
                io.print(f'Template "{name}" removed.', 'success')
            else:
                io.print(f'Template "{name}" not removed.', 'warning')
        else:
            io.print(f'Template "{name}" not found.', 'warning')

    def show(self, name: str) -> None:
        '''
        Show the document type with the given name.

        Args:
            name (str): The name of the document type.
        '''
        if name in self.doc_type_repo.get_list(False).keys():
            doc_type = self.doc_type_repo.load_by_name(name)
            doc_type.show()
            self.doc_type_repo.save(doc_type)
            io.print(f'Document type "{name}" now visible.', 'success')
        else:
            io.print(f'Document type "{name}" not found.', 'warning')
