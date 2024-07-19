from plainvoice.model.client import Client
from plainvoice.model.document import Document
from plainvoice.model.config import Config
from plainvoice.model.scripts import Scripts
from plainvoice.model.templates import Templates
from plainvoice.utils import file_utils
from plainvoice.view import printing as p

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
@click.argument('arg')
def test(arg: str):
    '''WIP: for testing during development'''
    clients = Client()
    clients.load_from_yaml_file(arg)
    clients.disable()
    clients.save()
    file_utils.open_in_editor(clients.get_absolute_filename(arg))


@cli.group(context_settings=dict(help_option_names=['-h', '--help']))
def clients():
    '''
    Add, edit, list or delete clients.
    '''
    pass


@clients.command('delete')
@click.argument('clientid')
def clients_delete(clientid: str):
    '''Deletes a client with the given CLIENTID.'''
    client = Client()
    filename = client.get_absolute_filename(clientid)
    if file_utils.delete_file_with_prompt(filename):
        p.print_success(f'Deleted client "{clientid}" successfully.')
    else:
        p.print_info(f'Did not delete client "{clientid}".')


@clients.command('edit')
@click.argument('clientid')
def clients_edit(clientid: str):
    '''
    Edit a client (or add it new, if it does not exist).
    '''
    client = Client()
    client.client_id = clientid
    if not client.file_exists():
        client.save()
    # load and re-save it for appending missing (potentially new)
    # attributes / variables of the data set
    client.load_from_yaml_file(clientid)
    client.save()
    # then open it in the editor
    file_utils.open_in_editor(client.get_absolute_filename(clientid))


@clients.command('list')
@click.option(
    '-i',
    '--inactive',
    is_flag=True,
    help='List inactive clients as well'
)
def clients_list(inactive: bool):
    '''List available (or also inactive) clients.'''
    clients = Client()
    clients_list = clients.get_list()
    if clients_list:
        p.print_items_in_columns(clients_list)
    else:
        p.print_info('Either no clients or something went wrong.')


@cli.command()
def config():
    '''Open the config in the defined editor. By default this is vi.'''
    config = Config()

    # probably for the first time, create the config file
    if not config.file_exists():
        p.print_formatted(
            f'Creating default "config" new at "{config.datadir}/" ...'
        )
    # then save it, yet also save it eveytime to fill new attributes, which
    # were added later in the development
    config.save()
    # now load it
    file_utils.open_in_editor(config.configfile)


@cli.group(context_settings=dict(help_option_names=['-h', '--help']))
def invoices():
    '''
    Create, edit, list and delete invoices.
    '''
    pass


@invoices.command('create')
@click.argument('name')
def invoices_create(name):
    '''Create a new invoice.'''
    # TODO
    pass


@cli.command()
@click.argument('filename')
@click.argument('template')
def render(filename: str, template: str):
    '''Renders the given FILENAME with the given TEMPLATE name.'''
    # I import the modul just now, because the weasyprint modul loads
    # quite slowly. And I do not want the programm to start slow for
    # every other task to do.
    from view.render import Render
    render = Render()
    invoice = Document()
    output_filename = file_utils.replace_file_extension_with_pdf(filename)
    if not invoice.load_from_yaml_file(filename, False):
        p.print_error(f'Could not load "{filename}".')
        exit(1)
    render.set_template(template)
    if not render.render(invoice, output_filename):
        p.print_error(f'Could not render "{filename}".')
    else:
        p.print_success(f'Successfully rendered {output_filename}!')


@cli.group(context_settings=dict(help_option_names=['-h', '--help']))
def scripts():
    '''List or run custom scripts.'''
    pass


@scripts.command('delete')
@click.argument('scriptname')
def scripts_delete(scriptname: str):
    '''Deletes a script with the given SCRIPTNAME.'''
    scripts = Scripts()
    filename = scripts.get_absolute_filename(scriptname)
    if file_utils.delete_file_with_prompt(filename):
        p.print_success(f'Deleted script "{scriptname}" successfully.')
    else:
        p.print_info(f'Did not delete script "{scriptname}".')


@scripts.command('edit')
@click.argument('scriptname')
def scripts_edit(scriptname: str):
    '''
    Edit a script (or add it new, if it does not exist).
    '''
    scripts = Scripts()
    file_utils.open_in_editor(scripts.get_absolute_filename(scriptname))


@scripts.command('list')
def scripts_list():
    '''
    List possible scripts, which are located at ~/.plainvoice/scripts/*.py
    '''
    scripts = Scripts()
    scripts = scripts.get_list()
    if scripts:
        p.print_items_in_columns(scripts)
    else:
        p.print_info('Either no scripts or something went wrong.')


@scripts.command('run')
@click.argument('scriptname')
@click.argument('filename')
def scripts_run(scriptname: str, filename: str):
    '''
    Use a custom user SCRIPT in the ~/.plainvoice/scripts folder
    to do stuff with the data from the FILENAME file (probably
    an invoice or quote). A SCRIPTNAME is chosen without the
    file ending: scriptname.py will be executed when this command
    is ran with just the argument "scriptname", for example.

    You can use the following variables inside your script:\n
      invoice: the invoice object
    '''
    invoice = Document()
    if not invoice.load_from_yaml_file(filename, False):
        p.print_error(f'Could not load "{filename}".')
        exit(1)
    scripts = Scripts()
    if not scripts.load_script_string_from_python_file(scriptname):
        p.print_error(f'Could not find script "{scriptname}". Does it exist?')
        exit(1)
    ctx = click.get_current_context()
    verbose = ctx.obj.get('verbose', 0)
    if verbose >= 1:
        p.print_formatted('Trying to execute the follwing Python string:')
        p.print_formatted(scripts.python_string)
    if scripts.run(invoice):
        p.print_success(f'Ran script "{scriptname}"!')
    else:
        p.print_error(f'Could not run script "{scriptname}".')


@cli.group(context_settings=dict(help_option_names=['-h', '--help']))
def templates():
    '''List, add, edit or delete a render or posting template.'''
    pass


@templates.command('create')
@click.argument('templatename')
def templates_create(templatename: str):
    '''
    Initialize a new template on the basis of the default
    template and name it with the given TEMPLATENAME. It basically
    just will copy the default invoice.j2 template to the
    data dirs templates folder as a starting point.
    '''
    templates = Templates()
    if templates.create(templatename):
        p.print_success(
            'Copied default template to data dir'
            + f' folder with the name "{templatename}".'
        )
        file_utils.open_in_editor(
            templates.get_absolute_filename(templatename)
        )
    else:
        p.print_error(f'Could not copy default template to data dir folder.')


@templates.command('delete')
@click.argument('templatename')
def templates_delete(templatename: str):
    '''Deletes a template with the given TEMPLATENAME.'''
    templates = Templates()
    filename = templates.get_absolute_filename(templatename)
    if file_utils.delete_file_with_prompt(filename):
        p.print_success(f'Deleted template "{templatename}" successfully.')
    else:
        p.print_info(f'Did not delete template "{templatename}".')


@templates.command('edit')
@click.argument('templatename')
def templates_edit(templatename: str):
    '''
    Edit a template (or add it new, if it does not exist).
    '''
    templates = Templates()
    file_utils.open_in_editor(templates.get_absolute_filename(templatename))


@templates.command('list')
def templates_list():
    '''List available templates.'''
    templates = Templates()
    templates_list = templates.get_list()
    if templates_list:
        p.print_formatted(', '.join(templates_list))
    else:
        p.print_info('Either there are no templates or something went wrong.')
