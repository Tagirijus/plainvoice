'''
template module

This module holds all the commands for the document type
handling.
'''

from plainvoice.controller.io_service.io_service import IOService as io
from plainvoice.model.config import Config
from plainvoice.model.template.template_repository import TemplateRepository
from plainvoice.utils import file_utils

import click
import os


@click.group(context_settings=dict(help_option_names=['-h', '--help']))
@click.pass_context
def template(ctx):
    """
    Create or edit templates.
    """
    ctx = ctx


@template.command('edit')
@click.argument('name')
def template_edit(name):
    """Create and / or edit a document type."""
    template_repo = TemplateRepository(str(Config().get('templates_folder')))
    file_name = template_repo.get_absolute_filename(name)
    if not os.path.exists(file_name):
        template_repo.create_template(name)
    file_utils.open_in_editor(
        file_name
    )


@template.command('list')
def template_list():
    """List available templates."""
    template_repo = TemplateRepository(
        str(Config().get('templates_folder'))
    )
    io.print_list(sorted(template_repo.get_template_names()))


@template.command('new')
@click.argument('name')
@click.pass_context
def template_new(ctx, name):
    """
    Create a new templates or edit it if it exists already. It is basically
    an alias for the "edit" command.
    """
    ctx.invoke(template_edit, name=name)


@template.command('remove')
@click.argument('name')
def template_remove(name):
    """Remove a template."""
    template_repo = TemplateRepository(str(Config().get('templates_folder')))
    if template_repo.exists(name):
        if io.ask_yes_no(f'Remove template "{name}"?'):
            template_repo.remove(name)
            io.print(f'Template "{name}" removed.', 'success')
        else:
            io.print(f'Template "{name}" not removed.', 'warning')
    else:
        io.print(f'Template "{name}" not found.', 'warning')
