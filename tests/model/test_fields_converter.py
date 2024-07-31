from plainvoice.model.field.fields_converter import FieldsConverter
from plainvoice.model.field.field_descriptor import FieldDescriptor

from decimal import Decimal


def test_convert():
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

    converted = fields_converter.convert_from(data)

    assert converted == {
        'user': 'Manuel',
        'age': 0,
        'height': Decimal('1.87')
    }

    converted['height'] = Decimal('1.92')
    back_converted = fields_converter.convert_to(converted)

    assert back_converted == {
        'user': 'Manuel',
        'age': 0,
        'height': 1.92
    }
