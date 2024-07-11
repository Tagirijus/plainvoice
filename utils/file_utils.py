"""
TODO: This util still has parts from the VIEW inside it (view.printing).
      Normally I would like to separate it from the logic, yet at the
      moment I do have a headache to do so here ...
"""

import subprocess
from controller.prompting import prompt_yes_no
from model.files import Files
from model.config import Config
from view import printing as p


def delete_file_with_prompt(filename: str) -> bool:
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


def open_in_editor(filename: str) -> None:
    """
    Open the given file in the specified default editor.

    Args:
        filename (str): The file to open.
    """
    config = Config()

    p.print_formatted(
        f'Opening "{filename}"'
        + f' with "{config.EDITOR}" ...'
    )

    subprocess.run([config.EDITOR, filename])


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
