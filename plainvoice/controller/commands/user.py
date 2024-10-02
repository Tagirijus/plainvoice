'''
user module

This module holds all the commands for the user handling.
It works with the document type set in the config for "user"
and works as some kind of wrapper for the "document" command.
'''

from plainvoice.model.config import Config
from plainvoice.controller.document_controller import DocumentController

import click


@click.group(context_settings=dict(help_option_names=['-h', '--help']))
@click.pass_context
def user(ctx):
    '''
    Do stuff with users.
    '''
    ctx = ctx


@user.command('edit')
@click.argument('name')
def user_edit(name):
    '''
    Edit a user, if it exists. Also update its fixed fields
    according to the users document type.
    '''
    DocumentController().edit(str(Config().get('user_type')), name)


@user.command('hide')
@click.argument('name')
def user_hide(name):
    '''Hide a user.'''
    DocumentController().change_visibility(str(Config().get('user_type')), name, True)


@user.command('list')
@click.option('-a', '--show-all', is_flag=True, help='Also list hidden items')
def user_list(show_all):
    '''List available and visible users.'''
    DocumentController().list(str(Config().get('user_type')), show_all)


@user.command('new')
@click.argument('name')
def user_new(name):
    '''Create a new user or edit it if it exists already.'''
    DocumentController().new(str(Config().get('user_type')), name)


@user.command('remove')
@click.argument('name')
def user_remove(name):
    '''Remove a user.'''
    DocumentController().remove(str(Config().get('user_type')), name)


@user.command('render')
@click.argument('name')
@click.argument('template', required=False)
@click.option('-o', '--output-file', default='', help='The output file')
@click.pass_context
def user_render(ctx, name, template, output_file):
    '''Render a user.'''
    DocumentController().render(
        str(Config().get('user_type')), name, template, ctx.obj['user'], output_file
    )


@user.command('script')
@click.argument('name')
@click.argument('script', required=False)
@click.option('-q', '--quiet', is_flag=True, help='Do not output from plainvoice')
@click.pass_context
def user_script(ctx, name, script, quiet):
    '''Execute a script on the given user.'''
    DocumentController().script(
        str(Config().get('user_type')), name, script, ctx.obj['user'], quiet
    )


@user.command('show')
@click.argument('name')
def user_show(name):
    '''Show a user.'''
    DocumentController().change_visibility(str(Config().get('user_type')), name, False)


@user.command('update')
@click.argument('name')
def user_update(name):
    '''
    Update a user with new fixed fields according to a maybe
    updated user docuemnt type. After that edit it immediately.
    Basically this is just an alias for the edit command.
    '''
    DocumentController().edit(str(Config().get('user_type')), name)
