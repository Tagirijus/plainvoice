'''
Printing class

With this class I want to have some kind of wrapper for certain
moduls for output. There is also the IOFacade class, which might
seem very similar. Yet the IOFacade class will mainly use this
class' methods so that in case I want to switch certain output
moduls, I only have to do it here and not change logic too much
in the end.
'''

import click
import os
import rich

from rich import box
from rich.console import Console
from rich.table import Table


class Printing:
    '''
    Simple printing output methods.
    '''

    @staticmethod
    def print_error(message: str) -> None:
        '''
        Print error output.

        Args:
            message (str): The message to display.
        '''
        rich.print(f':warning: [red]{message}[/red]')

    @staticmethod
    def print_formatted(message: str) -> None:
        '''
        Print formatted output.

        Args:
            message (str): \
                The message to display. Can have prompt_toolkit formatting \
                syntax in the string like <bold> or so.
        '''
        rich.print(message)

    @staticmethod
    def print_if_verbose(err: Exception) -> None:
        '''
        This function checks if "verbose" is enabled and then
        prints out error messages with traceback on level 2
        of verbosity.

        Args:
            err (str): The error message to display.
        '''
        ctx = click.get_current_context()
        verbose = ctx.obj.get('verbose', 0)
        if verbose >= 1:
            Printing.print_warning(str(err))
        if verbose >= 2:
            import traceback
            Printing.print_formatted(traceback.format_exc())

    @staticmethod
    def print_info(message: str) -> None:
        '''
        Print info output.

        Args:
            message (str): The message to display.
        '''
        rich.print(f'[blue]{message}[/blue]')

    @staticmethod
    def print_items_in_columns(items: list[str], padding: int = 3) -> None:
        '''
        Prints the given list in equally spread columns.

        Args:
            items (list): The items to print.
            padding (int): The padding between the elements. (default: `3`)
        '''
        terminal_width = os.get_terminal_size().columns
        max_item_length = max(len(item) for item in items)
        col_width = max_item_length + padding
        num_cols = terminal_width // col_width

        for i, item in enumerate(items):
            end_char = '\n' if (i + 1) % num_cols == 0 else ' ' * padding
            print(f'{item:<{max_item_length}}', end=end_char)

        if len(items) % num_cols != 0:
            print()

    @staticmethod
    def print_success(message: str) -> None:
        '''
        Print success output.

        Args:
            message (str): The message to display.
        '''
        rich.print(f'[green]{message}[/green]')

    @staticmethod
    def print_table(
        columns: list[dict] = [],
        rows: list[list] = [[]],
        title: str = ''
    ) -> None:
        '''
        Print a table with the given columns and the given rows, cotaining
        columns.

        Args:
            columns (list): \
                The columns / header. A list with dicts, describing the \
                columns and their style.
            rows (list[list]): \
                The multidimensional list of rows. Each row is \
                a list itself, containing strings with the data \
                to display. The item count should be the same as \
                the columns / header count, of course!
        '''
        table = Table(title=title, box=box.SQUARE)

        for column in columns:
            table.add_column(**column)

        for row in rows:
            table.add_row(*row)  # type: ignore

        console = Console()
        console.print(table)

    @staticmethod
    def print_warning(message: str) -> None:
        '''
        Print warning output.

        Args:
            message (str): The message to display.
        '''
        rich.print(f'[yellow]{message}[/yellow]')
