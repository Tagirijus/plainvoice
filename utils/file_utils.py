"""
TODO: This util still has parts from the VIEW inside it (view.printing).
      Normally I would like to separate it from the logic, yet at the
      moment I do have a headache to do so here ...
"""

import os
import subprocess
from controller.prompting import prompt, prompt_yes_no
from model.files import Files
from model.settings import Settings
from view import error_printing
from view import printing as p


def open_in_editor(filename: str) -> None:
    """
    Open the given file in the specified default editor.

    Args:
        filename (str): The file to open.
    """
    S = Settings()

    p.print_formatted(
        f'Opening "{filename}"'
        + f' with "{S.EDITOR}" ...'
    )

    subprocess.run([S.EDITOR, filename])


def edit_config() -> None:
    """
    Open the config file in the defined editor.
    """
    S = Settings()

    # probably for the first time, create the config file
    if not os.path.exists(S.CONFIGFILE):
        p.print_formatted(f'Creating default "config" at "{S.DATADIR}/" ...')
    # then save it, yet also save it eveytime to fill new attributes, which
    # were added later in the development
    Files().save_dict_to_yaml_file(
        S.get_config_as_dict(),
        S.CONFIGFILE
    )
    # now load it
    open_in_editor(S.CONFIGFILE)


def replace_file_extension_with_pdf(filename: str) -> str:
    """
    Replace the given input filename extension with .pdf.

    Args:
        filename (str): \
            Can be any filename with any extension in the filename \
            which will be replaced by ".pdf".

    Returns:
        str: The new output filename with .pdf extension.
    """
    if '.' in filename:
        name, _ = filename.rsplit('.', 1)
        return f'{name}.pdf'
    else:
        return f'{filename}.pdf'


def delete_file(filename: str) -> bool:
    """
    Deletes a filename after prompting was yes/y.

    Args:
        filename (str): The filename to delete.

    Returns:
        bool: Returns True on success.
    """
    answer, _ = prompt_yes_no(f'Delete "{filename}"?')
    if answer:
        Files().remove(filename)
        return True
    else:
        return False
