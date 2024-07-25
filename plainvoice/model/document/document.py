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
from plainvoice.model.document.document_connector import DocumentConnector
from plainvoice.model.document.document_type import DocumentType

# with this modul I can refer to the class itself in the annotations
# of the class methods etc.
from typing import Self


class Document(BaseModel):
    '''
    Base class which implements the flexible data-dict, the
    user can set in the YAML later to have as many fields
    as they want. This class should be inherited by
    Invoice or Client.
    '''

    _instances: dict = {}
    '''
    A collection of all instances being already initiated during
    runtime. This way I can avoid having two instances of basically
    the same data set. And then, when I want to get this from a
    connectin of another document, yet loaded it before that already
    manually, I would end up having two different kind of instances,
    which are supposed to be the same and just reference to each other
    or so.
    '''

    IGNORE_FIELDNAMES: list = [
        # the base attributes from the Base class
        'code', 'name', 'visible',
        # non data_prebuilt or non data_user attributes
        'document_type', 'document_connections'
    ]
    '''
    These are the fieldnames to be ignored during the
    automatic setter methods. Basically these are the
    base attributes of the classe and the ones, which
    are not in the data_prebuilt or data_user variables.
    '''

    def __new__(cls, *args, **kwargs):
        '''
        Here I create an instance, as if I would create
        such a document. Yet after that I check if its
        internal instance id might already be in the
        _instances and use this instead then.
        '''
        instance = super().__new__(cls)
        instance.__init__(*args, **kwargs)
        instance_id = instance._get_instance_id()
        if instance_id in cls._instances:
            return cls._instances[instance_id]
        else:
            return instance

    def __init__(
        self,
        name: str = '',
        document_type_name: str = '',
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

        self.document_connector = DocumentConnector(self)
        '''
        The DocumentConnector component to let documents connect. With this
        the special `document_connections` attribute form the YAML will be
        interpreted and documents will be to loaded automatically (if
        possible).
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

        # after loading and initiating, add it to the _instances
        self._add_to_instances()

    def add_connection(self, document) -> None:
        '''
        Add a document to the connections. This way you can link two (or more)
        documents to each other. The method will not save the linked state
        for this nor for the other documents, unless save() is being called.

        Args:
            document (Document): \
                The document to add to the connections.
        '''
        self.document_connector.add_connection(document, self)

    def _add_to_instances(self) -> None:
        '''
        Add this document to the instances according to its
        internal instance id.
        '''
        if (
            self._get_instance_id() not in self._instances
            # also do not let empty documents get added to
            # this instances dict
            and self.name != ''
        ):
            self._instances[self._get_instance_id()] = self

    @property
    def delete_connection(self):
        return self.document_connector.delete_connection

    def fill_empty_prebuilt_fields(self) -> None:
        '''
        Fill the prebuilt data with an empty data type according
        to the wanted type. This is important so that even
        "non set" variables will get stored into the YAML so that
        the "prebuilt" thing makes sense after all. This is needed
        for the user to SEE the fields in the YAML and thus KNOWS
        that they exist. This is the logic behind it!
        '''
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
        self.document_connector.from_dict(values)

    def _from_dict_data(self, values: dict) -> None:
        '''
        Fill the objects attributes / data from the given dict,
        yet here for just the data.

        Args:
            values (dict): The dict values to fill the object.
        '''
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
        '''
        Fill the objects attributes / data from the given dict,
        yet here for just the document type.

        Args:
            values (dict): The dict values to fill the object.
        '''
        document_type_name = values.get('document_type', None)
        if document_type_name is not None:
            if self.document_type.name != document_type_name:
                self.set_document_type(document_type_name)

    def get_existing_instance(
        self,
        instance: Self
    ) -> Self:
        '''
        Check if the given instance might already exist
        in the Document class global attribute _instances and
        then refer to this instead for data consistency.

        Args:
            instance (Document): The Document instance to check.

        Returns:
            Document: Returns the final Document instance.
        '''
        new_instance_id = instance._get_instance_id()
        if new_instance_id in self._instances:
            actual_instance = self._instances[new_instance_id]
            instance = actual_instance
        return instance

    @property
    def get_connection_by_filename(self):
        return self.document_connector.get_connection_by_filename

    @property
    def get_connections_filepaths(self):
        return self.document_connector.get_connections_filepaths

    def _get_instance_id(self) -> str:
        '''
        Generate and return the id, used for finding the relating
        instance for this document. Well, or setting it after
        initialization. It is basically just the type and the
        name of the document combined.

        Returns:
            str: Returns the instance id string.
        '''
        return f'{self.document_type.name}::{self.name}'

    def load_from_name(self, name: str) -> None:
        '''
        Load the data object from just it's name. The
        method will look into the data objects folder
        in the program's folder automatically.

        Args:
            name (str): The name of the data object.
        '''
        super().load_from_name(name)
        self._add_to_instances()

    def rename(self, new_name: str) -> bool:
        '''
        Renames the document and since its basically almost
        the filename, it will rename all references in its
        connections as well.

        Args:
            new_name (str): The new name for this document.

        Returns:
            bool: Returns True on success.
        '''

        # first "save" the old filepath in a variable, it
        # is neede later in the rename_self_in_connections()
        # method, since it will go through the connections,
        # which still have the old filepath after all
        old_filepath = self.get_absolute_filename()

        # rename stuff according to the parent class
        success = super().rename(new_name)

        # then rename the connections and return the success
        # value
        return (
            success and
            self.rename_self_in_connections(new_name, old_filepath)
        )

    def rename_self_in_connections(
        self,
        new_name: str,
        old_filepath: str
    ) -> bool:
        '''
        This method will go through all connections of this document
        and rename itself in their and save the connnected document
        so that the change will take effect immediately.

        Args:
            new_name (str): \
                The new name for this document.
            old_filepath (str): \
                The old filepath, which is still saved in the \
                connected connections list.

        Returns:
            bool: Returns True on success.
        '''
        try:
            new_filepath = self.get_absolute_filename()
            for connection_filepath in self.get_connections_filepaths():
                connection = self.get_connection_by_filename(
                    connection_filepath
                )
                connection.document_connector.connections_filepaths.remove(
                    old_filepath
                )
                connection.document_connector.connections_filepaths.append(
                    new_filepath
                )
                connection.save()
            return True
        except Exception:
            return False

    def save(self, save_connections: bool = True) -> bool:
        '''
        Save the document. It uses the BaseModel save()
        method, yet extends it by saving all the connected
        documents as well.

        Args:
            save_connections (bool): \
                Tells the method to also save the connections. \
                I need this argument so that this method itself \
                can call this method on the connected documents, yet \
                without them letting this linked document save \
                itself again. It would be an infintie loop.

        Returns:
            bool: Returns True on success.
        '''
        # well ... there has to be a name, it's the filename after all!
        if self.name == '':
            return False

        success = []
        if save_connections:
            active_connections = self.document_connector.connections_filepaths
            for connection in active_connections:
                tmp_document = self.get_connection_by_filename(connection)
                success.append(tmp_document.save(False))
            deleted_connections = self.document_connector.deleted_connections
            for deleted_connection in deleted_connections:
                deleted_connections.remove(deleted_connection)
                success.append(deleted_connection.save(False))
        return super().save() and False not in success

    def set(self, fieldname: str, value) -> bool:
        '''
        Set the value to the fieldname.

        Args:
            fieldname (str): The fieldname to set.
            value (object): The value to set.

        Returns:
            bool: Returns True on success.
        '''
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
        '''
        Changes the document type and adjusts internal variables
        accordingly automatically.

        Args:
            document_type_name (str): The name of the document type.

        Returns:
            bool: Returns True on success.
        '''
        try:
            self.document_type.load_from_name(document_type_name)
            self.repository.set_folder(
                self.document_type.get('document_folder')
            )
            self.repository.set_filename_pattern(
                self.document_type.get('document_filename_pattern')
            )
            self.fill_empty_prebuilt_fields()
            # also correct the name. if I create a blank Document
            # from file, the name will be generated with the help
            # of FilePathGenerator().extract_name_from_path(). Yet
            # this method uses the DocumentType.document_folder to
            # remove it from the filename string. yet in a blank
            # document this folder is not set, before the document
            # type was loaded (like in here). so I should "fix" the
            # name of the document!
            self.name = self.repository.file.extract_name_from_path(self.name)
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
        '''
        The fields of this document class; yet only
        the base attributes.

        Returns:
            dict: The dict.
        '''
        return {
            'document_type': str(self.document_type),
            'document_connections': self.document_connector.to_list()
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
