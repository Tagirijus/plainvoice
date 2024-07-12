from plainvoice.model.base import Base


class Client(Base):
    """
    The client class, which holds client data.
    """

    def __init__(
        self,
        client_id: str = '',
        receiver: str = '',
        default_currency: str = '€',
        enabled: bool = True,
    ):
        """
        A client, which holds certain client data

        Args:
            client_id (str): The client id. (default: `''`)
            receiver (str): The receiver string in multiline. (default: `''`)
            default_currency (str): The currecny character. (default: `'€'`)
            enabled (bool): Set the client to active. (default: `True`)
        """
        self.client_id: str = client_id
        """
        The clients id. It should be set before saving, since it is used
        for the filename as well. Also it should not double another
        clients client_id.
        """

        self.receiver: str = ''
        """
        The multiline for the receiver. This can be used on the invoice
        or document during rendering later, for example.
        """

        self.default_currency: str = '€'
        """
        The default currecny, which should be used for new invoices
        for the client.
        """

        self.enabled: bool = True
        """
        Boolean if the client is enabled and thus e.g. should be
        shown later in the TUI of this programm or not. E.g. in a
        list where you can choose from clients at any point.
        """

    def disable(self) -> None:
        """
        Disables the client. It basically just changes the self.enabled
        attribute to False.
        """
        self.enabled = False

    def enable(self) -> None:
        """
        Enables the client. It basically just changes the self.enabled
        attribute to True.
        """
        self.enabled = True

    def from_dict(self, values: dict = {}) -> None:
        """
        Sets the class attributes from the given dict.

        Args:
            values (dict): \
                The dict containing all the data for the class \
                attributes to be filled. (default: `{}`)
        """
        self.client_id = values.get('client_id', '')
        self.receiver = values.get('receiver', '')
        self.default_currency = values.get('default_currency', '€')
        self.enabled = values.get('enabled', True)
