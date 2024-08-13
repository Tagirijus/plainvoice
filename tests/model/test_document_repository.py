from plainvoice.model.document.document import Document
from plainvoice.model.document.document_repository import DocumentRepository

import os


def test_document_from_absolute_filename(test_data_folder, test_data_file):
    # set the test data folder
    test_folder = test_data_folder('document_repository')
    types_folder = test_folder + '/types'
    test_file = test_data_file('document_repository/docs/invoice_1.yaml')

    # instantiate the document repository
    # do not set the document type name so that
    # at the moment the repo will not know it.
    # this test is supposed to get the document
    # type name from the document YAML itself to
    # load the document type!
    doc_repo = DocumentRepository('', types_folder)

    # now load a document with the filename "invoice_1"
    doc = doc_repo.load_document_from_file(test_file)

    # it should have the title 'invoice #1' and is invisible
    assert doc.is_visible() is False
    assert doc.get_fixed('title', True) == 'invoice #1'
    assert doc.get_additional('company') == 'Plainvoice Inc.'


def test_document_from_name(test_data_folder):
    # set the test data folder
    test_folder = test_data_folder('document_repository')
    types_folder = test_folder + '/types'

    # instantiate the document repository
    doc_repo = DocumentRepository('invoice', types_folder)

    # now load a document with the filename "invoice_1"
    doc = doc_repo.load_document_from_name('invoice_1')

    # it should have the title 'invoice #1' and is invisible
    assert doc.is_visible() is False
    assert doc.get_fixed('title', True) == 'invoice #1'
    assert doc.get_additional('company') == 'Plainvoice Inc.'


def test_document_linking(test_data_folder):
    # set the test data folder
    test_folder = test_data_folder('document_repository')
    types_folder = test_folder + '/types'

    # instantiate the document repository
    doc_repo = DocumentRepository('invoice', types_folder)

    # now load a document with the filename "invoice_1"
    doc = doc_repo.load_document_from_name('invoice_1')

    # now get the linked client_1
    linked_client = doc_repo.get_links_from_document_as_document(doc)[0]

    assert linked_client.get_fixed('first_name', True) == 'manu'
    assert linked_client.get_fixed('last_name', True) == 'nunu'


def test_save_document(test_data_folder):
    # set the test data folder
    test_folder = test_data_folder('document_repository')
    types_folder = test_folder + '/types'

    # instantiate the document repository
    doc_repo = DocumentRepository('invoice', types_folder)

    # and a document with some data
    doc = Document('invoice')
    doc.set_fixed_fields_descriptor(
        doc_repo.get_descriptor()
    )
    doc.set_fixed('title', 'invoice saving title', True)

    # save it
    abs_filename = doc_repo.save(doc, 'invoice_saving')

    # load the saved file again
    # first "clear" the saved value
    doc.set_fixed('title', '', True)
    assert doc.get_fixed('title', True) == ''
    # then load it / also use the absolute filename here, for testing
    doc.from_dict(
        doc_repo.load_dict_from_name(abs_filename)
    )

    # now it should be the previously stored value again
    assert doc.get_fixed('title', True) == 'invoice saving title'

    # now change the value again and save it by using
    # only the save() method without the name argument;
    # the DocumentRepository should get the absolute
    # filename from the temp attribute abs_filename of
    # the Document class now
    doc.set_fixed('title', 'invoice saving title new', True)
    abs_filename = doc_repo.save(doc)

    # change things and load it again to see if the first change
    # got saved
    doc.set_fixed('title', 'unsaved', True)
    doc.from_dict(
        doc_repo.load_dict_from_name(abs_filename)
    )
    assert doc.get_fixed('title', True) == 'invoice saving title new'

    # finally remove the testing file again
    os.remove(abs_filename)


def test_save_document_without_name(test_data_folder):
    # set the test data folder
    test_folder = test_data_folder('document_repository')
    types_folder = test_folder + '/types'

    # instantiate the document repository
    doc_repo = DocumentRepository('invoice', types_folder)

    # and a document with some data
    doc = Document('invoice')
    doc.set_fixed_fields_descriptor(
        doc_repo.get_descriptor()
    )
    doc.set_fixed('title', 'invoice save state testing', True)

    # save it, yet without giving a name
    abs_filename = doc_repo.save(doc)

    # this should not have saved the file, thus abs_filename
    # being blank
    assert abs_filename == ''
