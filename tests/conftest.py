import pytest
import os


@pytest.fixture
def set_test_data_dir_for_doc_repo():
    '''
    With this method, I can modify the given document
    repository to have the string "{test_data_dir}"
    replaced with the actual test data folder.
    '''
    def _test_data_file(doc_repo, subfolders: str = ''):
        doc_repo.file.set_folder(
            doc_repo.file.get_folder().replace(
                '{test_data_dir}',
                os.path.join(
                    os.path.dirname(__file__),
                    'data',
                    subfolders
                )
            )
        )

    return _test_data_file


@pytest.fixture
def test_data_file():
    '''
    This fixture method for pytest returns a callable,
    which is a method, which can return the absolute
    path of the given filename, which should be inside
    the test data folder.
    '''
    base_dir = os.path.dirname(__file__)
    data_dir = os.path.join(base_dir, 'data')

    def _test_data_file(filename: str = ''):
        return os.path.join(data_dir, filename)

    return _test_data_file


@pytest.fixture
def test_data_folder():
    '''
    This fixture method for pytest returns the data folder and
    optionally another folder inside it as a path string.
    '''
    base_dir = os.path.dirname(__file__)

    def _test_data_folder(relative_folder: str = ''):
        return os.path.join(base_dir, 'data', relative_folder)

    return _test_data_folder


@pytest.fixture
def test_temp_file():
    '''
    This fixture creates a temporary file to work with inside the tests
    and removes it afterward. The content and filename can be set by
    calling the fixture within the test function.

    The file will be created temporarily inside the test/data folder.
    '''
    created_files = []

    def _create_temp_file(
        filename='_pytest_temp_file.txt',
        content='pytest is testing ...'
    ):
        base_dir = os.path.dirname(__file__)
        data_dir = os.path.join(base_dir, 'data')
        filepath = os.path.join(data_dir, filename)

        with open(filepath, 'w') as f:
            f.write(content)

        created_files.append(filepath)
        return filepath

    yield _create_temp_file

    # Cleanup after the test
    for filepath in created_files:
        if os.path.exists(filepath):
            os.remove(filepath)
