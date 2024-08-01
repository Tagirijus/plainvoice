from plainvoice.model.field.field_type_converter import FieldTypeConverter


def test_converting():
    field_type_converter = FieldTypeConverter('int', int, 0, str, '0')

    to_internal = field_type_converter.convert_to_internal(1)
    assert to_internal == 1

    to_readable = field_type_converter.convert_to_readable(to_internal)
    assert to_readable == '1'
