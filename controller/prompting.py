from prompt_toolkit import prompt as ptk_prompt
from prompt_toolkit.completion import WordCompleter


def prompt(message, choices=[]):
    completer = WordCompleter(choices)
    return ptk_prompt(message, completer=completer)
