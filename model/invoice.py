from datetime import datetime
from decimal import Decimal
from model.base import Base
from model.client import Client
from model.posting import Posting


class Invoice(Base):
    def __init__(self):
        super(Invoice, self).__init__()

    def folder(self, filename):
        return 'invoices/' + filename

    def set_from_dict(self, values={}):
        self.client_id = values.get('client_id', '')
        self.receiver = values.get('receiver', '')

        self.date = values.get('date', datetime.now())
        self.delivery = values.get('delivery', '')

        self.title = values.get('title', '')
        self.code = values.get('code', '')

        self.comment = values.get('comment', '')
        self.due_days = values.get('due_days', '')
        self.paid_date = values.get('paid_date', None)

        self.wage = Decimal(str(values.get('wage', '40')))
        self.currency = values.get('currency', '€')
        self.round_price = values.get('round_price', False)

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
            'client_id': self.client_id,
            'receiver': self.receiver,

            'date': self.date.strftime('%Y-%m-%d'),
            'delivery': self.delivery,

            'title': self.title,
            'code': self.code,

            'comment': self.comment,
            'due_days': self.due_days,
            'paid_date': self.paid_date.strftime('%Y-%m-%d') if isinstance(self.paid_date, datetime) else None,

            'wage': float(self.wage),
            'currency': self.currency,
            'round_price': self.round_price,

            'postings': [p.get_as_dict() for p in self.postings],
        }

    def generate_receiver(self):
        C = Client()
        if C.load(self.client_id):
            self.receiver = C.generate_receiver()
