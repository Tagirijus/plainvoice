from plainvoice.model.document.document_repository import DocumentRepository
from plainvoice.view.render import Render
from plainvoice.utils import doc_utils

import os


def test_render_document(test_data_folder, test_data_file):
    # set the test data folder
    test_folder = test_data_folder('render_tests')
    templates_folder = test_folder + '/templates'
    rendered_file = test_data_file('document_repository/docs/invoice_1.pdf')

    # create a render instance
    render = Render(templates_folder)

    # also set the test data folder for the documents
    test_folder_doc = test_data_folder('document_repository')
    types_folder = test_folder_doc + '/types'

    # instantiate the document repository
    doc_repo = DocumentRepository(types_folder)

    # load by doc_typename + name combi
    doc = doc_repo.load('invoice_1', 'invoice')

    # now render this document without giving a name, thus it should
    # use the loaded documents filename
    render.render('invoice', doc, doc_repo.get_user_by_username())

    # there now should exist the rendered_file
    assert os.path.exists(rendered_file) is True
    # remove the file again
    os.unlink(rendered_file)
