'''
DataModel Class

This class is supposed to be the base structure of an object.
Basically it's even almost some kind of interface after all.
With this I want to have some very basic method / technique
with which the programm can convert data to YAML and vice versa.

The principle is that this class hold rather flexible / extendible.
There are base attributes, which are really rather "hard-coded" stuff
and not that flexible. Maybe for childs of this class.

Yet there are two more kinds of "data-sets", which hold so called
"fields", as I call them during development.

The one data-set needs some kind of field type description, done via
the FieldConversionManager. It will hold internally specific types
and in the export (e.g. the YAML) such fields are converted in a
more readbale format (that's where the plaintext mindset comes in).
Also it needs either a describign dict or it is possible to add certain
fixed fields via add_field_descriptor(). That way the class knows
1. what these fields shall hold for a type (and how to convert it
to readable or to internal format) and 2. what default value it
should hold, if it is not defined be the user. Such fields are
"fixed", which means tha they always exist (almost like class
attributes), yet in a dictionary. The other data-set is absolutely
flexible and will only be filled by additional fields, the user
can define on the fly (later in the YAML). The downsite is that
such fields can only hold basic Python types.

The idea is that the user may define certain document types later
by only providing a dict as a descriptor to tell how a field is
called, what type it is (there will be a set of possible types)
and what its default value is.

I really hope, it is clear and also I hope I myself will understand
this whole principle in a year or so still. :D
'''

from plainvoice.model.field.field_conversion_manager \
    import FieldConversionManager
from plainvoice.utils import data_utils
from typing import Any, Callable


