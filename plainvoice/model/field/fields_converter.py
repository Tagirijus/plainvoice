'''
FieldsConverter class

This class basically mainly just "executes", what the FieldDescriptor
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


from plainvoice.model.field.field_descriptor import FieldDescriptor


class FieldsConverter:
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

        The principle is to fill the type_to_* with FieldDescriptors,
        which later will be used in an additional initializing step
        to generate the name_to_* dicts with correct callable.

        Then it is possible to get a dict to convert, which should have
        keys, which exists in the name_to_* dicts (I call them "field names")
        and then use the callable on the value of such a dict to convert
        the variable (useing name_to_converter). Or use the default on
        name_to_default if the variable on that dict is None or if it
        does not even exist in the dict.
        '''
        self.name_to_from_converter = {}
        '''
        Callable converters (from YAML) on the field names as the key.
        '''

        self.name_to_default = {}
        '''
        The defaults for the respecting type with the
        field name as the key.
        '''

        self.name_to_to_converter = {}
        '''
        Callable converters (to YAML) on the field name as the key.
        '''

        self.type_to_from_converter = {}
        '''
        Callable converters (from YAML) on the type names as the key.
        '''

        self.type_to_default = {}
        '''
        The defaults for the respecting type with the
        type name as the key.
        '''

        self.type_to_to_converter = {}
        '''
        Callable converters (to YAML) on the type names as the key.
        '''

        self.user_descriptor = {}
        '''
        The dict, which the user can, for example, set up in the
        YAML later. It will describe the types with the field name
        as the key and the type name as a string as its value.
        '''

    def add_field(self, field_descriptor: FieldDescriptor) -> None:
        '''
        Add a FieldDescriptor to the internal type_to_* dicts,
        which will be used to initialize the name_to_* dicts
        later.

        Args:
            field (FieldDescriptor): \
            A FieldDescriptor, able to convert the given input \
            to the respecting type.
        '''
        field_type_str = str(field_descriptor)
        default_value = field_descriptor.get_default()
        converter_from = field_descriptor.converter_from
        converter_to = field_descriptor.converter_to

        self.type_to_from_converter[field_type_str] = converter_from
        self.type_to_to_converter[field_type_str] = converter_to
        self.type_to_default[field_type_str] = default_value

    def convert_from(self, data: dict) -> dict:
        '''
        Converts the given dict from the YAML and outputs it
        with the correctly converted types on the keys values.

        Args:
            data (dict): The input data dict.

        Returns:
            dict: Returns the converted dict.
        '''
        output = {}
        field_names_not_existing = list(self.user_descriptor.keys())
        for field_name in data:
            value = data[field_name]
            if (
                field_name in self.name_to_from_converter
                and field_name in self.name_to_default
            ):
                field_names_not_existing.remove(field_name)
                converter = self.name_to_from_converter[field_name]
                default = self.name_to_default[field_name]
                if value is None:
                    output[field_name] = default
                else:
                    output[field_name] = converter(value)
        output.update(
            self.fill_missing_field_names(field_names_not_existing)
        )
        return output

    def convert_to(self, data: dict) -> dict:
        '''
        Converts the given dict to the 'human readbale' dict
        to store in the YAML later.

        Args:
            data (dict): The input data dict.

        Returns:
            dict: Returns the converted dict.
        '''
        output = {}
        field_names_not_existing = list(self.user_descriptor.keys())
        for field_name in data:
            value = data[field_name]
            if field_name in self.name_to_to_converter:
                field_names_not_existing.remove(field_name)
                converter = self.name_to_to_converter[field_name]
                output[field_name] = converter(value)
        output.update(
            self.fill_missing_field_names(field_names_not_existing)
        )
        return output

    def fill_missing_field_names(self, missing_field_names: list) -> dict:
        '''
        Gets a list with missing field names and outputs the defaults
        accordingly to the internal defaults dict.

        Args:
            missing_field_names (list): List with missing field names.

        Returns:
            dict: Returns a dict with the missing fields and their defaults.
        '''
        output = {}
        for missing_field in missing_field_names:
            if missing_field in self.name_to_default:
                output[missing_field] = self.name_to_default[missing_field]
        return output

    def set_descriptor(self, descriptor: dict) -> None:
        '''
        Set the internal descriptor dict. It should be something
        like this:

        {
            'field_a': 'str',
            'field_b': 'int'
        }

        Args:
            descriptor (dict): The descriptor dict.
        '''
        self.user_descriptor = descriptor
        for field_name in self.user_descriptor:
            type_name = self.user_descriptor[field_name]
            if (
                type_name in self.type_to_from_converter
                and type_name in self.type_to_default
            ):
                self.name_to_from_converter[field_name] = \
                    self.type_to_from_converter[type_name]
                self.name_to_to_converter[field_name] = \
                    self.type_to_to_converter[type_name]
                self.name_to_default[field_name] = \
                    self.type_to_default[type_name]
