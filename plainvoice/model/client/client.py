'''
Client Class

This class is for storing client data and maybe linking documents
to them. Technically it inherits from the DataModel and it has
basically "hard-coded" fixed fields straight ahead.
'''


from plainvoice.model.data.data_model import DataModel


class Client(DataModel):
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
        super().__init__()
        self._init_fixed_fields()

        self.client_id = client_id
        '''
        The id for the client. Can be anything the user wants.
        '''

    def _init_fixed_fields(self) -> None:
        '''
        Initialize the fixed fields for this special DataModel child.
        '''
        self.define_fixed_field_type('str', str, str)
        self.add_field_descriptor('company', 'str', '')
        self.add_field_descriptor('attention', 'str', 'Attn.')
        self.add_field_descriptor('salutation', 'str', 'Mr.')
        self.add_field_descriptor('first_name', 'str', '')
        self.add_field_descriptor('last_name', 'str', '')
        self.add_field_descriptor('street', 'str', '')
        self.add_field_descriptor('post_code', 'str', '')
        self.add_field_descriptor('country', 'str', '')
        self.add_field_descriptor('city', 'str', '')
        self.add_field_descriptor('language', 'str', '')

    def get_client_id(self) -> str:
        '''
        Get the client id.

        Returns:
            str: Returns the client id as a string.
        '''
        return self.client_id

    def set_client_id(self, client_id: str) -> None:
        '''
        Set the client id, which can be any string.

        Args:
            client_id (str): The client id.
        '''
        self.client_id = client_id

    def __str__(self) -> str:
        '''
        Represent this class as a string.

        Returns:
            srt: The readable string.
        '''
        client_id = self.get_client_id()
        first = self.get_fixed('first_name')
        last = self.get_fixed('last_name')
        return f'{client_id}: {first} {last}'
