from controller import prompting
from utils import config_utils
from model.invoice import Invoice
from model.script import Script
from model.settings import Settings
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
    # I import the modul just now, because the weasyprint modul loads
    # quite slowly. And I do not want the programm to start slow for
    # every other task to do.
    from view.render import Render
    R = Render()
    I = Invoice()
    output_filename = config_utils.replace_file_ending_with_pdf(filename)
    if not I.load_from_yaml_file(filename, False):
        p.print_error(f'Could not load "{filename}".')
        exit(1)
    R.set_template(template)
    if not R.render(I, output_filename):
        p.print_error(f'Could not render "{filename}".')
    else:
        p.print_success(f'Successfully rendered {output_filename}!')


@cli.command()
@click.argument('filename')
@click.argument('script')
def script(filename, script):
    """
    Use a custom user SCRIPT in the ~/.plainvoice/scripts folder
    to do stuff with the data from the FILENAME file (probably
    an invoice or quote).

    You can use the following variables inside your script:\n
      invoice: the invoice object
    """
    I = Invoice()
    if not I.load_from_yaml_file(filename, False):
        p.print_error(f'Could not load "{filename}".')
        exit(1)
    S = Script()
    if not S.load_script_string_from_python_file(script):
        p.print_error(f'Could not find script "{script}". Does it exist?')
        exit(1)
    if S.run(I):
        p.print_success(f'Ran script "{script}"!')
    else:
        p.print_error(f'Could not run script "{script}".')



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
