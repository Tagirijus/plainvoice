from rich.console import Console
from rich.text import Text


console = Console()


def print_info(message):
    text = Text(message, style="blue")
    console.print(text)

def print_warning(message):
    text = Text(message, style="yellow")
    console.print(text)

def print_error(message):
    text = Text(message, style="red")
    console.print(text)

def print_formatted(message):
    """
    Prints a message with embedded color tags.
    Example: print_formatted("This is [red]red[/red] and this is [blue]blue[/blue].")
    """
    console.print(message)
