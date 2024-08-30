'''
document module

This module holds all the commands for the document handling.
'''

from plainvoice.controller.document_controller import DocumentController

import click


@click.option('-t', '--type', default='', help='The document type')
@click.group(context_settings=dict(help_option_names=['-h', '--help']))
@click.pass_context
def doc(ctx, type):
    '''
    Do stuff with documents.
    '''
    ctx = ctx
    ctx.obj['type'] = type


@doc.command('edit')
@click.argument('name')
@click.pass_context
def doc_edit(ctx, name):
    '''
    Edit a document, if it exists. Also update its fixed fields
    according to the document type.
    '''
    DocumentController().edit(ctx.obj['type'], name)


@doc.command('hide')
@click.argument('name')
@click.pass_context
def doc_hide(ctx, name):
    '''Hide a document.'''
    DocumentController().change_visibility(ctx.obj['type'], name, True)


@doc.command('list')
@click.option('-a', '--show-all', is_flag=True, help='Also list hidden items')
@click.pass_context
def doc_list(ctx, show_all):
    '''List available and visible documents.'''
    DocumentController().list(ctx.obj['type'], show_all)


@doc.command('new')
@click.argument('name')
@click.pass_context
def doc_new(ctx, name):
    '''Create a new document or edit it if it exists already.'''
    DocumentController().new(ctx.obj['type'], name)


@doc.command('remove')
@click.argument('name')
@click.pass_context
def doc_remove(ctx, name):
    '''Remove a document.'''
    DocumentController().remove(ctx.obj['type'], name)


@doc.command('render')
@click.argument('name')
@click.argument('template', required=False)
@click.option('-o', '--output-file', default='', help='The output file')
@click.pass_context
def doc_render(ctx, name, template, output_file):
    '''Render a document.'''
    DocumentController().render(
        ctx.obj['type'],
        name,
        template,
        ctx.obj['user'],
        output_file
    )


@doc.command('script')
@click.argument('name')
@click.argument('script', required=False)
@click.option(
    '-q',
    '--quiet',
    is_flag=True,
    help='Do not output from plainvoice'
)
@click.pass_context
def doc_script(ctx, name, script, quiet):
    '''Execute a script on the given document.'''
    DocumentController().script(
        ctx.obj['type'],
        name,
        script,
        ctx.obj['user'],
        quiet
    )


@doc.command('show')
@click.argument('name')
@click.pass_context
def doc_show(ctx, name):
    '''Show a document.'''
    DocumentController().change_visibility(ctx.obj['type'], name, False)


@doc.command('update')
@click.argument('name')
@click.pass_context
def doc_update(ctx, name):
    '''
    Update a document with new fixed fields according to a maybe
    updated docuemnt type. After that edit it immediately. Basically
    this is just an alias for the edit command.
    '''
    DocumentController().edit(ctx.obj['type'], name)
