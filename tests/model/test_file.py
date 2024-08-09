from plainvoice.model.file.file import File

import os


def test_copy(test_temp_file):
    # prepare a filename to copy to
    # and copy it
    temp_file_content = 'plainvoice testing File class ...'
    temp_file_name = '_plainvoice_File_test.txt'
    temp_file = test_temp_file(temp_file_name, temp_file_content)
    temp_file_name_copy = temp_file + '.copy'

    file = File()
    file.copy(temp_file, temp_file_name_copy)

    if os.path.exists(temp_file_name_copy):
        with open(temp_file, 'r') as temp_file:
            data = temp_file.read()
        os.remove(temp_file_name_copy)

    # the content of the copied file should be
    # the same as the original one
    assert data == temp_file_content


def test_get_extension_get_folder():
    # create a File instance
    file = File()

    # the File object uses its component FilePathGenerator
    # for getthing the default extension and folder, if
    # no such things were set during initialisation
    assert file.get_extension() == 'yaml'
    assert file.get_folder() == './'

    # create a File with own set extension and folder
    file_b = File('/home/user', '.py')

    # now the set variables should be used for the
    # internal variables for extension and folder.
    # also the dot from the extension should get
    # removed.
    assert file_b.get_extension() == 'py'
    assert file_b.get_folder() == '/home/user'


def test_replace_file_extension_with_pdf():
    # prepare some variables to test on
    filename = '/home/user/.plainvoice/invoice.html'
    filename_pdf = File().replace_extension_with_pdf(filename)

    # the respecting method should have replaced the extension
    # with the correct PDF extension
    assert filename_pdf == '/home/user/.plainvoice/invoice.pdf'
