'''
doctype module

This module holds all the commands for the document type
handling.
'''

import click


@click.group(context_settings=dict(help_option_names=['-h', '--help']))
def doctype():
    """
    Create or edit document types.
    """
    print('DOCTYPES')
