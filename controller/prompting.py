from prompt_toolkit import prompt as ptk_prompt
from prompt_toolkit.completion import WordCompleter


def prompt(message: str, choices: list = []) -> str:
    """
    Prompting the user in the terminal without fancy GUI.

    Args:
        message (str): The message to display on prompting.
        choices (list): The options list. (default: `[]`)

    Returns:
        str: The prompting process.
    """
    completer = WordCompleter(choices)
    return ptk_prompt(message, completer=completer)
