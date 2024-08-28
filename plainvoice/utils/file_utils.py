'''
Some functions / helper for file handling and/or opening.
'''

from plainvoice.model.config import Config

import subprocess


def open_in_editor(file_name: str) -> None:
    '''
    Opens the given file in the defautl editor according
    to the config.

    Args:
        file_name (str): The file name to open.
    '''
    config = Config()
    try:
        subprocess.run([str(config.get('editor')), file_name])
    except Exception as e:
        print(e)
        subprocess.run(['vi', file_name])
