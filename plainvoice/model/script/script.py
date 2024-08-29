'''
Script class

This class will hold (get on init) a string containing Python script.
It will be able to execute this script with certain parameter, which
can be used inside those scripts then. E.g. a document.
'''

from plainvoice.model.config import Config
from plainvoice.model.data.data_model import DataModel


class Script:
    '''
    The class for the script extension of plainvoice.
    '''

    def __init__(self, python_string: str):
        '''
        The script class contains just the Python executable string
        and will be able to execute it.

        Args:
            python_string (str): A string containing Python code.
        '''
        self.python_string = python_string

    def run(self, data: DataModel, user: DataModel) -> bool:
        '''
        Runs the python code in the python_string attribute. Also
        this method gets arguments, which then will be passed to
        the script itself.

        Args:
            data (DataModel): \
                The DataModel object, which will be accessible \
                in the script to run as "data".
            user (DataModel): \
                The user DataModel to be used in the scripts.

        Returns:
            bool: \
                Returns True if the script ran successfully. \
                At least regarding the main program.
        '''
        try:
            config = Config()
            exec(self.python_string)
            return True
        except Exception:
            return False
