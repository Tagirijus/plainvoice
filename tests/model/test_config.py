from plainvoice.model.config import Config


def test_config():
    '''
    Simply tests, if the config test folder is used as the data_dir.
    '''
    conf = Config()

    # just for this test I set an editor command, which does not exist;
    # during the tests I probably do not want to use an editor anyway (;
    assert conf.get('editor') == 'this_is_no_editor'
