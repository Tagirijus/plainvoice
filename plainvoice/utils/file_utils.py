'''
TODO: This util still has parts from the VIEW inside it (view.printing).
      Normally I would like to separate it from the logic, yet at the
      moment I do have a headache to do so here ...
'''

import subprocess
from plainvoice.controller.prompting import prompt_yes_no
from plainvoice.model.file.file import File
from plainvoice.model.config import Config
from plainvoice.view.printing import Printing as p


def delete_file_with_prompt(filename: str) -> bool:
    '''
    Deletes a filename after prompting was yes/y.

    Args:
        filename (str): The filename to delete.

    Returns:
        bool: Returns True on success.
    '''
    answer = prompt_yes_no(f'Delete "{filename}"?')
    if answer:
        File().remove(filename)
        return True
    else:
        return False


def open_in_editor(filename: str) -> None:
    '''
    Open the given file in the specified default editor.

    Args:
        filename (str): The file to open.
    '''
    config = Config()

    p.print_formatted(
        f'Opening "{filename}"'
        + f' with "{config.editor}" ...'
    )

    try:
        subprocess.run([config.editor, filename])
    except Exception as e:
        print(e)
        subprocess.run(['vi', filename])
