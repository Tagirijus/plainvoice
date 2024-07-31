from plainvoice.model.field.field_descriptor import FieldDescriptor


def test_converting():
    field_descriptor = FieldDescriptor('str', '0', str, int)
    from_variable = field_descriptor.convert_from(1)
    to_variable = field_descriptor.convert_to(from_variable)
    assert to_variable == 1

def test_default():
    field_descriptor = FieldDescriptor('str', '0', str, str)
    assert field_descriptor.get_default() == '0'
