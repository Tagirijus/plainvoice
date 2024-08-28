'''
This test is supposed to represent a whole test run, basically.
It won't test a specific thign in particular, but a whole programm
test run as if plainvoice was installed fresh and the user has to
set up new data, etc.; which includes:

- Creating default type
- Creating default template
- Create an invoice with certain data
- Check the date methods of the Document object
- Check the calculation methods of the Posting objects
- Rendering this invoice
'''

from plainvoice.model.document.document_repository import DocumentRepository
from plainvoice.model.document.document_type_repository import \
    DocumentTypeRepository
from plainvoice.view.render import Render
from plainvoice.model.template.template_repository import TemplateRepository

from datetime import datetime, timedelta
import os
import shutil


def test_invoice_testrun(test_data_folder, test_data_file):
    # set the test data folder
    test_folder = test_data_folder('invoice_test')
    types_folder = test_folder + '/types'
    invoices_folder = test_folder + '/invoices'
    templates_folder = test_folder + '/templates'
    test_doc_type_file = test_data_file(
        'invoice_test/types/test_invoice_type.yaml'
    )
    test_doc_file = test_data_file(
        'invoice_test/invoices/test_invoice_doc.yaml'
    )
    test_doc_template_file = test_data_file(
        'invoice_test/templates/test_invoice_template.jinja'
    )
    test_doc_file_rendered = test_data_file(
        'invoice_test/invoices/test_invoice_doc.pdf'
    )

    # ###
    # Document testing
    # ###

    # create a DocumentTypeRepository
    doc_type_repo = DocumentTypeRepository(types_folder)

    # create a new doc type from scratch
    doc_type_repo.create_type('test_invoice_type')
    # it's done in another test already, yet just test it again here
    assert os.path.exists(test_doc_type_file) is True

    # for this test load this document type, change the folder to
    # the test folder and save it again
    test_doc_type = doc_type_repo.load_by_name('test_invoice_type')
    test_doc_type.set_fixed('folder', invoices_folder, True)
    doc_type_repo.save(test_doc_type)

    # now create a new document on this new type basis
    # for that first create a DocumentRepository
    doc_repo = DocumentRepository(types_folder)
    new_doc = doc_repo.create_document('test_invoice_type', 'test_invoice_doc')
    assert os.path.exists(new_doc.get_filename()) is True
    assert new_doc.get_filename() == test_doc_file

    # test default values, which should exist; do it by comparing the
    # internal dict "fixed", instead of the get_fixed() method, because
    # latter one will always return the default anyway, but this won't
    # get the info, if the default values were set into the file directly
    # already!
    #
    # also get the today date, since a date type can also have a string like
    # "+0" or "+14" (etc.) as a default, which will be interpreted as
    # "add/substract that many days from today to get the new date"
    date_default = datetime.now()
    due_date_default = datetime.now() + timedelta(days=14)
    should_be_fixed = {
        'date': date_default.strftime('%Y-%m-%d'),
        'due_date': due_date_default.strftime('%Y-%m-%d'),
        'title': 'invoice #',
        'receiver': 'Company Ltd.\nFirst M. Last\nStreet 9\n12345 City',
        'postings': []
    }
    assert new_doc._to_dict_fixed(True) == should_be_fixed

    # ###
    # Calculation testing
    # ###

    # set dates
    new_doc.set_fixed('date', '2024-08-27', True)
    new_doc.set_fixed('due_date', '2024-08-27', True)

    # add 14 days to the due date and check if it worked
    new_doc.add_days_to_date('due_date', 14)
    assert new_doc.get_fixed('due_date', True) == '2024-09-10'

    # it should also be 14 days in difference to the date
    assert new_doc.days_between_dates('date', 'due_date') == 14

    # now add some postings to the invoice
    # this one would be 8.75€ total + 0.88€ Vat = 9.63€
    new_doc.get_fixed('postings', False).add_posting(
        'posting a',
        'posting a details',
        '5.00 €',
        '1:45 min',
        '10 %'
    )
    posting_a = new_doc.get_fixed('postings', False).get_posting(0)
    assert posting_a.get_total(True) == '8.75 €'
    assert posting_a.get_vat(True) == '0.88 €'
    assert posting_a.get_total_with_vat(True) == '9.63 €'

    # this one would be 3.75€ total + 0.19€ Vat = 3.94€
    new_doc.get_fixed('postings', False).add_posting(
        'posting b',
        'posting b details',
        '2.50 €',
        '1.5 pieces',
        '5 %'
    )
    posting_b = new_doc.get_fixed('postings', False).get_posting(1)
    assert posting_b.get_total(True) == '3.75 €'
    assert posting_b.get_vat(True) == '0.19 €'
    assert posting_b.get_total_with_vat(True) == '3.94 €'

    # and how about all postings in total?
    postings = new_doc.get_fixed('postings', False)
    assert postings.get_total(True) == '12.50 €'
    assert postings.get_vat(True) == '1.07 €'
    assert postings.get_total_with_vat(True) == '13.57 €'

    # ###
    # Template testing
    # ###

    # create a template from basic template
    template_repo = TemplateRepository(templates_folder)
    template_repo.create_template('test_invoice_template')
    assert os.path.exists(test_doc_template_file) is True

    # now render the previous document with this template
    render = Render(templates_folder)
    render.render('test_invoice_template', new_doc)
    assert os.path.exists(test_doc_file_rendered) is True

    # remove all the test files again
    shutil.rmtree(test_folder)
