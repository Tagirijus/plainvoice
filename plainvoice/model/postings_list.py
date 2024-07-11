from decimal import Decimal
from plainvoice.model.base import Base
from plainvoice.model.posting import Posting
from plainvoice.utils import math_utils


class PostingsList(Base):
    """
    This class controlls the list for postings.
    """

    postings: list = []
    """
    The internal list for the postings.
    """

    def add_posting(
        self,
        title: str,
        detail: str,
        unit_price: str,
        quantity: str,
        vat: str = '0 %'
    ) -> None:
        """
        This method adds a Posting to the postings list.

        Args:
            title (str): \
                The title of the posting.
            detail (str): \
                The description / details of the posting.
            unit_price (str): \
                The unit price of the posting. Enter as a \
                string. It will be converted internally to \
                a Decimal object.
            quantity (str): \
                The quantity string. This is a string, which can \
                contain the unit as well. Internally there is some \
                kind of parser, which will be able to understand \
                the number and split it from the unit type.
            vat (str): \
                The vat string. Is a string which can include the \
                percentage sign for better readability in the YAML \
                file later. (default: `'0 %'`)
        """
        posting = Posting()
        posting.title = title
        posting.detail = detail
        posting.unit_price = Decimal(str(unit_price))
        posting.quantity = str(quantity)
        posting.vat = str(vat)
        self.postings.append(posting)

    def calc_total(self, net: bool = True) -> Decimal:
        """
        Calculate and return the total summarized of all postings.

        Args:
            net (bool): If True the total is the net value. (default: `True`)

        Returns:
            Decimal: The total amount as a Decimal.
        """
        out = Decimal('0')
        for posting in self.postings:
            out += posting.calc_total(net)
        return math_utils.round2(out)

    def calc_vat(self) -> Decimal:
        """
        Calculates and returns just the vat amount from the total
        of all postings.

        Returns:
            Decimal: The vat amount as a Decimal.
        """
        total_gross = self.calc_total(False)
        total_net = self.calc_total(True)
        return math_utils.round2(total_net - total_gross)

    def from_dicts(self, values: list = []) -> None:
        """
        Setting the class attributes from a given dict.

        Args:
            values (list): \
                The list containing Posting dicts to use \
                for filling the attributes. (default: `{}`)
        """
        for posting in values:
            self.add_posting(
                posting.get('title', ''),
                posting.get('detail', ''),
                posting.get('unit_price', ''),
                posting.get('quantity', ''),
                posting.get('vat', '')
            )

    def has_vat(self):
        return self.calc_total() != self.calc_total(False)

    def to_dicts(self) -> list[dict]:
        """
        Convert all the Posting objects inside the list
        to a dict and return the list.

        Returns:
            list: The list containing the dicts of the postings.
        """
        out = []
        for posting in self.postings:
            out.append(posting.to_dict())
        return out
