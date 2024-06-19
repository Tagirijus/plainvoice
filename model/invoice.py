from datetime import datetime
from decimal import Decimal
from model.client import Client
from model.posting import Posting


class Invoice(object):
    def __init__(self):
        # basically set the defaults, due to the empty
        # dict, which is given as a parameter
        self.set_from_dict({})


        self.client = Client()

        self.title = ''
        self.code = ''

        self.comment = ''
        self.date = datetime.now()
        self.delivery = ''
        self.due_days = 14
        self.paid_date = None

        self.wage = Decimal()
        self.currency = '€'
        self.round_price = False

        self.postings = []

    def set_from_dict(self, values):
        C = Client()
        self.client = C.set_from_dict(values.get('client', {}))

        self.title = values.get('title', '')
        self.code = values.get('code', '')

        self.comment = values.get('comment', '')
        self.date = values.get('date', '')
        self.delivery = values.get('delivery', '')
        self.due_days = values.get('due_days', '')
        self.paid_date = values.get('paid_date', '')

        self.wage = Decimal(values.get('wage', '40'))
        self.currency = values.get('currency', '€')
        self.round_price = values.get('round_price', '')

        self.postings = []
        for posting in values.get('postings', []):
            P = Posting()
            P.set_from_dict(posting)
            self.postings.append(P)

    def get_as_dict(self):
        postings = [p.get_as_dict() for p in self.postings]
        return {
            'client': self.client.get_as_dict(),

            'title': self.title,
            'code': self.code,

            'comment': self.comment,
            'date': self.date,
            'delivery': self.delivery,
            'due_days': self.due_days,
            'paid_date': self.paid_date,

            'wage': self.wage,
            'currency': self.currency,
            'round_price': self.round_price,

            'postings': postings,
        }
