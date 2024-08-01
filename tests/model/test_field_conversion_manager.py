from plainvoice.model.field.field_conversion_manager \
    import FieldConversionManager
from plainvoice.model.field.field_type_converter import FieldTypeConverter

from decimal import Decimal


def test_convert_dict():
    field_conversion_manager = FieldConversionManager()
    field_conversion_manager.add_field(FieldTypeConverter('str', '', str, str))
    field_conversion_manager.add_field(FieldTypeConverter('int', 0, int, int))
    field_conversion_manager.add_field(FieldTypeConverter(
        'Decimal',
        Decimal(0),
        lambda x: Decimal(str(x)),
        lambda x: float(x))
    )

    descriptor = {
        'user': 'str',
        'age': 'int',
        'height': 'Decimal'
    }

    data = {
        'user': 'Manuel',
        'height': 1.87
    }

    field_conversion_manager.set_descriptor(descriptor)

    converted = field_conversion_manager.convert_dict_to_internal(data)

    assert converted == {
        'user': 'Manuel',
        'age': 0,
        'height': Decimal('1.87')
    }

    converted['height'] = Decimal('1.92')
    back_converted = field_conversion_manager.convert_dict_to_readable(
        converted
    )

    assert back_converted == {
        'user': 'Manuel',
        'age': 0,
        'height': 1.92
    }


def test_convert_field():
    field_conversion_manager = FieldConversionManager()
    field_conversion_manager.add_field(FieldTypeConverter('int', 9, int, str))

    descriptor = {
        'age': 'int'
    }

    data = {
        'age': '1'
    }

    field_conversion_manager.set_descriptor(descriptor)

    converted = field_conversion_manager.convert_field_to_internal('age', data)

    assert converted == 1

    new_data = {
        'age': converted
    }

    back_converted = field_conversion_manager.convert_field_to_readbale(
        'age',
        new_data
    )

    assert back_converted == '1'
