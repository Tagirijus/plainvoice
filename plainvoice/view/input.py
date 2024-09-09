'''
Input class

This class is similar to the Output class, yet for input. See
the Output doc for further detail. TL;DR: the idea is that in
case of a replacement for certain modules, I only want to have
this class adjusted and not the IOFacade class.
'''

from rich.prompt import Confirm


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
