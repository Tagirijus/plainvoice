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
        'name_of_field': {
            'type': 'type_of_field',
            'default': 'readable_default_for_field'
        }, ...
    }

    e.g.:

    {
        'username': {
            'type': 'str',
            'default': ''
        },
        'age': {
            'type': 'Decimal',
            'default': Decimal(0)
        },
        'number': {
            'type': 'int',
            'default': 0
        }
    }

    Then you can convert this dict:

    {
        'username': 'Manuel',
        'age': '35',
        'number': None
    }

    To a "converted" dict later:

    {
        'username': 'Manuel',
        'age': Decimal(35),
        'number': 0
    }

    It is supposed to go the oher way around as well, in case I want
    to store the data "back to the YAML file". I call it internal or
    readable; thus to_internal (from YAML) or to_readable (to YAML).
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
        self.name_to_default: dict[str, object] = {}
        '''
        The dict with field names as key and the respecting readable default
        as value.
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

        self.user_descriptor: dict[str, dict[str, object]] = {}
        '''
        With this dict it is possible to describe the fields like so:
        {
            'field_name': {
                'type': 'type_of_field',
                'default': 'default_for_field'
            }
        }
        So the 'type' value should be the field_type_str of the
        FieldTypeConverter object, which should be added before.
        The 'default' is for the case, when the readable type,
        for example, has "None" / "null" and needs a default
        value. Also it is used to fill not yet set fields.
        '''

    def add_field_type(
        self,
        field_type_str: str,
        to_internal: Callable,
        to_readable: Callable
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
            to_readable (Callable): \
                The callable with which the fields data gets \
                converted to readbale from internal.
        '''
        field_type_converter = FieldTypeConverter(
            field_type_str,
            to_internal,
            to_readable
        )
        field_type_str = str(field_type_converter)

        self.type_to_field_type_converter[field_type_str] = \
            field_type_converter

    def add_field_descriptor(
        self,
        field_name: str,
        type_name: str,
        default: object,
    ) -> None:
        '''
        Add a field descriptor to the user_descriptor dict, which
        has the format {'field name': {'type': str, 'default': str}}.
        With the given parameter you basically add such a dict
        entry and have some kind of wrapper.

        Args:
            field_name (str): \
                The name for the field. It will become the dict key.
            type_name (str): \
                The string describing the field type.
            default (object): \
                Any kind of default, which should represent the \
                readable default later. So it should be a basic \
                Python object like str, int, float, list or dict.
        '''
        self.user_descriptor[field_name] = {
            'type': type_name,
            'default': default
        }
        self.name_to_default[field_name] = default
        if type_name in self.type_to_field_type_converter:
            self.name_to_field_type_converter[field_name] = \
                self.type_to_field_type_converter[type_name]

    def convert_dict(self, data: dict, readable: bool = False) -> dict:
        '''
        Converts the given dict to either to the readbale type
        or the internal type.

        Args:
            data (dict): The input data dict.
            readable (bool): Converts to readable if True.

        Returns:
            dict: Returns the converted dict.
        '''
        output = {}
        field_names_not_existing = list(self.user_descriptor.keys())
        for field_name in data:
            if field_name in self.name_to_field_type_converter:
                field_names_not_existing.remove(field_name)
                output[field_name] = self.convert_field(
                    field_name,
                    data,
                    readable
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
        return self.convert_dict(data, False)

    def convert_dict_to_readable(self, data: dict) -> dict:
        '''
        Converts the given dict to the readable format.

        Args:
            data (dict): The input data dict.

        Returns:
            dict: Returns the converted dict.
        '''
        return self.convert_dict(data, True)

    def convert_field(
        self,
        field_name: str,
        data: dict,
        readable: bool = False
    ) -> object:
        '''
        Convert just the given field_name with the given data to either
        the internal or readable format. This is basically the main
        method for the whole class mechanic, since it is used for
        the whoel dict-conversion as well.

        Args:
            field_name (str): \
                The field name.
            data (dict): \
                The dict, which should contain the value to
                convert on the key, set by field_name.
            readable (bool): \
                Converts to readable if True.

        Returns:
            object: Returns the raw object format for the given data.
        '''
        output = data.get(field_name, None)

        if field_name in self.name_to_field_type_converter:

            # convert the value
            field_type_converter = \
                self.name_to_field_type_converter[field_name]
            if readable:
                output = field_type_converter.convert_to_readable(
                    data.get(field_name)
                )
            else:
                output = field_type_converter.convert_to_internal(
                    data.get(field_name)
                )

            # if it's "None" from conversion,
            # get the fields default, yet convert it again, since
            # the default is the readable default and should also
            # be converted
            if (
                output is None
                and field_name in self.name_to_default
            ):
                output = self.name_to_default[field_name]
                if readable:
                    output = field_type_converter.convert_to_readable(
                        output
                    )
                else:
                    output = field_type_converter.convert_to_internal(
                        output
                    )

        # there is no converter (should not happen, though) and
        # the default should still be got from the defaults
        elif (
            output is None
            and field_name in self.name_to_default
        ):
            output = self.name_to_default[field_name]

        return output

    def convert_field_to_internal(self, field_name: str, data: dict) -> object:
        '''
        Convert just the given field_name with the given data to the
        internal format.

        Args:
            field_name (str): \
                The field name.
            data (dict): \
                The dict, which should contain the value to
                convert on the key, set by field_name.

        Returns:
            object: Returns the raw object format for the given data.
        '''
        return self.convert_field(field_name, data, False)

    def convert_field_to_readable(self, field_name: str, data: dict) -> object:
        '''
        Convert just the given field_name with the given data to the
        readable format.

        Args:
            field_name (str): \
                The field name.
            data (dict): \
                The dict, which should contain the value to
                convert on the key, set by field_name.

        Returns:
            object: Returns the raw object format for the given data.
        '''
        return self.convert_field(field_name, data, True)

    def fill_missing_field_names(self, missing_field_names: list) -> dict:
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
            if missing_field in self.name_to_default:
                output[missing_field] = self.name_to_default[missing_field]
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
            'username': {
                'type': 'str',
                'default': ''
            },
            'age': {
                'type': 'Decimal',
                'default': Decimal(0)
            }, ...
        }

        And then initialize the internal variables. Basically what
        it does is assigning the existing FieldTypeConvert
        objects from the self.type_to_field_type_converter to the
        dict self.name_to_field_type_converter yet with the
        field names as the key instead of the type name. Also it does
        fill the internal default converter dict.

        Args:
            descriptor (dict): The descriptor dict.
        '''
        self.user_descriptor = descriptor
        for field_name in self.user_descriptor:
            # just add the default straight ahead
            default = self.user_descriptor[field_name]['default']
            self.name_to_default[field_name] = default

            # then add the field type, if a type converter exists
            type_name = self.user_descriptor[field_name]['type']
            if type_name in self.type_to_field_type_converter:
                self.name_to_field_type_converter[field_name] = \
                    self.type_to_field_type_converter[type_name]
