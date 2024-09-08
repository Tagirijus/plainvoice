'''
IOService class

Handles certain user inputs and outputs.
'''

from plainvoice.model.config import Config
from plainvoice.model.document.document import Document
from plainvoice.view.printing import Printing

from datetime import datetime
from rich.prompt import Confirm


class IOFacade:
    '''
    The input output facade.
    '''

    @staticmethod
    def ask_yes_no(message: str) -> bool:
        '''
        Ask user simple yes/no question and get bool in return.

        Args:
            message (str): The message to ask.

        Returns:
            bool: Returns True if user replied positively.
        '''
        return Confirm.ask(message)

    @staticmethod
    def print(message: str, type: str = 'formatted') -> None:
        '''
        Prints a message with the level type.

        Args:
            message (str): \
                The message to print.
            type (str): \
                The type / level of output. Options are: \
                error, formatted (default and fallback), info \
                success, warning
        '''
        if type == 'error':
            Printing.print_error(message)
        elif type == 'info':
            Printing.print_info(message)
        elif type == 'success':
            Printing.print_success(message)
        elif type == 'warning':
            Printing.print_warning(message)
        else:
            Printing.print_formatted(message)

    @staticmethod
    def print_doc_calc(doc: Document, print_type: bool = False) -> None:
        '''
        Prints a single document calculation in a pretty way.

        Args:
            doc (Document): The document to print.
        '''
        due_date = doc.get_due_date(False)
        if isinstance(due_date, datetime):
            due_date = due_date.strftime(
                str(Config().get('date_output_format'))
            )
            due_date = f'[normal]{due_date}[/normal]'
        title = f'[white]{doc.get_name()}[/white]'
        total_with_vat = f'[green]{doc.get_total_with_vat(True)}[/green]'
        Printing.print_formatted(
            f'{due_date} {title}: {total_with_vat}'
        )

    @staticmethod
    def print_list(items: list[str], padding: int = 3) -> None:
        '''
        Prints the given list in equally spread columns.

        Args:
            items (list): The items to print.
            padding (int): The padding between the elements. (default: `3`)
        '''
        Printing.print_items_in_columns(items, padding)
