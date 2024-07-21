from decimal import Decimal
from datetime import datetime
from plainvoice.model.base.base_model import BaseModel


class DocumentType(BaseModel):
    '''
    This class can describe a document and it's needed
    data fields and where it is stored etc.
    '''

    DEFAULT_PREBUILT_FIELDS: dict = {}
    '''
    The fields, which are pre-built already to be filled by the
    user, next to the dynamic optional fields, the user can set
    by their own.
    '''

    TYPE_MAPPING: dict = {
        'str': str,
        'int': int,
        'list': list,
        'dict': dict,
        'date': datetime,
        'Decimal': Decimal
    }
    '''
    The type mapping dict, which includes all possible type
    strings and what they will reflect in the code later.
    '''

    def __init__(self, name: str = '', document_folder: str = './'):
        '''
        This class can describe a document and it's needed
        data fields and where it is stored etc.

        Args:
            name (str): \
                The readbale name for the document type. (default: `'dummy'`)
            folder (str | None): \
                The folder to store the document type to. '{pv}' inside the \
                string can be used, which will be replaced with the programs \
                root data dir. So use '{pv}/invoices', for example, so that \
                the 'invoices' folder inside the programs data dir will be \
                used. Leave empty, so that the folder will be the working \
                dirs folder form which the program was started. \
                (default: `None`)

        '''
        super().__init__(name, '{pv}/types')

        self.document_folder = document_folder or self.DEFAULT_FOLDER
        '''
        The folder for the document, which gets this document type.
        '''

        self.prebuilt_fields = self.DEFAULT_PREBUILT_FIELDS
        '''
        The required fields as a dict, set by the user. It will contain
        the label for the field as the key and the type as its value.
        The type is set as a string, which the programm will try to
        understand correctly.
        '''

        # set values according to the init arguments
        if name != '':
            self.load_from_name(name)

    def __str__(self) -> str:
        '''
        Represent this class as a string with its name.

        Returns:
            srt: The readable name string.
        '''
        return self.name

    def from_dict(self, values: dict) -> None:
        '''
        Basically load this object from a dict.

        Args:
            values (dict): The dict to be used to fill this object.
        '''
        super().from_dict(values)
        self.document_folder = values.get(
            'document_folder', self.DEFAULT_FOLDER
        )
        self.required_fields = values.get(
            'prebuilt_fields', self.DEFAULT_PREBUILT_FIELDS
        )

    def parse_type(
        self,
        type: str,
        key: str = '_empty',
        values: dict = {'_empty': None}
    ) -> object:
        '''
        Parse the given type, which should be a value from the
        TYPE_MAPPINGS, against values[key]. The value is, for
        example the value from the loading YAML and probably
        a basic python type, which should maybe be translated
        to something else. E.g. Decimal is stored as float
        in "my YAML format" for better readability. As a
        fallback this method returns None.

        Args:
            type (str): \
                Should be a value from the TYPE_MAPPINGS.

            key (str): \
                The key where the value is stored in the \
                values dict. Leave this and values empty \
                to get empty default types.

            values (dict): \
                The loaded YAML dict. Leace this and key \
                empty to get empty default types.

        Returns:
            object: Returns the value in the wanted type.
        '''
        value = values.get(key, None)
        if key not in self.prebuilt_fields or key == '_empty':
            return None
        else:
            return self.parse_type_mapper(type, value)

    @staticmethod
    def parse_type_mapper(type: str, value) -> object:
        '''
        Get the value and try to call it into the wanted type.

        Args:
            type (str): \
                The wanted type.
            value: \
                Any kind of variable. I avoided setting a type \
                in the annotations, due to my code linter would \
                give me an error hint, otherwise.

        Returns:
            object: Returns the called new variable.
        '''
        if type == 'str':
            if value is None:
                return ''
            else:
                return str(value)
        elif type == 'int':
            if value is None:
                return 0
            else:
                return int(value)
        elif type == 'float':
            if value is None:
                return 0.0
            else:
                return float(value)
        elif type == 'list':
            if value is None:
                return []
            else:
                return list(value)
        elif type == 'dict':
            if value is None:
                return {}
            else:
                return dict(value)
        elif type == 'Decimal':
            if value is None:
                return Decimal()
            else:
                return Decimal(str(value))

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
            if fieldname == 'document_folder':
                self.document_folder = str(value)
            elif fieldname == 'prebuilt_fields':
                self.prebuilt_fields = dict(value)
            return super().set(fieldname, value)
        except Exception:
            return False

    def to_dict(self) -> dict:
        '''
        Converts the object to a dict, which can e.g. be used to
        be converted and stored inside a YAML.

        Returns:
            dict: The object as a dict.
        '''
        output = super().to_dict()
        output.update(self.to_dict_additional())
        return output

    def to_dict_additional(self) -> dict:
        '''
        Converts the object to a dict, which can e.g. be used to
        be converted and stored inside a YAML. This method
        outputs the other attributes only. This becomes handy
        in the to_yaml_string() method, in which I want only
        certain parts of the dict to be generated so that
        I can put comments in between them.

        Returns:
            dict: The object as a dict.
        '''
        return {
            'document_folder': self.document_folder,
            'prebuilt_fields': self.prebuilt_fields
        }

    def to_yaml_string(self, comments: bool = True) -> str:
        '''
        Convert the object to a YAML string, including comments
        for better structuring the file and for it to be better
        human readable.

        Args:
            comments (bool): \
                If True, this method adds comments to structure \
                the YAML file better.

        Returns:
            str: Return the final YAML string.
        '''
        output = self.repository.file.to_yaml_string(
            super().to_dict()
        )
        output += '''

# document_folder
#    defines where the documents, which get this document type
#    get their data stored
#
# prebuilt_fields
#     use the key as the name / label for the field and use its
#     value to describe its variable type. possible type names are:
#     python types: str, int, float, list, dict
#     additional types: Decimal (better use instead of float!), \
PostingsList, Posting

'''
        output += self.repository.file.to_yaml_string(
            self.to_dict_additional()
        )
        return output
