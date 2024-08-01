'''
FieldTypeConverter class

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
'''


from typing import Any, Callable


class FieldTypeConverter:
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
        to_internal: Callable,
        internal_default: object,
        to_readable: Callable,
        readable_default: object = None,
    ):
        '''
        This class describes a field with its type, default value,
        and a function to convert a string to the appropriate type.

        Args:
            field_type_str (str): \
                Basically the Python tyoe or Python class \
                as a string so that this can be used as a string \
                in the YAML for the data object later.
            to_internal (Callable): \
                The callable with which the fields type gets \
                converted from readbale to internal type.
            internal_default (object): \
                The default for the internal value.
            to_readable (Callable): \
                The callable with which the fields data gets \
                converted to readbale from internal.
            readbale_default (object): \
                The default for the readbale value. Can be left blank \
                so that the internal_default value will be used.
        '''
        self.field_type_str = field_type_str
        self.to_internal = to_internal
        self.internal_default = internal_default
        self.to_readable = to_readable
        self.readable_default = (
            readable_default if readable_default else internal_default
        )

    def __str__(self):
        '''
        Simply represent this class as it's field type string.
        '''
        return self.field_type_str

    def convert_to_internal(self, value: Any) -> Any:
        '''
        Convert the "readable" value to the appropriate type.

        Args:
            value (Any): Any value to convert.
        '''
        if value is None:
            return self.get_internal_default()
        else:
            return self.to_internal(value)

    def convert_to_readable(self, value: Any) -> Any:
        '''
        Convert the type to a "readbale" value.

        Args:
            value (Any): Any value to convert.
        '''
        if value is None:
            return self.get_readable_default()
        else:
            return self.to_readable(value)

    def get_internal_default(self) -> object:
        '''
        Get the internal default.

        Returns:
            object: Returns the internal default.
        '''
        return self.internal_default

    def get_readable_default(self) -> object:
        '''
        Get the readable default.

        Returns:
            object: Returns the readable default.
        '''
        return self.readable_default