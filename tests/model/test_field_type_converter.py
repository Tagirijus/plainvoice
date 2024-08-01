from plainvoice.model.field.field_type_converter import FieldTypeConverter


def test_converting():
    # prepare some variables to test with
    field_type_converter = FieldTypeConverter('int', int, str)

    # the FieldTypeConverter should use the str to convert to
    # int for the internal type
    to_internal = field_type_converter.convert_to_internal('1')
    assert to_internal == 1

    # vice verse the FieldTypeConverter should use the int to
    # convert to int for the readable type
    to_readable = field_type_converter.convert_to_readable(to_internal)
    assert to_readable == '1'
