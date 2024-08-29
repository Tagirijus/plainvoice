'''
script module

This module holds all the commands for the scripts handling.
'''

from plainvoice.controller.io_service.io_service import IOService as io
from plainvoice.model.config import Config
from plainvoice.model.script.script_repository import ScriptRepository
from plainvoice.utils import file_utils

import click


@click.group(context_settings=dict(help_option_names=['-h', '--help']))
@click.pass_context
def script(ctx):
    """
    Create or edit scripts.
    """
    ctx = ctx


@script.command('edit')
@click.argument('name')
def script_edit(name):
    """Create and / or edit a script."""
    script_repo = ScriptRepository(str(Config().get('scripts_folder')))
    if not script_repo.exists(name):
        script_repo.create_script(name)
    file_utils.open_in_editor(
        script_repo.get_absolute_filename(name)
    )


@script.command('list')
def script_list():
    """List available scripts."""
    script_repo = ScriptRepository(str(Config().get('scripts_folder')))
    io.print_list(sorted(script_repo.get_script_names()))


@script.command('new')
@click.argument('name')
@click.pass_context
def script_new(ctx, name):
    """
    Create a new scripts or edit it if it exists already. It is basically
    an alias for the "edit" command.
    """
    ctx.invoke(script_edit, name=name)


@script.command('remove')
@click.argument('name')
def script_remove(name):
    """Remove a script."""
    script_repo = ScriptRepository(str(Config().get('scripts_folder')))
    if script_repo.exists(name):
        if io.ask_yes_no(f'Remove script "{name}"?'):
            script_repo.remove(name)
            io.print(f'Script "{name}" removed.', 'success')
        else:
            io.print(f'Script "{name}" not removed.', 'warning')
    else:
        io.print(f'Script "{name}" not found.', 'warning')
