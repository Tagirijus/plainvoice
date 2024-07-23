'''
Document Class

This class is the main document object. It can be anything, due to the
DocumentType class, which is a component of this class. The DocumentType
class will describe in which folder such documents are being stored. It
also describes which basic fields are meant to exist for this kind of
document.

It is possible to store even more values inside the YAML by just defining
a key and a value. The document will understand it and store the data
in the data_user attribute automatically.
'''


from plainvoice.model.base.base_model import BaseModel
from plainvoice.model.document.document_type import DocumentType


class Document(BaseModel):
    '''
    Base class which implements the flexible data-dict, the
    user can set in the YAML later to have as many fields
    as they want. This class should be inherited by
    Invoice or Client.
    '''

    IGNORE_FIELDNAMES: list = [
        # the base attributes from the Base class
        'id', 'name', 'visible',
        # non data_prebuilt / data_user attributes
        'document_type'
    ]
    """
    These are the fieldnames to be ignored during the
    automatic setter methods. Basically these are the
    base attributes of the classe and the ones, which
    are not in the data_prebuilt or data_user variables.
    """

    def __init__(
        self,
        document_type_name: str = '',
        name: str = '',
        filename_pattern: str = '{id}'
    ):
        super().__init__(name)

        self.data_prebuilt = {}
        '''
        The internal objects dict, which contains all the data for the
        pre built fields.
        '''

        self.data_user = {}
        '''
        The internal objects dict, which can store all needed additional
        data set by the user.
        '''

        self.document_type = DocumentType(
            name=document_type_name,
            document_filename_pattern=filename_pattern
        )
        '''
        The DocumentType, which will describe the type of this object.
        A user can configure custom types of documents besides the
        basic ones.
        '''
        self.set_document_type(document_type_name)

        # change the name again to reflect it better, if the name
        # was left empty
        # set values according to the init arguments
        if name != '':
            self.load_from_name(name)
        else:
            self.name = (
                f'new {self.document_type.get('name')}' if name == '' else name
            )

    def fill_empty_prebuilt_fields(self) -> None:
        """
        Fill the prebuilt data with an empty data type according
        to the wanted type. This is important so that even
        "non set" variables will get stored into the YAML so that
        the "prebuilt" thing makes sense after all. This is needed
        for the user to SEE the fields in the YAML and thus KNOWS
        that they exist. This is the logic behind it!
        """
        for fieldname in self.document_type.prebuilt_fields.keys():
            if fieldname not in self.data_prebuilt.keys():
                self.data_prebuilt[fieldname] = (
                    self.document_type.parse_type(
                        fieldname,
                        None
                    )
                )

    def from_dict(self, values: dict) -> None:
        '''
        Fill the objects attributes / data from the given dict.

        Args:
            values (dict): The dict values to fill the object.
        '''
        self._from_dict_base(values)
        self._from_dict_document_type(values)
        self._from_dict_data(values)

    def _from_dict_data(self, values: dict) -> None:
        """
        Fill the objects attributes / data from the given dict,
        yet here for just the data.

        Args:
            values (dict): The dict values to fill the object.
        """
        prebuilt_keys = self.document_type.prebuilt_fields.keys()
        self.data_prebuilt = {}
        self.data_user = {}
        # if there are no values of the prebuilt fields yet,
        # add them. otherwise they would never be shown in
        # the YAML file, when saved for the first time.
        self.fill_empty_prebuilt_fields()
        for fieldname in values:
            if fieldname in prebuilt_keys:
                self.data_prebuilt[fieldname] = (
                    self.document_type.parse_type(
                        fieldname,
                        values[fieldname]
                    )
                )
            elif fieldname not in self.IGNORE_FIELDNAMES:
                self.data_user[fieldname] = values.get(fieldname, None)

    def _from_dict_document_type(self, values: dict) -> None:
        """
        Fill the objects attributes / data from the given dict,
        yet here for just the document type.

        Args:
            values (dict): The dict values to fill the object.
        """
        document_type_name = values.get('document_type', None)
        if document_type_name is not None:
            if self.document_type.name != document_type_name:
                self.set_document_type(document_type_name)

    def set(self, fieldname: str, value) -> bool:
        """
        Set the value to the fieldname.

        Args:
            fieldname (str): The fieldname to set.
            value (object): The value to set.

        Returns:
            bool: Returns True on success.
        """
        try:
            prebuilt_keys = self.document_type.prebuilt_fields.keys()
            if fieldname in prebuilt_keys:
                self.data_prebuilt[fieldname] = (
                    self.document_type.parse_type(
                        fieldname,
                        value
                    )
                )
            elif fieldname not in self.IGNORE_FIELDNAMES:
                self.data_user[fieldname] = value
            return super().set(fieldname, value)
        except Exception:
            return False

    def set_document_type(self, document_type_name: str) -> bool:
        """
        Changes the document type and adjusts internal variables
        accordingly automatically.

        Args:
            document_type_name (str): The name of the document type.

        Returns:
            bool: Returns True on success.
        """
        try:
            self.document_type.load_from_name(document_type_name)
            self.repository.set_folder(
                str(self.document_type.get('document_folder'))
            )
            self.repository.set_filename_pattern(
                str(self.document_type.get('document_filename_pattern'))
            )
            self.fill_empty_prebuilt_fields()
            return True
        except Exception:
            return False

    def to_dict(self) -> dict:
        '''
        Convert the object to a dict.

        Returns:
            dict: Class attributes and the self.data as a dict.
        '''
        output = super().to_dict()
        output.update(self.to_dict_document())
        output.update(self.to_dict_prebuilt())
        output.update(self.to_dict_user())
        return output

    def to_dict_document(self) -> dict:
        """
        The fields of this document class; yet only
        the base attributes.

        Returns:
            dict: The dict.
        """
        return {
            'document_type': str(self.document_type)
        }

    def to_dict_prebuilt(self) -> dict:
        '''
        The prebuilt fields as a dict.

        Returns:
            dict: The dict.
        '''
        return self.document_type.to_dict_types(self.data_prebuilt)

    def to_dict_user(self) -> dict:
        '''
        The user fields as a dict.

        Returns:
            dict: The dict.
        '''
        return self.data_user

    def to_yaml_string(self, show_comments: bool = True) -> str:
        '''
        Convert the object to a YAML string, including comments
        for better structuring the file and for it to be better
        human readable.

        Args:
            show_comments (bool): \
                If True, this method adds comments to structure \
                the YAML file better.

        Returns:
            str: Return the final YAML string.
        '''
        output = self.repository.file.to_yaml_string(
            super().to_dict()
        )
        if show_comments:
            output += '''

# document base attributes

'''
        output += self.repository.file.to_yaml_string(
            self.to_dict_document()
        )
        if show_comments:
            output += '''

# prebuilt fields defined by the document type

'''
        output += self.repository.file.to_yaml_string(
            self.to_dict_prebuilt()
        )
        if show_comments:
            output += '''

# additional user fields. should be basic Python type (str, int, float, \
list, dict)

'''
        if self.data_user:
            output += self.repository.file.to_yaml_string(
                self.to_dict_user()
            )
        return output
