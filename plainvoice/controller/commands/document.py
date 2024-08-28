'''
document module

This module holds all the commands for the document handling.
'''

import click


@click.group(context_settings=dict(help_option_names=['-h', '--help']))
def doc():
    """
    Do stuff with documents.
    """
    print('DOCS')
