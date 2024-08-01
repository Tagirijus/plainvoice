from plainvoice.model.field.field_conversion_manager \
    import FieldConversionManager

from decimal import Decimal


def test_convert_dict():
    # prepare some variables to test with
    # I create a FieldConversionManager instance and add
    # some FieldTypeConverter instances to it
    field_conversion_manager = FieldConversionManager()
    field_conversion_manager.add_field_type('str', str, str)
    field_conversion_manager.add_field_type('int', int, int)
    field_conversion_manager.add_field_type(
        'Decimal',
        lambda x: Decimal(str(x)),
        lambda x: float(x)
    )

    # then add to the descriptor to describe the fields and their
    # wanted types and assign it to the FieldConversionManager
    field_conversion_manager.add_field_descriptor(
        'user', 'str', ''
    )
    field_conversion_manager.add_field_descriptor(
        'age', 'int', 0
    )
    field_conversion_manager.add_field_descriptor(
        'height', 'Decimal', 0.0
    )

    # here I define some test data, which could be the content
    # of a YAML later, for example
    readable_data = {
        'user': 'Manuel',
        'height': 1.87
    }

    # testing the conversion to internal for a whole dict
    internal_data = field_conversion_manager.convert_dict_to_internal(
        readable_data
    )
    assert internal_data == {
        'user': 'Manuel',
        'age': 0,
        'height': Decimal('1.87')
    }

    # I change some value and then
    # testing the conversion back to readable whole dict
    internal_data['height'] = Decimal('1.92')
    back_to_readable_data = field_conversion_manager.convert_dict_to_readable(
        internal_data
    )
    assert back_to_readable_data == {
        'user': 'Manuel',
        'age': 0,
        'height': 1.92
    }


def test_convert_field():
    # again I am instantiating a FieldConversionManager
    # with just one FieldTypeConverter
    field_conversion_manager = FieldConversionManager()
    field_conversion_manager.add_field_type('int', int, str)

    # then create the descriptor to describe the fields and their
    # wanted types and assign it to the FieldConversionManager
    # this time with defining the descriptor manually, to test
    # the .set_descriptor() method as well
    descriptor = {
        'age': {
            'type': 'int',
            'default': 0
        }
    }
    field_conversion_manager.set_descriptor(descriptor)

    # here I define some test data, which could be the content
    # of a YAML later, for example
    readable_data = {
        'age': '1'
    }

    # testing the conversion to internal for a single field
    internal_data = field_conversion_manager.convert_field_to_internal(
        'age',
        readable_data
    )
    assert internal_data == 1

    # then I change some data and then
    # testing the conversion to readable for a single field
    new_data = {
        'age': internal_data
    }
    back_to_readable_data = field_conversion_manager.convert_field_to_readable(
        'age',
        new_data
    )
    assert back_to_readable_data == '1'


def test_default():
    # prepare some variables to test with
    # I create a FieldConversionManager instance and add
    # a FieldTypeConverter instances to it
    field_conversion_manager = FieldConversionManager()
    field_conversion_manager.add_field_type('str', str, str)

    # then append the descriptor with a field and a default
    field_conversion_manager.add_field_descriptor(
        'user', 'str', 'manu'
    )

    # the field now should exist and already have the default,
    # even with an empty dict to convert given
    internal_data = field_conversion_manager.convert_field_to_internal(
        'user', {}
    )
    assert internal_data == 'manu'
