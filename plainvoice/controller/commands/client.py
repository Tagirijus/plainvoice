'''
client module

This module holds all the commands for the client handling.
It works with the document type set in the config for "client"
and works as some kind of wrapper for the "document" command.
'''

from plainvoice.model.config import Config
from plainvoice.controller.document_controller import DocumentController

import click


@click.group(context_settings=dict(help_option_names=['-h', '--help']))
@click.pass_context
def client(ctx):
    '''
    Do stuff with clients.
    '''
    ctx = ctx


@client.command('edit')
@click.argument('name')
def client_edit(name):
    '''
    Edit a client, if it exists. Also update its fixed fields
    according to the clients document type.
    '''
    DocumentController().edit(str(Config().get('client_type')), name)


@client.command('hide')
@click.argument('name')
def client_hide(name):
    '''Hide a client.'''
    DocumentController().change_visibility(str(Config().get('client_type')), name, True)


@client.command('list')
@click.option('-a', '--show-all', is_flag=True, help='Also list hidden items')
def client_list(show_all):
    '''List available and visible clients.'''
    DocumentController().list(str(Config().get('client_type')), show_all)


@client.command('new')
@click.argument('name')
def client_new(name):
    '''Create a new client or edit it if it exists already.'''
    DocumentController().new(str(Config().get('client_type')), name)


@client.command('remove')
@click.argument('name')
def client_remove(name):
    '''Remove a client.'''
    DocumentController().remove(str(Config().get('client_type')), name)


@client.command('render')
@click.argument('name')
@click.argument('template', required=False)
@click.option('-o', '--output-file', default='', help='The output file')
@click.pass_context
def client_render(ctx, name, template, output_file):
    '''Render a client.'''
    DocumentController().render(
        str(Config().get('client_type')), name, template, ctx.obj['user'], output_file
    )


@client.command('script')
@click.argument('name')
@click.argument('script', required=False)
@click.option('-q', '--quiet', is_flag=True, help='Do not output from plainvoice')
@click.pass_context
def client_script(ctx, name, script, quiet):
    '''Execute a script on the given client.'''
    DocumentController().script(
        str(Config().get('client_type')), name, script, ctx.obj['user'], quiet
    )


@client.command('show')
@click.argument('name')
def client_show(name):
    '''Show a client.'''
    DocumentController().change_visibility(
        str(Config().get('client_type')), name, False
    )


@client.command('update')
@click.argument('name')
def client_update(name):
    '''
    Update a client with new fixed fields according to a maybe
    updated client docuemnt type. After that edit it immediately.
    Basically this is just an alias for the edit command.
    '''
    DocumentController().edit(str(Config().get('client_type')), name)
