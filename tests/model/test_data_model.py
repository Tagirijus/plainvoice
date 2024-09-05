from plainvoice.model.data.data_model import DataModel


def test_additional():
    # instantiate a DataModel and set some additional field
    data_model = DataModel()
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

    # a not-set additional should return None
    assert data_model.get('does_not_exist') is None


def test_create_instance():
    # I create a new instance via typical Python code
    # yet also with the inbuilt create_instance() method
    data_model = DataModel()
    new_data_model = data_model.create_instance()
    new_data_model.hide()

    # then I check if these are the same object types
    # and check the changed attribute as well
    assert isinstance(new_data_model, DataModel)
    assert new_data_model.is_visible() is False


def test_default_in_fixed():
    # I create a DataModel instance and create some fixed
    # fields
    data_model = DataModel()
    data_model.define_fixed_field_type('str', str, str)
    data_model.add_field_descriptor('user', 'str', 'default')

    # now I want to test, if this field already got filled
    # with the default
    assert data_model.get_fixed('user') == 'default'

    # but when I set it manually to None, it should stay that way
    data_model.set_fixed('user', None, False)
    assert data_model.get_fixed('user') is None


def test_fixed():
    # I create a DataModel instance and create some fixed
    # fields, which are internally some FieldTypeConverter
    # objects added to the internal FieldConversionManager
    data_model = DataModel()
    data_model.define_fixed_field_type('str', str, str)
    data_model.define_fixed_field_type('intstr', int, str)
    data_model.define_fixed_field_type('int', int, int)

    # then I extend the descriptor, describing the field names
    # and their wanted type and defaults
    data_model.add_field_descriptor('user', 'str', '')
    data_model.add_field_descriptor('age', 'intstr', '0')
    data_model.add_field_descriptor('number', 'int', 0)
    data_model.add_field_descriptor('default', 'str', 'def')

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
    # also check, just in case, if the default got added
    # as well, despite the fact that the key was not in
    # the readable_data dict
    assert data_model.get_fixed('default', True) == 'def'

    # also test the setter
    # if the field does not exist at all, do not set the
    # field, thus return None on getting
    data_model.set_fixed('not_existing', True)
    assert data_model.get_fixed('not_existing') is None
    # now set an existing field
    data_model.set_fixed('age', '30', True)
    assert data_model.get_fixed('age', False) == 30
    # also try to set it with its internal value
    data_model.set_fixed('number', 99, False)
    assert data_model.get_fixed('number', False) == 99


def test_from_dict():
    # again I create a DataModel instance and testing
    # data to load from
    data_model = DataModel()
    readable_data = {
        'visible': False
    }
    data_model.from_dict(readable_data)

    # the base data should be set correctly
    assert data_model.is_visible() is False


def test_getter_setter():
    # here I create a DataModel instance
    # and test directly the getter for the base
    # attributes
    data_model = DataModel()
    assert data_model.is_visible() is True

    # then I test the setter accordingly and at the same
    # time the getter again
    data_model.hide()
    assert data_model.is_visible() is False
    data_model.show()
    assert data_model.is_visible() is True


def test_to_dict():
    # here I create a DataModel instance,
    # hide it (using the setter for visible)
    # and test if the value was set correctly
    # by checking the converted dict this time
    data_model = DataModel()
    data_model.hide()
    saver = data_model.to_dict()
    assert saver.get('visible') is False


def test_to_yaml_string_all():
    # preapre the DataModel instance
    data_model = DataModel()
    # define a fiexed field "fixed" with the default
    # "nothing" so that without setting it with the
    # setter, it still should appear in the YAML later
    data_model.define_fixed_field_type('str', str, str)
    data_model.add_field_descriptor('fixed', 'str', 'nothing')
    # also set an additional field to the additional
    data_model.set_additional('testing', 'manu\nanna\nluna')
    # now hide it so that a base variable also gets modified
    data_model.hide()
    # converty McConvert
    out_string = data_model.to_yaml_string()

    # the output string should be the correct YAML string
    # I am aiming for
    assert out_string == '''
# base variables

visible: false


# fixed fields

fixed: nothing


# additional fields

testing: |-
  manu
  anna
  luna
'''.strip()


def test_to_yaml_string_only_base():
    # preapre the DataModel instance
    data_model = DataModel()
    # change base attribute
    data_model.hide()
    # converty McConvert
    out_string = data_model.to_yaml_string()

    # the output string should be the correct YAML string
    # I am aiming for
    assert out_string == '''# base variables

visible: false
'''.strip()
