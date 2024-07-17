from decimal import Decimal
from datetime import datetime
from plainvoice.model.document_type import DocumentType
from plainvoice.model.filemanager import FileManager
from plainvoice.utils import date_utils


class Document:
    """
    Base class which implements the flexible data-dict, the
    user can set in the YAML later to have as many fields
    as they want. This class should be inherited by
    Invoice or Client.
    """

    def __init__(self):
        self.id = None
        """
        The id of the class. For an invoice this could be used as
        an invoice id, for example.
        """

        self.document_type = DocumentType()
        """
        The DocumentType, which will describe the type of this object.
        A user can configure custom types of documents besides the
        basic ones.
        """

        self.data_required = {}
        """
        The internal objects dict, which contains alls the needed data
        sets, assigned by the DocumentType.
        """

        self.data_user = {}
        """
        The internal objects dict, which can store all needed additional
        data set from the user.
        """

    def from_dict(self, values: dict) -> None:
        """
        Fill the objects attributes / data from the given dict.

        Args:
            values (dict): The dict values to fill the object.
        """
        self.id = values.get('id', None)
        document_type_name = values.get('document_type', None)
        if document_type_name is None:
            raise Exception(
                'document_type not available in Document.from_dict()'
            )
        else:
            self.set_document_type(document_type_name)

        ignore_keys = ['id', 'document_type']
        required_keys = self.document_type.required_fields.keys()
        self.data_required = {}
        self.data_user = {}
        for key in values:
            if key in required_keys:
                self.data_required[key] = self.document_type.parse_type(
                    self.document_type.required_fields[key],
                    key,
                    values
                )
            elif key not in ignore_keys:
                self.data_user[key] = values.get(key, None)

    def get(self, key: str) -> object:
        """
        Get data from this object or its self.data_user dict
        or the self.data_required dict.

        Args:
            key (str): The key of the object or maybe the self.data dict.

        Returns:
            object: Returns the value, if found, or an empty string.
        """
        fetched = self.to_dict().get(key, None)
        return fetched

    def set_document_type(self, document_type_name: str = 'dummy') -> None:
        """
        Set the document type for this document by document types name.

        Args:
            document_type_name (str): The document type name.
        """
        if document_type_name == 'dummy':
            self.document_type = DocumentType()
        else:
            fm = FileManager('{pv}/types')
            document_type_dict = fm.load_from_yaml_file(document_type_name)
            document_type = DocumentType()
            document_type.from_dict(document_type_dict)
            self.document_type = document_type
        for key in self.document_type.required_fields:
            if key not in self.data_required:
                self.data_required[key] = self.document_type.parse_type(
                    self.document_type.required_fields[key]
                )

    def to_dict(self) -> dict:
        """
        Convert the object to a dict.

        Returns:
            dict: Class attributes and the self.data as a dict.
        """
        output = self.to_dict_base()
        output.update(self.to_dict_required())
        output.update(self.to_dict_user())
        return output

    def to_dict_base(self) -> dict:
        """
        The very base fields as a dict.

        Returns:
            dict: The dict.
        """
        return {
            'id': self.id,
            'document_type': str(self.document_type)
        }

    def to_dict_required(self) -> dict:
        """
        The required fields as a dict.

        Returns:
            dict: The dict.
        """
        out = {}
        for key in self.data_required:
            value = self.data_required[key]
            # store Decimal as float
            if isinstance(value, Decimal):
                out[key] = float(value)
            # datetimes as a YYYY-MM-DD string
            elif isinstance(value, datetime):
                out[key] = date_utils.datetime2str(value)
            # PostingsList as list having Postings
            # being converted to dicts
            elif value.__class__.__name__ == 'PostingsList':
                out[key] = value.to_dicts()
            # convert a single Posting to dict
            elif value.__class__.__name__ == 'Posting':
                out[key] = value.to_dict()
            # just output the value otherwise
            else:
                out[key] = value
        return out

    def to_dict_user(self) -> dict:
        """
        The user fields as a dict.

        Returns:
            dict: The dict.
        """
        return self.data_user

    def to_yaml_string(self, comments: bool = True) -> str:
        """
        Convert the object to a YAML string, including comments
        for better structuring the file and for it to be better
        human readable.

        Args:
            comments (bool): \
                If True, this method adds comments to structure \
                the YAML file better.

        Returns:
            str: Return the final YAML string.
        """
        output = """
# DOCUMENT
# the base attributes to describe the document

""".lstrip()
        output += FileManager().to_yaml_string(self.to_dict_base())
        output += """

# required fields defined by the document type

"""
        output += FileManager().to_yaml_string(self.to_dict_required())
        output += """

# additional user fields. should be basic Python type (str, int, float, \
list, dict)

"""
        if self.data_user:
            output += FileManager().to_yaml_string(self.to_dict_user())
        return output
