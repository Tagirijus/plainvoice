'''
template module

This module holds all the commands for the document type
handling.
'''

from plainvoice.controller.template_controller import TemplateController

import click


@click.group(context_settings=dict(help_option_names=['-h', '--help']))
@click.pass_context
def template(ctx):
    '''
    Create or edit templates.
    '''
    ctx = ctx


@template.command('edit')
@click.argument('name')
def template_edit(name):
    '''Create and / or edit a document type.'''
    TemplateController().edit(name)


@template.command('list')
def template_list():
    '''List available templates.'''
    TemplateController().list()


@template.command('new')
@click.argument('name')
def template_new(name):
    '''
    Create a new templates or edit it if it exists already. It is basically
    an alias for the "edit" command.
    '''
    TemplateController().edit(name)


@template.command('remove')
@click.argument('name')
def template_remove(name):
    '''Remove a template.'''
    TemplateController().remove(name)
