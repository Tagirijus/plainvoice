from prompt_toolkit import HTML
from prompt_toolkit import print_formatted_text


def print_info(message: str) -> None:
    """
    Print info output.

    Args:
        message (str): The message to display.
    """
    print_formatted_text(HTML(f'<ansiblue>{message}</ansiblue>'))


def print_warning(message: str) -> None:
    """
    Print warning output.

    Args:
        message (str): The message to display.
    """
    print_formatted_text(HTML(f'<ansiyellow>{message}</ansiyellow>'))


def print_error(message: str) -> None:
    """
    Print error output.

    Args:
        message (str): The message to display.
    """
    print_formatted_text(HTML(f'<ansired>{message}</ansired>'))


def print_success(message: str) -> None:
    """
    Print success output.

    Args:
        message (str): The message to display.
    """
    print_formatted_text(HTML(f'<ansigreen>{message}</ansigreen>'))


def print_formatted(message: str) -> None:
    """
    Print formatted output.

    Args:
        message (str): \
            The message to display. Can have prompt_toolkit formatting \
            syntax in the string like <bold> or so.
    """
    print_formatted_text(HTML(message))
