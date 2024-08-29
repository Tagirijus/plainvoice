'''
document module

This module holds all the commands for the document handling.
'''

from plainvoice.controller.iomanager.iomanager import IOManager as io
from plainvoice.model.config import Config
from plainvoice.model.document.document_repository import DocumentRepository
from plainvoice.model.script.script_repository import ScriptRepository
from plainvoice.model.template.template_repository import TemplateRepository
from plainvoice.utils import file_utils

import click


def get_doc_type_and_name(doc_type: str | None, name: str) -> tuple:
    '''
    Get a document name and a document type by the given
    arguments. While type cna be none, which could mean
    that the given name is a path to a document file.
    Extract it's document type then and return both
    accordingly.

    Args:
        doc_type (str): The document type name.
        name (str): The document name or file path.

    Returns:
        str: Returns final document type as string.
    '''
    doc_repo = DocumentRepository(str(Config().get('types_folder')))
    if not doc_type:
        # means that the given name should be a path
        # to a file directly
        doc_type = doc_repo.get_document_type_from_file(name)
        # also if the given name is not absolute nor have
        # "./" in the beginning, at the latter one at least
        if not name.startswith('/') and not name.startswith('./'):
            name = './' + name
    return doc_type, name


@click.option('-t', '--type', default='', help='The document type')
@click.group(context_settings=dict(help_option_names=['-h', '--help']))
@click.pass_context
def doc(ctx, type):
    """
    Do stuff with documents.
    """
    ctx.obj = {}
    ctx.obj['type'] = type


@doc.command('edit')
@click.argument('name')
@click.pass_context
def doc_edit(ctx, name):
    """Edit a document, if it exists."""
    doc_repo = DocumentRepository(str(Config().get('types_folder')))
    doc_type, name = get_doc_type_and_name(ctx.obj['type'], name)
    if doc_repo.exists(doc_type, name):
        file_utils.open_in_editor(
            doc_repo.get_filename(doc_type, name)
        )
    else:
        io.print(f'Document "{name}" not found!', 'warning')


@doc.command('hide')
@click.argument('name')
@click.pass_context
def doc_hide(ctx, name):
    """Hide a document."""
    doc_repo = DocumentRepository(str(Config().get('types_folder')))
    doc_type, name = get_doc_type_and_name(ctx.obj['type'], name)
    if doc_repo.exists(doc_type, name):
        doc = doc_repo.load(name, doc_type)
        doc.hide()
        doc_repo.save(doc)
        io.print(f'Document "{name}" now hidden.', 'success')
    else:
        io.print(f'Document "{name}" not found.', 'warning')


@doc.command('list')
@click.option('-a', '--show-all', is_flag=True, help='Also list hidden items')
@click.pass_context
def doc_list(ctx, show_all):
    """List available and visible documents."""
    doc_repo = DocumentRepository(str(Config().get('types_folder')))
    type = ctx.obj['type']
    # show_all has to be inverted, since the method will accept the keyword
    # show_only_visible, but for the cli interface I want to have the
    # flag to be used on showing all; thus logically it has to be named
    # different and the value has to be inverted then. bit confusing, but
    # hopefully no biggie after all ...
    docs_list = doc_repo.get_list(type, not show_all)
    if docs_list:
        io.print_list(
            sorted(
                doc_repo.get_list(type, not show_all).keys()
            )
        )
    else:
        io.print(f'No documents found for type "{type}".', 'warning')


@doc.command('new')
@click.argument('name')
@click.pass_context
def doc_new(ctx, name):
    """Create a new document or edit it if it exists already."""
    doc_repo = DocumentRepository(str(Config().get('types_folder')))
    doc_type, name = get_doc_type_and_name(ctx.obj['type'], name)
    if doc_type is None:
        io.print(f'Please specify a document type with -t/--type!', 'warning')
    else:
        doc_repo.create_document(doc_type, name)
        file_utils.open_in_editor(
            doc_repo.get_filename(doc_type, name)
        )


@doc.command('remove')
@click.argument('name')
@click.pass_context
def doc_remove(ctx, name):
    """Remove a document."""
    doc_repo = DocumentRepository(str(Config().get('types_folder')))
    doc_type, name = get_doc_type_and_name(ctx.obj['type'], name)
    if doc_repo.exists(doc_type, name):
        if io.ask_yes_no(f'Remove document "{name}"?'):
            doc_repo.remove(doc_type, name)
            io.print(f'Document "{name}" removed.', 'success')
        else:
            io.print(f'Document "{name}" not removed.', 'warning')
    else:
        io.print(f'Document "{name}" not found.', 'warning')


@doc.command('render')
@click.argument('name')
@click.argument('template', required=False)
@click.option('-o', '--output-file', default='', help='The output file')
@click.pass_context
def doc_render(ctx, name, template, output_file):
    """Render a document."""
    doc_repo = DocumentRepository(str(Config().get('types_folder')))
    doc_type, name = get_doc_type_and_name(ctx.obj['type'], name)
    template_repo = TemplateRepository(str(Config().get('templates_folder')))
    if template is None:
        io.print(f'Specify a template. Choose one of those:', 'warning')
        io.print_list(sorted(template_repo.get_template_names()))
    else:
        if doc_repo.exists(doc_type, name):
            # create the render engine; import only on demand,
            # since weasyprint is slow loading
            from plainvoice.view.render import Render
            render = Render(str(Config().get('templates_folder')))

            # load the document and render it
            doc = doc_repo.load(name, doc_type)
            if render.render(template, doc, output_file):
                io.print(
                    f'Rendered document "{name}" successfully.', 'success'
                )
            else:
                io.print(f'Rendering document "{name}" went wrong.', 'error')
        else:
            io.print(f'Document "{name}" not found.', 'warning')


@doc.command('script')
@click.argument('name')
@click.argument('script', required=False)
@click.option(
    '-q',
    '--quiet',
    is_flag=True,
    help='Do not output from plainvoice'
)
@click.pass_context
def doc_script(ctx, name, script, quiet):
    """Execute a script on the given document."""
    doc_repo = DocumentRepository(str(Config().get('types_folder')))
    doc_type, name = get_doc_type_and_name(ctx.obj['type'], name)
    script_repo = ScriptRepository(str(Config().get('scripts_folder')))
    if script is None:
        io.print(f'Specify a script. Choose one of those:', 'warning')
        io.print_list(sorted(script_repo.get_script_names()))
    else:
        if doc_repo.exists(doc_type, name):
            # get script
            script_obj = script_repo.load(script)

            # load the document and pass it to the script
            doc = doc_repo.load(name, doc_type)
            if not quiet:
                io.print(
                    f'Running script "{script}" on document "{name}" ...',
                    'success'
                )
            script_obj.run(doc)
        else:
            io.print(f'Document "{name}" not found.', 'warning')


@doc.command('show')
@click.argument('name')
@click.pass_context
def doc_show(ctx, name):
    """Hide a document."""
    doc_repo = DocumentRepository(str(Config().get('types_folder')))
    doc_type, name = get_doc_type_and_name(ctx.obj['type'], name)
    if doc_repo.exists(doc_type, name):
        doc = doc_repo.load(name, doc_type)
        doc.show()
        doc_repo.save(doc)
        io.print(f'Document "{name}" now visible.', 'success')
    else:
        io.print(f'Document "{name}" not found.', 'warning')
