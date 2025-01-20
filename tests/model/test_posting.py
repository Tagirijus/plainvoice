from plainvoice.model.quantity.price import Price
from plainvoice.model.posting.posting import Posting


def test_converting_posting():
    # create a posting instance with some values
    posting = Posting('title')
    # also the argument of set_fixed() "readable"
    # should be "True" by default
    posting.set_fixed('detail', 'just detail text')
    posting.set_fixed('unit_price', '3.00 €')
    posting.set_fixed('quantity', '1.5 pieces')
    posting.set_fixed('vat', '10 %')
    posting.set_fixed('notes', 'notes here')

    # generate the output dict manually
    output_manually = {
        'title': 'title',
        'detail': 'just detail text',
        'unit_price': '3.00 €',
        'quantity': '1.5 pieces',
        'vat': '10 %',
        'notes': 'notes here',
    }

    # this should be the same, when exported to dict;
    # for the fixed fields, though
    assert posting._to_dict_fixed(True) == output_manually

    # no I try to load this dict into a new Posting instance
    posting_new = Posting()
    posting_new.from_dict(output_manually)

    # check if all fields are correctly "loaded"
    assert posting_new.get_fixed('title', True) == 'title'
    assert posting_new.get_fixed('detail', True) == 'just detail text'
    assert posting_new.get_fixed('unit_price', True) == '3.00 €'
    assert posting_new.get_fixed('quantity', True) == '1.5 pieces'
    assert posting_new.get_fixed('vat', True) == '10 %'

    # and the string representation should also be checked
    assert str(posting_new) == '1.5 pieces, title: 4.95 € (0.45 € VAT)'


def test_is_zero():
    # test if the is_zero() method works correctly
    posting = Posting('title')
    assert posting.is_zero() is True


def test_posting_defaults():
    # create a posting instance
    posting = Posting('title')

    # check, if the defaults where set correctly
    # and also at the same time if the getters
    # are working correctly
    assert posting.get_fixed('title', True) == 'title'
    assert posting.get_fixed('detail', True) == ''
    assert posting.get_fixed('unit_price', True) == '0.00 €'
    assert posting.get_fixed('unit_price', False) == Price('0.00 €')
    assert posting.get_fixed('quantity', True) == '0'
    assert posting.get_fixed('vat', True) == '0 %'

    # also check what happens if I convert a Posting
    # from dict, while the dict is empty
    posting_2 = Posting().instance_from_dict({})
    assert posting_2.get_fixed('title', True) == ''
    assert posting_2.get_fixed('detail', True) == ''
    assert posting_2.get_fixed('unit_price', True) == '0.00 €'
    assert posting_2.get_fixed('unit_price', False) == Price('0.00 €')
    assert posting_2.get_fixed('quantity', True) == '0'
    assert posting_2.get_fixed('vat', True) == '0 %'


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

    # also check what happens if I convert a Posting
    # from dict and then do math on it
    posting_2 = Posting().instance_from_dict({})
    assert posting_2.get_total(True) == '0.00 €'


def test_vat():
    # create a posting instance
    posting = Posting('math posting')

    # default should not have vat
    assert posting.has_vat() is False

    # yet now I set a vat value
    posting.set_fixed('vat', '19 %', True)
    assert posting.has_vat() is True
