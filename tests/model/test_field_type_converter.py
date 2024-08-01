from plainvoice.model.field.field_type_converter import FieldTypeConverter


def test_converting():
    field_descriptor = FieldTypeConverter('str', str, int)
    from_variable = field_descriptor.convert_to_internal(1)
    assert from_variable == '1'
    to_variable = field_descriptor.convert_to_readable(from_variable)
    assert to_variable == 1
