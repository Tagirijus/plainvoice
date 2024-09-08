'''
DocumentCalculator class

This class is for calculating with a list of Document objects.

I created it to have a more sane overview about variables
I wanted to prepare for the list output in the IOFacade class.
Also maybe this class could get importanrt later on, when
more such calculations might get important and have to be
extended.
'''

from plainvoice.model.document.document import Document
from plainvoice.model.quantity.price import Price


class DocumentCalculator:
    '''
    This class is for calculating with a list of Document objects.
    '''

    def __init__(self, docs: list[Document]):
        '''
        This class is for calculating with a list of Document objects.
        '''

        self.docs: list[Document] = docs
        '''
        The raw list with Documents which are being calculated.
        '''

    def get_total(self, readable: bool = False) -> Price | str:
        '''
        Get the total summarized for all documents.

        Args:
            readable (bool): Convert the output to a readable.

        Returns:
            Price | str: The total amount as a Price or Any.
        '''
        return self._get_total_vat_and_both('total', readable)

    def _get_total_vat_and_both(
        self,
        what: str = 'total',
        readable: bool = False
    ) -> Price | str:
        '''
        Get the total for all internal included Document objects
        as either a Price object or a readbale string.

        Args:
            what (str): "total", "vat" or "total_with_vat"
            readable (bool): Convert the output to a readable.

        Returns:
            Price | str: Returns the total as a Price object or string.
        '''
        total = Price()
        for doc in self.docs:
            docs_total = doc._get_total_vat_and_both(what, False)
            if isinstance(docs_total, Price):
                total = total + docs_total
                # just set the last fetched currency as the new currency.
                # the probability is high that only one currency will
                # be used inside one document anyway.
                total.set_currency(docs_total.get_currency())
        if readable:
            return str(total)
        else:
            return total

    def get_total_with_vat(self, readable: bool = False) -> Price | str:
        '''
        Get the total with vat summarized for all docs.

        Args:
            readable (bool): Convert the output to a readable.

        Returns:
            Price | str: The total amount as a Price or Any.
        '''
        return self._get_total_vat_and_both('total_with_vat', readable)

    def get_vat(self, readable: bool = False) -> Price | str:
        '''
        Get the vat summarized for all docs.

        Args:
            readable (bool): Convert the output to a readable.

        Returns:
            Price | str: The total amount as a Price or Any.
        '''
        return self._get_total_vat_and_both('vat', readable)
