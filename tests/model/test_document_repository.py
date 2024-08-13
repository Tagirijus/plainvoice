from plainvoice.model.document.document import Document
from plainvoice.model.document.document_repository import DocumentRepository


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
    doc_repo.save(doc, 'invoice_saving')

    # load the saved file again
    # first "clear" the saved value
    doc.set_fixed('title', '', True)
    assert doc.get_fixed('title', True) == ''
    # then load it
    doc.from_dict(
        doc_repo.load_dict_from_name('invoice_saving')
    )

    # now it should be the previously stored value again
    assert doc.get_fixed('title', True) == 'invoice saving title'
