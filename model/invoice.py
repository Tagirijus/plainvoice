from datetime import datetime, timedelta
from decimal import Decimal
from model.base import Base
from model.client import Client
from model.posting import Posting
from model.settings import Settings
from utils import math_utils


class Invoice(Base):
    def __init__(self):
        super(Invoice, self).__init__()

    def folder(self, filename):
        return 'invoices/' + filename

    def set_from_dict(self, values={}):
        self.title = values.get('title', '')
        self.code = values.get('code', '')

        self.date_invoiced = self.load_datetime(values, 'date_invoiced', 'now')
        self.date_due = self.load_datetime(values, 'date_due')
        if self.date_due is None and not self.date_invoiced is None:
            self.date_due = self.date_invoiced + timedelta(days=Settings().DUE_DAYS)
        self.date_paid = self.load_datetime(values, 'date_paid')

        self.delivery = values.get('delivery', '')

        self.client_id = values.get('client_id', '')
        self.receiver = values.get('receiver', '')

        self.comment = values.get('comment', '')

        self.currency = values.get('currency', '€')
        self.round_price = values.get('round_price', False)

        self.additional = values.get('additional', {})

        self.postings = []
        for posting in values.get('postings', []):
            P = Posting()
            P.set_from_dict(posting)
            self.postings.append(P)

    def get_as_dict(self):
        """
        This output will also have influence on the sorting
        of the YAML keys in the YAML file later!
        """
        return {
            # clients will be stored as plaintext and
            # just soft-linked via client_id if neededlater
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
            'round_price': self.round_price,

            'additional': self.additional,

            'postings': [p.get_as_dict() for p in self.postings],

            # not sure at the moment, if I want the calculations
            # in the YAML, since it crowds the human readable
            # YAML a bit and makes the plaintext principle a
            # bit off.
            # 'total': {
            #     'net': float(self.calc_total(True)),
            #     'gross': float(self.calc_total(False)),
            #     'vat': float(self.calc_vat())
            # }
        }

    def generate_receiver(self):
        C = Client()
        if C.load(self.client_id):
            self.receiver = C.generate_receiver()

    def add_posting(self, title, detail, unit_price, amount, vat=0):
        P = Posting()
        P.title = title
        P.detail = detail
        P.unit_price = Decimal(str(unit_price))
        P.amount = str(amount)
        P.vat = str(vat)
        self.postings.append(P)

    def calc_total(self, net=True):
        out = Decimal('0')
        for posting in self.postings:
            out += posting.calc_total(net)
        return math_utils.round2(out)

    def calc_vat(self):
        total_gross = self.calc_total(False)
        total_net = self.calc_total(True)
        return math_utils.round2(total_net - total_gross)

    def has_vat(self):
        return self.calc_total() != self.calc_total(False)

    def get_days_till_due(self):
        if isinstance(self.date_due, datetime) and isinstance(self.date_invoiced, datetime):
            difference = self.date_due - self.date_invoiced
            return difference.days
        else:
            return False

    def get_additional(self, key):
        return self.additional.get(key, None)
