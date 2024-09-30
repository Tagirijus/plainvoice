'''
Input class

This class is similar to the Output class, yet for input. See
the Output doc for further detail. TL;DR: the idea is that in
case of a replacement for certain modules, I only want to have
this class adjusted and not the IOFacade class.
'''

from datetime import datetime
from rich.prompt import Confirm
from rich.prompt import Prompt


class Input:
    '''
    Simple input methods.
    '''

    @staticmethod
    def ask(message: str) -> bool:
        '''
        Ask user simple yes/no question and get bool in return.

        Args:
            message (str): The message to ask.

        Returns:
            bool: Returns True if user replied positively.
        '''
        return Confirm.ask(message)

    @staticmethod
    def ask_date() -> str:
        '''
        Ask for a date string, while suggesting the today
        date already.

        Returns:
            str: Returns the date string.
        '''
        now = datetime.now().strftime('%Y-%m-%d')
        return Prompt.ask('Enter date', default=now)
