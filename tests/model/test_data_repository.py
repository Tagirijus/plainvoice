from plainvoice.model.data.data_repository import DataRepository


def test_data_repository_absolute_filename():
    # create a DataRepository instance
    data_repo = DataRepository('/some/folder')

    # check if the filename generation works correctly
    abs_filename = data_repo.get_absolute_filename('test_file')
    assert abs_filename == '/some/folder/test_file.yaml'


def test_get_files_of_data_type_Data_repository(
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
        test_data_file('data_repository/test_document_b.yaml')
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
        'test_document_b'
    ])

    # now get only the visible one
    file_list = data_repo.get_list(True)
    names = list(file_list.keys())
    assert names == [
        'test_document_a'
    ]


def test_load_data_model_from_file(test_data_folder, test_data_file):
    # use the tests/data/data_repository folder for it
    folder = test_data_folder('data_repository')

    # get a test document file
    # test_file = test_data_file('data_repository/test_document_a.yaml')

    # create a DataRepository instance
    data_repo = DataRepository(folder)

    # get the dict from the file
    loader_dict = data_repo.load_from_name('test_document_a')

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
