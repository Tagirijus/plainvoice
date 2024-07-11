from prompt_toolkit import HTML
from prompt_toolkit import print_formatted_text

import os


def print_error(message: str) -> None:
    """
    Print error output.

    Args:
        message (str): The message to display.
    """
    print_formatted_text(HTML(f'<ansired>{message}</ansired>'))


def print_formatted(message: str) -> None:
    """
    Print formatted output.

    Args:
        message (str): \
            The message to display. Can have prompt_toolkit formatting \
            syntax in the string like <bold> or so.
    """
    print_formatted_text(HTML(message))


def print_info(message: str) -> None:
    """
    Print info output.

    Args:
        message (str): The message to display.
    """
    print_formatted_text(HTML(f'<ansiblue>{message}</ansiblue>'))


def print_items_in_columns(items: list[str], padding: int = 3) -> None:
    """
    Prints the given list in equally spread columns.

    Args:
        items (list): The items to print.
        padding (int): The padding between the elements. (default: `3`)
    """
    terminal_width = os.get_terminal_size().columns
    max_item_length = max(len(item) for item in items)
    col_width = max_item_length + padding
    num_cols = terminal_width // col_width

    for i, item in enumerate(items):
        end_char = "\n" if (i + 1) % num_cols == 0 else " " * padding
        print(f"{item:<{max_item_length}}", end=end_char)

    if len(items) % num_cols != 0:
        print()


def print_success(message: str) -> None:
    """
    Print success output.

    Args:
        message (str): The message to display.
    """
    print_formatted_text(HTML(f'<ansigreen>{message}</ansigreen>'))


def print_warning(message: str) -> None:
    """
    Print warning output.

    Args:
        message (str): The message to display.
    """
    print_formatted_text(HTML(f'<ansiyellow>{message}</ansiyellow>'))
