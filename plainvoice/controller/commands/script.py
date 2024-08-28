'''
script module

This module holds all the commands for the scripts handling.
'''

from plainvoice.model.config import Config
from plainvoice.model.script.script_repository import ScriptRepository
from plainvoice.utils import file_utils

import click
import os


@click.group(context_settings=dict(help_option_names=['-h', '--help']))
def script():
    """
    Create or edit scripts.
    """
    pass


@script.command('edit')
@click.argument('name')
def script_edit(name):
    """Create and / or edit a script."""
    script_repo = ScriptRepository(str(Config().get('scripts_folder')))
    file_name = script_repo.get_absolute_filename(name)
    if not os.path.exists(file_name):
        script_repo.create_script(name)
    file_utils.open_in_editor(
        file_name
    )


@script.command('list')
def script_list():
    """List available scripts."""
    script_repo = ScriptRepository(
        str(Config().get('scripts_folder'))
    )
    print(', '.join(sorted(script_repo.get_script_names())))
