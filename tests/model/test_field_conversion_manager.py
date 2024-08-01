from plainvoice.model.field.field_conversion_manager \
    import FieldConversionManager

from decimal import Decimal


def test_convert_dict():
    # prepare some variables to test with
    # I create a FieldConversionManager instance and add
    # some FieldTypeConverter instances to it
    field_conversion_manager = FieldConversionManager()
    field_conversion_manager.add_field_type('str', str, '', str)
    field_conversion_manager.add_field_type('int', int, 0, int)
    field_conversion_manager.add_field_type(
        'Decimal',
        lambda x: Decimal(str(x)),
        Decimal(0),
        lambda x: float(x)
    )

    # then create the descriptor to describe the fields and their
    # wanted types and assign it to the FieldConversionManager
    descriptor = {
        'user': 'str',
        'age': 'int',
        'height': 'Decimal'
    }
    field_conversion_manager.set_descriptor(descriptor)

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
    field_conversion_manager.add_field_type(
        'int', int, 9, str, '9'
    )

    # then create the descriptor to describe the fields and their
    # wanted types and assign it to the FieldConversionManager
    descriptor = {
        'age': 'int'
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

    # tehn I change some data and then
    # testing the conversion to readable for a single field
    new_data = {
        'age': internal_data
    }
    back_to_readable_data = field_conversion_manager.convert_field_to_readable(
        'age',
        new_data
    )
    assert back_to_readable_data == '1'
