'''
doctype module

This module holds all the commands for the document type
handling.
'''

from plainvoice.model.config import Config
from plainvoice.model.document.document_type_repository import \
    DocumentTypeRepository
from plainvoice.utils import file_utils

import click


@click.group(context_settings=dict(help_option_names=['-h', '--help']))
def type():
    """
    Create or edit document types.
    """
    pass


@type.command('edit')
@click.argument('name')
def type_edit(name):
    """Create and / or edit a document type."""
    doc_type_repo = DocumentTypeRepository(
        str(Config().get('types_folder'))
    )
    if name not in doc_type_repo.get_list(True).keys():
        doc_type_repo.create_type(name)
    file_utils.open_in_editor(
        doc_type_repo.get_absolute_filename(name)
    )
