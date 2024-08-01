from plainvoice.model.field.field_type_converter import FieldTypeConverter
from plainvoice.model.data.data_model import DataModel


def test_additional():
    data_model = DataModel('filename.yaml')
    data_model.set_additional('user', 'Manu')
    assert data_model.get_additional('user') == 'Manu'
    loader = {
        'user': 'Anna',
        'age': '32'
    }
    data_model.from_dict(loader)
    assert data_model.get('user') == 'Anna'
    assert data_model.get('age') == '32'


def test_create_instance():
    data_model = DataModel('filename.yaml')
    new_data_model = data_model.create_instance('new_filename.yaml')
    assert isinstance(new_data_model, DataModel)
    assert new_data_model.get_filename() == 'new_filename.yaml'


def test_fixed():
    data_model = DataModel('filename.yaml')
    data_model.field_conversion_manager.add_field(
        FieldTypeConverter('str', str, str),
        'empty'
    )
    data_model.field_conversion_manager.add_field(
        FieldTypeConverter('intstr', int, str),
        0
    )
    data_model.field_conversion_manager.add_field(
        FieldTypeConverter('int', int, int),
        0
    )
    descriptor = {
        'user': 'str',
        'age': 'intstr',
        'number': 'int'
    }
    data_model.field_conversion_manager.set_descriptor(descriptor)

    readable_data = {
        'user': 'Manu',
        'age': '36',
        'additional': 'something'
    }

    data_model.from_dict(readable_data)
    assert data_model.get_fixed('age', False) == 36
    assert data_model.get_fixed('age', True) == '36'
    assert data_model.get_fixed('number', False) == 0
    assert data_model.get_fixed('number', True) == 0


def test_from_dict():
    data_model = DataModel('filename.yaml')
    loader = {
        'filename': 'loaded_filename.yaml',
        'visible': False
    }
    data_model.from_dict(loader)
    assert data_model.get_filename() == 'loaded_filename.yaml'
    assert data_model.is_visible() is False


def test_getter_setter():
    data_model = DataModel('filename.yaml')
    assert data_model.get_filename() == 'filename.yaml'
    assert data_model.is_visible() is True
    data_model.set_filename('new_filename.yaml')
    assert data_model.get_filename() == 'new_filename.yaml'
    data_model.hide()
    assert data_model.is_visible() is False


def test_to_dict():
    data_model = DataModel('filename.yaml')
    data_model.hide()
    saver = data_model.to_dict()
    assert saver.get('visible') is False
