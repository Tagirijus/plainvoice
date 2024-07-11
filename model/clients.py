from model.base import Base


class Clients(Base):
    """
    The client class, which holds client data.
    """

    client_id: str
    """
    The clients id.
    """

    company: str
    """
    The company name of the client.
    """

    tax_id: str
    """
    The tax id of the client.
    """

    attention: str
    """
    The attention used on the invoice / quote for the client, if needed.
    """

    salutation: str
    """
    The salutation used on the invoice / quote for the client.
    """

    first_name: str
    """
    The clients first name.
    """

    last_name: str
    """
    The clients last name.
    """

    street: str
    """
    The clients street. Should contain the house number as well.
    """

    city: str
    """
    The clients city.
    """

    postcode: str
    """
    The clients postcode.
    """

    country: str
    """
    The country the client lives in.
    """

    default_currency: str
    """
    The default currecny, which should be used for new invoices
    for the client.
    """

    language: str
    """
    The language of the client. Could be used inside the jinja2
    template or so. Maybe even in this programm. I'd recommend to
    stick to the short country codes like "de" for german or
    "en" for english.
    """

    def __init__(self):
        super(Clients, self).__init__()
        self.FOLDER = 'clients/'
        self.EXTENSION = 'yaml'

    def generate_name(self) -> str:
        """
        This method overwrites the default Base method and is
        for generating a pattern for the filename without
        the path or the extension, based on the data types
        variables.

        Returns:
            str: Returns the name as a string.
        """
        return self.client_id

    def generate_receiver(self) -> str:
        """
        With this method a multiline receiver string to put
        on the invoice / quote can be generated. I chose to
        do it this way, since this also will be stored in the
        YAML file of the invoice plainly. This way the receiver
        or the client is better readable, in my opinion.

        Returns:
            str: The string containing the clients data as a receiver.
        """
        out = ''
        salute = ''

        if self.company != '':
            salute += f'{self.company}'
            salute += f'\n{self.attention} '

        if self.salutation != '':
            salute += f'{self.salutation} '

        out += f'{salute}{self.first_name} {self.last_name}'
        out += f'\n{self.street}'
        out += f'\n{self.postcode} {self.city}'

        if self.country != '':
            out += f'\n{self.country}'

        return out.strip()

    def get_as_dict(self) -> dict:
        """
        Get the class attributes as a dict.

        Returns:
            dict: The dict with all the attributes.
        """
        return {
            'client_id': self.client_id,

            'company': self.company,
            'tax_id': self.tax_id,

            'attention': self.attention,
            'salutation': self.salutation,
            'first_name': self.first_name,
            'last_name': self.last_name,

            'street': self.street,
            'city': self.city,
            'postcode': self.postcode,
            'country': self.country,

            'default_currency': self.default_currency,

            'language': self.language
        }

    def load_by_id(self, client_id: str) -> None:
        """
        This method will load the internal attributes from a
        client file by its client_id.

        TODO:
            - code it! ...

        Args:
            client_id (str): The client id as a string.
        """
        pass

    def set_from_dict(self, values: dict = {}) -> None:
        """
        Sets the class attributes from the given dict.

        Args:
            values (dict): \
                The dict containing all the data for the class \
                attributes to be filled. (default: `{}`)
        """
        self.client_id = values.get('client_id', '')

        self.company = values.get('company', '')
        self.tax_id = values.get('tax_id', '')

        self.attention = values.get('attention', 'Attn.')
        self.salutation = values.get('salutation', '')
        self.first_name = values.get('first_name', '')
        self.last_name = values.get('last_name', '')

        self.street = values.get('street', '')
        self.city = values.get('city', '')
        self.postcode = values.get('postcode', '')
        self.country = values.get('country', '')

        self.default_currency = values.get('default_currency', '€')

        self.language = values.get('language', 'en')
