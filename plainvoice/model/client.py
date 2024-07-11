from plainvoice.model.base import Base


class Client(Base):
    """
    The client class, which holds client data.
    """

    client_id: str
    """
    The clients id.
    """

    receiver: str
    """
    Multiline for the receiver.
    """

    default_currency: str
    """
    The default currecny, which should be used for new invoices
    for the client.
    """

    enabled: bool
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
