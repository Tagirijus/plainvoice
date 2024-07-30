from plainvoice.model.base.base_model import BaseModel


def test_create_instance():
    base_model = BaseModel('filename.yaml')
    new_base_model = base_model.create_instance('new_filename.yaml')
    assert isinstance(new_base_model, BaseModel)
    assert new_base_model.get_filename() == 'new_filename.yaml'


def test_from_dict():
    base_model = BaseModel('filename.yaml')
    loader = {
        'filename': 'loaded_filename.yaml',
        'visible': False
    }
    base_model.from_dict(loader)
    assert base_model.get_filename() == 'loaded_filename.yaml'
    assert base_model.is_visible() is False


def test_getter_setter():
    base_model = BaseModel('filename.yaml')
    assert base_model.get_filename() == 'filename.yaml'
    assert base_model.is_visible() is True
    base_model.set_filename('new_filename.yaml')
    assert base_model.get_filename() == 'new_filename.yaml'
    base_model.hide()
    assert base_model.is_visible() is False


def test_to_dict():
    base_model = BaseModel('filename.yaml')
    base_model.hide()
    saver = base_model.to_dict()
    assert saver.get('visible') is False
