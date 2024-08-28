'''
template module

This module holds all the commands for the document type
handling.
'''

from plainvoice.model.config import Config
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
    # I import it only if needed, since weasyprint loads slowly
    from plainvoice.view.render import Render

    render = Render(str(Config().get('templates_folder')))
    file_name = render.get_absolute_filename(name)
    if not os.path.exists(file_name):
        render.create_template(name)
    file_utils.open_in_editor(
        file_name
    )
