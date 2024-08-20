from plainvoice.model.document.document import Document
from plainvoice.model.document.document_type import DocumentType
from plainvoice.model.document.document_type_repository import \
    DocumentTypeRepository
from plainvoice.model.document.document_repository import DocumentRepository

import pytest
import shutil


@pytest.fixture()
def setup_and_teardown(test_data_folder):
    '''
    Create some test documents to test the linking on and
    remove them after the test again.
    '''
    test_folder = test_data_folder('document_linking')
    types_folder = test_folder + '/types'
    clients_folder = test_folder + '/clients'
    docs_folder = test_folder + '/docs'

    # instantiate the document type repository
    # to be able to save and load the doc types
    doc_type_repo = DocumentTypeRepository(types_folder)

    # create types
    client_type = DocumentType(clients_folder)
    client_type.define_fixed_field_type('str', str, str)
    client_type.add_fixed_field('name', 'str', '')
    doc_type_repo.save(client_type, 'client')

    doc_type = DocumentType(docs_folder)
    doc_type.define_fixed_field_type('str', str, str)
    doc_type.add_fixed_field('title', 'str', 'new document')
    doc_type_repo.save(doc_type, 'doc')

    # instantiate the document repository
    # to be able to save and load the docs
    doc_repo = DocumentRepository(types_folder)

    # now create some test documents
    client_1 = doc_repo.new_document_by_type('client')
    client_1.set_fixed('name', 'manu', True)
    doc_repo.save(client_1, 'client_1')
    client_2 = Document('client')
    client_2.set_fixed('name', 'luna', True)
    doc_repo.save(client_2, 'client_2')

    doc_1 = doc_repo.new_document_by_type('doc')
    doc_1.set_fixed('title', 'the first document', True)
    doc_repo.save(doc_1, 'doc_1')
    doc_2 = doc_repo.new_document_by_type('doc')
    doc_2.set_fixed('title', 'the second document', True)
    doc_repo.save(doc_2, 'doc_2')

    yield

    # finally just remove the whole test data folder,
    # including its content, which was temporary anyway
    shutil.rmtree(test_folder)


def test_link_documents(setup_and_teardown, test_data_folder):
    test_folder = test_data_folder('document_linking')
    types_folder = test_folder + '/types'

    # instantiate the document repository
    doc_repo = DocumentRepository(types_folder)

    # get the first client and the first document
    client_1 = doc_repo.load('client_1', 'client')
    doc_1 = doc_repo.load('doc_1', 'doc')

    # now link those two
    doc_repo.links.add_link(client_1, doc_1)

    # check the link on runtime (there should be one now on both sites)
    client_1_links = doc_repo.get_links_of_document(client_1)
    doc_1_links = doc_repo.get_links_of_document(doc_1)
    assert len(client_1_links) == 1
    assert len(doc_1_links) == 1

    # save both document
    doc_repo.save(client_1)
    doc_repo.save(doc_1)

    # generate a completely new doc repo so that the cache
    # does not know about the two documents
    doc_repo_new = DocumentRepository(types_folder)

    # now load the client
    client_new = doc_repo_new.load('client_1', 'client')

    # now get it's first linked document
    client_new_links = doc_repo_new.get_links_of_document(client_new)
    assert len(client_new_links) == 1
    # ok, linked document should exist, put it onto a variable
    # for more intutiive ongoing tests
    linked_doc = client_new_links[0]
    assert linked_doc.get_fixed('title', True) == 'the first document'

    # does the link works vice versa?
    doc_new_links = doc_repo_new.get_links_of_document(linked_doc)
    assert len(doc_new_links) == 1
    # ok, linked client should exist, put it onto a variable
    # for more intutiive ongoing tests
    linked_client = doc_new_links[0]
    assert linked_client.get_fixed('name', True) == 'manu'

    # quickly also check caching; load the linked doc_1 again,
    # which should be a reference only
    doc_again = doc_repo_new.load('doc_1', 'doc')
    assert doc_again == linked_doc


def test_rename_doc_and_links_respectively(
    setup_and_teardown,
    test_data_folder
):
    test_folder = test_data_folder('document_linking')
    types_folder = test_folder + '/types'

    # instantiate the document repository
    doc_repo = DocumentRepository(types_folder)

    # get the first client and the first document
    client_1 = doc_repo.load('client_1', 'client')
    doc_1 = doc_repo.load('doc_1', 'doc')

    # now link those two and save both already
    doc_repo.links.add_link(client_1, doc_1)
    doc_repo.save(client_1)
    doc_repo.save(doc_1)

    # now comes the testing part:
    #   I want to change a value of one document,
    #   rename it and see only the link was changed.
    #   The changed value shall not be saved already.
    #   So renaming should only rename the file, adjust
    #   the cache and adjust the absolute filename of
    #   the doc in its links. Latter one wil be saved
    #   immediately, though.
    doc_repo.rename_document(doc_1, 'doc_one')
    doc_1.set_fixed('title', 'the 1st document', True)

    # quickly check the cache integrity
    doc_1_reload = doc_repo.load('doc_one', 'doc')
    assert doc_1_reload == doc_1

    # now I use a new repo to laod both docs again;
    # the client should now have the new path of doc_1,
    # but doc_1 title should still be the old one.
    doc_repo_new = DocumentRepository(types_folder)
    client_new = doc_repo_new.load('client_1', 'client')
    doc_new = doc_repo_new.load('doc_one', 'doc')

    doc_new_from_client_link = client_new.get_links()[0]

    # the document values should not have changed
    assert doc_new.get_fixed('title', True) == 'the first document'

    # the link in client (the absolute path) should be changed
    assert 'doc_one' in doc_new_from_client_link
    assert 'doc_1' not in doc_new_from_client_link
