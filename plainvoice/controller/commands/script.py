'''
script module

This module holds all the commands for the scripts handling.
'''

from plainvoice.controller.script_controller import ScriptController

import click


@click.group(context_settings=dict(help_option_names=['-h', '--help']))
@click.pass_context
def script(ctx):
    '''
    Create or edit scripts.
    '''
    ctx = ctx


@script.command('edit')
@click.argument('name')
def script_edit(name):
    '''Create and / or edit a script.'''
    ScriptController().edit(name)


@script.command('list')
def script_list():
    '''List available scripts.'''
    ScriptController().list()


@script.command('new')
@click.argument('name')
def script_new(name):
    '''
    Create a new scripts or edit it if it exists already. It is basically
    an alias for the "edit" command.
    '''
    ScriptController().edit(name)


@script.command('remove')
@click.argument('name')
def script_remove(name):
    '''Remove a script.'''
    ScriptController().remove(name)
