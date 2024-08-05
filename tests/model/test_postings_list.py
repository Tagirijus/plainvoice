from plainvoice.model.posting.postings_list import PostingsList


def test_convert_postings_list():
    # create an instance
    postings_list = PostingsList()

    # create test dict, which could be data loaded from
    # a YAML, for example
    load_data = {
        'visible': True,
        'postings': [
            {
                'title': 'item a',
                'detail': '',
                'unit_price': '3.00 €',
                'quantity': '2',
                'vat': '0 %'
            },
            {
                'title': 'item b',
                'detail': 'the second item',
                'unit_price': '2.00 €',
                'quantity': '5',
                'vat': '10 %'
            }
        ]
    }

    # load it to the instance
    postings_list.from_dict(load_data)

    # check just a few values and also the postings getter at the same time
    assert postings_list.get_posting(0).get_fixed('title', True) == \
        'item a'
    assert postings_list.get_posting(0).get_fixed('unit_price', True) == \
        '3.00 €'
    assert postings_list.get_posting('item b').get_fixed('detail', True) == \
        'the second item'
    assert postings_list.get_posting('item b').get_fixed('vat', True) == \
        '10 %'


def test_math_operations():
    # setting up a list with some postings
    postings_list = PostingsList()

    # initially it should have no vat
    assert postings_list.has_vat() is False

    postings_list.add_posting(
        'Item a',
        'Just a test item: a.',
        '1.50 €',
        '10:00 min',
        '0 %'
    )
    postings_list.add_posting(
        'Item b',
        'Just a test item: b.',
        '5.00 €',
        '2.5 min',
        '5 %'
    )
    postings_list.add_posting(
        'Item c',
        'just a test item: c.',
        '2.00 €',
        '3:30 min',
        '10 %'
    )

    # now check if the total is correct;
    # it should be:
    #    10 * 1.50€  (15€)
    #  + 2.5 * 5€   (12.50€)
    #  + 3.5 * 2€   (7€)
    #  = 34.50 €
    assert postings_list.get_total(True) == '34.50 €'

    # the vat should be:
    #    12.50€ * 5 % (0.625€, will be rounded to 0.63€)
    #  + 7€ * 10 %    (0.7€)
    #  = 1.33 €
    assert postings_list.get_vat(True) == '1.33 €'

    # it should have vat now with the added postings
    assert postings_list.has_vat() is True
