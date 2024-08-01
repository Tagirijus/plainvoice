'''
DataModel Class

This class is supposed to be the base structure of an object.
Basically it's even almost some kind of interface after all.
With this I want to have some very basic method / technique
with which the programm can convert data to YAML and vice versa.
'''

from plainvoice.model.field.fields_converter import FieldsConverter


class DataModel:
    '''
    Base data model.
    '''

    def __init__(self, filename: str):
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

        self.fields_converter = FieldsConverter()
        '''
        The FieldsConverter, which can handle the self.fixed
        fields and convert them back and forth to or from
        the wanted readable format, e.g. for the YAML file.

        The respecintg repository, which will handle the
        file loading and saving, will handle this component.
        Maybe even child classes of this class will use
        this component to "hard code" fields and offer a
        hard-coded data object. E.g. like Clients, which
        should have a certain set of fields, or so.
        '''

        self.filename = filename
        '''
        The absolute filename for this data object.
        '''

        self.fixed = {}
        '''
        The "fixed" fields for the data object. The idea is to
        have fields, which should have some kind of a "readable"
        value in the YAML file later. Yet when I would store a
        Decimal object in the YAML, it would not read well. For
        this purpose there is the FieldsConverter, which would
        be able to convert it with the respecting FieldDescriptor
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

    @classmethod
    def create_instance(cls, filename: str):
        return cls(filename)

    def from_dict(self, values: dict) -> None:
        '''
        This is basically an abstract method, which
        should be overwritten by the child. It is for
        filling the class attributes from a dict.

        Yet self._from_dict_base(values) can be used,
        or maybe even should be used inside the overwritten
        childs method so that base attributes will also
        be filled on loading from dict.

        Also self._from_dict_additional(values) should be
        used, if additional fields, which might be keys in
        the YAML file, to which there are no attributes in
        this class, should be loaded as well from dict and
        put into the self.additional dict.

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
        fixed_fields = self.fields_converter.get_fieldnames()
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
        self.filename = values.get('filename', self.filename)
        self.visible = bool(values.get('visible', self.visible))

    def _from_dict_fixed(self, values: dict) -> None:
        '''
        Convert given dict data to be put onto the fixed fields.

        Args:
            values (dict): The dict to load additional fields from.
        '''
        self.fixed = {}
        self.fixed = self.fields_converter.convert_dict_from(values)

    def get(self, fieldname: str, readable: bool = False) -> object:
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
            object: Returns the class attribute, an additional field or None.
        '''
        return self.to_dict(readable).get(fieldname)

    def get_additional(self, fieldname: str) -> object:
        '''
        Get an additional field from the additional dict. This might
        be an additional key from the YAML in the datas file, yet one,
        which is no original attritbute of the class.

        Args:
            fieldname (str): The fieldname / key of the additional field.

        Returns:
            object: Returns the respecting data, if existend.
        '''
        return self.additional.get(fieldname)

    def get_filename(self) -> str:
        '''
        Get the absolute filename of this object.

        Returns:
            str: Returns the absolute filename as a string.
        '''
        return self.filename

    def get_fixed(self, fieldname: str, readable: bool = False) -> object:
        '''
        Get an fixed field from the fixed dict. This is a field,
        which is defined by the FieldDescriptor. Also it is possible
        to get this field in a readable type or in its raw type.

        Args:
            fieldname (str): \
                The fieldname / key of the additional field.
            readable (bool): \
                If True the FieldsConverter converts the whole dict
                first to the readbale format and then outputs its value.

        Returns:
            object: Returns the respecting data, if existend.
        '''
        if readable:
            return self.fields_converter.convert_field_to(
                fieldname, self.fixed
            )
        else:
            return self.fixed.get(fieldname)

    def hide(self) -> None:
        '''
        Hide the object. Set internal visible attribute to False.
        '''
        self.visible = False

    def is_visible(self) -> bool:
        '''
        Return if this object is visible or not.

        Returns:
            bool: Returns True if visible, else False.
        '''
        return self.visible

    def set_additional(self, fieldname: str, data: object) -> None:
        '''
        Set an additional value to the field with the given fieldname.
        Basically it is just the internal dict, which will be extended
        or modified. Later it might be a new key in the YAML file.

        Args:
            fieldname (str): \
                The fieldname of the additional data field.
            data (object): \
                The data to set into this field. If "None" it will \
                delete the data field.
        '''
        if data is None and fieldname in self.additional:
            del self.additional[fieldname]
        else:
            self.additional[fieldname] = data

    def set_filename(self, filename: str) -> None:
        '''
        Set the absolute filename to this data object.

        Args:
            filename (str): The absolute filename to this data object.
        '''
        self.filename = filename

    def set_fixed(
        self,
        fieldname: str,
        data: object,
        readable: bool = False
    ) -> None:
        '''
        Set a fixed value to the internal fixed fields dict. The data
        can be the internal type or, if readable == True, even the
        readable format, which would be used in the YAML later.

        Args:
            fieldname (str): \
                The fieldname of the additional data field.
            data (object): \
                The data to set into this field. If "None" it will \
                delete the data field.
        '''
        if data is None and fieldname in self.additional:
            del self.additional[fieldname]
        else:
            self.additional[fieldname] = data

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
            return self.fields_converter.convert_dict_to(self.fixed)
        else:
            return self.fixed
