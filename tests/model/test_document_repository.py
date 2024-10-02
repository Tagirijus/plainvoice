from plainvoice.model.document.document import Document
from plainvoice.model.document.document_repository import DocumentRepository
from plainvoice.model.document.document_type_repository import DocumentTypeRepository

from datetime import datetime
import os


def test_create_default_doc_type(test_data_folder, test_data_file):
    # set the test data folder
    test_folder = test_data_folder('document_repository')
    types_folder = test_folder + '/types'
    test_file = test_data_file('document_repository/types/new_type.yaml')

    # create a DocumentTypeRepository
    doc_type_repo = DocumentTypeRepository(types_folder)

    # create a new doc type from scratch
    doc_type_repo.create_type('new_type')

    # this file should now exist in the doc types folder
    assert os.path.exists(test_file) is True
    # remove the file again
    os.unlink(test_file)


def test_document_cache(test_data_folder, test_data_file):
    # set the test data folder
    test_folder = test_data_folder('document_repository')
    types_folder = test_folder + '/types'
    test_file = test_data_file('document_repository/docs/invoice_1.yaml')

    # instantiate the document repository
    doc_repo = DocumentRepository(types_folder)

    # load by doc_typename + name combi
    doc = doc_repo.load('invoice_1', 'invoice')

    # now the cache should also have filled the document into
    # the cache, which is accessible by abs_filename; test it!
    assert doc == doc_repo.cache.get_by_filename(test_file)

    # instantiate a new document repository
    doc_repo = DocumentRepository(types_folder)

    # now load it first by absolute filename
    doc = doc_repo.load(test_file)

    # now it should also be fetchable by doc_typename + name combi
    assert doc == doc_repo.cache.get_by_doc_type_and_name('invoice', 'invoice_1')


def test_document_due_list_invoices_only(test_data_folder):
    # set the test data folder
    test_folder = test_data_folder('document_repository')
    types_folder = test_folder + '/types'

    # instantiate the document repository
    doc_repo = DocumentRepository(types_folder)

    # check if the correct due invoices are being fetched:
    #   - due
    #   - overdue
    #   - also not visible ones
    invoices_due_and_overdue = doc_repo.get_due_docs('invoice_due', True, True, False)
    # it should be these invoices only
    codes_check = set(['1', '4', '5', '6'])
    codes_fetched = set([d.get('code', False) for d in invoices_due_and_overdue])
    assert codes_check == codes_fetched

    # check if the correct due invoices are being fetched:
    #   - due
    #   - overdue
    #   - only visible ones
    invoices_due_and_overdue = doc_repo.get_due_docs('invoice_due', True, True, True)
    # it should be these invoices only
    codes_check = set(['1', '5'])
    codes_fetched = set([d.get('code', False) for d in invoices_due_and_overdue])
    assert codes_check == codes_fetched

    # check if the correct due invoices are being fetched:
    #   - due
    #   - not overdue
    #   - also not visible ones
    invoices_due_and_overdue = doc_repo.get_due_docs('invoice_due', True, False, False)
    # it should be these invoices only
    codes_check = set(['1', '4'])
    codes_fetched = set([d.get('code', False) for d in invoices_due_and_overdue])
    assert codes_check == codes_fetched

    # check if the correct due invoices are being fetched:
    #   - not due
    #   - overdue
    #   - also not visible ones
    invoices_due_and_overdue = doc_repo.get_due_docs('invoice_due', False, True, False)
    # it should be these invoices only
    codes_check = set(['5', '6'])
    codes_fetched = set([d.get('code', False) for d in invoices_due_and_overdue])
    assert codes_check == codes_fetched

    # check if the correct due invoices are being fetched:
    #   - not due
    #   - overdue
    #   - only visible ones
    invoices_due_and_overdue = doc_repo.get_due_docs('invoice_due', False, True, True)
    # it should be these invoices only
    codes_check = set(['5'])
    codes_fetched = set([d.get('code', False) for d in invoices_due_and_overdue])
    assert codes_check == codes_fetched

    # check if the correct due invoices are being fetched:
    #   - due
    #   - not overdue
    #   - only visible ones
    invoices_due_and_overdue = doc_repo.get_due_docs('invoice_due', True, False, True)
    # it should be these invoices only
    codes_check = set(['1'])
    codes_fetched = set([d.get('code', False) for d in invoices_due_and_overdue])
    assert codes_check == codes_fetched


