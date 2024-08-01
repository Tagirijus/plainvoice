'''
FieldConversionManager class

This class basically mainly just "executes", what the FieldTypeConverter
describes. With this class you can set up fields for a data object
later and then convert the fields to the human readable type to store
in the YAML or convert it back from it.

It is also for filling missing fields. E.g. if the user did not enter
some field, yet the descriptor knows this field. Then it will just
added to the dict with its defined default value.

TODO: Maybe I could make the default-value-adding process optional
with a class attribute. Just in case that I, at some point, to not
want that "empty fields" will still be added. Yet in the human readable
YAML feil later the idea is to see what kind of fields are supposed
to exist for a certain document type, for example. E.g. an invoice
is supposed to have a postings list.
'''


from plainvoice.model.field.field_type_converter import FieldTypeConverter

from typing import Callable


class FieldConversionManager:
    '''
    This class will handle the described fields and their types
    and is able to convert a given dict, which has such fields
    as keys, to the correct type. It could be like this:

    The dict format to describe a field:

    {
        'name_of_field': 'type_of_field'
    }

    e.g.:

    {
        'username': 'str',
        'age': 'Decimal',
        'number': 'int'
    }

    Then you can convert this dict:

    {
        'username': 'Manuel',
        'age': '35',
        'number': '9'
    }

    To a "converted" dict later:

    {
        'username': 'Manuel',
        'age': Decimal(35),
        'number': 9
    }

    It is supposed to go the oher way around as well, in case I want
    to store the data "back to the YAML file".
    '''

    def __init__(self):
        '''
        Create an instance of this class with the given fields,
        which should describe the fields.

        The principle is to fill the type_to_* with FieldTypeConverters,
        which later will be used in an additional initializing step
        to generate the name_to_* dicts with correct callable.

        Then it is possible to get a dict to convert, which should have
        keys, which exists in the name_to_* dicts (I call them "field names")
        and then use the callable on the value of such a dict to convert
        the variable (useing name_to_converter). Or use the default on
        name_to_default if the variable on that dict is None or if it
        does not even exist in the dict.
        '''
        self.name_to_field_type_converter: dict[str, FieldTypeConverter] = {}
        '''
        The dict with field names as key and the respecting FieldTypeConverter
        as value.
        '''

        self.type_to_field_type_converter: dict[str, FieldTypeConverter] = {}
        '''
        The dict with type names as key and the respecting FieldTypeConverter
        as value.
        '''

        self.user_descriptor = {}
        '''
        The dict, which the user can, for example, set up in the
        YAML later. It will describe the types with the field name
        as the key and the type name as a string as its value.
        '''

    def add_field_type(
        self,
        field_type_str: str,
        to_internal: Callable,
        internal_default: object,
        to_readable: Callable,
        readable_default: object = None,
    ) -> None:
        '''
        Basically this method will instantiate a new FieldTypeConverter
        with the given values and add it to the internal dict
        accordingly.

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
        field_type_converter = FieldTypeConverter(
            field_type_str,
            to_internal,
            internal_default,
            to_readable,
            readable_default
        )
        field_type_str = str(field_type_converter)

        self.type_to_field_type_converter[field_type_str] = \
            field_type_converter

    def convert_dict(self, data: dict, to_internal: bool = True) -> dict:
        '''
        Converts the given dict to either to the readbale type
        or the internal type.

        Args:
            data (dict): The input data dict.
            to_internal (bool): Converts to internal if True.

        Returns:
            dict: Returns the converted dict.
        '''
        output = {}
        field_names_not_existing = list(self.user_descriptor.keys())
        for field_name in data:
            value = data[field_name]
            if field_name in self.name_to_field_type_converter:
                field_names_not_existing.remove(field_name)
                field_type_converter = \
                    self.name_to_field_type_converter[field_name]
                if to_internal:
                    output[field_name] = (
                        field_type_converter.convert_to_internal(value)
                    )
                else:
                    output[field_name] = (
                        field_type_converter.convert_to_readable(value)
                    )
        output.update(
            self.fill_missing_field_names(field_names_not_existing)
        )
        return output

    def convert_dict_to_internal(self, data: dict) -> dict:
        '''
        Converts the given dict to the internal format.

        Args:
            data (dict): The input data dict.

        Returns:
            dict: Returns the converted dict.
        '''
        return self.convert_dict(data, True)

    def convert_dict_to_readable(self, data: dict) -> dict:
        '''
        Converts the given dict to the readable format.

        Args:
            data (dict): The input data dict.

        Returns:
            dict: Returns the converted dict.
        '''
        return self.convert_dict(data, False)

    def convert_field(
        self,
        fieldname: str,
        data: dict,
        to_internal: bool = True
    ) -> object:
        '''
        Convert just the given fieldname with the given data to either
        the internal or readable format.

        Args:
            fieldname (str): \
                The field name.
            data (dict): \
                The dict, which should contain the value to
                convert on the key, set by fieldname.
            to_internal (bool): \
                Converts to internal if True.

        Returns:
            object: Returns the raw object format for the given data.
        '''
        if (
            fieldname in data
            and fieldname in self.name_to_field_type_converter
        ):
            field_type_converter = self.name_to_field_type_converter[fieldname]
            if to_internal:
                return field_type_converter.convert_to_internal(
                    data[fieldname]
                )
            else:
                return field_type_converter.convert_to_readable(
                    data[fieldname]
                )
        else:
            return None

    def convert_field_to_internal(self, fieldname: str, data: dict) -> object:
        '''
        Convert just the given fieldname with the given data to the
        internal format.

        Args:
            fieldname (str): \
                The field name.
            data (dict): \
                The dict, which should contain the value to
                convert on the key, set by fieldname.

        Returns:
            object: Returns the raw object format for the given data.
        '''
        return self.convert_field(fieldname, data, True)

    def convert_field_to_readable(self, fieldname: str, data: dict) -> object:
        '''
        Convert just the given fieldname with the given data to the
        readable format.

        Args:
            fieldname (str): \
                The field name.
            data (dict): \
                The dict, which should contain the value to
                convert on the key, set by fieldname.

        Returns:
            object: Returns the raw object format for the given data.
        '''
        return self.convert_field(fieldname, data, False)

    def fill_missing_field_names(
        self,
        missing_field_names: list,
        to_internal: bool = True
    ) -> dict:
        '''
        Gets a list with missing field names and outputs the defaults
        accordingly to the internal defaults dict.

        Args:
            missing_field_names (list): List with missing field names.
            to_internal (bool): Converts to internal if True.

        Returns:
            dict: Returns a dict with the missing fields and their defaults.
        '''
        output = {}
        for missing_field in missing_field_names:
            if missing_field in self.name_to_field_type_converter:
                field_type_converter = \
                    self.name_to_field_type_converter[missing_field]
                if to_internal:
                    output[missing_field] = \
                        field_type_converter.get_internal_default()
                else:
                    output[missing_field] = \
                        field_type_converter.get_readable_default()
        return output

    def get_fieldnames(self) -> list:
        '''
        Get the fieldnames, which were defined by the given
        descriptor dict (its keys).

        Returns:
            list: Returns the fieldnames as a list.
        '''
        return list(self.user_descriptor.keys())

    def set_descriptor(self, descriptor: dict) -> None:
        '''
        Set the internal descriptor dict. It should be something
        like this:

        {
            'field_a': 'str',
            'field_b': 'int'
        }

        And then initialize the internal variables. Basically what
        it does is assigning the existing FieldTypeConvert
        objects from the self.type_to_field_type_converter to the
        dict self.name_to_field_type_converter yet with the
        field names as the key instead of the type name.

        Args:
            descriptor (dict): The descriptor dict.
        '''
        self.user_descriptor = descriptor
        for field_name in self.user_descriptor:
            type_name = self.user_descriptor[field_name]
            if type_name in self.type_to_field_type_converter:
                self.name_to_field_type_converter[field_name] = \
                    self.type_to_field_type_converter[type_name]
