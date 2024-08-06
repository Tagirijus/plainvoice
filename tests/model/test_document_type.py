from plainvoice.model.document.document_type import DocumentType


def test_document_type_init():
    # first create an instance
    doc_type = DocumentType(
        'doc name',
        'doc folder',
        'doc pattern'
    )

    # now let's check if values were set correctly
    assert doc_type.get_fixed('name', True) == 'doc name'
    assert doc_type.get_fixed('folder', True) == 'doc folder'
    assert doc_type.get_fixed('filename_pattern', True) == 'doc pattern'


def test_document_type_fixed_fields():
    # first create an instance
    doc_type = DocumentType()

    # add some fixed field
    doc_type.add_fixed_field('user', 'str')
    doc_type.add_fixed_field('age', 'int')

    # check, if the resulting descriptor is correct
    should_be = {
        'user': 'str',
        'age': 'int'
    }
    assert doc_type.get_descriptor() == should_be
