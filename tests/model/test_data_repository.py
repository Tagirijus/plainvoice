from plainvoice.model.data.data_repository import DataRepository

import os
import pytest


def test_data_repository_absolute_filename():
    # create a DataRepository instance
    data_repo = DataRepository('/some/folder')

    # check if the filename generation works correctly
    abs_filename = data_repo.get_absolute_filename('test_file')
    assert abs_filename == '/some/folder/test_file.yaml'


def test_get_files_of_data_type_Data_repository(tmp_path):
    # info to myelf:
    #   tmp_path is a pytest feature, with which a temporary
    #   folde rcan be created and files inside it respectively.
    #   it is called "fixture".

    # create temporary file/s
    file1 = tmp_path / '_plainvoice_test_data_repository_1.yaml'
    file2 = tmp_path / '_plainvoice_test_data_repository_2.yaml'
    file3 = tmp_path / '_plainvoice_test_data_repository_3.txt'
    file1.write_text('visible: true')
    file2.write_text('visible: false')
    file3.write_text('temp plainvoice text')

    # create a DataRepository instance
    data_repo = DataRepository(str(tmp_path))

    # only the yaml files shoudl be included now
    file_list = data_repo.get_files_of_data_type()
    assert file_list == [
        str(file1), str(file2)
    ]


def test_list_from_data_repository(tmp_path):
    # info to myelf:
    #   tmp_path is a pytest feature, with which a temporary
    #   folde rcan be created and files inside it respectively.
    #   it is called "fixture".

    # create temporary file/s
    file1 = tmp_path / '_plainvoice_test_data_repository_1.yaml'
    file2 = tmp_path / '_plainvoice_test_data_repository_2.yaml'
    file1.write_text('visible: true')
    file2.write_text('visible: false')

    # create a DataRepository instance
    data_repo = DataRepository(str(tmp_path))

    # get the test files, which should just be the
    # ones, created for this pytest; also the method
    # will just get the pure name
    file_list = data_repo.get_list(False)
    names = list(file_list.keys())
    assert names == [
        '_plainvoice_test_data_repository_1',
        '_plainvoice_test_data_repository_2'
    ]

    # now get only the visible one
    file_list = data_repo.get_list(True)
    names = list(file_list.keys())
    assert names == [
        '_plainvoice_test_data_repository_1'
    ]


def test_load_data_model_from_file(tmp_path):
    # info to myelf:
    #   tmp_path is a pytest feature, with which a temporary
    #   folde rcan be created and files inside it respectively.
    #   it is called "fixture".

    # create temporary file/s
    file = tmp_path / '_plainvoice_test_data_repository.yaml'
    file.write_text('''
# base variables

visible: false


# fixed fields

fixed: nothing


# additional fields

testing: |-
  manu
  anna
  luna
''')

    # create a DataRepository instance
    # the folder might be not relevant here, since
    # I will do the test by loading the relative
    # filename to the program start
    data_repo = DataRepository('./')

    # get the dict from the file
    loader_dict = data_repo.load_from_name(str(file))

    # it should be the following dict now;
    # by the way: this dict is supposed to be used
    # with e.g. DataModel().instance_from_dict(loader_dict)
    # to be used to instantiate a new DataModel, thus loading
    # the data!
    should_be = {
        'visible': False,
        'fixed': 'nothing',
        'testing': 'manu\nanna\nluna'
    }
    assert loader_dict == should_be
