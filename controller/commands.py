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

    # from model.client import Client
    # C = Client()
    # if C.load('MSMS02'):
    #     p.print_success('Client loaded!')
    # else:
    #     p.print_error('Could not load client!')



    # from model.invoice import Invoice
    # I = Invoice()

    # I.client_id = 'MSMS01'
    # I.generate_receiver()
    # I.add_posting(
    #     'Musik',
    #     'Produktion von Musik',
    #     40.0,
    #     '1,20 min'
    # )
    # if I.save('Rechnung_2024_-_450'):
    #     p.print_success('Saved invoice!')
    # else:
    #     p.print_error('Could not save invoice!')

    # if I.load('Rechnung_2024_-_450'):
    #     p.print_success('Loaded invoice!')
    #     print(I.receiver)
    # else:
    #     p.print_error('Could not load invoice!')


    # from model.posting import Posting
    # P = Posting()
    # P.set_from_dict({
    #     'unit_price': '40',
    #     'amount': '1:30 h',
    #     'vat': '19 %'
    # })
    # print(P.calc_total())
    # print(P.calc_total(False))
    # print(P.calc_vat())

    from model.invoice import Invoice
    I = Invoice()
    I.add_posting(
        'Musik',
        'Musikproduktion',
        '100.0',
        '1:30 min',
        '19 %'
    )
    I.add_posting(
        'Sounddesign',
        'Produktion von Sounds',
        '100.0',
        '10 Stk',
        '19 %'
    )
    I.add_posting(
        'Nutzungsrecht',
        'Das Recht, alles nutzen zu dürfen',
        '250',
        '1',
        '7 %'
    )
    if I.save('Rechnung_2024_-_450'):
        p.print_success('Saved invoice!')
    else:
        p.print_error('Could not save invoice!')
