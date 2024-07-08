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


def prompt_yes_no(message: str) -> tuple[bool, str]:
    """
    Prompting the user for a simple yes/no question.

    Args:
        message (str): \
            The message to display on asking. It gets
            appended by " [(y)es/(n)o]" by default.

    Returns:
        tuple: \
            bool: True, if "yes" or "y" was answered.
            str: The prompting process.
    """
    answer = prompt(message + " [yes/no] ")
    return answer.lower() in ['yes', 'y'], answer
