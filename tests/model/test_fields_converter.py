from plainvoice.model.field.fields_converter import FieldsConverter
from plainvoice.model.field.field_descriptor import FieldDescriptor

from decimal import Decimal


def test_convert_dict():
    fields_converter = FieldsConverter()
    fields_converter.add_field(FieldDescriptor('str', '', str, str))
    fields_converter.add_field(FieldDescriptor('int', 0, int, int))
    fields_converter.add_field(FieldDescriptor(
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

    fields_converter.set_descriptor(descriptor)

    converted = fields_converter.convert_dict_from(data)

    assert converted == {
        'user': 'Manuel',
        'age': 0,
        'height': Decimal('1.87')
    }

    converted['height'] = Decimal('1.92')
    back_converted = fields_converter.convert_dict_to(converted)

    assert back_converted == {
        'user': 'Manuel',
        'age': 0,
        'height': 1.92
    }


def test_convert_field():
    fields_converter = FieldsConverter()
    fields_converter.add_field(FieldDescriptor('int', 9, int, str))

    descriptor = {
        'age': 'int'
    }

    data = {
        'age': '1'
    }

    fields_converter.set_descriptor(descriptor)

    converted = fields_converter.convert_field_from('age', data)

    assert converted == 1

    new_data = {
        'age': converted
    }

    back_converted = fields_converter.convert_field_to('age', data)

    assert back_converted == '1'
