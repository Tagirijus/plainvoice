from plainvoice.model.data.data_model import DataModel
from plainvoice.model.posting.posting import Posting
from plainvoice.model.quantity.price import Price

from typing import Any


class PostingsList(DataModel):
    '''
    This class controlls the list for postings.
    '''

    def __init__(self):
        '''
        This class controlls the list for postings.
        '''
        super().__init__()
        self._init_fixed_fields()

    def add_posting(
        self,
        title: str = '',
        detail: str = '',
        unit_price: str = '1.00 €',
        quantity: str = '1',
        vat: str = '0 %'
    ) -> None:
        '''
        This method adds a Posting to the postings list. Use
        only readable values for adding it.

        Args:
            title (str): \
                The title of the posting. (default: `''`)
            detail (str): \
                The description / details of the posting. (default: `''`)
            unit_price (str): \
                The unit price of the posting. (default: `'1.00 €'`)
            quantity (str): \
                The quantity for the posting. (default: `'1'`)
            vat (str): \
                The vat for the posting. (default: `'0 %'`)
        '''
        posting = Posting(title)
        posting.set_fixed('detail', detail, True)
        posting.set_fixed('unit_price', unit_price, True)
        posting.set_fixed('quantity', quantity, True)
        posting.set_fixed('vat', vat, True)
        self.get_fixed('postings', False).append(posting)

    def get_total(self, readable: bool = False) -> Price | Any:
        '''
        Calculate and return the total summarized of all postings.

        Args:
            readable (bool): Convert the output to a readable.

        Returns:
            Price | Any: The total amount as a Price or Any.
        '''
        output = 0
        for posting in self.get_fixed('postings', False):
            output = posting.get_total(False) + output
        if readable:
            output = \
                self.fixed_field_conversion_manager.convert_value_to_readable(
                    output,
                    'Price'
                )
        return output

    def get_posting(self, id_or_title: int | str) -> Posting:
        '''
        Get a posting by its index in the internal list or
        by its title.

        Args:
            id_or_title (int | str): The index of the posting or its title.

        Returns:
            Posting: Returns the Posting object.
        '''
        if (
            isinstance(id_or_title, int)
            and id_or_title < len(self.get_fixed('postings', False))
        ):
            return self.get_fixed('postings', False)[id_or_title]
        else:
            return self.get_posting_by_title(str(id_or_title))

    def get_posting_by_title(self, title: str) -> Posting:
        '''
        Get a posting by its title. Use the first occurence of
        the list, though.

        Args:
            title (str): The Posting title.

        Returns:
            Posting: Returns Posting with the mentioned title.
        '''
        output = Posting()
        for posting in self.get_fixed('postings', False):
            if posting.get_fixed('title', True) == title:
                output = posting
                break
        return output

    def get_vat(self, readable: bool = False) -> Price | Any:
        '''
        Calculates and returns just the vat amount from the total
        of all postings.

        Args:
            readable (bool): Convert the output to a readable.

        Returns:
            Price | Any: The vat amount as a Price or Any.
        '''
        output = 0
        for posting in self.get_fixed('postings', False):
            output = posting.get_vat(False) + output
        if readable:
            output = \
                self.fixed_field_conversion_manager.convert_value_to_readable(
                    output,
                    'Price'
                )
        return output

    def has_vat(self):
        return self.get_vat() != 0

    def _init_fixed_fields(self) -> None:
        '''
        Initialize the fixed fields for this special DataModel child.
        '''
        self.define_fixed_field_type(
            'Price',
            lambda x: Price(str(x)),
            str
        )
        self.define_fixed_field_type(
            'Postings',
            lambda x: (
                [Posting().instance_from_dict(y) for y in x]
            ),
            lambda x: x.to_dict(True)
        )

        self.add_field_descriptor('postings', 'Postings', [])
