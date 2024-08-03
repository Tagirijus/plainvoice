from plainvoice.model.posting.posting import Posting


def test_posting_defaults():
    # create a posting instance
    posting = Posting('title')

    # check, if the defaults where set correctly
    # and also at the same time if the getters
    # are working correctly
    assert posting.get_fixed('title', True) == 'title'
    assert posting.get_fixed('detail', True) == ''
    assert posting.get_fixed('unit_price', True) == '1.00 €'
    assert posting.get_fixed('quantity', True) == '1'
    assert posting.get_fixed('vat', True) == '0 %'


def test_math_operations():
    # create a posting instance
    posting = Posting('math posting')

    # fill some variables and check them as well with getters
    posting.set_fixed('unit_price', '5.00 €', True)
    assert posting.get_fixed('unit_price', True) == '5.00 €'
    posting.set_fixed('quantity', '3:00 min', True)
    assert posting.get_fixed('quantity', True) == '3:00 min'
    posting.set_fixed('vat', '10 %', True)
    assert posting.get_fixed('vat', True) == '10 %'

    # check if the internal math also works
    assert posting.get_total(True) == '15.00 €'
    assert posting.get_vat(True) == '1.50 €'
