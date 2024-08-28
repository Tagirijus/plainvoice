'''
commands module

The module combines certain command modueles to serve all needed
commands for the programm to be controlled via command line.
'''

from . import document
from . import doctype
from . import template
from . import script

from plainvoice.model.config import Config
from plainvoice.utils import file_utils

import click


@click.group(
    context_settings=dict(help_option_names=['-h', '--help'])
)
@click.option(
    '-v',
    '--verbose',
    count=True,
    help='Increase verbosity level (can be used multiple times)'
)
@click.pass_context
def cli(ctx: click.Context, verbose: bool):
    '''
    Creating invoices and quotes with a plaintext mindset.
    '''
    ctx.obj = ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose


@cli.command()
def config():
    '''Open the config in the defined editor. By default this is vi.'''
    config = Config()
    file_utils.open_in_editor(config.config_file)


cli.add_command(document.doc)
cli.add_command(doctype.type)
cli.add_command(template.template)
cli.add_command(script.script)