def test_document_due_list_all_types(test_data_folder):
    # set the test data folder
    test_folder = test_data_folder('document_repository')
    types_folder = test_folder + '/types'

    # instantiate the document repository
    doc_repo = DocumentRepository(types_folder)

    # check if the correct due invoices AND quotes are being fetched:
    #   - due
    #   - overdue
    #   - also not visible ones
    invoices_due_and_overdue = doc_repo.get_due_docs('', True, True, False)
    # it should be these invoices only
    codes_check = set(['1', '4', '5', '6', 'q1', 'q2', 'q3', 'q4'])
    codes_fetched = set([d.get('code', False) for d in invoices_due_and_overdue])
    assert codes_check == codes_fetched

    # check if the correct due invoices AND quotes are being fetched:
    #   - due
    #   - overdue
    #   - only visible ones
    invoices_due_and_overdue = doc_repo.get_due_docs('', True, True, True)
    # it should be these invoices only
    codes_check = set(['1', '5', 'q1', 'q2'])
    codes_fetched = set([d.get('code', False) for d in invoices_due_and_overdue])
    assert codes_check == codes_fetched

    # check if the correct due invoices AND quotes are being fetched:
    #   - due
    #   - not overdue
    #   - also not visible ones
    invoices_due_and_overdue = doc_repo.get_due_docs('', True, False, False)
    # it should be these invoices only
    codes_check = set(['1', '4', 'q1', 'q3'])
    codes_fetched = set([d.get('code', False) for d in invoices_due_and_overdue])
    assert codes_check == codes_fetched

    # check if the correct due invoices AND quotes are being fetched:
    #   - not due
    #   - overdue
    #   - also not visible ones
    invoices_due_and_overdue = doc_repo.get_due_docs('', False, True, False)
    # it should be these invoices only
    codes_check = set(['5', '6', 'q2', 'q4'])
    codes_fetched = set([d.get('code', False) for d in invoices_due_and_overdue])
    assert codes_check == codes_fetched

    # check if the correct due invoices AND quotes are being fetched:
    #   - not due
    #   - overdue
    #   - only visible ones
    invoices_due_and_overdue = doc_repo.get_due_docs('', False, True, True)
    # it should be these invoices only
    codes_check = set(['5', 'q2'])
    codes_fetched = set([d.get('code', False) for d in invoices_due_and_overdue])
    assert codes_check == codes_fetched

    # check if the correct due invoices AND quotes are being fetched:
    #   - due
    #   - not overdue
    #   - only visible ones
    invoices_due_and_overdue = doc_repo.get_due_docs('', True, False, True)
    # it should be these invoices only
    codes_check = set(['1', 'q1'])
    codes_fetched = set([d.get('code', False) for d in invoices_due_and_overdue])
    assert codes_check == codes_fetched


def test_document_from_absolute_filename(test_data_folder, test_data_file):
    # set the test data folder
    test_folder = test_data_folder('document_repository')
    types_folder = test_folder + '/types'
    test_file = test_data_file('document_repository/docs/invoice_1.yaml')

    # instantiate the document repository
    doc_repo = DocumentRepository(types_folder)

    # now load a document with the absolute filename
    # for "invoice_1"
    doc = doc_repo.load(test_file)

    # it should have the title 'invoice #1' and is invisible
    assert doc.is_visible() is False
    assert doc.get_fixed('title', True) == 'invoice #1'
    assert doc.get_additional('company') == 'Plainvoice Inc.'


def test_document_from_name(test_data_folder):
    # set the test data folder
    test_folder = test_data_folder('document_repository')
    types_folder = test_folder + '/types'

    # instantiate the document repository
    doc_repo = DocumentRepository(types_folder)

    # now load a document with the filename "invoice_1"
    # and the document type name "invoice"
    doc = doc_repo.load('invoice_1', 'invoice')

    # it should have the title 'invoice #1' and is invisible
    assert doc.is_visible() is False
    assert doc.get_fixed('title', True) == 'invoice #1'
    assert doc.get_additional('company') == 'Plainvoice Inc.'


