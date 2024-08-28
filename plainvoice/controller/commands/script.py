'''
script module

This module holds all the commands for the scripts handling.
'''

import click


@click.group(context_settings=dict(help_option_names=['-h', '--help']))
def script():
    """
    Create or edit scripts.
    """
    print('SCRIPTS')
