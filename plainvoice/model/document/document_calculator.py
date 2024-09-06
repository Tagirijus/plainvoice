'''
DocumentCalculator class

This class is for processing and calculating the due, overdue
etc. data for a list of Document objects.

I created it to have a more sane overview about variables
I wanted to prepare for the list output in the IOFacade class.
Also maybe this class could get importanrt later on, when
more such calculations might get important and have to be
extended.
'''

from plainvoice.model.document.document import Document


class DocumentCalculator:
    '''
    This class is for processing and calculating the due, overdue
    etc. data for a list of Document objects.
    '''

    def __init__(self, due_docs: list[Document]):
        '''
        This class is for processing and calculating the due, overdue
        etc. data for a list of Document objects.
        '''

        self.due_docs: list[Document] = due_docs
        '''
        The raw list with Documents which are due and to be
        processed by this class.
        '''
