from plainvoice.model.data.data_model import DataModel
from plainvoice.model.data.data_repository import DataRepository


def test_data_repository_absolute_filename():
    # create a DataRepository instance
    data_repo = DataRepository('/some/folder')

    # check if the filename generation works correctly
    abs_filename = data_repo.get_absolute_filename('test_file')
    assert abs_filename == '/some/folder/test_file.yaml'


def test_get_files_of_data_type_data_repository(
    test_data_folder,
    test_data_file
):
    # use the tests/data/data_repository folder for it
    folder = test_data_folder('data_repository')

    # create a DataRepository instance
    data_repo = DataRepository(folder)

    # only the yaml files shoudl be included now
    file_list = data_repo.get_files_of_data_type()
    # this test will not work anymore, if I add additional test
    # files to this folder: "tests/data/data_repository"!
    assert set(file_list) == set([
        test_data_file('data_repository/test_document_a.yaml'),
        test_data_file('data_repository/test_document_b.yaml'),
        test_data_file('data_repository/test_document_loading.yaml'),
        test_data_file('data_repository/test_document_saving.yaml')
    ])


def test_list_from_data_repository(test_data_folder):
    # use the tests/data/data_repository folder for it
    folder = test_data_folder('data_repository')

    # create a DataRepository instance
    data_repo = DataRepository(folder)

    # get the test files, which should just be the
    # ones, created for this pytest; also the method
    # will just get the pure name
    file_list = data_repo.get_list(False)
    names = list(file_list.keys())
    assert set(names) == set([
        'test_document_a',
        'test_document_b',
        'test_document_loading',
        'test_document_saving'
    ])

    # now get only the visibles one
    file_list = data_repo.get_list(True)
    names = list(file_list.keys())
    assert set(names) == set([
        'test_document_a',
        'test_document_loading',
        'test_document_saving'
    ])


def test_load_data_model_from_file(test_data_folder, test_data_file):
    # use the tests/data/data_repository folder for it
    folder = test_data_folder('data_repository')

    # create a DataRepository instance
    data_repo = DataRepository(folder)

    # get the dict from the file
    loader_dict = data_repo.load_dict_from_name('test_document_loading')

    # it should be the following dict now;
    # by the way: this dict is supposed to be used
    # with e.g. DataModel().instance_from_dict(loader_dict)
    # to be used to instantiate a new DataModel, thus loading
    # the data!
    should_be = {
        'visible': True,
        'fixed field': 'abc',
        'very fixed': 'def',
        'optionally added': 9
    }
    assert loader_dict == should_be


def test_save_data_model_to_file(test_data_folder):
    # use the tests/data/data_repository folder for it
    folder = test_data_folder('data_repository')

    # create a DataRepository instance
    data_repo = DataRepository(folder)

    # and also a DataModel with some test stuff
    data_model = DataModel()
    data_model.define_fixed_field_type('str', str, str)
    data_model.add_field_descriptor('user', 'str', 'manu')
    data_model.set_fixed('user', 'manuel')

    # save this to the file
    data_repo.save(data_model, 'test_document_saving')

    # now load it again onto a new variable
    data_repo.load_dict_from_name('test_document_saving')
    loader_dict = data_repo.load_dict_from_name('test_document_saving')
    # for that "reset" the changed values, so that they should be
    # filled again on the loading process correctly
    data_model.set_fixed('user', '')
    assert data_model.get_fixed('user', True) == ''
    data_model.from_dict(loader_dict)

    # hopefully the loaded vlaues are correct now
    assert data_model.get_fixed('user', True) == 'manuel'
