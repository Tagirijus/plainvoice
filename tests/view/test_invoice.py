'''
This test is supposed to represent a whole test run, basically.
It won't test a specific thign in particular, but a whole programm
test run as if plainvoice was installed fresh and the user has to
set up new data, etc.; which includes:

- Creating default type
- Creating default template
- Create an invoice with certain data
- Check the calculation methods of Document
- Check the date methods of Document
'''

from plainvoice.model.document.document_repository import DocumentRepository
from plainvoice.model.document.document_type_repository import \
    DocumentTypeRepository
from plainvoice.view.render import Render

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
    # get info if the default values were set into the file directly
    # already!
    should_be_fixed = {
        'date': None,
        'due_date': None,
        'title': 'invoice #',
        'receiver': 'Company Ltd.\nFirst M. Last\nStreet 9\n12345 City',
        'postings': []
    }
    assert new_doc._to_dict_fixed(True) == should_be_fixed

    # ###
    # Template testing
    # ###

    # create a template from basic template
    render = Render(templates_folder)
    render.create_template('test_invoice_template')
    assert os.path.exists(test_doc_template_file) is True

    # now render the previous document with this template
    render.render('test_invoice_template', new_doc)
    assert os.path.exists(test_doc_file_rendered) is True

    # remove all the test files again
    shutil.rmtree(test_folder)
