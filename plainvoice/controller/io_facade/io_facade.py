'''
IOFacade class

With this class I have some of the "wrapper" layer for the output
and input. It might seem similar to the Printing class. Yet the
Printing class is the one mainly holding and using other modules.
In case I would like or need to reaplce such modules, I want to
do it in one class only. That's why this class mainly USES the
Printing class' methods.
'''

from plainvoice.model.config import Config
from plainvoice.model.document.document import Document
from plainvoice.model.document.document_calculator \
    import DocumentCalculator
from plainvoice.view.input import Input
from plainvoice.view.printing import Printing

from datetime import datetime


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
        return Input.ask(message)

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
    def print_doc_calc(doc: Document) -> None:
        '''
        Prints a single document calculation in a pretty way.

        Args:
            doc (Document): The document to print.
        '''
        issued_date = doc.get_issued_date(False)
        if isinstance(issued_date, datetime):
            issued_date = issued_date.strftime(
                str(Config().get('date_output_format'))
            )
            issued_date = f'[normal]{issued_date}[/normal]'
        due_date = doc.get_due_date(False)
        if isinstance(due_date, datetime):
            due_date = due_date.strftime(
                str(Config().get('date_output_format'))
            )
            due_date = f'[normal][yellow]{due_date}[/yellow][/normal]'
        title = f'[white]{doc.get_name()}[/white]'
        total_with_vat = f'[green]{doc.get_total_with_vat(True)}[/green]'
        Printing.print_formatted(
            f'{issued_date} -> {due_date} {title}: {total_with_vat}'
        )

    @staticmethod
    def print_doc_due_table(
        docs: list[Document],
        title: str = '',
        print_type: bool = False
    ) -> None:
        '''
        Prints a single document calculation in a pretty way.

        Args:
            doc (Document): The document to print.
            title (str): The title of the table.
            print_type (bool): Print the type as well.
        '''
        header = [
            {
                'header': 'Date',
                'style': 'cyan'
            },
            {
                'header': 'Due date',
                'style': 'yellow'
            },
            {
                'header': 'Days till due'
            },
            {
                'header': 'Title'
            },
            {
                'header': 'Total',
                'style': 'green'
            },
        ]
        rows = []
        doc_calc = DocumentCalculator(docs)
        for doc in docs:
            issued_date = doc.get_issued_date(False)
            if isinstance(issued_date, datetime):
                issued_date = issued_date.strftime(
                    str(Config().get('date_output_format'))
                )
            due_date = doc.get_due_date(False)
            if isinstance(due_date, datetime):
                due_date = due_date.strftime(
                    str(Config().get('date_output_format'))
                )
            due_days = doc.days_till_due_date()
            if isinstance(due_days, int) and due_days > 0:
                due_days = f'[blue]{due_days}[/blue]'
            else:
                due_days = f'[red]{due_days}[/red]'
            doc_title = doc.get_name()
            if print_type:
                doc_title = f'{doc.get_document_typename()}: {doc_title}'
            rows.append([
                    issued_date,
                    due_date,
                    due_days,
                    doc_title,
                    doc.get_total_with_vat(True)
            ])
        rows.append([
            '---',
            '---',
            '---',
            '---',
            '---'
        ])
        rows.append([
            '',
            '',
            '',
            'Total',
            doc_calc.get_total_with_vat(True)
        ])
        Printing.print_table(header, rows, title)

    @staticmethod
    def print_list(items: list[str], padding: int = 3) -> None:
        '''
        Prints the given list in equally spread columns.

        Args:
            items (list): The items to print.
            padding (int): The padding between the elements. (default: `3`)
        '''
        Printing.print_items_in_columns(items, padding)
