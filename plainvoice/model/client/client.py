'''
Client Class

This class is for storing client data and maybe linking documents
to them. Internally it basically is just a Document, yet with some
kind of hard-coded DocumentType by inheritting from DocumentHardcodeType.
Inside it. The idea is to have one kind of 'document', which can be
linked to other documents: clients have invoices or quotes, for example.
Maybe at some point (if not already there) it will be possible to link
documents between each other. Yet I wanted to have some more restrict
logic here: clients and all their linked documents, which belong to them.
'''


from plainvoice.model.config import Config
from plainvoice.model.document.document_hardcode_type import \
    DocumentHardcodeType


class Client(DocumentHardcodeType):
    '''
    This class holds information about the client.
    '''

    def __init__(self, client_id: str = ''):
        '''
        This class is for clients data. It is supposed to be able
        to link to certain documents for the clients.

        Args:
            client_id (str): \
                The client id. (default: defined by the \
                method for finding the next id.)
        '''
        super().__init__(
            client_id,
            'client',
            Config().client_filename_pattern,
            Config().client_folder
        )

        self.default_fields = {
            'company': ('str', ''),
            'attention': ('str', 'Attn.'),
            'salutation': ('str', 'Mr.'),
            'first_name': ('str', ''),
            'last_name': ('str', ''),
            'street': ('str', ''),
            'post_code': ('str', ''),
            'country': ('str', ''),
            'city': ('str', ''),
            'language': ('str', '')
        }

        if client_id == '':
            client_id = self.get_next_code()

        # name and id of the object is the same
        # for client objects
        self.code = client_id
        self.name = client_id
        self.load_from_name(self.name)

    def __str__(self) -> str:
        '''
        Represent this class as a string.

        Returns:
            srt: The readable string.
        '''
        client_id = self.code
        first = self.data_prebuilt['first_name']
        last = self.data_prebuilt['last_name']
        return f'{client_id}: {first} {last}'