def test_document_type_repository(test_data_folder):
    # set the test data folder
    test_folder = test_data_folder('document_repository')
    types_folder = test_folder + '/types'

    # instantiate the document type repository
    # normally it is supposed to work without setting a folder,
    # since later it should be controlled via the config. yet for
    # this test I set it, since I need to set it in the data
    # test folder
    doc_type_repo = DocumentTypeRepository(types_folder)

    # there should be an invoice document type in my test data
    invoice_type = doc_type_repo.load_by_name('invoice')

    # this should be the descriptor dict, which the document
    # type can provide
    should_be_descriptor = {'title': {'type': 'str', 'default': 'invoice #'}}
    assert invoice_type.get_descriptor() == should_be_descriptor

    # also it should have such additional fixed fields
    assert (
        invoice_type.get_fixed('folder', False)
        == '{test_data_dir}/document_repository/docs'
    )
    assert invoice_type.get_fixed('filename_pattern', False) == 'invoice_{code}'


def test_document_loading_without_existing_type(test_data_folder):
    # set the test data folder
    test_folder = test_data_folder('document_repository')
    types_folder = test_folder + '/types'

    # instantiate the document repository
    doc_repo = DocumentRepository(types_folder)

    # --- --- test for loading with doc type + name --- ---
    # now load a document with the name "invoice_1"
    # and the document type name "invoice"
    doc = doc_repo.load('invoice_1', 'not_existing')
    # should have no absolute filename, thus basically not loaded
    assert doc.get_filename() == ''

    # --- --- test for loading with absolute filename --- ---
    # now load a document with the absolute filename;
    # this time the doc should still be loaed, yet without
    # setting the fixed fields to fiexed fields, yet to
    # additional fields instead.

    # for that, use the specific test document for it, which
    # has set a type, which does not exist
    test_file = test_folder + '/docs2/no_type.yaml'
    doc = doc_repo.load(test_file)

    # I set these fixed fields:
    #   title: 'the title'
    #   other field: 'this is fixed'
    # and this additional field:
    #   add: 'additional field'
    # should be all on additional fields now
    assert doc.get_additional('title') == 'the title'
    assert doc.get_additional('other field') == 'this is fixed'
    assert doc.get_additional('add') == 'additional field'

    # and the magic get() method should also work
    assert doc.get('title') == 'the title'
    assert doc.get('other field') == 'this is fixed'
    assert doc.get('add') == 'additional field'


def test_generate_next_filename(test_data_folder):
    # set the test data folder
    test_folder = test_data_folder('document_repository')
    types_folder = test_folder + '/types'

    # since Populator class will have a placeholder for
    # the actual year and this test should also succeed
    # in the future, I have to construct my testing string
    # here with the actual date as well
    year = datetime.now().year

    # instantiate the document repository
    doc_repo = DocumentRepository(types_folder)

    assert (
        doc_repo.generate_next_name('invoice_filename') == f'{year}/invoice_{year}_-_4'
    )


def test_save_document(test_data_folder):
    # set the test data folder
    test_folder = test_data_folder('document_repository')
    types_folder = test_folder + '/types'

    # instantiate the document repository
    doc_repo = DocumentRepository(types_folder)

    # and a document with some data
    doc = Document('invoice')
    doc.set_fixed_fields_descriptor(doc_repo.get_descriptor('invoice'))
    doc.set_fixed('title', 'invoice saving title', True)

    # save it
    abs_filename = doc_repo.save(doc, 'invoice_saving')

    # load the saved file again
    # first "clear" the saved value
    doc.set_fixed('title', '', True)
    assert doc.get_fixed('title', True) == ''
    # then load it / also use the absolute filename here, for testing
    # instantiate a new document repository for this, so that the
    # cache won't load the other old instance
    doc_repo = DocumentRepository(types_folder)
    doc = doc_repo.load(abs_filename)

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
    # instantiate a new document repository for this, so that the
    # cache won't load the other old instance
    doc_repo = DocumentRepository(types_folder)
    doc = doc_repo.load(abs_filename)
    assert doc.get_fixed('title', True) == 'invoice saving title new'

    # finally remove the testing file again
    os.remove(abs_filename)


def test_save_document_without_name(test_data_folder):
    # set the test data folder
    test_folder = test_data_folder('document_repository')
    types_folder = test_folder + '/types'

    # instantiate the document repository
    doc_repo = DocumentRepository(types_folder)

    # and a document with some data
    doc = Document('invoice')
    doc.set_fixed_fields_descriptor(doc_repo.get_descriptor('invoice'))
    doc.set_fixed('title', 'invoice save state testing', True)

    # save it, yet without giving a name
    abs_filename = doc_repo.save(doc)

    # this should not have saved the file, thus abs_filename
    # being blank
    assert abs_filename == ''
