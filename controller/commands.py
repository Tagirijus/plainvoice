from controller.list_chooser import ListChooser
from model.clients import Clients
from model.invoices import Invoices
from model.scripts import Scripts
from model.templates import Templates
from utils import file_utils
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
def cli(ctx: click.Context, verbose: bool):
    """
    Creating invoices and quotes with a plaintext mindset.
    """
    ctx.obj = ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose


@cli.command()
@click.argument('filename')
def test(filename: str):
    """WIP: for testing during development"""
    LC = ListChooser(['test', 'zwei', 'drei'])
    user = LC.prompt()
    print(user)

    # from model.clients import Clients
    # C = Clients()
    # C.attention = 'Attn.'
    # C.company = 'Tagirijus GmbH & CO KG\nPupsen-Stark'
    # C.first_name = 'Manu'
    # C.last_name = 'Senf'
    # C.street = 'Straßy 1'
    # C.postcode = '12345'
    # C.city = 'Hausen'
    # print(C.generate_receiver())

    # from model.invoices import Invoice
    # Inv = Invoice()
    # Inv.load_from_yaml_file(filename, False)
    # Inv.add_posting(
    #     'Test',
    #     'Kommentar',
    #     '10.0',
    #     '2',
    #     '0 %'
    # )
    # if Inv.save_to_yaml_file(filename, False):
    #     p.print_success('Invoice saved!')
    # else:
    #     p.print_error('Invoice NOT saved!')


@cli.group(context_settings=dict(help_option_names=['-h', '--help']))
def clients():
    """
    Add, edit, list or delete clients.
    """
    pass


@clients.command('delete')
@click.argument('clientid')
def clients_delete(clientid: str):
    """Deletes a client with the given CLIENTID."""
    C = Clients()
    filename = C.get_absolute_filename(clientid)
    if file_utils.delete_file_with_prompt(filename):
        p.print_success(f'Deleted client "{clientid}" successfully.')
    else:
        p.print_info(f'Did not delete client "{clientid}".')


@clients.command('edit')
@click.argument('clientid')
def clients_edit(clientid: str):
    """
    Edit a client (or add it new, if it does not exist).
    """
    C = Clients()
    C.client_id = clientid
    if not C.file_exists():
        C.save()
    # load and re-save it for appending missing (potentially new)
    # attributes / variables of the data set
    C.load_from_yaml_file(clientid)
    C.save()
    # then open it in the editor
    file_utils.open_in_editor(C.get_absolute_filename(clientid))


@clients.command('list')
@click.option(
    '-i',
    '--inactive',
    is_flag=True,
    help='List inactive clients as well'
)
def clients_list(inactive: bool):
    """List available (or also inactive) clients."""
    C = Clients()
    clients = C.get_list()
    if clients:
        p.print_items_in_columns(clients)
    else:
        p.print_info('Either no clients or something went wrong.')


@cli.command()
def config():
    """Open the config in the defined editor. By default this is vi."""
    file_utils.edit_config()


@cli.command()
@click.argument('filename')
@click.argument('template')
def render(filename: str, template: str):
    """Renders the given FILENAME with the given TEMPLATE name."""
    # I import the modul just now, because the weasyprint modul loads
    # quite slowly. And I do not want the programm to start slow for
    # every other task to do.
    from view.render import Render
    R = Render()
    Inv = Invoices()
    output_filename = file_utils.replace_file_extension_with_pdf(filename)
    if not Inv.load_from_yaml_file(filename, False):
        p.print_error(f'Could not load "{filename}".')
        exit(1)
    R.set_template(template)
    if not R.render(Inv, output_filename):
        p.print_error(f'Could not render "{filename}".')
    else:
        p.print_success(f'Successfully rendered {output_filename}!')


@cli.group(context_settings=dict(help_option_names=['-h', '--help']))
def scripts():
    """List or run custom scripts."""
    pass


@scripts.command('delete')
@click.argument('scriptname')
def scripts_delete(scriptname: str):
    """Deletes a script with the given SCRIPTNAME."""
    S = Scripts()
    filename = S.get_absolute_filename(scriptname)
    if file_utils.delete_file_with_prompt(filename):
        p.print_success(f'Deleted script "{scriptname}" successfully.')
    else:
        p.print_info(f'Did not delete script "{scriptname}".')


@scripts.command('edit')
@click.argument('scriptname')
def scripts_edit(scriptname: str):
    """
    Edit a script (or add it new, if it does not exist).
    """
    S = Scripts()
    file_utils.open_in_editor(S.get_absolute_filename(scriptname))


@scripts.command('list')
def scripts_list():
    """
    List possible scripts, which are located at ~/.plainvoice/scripts/*.py
    """
    S = Scripts()
    scripts = S.get_list()
    if scripts:
        p.print_items_in_columns(scripts)
    else:
        p.print_info('Either no scripts or something went wrong.')


@scripts.command('run')
@click.argument('scriptname')
@click.argument('filename')
def scripts_run(scriptname: str, filename: str):
    """
    Use a custom user SCRIPT in the ~/.plainvoice/scripts folder
    to do stuff with the data from the FILENAME file (probably
    an invoice or quote). A SCRIPTNAME is chosen without the
    file ending: scriptname.py will be executed when this command
    is ran with just the argument "scriptname", for example.

    You can use the following variables inside your script:\n
      invoice: the invoice object
    """
    Inv = Invoices()
    if not Inv.load_from_yaml_file(filename, False):
        p.print_error(f'Could not load "{filename}".')
        exit(1)
    S = Scripts()
    if not S.load_script_string_from_python_file(scriptname):
        p.print_error(f'Could not find script "{scriptname}". Does it exist?')
        exit(1)
    ctx = click.get_current_context()
    verbose = ctx.obj.get('verbose', 0)
    if verbose >= 1:
        p.print_formatted('Trying to execute the follwing Python string:')
        p.print_formatted(S.python_string)
    if S.run(Inv):
        p.print_success(f'Ran script "{scriptname}"!')
    else:
        p.print_error(f'Could not run script "{scriptname}".')


@cli.group(context_settings=dict(help_option_names=['-h', '--help']))
def templates():
    """List, add, edit or delete a render or posting template."""
    pass


@templates.command('create')
@click.argument('templatename')
def templates_create(templatename: str):
    """
    Initialize a new template on the basis of the default
    template and name it with the given TEMPLATENAME. It basically
    just will copy the default invoice.j2 template to the
    data dirs templates folder as a starting point.
    """
    T = Templates()
    if T.create(templatename):
        p.print_success(
            'Copied default template to data dir'
            + f' folder with the name "{templatename}".'
        )
        file_utils.open_in_editor(T.get_absolute_filename(templatename))
    else:
        p.print_error(f'Could not copy default template to data dir folder.')


@templates.command('delete')
@click.argument('templatename')
def templates_delete(templatename: str):
    """Deletes a template with the given TEMPLATENAME."""
    T = Templates()
    filename = T.get_absolute_filename(templatename)
    if file_utils.delete_file_with_prompt(filename):
        p.print_success(f'Deleted template "{templatename}" successfully.')
    else:
        p.print_info(f'Did not delete template "{templatename}".')


@templates.command('edit')
@click.argument('templatename')
def templates_edit(templatename: str):
    """
    Edit a template (or add it new, if it does not exist).
    """
    S = Templates()
    file_utils.open_in_editor(S.get_absolute_filename(templatename))


@templates.command('list')
def templates_list():
    """List available templates."""
    T = Templates()
    templates = T.get_list()
    if templates:
        p.print_formatted(', '.join(templates))
    else:
        p.print_info('Either there are no templates or something went wrong.')
