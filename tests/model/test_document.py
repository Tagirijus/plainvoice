from plainvoice.model.document.document import Document
from plainvoice.model.document.document_type import DocumentType


def test_document_due_calculation():
    # create the instances
    doc = Document()
    doc_type = DocumentType()

    # set which fields are supposed to be the due and done date
    doc_type.set_fixed('date_due_fieldname', 'date_due', True)
    doc_type.set_fixed('date_done_fieldname', 'date_paid', True)

    # create two date fields for the test
    doc_type.add_fixed_field('date_due', 'date', None)
    doc_type.add_fixed_field('date_paid', 'date', None)
    doc_type.add_fixed_field('date_now', 'date', None)

    # set the doc to the doc_type descriptor
    doc.init_internals_with_doctype(doc_type)

    # fill the due date
    doc.set_fixed('date_due', '2024-09-03', True)

    # check if the correct fields will be used for
    # due and done/paid date
    assert doc.get_due_date(True) == '2024-09-03'
    assert doc.get_done_date(False) is None

    # the remaining days to due should be negative
    # since this test is written in the past and I set a due
    # date accordingly into the past, so that the test will
    # pass (hopefully) also in the future as well
    days_till_due_date = doc.days_till_due_date()
    assert (
        days_till_due_date is not None
        and days_till_due_date < 0
    )

    # also since the due date is in the past, the document
    # is supposed to be overdue
    assert doc.is_overdue() is True

    # now set an alternative to "now" for checking and set it to
    # the past before due date, so that the overdue will become
    # False
    doc.set_fixed('date_now', '2024-09-02', True)
    assert doc.is_overdue('date_now') is False

    # remove it again
    doc.set_fixed('date_now', None, False)
    assert doc.is_overdue() is True

    # now make the document "done" by setting the date
    # accordingly
    doc.set_fixed('date_paid', '2024-09-03', True)
    assert doc.is_overdue() is False

    # now remove the due date; then no days_till_due_date()
    # should be returned but None instead
    doc.set_fixed('date_due', None, False)
    assert doc.days_till_due_date() is None


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
