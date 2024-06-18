from datetime import datetime
from decimal import Decimal
from model.client import Client


class Invoice(object):
    def __init__(self):
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
