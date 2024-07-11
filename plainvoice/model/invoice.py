from datetime import datetime, timedelta
from decimal import Decimal
from plainvoice.model.base import Base
from plainvoice.model.postings_list import PostingsList
from plainvoice.model.config import Config
from plainvoice.utils import date_utils


class Invoice(Base):
    """
    The invoice class, which can basically also be a quote.
    """

    code: str
    """
    The invoice or quote code.
    """

    client_id: str
    """
    The id of the client, which also will be used for linking
    a client to the invoice internally, if needed.
    """

    date_invoiced: datetime
    """
    The datetime object for the invoice date.
    """

    date_due: datetime
    """
    The datetime object for the due date.
    """

    date_paid: datetime
    """
    The datetime object for the paid date.
    """

    receiver: str
    """
    A whole receiver string, which will be generated from the
    client object. For better readability in the YAML file
    I decided to use this as a whole multiline string. Also
    foreign countries have different kinds of formatting here.
    I want to be able to address this easily.
    """

    data: dict
    """
    The internal objects dict, which can store all needed additional
    data.
    """

    currency: str
    """
    The currency as a string symbol.
    """

    postings: PostingsList
    """
    The list with all the Posting objects, yet inside the PostingsList
    object, which can controll it and output all the postings as
    dicts inside a list.
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
        self.postings.add_posting(
            title,
            detail,
            unit_price,
            quantity,
            vat
        )

    def calc_total(self, net: bool = True) -> Decimal:
        """
        Calculate and return the total summarized of all postings.

        Args:
            net (bool): If True the total is the net value. (default: `True`)

        Returns:
            Decimal: The total amount as a Decimal.
        """
        return self.postings.calc_total()

    def calc_vat(self) -> Decimal:
        """
        Calculates and returns just the vat amount from the total
        of all postings.

        Returns:
            Decimal: The vat amount as a Decimal.
        """
        return self.postings.calc_vat()

    def from_dict(self, values: dict = {}) -> None:
        """
        Setting the class attributes from a given dict.

        Args:
            values (dict): \
                The dict to use for filling the attributes. (default: `{}`)
        """
        self.code = values.get('code', '')
        self.client_id = values.get('client_id', '')

        self.date_invoiced = date_utils.datetime_from_dict_key(
            values,
            'date_invoiced',
            'now'
        )
        self.date_due = date_utils.datetime_from_dict_key(
            values,
            'date_due'
        )
        if self.date_due is None and self.date_invoiced is not None:
            self.date_due = (
                self.date_invoiced + timedelta(
                    days=Config().default_due_days
                )
            )
        self.date_paid = date_utils.datetime_from_dict_key(values, 'date_paid')

        self.receiver = values.get('receiver', '')

        self.data = values.get('data', {})

        self.currency = values.get('currency', '€')
        self.postings.from_dicts(values.get('postings', []))

    def get_days_till_due(self) -> int:
        """
        Caclulates the days difference between the invoiced date
        and the due date. Thsi method can be used inside the jinja2
        template like 'invoice.get_days_till_due()'.

        Returns:
            int: Returns the days as an integer or -1 on error.
        """
        if (
            isinstance(self.date_due, datetime)
            and isinstance(self.date_invoiced, datetime)
        ):
            difference = self.date_due - self.date_invoiced
            return difference.days
        else:
            return -1

    def has_vat(self):
        return self.postings.has_vat()
