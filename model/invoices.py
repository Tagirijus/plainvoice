from datetime import datetime, timedelta
from decimal import Decimal
from model.base import Base
from model.clients import Clients
from model.postings import Postings
from model.settings import Settings
from utils import math_utils


class Invoices(Base):
    """
    The invoice class, which can basically also be a quote.
    """

    title: str
    """
    The title of the whole invoice or quote.
    """

    code: str
    """
    The invoice or quote code.
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

    delivery: str
    """
    The text for the delivery field. I did not choose a datetime
    here, since I want to be able (at least in my invoices) to
    also define a range here like 'Jan 2024 - Mar 2024' or so.
    """

    client_id: str
    """
    The id of the client, which also will be used for linking
    a client to the invoice internalle, if needed.
    """

    receiver: str
    """
    A whole receiver string, which will be generated from the
    client object. For better readability in the YAML file
    I decided to use this as a whole multiline string. Also
    foreign countries have different kinds of formatting here.
    I want to be able to address this easily.
    """

    comment: str
    """
    A possible comment / additional text for the invoice.
    """

    currency: str
    """
    The currency as a string symbol.
    """

    additional: dict
    """
    Additional values to be used on the invoice. This is my flexible
    approach for the user to have all kinds of additional fields during
    the rendering process of the jinja2 template. E.g. if you want to
    have a clients vat number as well on the invoice, you could add
    it in this variable as "client_vat_id" or so. Later you can access
    this variable in the jinja2 template with
    invoice.get_additional('client_vat_id').
    """

    postings: list
    """
    The list containing all the Posting objects.
    """

    def __init__(self):
        super(Invoices, self).__init__()
        self.FOLDER = 'invoices/'
        self.EXTENSION = 'yaml'

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
        P = Postings()
        P.title = title
        P.detail = detail
        P.unit_price = Decimal(str(unit_price))
        P.quantity = str(quantity)
        P.vat = str(vat)
        self.postings.append(P)

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

    def get_as_dict(self) -> dict:
        """
        This output will also have influence on the sorting
        of the YAML keys in the YAML file later! So I'd like
        to stick with this sorting for better readability.

        In case somebody knows how to better sort it for the
        final file, feel free to teach me!

        Returns:
            dict: The class attributes as a dict.
        """
        return {
            # clients will be stored as plaintext and
            # just soft-linked via client_id if needed later
            'title': self.title,
            'code': self.code,

            'date_invoiced': self.datetime2str(self.date_invoiced),
            'date_due': self.datetime2str(self.date_due),
            'date_paid': self.datetime2str(self.date_paid),

            'delivery': self.delivery,

            'client_id': self.client_id,
            'receiver': self.receiver,

            'comment': self.comment,

            'currency': self.currency,

            'additional': self.additional,

            'postings': [p.get_as_dict() for p in self.postings],

            # not sure at the moment, if I want the calculations
            # in the YAML, since it crowds the human readable
            # YAML a bit and makes the plaintext principle a
            # bit off.
            # 'total': {
            #     'net': float(self.calc_total(False)),
            #     'gross': float(self.calc_total(True)),
            #     'vat': float(self.calc_vat())
            # }
        }

    def get_additional(self, key: str) -> object:
        """
        Returns an additional value, if it is set. The invoices
        additional attribut is for the user to save almost every
        kind of additinal data into. This then later can be accessed
        in the jinja2 template by 'invoice.get_additional(KEY)'.
        If it does not exist, the method simply will return None.

        Args:
            key (str): The key name.

        Returns:
            object: \
                Will be None, if the key does not exist, otherwise
                it will be the data type, the user used in the
                YAML file.
        """
        return self.additional.get(key, None)

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

    def generate_receiver(self) -> None:
        """
        This method fills the internal receiver attribute
        from the client data. I am using this for better
        readability in the YAML file after saving an
        invoice / quote.
        """
        C = Clients()
        if C.load_from_yaml_file(self.client_id):
            self.receiver = C.generate_receiver()

    def has_vat(self):
        return self.calc_total() != self.calc_total(False)

    def set_from_dict(self, values: dict = {}) -> None:
        """
        Setting the class attributes from a given dict.

        Args:
            values (dict): \
                The dict to use for filling the attributes. (default: `{}`)
        """
        self.title = values.get('title', '')
        self.code = values.get('code', '')

        self.date_invoiced = self.datetime_from_dict_key(
            values,
            'date_invoiced',
            'now'
        )
        self.date_due = self.datetime_from_dict_key(
            values,
            'date_due'
        )
        if self.date_due is None and self.date_invoiced is not None:
            self.date_due = (
                self.date_invoiced + timedelta(
                    days=Settings().DEFAULT_DUE_DAYS
                )
            )
        self.date_paid = self.datetime_from_dict_key(values, 'date_paid')

        self.delivery = values.get('delivery', '')

        self.client_id = values.get('client_id', '')
        self.receiver = values.get('receiver', '')

        self.comment = values.get('comment', '')

        self.currency = values.get('currency', '€')

        self.additional = values.get('additional', {})

        self.postings = []
        for posting in values.get('postings', []):
            P = Postings()
            P.set_from_dict(posting)
            self.postings.append(P)
