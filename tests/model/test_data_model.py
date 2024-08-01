from plainvoice.model.field.field_type_converter import FieldTypeConverter
from plainvoice.model.data.data_model import DataModel


def test_additional():
    # instantiate a DataModel and set some additional field
    data_model = DataModel('filename.yaml')
    data_model.set_additional('user', 'Manu')

    # this field should be getable
    assert data_model.get_additional('user') == 'Manu'

    # then I create some test data and load it to the instance
    loader = {
        'user': 'Anna',
        'age': '32'
    }
    data_model.from_dict(loader)

    # again these new data should be getable and updated from
    # the old ones.
    assert data_model.get('user') == 'Anna'
    assert data_model.get('age') == '32'


def test_create_instance():
    # I create a new instance via typical Python code
    # yet also with the inbuilt create_instance() method
    data_model = DataModel('filename.yaml')
    new_data_model = data_model.create_instance('new_filename.yaml')

    # then I check if these are the same object types
    # and also if a variable for the create_instance()
    # created instance is correct
    assert isinstance(new_data_model, DataModel)
    assert new_data_model.get_filename() == 'new_filename.yaml'


def test_fixed():
    # I create a DataModel instance and create some fixed
    # fields, which are internally some FieldTypeConverter
    # objects added to the internal FieldConversionManager
    data_model = DataModel('filename.yaml')
    data_model.field_conversion_manager.add_field(
        FieldTypeConverter('str', str, 'empty', str)
    )
    data_model.field_conversion_manager.add_field(
        FieldTypeConverter('intstr', int, 0, str, '0')
    )
    data_model.field_conversion_manager.add_field(
        FieldTypeConverter('int', int, 0, int)
    )

    # then I create a descriptor, describing the field names
    # and their wanted type; and then I assign it to the
    # FieldConversionManager of DataModel
    descriptor = {
        'user': 'str',
        'age': 'intstr',
        'number': 'int'
    }
    data_model.field_conversion_manager.set_descriptor(descriptor)

    # here I create some testing data, which might be the content
    # of a YAML later. then I load this dict into the DataModel
    readable_data = {
        'user': 'Manu',
        'age': '36',
        'additional': 'something'
    }
    data_model.from_dict(readable_data)

    # the fixed fields should now be the respecing data types
    # according to the FieldTypeConverter settings above
    assert data_model.get_fixed('age', False) == 36
    assert data_model.get_fixed('age', True) == '36'
    assert data_model.get_fixed('number', False) == 0
    assert data_model.get_fixed('number', True) == 0


def test_from_dict():
    # again I create a DataModel instance and testing
    # data to load from
    data_model = DataModel('filename.yaml')
    readable_data = {
        'filename': 'loaded_filename.yaml',
        'visible': False
    }
    data_model.from_dict(readable_data)

    # the base data should be set correctly
    assert data_model.get_filename() == 'loaded_filename.yaml'
    assert data_model.is_visible() is False


def test_getter_setter():
    # here I create a DataModel instance
    # and test directly the getter for the base
    # attributes
    data_model = DataModel('filename.yaml')
    assert data_model.get_filename() == 'filename.yaml'
    assert data_model.is_visible() is True

    # then I test the setter accordingly and at the same
    # time the getter again
    data_model.set_filename('new_filename.yaml')
    assert data_model.get_filename() == 'new_filename.yaml'
    data_model.hide()
    assert data_model.is_visible() is False
    data_model.show()
    assert data_model.is_visible() is True


def test_to_dict():
    # here I create a DataModel instance,
    # hide it (using the setter for visible)
    # and test if the value was set correctly
    # by checking the converted dict this time
    data_model = DataModel('filename.yaml')
    data_model.hide()
    saver = data_model.to_dict()
    assert saver.get('visible') is False
