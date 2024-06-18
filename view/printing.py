from prompt_toolkit import HTML
from prompt_toolkit import print_formatted_text


def print_info(message):
    print_formatted_text(HTML(f'<ansiblue>{message}</ansiblue>'))

def print_warning(message):
    print_formatted_text(HTML(f'<ansiyellow>{message}</ansiyellow>'))

def print_error(message):
    print_formatted_text(HTML(f'<ansired>{message}</ansired>'))

def print_success(message):
    print_formatted_text(HTML(f'<ansigreen>{message}</ansigreen>'))

def print_formatted(message):
    print_formatted_text(HTML(message))
