'''
document module

This module holds all the commands for the document handling.
'''

from . import document_link

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


@doc.command('due')
@click.option(
    '-d', '--due-only', is_flag=True, help='List only due without overdue items'
)
@click.option(
    '-o',
    '--overdue-only',
    is_flag=True,
    help='List only overdue without due-only items',
)
@click.option('-a', '--show-all', is_flag=True, help='Also list hidden items')
@click.pass_context
def doc_due(ctx, due_only, overdue_only, show_all):
    '''
    List all documents of a certain type (or all  types if not defined),
    which are due.
    '''
    DocumentController().list_due(ctx.obj['type'], due_only, overdue_only, show_all)


@doc.command('done')
@click.argument('code')
@click.option(
    '-d', '--date', default='', help='Set the date for the done-date via CLI already'
)
@click.option(
    '-f',
    '--force',
    is_flag=True,
    help='Force set the via --date/-d set date without asking',
)
@click.pass_context
def doc_done(ctx, code, date, force):
    '''
    Set the document with the given CODE to "done". This will
    set the documents "done date" to the given date, or it
    will ask for a date to set it to.
    '''
    DocumentController().set_document_done(ctx.obj['type'], code, date, force)


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
@click.argument('name', default='', required=False)
@click.option(
    '-c', '--client', default='', help='The client to link to the new document directly'
)
@click.pass_context
def doc_new(ctx, name='', client=''):
    '''Create a new document or edit it if it exists already.'''
    DocumentController().new(ctx.obj['type'], name, client, ctx.obj['user'])


@doc.command('populate')
@click.argument('name')
@click.pass_context
def doc_populate(ctx, name):
    '''
    Populate fields in a document. This will also "update" the document so that it will
    have all fields according to the (maybe updated) document type.
    '''
    DocumentController().populate(ctx.obj['type'], name, ctx.obj['user'])


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
        ctx.obj['type'], name, template, ctx.obj['user'], output_file
    )


@doc.command('script')
@click.argument('name')
@click.argument('script', required=False)
@click.option('-q', '--quiet', is_flag=True, help='Do not output from plainvoice')
@click.pass_context
def doc_script(ctx, name, script, quiet):
    '''Execute a script on the given document.'''
    DocumentController().script(ctx.obj['type'], name, script, ctx.obj['user'], quiet)


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


doc.add_command(document_link.link)
