from plainvoice.model.document.document_repository import DocumentRepository
from plainvoice.model.document.document import Document


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
    linked_client = doc_repo.get_links_from_document(doc, False)[0]

    # WEITER HIER
    # get_links_from_document() mit separatem getter, der Document bekommt
    # und separatem getter für strings
    if isinstance(linked_client, Document):
        assert linked_client.get_fixed('first_name', True) == 'manu'
        assert linked_client.get_fixed('last_name', True) == 'nunu'
    else:
        raise TypeError('linked_client is no Document')
