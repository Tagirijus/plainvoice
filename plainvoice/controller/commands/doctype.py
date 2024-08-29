'''
doctype module

This module holds all the commands for the document type
handling.
'''

from plainvoice.controller.io_service.io_service import IOService as io
from plainvoice.model.config import Config
from plainvoice.model.document.document_type_repository import \
    DocumentTypeRepository
from plainvoice.utils import file_utils

import click


@click.group(context_settings=dict(help_option_names=['-h', '--help']))
@click.pass_context
def type(ctx):
    """
    Create or edit document types.
    """
    ctx = ctx


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


@type.command('hide')
@click.argument('name')
def type_hide(name):
    """Hide a document type."""
    doc_type_repo = DocumentTypeRepository(
        str(Config().get('types_folder'))
    )
    if name in doc_type_repo.get_list(True).keys():
        doc_type = doc_type_repo.load_by_name(name)
        doc_type.hide()
        doc_type_repo.save(doc_type)
        io.print(f'Document type "{name}" now hidden.', 'success')
    else:
        io.print(f'Document type "{name}" not found.', 'warning')


@click.option('-a', '--show-all', is_flag=True, help='Also list hidden items')
@type.command('list')
def type_list(show_all):
    """List available and visible document types."""
    doc_type_repo = DocumentTypeRepository(
        str(Config().get('types_folder'))
    )
    io.print_list(sorted(doc_type_repo.get_list(not show_all).keys()))


@type.command('new')
@click.argument('name')
@click.pass_context
def type_new(ctx, name):
    """
    Create a new document type or edit it if it exists already. It is basically
    an alias for the "edit" command.
    """
    ctx.invoke(type_edit, name=name)


@type.command('remove')
@click.argument('name')
def type_remove(name):
    """Remove a document type."""
    type_repo = DocumentTypeRepository(str(Config().get('types_folder')))
    if type_repo.exists(name):
        if io.ask_yes_no(f'Remove type "{name}"?'):
            type_repo.remove(name)
            io.print(f'Template "{name}" removed.', 'success')
        else:
            io.print(f'Template "{name}" not removed.', 'warning')
    else:
        io.print(f'Template "{name}" not found.', 'warning')


@type.command('show')
@click.argument('name')
def type_show(name):
    """Show a document type."""
    doc_type_repo = DocumentTypeRepository(
        str(Config().get('types_folder'))
    )
    if name in doc_type_repo.get_list(False).keys():
        doc_type = doc_type_repo.load_by_name(name)
        doc_type.show()
        doc_type_repo.save(doc_type)
        io.print(f'Document type "{name}" now visible.', 'success')
    else:
        io.print(f'Document type "{name}" not found.', 'warning')
