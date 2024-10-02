from plainvoice.model.document.document import Document
from plainvoice.model.document.document_calculator import DocumentCalculator
from plainvoice.model.document.document_type import DocumentType


def test_doc_calc_total():
    # first create documents to calculate
    doc1 = Document()
    doc2 = Document()
    doc_type = DocumentType()

    # get them some fields to calculate on
    doc_type.add_fixed_field('posting', 'Posting', {})
    doc_type.add_fixed_field('postings', 'PostingsList', [])

    # set the doc to the doc_type descriptor
    doc1.set_fixed_fields_descriptor(doc_type.get_descriptor())
    doc2.set_fixed_fields_descriptor(doc_type.get_descriptor())

    # fill them with numbers
    doc1.get('posting').set_fixed('quantity', '1', True)
    doc1.get('posting').set_fixed('unit_price', '1.00 €', True)
    doc1.get('postings').add_posting(
        title='', detail='', unit_price='1.00 €', quantity='1', vat='0 %'
    )
    doc2.get('postings').add_posting(
        title='', detail='', unit_price='2.00 €', quantity='1', vat='0 %'
    )
    doc2.get('postings').add_posting(
        title='', detail='', unit_price='3.00 €', quantity='1', vat='10 %'
    )

    # put both documents into the documents calcualtor
    doc_calc = DocumentCalculator([doc1, doc2])

    # all should sum up to 7.00 € for the total
    assert doc_calc.get_total(True) == '7.00 €'

    # all should sum up to 0.30 € for the vat
    assert doc_calc.get_vat(True) == '0.30 €'

    # all should sum up to 7.30 € for the total with vat
    assert doc_calc.get_total_with_vat(True) == '7.30 €'
