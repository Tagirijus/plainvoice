'''
doctype module

This module holds all the commands for the document type
handling.
'''

from plainvoice.controller.document_type_controller import \
    DocumentTypeController

import click


@click.group(context_settings=dict(help_option_names=['-h', '--help']))
@click.pass_context
def type(ctx):
    '''
    Create or edit document types.
    '''
    ctx = ctx


@type.command('edit')
@click.argument('name')
def type_edit(name):
    '''Create and / or edit a document type.'''
    DocumentTypeController().edit(name)


@type.command('hide')
@click.argument('name')
def type_hide(name):
    '''Hide a document type.'''
    DocumentTypeController().hide(name)


@click.option('-a', '--show-all', is_flag=True, help='Also list hidden items')
@type.command('list')
def type_list(show_all):
    '''List available and visible document types.'''
    DocumentTypeController().list(show_all)


@type.command('new')
@click.argument('name')
def type_new(name):
    '''
    Create a new document type or edit it if it exists already. It is basically
    an alias for the "edit" command.
    '''
    DocumentTypeController().edit(name)


@type.command('remove')
@click.argument('name')
def type_remove(name):
    '''Remove a document type.'''
    DocumentTypeController().remove(name)


@type.command('show')
@click.argument('name')
def type_show(name):
    '''Show a document type.'''
    DocumentTypeController().show(name)
