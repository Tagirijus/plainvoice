'''
DocumentType Class

This class is for describing a Document class. The idea is that the user should
be able to create own document types later and the Document class can be more
flexible that way. With this class the user can describe the fixed fields or
a DataModel object. Also this object holds the information about where such
documents are being stored (e.g. folder).
'''

from plainvoice.model.data.data_model import DataModel


class DocumentType(DataModel):
    '''
    This class can describe a document and it's needed
    data fields and where it is stored etc.
    '''

    def __init__(self, folder: str = '', filename_pattern: str = ''):
        '''
        This class can describe a document and it's needed
        data fields and where it is stored etc.

        Args:
            folder (str): \
                The folder to store the document type to. '{app_dir}' inside \
                the string can be used, which will be replaced with the \
                programs root data dir. So use '{app_dir}/invoices', for \
                example, so that the 'invoices' folder inside the programs \
                data dir will be used. Leave empty, so that the folder will \
                be the working dirs folder form which the program was started.\
                (default: `None`)
            filename_pattern (str): \
                The filename pattern for the document, which is used to \
                get filenam eetxractions and geenrating new ids and \
                names for the document.

        '''
        super().__init__()
        self._init_fixed_fields()
        self.set_fixed('folder', folder, True)
        self.set_fixed('filename_pattern', filename_pattern, True)

    def add_fixed_field(self, name: str, typename: str, default: object) -> None:
        '''
        Add a fixed field to the document type.

        Args:
            name (str): \
                Name of the field. In the saved YAML later this \
                would be the key of the stored data.
            typename (str): \
                Name of the field type. This should be the type name \
                string, which will be defined in the document class \
                with define_fixed_field_type() later. Not in this \
                class, though! More types will be defined in the \
                document class, which will be the main class for \
                documents, thus having all possible field types.
            default (object): \
                Any kind of default, which should represent the \
                readable default later. So it should be a basic \
                Python object like str, int, float, list or dict.
        '''
        self.get_fixed('fixed_fields', False)[name] = {
            'type': typename,
            'default': default,
        }

    def get_descriptor(self) -> dict:
        '''
        Get teh descriptor to be used as a descriptor for the
        document class fixed fields then.

        Returns:
            dict: Returns the descriptor dict.
        '''
        return self.get_fixed('fixed_fields', False)

    def get_filename_pattern(self) -> str:
        '''
        Get the filename pattern of the document type.

        Returns:
            str: Returns the filename pattern as a string.
        '''
        return self.get_fixed('filename_pattern', False)

    def get_folder(self) -> str:
        '''
        Get the folder of the document type.

        Returns:
            str: Returns the folder as a string.
        '''
        return self.get_fixed('folder', False)

    def _init_fixed_fields(self) -> None:
        '''
        Initialize the fixed fields for this special DataModel child.
        '''
        self.define_fixed_field_type('str', str, str)
        self.define_fixed_field_type('dict', dict, dict)
        self.define_fixed_field_type('list', list, list)

        self.add_field_descriptor('folder', 'str', '')
        self.add_field_descriptor('filename_pattern', 'str', '')
        self.add_field_descriptor('date_issued_fieldname', 'str', '')
        self.add_field_descriptor('date_due_fieldname', 'str', '')
        self.add_field_descriptor('date_done_fieldname', 'str', '')
        self.add_field_descriptor('title_fieldname', 'list', [])
        self.add_field_descriptor('code_fieldname', 'str', '')
        self.add_field_descriptor('fixed_fields', 'dict', {})

    def __str__(self) -> str:
        '''
        Represent this class as a string with its name.

        Returns:
            srt: The readable name string.
        '''
        folder = self.get_fixed('folder', True)
        filename_pattern = self.get_fixed('filename_pattern', True)
        return f'{folder}: {filename_pattern}'
