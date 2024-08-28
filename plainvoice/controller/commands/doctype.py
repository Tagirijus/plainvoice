'''
doctype module

This module holds all the commands for the document type
handling.
'''

import click


@click.group(context_settings=dict(help_option_names=['-h', '--help']))
def type():
    """
    Create or edit document types.
    """
    pass


@type.command('edit')
@click.argument('name')
def type_edit(name):
    """Create and / or edit a document type."""
    print(name)
