from controller import prompting
from controller import utils
from model.settings import Settings
from model.template import Template
from view import printing as p

import click


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
@click.argument('filename')
@click.argument('template')
def render(filename, template):
    """Renders the given file with the given template name."""
    from view.renderer import Renderer
    R = Renderer()
    if not R.set_data(filename):
        p.print_error(f'"{data}" not found.')
        exit(1)
    if not R.set_template(template):
        p.print_error(f'Could not set template to "{template}". Does it exist?')
        exit(1)
    if not R.render():
        p.print_error(f'Could not render "{filename}".')
    else:
        p.print_success(f'Successfully rendered {R.get_output_filename()}!')



@cli.command()
@click.argument(
    'name',
    default=None,
    type=click.Choice(Template().types, case_sensitive=False),
    required=False
)
def templates(name):
    """List, add, edit or delete a render or posting template."""
    T = Template()
    if name is None:
        name = prompting.prompt('What type of template? ', choices=Template().types)
    p.print_formatted(f'"{name}" chosen')


@cli.command()
def test():
    """TESTING"""
    from model.client import Client
    C = Client()
    # C.client_id = 'MSMS01'
    # C.first_name = 'Manuel'
    if C.load('MSMS01'):
        p.print_success('Loaded client!')
        print(C.default_wage)
    else:
        p.print_error('Could not load client!')