class DataModel:
    '''
    Base data model.
    '''

    def __init__(self):
        '''
        The base class for the apps data structure.
        '''

        self.additional = {}
        '''
        The dict, which holds additional possible data,
        which are dynamically to add / delete by the user.
        These are data, which are not part of the base
        data set as described by the class. This way later
        the YAML, which will store all the data, can have
        fields, which would be loaded into this dict, if
        the key is no attribute of this class; thus an
        additional attribute so to speak.
        '''

        self.fixed_field_conversion_manager = FieldConversionManager()
        '''
        The FieldConversionManager, which can handle the self.fixed
        fields and convert them back and forth to or from
        the wanted readable format, e.g. for the YAML file.

        The respecintg repository, which will handle the
        file loading and saving, will handle this component.
        Maybe even child classes of this class will use
        this component to "hard code" fields and offer a
        hard-coded data object. E.g. like Clients, which
        should have a certain set of fields, or so.
        '''

        self.fixed = {}
        '''
        The "fixed" fields for the data object. The idea is to
        have fields, which should have some kind of a "readable"
        value in the YAML file later. Yet when I would store a
        Decimal object in the YAML, it would not read well. For
        this purpose there is the FieldConversionManager, which would
        be able to convert it with the respecting FieldTypeConverter
        item.

        Also with the fixed fields empty fields will be stored
        with a set default in the YAML. This will become handy,
        if the user legt the programm create a new YAML file.
        Then empty fields with their defaults will be generated
        as well and the user can see what fields are supposed
        to exist in this data object.
        '''

        self.visible = True
        '''
        Sets if the data set should be visible when e.g. listing datas
        and this data would be hidden in such a list then.
        '''

    def add_field_descriptor(
        self,
        fieldname: str,
        typename: str,
        default: Any,
    ) -> None:
        '''
        Add a field descriptor to the FieldConversionManager. This
        is basically a wrapper method for the FieldConversionManager
        method .add_field_descriptor(). Yet also it serves to fill
        the new field with its default already so that it is
        accessible already.

        Args:
            fieldname (str): \
                The name for the field. It will become the dict key.
            typename (str): \
                The string describing the field type.
            default (object): \
                Any kind of default, which should represent the \
                readable default later. So it should be a basic \
                Python object like str, int, float, list or dict.
        '''
        self.fixed_field_conversion_manager.add_field_descriptor(
            fieldname,
            typename,
            default
        )
        self.fixed[fieldname] = \
            self.fixed_field_conversion_manager.convert_field_to_internal(
                fieldname, {}
            )

    @classmethod
    def create_instance(cls):
        return cls()

    def define_fixed_field_type(
        self,
        field_type_str: str,
        to_internal: Callable,
        to_readable: Callable
    ) -> None:
        '''
        Define / add a field to the fixed fields. It's basically a
        wrapper for the FieldConversionManager.add_field_type() methods
        and takes arguments, which are needed to initialize a
        FieldTypeConverter instance.

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
        self.fixed_field_conversion_manager.add_field_type(
            field_type_str,
            to_internal,
            to_readable
        )

    def from_dict(self, values: dict) -> None:
        '''
        This method combines the other private methods for filling
        the "fields" and class attributes from a given dict. The
        values for the "fixed" fields should be in the readable
        format.

        Args:
            values (dict): The dict to load the attributes from.
        '''
        self._from_dict_additional(values)
        self._from_dict_base(values)
        self._from_dict_fixed(values)

    def _from_dict_additional(self, values: dict) -> None:
        '''
        Getting data from the given dict and store them to
        the self.additional dict, if the key does not exist
        in the classes attributes.

        Args:
            values (dict): The dict to load additional fields from.
        '''
        self.additional = {}
        fixed_fields = self.fixed_field_conversion_manager.get_fieldnames()
        for key in values:
            if (
                key not in self.__dict__.keys()
                and key not in fixed_fields
            ):
                self.additional[key] = values[key]

    def _from_dict_base(self, values: dict) -> None:
        '''
        Loading internal attributes from the given dict.

        Args:
            values (dict): The dict to load the attributes from.
        '''
        self.visible = bool(values.get('visible', self.visible))

    def _from_dict_fixed(self, values: dict) -> None:
        '''
        Convert given dict data to be put onto the fixed fields. The
        values in of these fields should be in the readable format.

        Args:
            values (dict): The dict to load additional fields from.
        '''
        self.fixed = {}
        self.fixed = \
            self.fixed_field_conversion_manager.convert_dict_to_internal(
                values
            )

    def get(self, fieldname: str, readable: bool = False) -> Any:
        '''
        This is a magical getter method, which will return either
        a class attribute with the fieldname, if it exists, or
        a fixed field or an additional one. Internally it will
        convert the object to a dict, which should create a flat
        dict and output the value on the given key then.

        Args:
            fieldname (str): \
                The class attribute or additional fieldname.
            readable (bool): \
                If True, fixed fields will be converted to readble \
                first (default: `False`)

        Returns:
            Any: Returns the class attribute, an additional field or None.
        '''
        return self.to_dict(readable).get(fieldname)

    def get_additional(self, fieldname: str) -> Any:
        '''
        Get an additional field from the additional dict. This might
        be an additional key from the YAML in the datas file, yet one,
        which is no original attritbute of the class.

        Args:
            fieldname (str): The fieldname / key of the additional field.

        Returns:
            Any: Returns the respecting data, if existend.
        '''
        return self.additional.get(fieldname)

    def get_fixed(self, fieldname: str, readable: bool = True) -> Any:
        '''
        Get an fixed field from the fixed dict. This is a field,
        which is defined by the FieldTypeConverter. Also it is possible
        to get this field in a readable type or in its raw type.

        Args:
            fieldname (str): \
                The fieldname / key of the additional field.
            readable (bool): \
                If True the FieldConversionManager converts the whole dict
                first to the readbale format and then outputs its value.

        Returns:
            Any: Returns the respecting data, if existend.
        '''
        if readable:
            return \
                self.fixed_field_conversion_manager.convert_field_to_readable(
                    fieldname, self.fixed
                )
        else:
            return self.fixed.get(fieldname)

    def hide(self) -> None:
        '''
        Hide the object. Set internal visible attribute to False.
        '''
        self.visible = False

    @classmethod
    def instance_from_dict(cls, values: dict):
        output = cls()
        output.from_dict(values)
        return output

    def is_visible(self) -> bool:
        '''
        Return if this object is visible or not.

        Returns:
            bool: Returns True if visible, else False.
        '''
        return self.visible

    def set_additional(self, fieldname: str, value: Any) -> None:
        '''
        Set an additional value to the field with the given fieldname.
        Basically it is just the internal dict, which will be extended
        or modified. Later it might be a new key in the YAML file.

        Args:
            fieldname (str): \
                The fieldname of the additional data field.
            value (object): \
                The value to set into this field. If "None" it will \
                delete the data field.
        '''
        if value is None and fieldname in self.additional:
            del self.additional[fieldname]
        else:
            self.additional[fieldname] = value

    def set_fixed_fields_descriptor(self, descriptor: dict) -> None:
        '''
        Set the descriptor dict for the fixed field conversion
        manager of this class. It should look something like
        this:

        {
            'field_a': {
                'type': 'str',
                'default': 'default string'
            },
            'field_b': {
                'type': 'int',
                'default': 0
            }
        }

        This also initializes certain variables of the internal
        field conversion manager.

        Args:
            descriptor (dict): The descriptor dict.
        '''
        return self.fixed_field_conversion_manager.set_descriptor(descriptor)

    def set_fixed(
        self,
        fieldname: str,
        value: Any,
        is_readable: bool = True
    ) -> None:
        '''
        Set a fixed value to the internal fixed fields dict. The value
        can be the internal type or, if is_readable == True, the readable
        format which gets converted to internal before setting it to the
        fixed field.

        Args:
            fieldname (str): \
                The fieldname of the additional data field.
            value (object): \
                The value to set into this field. If "None" it will \
                set the field to its default.
            is_readable (bool): \
                If True, the input is supposed to be the readable \
                format and has to be converted first.
        '''
        # do nothing, if the fieldname does not exist
        if fieldname not in \
                self.fixed_field_conversion_manager.get_fieldnames():
            return None

        # convert it to internal first, if needed
        if is_readable:
            value = \
                self.fixed_field_conversion_manager.convert_field_to_internal(
                    fieldname,
                    {fieldname: value}
                )

        # finally set the value
        # if the value is None, the fixed should become its default
        if value is None and fieldname in self.fixed:
            self.fixed[fieldname] = \
                self.fixed_field_conversion_manager.get_default_for_fieldname(
                    fieldname, False
                )
        # otherwise simply set the value to the fixed field
        else:
            self.fixed[fieldname] = value

    def show(self) -> None:
        '''
        Show the object. Set internal visible attribute to True.
        '''
        self.visible = True

    def to_dict(self, readable: bool = False) -> dict:
        '''
        This method is for exporting all the needed data
        of the object to a dict. Like the from_dict()
        method it is some kind of abstract method and should
        be overwritten by the child class. self._to_dict_base()
        should also be used to get the base attributes as well,
        if the base attributes are needed in the output. Also
        there is self._to_dict_additional() to get the
        additional fields in a separate dict.

        Args:
            readable (bool): \
                If True, fixed fields will be converted to readble \
                first (default: `False`)

        Returns:
            dict: Returns the data as a dict.
        '''
        output = {}
        # the order here is important to the output of the YAML
        # later! that's why this isn't alphabetically
        output.update(self._to_dict_base())
        output.update(self._to_dict_fixed(readable))
        output.update(self._to_dict_additional())
        return output

    def _to_dict_additional(self) -> dict:
        '''
        Get the additional fields of this object as a dict.

        Returns:
            dict: Returns additional attributes as a dict.
        '''
        return self.additional

    def _to_dict_base(self) -> dict:
        '''
        Get the base attributes of this object as a dict.

        Returns:
            dict: Returns base attributes as a dict.
        '''
        return {
            'visible': self.visible
        }

    def _to_dict_fixed(self, readable: bool = False) -> dict:
        '''
        Get the fixed fields of this object as a dict. Also they
        can be output in a readble converted format or not.

        Args:
            readable (bool): \
                If True, fields will be converted to readble \
                first (default: `False`)
        '''
        if readable:
            return \
                self.fixed_field_conversion_manager.convert_dict_to_readable(
                    self.fixed
                )
        else:
            return self.fixed

    def to_yaml_string(self) -> str:
        '''
        Convert the data object to a readable YAML string and
        use readable type fromats in this process.

        Returns:
            str: Returns the readable YAML string.
        '''

        # # # # BASE ATTRIBUTES
        base_str = f'''# base variables

{data_utils.to_yaml_string(self._to_dict_base()).strip()}
'''.strip() if self._to_dict_base() else ''

        # # # # FIXED FIELDS
        fixed_str = f'''# fixed fields

{data_utils.to_yaml_string(self._to_dict_fixed()).strip()}
'''.strip() if self._to_dict_fixed() else ''

        # # # # ADDITIONAl FIELDS
        additional_str = f'''# additional fields

{data_utils.to_yaml_string(self._to_dict_additional()).strip()}
'''.strip() if self._to_dict_additional() else ''

        return '\n\n\n'.join(
            x for x in [base_str, fixed_str, additional_str] if x
        ).strip()
