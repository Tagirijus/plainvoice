'''
document module

This module holds all the commands for the document handling.
'''

from plainvoice.controller.iomanager.iomanager import IOManager as io
from plainvoice.model.config import Config
from plainvoice.model.document.document_repository import DocumentRepository
from plainvoice.utils import file_utils

import click


def get_doc_type_and_name(type: str | None, name: str) -> tuple:
    '''
    Get a document name and a document type by the given
    arguments. While type cna be none, which could mean
    that the given name is a path to a document file.
    Extract it's document type then and return both
    accordingly.

    Args:
        type (str): The document type name.
        name (str): The document name or file path.

    Returns:
        str: Returns final document type as string.
    '''
    doc_repo = DocumentRepository(
        str(Config().get('types_folder'))
    )
    if not type:
        # means that the given name should be a path
        # to a file directly
        type = doc_repo.get_document_type_from_file(name)
        # also if the given name is not absolute nor have
        # "./" in the beginning, at the latter one at least
        if not name.startswith('/') and not name.startswith('./'):
            name = './' + name
    return type, name


@click.option('-t', '--type', default='', help='The document type')
@click.group(context_settings=dict(help_option_names=['-h', '--help']))
@click.pass_context
def doc(ctx, type):
    """
    Do stuff with documents.
    """
    ctx.obj = {}
    ctx.obj['type'] = type


@doc.command('edit')
@click.argument('name')
@click.pass_context
def doc_edit(ctx, name):
    """Create and / or edit a document."""
    doc_repo = DocumentRepository(
        str(Config().get('types_folder'))
    )
    type, name = get_doc_type_and_name(ctx.obj['type'], name)
    if doc_repo.exists(type, name):
        file_utils.open_in_editor(
            doc_repo.get_filename(type, name)
        )
    else:
        io.print(f'Document "{name}" not found!', 'warning')


@doc.command('list')
@click.pass_context
def doc_list(ctx):
    """List available and visible documents."""
    doc_repo = DocumentRepository(
        str(Config().get('types_folder'))
    )
    type = ctx.obj['type']
    docs_list = doc_repo.get_list(type, True)
    if docs_list:
        io.print_list(
            sorted(
                doc_repo.get_list(type, True).keys()
            )
        )
    else:
        io.print(f'No documents found for type "{type}".', 'warning')
