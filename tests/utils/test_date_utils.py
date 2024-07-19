from datetime import datetime
from plainvoice.utils import date_utils


def test_datetime2str():
    tmp_date = datetime.strptime("2024-07-19", "%Y-%m-%d")
    assert date_utils.datetime2str(tmp_date) == "2024-07-19"


def test_datetime_from_dict_key():
    tmp_date_a = datetime.strptime("2024-07-19", "%Y-%m-%d")
    tmp_date_now = datetime.now()
    tmp_dict = {
        "test_date": "2024-07-19",
        "other_date": tmp_date_a
    }

    # fetching test_date from dict: convert from string
    tmp_date_b = date_utils.datetime_from_dict_key(tmp_dict, "test_date")
    assert tmp_date_a == tmp_date_b

    # fetching other_date from dict: simply get datetime
    tmp_date_c = date_utils.datetime_from_dict_key(tmp_dict, "other_date")
    assert tmp_date_a == tmp_date_c

    # getting now, when no key is found
    tmp_date_d = date_utils.datetime_from_dict_key(tmp_dict, "", "now")
    assert (
        tmp_date_now.strftime("%Y-%m-%d")
        == tmp_date_d.strftime("%Y-%m-%d")  # type: ignore
    )

    # getting None, due to no found key
    tmp_date_e = date_utils.datetime_from_dict_key(tmp_dict, "")
    assert tmp_date_e is None
