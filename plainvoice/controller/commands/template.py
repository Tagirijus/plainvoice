'''
template module

This module holds all the commands for the document type
handling.
'''

from plainvoice.model.config import Config
from plainvoice.model.template.template_repository import TemplateRepository
from plainvoice.utils import file_utils

import click
import os


@click.group(context_settings=dict(help_option_names=['-h', '--help']))
def template():
    """
    Create or edit templates.
    """
    pass


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
    """List available and visible templates."""
    template_repo = TemplateRepository(
        str(Config().get('templates_folder'))
    )
    print(', '.join(sorted(template_repo.get_template_names())))
