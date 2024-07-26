'''
DocumentHardcodeType Class

This class basically is a wrapper for the classes, which are
supposed to have a hard-coded unchangable DocumentType like
Client, for example. Basically it is just a Document object
with a "hard-coded" DocumentType, which won't be loaded
from any file or so.
'''

from plainvoice.model.document.document import Document
from plainvoice.model.document.document_type import DocumentType


class DocumentHardcodeType(Document):
    '''
    Document with a hard-coded DocumentType.
    '''

    def __init__(
        self,
        name: str = '',
        document_type_name: str = '',
        filename_pattern: str = '',
        folder: str = ''
    ):
        '''
        This class is for clients data. It is supposed to be able
        to link to certain documents for the clients.

        Args:
            name (str): \
                The name of the file, basically.
            document_type_name (str): \
                The name of the document type to SET. \
                In contrast to the Document class, it is \
                supposed to set a name here. It will internally \
                be set to "_{document_type_name}" and used in \
                saving the document. It is just readability, so \
                when looking into the respecting YAML it might get \
                clear which type it is and that it is hard-coded, due \
                to the underscore.
            filename_pattern (str): \
                The pattern how filenames will be generated, \
                or codes be extracted.
        '''
        self.document_hardcoded_type_name = f'_{document_type_name}'
        self.document_hardcoded_filename_pattern = filename_pattern
        self.document_hardcoded_folder = folder

        self.default_fields: dict = {}
        '''
        !!! Childs should overwrite this variable !!!
        The dict describing the prebuilt fields and also
        holding the default values for it. It can describe
        the type of the prebuilt field and also fill its
        default value. I wanted to have this in one global
        variable so that it can get modified in one place
        easier.
        The key is the fieldname and its value is a tupple
        describing its type and default value.
        '''

        self.default_fields_types = {}
        self.default_fields_defaults = {}
        '''
        These two variables are cache variables for the
        default_fields variable and will get filled
        on demand.
        '''

        # the init of the parent class Document has to be
        # at the end of this own __init__ method, since
        # otherwise some attributes would not be available
        # in its child instances.
        # Maybe it's a sign of a bad structure here ...
        super().__init__(
            name,
            self.document_hardcoded_type_name,
            filename_pattern
        )

        self.init_document_type()

    def fill_empty_prebuilt_fields(self) -> None:
        '''
        Overwrites the method from Document class.

        It fills the empty prebuilt fields and fills them
        with defaults already with the help of the method
        self.generate_default_fields_dict()
        '''
        self.data_prebuilt = self.generate_default_fields_dict('defaults')

    def from_dict(self, values: dict) -> None:
        '''
        Fill the objects attributes / data from the given dict.
        This overwrites the Document from_dict() method, which
        also have the from_dict_document_type() method in use.
        Yet for the client I need the hard coded DocumentType
        and thus does not want it be searched in the document
        types folder, since it should not exist there.

        Args:
            values (dict): The dict values to fill the object.
        '''
        self._from_dict_base(values)
        self._from_dict_data(values)

    def generate_default_fields_dict(self, what: str = '') -> dict:
        '''
        Getting or generating the default fields dict. It can
        be the fieldnames with its types, the fieldnames with
        its defautl values or even the plain default_fields
        constant of this class (as a fallback).

        Args:
            what (str): \
                Choose from `'types'`, `'defaults'` or aynthing \
                else to get the default_fields constant.

        Returns:
            dict: Returns the wanted dict.
        '''
        # initialize cache variables so that the for loop
        # will only have to run once.
        if (
            not self.default_fields_types
            or not self.default_fields_defaults
        ):
            self.default_fields_types = {}
            self.default_fields_defaults = {}
            for fieldname in self.default_fields:
                types = self.default_fields[fieldname][0]
                defaults = self.default_fields[fieldname][1]
                self.default_fields_types[fieldname] = types
                self.default_fields_defaults[fieldname] = defaults

        # simply access the data from here on
        if what == 'types':
            return self.default_fields_types
        elif what == 'defaults':
            return self.default_fields_defaults
        else:
            return self.default_fields

    def init_document_type(self) -> None:
        '''
        Initialize the document type. The class gets
        inherited from the Document class and with this
        method I want to define a hard coded DocumentType
        for just this client class.
        '''
        # since this DocumentType is somehow hard-coded,
        # I cannot define the name on init, since the
        # DocumentType init method would try to automatically
        # load the DocumentType. in that process it would
        # set the default folder to './' and somehow overwrite
        # my set folder here
        # TODO: Not sure, if this is a sign of quite bad
        #       coding practice, oh boy ...
        doc_type = DocumentType(
            '',
            self.document_hardcoded_folder,
            self.document_hardcoded_filename_pattern
        )
        doc_type.name = self.document_hardcoded_type_name
        doc_type.set(
            'prebuilt_fields',
            self.generate_default_fields_dict('types')
        )
        self.document_type = doc_type

        # also set the folder for the repository. this method
        # otherwise would be executed in the set_document_type()
        # method of the Document class, yet this method also
        # loads the DocumentType by name. And here in this
        # Client class I need the hard coded document type.
        self.repository.set_folder(
            self.document_type.get('document_folder')
        )
        # same for filename_pattern
        self.repository.set_filename_pattern(
            self.document_type.get('document_filename_pattern')
        )
