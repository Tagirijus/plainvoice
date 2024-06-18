import click
from controller import utils
from controller import prompting
from model.settings import Settings
from model.templates import Templates
from view import printing


@click.group(
    context_settings=dict(help_option_names=['-h', '--help'])
)
def cli():
    """
    Creating invoices and quotes with a plaintext mindset.
    """
    pass


@cli.command()
def config():
    """Open the config in the defined editor. By default this is vi."""
    utils.edit_config()


@cli.command()
@click.argument(
    'name',
    default=None,
    type=click.Choice(Templates().get_types(), case_sensitive=False),
    required=False
)
def templates(name):
    """List, add, edit or delete a render or posting template."""
    T = Templates()
    if name is None:
        name = prompting.prompt('What type of template? ', choices=Templates().get_types())
    printing.print_formatted(f'"{name}" chosen')
