from plainvoice.model.document.document import Document
from plainvoice.model.document.document_type import DocumentType


def test_document_init():
    # create an instance
    doc = Document('doc type')

    # the document type name check
    assert doc.get_document_typename() == 'doc type'

    # now change it
    doc.set_document_typename('new doc type')

    # and check if setter works
    assert doc.get_document_typename() == 'new doc type'


def test_document_fixed_fields_conversion():
    # create the instances
    doc = Document()
    doc_type = DocumentType()

    # create all available field types with the
    # DocumentType first
    doc_type.add_fixed_field('string', 'str', 'empty')
    doc_type.add_fixed_field('integer', 'int', 0)
    doc_type.add_fixed_field('dictionary', 'dict', {'foo': 'bar'})
    doc_type.add_fixed_field('list', 'list', [1, 2, 3])
    doc_type.add_fixed_field('date', 'date', '1970-01-01')
    doc_type.add_fixed_field('decimal', 'Decimal', 1.5)
    doc_type.add_fixed_field('posting', 'Posting', {})
    doc_type.add_fixed_field('postings', 'PostingsList', [])
    doc_type.add_fixed_field('quantity', 'Quantity', '1')
    doc_type.add_fixed_field('price', 'Price', '1.00 €')
    doc_type.add_fixed_field('percentage', 'Percentage', '10 %')

    # set the doc to the doc_type descriptor
    doc.set_fixed_fields_descriptor(
        doc_type.get_descriptor()
    )

    # now check create an example loader dict, which could be
    # the content of a YAML later
    loader = {
        'visible': False,
        'doc_typename': 'invoice',
        'integer': 9,
        'links': [],
        'dictionary': {
            'val a': 'a',
            'val b': 'b'
        },
        'list': ['a', 'b', 'c'],
        'date': '2024-08-07',
        'decimal': 2.75,
        'posting': {
            'title': 'posting title',
            'detail': 'posting detail text',
            'unit_price': '1.00 €',
            'quantity': '1:45 min',
            'vat': '5 %',
            'notes': ''
        },
        'postings': [
            {
                'title': 'postings a',
                'detail': 'postings detail text a',
                'unit_price': '2.00 €',
                'quantity': '2.0 postings',
                'vat': '10 %',
                'notes': ''
            },
            {
                'title': 'postings b',
                'detail': 'postings detail text b',
                'unit_price': '3.00 €',
                'quantity': '3.0 postings',
                'vat': '15 %',
                'notes': ''
            }
        ],
        'quantity': '1:45 min',
        'price': '9.00 €',
        'percentage': '50 %',
        'i_am_additional': 'manu'
    }

    # load this big dict into the doc
    doc.from_dict(loader)

    # prepare how the internal updated dict should be
    # the default for 'string' should be 'empty'
    loader.update({'string': 'empty'})

    # is the conversion back the same?
    assert doc.to_dict(True) == loader

    # check the variables here. I will even use the magic .get() method
    # to test it at the same time.

    # now check some base attributes
    assert doc.is_visible() is False
    assert doc.get_document_typename() == 'invoice'

    # now check fixed fields: simple Python types
    # the first string even should contain the default
    assert doc.get_fixed('string', True) == 'empty'

    # test the posting/s calculations
    # total of single posting: 1:45 min * 1.00 € == 1.75 €
    total = doc.get('posting').get_total(True)
    assert total == '1.75 €'

    # total should be 2 * 2.00 € + 3 * 3.00 € == 13.00 €
    total = doc.get('postings').get_total(True)
    assert total == '13.00 €'
    # vat should be 2 * 2.00 € * 10 % == 0.40 €
    #             + 3 * 3.00 € * 15 % == 1.35 €
    #                                 == 1.75 €
    total = doc.get('postings').get_vat(True)
    assert total == '1.75 €'

    # test date type
    doc.add_days_to_date('date', -2)
    assert doc.get('date', True) == '2024-08-05'


def test_document_lists():
    # create the instances
    doc = Document()

    # add links
    filename = '/foo/bar/file.yaml'
    doc.add_link(filename)

    # check if it now exists
    assert doc.link_exists(filename) is True
    assert filename in doc.get_links()

    # remove it again
    doc.remove_link(filename)

    # now it should not exist anymore
    assert doc.link_exists(filename) is False
    assert filename not in doc.get_links()
