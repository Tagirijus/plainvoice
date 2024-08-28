'''
template module

This module holds all the commands for the document type
handling.
'''

import click


@click.group(context_settings=dict(help_option_names=['-h', '--help']))
def template():
    """
    Create or edit templates.
    """
    print('TEMPLATES')
