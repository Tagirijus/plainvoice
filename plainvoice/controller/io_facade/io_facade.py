'''
IOService class

Handles certain user inputs and outputs.
'''

from plainvoice.model.document.document_calculator import \
    DocumentCalculator
from plainvoice.view.printing import Printing
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
    def print_due_list(doc_due_calculator: DocumentCalculator) -> None:
        '''
        Prints the due documents in a pretty way.

        Args:
            docs (list): The list containing the due document objects.
        '''
        # TODO / WIP !
        print(doc_due_calculator)

    @staticmethod
    def print_list(items: list[str], padding: int = 3) -> None:
        '''
        Prints the given list in equally spread columns.

        Args:
            items (list): The items to print.
            padding (int): The padding between the elements. (default: `3`)
        '''
        Printing.print_items_in_columns(items, padding)
