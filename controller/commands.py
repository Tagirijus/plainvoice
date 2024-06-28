from controller import prompting
from utils import config_utils
from model.settings import Settings
from model.template import Template
from view import printing as p

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
def cli(ctx, verbose):
    """
    Creating invoices and quotes with a plaintext mindset.
    """
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose


@cli.command()
def config():
    """Open the config in the defined editor. By default this is vi."""
    config_utils.edit_config()


@cli.command()
@click.argument('filename')
@click.argument('template')
def render(filename, template):
    """Renders the given FILENAME with the given TEMPLATE name."""
    # I import it just now, because the weasyprint modul loads quite
    # slowly. And I do not want the programm to start slow for every
    # other task to do.
    from view.render import Render
    R = Render()
    if not R.set_file(filename):
        p.print_error(f'"{filename}" not found.')
        exit(1)
    if not R.load_file():
        p.print_error(f'Error loading "{filename}"!')
        exit(1)
    if not R.set_template(template):
        p.print_error(f'Could not set template to "{template}". Does it exist?')
        exit(1)
    if not R.render():
        p.print_error(f'Could not render "{filename}".')
    else:
        p.print_success(f'Successfully rendered {R.output_filename}!')



@cli.command()
def templates():
    """List, add, edit or delete a render or posting template."""
    p.print_formatted(f'<i>Todo ...</i>')


@cli.command()
@click.argument('filename')
def test(filename):
    """WIP: for testing during development"""
    from model.invoice import Invoice
    I = Invoice()
    I.load(filename, False)
    I.add_posting(
        'Test',
        'Kommentar',
        10.0,
        2,
        0
    )
    if I.save(filename, False):
        p.print_success('Invoice saved!')
    else:
        p.print_error('Invoice NOT saved!')
