from plainvoice.model.file.file import File

import os
import pytest

FILE_TEST_PATH = './_plainvoice_tests.yaml'
FILE_TEST_CONTENT = 'plainvoice testing'


@pytest.fixture
def temp_file():
    file_path = FILE_TEST_PATH

    with open(file_path, 'w') as f:
        f.write(FILE_TEST_CONTENT)

    yield file_path

    if os.path.exists(file_path):
        os.remove(file_path)


def test_copy(temp_file):
    temp_file_copy = temp_file + '.copy'
    file = File()
    file.copy(temp_file, temp_file_copy)
    if os.path.exists(temp_file_copy):
        with open(temp_file, 'r') as test_file:
            data = test_file.read()
        os.remove(temp_file_copy)
    assert data == FILE_TEST_CONTENT


def test_get_extension_get_folder():
    file = File('./')
    assert file.get_extension() == 'yaml'
    assert file.get_folder() == './'


def test_replace_file_extension_with_pdf():
    filename = '/home/user/.plainvoice/invoice.html'
    filename_pdf = File().replace_file_extension_with_pdf(filename)
    assert filename_pdf == '/home/user/.plainvoice/invoice.pdf'


def test_to_yaml_string():
    in_dict = {
        'name': 'manuel',
        'age': 36,
        'dev': False,
        'list': ['a', 'b', 'c']
    }
    out_string = File().to_yaml_string(in_dict)
    assert out_string == '''name: manuel
age: 36
dev: false
list:
- a
- b
- c
'''
