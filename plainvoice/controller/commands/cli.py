'''
commands module

The module combines certain command modueles to serve all needed
commands for the programm to be controlled via command line.
'''

from . import client
from . import document
from . import doctype
from . import script
from . import template
from . import user

from plainvoice.model.config import Config
from plainvoice.utils import file_utils

import click


@click.group(context_settings=dict(help_option_names=['-h', '--help']))
@click.option(
    '-v',
    '--verbose',
    count=True,
    help='Increase verbosity level (can be used multiple times)',
)
@click.option(
    '-u',
    '--user',
    default='',
    help='Set the user to use. See config comments for more info.',
)
@click.pass_context
def pv_cli(ctx: click.Context, verbose: bool, user: str):
    '''
    Creating invoices and quotes with a plaintext mindset.
    '''
    ctx.obj = ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose
    ctx.obj['user'] = user


@pv_cli.command()
def config():
    '''Open the config in the defined editor. By default this is vi.'''
    config = Config()
    file_utils.open_in_editor(config.config_file)


pv_cli.add_command(client.client)
pv_cli.add_command(document.doc)
pv_cli.add_command(doctype.type)
pv_cli.add_command(script.script)
pv_cli.add_command(template.template)
pv_cli.add_command(user.user)
