from datetime import datetime
from plainvoice.utils import date_utils


def test_datetime2str():
    # the datetime object should be in the format "%Y-%m-%d"
    # since the helper method is basically some kind of
    # wrapper method for datetime.strftime('%Y-%m-%d')
    tmp_date = datetime.strptime('2024-07-19', '%Y-%m-%d')
    assert date_utils.datetime2str(tmp_date) == '2024-07-19'
