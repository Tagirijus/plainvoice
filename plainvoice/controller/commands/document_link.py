'''
document_linl module

This module holds all the commands for the document linking handling.
'''

from plainvoice.controller.document_controller import DocumentController

import click


@click.option(
    '-t',
    '--type',
    default='',
    help='The document type of the linked document'
)
@click.group(context_settings=dict(help_option_names=['-h', '--help']))
@click.pass_context
def link(ctx, type):
    '''
    Do linking stuff with documents.
    '''
    ctx = ctx
    ctx.obj['type_link'] = type


@link.command('add')
@click.argument('name_b')
@click.argument('name_a')
@click.pass_context
def doc_add(ctx, name_b, name_a):
    '''Add link between two documents.'''
    DocumentController().link_documents(
        ctx.obj['type'],
        name_a,
        ctx.obj['type_link'],
        name_b
    )
