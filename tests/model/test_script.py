from plainvoice.model.data.data_model import DataModel
from plainvoice.model.script.script_repository import ScriptRepository
from plainvoice.utils import doc_utils


def test_script_loading(test_data_folder):
    # set the test data folder
    test_folder = test_data_folder('script_repository')
    scripts_folder = test_folder + '/scripts'

    # create the repo and load a script with it
    script_repo = ScriptRepository(scripts_folder)
    script = script_repo.load('a_test_script')

    # create some testing data
    data_model = DataModel()
    data_model.define_fixed_field_type('str', str, str)
    data_model.add_field_descriptor('title', 'str', 'no title')
    data_model.set_fixed('title', 'test_script set title', True)

    # the test script should just modify this DataModel's fixed field
    # 'title' to 'a_test_script set title'
    doc_repo = doc_utils.get_doc_repo()
    script.run(data_model, doc_repo.get_user_by_username())
    assert data_model.get_fixed('title', True) == 'a_test_script set title'
