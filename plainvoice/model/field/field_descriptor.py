'''
FieldDescriptor class

With this class I want be able to define a data type. The idea is
to have a describing dict in a YAML later (created by the user)
which will describe needed fields for a certain document type.
This shall be done with pure strings, describing the data type
to a given field name (basically a dict key). This describing
dict can look like this:

{
    'username': 'str',
    'age': 'int'
}

This class holds the information on how to convert to and from
the YAML format.

The reason for this is: if I use a Decimal or any other class I
come up with, I do not want the YAML to save this Python object
into the file. For Decimals I want to keep it human readable in
the YAML file; like:

    amount: 1.5

Instead of

    amount: <python.object.Decimal> ...

Or however this could look like. Thus I need some kind of
converter, which will know on which field name (key) which type
of data exists and how to convert it in both directions.


INFO:
I maybe should have renamed the attributes to something like
converter_from_readable and converter_to_readbale to make
clear that it basically is just about conversion between
some kind of "more readable" type, used in the YAML later.
Yet names get longer and longer, argh ...
'''


from typing import Any, Callable


class FieldDescriptor:
    '''
    This class describes a field with its type, default value,
    and functions to convert a string to the appropriate type,
    or back to the wanted readable type (e.g. if I want to have
    Decimal being represented as a float in the YAML for better
    readability in the file).
    '''

    def __init__(
        self,
        field_type_str: str,
        default_value: Any,
        converter_from: Callable,
        converter_to: Callable
    ):
        '''
        This class describes a field with its type, default value,
        and a function to convert a string to the appropriate type.

        Args:
            field_type_str (str): \
                Basically the Python tyoe or Python class \
                as a string so that this can be used as a string \
                in the YAML for the data object later.
            default_value (Any): \
                The default value for this field, if the user \
                did not input anything yet.
            converter_from (Callable): \
                The callable with which the fields type gets \
                initialized from the given readbale variable later.
            converter_to (Callable): \
                The callable with which the fields data gets \
                converted to readbale variables later.
        '''
        self.field_type_str = field_type_str
        self.default_value = default_value
        self.converter_from = converter_from
        self.converter_to = converter_to

    def __str__(self):
        '''
        Simply represent this class as it's field type string.
        '''
        return self.field_type_str

    def convert_from(self, value: Any) -> Any:
        '''
        Convert the "readable" value to the appropriate type.
        '''
        return self.converter_from(value)

    def convert_to(self, value: str) -> Any:
        '''
        Convert the type to a "readbale" value.
        '''
        return self.converter_to(value)

    def get_default(self) -> Any:
        '''
        Get the default of this field.

        Returns:
            Any: Returns the default in its type.
        '''
        return self.default_value
