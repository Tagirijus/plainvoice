'''
Posting Class

This class will represent a single posting on an invoice
or a quote. It will be able to do math operations for
the posting as well.
'''


from plainvoice.model.config import Config
from plainvoice.model.document.document_hardcode_type import \
    DocumentHardcodeType
from plainvoice.model.quantity.percentage import Percentage
from plainvoice.model.quantity.price import Price
from plainvoice.model.quantity.quantity import Quantity


class Posting(DocumentHardcodeType):
    '''
    This class represents a posting on an invoice or quote.
    '''

    def __init__(
        self,
        title: str = '',
        detail: str = '',
        unit_price: str = '1.00 €',
        quantity: str = '1',
        vat: str = '0 %'
    ):
        '''
        This class is for clients data. It is supposed to be able
        to link to certain documents for the clients.

        Args:
            title (str): \
                The name of the posting.
        '''
        super().__init__(
            title,
            'posting',
            '',
            Config().posting_folder
        )

        self.default_fields = {
            'title': ('str', title),
            'detail': ('str', detail),
            'unit_price': ('Price', Price(unit_price)),
            'quantity': ('Quantity', Quantity(quantity)),
            'vat': ('Percentage', Percentage(vat))
        }

        self.code = self.get_next_code()
        self.name = title
        self.load_from_name(self.name)

    def __str__(self) -> str:
        '''
        Represent this class as a string.

        Returns:
            srt: The readable string.
        '''
        quantity = self.data_prebuilt['quantity']
        title = self.data_prebuilt['title']
        unit_price = self.data_prebuilt['unit_price']
        total = self.get_total()
        vat = self.get_vat()
        return (
            f'{quantity} - {title} [{unit_price}]: {total + vat} (VAT: {vat})'
        )

    def get_total(self) -> Price:
        '''
        Calculate and return the total.

        Returns:
            Price: Returns the total as a Price object.
        '''
        return (
            self.data_prebuilt['unit_price'] * self.data_prebuilt['quantity']
        )

    def get_vat(self) -> Price:
        '''
        Calculate the vat from the total and return it.

        Returns:
            Price: Returns the vat of the total as a Price object.
        '''
        return (
            self.get_total() * self.data_prebuilt['vat']
        )
